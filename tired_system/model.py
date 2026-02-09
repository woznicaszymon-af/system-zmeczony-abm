from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional
import numpy as np
import networkx as nx
import mesa
from mesa.datacollection import DataCollector

from .agents import VassalAgent, LordAgent, VassalParams
from .metrics import clip01, safe_mean, safe_corr, gini, logistic, EndState


@dataclass(frozen=True)
class ModelParams:
    # populacja / sieć
    n_vassals: int = 250
    n_lords: int = 12
    peer_k: int = 6
    peer_rewire_p: float = 0.05

    # parametry makro (0..1)
    I_work: float = 0.6
    A_affect: float = 0.5
    R_power: float = 0.6
    C_conflict: float = 0.6
    G_regen: float = 0.6

    # wagi / dynamika (0..1)
    alpha: float = 0.22
    beta: float = 0.12
    kappa: float = 0.18
    gamma: float = 0.22
    delta: float = 0.12
    eta: float = 0.20
    mu: float = 0.20
    nu: float = 0.16
    rho: float = 0.08
    sigma: float = 0.16
    tau: float = 0.12

    # progi końcowe
    TH_reform: float = 0.65
    TH_exit: float = 0.35
    e_min: float = 0.20
    s_min: float = 0.20

    # skale techniczne
    max_steps: int = 400
    access_scale: int = 10
    visibility_weight: float = 0.25

    regen_base: float = 0.18
    regen_work_penalty: float = 0.07

    overload_threshold: float = 1.10
    overload_scale: float = 0.10

    # rozstrzygnięcie konfliktu (probabilistycznie)
    rp_threshold: float = 0.35
    rp_scale: float = 0.10

    # selekcja access
    w_loy: float = 1.40
    w_cent: float = 0.60
    w_perf: float = 1.00

    # seed
    seed: Optional[int] = 42


class TiredSystemModel(mesa.Model):
    """
    ABM „System zmęczony”: dryf / reforma / rozpad.
    Mesa 3.x: aktywacja przez AgentSet, ale logika kroków jest sterowana centralnie.
    """

    def __init__(self, params: ModelParams):
        super().__init__(seed=params.seed)
        self.p = params
        self.rng = np.random.default_rng(params.seed)

        self.step_count = 0
        self.running = True
        self.status = "running"  # running | reform | collapse | max_steps
        self.resolution_event_last = False

        # sieci
        self.peer_graph = self._build_peer_graph(params.n_vassals, params.peer_k, params.peer_rewire_p)
        self.patron_map: Dict[str, str] = {}  # vassal_node -> lord_node
        self.full_graph = nx.Graph()

        # agenci
        self.vassals: List[VassalAgent] = []
        self.lords: List[LordAgent] = []

        self._init_agents_and_graph()

        # centralności (używane w workload i selekcji access)
        self.centrality = nx.degree_centrality(self.full_graph)

        # data collector
        self.datacollector = DataCollector(
            model_reporters={
                "status": lambda m: m.status,
                "resolution_event": lambda m: m.resolution_event_last,
                "A_t": lambda m: m._A_t,
                "collective_regen": lambda m: m._collective_regen,
                "ConflictIntensity": lambda m: m._conflict_intensity,
                "ResolutionPotential": lambda m: m._resolution_potential,
                "mean_E": lambda m: m._mean("E"),
                "mean_F": lambda m: m._mean("F"),
                "mean_Sense": lambda m: m._mean("Sense"),
                "mean_Out": lambda m: m._mean("Out"),
                "mean_Fear": lambda m: m._mean("Fear"),
                "mean_Loy": lambda m: m._mean("Loy"),
                "mean_Coord": lambda m: m._mean("Coord"),
                "gini_F": lambda m: gini([a.F for a in m.vassals]),
                "gini_access": lambda m: gini([a.access_received for a in m.vassals]),
                "corr_access_loy": lambda m: safe_corr(
                    [a.access_received for a in m.vassals],
                    [a.Loy for a in m.vassals],
                ),
                "exit_share": lambda m: m._exit_share(),
            },
            agent_reporters={
                "type": lambda a: a.__class__.__name__,
                "node_id": lambda a: getattr(a, "node_id", ""),
                "E": lambda a: getattr(a, "E", np.nan),
                "F": lambda a: getattr(a, "F", np.nan),
                "Sense": lambda a: getattr(a, "Sense", np.nan),
                "Out": lambda a: getattr(a, "Out", np.nan),
                "Fear": lambda a: getattr(a, "Fear", np.nan),
                "Coord": lambda a: getattr(a, "Coord", np.nan),
                "Loy": lambda a: getattr(a, "Loy", np.nan),
                "access_received": lambda a: getattr(a, "access_received", np.nan),
            },
        )

        # inicjalne wartości „globalne”
        self._A_t = 0.0
        self._collective_regen = 0.0
        self._conflict_intensity = 0.0
        self._resolution_potential = 0.0

        # zbierz t=0
        self.datacollector.collect(self)

    def _build_peer_graph(self, n: int, k: int, p: float) -> nx.Graph:
        k = int(max(2, min(k, n - 1)))
        if k % 2 == 1:
            k += 1
        if n < 4:
            return nx.complete_graph(n)
        return nx.watts_strogatz_graph(n=n, k=k, p=float(np.clip(p, 0.0, 1.0)), seed=self.p.seed)

    def _init_agents_and_graph(self) -> None:
        # 1) dodaj węzły lordów
        for j in range(self.p.n_lords):
            node = f"L{j}"
            self.full_graph.add_node(node)

        # 2) dodaj węzły wasali (mapowanie indeksów peer_graph -> V*)
        for i in range(self.p.n_vassals):
            self.full_graph.add_node(f"V{i}")

        # 3) krawędzie peer (tylko między wasalami)
        for u, v in self.peer_graph.edges():
            self.full_graph.add_edge(f"V{u}", f"V{v}", kind="peer")

        # 4) patronaż: każdy wasal dostaje lorda (losowo, ale można podmienić na regułę)
        for i in range(self.p.n_vassals):
            lord = f"L{int(self.rng.integers(0, self.p.n_lords))}"
            v = f"V{i}"
            self.patron_map[v] = lord
            self.full_graph.add_edge(v, lord, kind="patronage")

        # 5) utwórz agentów
        vp = VassalParams(
            alpha=self.p.alpha, beta=self.p.beta, kappa=self.p.kappa,
            gamma=self.p.gamma, delta=self.p.delta, eta=self.p.eta,
            mu=self.p.mu, nu=self.p.nu,
            rho=self.p.rho, sigma=self.p.sigma, tau=self.p.tau
        )

        # lords
        for j in range(self.p.n_lords):
            node = f"L{j}"
            lord = LordAgent(
                self,
                node_id=node,
                Access=float(self.rng.uniform(0.45, 0.90)),
                Cap=float(self.rng.uniform(0.40, 0.90)),
                Doxa=float(self.rng.uniform(0.30, 0.80)),
                Buffer=float(self.rng.uniform(0.30, 0.85)),
            )
            self.lords.append(lord)

        # vassals
        for i in range(self.p.n_vassals):
            node = f"V{i}"
            patron = self.patron_map[node]
            base_workload = float(self.rng.uniform(0.50, 0.90))
            exit_option = float(self.rng.uniform(0.05, 0.80))
            vassal = VassalAgent(
                self,
                node_id=node,
                patron_id=patron,
                base_workload=base_workload,
                exit_option=exit_option,
                p=vp,
            )
            self.vassals.append(vassal)

    # --- pomocnicze agregaty ---
    def _mean(self, attr: str) -> float:
        return float(np.mean([getattr(a, attr) for a in self.vassals]))

    def _exit_share(self) -> float:
        e_min, s_min = self.p.e_min, self.p.s_min
        bad = sum(1 for a in self.vassals if (a.E < e_min and a.Sense < s_min))
        return float(bad / max(1, len(self.vassals)))

    def _compute_collective_regen(self) -> float:
        """
        Regeneracja zbiorowa = funkcja sieci wsparcia * (1 - G_regen).
        Tu: lokalne wsparcie ~ średnia z (1-F)*(1-Fear) u sąsiadów peer.
        """
        G_regen = self.p.G_regen
        support_vals = []
        for i, a in enumerate(self.vassals):
            # peer neighbors w peer_graph
            neigh_idx = list(self.peer_graph.neighbors(i))
            if not neigh_idx:
                support_vals.append(0.0)
                continue
            neigh = [self.vassals[j] for j in neigh_idx]
            local_support = np.mean([(1.0 - n.F) * (1.0 - n.Fear) for n in neigh])
            support_vals.append(float(np.clip(local_support, 0.0, 1.0)))

        base = float(np.mean(support_vals)) if support_vals else 0.0
        return float(np.clip(base * (1.0 - G_regen), 0.0, 1.0))

    def _draw_affect_shock(self) -> float:
        """
        A(t) zależne od A_affect z szumem: większe A_affect -> częściej mocne bodźce.
        """
        base = self.p.A_affect
        # mieszanka: zwykły szum + rzadkie „szoki”
        normal = float(self.rng.normal(loc=base, scale=0.10))
        shock = float(self.rng.uniform(0.0, 1.0)) if self.rng.random() < (0.10 + 0.25 * base) else 0.0
        A_t = 0.75 * normal + 0.25 * shock
        return float(np.clip(A_t, 0.0, 1.0))

    def _allocate_access(self) -> None:
        """
        Krok 5.1–5.3: lords przydzielają access wasalom (patronage edges).
        """
        # wyczyść poprzedni krok
        for a in self.vassals:
            a.access_received = 0.0

        # przygotuj listy wasali per lord
        by_lord: Dict[str, List[VassalAgent]] = {lord.node_id: [] for lord in self.lords}
        for a in self.vassals:
            by_lord[a.patron_id].append(a)

        for lord in self.lords:
            candidates = by_lord.get(lord.node_id, [])
            if not candidates:
                continue

            budget = max(1, int(round(lord.Access * self.p.access_scale)))

            # scoring: Loy + centrality + performance
            scores = []
            for a in candidates:
                cent = float(self.centrality.get(a.node_id, 0.0))
                s = (
                    self.p.w_loy * a.Loy +
                    self.p.w_cent * cent +
                    self.p.w_perf * a.performance +
                    0.10 * lord.Doxa
                )
                scores.append(float(s))

            scores = np.array(scores, dtype=float)
            # softmax
            scores = scores - scores.max()
            weights = np.exp(scores)
            weights = weights / weights.sum() if weights.sum() > 0 else np.ones_like(weights) / len(weights)

            chosen_idx = self.rng.choice(len(candidates), size=min(budget, len(candidates)), replace=False, p=weights)
            for idx in chosen_idx:
                candidates[int(idx)].access_received = 1.0

    def _compute_conflict_and_resolution(self) -> Tuple[float, float, bool]:
        """
        Krok 6: konflikt bez rozstrzygnięcia.
        ConflictIntensity = mean(Out) * C_conflict
        ResolutionPotential = f(mean(Coord), (1 - R_power), spójność sieci)
        """
        conflict_intensity = float(self._mean("Out") * self.p.C_conflict)

        # spójność sieci wsparcia: udział największej składowej w peer_graph
        comps = list(nx.connected_components(self.peer_graph))
        if comps:
            giant = max(len(c) for c in comps) / self.p.n_vassals
        else:
            giant = 0.0

        cohesion = float(np.clip(giant, 0.0, 1.0))
        resolution_potential = float(np.clip(self._mean("Coord") * (1.0 - self.p.R_power) * (0.5 + 0.5 * cohesion), 0.0, 1.0))

        # prawdopodobieństwo rozstrzygnięcia: logistyczne wokół rp_threshold
        z = (resolution_potential - self.p.rp_threshold) / max(1e-6, self.p.rp_scale)
        p_res = logistic(z)
        resolution_event = bool(self.rng.random() < p_res)

        return conflict_intensity, resolution_potential, resolution_event

    def step(self) -> EndState:
        if not self.running:
            return EndState(self.status, self.step_count, self.resolution_event_last, self._mean("Coord"), self._exit_share())

        self.step_count += 1

        # (7.2) collective_regen(t)
        self._collective_regen = self._compute_collective_regen()

        # (1) bodziec afektywny A(t)
        self._A_t = self._draw_affect_shock()

        # (2–4) aktualizacja wasali
        for a in self.vassals:
            cent = float(self.centrality.get(a.node_id, 0.0))
            a.update_core_states(
                A_t=self._A_t,
                I_work=self.p.I_work,
                collective_regen=self._collective_regen,
                G_regen=self.p.G_regen,
                visibility_weight=self.p.visibility_weight,
                centrality=cent,
                regen_base=self.p.regen_base,
                regen_work_penalty=self.p.regen_work_penalty,
                overload_threshold=self.p.overload_threshold,
                overload_scale=self.p.overload_scale,
            )

        # (5) lords przydzielają access
        self._allocate_access()

        # (5.4) lojalność po access
        for a in self.vassals:
            a.update_loyalty_after_access()

        # (6) konflikt i rozstrzygnięcie
        self._conflict_intensity, self._resolution_potential, self.resolution_event_last = self._compute_conflict_and_resolution()

        # (8) warunki końcowe
        mean_coord = self._mean("Coord")
        exit_share = self._exit_share()

        if (mean_coord > self.p.TH_reform) and self.resolution_event_last:
            self.status = "reform"
            self.running = False
        elif exit_share > self.p.TH_exit:
            self.status = "collapse"
            self.running = False
        elif self.step_count >= self.p.max_steps:
            self.status = "max_steps"
            self.running = False

        self.datacollector.collect(self)

        return EndState(self.status, self.step_count, self.resolution_event_last, mean_coord, exit_share)

    def run(self) -> EndState:
        state = EndState(self.status, self.step_count, self.resolution_event_last, self._mean("Coord"), self._exit_share())
        while self.running:
            state = self.step()
        return state

    # --- eksport danych ---
    def get_model_df(self):
        return self.datacollector.get_model_vars_dataframe()

    def get_agent_df(self):
        return self.datacollector.get_agent_vars_dataframe()

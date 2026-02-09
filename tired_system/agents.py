from __future__ import annotations

from dataclasses import dataclass
import numpy as np
import mesa

from .metrics import clip01


@dataclass
class VassalParams:
    # koszty / wagi
    alpha: float
    beta: float
    kappa: float
    gamma: float
    delta: float
    eta: float
    mu: float
    nu: float
    rho: float
    sigma: float
    tau: float


class VassalAgent(mesa.Agent):
    """
    Wasal: E, F, Sense, Out, Fear, Coord, Loy.
    Logika update'ów jest zorkiestrowana przez model (stage'owanie),
    ale agent przechowuje stan i policzone w kroku zmienne pośrednie.
    """

    def __init__(
        self,
        model: mesa.Model,
        node_id: str,
        patron_id: str,
        base_workload: float,
        exit_option: float,
        p: VassalParams,
    ):
        super().__init__(model)
        self.node_id = node_id
        self.patron_id = patron_id

        # heterogeniczność
        self.base_workload = float(base_workload)     # bazowe obciążenie
        self.exit_option = float(exit_option)         # "alternatywa wyjścia" 0..1

        # stan (0..1)
        rng = model.rng
        self.E = float(rng.uniform(0.55, 0.80))
        self.F = float(rng.uniform(0.10, 0.35))
        self.Sense = float(rng.uniform(0.55, 0.85))
        self.Out = float(rng.uniform(0.20, 0.50))
        self.Fear = float(rng.uniform(0.20, 0.50))
        self.Coord = float(rng.uniform(0.20, 0.55))
        self.Loy = float(rng.uniform(0.20, 0.55))

        # bookkeeping
        self.access_received = 0.0
        self.workload_last = 0.0
        self.regen_last = 0.0
        self.performance = 0.0  # proxy do selekcji: (E + Sense - F)/2

        self.p = p

    def compute_workload(self, I_work: float, visibility_weight: float, centrality: float) -> float:
        # koszt widzialności: rośnie wraz z lojalnością i centralnością (status = praca)
        visibility_cost = visibility_weight * (0.6 * self.Loy + 0.4 * centrality)
        noise = float(self.model.rng.normal(0.0, 0.10))
        workload = self.base_workload + I_work * (0.5 + noise) + visibility_cost + 0.10 * self.access_received
        return float(np.clip(workload, 0.0, 2.0))

    def compute_risk_exclusion(self) -> float:
        # ryzyko wykluczenia rośnie, gdy:
        # - niska lojalność
        # - brak dostępu (access_received ~ 0)
        # - słaba alternatywa wyjścia (exit_option niskie)
        lack_access = 1.0 - float(np.clip(self.access_received, 0.0, 1.0))
        lack_exit = 1.0 - self.exit_option
        risk = 0.25 * (1.0 - self.Loy) + 0.25 * lack_access + 0.20 * lack_exit
        return clip01(risk)

    def update_core_states(
        self,
        A_t: float,
        I_work: float,
        collective_regen: float,
        G_regen: float,
        visibility_weight: float,
        centrality: float,
        regen_base: float,
        regen_work_penalty: float,
        overload_threshold: float,
        overload_scale: float,
    ) -> None:
        """
        Kroki 2–4 + 7 (częściowo): energia, sens, afekt, zmęczenie, koordynacja.
        """
        p = self.p

        # (2) obciążenie
        workload = self.compute_workload(I_work, visibility_weight, centrality)
        self.workload_last = workload

        # (7.1) prywatna regeneracja energetyczna (częściowo zneutralizowana)
        # im większe G_regen, tym większa "kara" (odpoczynek tylko jako powrót do mobilizacji)
        private_rest = max(0.0, regen_base - regen_work_penalty * workload)
        penalty = G_regen * 0.6 * private_rest
        regen_i = max(0.0, private_rest - penalty)
        self.regen_last = regen_i

        # (2.2) energia
        self.E = clip01(self.E - p.alpha * workload + regen_i)

        # (2.3) sens
        self.Sense = clip01(self.Sense - p.beta * workload)

        # (3) afekt jako paliwo
        self.Out = clip01(self.Out + p.gamma * A_t - p.delta * self.F)
        risk_excl = self.compute_risk_exclusion()
        self.Fear = clip01(self.Fear + p.eta * A_t + risk_excl)

        # (4.1) zmęczenie
        overload = max(0.0, workload - overload_threshold)
        overload_shock = overload_scale * overload
        self.F = clip01(self.F + p.kappa * (1.0 - self.E) + overload_shock)

        # (4.2) koordynacja: tłumiona przez zmęczenie, wzmacniana przez regenerację zbiorową
        # kolektywna regeneracja jest też tłumiona przez G_regen (robi to model)
        self.Coord = clip01(self.Coord - p.mu * self.F + p.nu * collective_regen)

        # proxy "performance"
        self.performance = clip01(0.5 * (self.E + self.Sense) - 0.5 * self.F)

    def update_loyalty_after_access(self) -> None:
        """
        Krok 5.4: lojalność po przydziale access.
        """
        p = self.p
        got = 1.0 if self.access_received > 0.0 else 0.0

        if got > 0.0:
            self.Loy = clip01(self.Loy + p.rho * got + p.sigma * self.Fear - p.tau * (1.0 - self.Sense))
        else:
            self.Loy = clip01(self.Loy + p.sigma * self.Fear - p.tau * (1.0 - self.Sense))

        # koszt dyspozycyjności: lojalność zużywa energię (autoeksploatacja)
        self.E = clip01(self.E - 0.05 * self.Loy)

    def step(self) -> None:
        # Model steruje etapami — tu zostawiamy puste, by nie dublować logiki.
        return


class LordAgent(mesa.Agent):
    """
    Lord: przydziela access wasalom (gatekeeping).
    """

    def __init__(self, model: mesa.Model, node_id: str, Access: float, Cap: float, Doxa: float, Buffer: float):
        super().__init__(model)
        self.node_id = node_id
        self.Access = float(np.clip(Access, 0.0, 1.0))
        self.Cap = float(np.clip(Cap, 0.0, 1.0))
        self.Doxa = float(np.clip(Doxa, 0.0, 1.0))
        self.Buffer = float(np.clip(Buffer, 0.0, 1.0))

    def step(self) -> None:
        return

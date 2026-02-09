# Calibration (how to “set” the model’s trajectories)

In this ABM, “calibration” does **not** mean fitting to empirical data. It means tuning the mechanism so that the model enters recognizable dynamic regimes: **drift**, **breakthrough** (reform/resolution), or **exit/collapse**. In this construction, breakthroughs are formally defined by thresholds and terminal events (e.g., reform: `mean(Coord) > TH_reform` plus the occurrence of a “resolution”; collapse: crossing `TH_exit` by the share of agents with low `E` and `Sense`).

---

## 1) Levers (what controls what)

The following “knobs” matter most, because each trajectory is a different relationship between energy/fatigue, affect, coordination, power redundancy, and regeneration:

- **Fatigue production:** `I_work` (busyness inflation) + cost weights `α`, `β` (energy and meaning) + accumulation `κ`.
- **Agency blockade:** the impact of fatigue on coordination `μ` and the “rescue” via collective regeneration `ν * collective_regen(t)`, which is damped by `G_regen`.
- **Affect as fuel (reactivity):** `A_affect` + weights `γ`, `η` (arousal/fear).
- **Conflict without resolution:** `C_conflict` increases dispute intensity, while `R_power` lowers the chances of “closing” the conflict via redundancy.
- **Affective feudalism (lock-in):** `Access → Loy` (access allocation + loyalty update via `ρ`, `σ`, `τ`) stabilizes dependency even under erosion of meaning.

**General rule:**
- if you want **drift**, keep conflict and busyness high, coordination low, and do not allow regeneration to build agency;
- if you want **reform**, loosen the coordination blockades and reduce redundancy that captures/neutralizes conflict;
- if you want **collapse**, drive energy and meaning downward faster than the system can “amortize” it via access/loyalty.

---

## 2) Quick tuning procedure (7 steps)

1. **Set the baseline:** average initial states (`E`, `Sense`, `F`) and the “noise” in loads.
2. **Block the two breakthroughs at the start:** set thresholds so that, under baseline, neither reform nor exit occurs in the first ~10–20% of the horizon (otherwise the model becomes “trivial”).
3. **Choose a target** (drift / reform / collapse) and tune only **2–3 knobs at a time**.
4. **First tune the system’s energetics** (`I_work`, `α`, `κ`, `β`), only then tune affect (`A_affect`, `γ`, `η`).
5. **Only at the end tune the breakthrough politics** (`R_power`, `C_conflict`, `G_regen`, `μ`, `ν`) — because this determines whether conflict “dies out”, “drifts”, or closes.
6. **Check regime stability:** does the outcome persist under small changes (e.g., ±10%) of one parameter?
7. **Define the regime signature:** write down 3–4 indicators that always look the same in that regime (see below).

---

## 3) Three ready-made calibration sets (heuristics)

Below are three “recipes” — not as the only values, but as directions that, in your logic, should generate the corresponding dynamics (because they directly strengthen or weaken the conditions from Steps 6–8 of the pseudocode: conflict, resolution potential, regeneration, and terminal thresholds).

### A) Regime: DRIFT (persistence / conflict idling)

**Goal:** high conflict and high busyness, but no coordination and no exit.

- **High:** `I_work`, `C_conflict`, `R_power`, `G_regen` (neutralizing agentic regeneration).
- **Moderate–high:** `A_affect` (enough fuel for reactivity), but not so high that it drives energy down too fast.
- **Weights:** `μ` rather high (fatigue strongly suppresses coordination), `ν` low (collective regeneration weak), `σ` high (fear “sticks” loyalty), `ρ` moderate (access as a carrot).
- **Thresholds:** raise `TH_reform` (so it doesn’t “jump” into reform), and either raise `TH_exit` or lower `e_min/s_min` (so the system can persist despite low meaning).

**Regime signature (what you’ll see in outputs):**
- `mean(Out)` and `ConflictIntensity` high, but `mean(Coord)` stays below `TH_reform`;
- `mean(F)` rises and plateaus high; `mean(Sense)` erodes;
- loyalty holds (or grows) despite falling meaning — classic feudal lock-in.

---

### B) Regime: REFORM / RESOLUTION (breakthrough)

**Goal:** make conflict closable: coordination rises and redundancy does not capture the breakthrough.

- **Low:** `R_power` (fewer backup neutralization channels), `G_regen` (regeneration less neutralized), `C_conflict` (less “idling”).
- **Moderate:** `I_work` (so energy isn’t immediately consumed), `A_affect` (should provide a “spark”, not burn resources).
- **Weights:** reduce `μ` (fatigue weakly suppresses coordination), raise `ν` (collective regeneration genuinely builds `Coord`).
- **Thresholds:** set `TH_reform` to be achievable (not too low to happen by accident, not too high to be impossible).

**Regime signature:**
- `mean(Coord)` rises and crosses `TH_reform`, and the “resolution” event occurs more often (because `(1 − R_power)` is higher);
- `mean(F)` falls or stops rising;
- conflict ceases to be purely reactive: the gap “high `Out` / low `Coord`” narrows.

---

### C) Regime: EXIT / COLLAPSE (outflow, relationship leakage)

**Goal:** drive energy and meaning down so that the amortization system is overwhelmed — and `TH_exit` is met (a large share of agents have `E < e_min` and `Sense < s_min`).

- **High:** `I_work`, `α`, `β`, `κ` (energy and meaning drop quickly; fatigue accumulates fast).
- **High:** `G_regen` (regeneration is ineffective) — no “bounce back”.
- **Affect:** two routes:
  - **(C1) affective burnout:** high `A_affect`, high `γ/η` → high arousal/fear, but rapid energy erosion;
  - **(C2) cold shutdown:** low `A_affect` → little fuel, quick drop in activity and meaning.
- **Feudalism weakens:** lower `ρ` (access rewards bind less), lower `σ` (fear binds loyalty less), or introduce heterogeneity of “exit alternatives” so some agents can truly exit.
- **Thresholds:** lower `TH_exit` and raise `e_min/s_min` (exit becomes “easier” and triggers earlier).

**Regime signature:**
- sharp drop in `mean(E)` and `mean(Sense)` + fast growth of the share of agents below thresholds;
- `Loy` no longer stabilizes the system (either falls, or doesn’t translate into `Access`), and the patronage network “breaks”.

---

## Mini chart scheme for an appendix (example results)

1. **“System thermodynamics”:** `mean(E)`, `mean(F)`, `mean(Sense)` (time)  
2. **“Dispute vs agency”:** `mean(Out)`, `mean(Coord)` + line `TH_reform` (time)  
3. **“Conflict without resolution”:** `ConflictIntensity(t)` vs `ResolutionPotential(t)` (scatter)  
4. **“Feudalization”:** `Access_received(i)` vs `Loy(i)` + `corr(Access_received, Loy)` (scatter)  
5. **“Cost inequality”:** distribution of `F` at start vs end (hist/violin)  
6. **“Regime map”:** heatmap `I_work` × `G_regen` with outcome class (drift/reform/collapse)

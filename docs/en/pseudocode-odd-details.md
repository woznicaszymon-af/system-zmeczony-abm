# ABM “Tired System” — Pseudocode (ODD – Details)

## Inputs
- N vassals, M lords, a relationship graph (patronage / cooperation / conflict)
- environment parameters: `I_work`, `A_affect`, `R_power`, `C_conflict`, `G_regen`
- thresholds: `TH_reform`, `TH_exit`, `TH_breakdown`
- update weights: `α`, `β`, `γ`, `η`, `κ`, `μ`, `ν`, `ρ`, `σ`, `τ`
- horizon: `T` steps

---

## Initialization
1. Create the population of vassals and lords.
2. Draw/set heterogeneity (e.g., resilience, exit alternatives, network centrality).
3. Set initial vassal states:
   - `E` ~ moderate, `F` ~ low/medium, `Sense` ~ medium/high,
   - `Out`, `Fear`, `Loy`, `Coord` ~ moderate (or context-dependent).
4. Set lord states (`Access`, `Cap`, `Doxa`, `Buffer`) and patronage relationships.

---

## Simulation loop (for t = 1…T)

### Step 1 — system stimuli
1.1 Draw an affective stimulus `A(t)` driven by `A_affect` (e.g., a media/organizational shock).  
1.2 Determine the “busyness inflation” level as a workload component driven by `I_work`.

### Step 2 — workload and energy (work as the maintenance of work)
For each vassal `i`:
2.1 Compute `Workload_i = base + I_work * noise + visibility_cost` (e.g., increasing with loyalty or network position).  
2.2 Update energy:  
`E_i ← clip(E_i − α * Workload_i + regen_i)`  
2.3 Update meaning:  
`Sense_i ← clip(Sense_i − β * Workload_i)`

### Step 3 — affect as fuel
For each vassal `i`:
3.1 `Out_i ← clip(Out_i + γ * A(t) − δ * F_i)`  
3.2 `Fear_i ← clip(Fear_i + η * A(t) + risk_exclusion_i)`

### Step 4 — fatigue and coordination
For each vassal `i`:
4.1 `F_i ← clip(F_i + κ * (1 − E_i) + overload_shock_i)`  
4.2 `Coord_i ← clip(Coord_i − μ * F_i + ν * collective_regen(t))`

### Step 5 — feudal interactions (access ↔ loyalty)
For each lord `j`:
5.1 Set an “access” budget to distribute (e.g., `Access_j * institutional_resource`).  
5.2 For candidates `i` under `j`, compute:  
`P(access_i | j) = function(Loy_i, centrality_i, performance_i)`  
5.3 Allocate access (randomly / proportionally to `P`).

For each vassal `i`:
5.4 If `i` received access:  
`Loy_i ← clip(Loy_i + ρ * 1 + σ * Fear_i − τ * (1 − Sense_i))`  
otherwise:  
`Loy_i ← clip(Loy_i + σ * Fear_i − τ * (1 − Sense_i))`

(Interpretation: loyalty rises both through reward and through fear; meaning is protective.)

### Step 6 — conflict without resolution
6.1 `ConflictIntensity ← mean(Out) * C_conflict`  
6.2 `ResolutionPotential ← function(mean(Coord), (1 − R_power), network_structure)`  
6.3 The “resolution” event occurs with probability `p = g(ResolutionPotential, threshold)`.

### Step 7 — regeneration (neutralized vs agentic)
For each vassal `i`:
7.1 `regen_i ← private_rest − penalty(G_regen, forms_of_regeneration)`  
7.2 `collective_regen(t) ← function(network_support) * (1 − G_regen)`

(Interpretation: the higher `G_regen`, the less regeneration that increases coordination.)

### Step 8 — terminal conditions
8.1 If `mean(Coord) > TH_reform` AND “resolution” occurred:  
Record: **REFORM / BREAKTHROUGH** and stop (optional).  
8.2 If the share of agents with `(E < e_min AND Sense < s_min)` exceeds `TH_exit`:  
Record: **EXIT / COLLAPSE** and stop (optional).  
8.3 If nothing occurs:  
Continue (the system persists / drifts).

---

## Outputs
- time series: `mean(F)`, `mean(E)`, `mean(Sense)`, `mean(Out)`, `mean(Fear)`, `mean(Loy)`, `mean(Coord)`
- inequalities (e.g., distribution of `F` and `Access`)
- feudalization measures: `corr(Access_received, Loy)` and access concentration
- conflict-without-resolution index: high `ConflictIntensity` with low `ResolutionPotential`
- trajectory classification: persistence/drift vs breakthrough vs exit

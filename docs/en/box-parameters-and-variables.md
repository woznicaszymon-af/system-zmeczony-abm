# BOX: Parameters, Variables, and Definitions (ABM “Tired System”)

## A. Agents and roles
- **Vassal (W)** — a system participant operating under permanent mobilization; their “currency” is availability, loyalty, affect, and alignment with the system’s rhythm.  
- **New Lord (L)** — an actor who aggregates access (projects, visibility, gatekeeping), symbolic capital, and the power to include/exclude; stabilizes relations of dependence.

## B. Vassal state variables *(typically 0–1)*
- **`E_i`** — energy: a psychophysical resource (decreases under load; increases through regeneration).
- **`F_i`** — fatigue: accumulated energy deficit (rises when `E` falls; acts as a “coordination brake”).
- **`Sense_i`** — meaning/teleology: the subjective sense that effort leads somewhere (declines in “motion without progress”).
- **`Out_i`** — arousal/outrage: reactive conflict energy (can sustain activity, but consumes `E`).
- **`Fear_i`** — exclusion fear: anxiety about falling out of circulation (strengthens loyalty, weakens propensity to revolt).
- **`Loy_i`** — loyalty: attachment to a lord/organization as a “contract” (loyalty exchanged for illusory security/access).
- **`Coord_i`** — coordination capacity: readiness for collective action (drops with fatigue; rises with collective regeneration).

## C. Lord state variables *(0–1)*
- **`Access_j`** — access control: ability to allocate projects, visibility pathways, inclusion.
- **`Cap_j`** — capital: combined symbolic/institutional resources (reinforces position).
- **`Doxa_j`** — doxa strength: capacity to set “common sense” and loyalty norms.
- **`Buffer_j`** — redundant buffer: ability to absorb crises (coupled to power redundancy in the environment).

## D. Environment parameters *(drive dynamics; 0–1)*
- **`I_work`** — busyness inflation: how much “work-about-work” (procedures, meetings, reporting) the system adds.
- **`A_affect`** — affective stimulus intensity: how much fuel is supplied by fear/outrage/pressure.
- **`R_power`** — power redundancy: how many backup channels stabilize the system and neutralize breakthroughs.
- **`C_conflict`** — conflict-without-resolution: how strongly the system turns conflict into “idle running”.
- **`G_regen`** — regeneration neutralization: to what extent rest is allowed only as a return to mobilization  
  *(1 = strong neutralization; 0 = agentic regeneration).*

## E. Update parameters *(weights; typically 0.01–0.2)*
- **`α`** — energetic cost of workload.
- **`β`** — meaning cost of “motion without progress”.
- **`γ`, `η`** — impact of affective stimuli on `Out` / `Fear`.
- **`κ`** — fatigue accumulation rate.
- **`μ`, `ν`** — impact of fatigue and regeneration on coordination.
- **`ρ`, `σ`, `τ`** — weights for loyalty growth (access reward, fear, meaning erosion).

## F. Outputs *(what the model reports)*
- **Operational stability:** share of time without “breakthrough events” (reform / mass exit / collapse).
- **Mean fatigue and fatigue inequality:** who pays the cost of persistence.
- **Conflict without resolution:** high `Out` with low `Coord`.
- **Feudalization strength:** the `Access → Loy` link (and access concentration).
- **Drift:** changing topics/activity without structural change.

## G. Terminal events *(breakthroughs)*
- **Reform / resolution:** when mean coordination crosses a threshold and redundancy does not “capture” the conflict.
- **Exit / relationship collapse:** when energy and meaning drop below thresholds and outflow rises.
- **Persistence / drift:** when conflict continues but coordination remains too low to resolve it.

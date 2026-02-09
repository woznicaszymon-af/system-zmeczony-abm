# Example results (figure scheme)

This section provides ready-to-paste figure descriptions for the appendix. The plots map directly to the model’s output measures and regime classification.

## Fig. 1 — “System thermodynamics”: E, F, Sense (time)
Time series: `mean(E)`, `mean(F)`, `mean(Sense)`
- Drift: `F` rises and plateaus; `E` low-stable; `Sense` slowly erodes.
- Reform: `F` slows/falls; `Sense` stabilizes or rebounds.
- Collapse: `E` and `Sense` drop fast; `F` saturates high.

## Fig. 2 — “Dispute vs agency”: Out and Coord (time)
Time series: `mean(Out)`, `mean(Coord)` + horizontal line `TH_reform`
- Drift: `Out` high, `Coord` stays below threshold.
- Reform: `Coord` rises and crosses `TH_reform`.
- Collapse: `Out` may be high (burnout) or low (shutdown), but `Coord` does not build.

## Fig. 3 — “Conflict without resolution”: phase map (scatter)
Points over time: `ConflictIntensity(t)` on X vs `ResolutionPotential(t)` on Y
- Drift: cloud in “high conflict / low resolution” (idling).
- Reform: cloud shifts upward (resolution potential rises).
Definitions of these quantities are in Steps 6.1–6.2 of the pseudocode.

## Fig. 4 — “Feudalization”: Access vs Loy (scatter) + correlation
Scatter: `Access_received(i)` vs `Loy(i)` (end of simulation) + `corr(Access_received, Loy)`
- Drift: strong positive relationship (access locks loyalty).
- Reform: relationship may weaken (meaning/coordination starts “competing” with loyalty).
- Collapse: relationship breaks down (access no longer buys stability).

## Fig. 5 — “Cost inequality”: fatigue distribution (histogram/violin)
Distribution of `F` at start vs end (two panels)
- Drift: inequality of fatigue rises (who pays the cost of persistence).
- Reform: distribution flattens (fewer extremes).
- Collapse: lots of mass at high `F` + tail near `E≈0`.

## Fig. 6 — “Regime map”: 2D phase diagram (heatmap)
X-axis: `I_work` (busyness inflation)  
Y-axis: `G_regen` (neutralization of regeneration)  
Color: outcome class (drift / reform / collapse) per terminal conditions (Step 8).

This is the “strongest” appendix chart: in one image it shows where the system drifts, where it breaks, and where it allows resolution.

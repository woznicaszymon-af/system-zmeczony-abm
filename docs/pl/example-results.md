# Przykładowe wyniki (schemat rycin)

Ten dokument zawiera gotowe do wklejenia opisy rycin do aneksu. Wykresy mapują się bezpośrednio na miary wyjściowe modelu oraz klasyfikację reżimów.

## Rys. 1 — „Termodynamika systemu”: E, F, Sense (czas)
Szeregi czasowe: `mean(E)`, `mean(F)`, `mean(Sense)`
- **Dryf:** `F` rośnie i wchodzi w plateau; `E` nisko‑stabilne; `Sense` powoli eroduje.
- **Reforma:** `F` hamuje/spada; `Sense` stabilizuje się lub odbija.
- **Rozpad:** `E` i `Sense` szybko spadają; `F` saturuje wysoko.

## Rys. 2 — „Spór vs sprawczość”: Out i Coord (czas)
Szeregi czasowe: `mean(Out)`, `mean(Coord)` + pozioma linia `TH_reform`
- **Dryf:** `Out` wysokie, `Coord` pozostaje poniżej progu.
- **Reforma:** `Coord` rośnie i przekracza `TH_reform`.
- **Rozpad:** `Out` może być wysokie (przepalenie) albo niskie (wygaszenie), ale `Coord` się nie buduje.

## Rys. 3 — „Konflikt bez rozstrzygnięcia”: mapa fazowa (scatter)
Punkty w czasie: `ConflictIntensity(t)` na osi X vs `ResolutionPotential(t)` na osi Y
- **Dryf:** chmura w obszarze „wysoki konflikt / niskie rozstrzygnięcie” (bieg jałowy).
- **Reforma:** chmura przesuwa się w górę (rośnie potencjał rozstrzygnięcia).
Definicje tych wielkości są w krokach 6.1–6.2 pseudokodu.

## Rys. 4 — „Feudalizacja”: Access vs Loy (scatter) + korelacja
Wykres rozrzutu: `Access_received(i)` vs `Loy(i)` (koniec symulacji) + `corr(Access_received, Loy)`
- **Dryf:** silna dodatnia zależność (dostęp „domyka” lojalność).
- **Reforma:** zależność może słabnąć (sens/koordynacja zaczynają „konkurować” z lojalnością).
- **Rozpad:** zależność się rozpada (dostęp nie kupuje już stabilności).

## Rys. 5 — „Nierówność kosztów”: rozkład zmęczenia (histogram/violin)
Rozkład `F` na początku vs na końcu (dwa panele)
- **Dryf:** rośnie nierówność zmęczenia (kto płaci koszt trwania).
- **Reforma:** rozkład się spłaszcza (mniej ekstremów).
- **Rozpad:** dużo masy przy wysokim `F` + ogon blisko `E≈0`.

## Rys. 6 — „Mapa reżimów”: diagram fazowy 2D (heatmap)
Oś X: `I_work` (inflacja zajętości)  
Oś Y: `G_regen` (neutralizacja regeneracji)  
Kolor: klasa wyniku (dryf / reforma / rozpad) wg warunków końcowych (Krok 8).

To „najmocniejsza” rycina do aneksu: w jednym obrazie pokazuje, gdzie system dryfuje, gdzie pęka i gdzie dopuszcza rozstrzygnięcie.

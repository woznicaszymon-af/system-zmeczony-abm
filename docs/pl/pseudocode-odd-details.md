# Pseudokod ABM „Systemu Zmęczonego” (ODD – Details)

## Wejście
- N wasali, M lordów, graf relacji (patronaż / współpraca / konflikt)
- parametry środowiska: `I_work`, `A_affect`, `R_power`, `C_conflict`, `G_regen`
- progi: `TH_reform`, `TH_exit`, `TH_breakdown`
- wagi aktualizacji: `α`, `β`, `γ`, `η`, `κ`, `μ`, `ν`, `ρ`, `σ`, `τ`
- horyzont: `T` kroków

---

## Inicjalizacja
1. Utwórz populację wasali i lordów.
2. Wylosuj/ustaw heterogeniczność (np. odporność, alternatywy wyjścia, centralność w sieci).
3. Ustaw stany początkowe wasali:
   - `E` ~ umiarkowane, `F` ~ niskie/średnie, `Sense` ~ średnie/wysokie,
   - `Out`, `Fear`, `Loy`, `Coord` ~ umiarkowane (lub zgodnie z kontekstem).
4. Ustaw stany lordów (`Access`, `Cap`, `Doxa`, `Buffer`) i relacje patronażu.

---

## Pętla symulacji (dla t = 1…T)

### Krok 1 — bodźce systemowe
1.1 Wylosuj bodziec afektywny `A(t)` zależny od `A_affect` (np. szok medialny/organizacyjny).  
1.2 Określ poziom „inflacji zajętości” jako komponent obciążenia zależny od `I_work`.

### Krok 2 — obciążenie i energia (praca jako obsługa pracy)
Dla każdego wasala `i`:
2.1 Wyznacz `Workload_i = base + I_work * noise + koszt_widzialności` (np. rośnie z lojalnością lub pozycją).  
2.2 Zaktualizuj energię:  
`E_i ← clip(E_i − α * Workload_i + regen_i)`  
2.3 Zaktualizuj sens:  
`Sense_i ← clip(Sense_i − β * Workload_i)`

### Krok 3 — afekt jako paliwo
Dla każdego wasala `i`:
3.1 `Out_i ← clip(Out_i + γ * A(t) − δ * F_i)`  
3.2 `Fear_i ← clip(Fear_i + η * A(t) + risk_exclusion_i)`

### Krok 4 — zmęczenie i koordynacja
Dla każdego wasala `i`:
4.1 `F_i ← clip(F_i + κ * (1 − E_i) + overload_shock_i)`  
4.2 `Coord_i ← clip(Coord_i − μ * F_i + ν * collective_regen(t))`

### Krok 5 — interakcje feudalne (dostęp ↔ lojalność)
Dla każdego lorda `j`:
5.1 Ustal pulę „dostępu” do rozdania (np. `Access_j * zasób_instytucjonalny`).  
5.2 Dla kandydatów `i` podległych `j` wyznacz:  
`P(access_i | j) = funkcja(Loy_i, centrality_i, performance_i)`  
5.3 Przydziel access (losowo/proporcjonalnie do `P`).

Dla każdego wasala `i`:
5.4 Jeśli otrzymał access:  
`Loy_i ← clip(Loy_i + ρ * 1 + σ * Fear_i − τ * (1 − Sense_i))`  
w przeciwnym razie:  
`Loy_i ← clip(Loy_i + σ * Fear_i − τ * (1 − Sense_i))`

*(Interpretacja: lojalność rośnie zarówno od nagrody, jak i od lęku; sens działa ochronnie.)*

### Krok 6 — konflikt bez rozstrzygnięcia
6.1 `ConflictIntensity ← mean(Out) * C_conflict`  
6.2 `ResolutionPotential ← function(mean(Coord), (1 − R_power), struktura_sieci)`  
6.3 Zdarzenie „rozstrzygnięcia” zachodzi z prawdopodobieństwem `p = g(ResolutionPotential, threshold)`.

### Krok 7 — regeneracja (zneutralizowana vs sprawcza)
Dla każdego wasala `i`:
7.1 `regen_i ← private_rest − penalty(G_regen, formy_regeneracji)`  
7.2 `collective_regen(t) ← funkcja_sieci_wsparcia * (1 − G_regen)`

*(Interpretacja: im większe `G_regen`, tym mniej regeneracji, która podnosi koordynację.)*

### Krok 8 — sprawdzenie warunków końcowych
8.1 Jeśli `mean(Coord) > TH_reform` i jednocześnie „rozstrzygnięcie” zaszło:  
Zapisz: **REFORMA / PRZEŁOM** i zakończ (opcjonalnie).  

8.2 Jeśli udział agentów z `(E < e_min i Sense < s_min)` przekroczy `TH_exit`:  
Zapisz: **EXIT / ROZPAD** i zakończ (opcjonalnie).  

8.3 Jeśli nic nie zaszło:  
Kontynuuj (system trwa / dryfuje).

---

## Wyjście
- szeregi czasowe: `mean(F)`, `mean(E)`, `mean(Sense)`, `mean(Out)`, `mean(Fear)`, `mean(Loy)`, `mean(Coord)`
- nierówności (np. rozkład `F` i `Access`)
- miary feudalizacji: `corr(Access_received, Loy)` i koncentracja dostępu
- indeks konfliktu bez rozstrzygnięcia: wysoki `ConflictIntensity` przy niskim `ResolutionPotential`
- klasyfikacja trajektorii: trwanie/dryf vs przełom vs exit

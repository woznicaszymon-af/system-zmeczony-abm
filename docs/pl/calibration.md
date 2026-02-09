# Kalibracja (jak „ustawiać” trajektorie modelu)

Kalibracja w tym ABM nie oznacza dopasowania do danych empirycznych, tylko strojenie mechanizmu tak, by model wchodził w rozpoznawalne reżimy dynamiczne: **dryf**, **przełom** (reforma/rozstrzygnięcie) lub **exit/rozpad**. W tej konstrukcji przełomy są formalnie zdefiniowane progami i zdarzeniami końcowymi (np. reforma: `mean(Coord) > TH_reform` + zajście „rozstrzygnięcia”; rozpad: przekroczenie `TH_exit` przez udział agentów o niskim `E` i `Sense`).

## 1) Dźwignie (co czym steruje)

Najważniejsze „pokrętła”, bo każda trajektoria to inna relacja między energią/zmęczeniem, afektem, koordynacją, redundancją władzy i regeneracją:

- **Produkcja zmęczenia:** `I_work` (inflacja zajętości) + wagi kosztu `α`, `β` (energia i sens) + akumulacja `κ`.
- **Blokada sprawczości:** wpływ zmęczenia na koordynację `μ` oraz „ratunek” w postaci regeneracji zbiorowej `ν * collective_regen(t)`, którą tłumi `G_regen`.
- **Afekt jako paliwo (reaktywność):** `A_affect` + wagi `γ`, `η` (pobudzenie/lęk).
- **Konflikt bez rozstrzygnięcia:** `C_conflict` podbija intensywność sporu, a `R_power` obniża szanse „domknięcia” przez redundancję.
- **Afektywny feudalizm (lock-in):** `Access → Loy` (alokacja dostępu + aktualizacja `Loy` przez `ρ`, `σ`, `τ`) stabilizuje zależność nawet przy erozji sensu.

**Zasada ogólna:**
- jeśli chcesz **dryfu**, utrzymuj wysoki konflikt i wysoką zajętość, ale niską koordynację i nie dopuszczaj regeneracji, która buduje sprawczość;
- jeśli chcesz **reformy**, poluzuj blokady koordynacji i ogranicz redundancję przechwytującą konflikt;
- jeśli chcesz **rozpadu**, doprowadź do spadku energii i sensu szybciej niż system potrafi to „zamortyzować” dostępem/lojalnością.

## 2) Szybka procedura strojenia (7 kroków)

1. Ustal bazę: średnie stany startowe (`E`, `Sense`, `F`) i „szum” obciążeń.
2. Zablokuj dwa przełomy na starcie: ustaw progi tak, by w bazie nie zaszła reforma ani exit w pierwszych ~10–20% horyzontu.
3. Wybierz cel (dryf / reforma / rozpad) i stroisz tylko 2–3 pokrętła naraz.
4. Najpierw ustaw energetykę systemu (`I_work`, `α`, `κ`, `β`), dopiero potem afekt (`A_affect`, `γ`, `η`).
5. Dopiero na końcu ustaw politykę przełomu (`R_power`, `C_conflict`, `G_regen`, `μ`, `ν`) — bo ona rozstrzyga, czy konflikt „gaśnie”, „dryfuje”, czy się domyka.
6. Sprawdź stabilność reżimu: czy wynik utrzymuje się przy drobnych zmianach (np. ±10%) jednego parametru.
7. Ustal podpis reżimu: spisz 3–4 wskaźniki, które w tym reżimie zawsze wyglądają tak samo.

## 3) Trzy gotowe zestawy kalibracyjne (heurystyki)

Poniżej trzy „przepisy” — jako kierunek ustawień, które w tej logice powinny generować odpowiednią dynamikę.

### A) Reżim: DRYF (trwanie / konflikt na biegu jałowym)

**Cel:** wysoki konflikt i zajętość, ale bez koordynacji i bez wyjścia.

- **Wysokie:** `I_work`, `C_conflict`, `R_power`, `G_regen`.
- **Umiarkowane–wysokie:** `A_affect` (paliwo na reaktywność), ale nie tak wysokie, by szybko przepalało energię.
- **Wagi:** `μ` raczej wysokie, `ν` niskie, `σ` wysokie, `ρ` umiarkowane.
- **Progi:** `TH_reform` podnieś; `TH_exit` także podnieś albo obniż `e_min/s_min`.

**Podpis reżimu:**
- `mean(Out)` i `ConflictIntensity` wysokie, ale `mean(Coord)` stale poniżej `TH_reform`;
- `mean(F)` rośnie i stabilizuje się wysoko; `mean(Sense)` eroduje;
- lojalność utrzymuje się (lub rośnie) mimo spadku sensu.

### B) Reżim: REFORMA / ROZSTRZYGNIĘCIE (przełom)

**Cel:** konflikt może się domknąć, bo rośnie koordynacja, a redundancja nie przechwytuje przełomu.

- **Niskie:** `R_power`, `G_regen`, `C_conflict`.
- **Umiarkowane:** `I_work`, `A_affect`.
- **Wagi:** `μ` obniż, `ν` podnieś.
- **Progi:** `TH_reform` ustaw „osiągalnie” (nie za nisko, nie za wysoko).

**Podpis reżimu:**
- `mean(Coord)` rośnie i przekracza `TH_reform`, a „resolution” zachodzi częściej;
- `mean(F)` spada lub przestaje rosnąć;
- maleje rozjazd: wysokie `Out` / niskie `Coord`.

### C) Reżim: EXIT / ROZPAD (odpływ, rozszczelnienie relacji)

**Cel:** spadek energii i sensu przebija amortyzację i spełnia się warunek `TH_exit`.

- **Wysokie:** `I_work`, `α`, `β`, `κ`.
- **Wysokie:** `G_regen` (brak „odbicia”).
- **Afekt — dwie ścieżki:**
  - (C1) przepalenie: wysokie `A_affect`, wysokie `γ/η`;
  - (C2) wygaszenie: niskie `A_affect`.
- **Feudalizm słabnie:** obniż `ρ`, obniż `σ` albo wprowadź heterogeniczność „alternatyw wyjścia”.
- **Progi:** `TH_exit` obniż, a `e_min/s_min` podnieś.

**Podpis reżimu:**
- gwałtowny spadek `mean(E)` i `mean(Sense)` + szybki wzrost udziału agentów poniżej progów;
- `Loy` nie stabilizuje już systemu; sieć patronażu się „przerywa”.

---

## Mini-schemat wykresów do aneksu (wyniki przykładowe)

Zestaw 6 wykresów + krótkie podpisy (format do wklejenia jako „Przykładowe wyniki — schemat”):

1. **„Termodynamika systemu”:** `mean(E)`, `mean(F)`, `mean(Sense)` (czas)  
2. **„Spór vs sprawczość”:** `mean(Out)`, `mean(Coord)` + linia `TH_reform` (czas)  
3. **„Konflikt bez rozstrzygnięcia”:** `ConflictIntensity(t)` vs `ResolutionPotential(t)` (scatter)  
4. **„Feudalizacja”:** `Access_received(i)` vs `Loy(i)` + `corr(Access_received, Loy)` (scatter)  
5. **„Nierówność kosztów”:** rozkład `F` na początku vs na końcu (hist/violin)  
6. **„Mapa reżimów”:** heatmapa `I_work` × `G_regen` z klasyfikacją (dryf/reforma/rozpad)

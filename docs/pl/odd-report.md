# Aneks: Model ABM „System Zmęczony” — raport ODD (Overview–Design concepts–Details)

Ten dokument opisuje model agentowy (ABM) jako **operacjonalizację mechanizmów** z książki: *system zmęczony*, *stabilność niskoenergetyczna*, *zmęczenie systemowe*, *afekt jako paliwo*, *konflikt bez rozstrzygnięcia*, *redundancja władzy* oraz (w wątku **Afektywnego Feudalizmu**) relacje **dostępu** i **lojalności**.  
Model nie ma „udowadniać” tez o świecie, tylko testować **dynamiczną spójność**: czy z założonych reguł wyłaniają się stabilne reżimy **dryfu**, **przełomu (reformy/rozstrzygnięcia)** lub **exit/rozpadu**.

**Powiązane pliki w repo:**
- Algorytm krok po kroku (ODD – Details): `docs/pl/pseudocode-odd-details.md`
- Strojenie reżimów (kalibracja): `docs/pl/calibration.md`
- Parametry i definicje zmiennych (box): `docs/pl/box-parameters-and-variables.md` *(jeśli istnieje / do uzupełnienia)*

---

## 1) Overview

### 1.1 Cel modelu
Celem jest symulacyjne sprawdzenie, jak system utrzymuje stabilność **bez wzrostu i bez reform**, poprzez:
- produkowanie i redystrybuowanie **zmęczenia systemowego** zamiast rozwiązywania sprzeczności,
- podtrzymywanie permanentnej mobilizacji i zajętości (**inflacja procedur, zadań, spotkań**),
- konwersję deficytów wartości na **afekt jako paliwo** (lęk/oburzenie/presja),
- „bezpieczne” utrzymywanie sporu jako **konfliktu bez rozstrzygnięcia**,
- utrzymywanie mikrohierarchii lord–wasal (Afektywny Feudalizm) poprzez **dostęp, widzialność, uznanie** i obietnicę ochrony przed wykluczeniem.

Wynikiem jest zestaw **testowalnych mechanizmów**: które kombinacje parametrów generują trwały **dryf**, a które prowadzą do **przełomu** (reforma/rozstrzygnięcie) lub **exit/rozpadu** (odpływ/rozszczelnienie relacji).

### 1.2 Pytania badawcze
- Czy inflacja pracy i zajętości może stabilizować system przez obniżanie energii i zdolności koordynacji?
- Czy afekt może działać jako substytut wartości i „paliwo” mobilizacji bez przełomu?
- Czy konflikt bez rozstrzygnięcia jest stabilnym reżimem dynamicznym (wysoka intensywność sporu + niska sprawczość)?
- Jaką rolę pełni redundancja władzy w utrzymaniu tego stanu?
- Kiedy tryb awaryjny Afektywnego Feudalizmu (dostęp ↔ lojalność) zwiększa stabilność, a kiedy pęka?

---

## 2) Jednostki, stan i środowisko

### 2.1 Typy agentów
**Wasale (W)**  
Jednostki funkcjonujące w warunkach permanentnej mobilizacji; ich kluczowym zasobem wymiany jest energia afektywna i lojalność (czas, dyspozycyjność, „zawsze online”, samoeksploatacja), a nie tylko praca rozumiana produktywnie.

**Nowi Lordowie (L)**  
Aktorzy agregujący dostęp i kapitał (instytucjonalny/społeczny/symboliczny) oraz modulujący warunki zależności: oferują ścieżki widzialności, włączania, ochrony przed wypadnięciem z obiegu — w zamian stabilizując relację lojalnościową.

### 2.2 Mechanizmy systemowe (S) — „architektura”
Nie jako „agent z intencją”, tylko jako reguły środowiskowe:
- inflacja zadań/procedur (produkowanie zajętości),
- bodźce afektywne (pobudzenie/oburzenie/lęk/presja),
- redundancja władzy (zapasowe kanały kontroli: prawo/rynek/moralność/algorytm),
- regeneracja zneutralizowana (odpoczynek dopuszczony głównie jako powrót do mobilizacji),
- konflikt bez rozstrzygnięcia jako stała dynamika pola publicznego.

### 2.3 Środowisko
- sieć organizacyjno‑platformowa (graf): relacje patronażu, hierarchie statusu, przepływy uwagi, rynki pracy „widzialności”,
- parametry makro: stagnacja wzrostu / deficyt sensu (brak nagrody materialnej za wysiłek), co przesuwa system w stronę afektu jako substytutu wartości.

---

## 3) Zmienne stanu

### 3.1 Wasal (i)
- `E_i` — energia/zasób psychofizyczny (spada od obciążeń; rośnie od regeneracji)
- `F_i` — zmęczenie (funkcja skumulowanego deficytu energii)
- `Loy_i` — lojalność wobec lorda/organizacji (wymiana: lojalność za bezpieczeństwo/dostęp)
- `Fear_i` — lęk przed wykluczeniem (wzmacnia lojalność, osłabia bunt)
- `Out_i` / `Outrage_i` — oburzenie/napęd konfliktu (podnosi „aktywność”, ale zużywa energię)
- `Sense_i` — poczucie sensu/teleologii pracy (maleje przy „ruchu w miejscu”)
- `C_i` / `Coord_i` — zdolność koordynacji (spada przy wysokim zmęczeniu; klucz do przełomu)

### 3.2 Lord (j)
- `Access_j` — kontrola dostępu (projekty, granty, widzialność, awanse, gatekeeping)
- `Cap_j` — kapitał (społeczno‑ekonomiczno‑symboliczny)
- `Doxa_j` — zdolność kształtowania norm lojalności (miękka hegemonia)
- `Buffer_j` — zdolność absorpcji kryzysów (redundancja, zapasowe kanały władzy)

---

## 4) Procesy i mechanizmy (intuicja + harmonogram)

Model jest dyskretny (`t = 1…T`). W każdej iteracji zachodzą procesy:

**(A) Produkcja zajętości zamiast produktywności**  
Środowisko generuje obciążenie: `Workload_i(t) = baza + inflacja + wymogi widzialności`.  
Efekt: spadek `E_i`, wzrost `F_i`, spadek `Sense_i` („praca nie prowadzi nigdzie”).

**(B) Afekt jako paliwo (substytut wartości)**  
Gdy nagroda materialna nie rośnie, system podbija bodźce afektywne: rosną `Outrage_i` i/lub `Fear_i`.  
To zwiększa aktywność, ale zużywa energię i podbija zmęczenie.

**(C) Relacja feudalna: dostęp → lojalność**  
Lord rozdaje dostęp selektywnie: im większy `Fear_i` i im mniejsze alternatywy wyjścia, tym łatwiej rośnie `Loy_i`.  
Lojalność zwiększa szansę otrzymania `Access`, ale kosztuje energię (dyspozycyjność, autoeksploatacja).

**(D) Konflikt bez rozstrzygnięcia (stabilizacja przez bieg jałowy)**  
Wysokie `Outrage` podnosi intensywność sporu, ale gdy `F` rośnie, reaktwyność przechodzi w cynizm/wycofanie. Bunt nie eskaluje, tylko gaśnie: „system nie tłumi protestów — on je wyczerpuje”.

**(E) Regeneracja zneutralizowana**  
Regeneracja istnieje, ale jest warunkowa: dopuszczona jest głównie taka, która nie podnosi koordynacji i refleksji strukturalnej (nie buduje zbiorowej sprawczości).

**(F) Kryterium stabilności niskoenergetycznej**  
System jest „stabilny”, gdy: średnie zmęczenie jest wysokie, ale funkcjonowanie trwa; nie dochodzi do skutecznej koordynacji; konflikt trwa, ale nie ma zwycięzców (brak reform strukturalnych).

> Szczegóły algorytmu (równania aktualizacji, progi i zdarzenia końcowe) są w `docs/pl/pseudocode-odd-details.md`.

---

## 5) Miary wyjściowe (raportowanie)

Proponowane wskaźniki:
- **Stabilność operacyjna:** udział kroków bez zdarzeń przełomu (strajk/masowe odejście/reforma).
- **Zmęczenie:** `mean(F)` oraz nierówność zmęczenia (kto płaci koszty stabilności).
- **Konflikt vs sprawczość:** wysoki `Outrage` przy niskiej `Coord` = konflikt bez rozstrzygnięcia.
- **Siła feudalizacji:** korelacja `Access_received ↔ Loy` oraz koncentracja dostępu.
- **Dryf systemowy:** zmiana tematów/konfliktów przy braku zmian strukturalnych („zmiana bez transformacji”).

---

## 6) Projekt eksperymentów symulacyjnych (pakiety)

Cztery proste pakiety (siatka parametrów + obserwacje):

**A) Inflacja pracy**  
Manipulacja: `I_work` (niska → wysoka)  
Oczekiwane: wzrost `F`, spadek `Coord`, wzrost stabilności „bez sensu”.

**B) Afekt jako paliwo**  
Manipulacja: `A_affect` (niska → wysoka)  
Oczekiwane: więcej konfliktu i mobilizacji, ale bez rozstrzygnięcia (wysokie `Out`, niska `Coord`).

**C) Feudalizacja dostępu**  
Manipulacja: koncentracja `Access_j` oraz waga zależności `Loy → access`  
Oczekiwane: stabilizacja przez lojalność w zamian za „ochronę”; kosztem rosnącego zmęczenia i spadającego sensu.

**D) (De)neutralizacja regeneracji**  
Manipulacja: `G_regen` (silna neutralizacja → realna regeneracja zbiorowa)  
Oczekiwane: spadek `F`, wzrost `Coord`, wzrost prawdopodobieństwa przełomu.

---

## 7) Hipotezy do testowania

**H1 (inflacja pracy → stabilność przez wyczerpanie)**  
Wzrost inflacji zadań/procedur powoduje wzrost średniego zmęczenia i spadek zdolności koordynacji, co zwiększa stabilność operacyjną mimo spadku sensu.

**H2 (afekt jako substytut wartości → aktywność bez sprawczości)**  
Podbijanie bodźców afektywnych zwiększa aktywność i konflikt, ale nie buduje sprawczości zbiorowej; konflikt utrzymuje się bez rozstrzygnięcia, a zmęczenie reguluje napięcia.

**H3 (feudalizacja → lojalność przy malejących nagrodach)**  
Im większa koncentracja dostępu i lęk wykluczenia, tym większa lojalność mimo braku realnego awansu; ceną jest wzrost zmęczenia i spadek sprawczości.

**H4 (regeneracja zbiorowa jako zdarzenie destabilizujące)**  
Jeśli regeneracja podnosi nie tylko `E`, ale i `Coord`, rośnie prawdopodobieństwo przełomu (reforma albo eskalacja poza bieg jałowy) — chyba że system równolegle wzmacnia redundancję i amortyzację afektywną.

---

## 8) Uwaga interpretacyjna (do wklejenia do książki)
Ten ABM nie jest „dowodem”, lecz testem dynamicznej spójności diagnozy: czy z mechanizmów inflacji zajętości, afektu jako paliwa, konfliktu bez rozstrzygnięcia, redundancji władzy, neutralizacji regeneracji oraz feudalizacji dostępu wyłania się stabilny reżim trwania bez przyszłości — system, który nie upada i nie zwycięża, tylko dryfuje.

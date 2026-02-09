# BOX: Parametry, zmienne i definicje (ABM „Systemu Zmęczonego”)

## A. Agenci i role
- **Wasal (W)** — uczestnik systemu funkcjonujący w trybie permanentnej mobilizacji; jego „walutą” są: dyspozycyjność, lojalność, afekt oraz zgodność z rytmem systemu.  
- **Nowy Lord (L)** — aktor agregujący dostęp (projekty, widzialność, gatekeeping), kapitał symboliczny i możliwość włączania/wykluczania; stabilizuje relacje zależności.

## B. Zmienne stanu wasala *(zwykle 0–1)*
- **`E_i`** — energia: zasób psychofizyczny (spada od obciążeń; rośnie od regeneracji).
- **`F_i`** — zmęczenie: skumulowany deficyt energii (rośnie, gdy `E` spada; działa jak „hamulec koordynacji”).
- **`Sense_i`** — sens/teleologia: subiektywne poczucie, że wysiłek prowadzi do celu (spada w „ruchu w miejscu”).
- **`Out_i`** — pobudzenie/oburzenie: reaktywna energia konfliktu (może podtrzymywać aktywność, ale zużywa `E`).
- **`Fear_i`** — lęk wykluczenia: obawa przed wypadnięciem z obiegu (wzmacnia lojalność, obniża skłonność do buntu).
- **`Loy_i`** — lojalność: przywiązanie do lorda/organizacji jako „kontrakt” (lojalność za iluzoryczne bezpieczeństwo/dostęp).
- **`Coord_i`** — zdolność koordynacji: gotowość do działań zbiorowych (spada przy zmęczeniu; rośnie przy regeneracji zbiorowej).

## C. Zmienne stanu lorda *(0–1)*
- **`Access_j`** — kontrola dostępu: zdolność przydzielania projektów, ścieżek widzialności, włączania.
- **`Cap_j`** — kapitał: łączny zasób symboliczny/instytucjonalny (wzmacnia pozycję).
- **`Doxa_j`** — siła *doxa*: zdolność ustanawiania „oczywistości” i norm lojalności.
- **`Buffer_j`** — bufor redundantny: zdolność amortyzacji kryzysów (sprzęgnięta z redundancją władzy w środowisku).

## D. Parametry środowiska *(sterują dynamiką; 0–1)*
- **`I_work`** — inflacja zajętości: ile „obsługi pracy” (procedury, spotkania, raportowanie) dokłada system.
- **`A_affect`** — natężenie bodźców afektywnych: ile paliwa dostarcza lęk/oburzenie/presja.
- **`R_power`** — redundancja władzy: ile kanałów zapasowych stabilizuje system i neutralizuje przełom.
- **`C_conflict`** — konflikt bez rozstrzygnięcia: jak silnie system przekształca konflikt w „bieg jałowy”.
- **`G_regen`** — neutralizacja regeneracji: na ile odpoczynek jest dopuszczany tylko jako powrót do mobilizacji  
  *(1 = silna neutralizacja; 0 = regeneracja sprawcza).*

## E. Parametry aktualizacji *(wagi; typowo 0.01–0.2)*
- **`α`** — koszt energetyczny obciążenia.
- **`β`** — koszt sensu od „ruchu w miejscu”.
- **`γ`, `η`** — wpływ bodźców afektywnych na `Out` / `Fear`.
- **`κ`** — tempo akumulacji zmęczenia.
- **`μ`, `ν`** — wpływ zmęczenia i regeneracji na koordynację.
- **`ρ`, `σ`, `τ`** — wagi wzrostu lojalności (dostęp, lęk, spadek sensu).

## F. Miary wyjściowe *(co raportuje model)*
- **Stabilność operacyjna:** odsetek czasu bez „przełomu” (reforma / masowy exit / rozpad).
- **Średnie zmęczenie i nierówność zmęczenia:** kto płaci koszt trwania.
- **Konflikt bez rozstrzygnięcia:** wysoki `Out` przy niskiej `Coord`.
- **Siła feudalizacji:** zależność `Access → Loy` (i koncentracja dostępu).
- **Dryf:** zmienność tematów i aktywności przy braku zmiany strukturalnej.

## G. Zdarzenia końcowe *(przełomy)*
- **Reforma / rozstrzygnięcie:** gdy średnia koordynacja przekroczy próg, a redundancja nie „przechwyci” konfliktu.
- **Exit / rozpad relacji:** gdy energia i sens spadną poniżej progów, rośnie odpływ.
- **Trwanie / dryf:** gdy konflikt trwa, ale koordynacja pozostaje zbyt niska, by go rozstrzygnąć.

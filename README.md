# System Zmęczony — ABM (MVP) / Tired System — ABM (MVP)

[PL](#pl) · [EN](#en)

---

## PL

Minimalne, odtwarzalne repozytorium modelu agentowego (Mesa 3.x) do „Systemu Zmęczonego”.
Repo zawiera skrypty do uruchamiania symulacji, eksportu wyników do CSV oraz podstawowych analiz i wykresów.

### Szybki start

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

### Pojedynczy przebieg (preset)

```bash
python run.py --preset dryf --seed 1
python run.py --preset reforma --seed 2
python run.py --preset rozpad --seed 3
```

Wyniki zapisują się do `out/` jako CSV.  
(Uwaga: `out/` to folder wynikowy — zwykle nie jest wersjonowany w repo.)

### Wykresy z CSV

```bash
python analyze.py --model_csv out/model_dryf_seed1.csv --show
```

### Mapa reżimów (I_work × G_regen)

```bash
python sweep_phase_diagram.py --preset dryf --grid 11 --savefig out/phase.png
```

### Dokumentacja
- `docs/pl/box-parameters-and-variables.md`
- `docs/pl/pseudocode-odd-details.md`
- `docs/pl/calibration.md`
- `docs/pl/odd-report.md`
- `docs/pl/example-results.md`


### Cytowanie

Jeśli cytujesz/wklejasz wyniki do tekstu: podaj link do repo oraz commit/tag, z którego pochodziły wyniki (reproducibility).

### Licencja

MIT — zob. plik `LICENSE`.

---

## EN

A minimal, reproducible agent-based model (ABM) repository (Mesa 3.x) accompanying “System Zmęczony” (“Tired System”).
Includes scripts to run simulations, export results to CSV, and generate basic analyses/plots.

### Quickstart

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

### Single run (preset)

```bash
python run.py --preset dryf --seed 1
python run.py --preset reforma --seed 2
python run.py --preset rozpad --seed 3
```

Outputs are written to `out/` as CSV files.  
(Note: `out/` is an output directory and is typically not tracked in git.)

### Plots from CSV

```bash
python analyze.py --model_csv out/model_dryf_seed1.csv --show
```

### Regime map (I_work × G_regen)

```bash
python sweep_phase_diagram.py --preset dryf --grid 11 --savefig out/phase.png
```

### Documentation
- `docs/en/box-parameters-and-variables.md`
- `docs/en/pseudocode-odd-details.md`
- `docs/en/calibration.md`
- `docs/en/odd-report.md`
- `docs/en/example-results.md`


### Citation

If you cite results: please include the repository URL and the commit/tag used to generate the outputs.

### License

MIT — see `LICENSE`.

from __future__ import annotations

import argparse
from itertools import product
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from tired_system import TiredSystemModel, PRESETS
from tired_system.model import ModelParams


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--preset", choices=list(PRESETS.keys()), default="dryf")
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--steps", type=int, default=250)
    ap.add_argument("--n_vassals", type=int, default=200)
    ap.add_argument("--n_lords", type=int, default=10)

    ap.add_argument("--I_min", type=float, default=0.10)
    ap.add_argument("--I_max", type=float, default=0.90)
    ap.add_argument("--G_min", type=float, default=0.10)
    ap.add_argument("--G_max", type=float, default=0.90)
    ap.add_argument("--grid", type=int, default=11)

    ap.add_argument("--outdir", type=str, default="out")
    ap.add_argument("--savefig", type=str, default=None)
    args = ap.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    base = ModelParams(
        n_vassals=args.n_vassals,
        n_lords=args.n_lords,
        max_steps=args.steps,
        seed=args.seed,
    )

    preset = PRESETS[args.preset].copy()
    for k, v in preset.items():
        if hasattr(base, k):
            base = base.__class__(**{**base.__dict__, k: v})

    I_vals = np.linspace(args.I_min, args.I_max, args.grid)
    G_vals = np.linspace(args.G_min, args.G_max, args.grid)

    rows = []
    for I_work, G_regen in product(I_vals, G_vals):
        p = base.__class__(**{**base.__dict__, "I_work": float(I_work), "G_regen": float(G_regen)})
        m = TiredSystemModel(p)
        end = m.run()
        rows.append({
            "I_work": float(I_work),
            "G_regen": float(G_regen),
            "status": end.status,
            "step": end.step,
            "mean_coord": end.mean_coord,
            "exit_share": end.exit_share,
        })

    df = pd.DataFrame(rows)
    csv_path = outdir / f"phase_{args.preset}_seed{args.seed}.csv"
    df.to_csv(csv_path, index=False)
    print(f"Saved: {csv_path}")

    # prosta wizualizacja: status -> liczba
    status_map = {"reform": 2, "running": 1, "max_steps": 1, "collapse": 0}
    df["status_code"] = df["status"].map(status_map).fillna(1).astype(int)

    pivot = df.pivot(index="G_regen", columns="I_work", values="status_code").sort_index(ascending=True)

    plt.figure()
    plt.imshow(pivot.values, aspect="auto", origin="lower")
    plt.title("Mapa reżimów (0=collapse, 1=dryf, 2=reform)")
    plt.xlabel("I_work (kolumny)")
    plt.ylabel("G_regen (wiersze)")
    plt.xticks(range(len(pivot.columns)), [f"{x:.2f}" for x in pivot.columns], rotation=90)
    plt.yticks(range(len(pivot.index)), [f"{y:.2f}" for y in pivot.index])

    if args.savefig:
        plt.savefig(args.savefig, dpi=150, bbox_inches="tight")
    else:
        plt.show()


if __name__ == "__main__":
    main()

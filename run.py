from __future__ import annotations

import argparse
from pathlib import Path
import pandas as pd

from tired_system import TiredSystemModel, PRESETS
from tired_system.model import ModelParams


def build_params_from_args(args) -> ModelParams:
    p = ModelParams(
        n_vassals=args.n_vassals,
        n_lords=args.n_lords,
        max_steps=args.steps,
        seed=args.seed,
    )

    if args.preset:
        preset = PRESETS[args.preset].copy()
        for k, v in preset.items():
            if hasattr(p, k):
                p = p.__class__(**{**p.__dict__, k: v})

    # override z CLI (jeśli podane)
    overrides = {
        "I_work": args.I_work,
        "A_affect": args.A_affect,
        "R_power": args.R_power,
        "C_conflict": args.C_conflict,
        "G_regen": args.G_regen,
        "TH_reform": args.TH_reform,
        "TH_exit": args.TH_exit,
        "e_min": args.e_min,
        "s_min": args.s_min,
    }
    for k, v in overrides.items():
        if v is not None:
            p = p.__class__(**{**p.__dict__, k: v})

    return p


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--preset", choices=list(PRESETS.keys()), default="dryf")
    ap.add_argument("--n_vassals", type=int, default=250)
    ap.add_argument("--n_lords", type=int, default=12)
    ap.add_argument("--steps", type=int, default=400)
    ap.add_argument("--seed", type=int, default=42)

    ap.add_argument("--I_work", type=float, default=None)
    ap.add_argument("--A_affect", type=float, default=None)
    ap.add_argument("--R_power", type=float, default=None)
    ap.add_argument("--C_conflict", type=float, default=None)
    ap.add_argument("--G_regen", type=float, default=None)

    ap.add_argument("--TH_reform", type=float, default=None)
    ap.add_argument("--TH_exit", type=float, default=None)
    ap.add_argument("--e_min", type=float, default=None)
    ap.add_argument("--s_min", type=float, default=None)

    ap.add_argument("--outdir", type=str, default="out")
    args = ap.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    params = build_params_from_args(args)
    model = TiredSystemModel(params)
    end_state = model.run()

    model_df = model.get_model_df()
    agent_df = model.get_agent_df()

    # pliki
    model_path = outdir / f"model_{args.preset}_seed{args.seed}.csv"
    agent_path = outdir / f"agents_{args.preset}_seed{args.seed}.csv"

    model_df.to_csv(model_path, index=True)
    agent_df.to_csv(agent_path, index=True)

    print("DONE")
    print(f"Status: {end_state.status} | step={end_state.step} | mean_coord={end_state.mean_coord:.3f} | exit_share={end_state.exit_share:.3f}")
    print(f"Saved: {model_path}")
    print(f"Saved: {agent_path}")


if __name__ == "__main__":
    main()

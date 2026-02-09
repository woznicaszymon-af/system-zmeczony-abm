from __future__ import annotations

import argparse
import pandas as pd
import matplotlib.pyplot as plt


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model_csv", required=True)
    ap.add_argument("--show", action="store_true")
    ap.add_argument("--save", type=str, default=None)
    args = ap.parse_args()

    df = pd.read_csv(args.model_csv)

    # zakładamy, że indeks kroku jest w pierwszej kolumnie (DataCollector zapisuje index)
    if "Step" in df.columns:
        t = df["Step"]
    else:
        t = df.index

    fig = plt.figure()
    plt.plot(t, df["mean_E"], label="mean_E")
    plt.plot(t, df["mean_F"], label="mean_F")
    plt.plot(t, df["mean_Sense"], label="mean_Sense")
    plt.legend()
    plt.title("E / F / Sense (średnie)")

    if args.save:
        plt.savefig(args.save, dpi=150, bbox_inches="tight")

    if args.show:
        plt.show()


if __name__ == "__main__":
    main()

# sessions/01_histogramas/main.py
# Session 1: Histograms from a CSV
# - Headless by default (saves PNGs into output/)
# - Use --column to plot a single numeric column; otherwise plots all numeric columns.

from pathlib import Path
import argparse
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

from common.io import resolve_repo_path, ensure_dir

def parse_args():
    p = argparse.ArgumentParser(description="Session 1 - Histograms from a CSV.")
    p.add_argument("--csv", required=True, help="CSV path (repo-relative or absolute).")
    p.add_argument("--column", help="Numeric column to plot. If omitted, plots all numeric columns.")
    p.add_argument("--bins", type=int, default=10, help="Number of bins (default: 10).")
    p.add_argument("--outdir", default="output/01_histogramas", help="Output directory.")
    p.add_argument("--show", action="store_true", help="Show windows (local dev only; not for Docker).")
    return p.parse_args()

def main():
    args = parse_args()

    # Use headless backend unless explicitly showing
    if not args.show:
        matplotlib.use("Agg")

    # Resolve paths
    repo_csv = Path(args.csv)
    if not repo_csv.is_absolute():
        repo_csv = resolve_repo_path(args.csv)
    out_dir = resolve_repo_path(args.outdir)
    ensure_dir(out_dir)

    if not repo_csv.exists():
        raise FileNotFoundError(f"CSV not found: {repo_csv}")

    print(f"Loading: {repo_csv}")

    # Autodetect separator (comma, tab, space, etc.)
    df = pd.read_csv(repo_csv, sep=None, engine="python")

    # Try converting any convertible columns to numeric
    for col in df.columns:
    df[col] = pd.to_numeric(df[col], errors="ignore")

    print(df.info())

    # Choose columns
    if args.column:
        if args.column not in df.columns:
            raise ValueError(f"Column '{args.column}' not found.")
        columns = [args.column]
    else:
        columns = df.select_dtypes(include="number").columns.tolist()
        if not columns:
            raise ValueError("No numeric columns to plot.")

    saved = []
    for col in columns:
        s = df[col].dropna()
        if s.empty:
            print(f"[skip] '{col}' is empty after dropna().")
            continue

        plt.figure()
        plt.hist(s, bins=args.bins, edgecolor="black")
        plt.title(f"Histogram - {col}")
        plt.xlabel(col)
        plt.ylabel("Frequency")

        if args.show:
            plt.show()
        else:
            out_file = out_dir / f"hist_{col}.png"
            plt.savefig(out_file, bbox_inches="tight", dpi=120)
            plt.close()
            saved.append(out_file)

    if saved:
        print("Saved:")
        for f in saved:
            print(f" - {f}")

if __name__ == "__main__":
    main()
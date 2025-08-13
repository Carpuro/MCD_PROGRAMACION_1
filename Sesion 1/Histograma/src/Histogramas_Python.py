# --- src/histograms.py
# CLI to plot histograms from a CSV.
# - Headless by default for Docker: saves PNGs to output/
# - Use --column to select one column, otherwise plots all numeric columns.

from pathlib import Path
import argparse
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

def parse_args():
    p = argparse.ArgumentParser(description="Plot histograms from a CSV.")
    p.add_argument("--csv", required=True, help="Path to CSV (repo-relative or absolute).")
    p.add_argument("--column", help="Numeric column to plot. If omitted, plots all numeric columns.")
    p.add_argument("--bins", type=int, default=10, help="Number of bins (default: 10).")
    p.add_argument("--outdir", default="output", help="Output directory (default: output).")
    p.add_argument("--show", action="store_true", help="Show windows (local dev only; not for Docker).")
    return p.parse_args()

def main():
    args = parse_args()

    # Headless backend unless explicitly showing
    if not args.show:
        matplotlib.use("Agg")

    repo_root = Path(__file__).resolve().parents[1]
    csv_path = Path(args.csv)
    if not csv_path.is_absolute():
        csv_path = (repo_root / csv_path).resolve()

    out_dir = Path(args.outdir)
    if not out_dir.is_absolute():
        out_dir = (repo_root / out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    if not csv_path.exists():
        raise FileNotFoundError(f"CSV not found: {csv_path}")

    print(f"Loading: {csv_path}")
    df = pd.read_csv(csv_path)
    print(df.info())

    # Decide columns
    if args.column:
        if args.column not in df.columns:
            raise ValueError(f"Column '{args.column}' not found.")
        cols = [args.column]
    else:
        cols = df.select_dtypes(include="number").columns.tolist()
        if not cols:
            raise ValueError("No numeric columns to plot.")

    saved = []
    for col in cols:
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
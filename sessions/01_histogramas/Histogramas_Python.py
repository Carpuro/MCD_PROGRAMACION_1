# from pathlib import Path
from pathlib import Path
from datetime import datetime
import argparse
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.ticker import FuncFormatter
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

    # Headless backend si no se pide mostrar
    if not args.show:
        matplotlib.use("Agg")

    # Paths
    repo_csv = Path(args.csv)
    if not repo_csv.is_absolute():
        repo_csv = resolve_repo_path(args.csv)
    out_dir = resolve_repo_path(args.outdir)
    ensure_dir(out_dir)

    if not repo_csv.exists():
        raise FileNotFoundError(f"CSV not found: {repo_csv}")

    # Load CSV Data
    print(f"Loading: {repo_csv}")
    df = pd.read_csv(repo_csv, sep=None, engine="python") # Automatically detect separator either tab or comma
    print(df.head())

    # Columns to plot
    if args.column:
        if args.column not in df.columns:
            raise ValueError(f"Column '{args.column}' not found.")
        columns = [args.column]
    else:
        columns = df.select_dtypes(include="number").columns.tolist()
        if not columns:
            raise ValueError("No numeric columns to plot.")

    saved = [] # List of saved figure paths
    summary_data = []  # Save stats here
    timestamp = datetime.now().strftime("%d_%m_%Y") # Timestamp for output files
    colors = cm.tab10.colors # Color map for histograms

    for i, col in enumerate(columns):
        s = df[col].dropna()
        if s.empty:
            print(f"[skip] '{col}' is empty after dropna().")
            continue

        # Save column stats
        stats = s.describe().to_dict()
        stats["column"] = col
        summary_data.append(stats)

        # Figure with improved UX
        plt.figure(figsize=(9, 6)) # Create a new figure with a specific size
        plt.hist(s, 
                 bins=args.bins,  # Number of bins
                 edgecolor="black", # Border color
                 color=colors[i % len(colors)], # Histogram color
                 alpha = 0.75, # Transparency
                 linewidth = 1.2) # Border line width
        plt.title(f"Histograma - {col}", fontsize=16, fontweight="bold", color="#333333")
        plt.xlabel(col, fontsize=14)
        plt.ylabel("Frecuencia", fontsize=14)
        plt.grid(axis="y", linestyle="--", alpha=0.5)
        plt.tight_layout()

        if args.show:
            plt.show()
        else:
            out_file = out_dir / f"hist_{col}_bins{args.bins}_{timestamp}.png"
            plt.savefig(out_file, bbox_inches="tight", dpi=120)
            plt.close()
            saved.append(out_file)

    # Save summary
    if summary_data:
        summary_df = pd.DataFrame(summary_data)
        summary_path = out_dir / f"resumen_{timestamp}.csv"
        summary_df.to_csv(summary_path, index=False)
        print(f"Resumen guardado en: {summary_path}")

    # Final Message
    if saved:
        print("Saved:")
        for f in saved:
            print(f" - {f}")

if __name__ == "__main__":
    main()
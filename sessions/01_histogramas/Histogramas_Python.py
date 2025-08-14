# sessions/01_histogramas/Histogramas_Python.py
# Session 1: Histograms from a CSV
# - Headless by default (saves PNGs into output/)
# - Use --column to plot a single numeric column; otherwise plots all numeric columns.
# - Robust CSV reading (auto-detects separator) and numeric coercion.
# - Optional time parsing (--timecol) to convert "mm:ss" etc. into seconds.

from pathlib import Path
import argparse
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

# Requires: ENV PYTHONPATH=/app (set in Dockerfile) and common/io.py present
from common.io import resolve_repo_path, ensure_dir


def parse_args():
    p = argparse.ArgumentParser(description="Session 1 - Histograms from a CSV.")
    p.add_argument("--csv", required=True, help="CSV path (repo-relative or absolute).")
    p.add_argument("--column", help="Numeric column to plot. If omitted, plots all numeric columns.")
    p.add_argument("--bins", type=int, default=10, help="Number of bins (default: 10).")
    p.add_argument("--outdir", default="output/01_histogramas", help="Output directory.")
    p.add_argument("--show", action="store_true", help="Show windows (local dev only; not for Docker).")
    # Optional helpers
    p.add_argument("--sep", help="CSV separator override (e.g., ',', ';', '\\t'). If omitted, auto-detect.")
    p.add_argument("--decimal", help="Decimal mark override, e.g., ',' for European CSVs.")
    p.add_argument("--timecol", help="Column with durations (e.g., 'mm:ss'); converts to seconds as <col>_seg.")
    return p.parse_args()


def read_csv_safely(csv_path: Path, sep: str | None, decimal: str | None) -> pd.DataFrame:
    # If user specifies sep/decimal, honor them; else auto-detect separator.
    read_kwargs = {}
    if sep is not None:
        read_kwargs["sep"] = sep
    else:
        read_kwargs["sep"] = None
        read_kwargs["engine"] = "python"  # needed for sep=None auto-detect

    if decimal is not None:
        read_kwargs["decimal"] = decimal

    df = pd.read_csv(csv_path, **read_kwargs)

    # Try to coerce any convertible column to numeric
    for col in df.columns:
        # errors='coerce' -> non-numeric -> NaN (so pandas can treat rest as numeric)
        coerced = pd.to_numeric(df[col], errors="coerce")
        # If coercion produced at least one non-NaN and changed dtype, keep it
        if coerced.notna().any():
            df[col] = coerced

    return df


def maybe_parse_time_seconds(df: pd.DataFrame, col: str) -> pd.DataFrame:
    """If 'col' exists, try parse durations to seconds and add <col>_seg."""
    if col not in df.columns:
        print(f"[info] --timecol '{col}' not found; skipping time parsing.")
        return df

    target = f"{col}_seg"
    try:
        # pandas handles formats like "mm:ss", "hh:mm:ss", "00:12:34.5"
        td = pd.to_timedelta(df[col], errors="coerce")
        if td.notna().any():
            df[target] = td.dt.total_seconds()
            print(f"[info] Created numeric time column: {target}")
        else:
            print(f"[info] Could not parse any durations in '{col}'.")
    except Exception as e:
        print(f"[warn] Failed to parse time in '{col}': {e}")
    return df


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
    df = read_csv_safely(repo_csv, sep=args.sep, decimal=args.decimal)

    # Optional: parse time column to seconds
    if args.timecol:
        df = maybe_parse_time_seconds(df, args.timecol)

    # Show quick info
    print(df.info())

    # Decide which columns to plot
    if args.column:
        if args.column not in df.columns:
            raise ValueError(f"Column '{args.column}' not found.")
        columns = [args.column]
    else:
        # numeric columns only
        columns = df.select_dtypes(include="number").columns.tolist()
        if not columns:
            # Help the user debug what pandas saw
            print("[debug] DataFrame dtypes:")
            print(df.dtypes)
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
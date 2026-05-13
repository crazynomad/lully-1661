"""Lully 1661 — merge multiple ZSBMS sales-export CSVs into one canonical file.

Use when:
- backfilling history in chunks (one .csv per quarter/year)
- weekly incremental sync (merge new window into the canonical CSV with
  a 14-day overlap to catch late edits / voids)

Dedupe key: (data, loja_num, codigo). When the same key appears in
multiple input files, the row from the LATER file wins — newer pulls
override older ones, which is what we want for retroactive corrections.

Usage:
    python3 scripts/merge-sales-csvs.py \\
        raw-requirements/data/zsbms-extract/chunks/*.csv \\
        --out raw-requirements/data/zsbms-extract/evo-vendas-produto-all.csv

Input CSVs are expected to share the schema emitted by parse-xls.py:
    data, loja_num, loja, codigo, produto, familia, sub_familia,
    quantidade, valor_sem_iva, valor_total
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd


SCHEMA = [
    "data", "loja_num", "loja", "codigo", "produto",
    "familia", "sub_familia", "quantidade", "valor_sem_iva", "valor_total",
]
DEDUPE_KEY = ["data", "loja_num", "codigo"]


def load_csv(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    missing = set(SCHEMA) - set(df.columns)
    if missing:
        sys.exit(f"error: {path.name} missing columns: {missing}")
    df["_source"] = path.name
    return df


def merge(paths: list[Path]) -> pd.DataFrame:
    """Concatenate inputs in file order and dedupe on (data, loja_num, codigo).

    The LAST occurrence wins — pass newer pulls later in the argument list
    if you want retroactive corrections to take effect.
    """
    frames = [load_csv(p) for p in paths]
    combined = pd.concat(frames, ignore_index=True)
    before = len(combined)
    deduped = combined.drop_duplicates(subset=DEDUPE_KEY, keep="last")
    after = len(deduped)
    print(f"merged {len(paths)} files: {before:,} rows → {after:,} after dedupe "
          f"({before - after:,} duplicates resolved)", file=sys.stderr)
    return deduped


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("inputs", type=Path, nargs="+",
                   help="one or more sales CSVs to merge (in date order, "
                        "oldest first; later files override earlier ones on "
                        "conflict)")
    p.add_argument("--out", type=Path, required=True,
                   help="output canonical CSV path")
    args = p.parse_args()

    for input_path in args.inputs:
        if not input_path.exists():
            sys.exit(f"error: input not found: {input_path}")

    merged = merge(args.inputs)
    merged = merged.drop(columns=["_source"]).sort_values(
        ["data", "loja_num", "codigo"]
    )
    merged.to_csv(args.out, index=False)

    n_days = merged["data"].nunique()
    n_lojas = merged["loja_num"].nunique()
    n_skus = merged["codigo"].nunique()
    revenue = merged["valor_total"].sum()
    print(
        f"→ {args.out.name}: {len(merged):,} rows · {n_days} dias · "
        f"{n_lojas} lojas · {n_skus} SKUs · €{revenue:,.0f}",
        file=sys.stderr,
    )


if __name__ == "__main__":
    main()

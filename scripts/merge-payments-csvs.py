"""Lully 1661 — merge ZSBMS payments-by-type chunks into one canonical CSV.

Third sibling of merge-sales-csvs.py / merge-tickets-csvs.py. Same
idempotent semantics, different schema and different dedupe key.

Input schema (from parse-payments-xls.py):
    data, loja_num, loja, tipo_pagamento, valor

Dedupe key: (data, loja_num, tipo_pagamento). When the same key appears
in multiple inputs, the row from the LATER file wins.

Usage:
    python3 scripts/merge-payments-csvs.py \\
        raw-requirements/data/zsbms-extract/chunks-payments/*.csv \\
        --out raw-requirements/data/zsbms-extract/payments-canonical.csv
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd


SCHEMA = ["data", "loja_num", "loja", "tipo_pagamento", "valor"]
DEDUPE_KEY = ["data", "loja_num", "tipo_pagamento"]


def load_csv(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    missing = set(SCHEMA) - set(df.columns)
    if missing:
        sys.exit(f"error: {path.name} missing columns: {missing}")
    df["_source"] = path.name
    return df


def merge(paths: list[Path]) -> pd.DataFrame:
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
                   help="one or more payments CSVs to merge (oldest first; "
                        "later files override earlier ones on conflict)")
    p.add_argument("--out", type=Path, required=True,
                   help="output canonical CSV path")
    args = p.parse_args()

    for ip in args.inputs:
        if not ip.exists():
            sys.exit(f"error: input not found: {ip}")

    merged = merge(args.inputs)
    merged = merged.drop(columns=["_source"]).sort_values(
        ["data", "loja_num", "tipo_pagamento"]
    )
    merged.to_csv(args.out, index=False)

    n_days = merged["data"].nunique()
    n_lojas = merged["loja_num"].nunique()
    n_types = merged["tipo_pagamento"].nunique()
    total = float(merged["valor"].sum())
    print(f"→ {args.out.name}: {len(merged):,} rows · {n_days} dias · "
          f"{n_lojas} lojas · {n_types} payment types · €{total:,.0f}",
          file=sys.stderr)


if __name__ == "__main__":
    main()

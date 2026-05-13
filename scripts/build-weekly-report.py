"""Lully 1661 — weekly client-format operational report.

Matches the existing client template (French, semaine X format):
4 sections (ALL STORES + Anjos + Campo + Beato), each with current /
S-1 / N-1 rows, columns for CA TTC / CA HT / Trafic / panier moyen /
Glovo / UberEats / Total E-Co, plus a cumul block.

v0 fills only the columns derivable from sales-canonical.csv (CA TTC,
CA HT, cumul, WoW / YoY deltas). Trafic, Glovo, UberEats and Pertes
are placeholder cells (the data lives in different ZSBMS reports —
ticket-level and Séries-filtered — and will be wired in once those
are backfilled).

Reads:  raw-requirements/data/zsbms-extract/sales-canonical.csv
Writes: raw-requirements/data/zsbms-extract/analysis/
            weekly-<week-end>.html

Run:    python3 scripts/build-weekly-report.py [--week-end DD-MM-YYYY]
        # default: most recent week ending in canonical
"""

from __future__ import annotations

import argparse
from datetime import date, timedelta
from pathlib import Path

import pandas as pd

REPO = Path(__file__).resolve().parent.parent
DATA = REPO / "raw-requirements" / "data" / "zsbms-extract"
OUT = DATA / "analysis"
OUT.mkdir(exist_ok=True)


# =========================================================================
# Number formatting (FR)
# =========================================================================
MONTHS_FR_LONG = ["janvier", "février", "mars", "avril", "mai", "juin",
                  "juillet", "août", "septembre", "octobre", "novembre", "décembre"]
MONTHS_FR_SHORT = ["jan", "fév", "mar", "avr", "mai", "juin",
                   "juil", "août", "sep", "oct", "nov", "déc"]


def fr_int(v: float) -> str:
    return f"{int(round(v)):,}".replace(",", " ")


def fr_money(v: float, decimals: int = 2) -> str:
    rounded = round(v, decimals)
    int_part = int(rounded)
    frac = abs(rounded - int_part)
    int_str = fr_int(int_part)
    if decimals:
        frac_str = f"{frac:.{decimals}f}"[2:]
        return f"{int_str},{frac_str} €"
    return f"{int_str} €"


def fr_pct(v: float, decimals: int = 2) -> str:
    s = f"{v:.{decimals}f}".replace(".", ",")
    return f"{s}%"


def fr_date_range(start: date, end: date) -> str:
    if start.month == end.month:
        return f"{start.day}–{end.day} {MONTHS_FR_LONG[end.month - 1]} {end.year}"
    return (f"{start.day} {MONTHS_FR_SHORT[start.month - 1]} – "
            f"{end.day} {MONTHS_FR_SHORT[end.month - 1]} {end.year}")


# =========================================================================
# Load data
# =========================================================================
df = pd.read_csv(DATA / "sales-canonical.csv")
df["data"] = pd.to_datetime(df["data"], format="%d-%m-%Y").dt.date

# Client uses "Campo" for what we call "Ourique"
LOJA_LABEL = {"Anjos": "Anjos", "Ourique": "Campo", "Beato": "Beato"}


def window_totals(start: date, end: date, loja: str | None = None) -> dict:
    """Aggregate canonical rows in [start, end] (inclusive) for one loja
    or all stores combined. Returns dict with the metrics we can compute."""
    sub = df[(df["data"] >= start) & (df["data"] <= end)]
    if loja:
        sub = sub[sub["loja"] == loja]
    return {
        "ca_ttc": float(sub["valor_total"].sum()),
        "ca_ht": float(sub["valor_sem_iva"].sum()),
        "n_lines": len(sub),  # not Trafic — placeholder marker
    }


# =========================================================================
# Build week / S-1 / N-1 windows
# =========================================================================
def render_report(week_end: date) -> str:
    week_start = week_end - timedelta(days=6)
    s1_end = week_end - timedelta(days=7)
    s1_start = week_start - timedelta(days=7)
    n1_end = date(week_end.year - 1, week_end.month, week_end.day)
    n1_start = date(week_start.year - 1, week_start.month, week_start.day)

    # Month-to-date and year-to-date for cumul block
    month_start = date(week_end.year, week_end.month, 1)
    year_start = date(week_end.year, 1, 1)
    month_start_n1 = date(week_end.year - 1, week_end.month, 1)
    year_start_n1 = date(week_end.year - 1, 1, 1)
    n1_today = date(week_end.year - 1, week_end.month, week_end.day)

    sections = []
    for label, loja in [("ALL STORES", None), ("Anjos", "Anjos"),
                        ("Campo", "Ourique"), ("Beato", "Beato")]:
        cur = window_totals(week_start, week_end, loja)
        s1 = window_totals(s1_start, s1_end, loja)
        n1 = window_totals(n1_start, n1_end, loja)
        sections.append({"label": label, "cur": cur, "s1": s1, "n1": n1})

    cumul = {
        "mensuel_cur": window_totals(month_start, week_end)["ca_ht"],
        "mensuel_n1": window_totals(month_start_n1, n1_today)["ca_ht"],
        "anuel_cur": window_totals(year_start, week_end)["ca_ht"],
        "anuel_n1": window_totals(year_start_n1, n1_today)["ca_ht"],
    }

    # Render HTML
    return render_html(
        week_start, week_end, s1_start, s1_end, n1_start, n1_end,
        sections, cumul,
    )


# =========================================================================
# HTML rendering
# =========================================================================
CSS = """
:root {
  --paper: #f4eedf;
  --paper-2: #efe6d4;
  --ink: #1a1613;
  --ink-2: #3c342e;
  --stone: #7a746b;
  --gold: #a68a3e;
  --ember: #b8563d;
  --rule: rgba(26, 22, 19, 0.18);
  --gain: #2e7d32;
  --loss: #c62828;
  --placeholder: #c9c0aa;
}
* { box-sizing: border-box; }
html, body { background: var(--paper); margin: 0; padding: 0; }
body {
  font-family: 'Helvetica Neue', Arial, sans-serif;
  color: var(--ink);
  font-size: 13px;
  line-height: 1.4;
  padding: 32px;
}
header {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  margin-bottom: 24px;
  padding-bottom: 14px;
  border-bottom: 1px solid var(--rule);
}
header h1 {
  font-family: Georgia, 'Times New Roman', serif;
  font-style: italic;
  font-weight: 400;
  margin: 0;
  font-size: 22px;
  color: var(--ink);
}
header .meta {
  font-size: 11px;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: var(--stone);
}
table.weekly {
  width: 100%;
  border-collapse: collapse;
  margin: 0 0 24px;
  font-variant-numeric: tabular-nums;
  font-size: 12px;
}
table.weekly caption {
  text-align: left;
  font-weight: 600;
  letter-spacing: 0.04em;
  padding: 12px 8px 6px;
  background: var(--paper-2);
  color: var(--ink);
  border-top: 2px solid var(--gold);
}
table.weekly th, table.weekly td {
  padding: 6px 8px;
  border-bottom: 1px solid var(--rule);
  text-align: right;
  white-space: nowrap;
}
table.weekly th {
  font-size: 10px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--stone);
  font-weight: 500;
  text-align: right;
  background: var(--paper-2);
}
table.weekly th:first-child, table.weekly td:first-child {
  text-align: left;
}
table.weekly tr.row-period td:first-child {
  font-weight: 600;
  color: var(--ink);
}
table.weekly tr.row-delta td {
  color: var(--stone);
  font-size: 11px;
  border-bottom: 1px solid rgba(26, 22, 19, 0.08);
}
table.weekly tr.row-delta td.gain { color: var(--gain); }
table.weekly tr.row-delta td.loss { color: var(--loss); }
table.weekly td.placeholder {
  color: var(--placeholder);
  font-style: italic;
}
table.cumul {
  width: 100%;
  border-collapse: collapse;
  font-variant-numeric: tabular-nums;
  font-size: 12px;
  margin: 8px 0 24px;
  border-top: 1px solid var(--rule);
  border-bottom: 1px solid var(--rule);
}
table.cumul td {
  padding: 10px 12px;
  border-right: 1px solid var(--rule);
}
table.cumul td:last-child { border-right: 0; }
table.cumul td .label {
  display: block;
  font-size: 10px;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--stone);
  margin-bottom: 4px;
}
table.cumul td .value { font-weight: 600; color: var(--ink); }
table.cumul td .compare { color: var(--stone); font-size: 11px; margin-left: 6px; }
.footnote {
  margin-top: 16px;
  font-size: 11px;
  color: var(--stone);
  font-style: italic;
  border-top: 1px dashed var(--rule);
  padding-top: 14px;
}
.footnote strong { color: var(--ember); font-style: normal; }
"""


COLUMNS = [
    ("CA TTC",      "ca_ttc"),
    ("CA HT",       "ca_ht"),
    ("Trafic",      "trafic"),         # placeholder
    ("Panier moyen", "panier"),         # placeholder (needs trafic)
    ("Panier moyen HT", "panier_ht"),   # placeholder
    ("Dont Glovo (€)", "glovo_eur"),    # placeholder
    ("Nbre orders", "glovo_n"),         # placeholder
    ("Panier Glovo", "glovo_panier"),   # placeholder
    ("Dont UberEats (€)", "ue_eur"),    # placeholder
    ("Nbre orders ", "ue_n"),           # placeholder (trailing space to dedupe key)
    ("Panier UE",   "ue_panier"),       # placeholder
    ("Total E-Co",  "ecom_total"),      # placeholder
]


def pct_delta(cur: float, prev: float) -> tuple[str, str]:
    """Return (formatted_pct, css_class)."""
    if prev == 0:
        return ("—", "")
    delta = (cur - prev) / prev * 100
    sign = "+" if delta >= 0 else ""
    return (f"{sign}{fr_pct(delta, 2)}", "gain" if delta >= 0 else "loss")


def metric_cell(key: str, vals: dict) -> str:
    """Render a single cell. Placeholders for missing fields."""
    if key in ("ca_ttc", "ca_ht"):
        v = vals[key]
        return f"<td>{fr_money(v)}</td>"
    return '<td class="placeholder">—</td>'


def delta_cell(key: str, cur_vals: dict, prev_vals: dict) -> str:
    if key in ("ca_ttc", "ca_ht") and prev_vals[key]:
        s, cls = pct_delta(cur_vals[key], prev_vals[key])
        return f'<td class="{cls}">{s}</td>'
    return '<td class="placeholder">—</td>'


def render_section(s: dict, periods: dict) -> str:
    rows = []
    rows.append(f'<tr class="row-period"><td>{periods["cur_label"]}</td>'
                + "".join(metric_cell(k, s["cur"]) for _, k in COLUMNS)
                + "</tr>")
    rows.append(f'<tr class="row-period"><td>VS S-1 ({periods["s1_label"]})</td>'
                + "".join(metric_cell(k, s["s1"]) for _, k in COLUMNS)
                + "</tr>")
    rows.append('<tr class="row-delta"><td>Δ S-1</td>'
                + "".join(delta_cell(k, s["cur"], s["s1"]) for _, k in COLUMNS)
                + "</tr>")
    rows.append(f'<tr class="row-period"><td>VS N-1 ({periods["n1_label"]})</td>'
                + "".join(metric_cell(k, s["n1"]) for _, k in COLUMNS)
                + "</tr>")
    rows.append('<tr class="row-delta"><td>Δ N-1</td>'
                + "".join(delta_cell(k, s["cur"], s["n1"]) for _, k in COLUMNS)
                + "</tr>")

    return f"""
<table class="weekly">
  <caption>{s['label']}</caption>
  <thead><tr><th>Période</th>{"".join(f"<th>{lbl}</th>" for lbl, _ in COLUMNS)}</tr></thead>
  <tbody>{"".join(rows)}</tbody>
</table>"""


def render_html(week_start, week_end, s1_start, s1_end, n1_start, n1_end,
                sections, cumul) -> str:
    periods = {
        "cur_label": fr_date_range(week_start, week_end),
        "s1_label": fr_date_range(s1_start, s1_end),
        "n1_label": fr_date_range(n1_start, n1_end),
    }

    sections_html = "\n".join(render_section(s, periods) for s in sections)

    mensuel_delta_pct, mensuel_cls = pct_delta(cumul["mensuel_cur"], cumul["mensuel_n1"])
    anuel_delta_pct, anuel_cls = pct_delta(cumul["anuel_cur"], cumul["anuel_n1"])

    cumul_html = f"""
<table class="cumul">
  <tr>
    <td>
      <span class="label">Cumul mensuel HT</span>
      <span class="value">{fr_money(cumul["mensuel_cur"], decimals=0)}</span>
      <span class="compare">N-1 {fr_money(cumul["mensuel_n1"], decimals=0)}
        <span class="{mensuel_cls}">({mensuel_delta_pct})</span>
      </span>
    </td>
    <td>
      <span class="label">Cumul annuel HT</span>
      <span class="value">{fr_money(cumul["anuel_cur"], decimals=0)}</span>
      <span class="compare">N-1 {fr_money(cumul["anuel_n1"], decimals=0)}
        <span class="{anuel_cls}">({anuel_delta_pct})</span>
      </span>
    </td>
    <td>
      <span class="label">Cumul trafic</span>
      <span class="value placeholder">—</span>
      <span class="compare">N-1 —</span>
    </td>
    <td>
      <span class="label">Pertes</span>
      <span class="value placeholder">Anjos — · Campo —</span>
    </td>
  </tr>
</table>"""

    return f"""<!doctype html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <title>Lully 1661 — Rapport hebdomadaire {periods["cur_label"]}</title>
  <style>{CSS}</style>
</head>
<body>
  <header>
    <h1>Lully 1661 — <em>rapport hebdomadaire</em></h1>
    <span class="meta">{periods["cur_label"]}</span>
  </header>

  {sections_html}

  {cumul_html}

  <p class="footnote">
    <strong>v0 — données partielles.</strong> Les colonnes
    <strong>CA TTC, CA HT</strong> et les cumuls HT viennent du POS ZSBMS
    (sales-canonical.csv). <strong>Trafic, Glovo, UberEats, Pertes</strong>
    nécessitent des rapports ZSBMS différents (tickets, Séries) qui ne sont
    pas encore intégrés au pipeline — à venir dans la v1.
  </p>
</body>
</html>
"""


# =========================================================================
# CLI
# =========================================================================
def main() -> None:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("--week-end", type=str, default=None,
                   help="last day of the week to report (DD-MM-YYYY). "
                        "Default: 04-05-2026 (matches client conversation).")
    args = p.parse_args()

    if args.week_end:
        d, m, y = map(int, args.week_end.split("-"))
        week_end = date(y, m, d)
    else:
        week_end = date(2026, 5, 4)

    html = render_report(week_end)
    fname = f"weekly-{week_end.isoformat()}.html"
    (OUT / fname).write_text(html, encoding="utf-8")
    print(f"→ {fname}")


if __name__ == "__main__":
    main()

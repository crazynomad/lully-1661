"""Lully 1661 — 2026 year-to-date weekly dashboard.

Renders an at-a-glance HTML page covering every complete Mon-Sun week of
2026, with:

    1. Headline cumul block (mensuel + annuel HT + trafic)
    2. Three brand-styled matplotlib line charts (weekly resolution):
         - Revenue (TTC): total + per-store on the same axes
         - Number of tickets: total + per-store
         - Average ticket (TTC): total + per-store
    3. A weekly KPI summary table
    4. Drill-down links to each per-week detailed FR report

Per-week reports are produced by re-running scripts/build-weekly-report.py
via subprocess for each Sunday week-end date.

Reads:
    raw-requirements/data/zsbms-extract/sales-canonical.csv
    raw-requirements/data/zsbms-extract/tickets-canonical.csv

Writes:
    raw-requirements/data/zsbms-extract/analysis/weekly-ytd-2026/
        ├── index.html                      ← dashboard
        ├── chart-revenue.png
        ├── chart-tickets.png
        ├── chart-avg-ticket.png
        └── weekly-YYYY-MM-DD.html × 19     ← per-week details
"""

from __future__ import annotations

import datetime as dt
import subprocess
import sys
from pathlib import Path

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd

REPO = Path(__file__).resolve().parent.parent
DATA = REPO / "raw-requirements" / "data" / "zsbms-extract"
OUT = DATA / "analysis" / "weekly-ytd-2026"
OUT.mkdir(parents=True, exist_ok=True)


# =========================================================================
# Brand
# =========================================================================
PAPER = "#f4eedf"
PAPER_2 = "#efe6d4"
INK = "#1a1613"
INK_2 = "#3c342e"
STONE = "#7a746b"
GOLD = "#a68a3e"
EMBER = "#b8563d"

LOJA_COLOR = {"Total": INK, "Anjos": EMBER, "Ourique": GOLD, "Beato": INK_2}
LOJA_LABEL_FR = {"Anjos": "Anjos", "Ourique": "Campo", "Beato": "Beato"}


def apply_brand(ax) -> None:
    ax.set_facecolor(PAPER)
    ax.tick_params(colors=INK_2, labelsize=9)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    for spine in ("left", "bottom"):
        ax.spines[spine].set_color(STONE)
        ax.spines[spine].set_linewidth(0.8)
    ax.title.set_color(INK)


# =========================================================================
# 1. Compute weekly aggregates
# =========================================================================
sales = pd.read_csv(DATA / "sales-canonical.csv")
sales["data"] = pd.to_datetime(sales["data"], format="%d-%m-%Y").dt.date

tickets = pd.read_csv(DATA / "tickets-canonical.csv")
tickets["data"] = pd.to_datetime(tickets["data"], format="%d-%m-%Y").dt.date

# Build list of Mon-Sun weeks ending in 2026, latest Sunday with full data.
year_start = dt.date(2026, 1, 1)
# First Sunday of 2026: Jan 4
first_sun = dt.date(2026, 1, 4)
# Last completed Sunday: Sundays up to (canonical max - 1 day)
data_max = max(sales["data"].max(), tickets["data"].max())
last_sun = data_max
while last_sun.weekday() != 6:  # 0=Mon..6=Sun
    last_sun -= dt.timedelta(days=1)

weeks: list[dict] = []
sun = first_sun
while sun <= last_sun:
    mon = sun - dt.timedelta(days=6)
    week = {"week_end": sun, "week_start": mon}
    # Per-loja + total
    for loja_name in ("Anjos", "Ourique", "Beato"):
        s = sales[(sales["data"] >= mon) & (sales["data"] <= sun) & (sales["loja"] == loja_name)]
        t = tickets[(tickets["data"] >= mon) & (tickets["data"] <= sun) & (tickets["loja"] == loja_name)]
        rev = float(s["valor_total"].sum())
        trafic = int(t["docs_emitidos"].sum())
        week[f"{loja_name}_rev"] = rev
        week[f"{loja_name}_trafic"] = trafic
        week[f"{loja_name}_avg"] = rev / trafic if trafic else 0.0
    s_all = sales[(sales["data"] >= mon) & (sales["data"] <= sun)]
    t_all = tickets[(tickets["data"] >= mon) & (tickets["data"] <= sun)]
    total_rev = float(s_all["valor_total"].sum())
    total_trafic = int(t_all["docs_emitidos"].sum())
    week["Total_rev"] = total_rev
    week["Total_trafic"] = total_trafic
    week["Total_avg"] = total_rev / total_trafic if total_trafic else 0.0
    weeks.append(week)
    sun += dt.timedelta(days=7)

print(f"Computing {len(weeks)} weeks from {weeks[0]['week_start']} to {weeks[-1]['week_end']}",
      file=sys.stderr)

# Pandas DataFrame for plotting
df_weeks = pd.DataFrame(weeks)


# =========================================================================
# 2. Three line charts
# =========================================================================
def chart(metric_suffix: str, ylabel: str, title: str, fname: str,
          fmt: str = "money") -> None:
    """metric_suffix: '_rev' / '_trafic' / '_avg'."""
    fig, ax = plt.subplots(figsize=(11, 4.2), facecolor=PAPER)
    x = df_weeks["week_end"]
    # Per-store first, total last (so total renders on top)
    for loja in ("Beato", "Ourique", "Anjos"):
        ax.plot(x, df_weeks[f"{loja}{metric_suffix}"],
                color=LOJA_COLOR[loja], linewidth=1.5, marker="o", markersize=4,
                label=LOJA_LABEL_FR[loja])
    ax.plot(x, df_weeks[f"Total{metric_suffix}"],
            color=INK, linewidth=2.5, marker="o", markersize=5, label="Total")

    ax.set_title(title, pad=14, fontsize=13, weight="bold")
    ax.set_ylabel(ylabel, color=INK_2, fontsize=10)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d %b"))
    ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.SU, interval=2))
    plt.setp(ax.get_xticklabels(), rotation=0, ha="center")
    apply_brand(ax)

    # Y-axis formatting
    if fmt == "money":
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{int(v):,} €".replace(",", " ")))
    elif fmt == "int":
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{int(v):,}".replace(",", " ")))
    elif fmt == "avg":
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.2f} €"))

    ax.legend(loc="upper left", frameon=False, fontsize=9, ncol=4)
    ax.grid(True, alpha=0.15, linestyle="--", linewidth=0.5)
    plt.tight_layout()
    plt.savefig(OUT / fname, dpi=140, facecolor=PAPER, bbox_inches="tight")
    plt.close()
    print(f"→ {fname}", file=sys.stderr)


chart("_rev", "Chiffre d'affaires (TTC)",
      "Évolution du chiffre d'affaires hebdomadaire — 2026 YTD",
      "chart-revenue.png", fmt="money")
chart("_trafic", "Nombre de tickets",
      "Évolution du trafic hebdomadaire (tickets émis) — 2026 YTD",
      "chart-tickets.png", fmt="int")
chart("_avg", "Panier moyen (TTC)",
      "Évolution du panier moyen hebdomadaire — 2026 YTD",
      "chart-avg-ticket.png", fmt="avg")


# =========================================================================
# 3. Per-week detail HTMLs (subprocess)
# =========================================================================
print(f"\nGenerating {len(weeks)} per-week detail reports...", file=sys.stderr)
for w in weeks:
    week_end = w["week_end"]
    cmd = [
        sys.executable, str(REPO / "scripts" / "build-weekly-report.py"),
        "--week-end", week_end.strftime("%d-%m-%Y"),
        "--out-dir", str(OUT),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  ERROR week_end={week_end}: {result.stderr.strip()}", file=sys.stderr)


# =========================================================================
# 4. Dashboard HTML
# =========================================================================
MONTHS_FR_LONG = ["janvier", "février", "mars", "avril", "mai", "juin",
                  "juillet", "août", "septembre", "octobre", "novembre", "décembre"]
MONTHS_FR_SHORT = ["jan", "fév", "mar", "avr", "mai", "juin",
                   "juil", "août", "sep", "oct", "nov", "déc"]


def fr_int(v: float) -> str:
    return f"{int(round(v)):,}".replace(",", " ")


def fr_money(v: float, decimals: int = 0) -> str:
    if decimals:
        rounded = round(v, decimals)
        int_part = int(rounded)
        frac = abs(rounded - int_part)
        frac_str = f"{frac:.{decimals}f}"[2:]
        return f"{fr_int(int_part)},{frac_str} €"
    return f"{fr_int(v)} €"


def fr_pct(v: float, decimals: int = 1) -> str:
    s = f"{v:.{decimals}f}".replace(".", ",")
    return f"{s}%"


def fr_week_range(start: dt.date, end: dt.date) -> str:
    m1 = MONTHS_FR_SHORT[start.month - 1]
    m2 = MONTHS_FR_SHORT[end.month - 1]
    if start.month == end.month:
        return f"{start.day}–{end.day} {m2}"
    return f"{start.day} {m1} – {end.day} {m2}"


# Year-to-date cumul
ytd_end = weeks[-1]["week_end"]
ytd_start = dt.date(2026, 1, 1)
ytd_n1_start = dt.date(2025, 1, 1)
ytd_n1_end = dt.date(2025, ytd_end.month, ytd_end.day)

ytd_sales = sales[(sales["data"] >= ytd_start) & (sales["data"] <= ytd_end)]
ytd_tickets = tickets[(tickets["data"] >= ytd_start) & (tickets["data"] <= ytd_end)]
ytd_sales_n1 = sales[(sales["data"] >= ytd_n1_start) & (sales["data"] <= ytd_n1_end)]
ytd_tickets_n1 = tickets[(tickets["data"] >= ytd_n1_start) & (tickets["data"] <= ytd_n1_end)]

cumul_ht = float(ytd_sales["valor_sem_iva"].sum())
cumul_ht_n1 = float(ytd_sales_n1["valor_sem_iva"].sum())
cumul_trafic = int(ytd_tickets["docs_emitidos"].sum())
cumul_trafic_n1 = int(ytd_tickets_n1["docs_emitidos"].sum())

ht_yoy = (cumul_ht - cumul_ht_n1) / cumul_ht_n1 * 100 if cumul_ht_n1 else 0
trafic_yoy = (cumul_trafic - cumul_trafic_n1) / cumul_trafic_n1 * 100 if cumul_trafic_n1 else 0


# Weekly KPI table rows
def wow_delta(values: list[float], i: int) -> tuple[str, str]:
    """Return (formatted_pct, css_class) comparing values[i] to values[i-1]."""
    if i == 0 or not values[i - 1]:
        return "—", ""
    delta = (values[i] - values[i - 1]) / values[i - 1] * 100
    sign = "+" if delta >= 0 else ""
    return f"{sign}{fr_pct(delta, 1)}", "gain" if delta >= 0 else "loss"


revenues = [w["Total_rev"] for w in weeks]
trafics = [w["Total_trafic"] for w in weeks]
avgs = [w["Total_avg"] for w in weeks]

table_rows = []
for i, w in enumerate(weeks):
    rev_d, rev_cls = wow_delta(revenues, i)
    tra_d, tra_cls = wow_delta([float(x) for x in trafics], i)
    avg_d, avg_cls = wow_delta(avgs, i)
    week_link = f"weekly-{w['week_end'].isoformat()}.html"
    table_rows.append(f"""
      <tr>
        <td><a href="{week_link}">{fr_week_range(w['week_start'], w['week_end'])}</a></td>
        <td class="num">{fr_money(w['Total_rev'])}</td>
        <td class="num {rev_cls}">{rev_d}</td>
        <td class="num">{fr_int(w['Total_trafic'])}</td>
        <td class="num {tra_cls}">{tra_d}</td>
        <td class="num">{fr_money(w['Total_avg'], decimals=2)}</td>
        <td class="num {avg_cls}">{avg_d}</td>
      </tr>""")


# Drill-down grid (per-week links)
drill_links = []
for w in weeks:
    label = fr_week_range(w["week_start"], w["week_end"])
    drill_links.append(
        f'<a class="drill-link" href="weekly-{w["week_end"].isoformat()}.html">'
        f'<span class="drill-label">S{(w["week_end"].isocalendar()[1]):02d}</span>'
        f'<span class="drill-date">{label}</span>'
        f'<span class="drill-rev">{fr_money(w["Total_rev"])}</span>'
        f'</a>'
    )


CSS = """
:root {
  --paper: #f4eedf;
  --paper-2: #efe6d4;
  --ink: #1a1613;
  --ink-2: #3c342e;
  --stone: #7a746b;
  --gold: #a68a3e;
  --gold-2: #c2a04a;
  --ember: #b8563d;
  --rule: rgba(26, 22, 19, 0.14);
  --rule-strong: rgba(26, 22, 19, 0.28);
  --gain: #2e7d32;
  --loss: #c62828;
  --font-display: 'Fraunces', Georgia, 'Times New Roman', serif;
  --font-accent: 'Instrument Serif', Georgia, serif;
  --font-body: 'Instrument Sans', system-ui, -apple-system, sans-serif;
}
* { box-sizing: border-box; }
html, body { background: var(--paper); margin: 0; }
body {
  color: var(--ink);
  font-family: var(--font-body);
  font-size: 14px;
  line-height: 1.55;
  -webkit-font-smoothing: antialiased;
}
.shell { max-width: 1100px; margin: 0 auto; padding: 0 32px; }
@media (max-width: 720px) { .shell { padding: 0 20px; } }

header.topbar {
  padding: 22px 32px;
  border-bottom: 1px solid var(--rule);
  display: flex; justify-content: space-between; align-items: baseline;
}
header.topbar .brand {
  font-family: var(--font-display);
  font-variation-settings: "opsz" 144;
  font-size: 22px;
  text-transform: lowercase;
  letter-spacing: 0.04em;
}
header.topbar .brand em { font-style: italic; color: var(--ember); font-family: var(--font-accent); }
header.topbar .doc-id {
  font-size: 11px;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  color: var(--stone);
}

section { padding: 60px 0; border-bottom: 1px solid var(--rule); }
section.compact { padding: 40px 0; }

.eyebrow {
  font-size: 11px;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  color: var(--gold);
  font-weight: 500;
  margin-bottom: 14px;
  display: inline-block;
}
h1.display, h2.display {
  font-family: var(--font-display);
  font-weight: 400;
  font-variation-settings: "opsz" 144;
  color: var(--ink);
  letter-spacing: -0.01em;
  margin: 0 0 16px;
  line-height: 1.08;
}
h1.display { font-size: clamp(34px, 5vw, 46px); margin-bottom: 22px; }
h2.display { font-size: clamp(24px, 3.4vw, 32px); }
h1.display em, h2.display em {
  font-family: var(--font-accent);
  font-style: italic;
  color: var(--ember);
}

p.lead { font-size: 16px; color: var(--ink-2); max-width: 64ch; margin: 0 0 14px; }

/* --- KPI strip --- */
.kpis {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 0;
  margin-top: 24px;
  border-top: 1px solid var(--rule);
  border-bottom: 1px solid var(--rule);
}
@media (max-width: 720px) { .kpis { grid-template-columns: 1fr; } }
.kpi { padding: 28px 22px; border-right: 1px solid var(--rule); }
.kpi:last-child { border-right: 0; }
@media (max-width: 720px) { .kpi { border-right: 0; border-bottom: 1px solid var(--rule); } .kpi:last-child { border-bottom: 0; } }
.kpi .kpi-label {
  font-size: 10px;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  color: var(--stone);
  margin-bottom: 8px;
}
.kpi .kpi-value {
  font-family: var(--font-display);
  font-variation-settings: "opsz" 72;
  font-weight: 400;
  font-size: clamp(28px, 3.2vw, 36px);
  line-height: 1;
  color: var(--ink);
  font-variant-numeric: tabular-nums;
}
.kpi .kpi-yoy {
  margin-top: 8px;
  font-size: 13px;
  color: var(--stone);
  font-family: var(--font-accent);
  font-style: italic;
}
.kpi .kpi-yoy .delta { font-family: var(--font-body); font-style: normal; font-weight: 600; }
.kpi .kpi-yoy .gain { color: var(--gain); }
.kpi .kpi-yoy .loss { color: var(--loss); }

/* --- Charts --- */
figure.chart {
  margin: 24px 0;
  background: var(--paper);
  border: 1px solid var(--rule);
  padding: 12px;
}
figure.chart img { display: block; width: 100%; height: auto; }
figure.chart figcaption {
  margin-top: 8px;
  font-family: var(--font-accent);
  font-style: italic;
  color: var(--stone);
  font-size: 13px;
  text-align: center;
}

/* --- Table --- */
table.weekly-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 24px;
  font-variant-numeric: tabular-nums;
  font-size: 13px;
}
table.weekly-table th, table.weekly-table td {
  padding: 10px 12px;
  text-align: left;
  border-bottom: 1px solid var(--rule);
  vertical-align: middle;
}
table.weekly-table th {
  font-size: 10px;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: var(--stone);
  font-weight: 500;
  border-bottom: 1px solid var(--rule-strong);
  background: var(--paper-2);
}
table.weekly-table td.num { text-align: right; }
table.weekly-table td.gain { color: var(--gain); }
table.weekly-table td.loss { color: var(--loss); }
table.weekly-table td a {
  color: var(--ink);
  text-decoration: none;
  border-bottom: 1px solid transparent;
  transition: border-color 160ms;
}
table.weekly-table td a:hover {
  border-bottom-color: var(--gold);
}

/* --- Drill grid --- */
.drill-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(170px, 1fr));
  gap: 8px;
  margin-top: 16px;
}
.drill-link {
  display: flex;
  flex-direction: column;
  padding: 12px 14px;
  border: 1px solid var(--rule);
  background: var(--paper);
  text-decoration: none;
  color: var(--ink);
  transition: border-color 160ms, background 160ms;
}
.drill-link:hover { border-color: var(--gold); background: var(--paper-2); }
.drill-link .drill-label {
  font-size: 10px;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: var(--gold);
  font-weight: 500;
}
.drill-link .drill-date {
  margin-top: 2px;
  font-size: 13px;
  color: var(--ink-2);
}
.drill-link .drill-rev {
  margin-top: 4px;
  font-family: var(--font-display);
  font-variation-settings: "opsz" 60;
  font-size: 17px;
  color: var(--ink);
  font-variant-numeric: tabular-nums;
}

footer.site {
  background: var(--ink);
  color: var(--paper);
  padding: 40px 32px;
}
footer.site .shell { display: flex; justify-content: space-between; align-items: baseline; gap: 16px; flex-wrap: wrap; }
footer.site .brand {
  font-family: var(--font-display);
  font-variation-settings: "opsz" 96;
  font-size: 18px;
  text-transform: lowercase;
  letter-spacing: 0.04em;
}
footer.site .brand em { color: var(--gold-2); font-family: var(--font-accent); font-style: italic; }
footer.site .meta {
  font-size: 11px;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: rgba(244, 238, 223, 0.5);
}

@media print {
  body { background: white; font-size: 11pt; }
  header.topbar, footer.site { background: white; color: black; }
  section { padding: 24px 0; break-inside: avoid-page; }
  figure.chart { break-inside: avoid; }
  table.weekly-table { break-inside: avoid; }
  .drill-grid { display: none; }
}
"""


yoy_ht_cls = "gain" if ht_yoy >= 0 else "loss"
yoy_trafic_cls = "gain" if trafic_yoy >= 0 else "loss"


HTML = f"""<!doctype html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Lully 1661 — Tableau de bord hebdomadaire 2026</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300..900;1,9..144,300..900&family=Instrument+Serif:ital@0;1&family=Instrument+Sans:ital,wght@0,400..700;1,400..700&display=swap">
  <style>{CSS}</style>
</head>
<body>
  <header class="topbar">
    <div class="brand">lully <em>1661</em></div>
    <div class="doc-id">Tableau de bord · {len(weeks)} semaines · 2026 YTD</div>
  </header>

  <section>
    <div class="shell">
      <div class="eyebrow">Tableau de bord hebdomadaire</div>
      <h1 class="display">2026 en {len(weeks)} semaines, <em>par boutique.</em></h1>
      <p class="lead">Tendances hebdomadaires depuis le 1<sup>er</sup> janvier 2026 jusqu'au {fr_week_range(weeks[-1]['week_start'], weeks[-1]['week_end'])}. Cumul HT, trafic et panier moyen — par boutique et au global.</p>

      <div class="kpis">
        <div class="kpi">
          <div class="kpi-label">Cumul HT (2026 YTD)</div>
          <div class="kpi-value">{fr_money(cumul_ht)}</div>
          <div class="kpi-yoy">N-1: {fr_money(cumul_ht_n1)} · <span class="delta {yoy_ht_cls}">{'+' if ht_yoy>=0 else ''}{fr_pct(ht_yoy, 1)}</span></div>
        </div>
        <div class="kpi">
          <div class="kpi-label">Trafic cumulé</div>
          <div class="kpi-value">{fr_int(cumul_trafic)}</div>
          <div class="kpi-yoy">N-1: {fr_int(cumul_trafic_n1)} · <span class="delta {yoy_trafic_cls}">{'+' if trafic_yoy>=0 else ''}{fr_pct(trafic_yoy, 1)}</span></div>
        </div>
        <div class="kpi">
          <div class="kpi-label">Panier moyen (moyen pondéré)</div>
          <div class="kpi-value">{fr_money(cumul_ht / cumul_trafic, decimals=2) if cumul_trafic else '—'}</div>
          <div class="kpi-yoy">N-1: {fr_money(cumul_ht_n1 / cumul_trafic_n1, decimals=2) if cumul_trafic_n1 else '—'}</div>
        </div>
      </div>
    </div>
  </section>

  <section>
    <div class="shell">
      <div class="eyebrow">Graphiques</div>
      <h2 class="display">Trois courbes, <em>une lecture.</em></h2>

      <figure class="chart">
        <img src="chart-revenue.png" alt="Chiffre d'affaires hebdomadaire par boutique">
        <figcaption>Chiffre d'affaires hebdomadaire (TTC) — total + 3 boutiques</figcaption>
      </figure>

      <figure class="chart">
        <img src="chart-tickets.png" alt="Trafic hebdomadaire par boutique">
        <figcaption>Nombre de tickets émis par semaine — total + 3 boutiques</figcaption>
      </figure>

      <figure class="chart">
        <img src="chart-avg-ticket.png" alt="Panier moyen hebdomadaire par boutique">
        <figcaption>Panier moyen hebdomadaire (TTC) — total + 3 boutiques</figcaption>
      </figure>
    </div>
  </section>

  <section>
    <div class="shell">
      <div class="eyebrow">Tableau récapitulatif</div>
      <h2 class="display">Semaine par semaine, <em>au global.</em></h2>
      <p class="lead">Variations semaine-sur-semaine (Δ) sur les trois indicateurs. Cliquez sur une semaine pour ouvrir le rapport détaillé.</p>

      <table class="weekly-table">
        <thead>
          <tr>
            <th>Semaine</th>
            <th class="num">CA TTC</th>
            <th class="num">Δ S-1</th>
            <th class="num">Trafic</th>
            <th class="num">Δ S-1</th>
            <th class="num">Panier moyen</th>
            <th class="num">Δ S-1</th>
          </tr>
        </thead>
        <tbody>{"".join(table_rows)}</tbody>
      </table>
    </div>
  </section>

  <section class="compact">
    <div class="shell">
      <div class="eyebrow">Rapports détaillés par semaine</div>
      <h2 class="display">{len(weeks)} rapports, <em>un clic.</em></h2>
      <p class="lead">Chaque rapport est au format complet (4 sections boutique + cumul mensuel/annuel/trafic + Δ S-1 / Δ N-1).</p>
      <div class="drill-grid">{"".join(drill_links)}</div>
    </div>
  </section>

  <footer class="site">
    <div class="shell">
      <div class="brand">lully <em>1661</em> · tableau de bord 2026</div>
      <div class="meta">généré le {dt.date.today().isoformat()} · {len(weeks)} semaines · YTD HT {fr_money(cumul_ht)}</div>
    </div>
  </footer>
</body>
</html>
"""

(OUT / "index.html").write_text(HTML, encoding="utf-8")
print(f"\n→ {OUT.relative_to(REPO)}/index.html", file=sys.stderr)
print(f"   {len(weeks)} weekly reports + 3 charts + dashboard", file=sys.stderr)

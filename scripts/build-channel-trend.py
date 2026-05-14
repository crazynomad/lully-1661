"""Lully 1661 — Channel receivables weekly trend (2026 YTD).

Reads:
    raw-requirements/data/zsbms-extract/payments-canonical.csv

Writes:
    raw-requirements/data/zsbms-extract/analysis/channel-trends-2026/
        ├── index.html
        ├── chart-1-stacked.png       (weekly stacked area, all channels)
        ├── chart-2-share-trend.png   (weekly online % share, single line)
        ├── chart-3-online-lines.png  (UE vs Glovo as separate lines)
        └── chart-4-per-store.png     (online € per store, weekly)

Focused complement to the main weekly dashboard: this one zooms entirely
on the in-store / online split — what the client asked to see week by
week since Jan 1 2026.

Run: python3 scripts/build-channel-trend.py
"""

from __future__ import annotations

import datetime as dt
from pathlib import Path

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd

REPO = Path(__file__).resolve().parent.parent
DATA = REPO / "raw-requirements" / "data" / "zsbms-extract"
OUT = DATA / "analysis" / "channel-trends-2026"
OUT.mkdir(parents=True, exist_ok=True)


PAPER = "#f4eedf"
PAPER_2 = "#efe6d4"
INK = "#1a1613"
INK_2 = "#3c342e"
STONE = "#7a746b"
GOLD = "#a68a3e"
GOLD_2 = "#c2a04a"
EMBER = "#b8563d"

CANAL_COLOR = {
    "En boutique": INK,
    "Uber Eats": EMBER,
    "Glovo": GOLD,
    "Bolt Food": INK_2,
}
LOJA_COLOR = {"Anjos": EMBER, "Campo": GOLD, "Beato": INK_2}
LOJA_LABEL = {"Anjos": "Anjos", "Ourique": "Campo", "Beato": "Beato"}


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
# Load + classify
# =========================================================================
df = pd.read_csv(DATA / "payments-canonical.csv")
df["data"] = pd.to_datetime(df["data"], format="%d-%m-%Y").dt.date

ONLINE_CHANNELS = {"Uber Eats", "Glovo", "Bolt Food", "iFood"}


def canal_of(tipo: str) -> str:
    return tipo if tipo in ONLINE_CHANNELS else "En boutique"


df["canal"] = df["tipo_pagamento"].apply(canal_of)

# Build weekly buckets (Mon-Sun)
year_start = dt.date(2026, 1, 1)
first_sun = dt.date(2026, 1, 4)
data_max = df["data"].max()
last_sun = data_max
while last_sun.weekday() != 6:
    last_sun -= dt.timedelta(days=1)

weeks: list[dict] = []
sun = first_sun
while sun <= last_sun:
    mon = sun - dt.timedelta(days=6)
    sub = df[(df["data"] >= mon) & (df["data"] <= sun)]
    row = {"week_end": sun, "week_start": mon}
    for canal in ("En boutique", "Uber Eats", "Glovo", "Bolt Food"):
        row[canal] = float(sub[sub["canal"] == canal]["valor"].sum())
    row["total"] = sum(row[c] for c in ("En boutique", "Uber Eats", "Glovo", "Bolt Food"))
    row["online"] = row["Uber Eats"] + row["Glovo"] + row["Bolt Food"]
    row["online_pct"] = row["online"] / row["total"] * 100 if row["total"] else 0
    # Per-loja online amounts
    for loja in ("Anjos", "Ourique", "Beato"):
        loja_sub = sub[sub["loja"] == loja]
        row[f"{loja}_online"] = float(
            loja_sub[loja_sub["canal"].isin(["Uber Eats", "Glovo", "Bolt Food"])]["valor"].sum()
        )
        row[f"{loja}_total"] = float(loja_sub["valor"].sum())
    weeks.append(row)
    sun += dt.timedelta(days=7)

w = pd.DataFrame(weeks)
n_weeks = len(w)
print(f"Computing {n_weeks} weeks: {w.iloc[0]['week_start']} → {w.iloc[-1]['week_end']}")


# =========================================================================
# Chart 1 — Stacked area (all channels)
# =========================================================================
fig, ax = plt.subplots(figsize=(11, 4.4), facecolor=PAPER)
canal_order = ["En boutique", "Uber Eats", "Glovo", "Bolt Food"]
present = [c for c in canal_order if w[c].sum() > 0]
ax.stackplot(
    w["week_end"],
    [w[c] for c in present],
    labels=present,
    colors=[CANAL_COLOR[c] for c in present],
    alpha=0.85,
)
ax.set_title("Chiffre d'affaires hebdomadaire par canal (TTC) — 2026 YTD",
             pad=14, fontsize=13, weight="bold")
ax.set_ylabel("CA hebdomadaire (TTC)", color=INK_2, fontsize=10)
ax.xaxis.set_major_formatter(mdates.DateFormatter("%d %b"))
ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.SU, interval=2))
apply_brand(ax)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{int(v):,} €".replace(",", " ")))
ax.legend(loc="upper left", frameon=False, fontsize=9, ncol=4)
ax.grid(True, alpha=0.15, linestyle="--", linewidth=0.5)
plt.tight_layout()
plt.savefig(OUT / "chart-1-stacked.png", dpi=140, facecolor=PAPER, bbox_inches="tight")
plt.close()
print("→ chart-1-stacked.png")


# =========================================================================
# Chart 2 — Online % share trend
# =========================================================================
fig, ax = plt.subplots(figsize=(11, 3.8), facecolor=PAPER)
ax.fill_between(w["week_end"], w["online_pct"], alpha=0.12, color=EMBER)
ax.plot(w["week_end"], w["online_pct"], color=EMBER, linewidth=2.5,
        marker="o", markersize=5, label="% online")
# YTD average line
ytd_avg = w["online"].sum() / w["total"].sum() * 100
ax.axhline(y=ytd_avg, color=STONE, linewidth=1, linestyle="--", alpha=0.7,
           label=f"Moyenne YTD ({ytd_avg:.1f}%)")

ax.set_title("Part des ventes en ligne (% du CA total hebdomadaire) — 2026 YTD",
             pad=14, fontsize=13, weight="bold")
ax.set_ylabel("% du CA total", color=INK_2, fontsize=10)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0f} %"))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%d %b"))
ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.SU, interval=2))
apply_brand(ax)
ax.legend(loc="upper left", frameon=False, fontsize=9)
ax.grid(True, alpha=0.15, linestyle="--", linewidth=0.5)
ax.set_ylim(bottom=0)
plt.tight_layout()
plt.savefig(OUT / "chart-2-share-trend.png", dpi=140, facecolor=PAPER, bbox_inches="tight")
plt.close()
print("→ chart-2-share-trend.png")


# =========================================================================
# Chart 3 — Online channels as separate lines (UE vs Glovo)
# =========================================================================
fig, ax = plt.subplots(figsize=(11, 3.8), facecolor=PAPER)
ax.plot(w["week_end"], w["Uber Eats"], color=EMBER, linewidth=2.2,
        marker="o", markersize=4, label="Uber Eats")
ax.plot(w["week_end"], w["Glovo"], color=GOLD, linewidth=2.2,
        marker="o", markersize=4, label="Glovo")
if w["Bolt Food"].sum() > 0:
    ax.plot(w["week_end"], w["Bolt Food"], color=INK_2, linewidth=2.2,
            marker="o", markersize=4, label="Bolt Food")

ax.set_title("Chiffre d'affaires hebdomadaire par plateforme en ligne (TTC) — 2026 YTD",
             pad=14, fontsize=13, weight="bold")
ax.set_ylabel("CA hebdomadaire (TTC)", color=INK_2, fontsize=10)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{int(v):,} €".replace(",", " ")))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%d %b"))
ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.SU, interval=2))
apply_brand(ax)
ax.legend(loc="upper left", frameon=False, fontsize=9)
ax.grid(True, alpha=0.15, linestyle="--", linewidth=0.5)
plt.tight_layout()
plt.savefig(OUT / "chart-3-online-lines.png", dpi=140, facecolor=PAPER, bbox_inches="tight")
plt.close()
print("→ chart-3-online-lines.png")


# =========================================================================
# Chart 4 — Online € per store, weekly
# =========================================================================
fig, ax = plt.subplots(figsize=(11, 4.0), facecolor=PAPER)
ax.plot(w["week_end"], w["Anjos_online"], color=LOJA_COLOR["Anjos"], linewidth=2.2,
        marker="o", markersize=4, label="Anjos")
ax.plot(w["week_end"], w["Ourique_online"], color=LOJA_COLOR["Campo"], linewidth=2.2,
        marker="o", markersize=4, label="Campo")
ax.plot(w["week_end"], w["Beato_online"], color=LOJA_COLOR["Beato"], linewidth=2.2,
        marker="o", markersize=4, label="Beato")

ax.set_title("Ventes en ligne hebdomadaires (TTC) par boutique — 2026 YTD",
             pad=14, fontsize=13, weight="bold")
ax.set_ylabel("CA online (TTC)", color=INK_2, fontsize=10)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{int(v):,} €".replace(",", " ")))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%d %b"))
ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.SU, interval=2))
apply_brand(ax)
ax.legend(loc="upper left", frameon=False, fontsize=9, ncol=3)
ax.grid(True, alpha=0.15, linestyle="--", linewidth=0.5)
plt.tight_layout()
plt.savefig(OUT / "chart-4-per-store.png", dpi=140, facecolor=PAPER, bbox_inches="tight")
plt.close()
print("→ chart-4-per-store.png")


# =========================================================================
# Compute YTD aggregates + per-loja
# =========================================================================
ytd_total = w["total"].sum()
ytd_in_store = w["En boutique"].sum()
ytd_ue = w["Uber Eats"].sum()
ytd_glovo = w["Glovo"].sum()
ytd_bolt = w["Bolt Food"].sum()
ytd_online = ytd_ue + ytd_glovo + ytd_bolt

# Per-loja YTD
per_loja_canal = df.pivot_table(
    index="loja", columns="canal", values="valor",
    aggfunc="sum", fill_value=0,
)
loja_total_canal = df.groupby("loja")["valor"].sum()

# Online vs offline % per loja
loja_online_pct = {}
for loja in ("Anjos", "Ourique", "Beato"):
    online = sum(per_loja_canal.loc[loja, c] for c in ("Uber Eats", "Glovo", "Bolt Food")
                 if c in per_loja_canal.columns)
    total = loja_total_canal.loc[loja]
    loja_online_pct[loja] = online / total * 100

# Trend signals
first_4 = w.iloc[:4]
last_4 = w.iloc[-4:]
trend_first = first_4["online_pct"].mean()
trend_last = last_4["online_pct"].mean()
trend_delta_pts = trend_last - trend_first

ue_first = first_4["Uber Eats"].sum() / 4
ue_last = last_4["Uber Eats"].sum() / 4
ue_growth = (ue_last - ue_first) / ue_first * 100 if ue_first else 0
glovo_first = first_4["Glovo"].sum() / 4
glovo_last = last_4["Glovo"].sum() / 4
glovo_growth = (glovo_last - glovo_first) / glovo_first * 100 if glovo_first else 0


# =========================================================================
# Format helpers
# =========================================================================
def fr_money(v: float, decimals: int = 0) -> str:
    if decimals:
        rounded = round(v, decimals)
        int_part = int(rounded)
        frac = abs(rounded - int_part)
        int_str = f"{int_part:,}".replace(",", " ")
        frac_str = f"{frac:.{decimals}f}"[2:]
        return f"{int_str},{frac_str} €"
    return f"{int(round(v)):,} €".replace(",", " ")


def fr_pct(v: float, decimals: int = 1) -> str:
    s = f"{v:.{decimals}f}".replace(".", ",")
    return f"{s} %"


def fr_week(start: dt.date, end: dt.date) -> str:
    months = ["jan", "fév", "mar", "avr", "mai", "juin",
              "juil", "août", "sep", "oct", "nov", "déc"]
    m1, m2 = months[start.month - 1], months[end.month - 1]
    if start.month == end.month:
        return f"{start.day}–{end.day} {m2}"
    return f"{start.day} {m1} – {end.day} {m2}"


# =========================================================================
# Weekly table rows
# =========================================================================
table_rows = []
for i, row in w.iterrows():
    online_pct = row["online_pct"]
    pct_cls = "gain" if online_pct >= ytd_avg else "loss"
    table_rows.append(f"""
      <tr>
        <td>{fr_week(row['week_start'], row['week_end'])}</td>
        <td class="num">{fr_money(row['En boutique'])}</td>
        <td class="num">{fr_money(row['Uber Eats'])}</td>
        <td class="num">{fr_money(row['Glovo'])}</td>
        <td class="num"><strong>{fr_money(row['online'])}</strong></td>
        <td class="num">{fr_money(row['total'])}</td>
        <td class="num {pct_cls}"><strong>{fr_pct(online_pct, 1)}</strong></td>
      </tr>""")


# =========================================================================
# Per-loja channel breakdown table
# =========================================================================
loja_rows = []
for loja in ("Anjos", "Ourique", "Beato"):
    label = LOJA_LABEL[loja]
    total = loja_total_canal.loc[loja]
    in_store = per_loja_canal.loc[loja].get("En boutique", 0)
    ue = per_loja_canal.loc[loja].get("Uber Eats", 0)
    glovo = per_loja_canal.loc[loja].get("Glovo", 0)
    online = ue + glovo
    pct = loja_online_pct[loja]
    loja_rows.append(f"""
      <tr>
        <td><strong>{label}</strong></td>
        <td class="num">{fr_money(total)}</td>
        <td class="num">{fr_money(in_store)}</td>
        <td class="num">{fr_money(ue)}</td>
        <td class="num">{fr_money(glovo)}</td>
        <td class="num"><strong>{fr_money(online)}</strong></td>
        <td class="num"><strong>{fr_pct(pct, 1)}</strong></td>
      </tr>""")


# =========================================================================
# CSS + HTML
# =========================================================================
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
  --font-display: 'Fraunces', Georgia, serif;
  --font-accent: 'Instrument Serif', Georgia, serif;
  --font-body: 'Instrument Sans', system-ui, -apple-system, sans-serif;
}
* { box-sizing: border-box; }
html, body { background: var(--paper); margin: 0; }
body { color: var(--ink); font-family: var(--font-body); font-size: 14px; line-height: 1.55; }
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
h1.display, h2.display, h3.display {
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
h3.display { font-size: 22px; }
h1.display em, h2.display em, h3.display em {
  font-family: var(--font-accent);
  font-style: italic;
  color: var(--ember);
}
p.lead { font-size: 16px; color: var(--ink-2); max-width: 64ch; margin: 0 0 14px; }
p { color: var(--ink-2); margin: 0 0 12px; max-width: 72ch; }

.kpis {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 0;
  margin-top: 24px;
  border-top: 1px solid var(--rule);
  border-bottom: 1px solid var(--rule);
}
@media (max-width: 880px) { .kpis { grid-template-columns: repeat(2, 1fr); } }
.kpi { padding: 26px 22px; border-right: 1px solid var(--rule); }
.kpi:last-child { border-right: 0; }
@media (max-width: 880px) { .kpi:nth-child(2n) { border-right: 0; } .kpi:nth-child(-n+2) { border-bottom: 1px solid var(--rule); } }
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
  font-size: clamp(26px, 3vw, 34px);
  line-height: 1;
  color: var(--ink);
  font-variant-numeric: tabular-nums;
}
.kpi .kpi-sub {
  margin-top: 6px;
  font-size: 12px;
  color: var(--stone);
  font-family: var(--font-accent);
  font-style: italic;
}

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

table.data {
  width: 100%;
  border-collapse: collapse;
  margin-top: 18px;
  font-variant-numeric: tabular-nums;
  font-size: 13px;
}
table.data th, table.data td {
  padding: 10px 12px;
  text-align: left;
  border-bottom: 1px solid var(--rule);
}
table.data th {
  font-size: 10px;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: var(--stone);
  font-weight: 500;
  border-bottom: 1px solid var(--rule-strong);
  background: var(--paper-2);
}
table.data td.num { text-align: right; }
table.data td.gain { color: var(--gain); }
table.data td.loss { color: var(--loss); }

.obs {
  background: var(--paper-2);
  border-left: 3px solid var(--gold);
  padding: 20px 24px;
  margin: 22px 0;
  font-family: var(--font-accent);
  font-style: italic;
  font-size: 17px;
  line-height: 1.55;
  color: var(--ink-2);
}
.obs .obs-label {
  display: block;
  font-family: var(--font-body);
  font-style: normal;
  font-size: 10px;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  color: var(--gold);
  font-weight: 500;
  margin-bottom: 8px;
}
.obs strong { color: var(--ember); font-weight: 600; font-style: normal; font-family: var(--font-body); }

footer.site {
  background: var(--ink);
  color: var(--paper);
  padding: 40px 32px;
}
footer.site .shell { display: flex; justify-content: space-between; align-items: baseline; gap: 16px; flex-wrap: wrap; }
footer.site .brand {
  font-family: var(--font-display);
  font-size: 18px;
  text-transform: lowercase;
}
footer.site .brand em { color: var(--gold-2); font-family: var(--font-accent); font-style: italic; }
footer.site .meta {
  font-size: 11px;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: rgba(244, 238, 223, 0.5);
}

@media print {
  body { background: white; }
  header.topbar, footer.site { background: white; color: black; }
  section { padding: 24px 0; break-inside: avoid-page; }
  figure.chart, table.data, .obs, .kpis { break-inside: avoid; }
}
"""

# Trend observation (calibrate phrasing on sign of trend_delta_pts)
if abs(trend_delta_pts) < 0.5:
    trend_text = f"La part en ligne est <strong>essentiellement stable</strong> sur l'année (moyenne {ytd_avg:.1f} %, écart entre les 4 premières et 4 dernières semaines: {trend_delta_pts:+.1f} pt). Le canal en ligne accompagne la croissance globale sans gagner ni perdre de part."
elif trend_delta_pts > 0:
    trend_text = f"La part en ligne <strong>progresse</strong>: les 4 premières semaines de 2026 affichaient une moyenne de {trend_first:.1f} %; les 4 dernières sont à {trend_last:.1f} % (+{trend_delta_pts:.1f} pt). Le canal en ligne capte une part croissante du chiffre d'affaires."
else:
    trend_text = f"La part en ligne <strong>recule légèrement</strong>: {trend_first:.1f} % sur les 4 premières semaines, {trend_last:.1f} % sur les 4 dernières ({trend_delta_pts:+.1f} pt). À suivre — peut indiquer un retour des clients en boutique, ou un essoufflement de la livraison."


HTML = f"""<!doctype html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Lully 1661 — Analyse des canaux 2026 YTD</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300..900;1,9..144,300..900&family=Instrument+Serif:ital@0;1&family=Instrument+Sans:ital,wght@0,400..700;1,400..700&display=swap">
  <style>{CSS}</style>
</head>
<body>
  <header class="topbar">
    <div class="brand">lully <em>1661</em></div>
    <div class="doc-id">Analyse des canaux · {n_weeks} semaines · 2026 YTD</div>
  </header>

  <section>
    <div class="shell">
      <div class="eyebrow">Analyse des canaux de vente</div>
      <h1 class="display">En boutique ou en ligne, <em>la trajectoire {n_weeks} semaines.</em></h1>
      <p class="lead">Répartition des recettes (TTC) entre les <strong>3 boutiques</strong> en physique (Dinheiro + Cartões) et les <strong>plateformes en ligne</strong> (Uber Eats, Glovo) — semaine par semaine du 1<sup>er</sup> janvier 2026 au {fr_week(w.iloc[-1]['week_start'], w.iloc[-1]['week_end'])} 2026. Source: ZSBMS, rapport <em>Pagamentos por Empregado e Tipos de Pagamento</em>, vérifié par recoupement avec les portails Glovo (±2 %) et Uber Eats (±7 %).</p>

      <div class="kpis">
        <div class="kpi">
          <div class="kpi-label">CA total YTD (TTC)</div>
          <div class="kpi-value">{fr_money(ytd_total)}</div>
          <div class="kpi-sub">{n_weeks} semaines</div>
        </div>
        <div class="kpi">
          <div class="kpi-label">Part en boutique</div>
          <div class="kpi-value">{fr_pct(ytd_in_store / ytd_total * 100, 1)}</div>
          <div class="kpi-sub">{fr_money(ytd_in_store)}</div>
        </div>
        <div class="kpi">
          <div class="kpi-label">Part en ligne</div>
          <div class="kpi-value">{fr_pct(ytd_online / ytd_total * 100, 1)}</div>
          <div class="kpi-sub">{fr_money(ytd_online)} · UE {fr_money(ytd_ue)} + Glovo {fr_money(ytd_glovo)}</div>
        </div>
        <div class="kpi">
          <div class="kpi-label">UE / Glovo ratio</div>
          <div class="kpi-value">{ytd_ue / ytd_glovo:.1f}×</div>
          <div class="kpi-sub">Uber Eats {ytd_ue/ytd_online*100:.0f}% de l'online</div>
        </div>
      </div>
    </div>
  </section>

  <section>
    <div class="shell">
      <div class="eyebrow">1 · Vue d'ensemble</div>
      <h2 class="display">Répartition par canal, <em>semaine par semaine.</em></h2>
      <p class="lead">La couche dominante en sombre est le canal physique (Dinheiro + Cartões). Les couches au-dessus représentent les canaux en ligne — visibles mais marginaux à cette échelle.</p>
      <figure class="chart">
        <img src="chart-1-stacked.png" alt="CA hebdomadaire empilé par canal">
        <figcaption>Chiffre d'affaires hebdomadaire (TTC) — empilement <em>En boutique</em> + <em>Uber Eats</em> + <em>Glovo</em></figcaption>
      </figure>
      <div class="obs">
        <span class="obs-label">Lecture</span>
        Le canal en boutique pèse environ <strong>{ytd_in_store / ytd_total * 100:.0f} %</strong> de la recette hebdomadaire totale tout au long de la période — c'est lui qui pilote la silhouette de la courbe. Les variations hebdomadaires que vous voyez (le pic en S2 du 5-11 jan, le creux à Pâques) viennent du canal en boutique, pas du online.
      </div>
    </div>
  </section>

  <section>
    <div class="shell">
      <div class="eyebrow">2 · Tendance de la part en ligne</div>
      <h2 class="display">Le online, <em>en pourcentage du total.</em></h2>
      <p class="lead">Pour évaluer si la livraison gagne ou perd du terrain, mieux vaut regarder la <strong>part en ligne</strong> que les valeurs absolues. La moyenne YTD est tracée en pointillés.</p>
      <figure class="chart">
        <img src="chart-2-share-trend.png" alt="Part en ligne hebdomadaire en %">
        <figcaption>% du CA total hebdomadaire venant du online (Uber Eats + Glovo)</figcaption>
      </figure>
      <div class="obs">
        <span class="obs-label">Tendance</span>
        {trend_text}
      </div>
    </div>
  </section>

  <section>
    <div class="shell">
      <div class="eyebrow">3 · Uber Eats vs Glovo</div>
      <h2 class="display">Deux plateformes, <em>deux dynamiques.</em></h2>
      <p class="lead">Uber Eats représente {ytd_ue/ytd_online*100:.0f} % du chiffre d'affaires en ligne, Glovo {ytd_glovo/ytd_online*100:.0f} %. À l'échelle hebdomadaire, les deux suivent globalement le même rythme avec des amplitudes différentes.</p>
      <figure class="chart">
        <img src="chart-3-online-lines.png" alt="UE vs Glovo par semaine">
        <figcaption>CA hebdomadaire par plateforme en ligne (TTC)</figcaption>
      </figure>
      <div class="obs">
        <span class="obs-label">Croissance des plateformes</span>
        Comparaison 4 premières semaines vs 4 dernières — <strong>Uber Eats: {ue_growth:+.0f} %</strong>, <strong>Glovo: {glovo_growth:+.0f} %</strong>. {("Les deux plateformes évoluent à peu près en parallèle." if abs(ue_growth - glovo_growth) < 15 else "Les deux plateformes évoluent à des rythmes différents — point d'attention sur celle qui décroche.")}
      </div>
    </div>
  </section>

  <section>
    <div class="shell">
      <div class="eyebrow">4 · Par boutique</div>
      <h2 class="display">Les trois boutiques, <em>pas la même dépendance au online.</em></h2>
      <p class="lead">Volume hebdomadaire de ventes en ligne (TTC) par boutique. Anjos pèse plus en absolu, mais Campo et Beato ont une part en ligne <strong>structurellement plus élevée</strong> (voir le tableau ci-dessous).</p>
      <figure class="chart">
        <img src="chart-4-per-store.png" alt="Online weekly per loja">
        <figcaption>Ventes en ligne hebdomadaires (TTC) par boutique</figcaption>
      </figure>

      <table class="data">
        <thead>
          <tr>
            <th>Boutique</th>
            <th class="num">CA total YTD</th>
            <th class="num">En boutique</th>
            <th class="num">Uber Eats</th>
            <th class="num">Glovo</th>
            <th class="num">Total en ligne</th>
            <th class="num">% online</th>
          </tr>
        </thead>
        <tbody>{"".join(loja_rows)}</tbody>
      </table>

      <div class="obs">
        <span class="obs-label">Insight</span>
        <strong>Beato ({fr_pct(loja_online_pct['Beato'], 1)})</strong> et <strong>Campo ({fr_pct(loja_online_pct['Ourique'], 1)})</strong> dépendent presque <strong>deux fois plus du online</strong> qu'Anjos ({fr_pct(loja_online_pct['Anjos'], 1)}). Anjos a une forte affluence en boutique qui amortit la part livraison; les deux autres maisons s'appuient davantage sur les plateformes pour compléter le revenu — autrement dit, <strong>une perturbation Glovo ou Uber Eats toucherait Beato et Campo plus durement qu'Anjos</strong>.
      </div>
    </div>
  </section>

  <section>
    <div class="shell">
      <div class="eyebrow">5 · Détail semaine par semaine</div>
      <h2 class="display">{n_weeks} semaines, <em>chaque ligne.</em></h2>

      <table class="data">
        <thead>
          <tr>
            <th>Semaine</th>
            <th class="num">En boutique</th>
            <th class="num">Uber Eats</th>
            <th class="num">Glovo</th>
            <th class="num">Total online</th>
            <th class="num">CA total</th>
            <th class="num">% online</th>
          </tr>
        </thead>
        <tbody>{"".join(table_rows)}</tbody>
      </table>
    </div>
  </section>

  <section class="compact">
    <div class="shell">
      <div class="eyebrow">Source & méthodologie</div>
      <h3 class="display">D'où viennent ces chiffres.</h3>
      <p>Les valeurs sont extraites du rapport <em>Pagamentos por Empregado e Tipos de Pagamento</em> dans ZSBMS, en mode <em>Informação Diária</em> (granularité quotidienne, ventilation par tipo de pagamento). Le canal <em>En boutique</em> agrège Dinheiro + Cartão de Débito + Cartão de Crédito + MB Way; le canal <em>en ligne</em> agrège Uber Eats + Glovo. Toutes les valeurs sont TTC.</p>
      <p>Un recoupement avec les portails marchands a été effectué pour avril 2026: Glovo (3 boutiques) écart <strong>−1,6 %</strong>; Uber Eats (Campo seul) écart <strong>−6,9 %</strong>. Le calcul de la part en ligne reste fiable à ce niveau de précision.</p>
    </div>
  </section>

  <footer class="site">
    <div class="shell">
      <div class="brand">lully <em>1661</em> · analyse des canaux 2026</div>
      <div class="meta">généré le {dt.date.today().isoformat()} · {n_weeks} semaines · {fr_money(ytd_total)} YTD</div>
    </div>
  </footer>
</body>
</html>
"""

(OUT / "index.html").write_text(HTML, encoding="utf-8")
print(f"\n→ {OUT.relative_to(REPO)}/index.html")

"""Lully 1661 — sales analytics from the ZSBMS Evolução de Vendas export.

Input:  raw-requirements/data/zsbms-extract/evo-vendas-produto-90d.csv
Output: raw-requirements/data/zsbms-extract/analysis/{*.png, observations.md}

Run:    python3 scripts/analyse-sales.py

The CSV and outputs live under raw-requirements/data/ (gitignored — they
contain client revenue figures). The script itself is tracked; the data
is not. Re-run after every new ZSBMS export drop.

Pairs with scripts/build-sales-report.py — that script consumes the same
CSV and produces the trilingual HTML deliverable.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd

# --- Brand colors (lifted from app/globals.css) ---------------------------
PAPER = "#f4eedf"
INK = "#1a1613"
INK2 = "#3c342e"
STONE = "#7a746b"
GOLD = "#a68a3e"
EMBER = "#b8563d"
LOJA_COLOR = {"Anjos": EMBER, "Ourique": GOLD, "Beato": INK2}

REPO = Path(__file__).resolve().parent.parent
DATA = REPO / "raw-requirements" / "data" / "zsbms-extract"
OUT = DATA / "analysis"
OUT.mkdir(exist_ok=True)


def apply_brand_style(ax) -> None:
    """Subtle, paper-not-glass styling that matches the demo site."""
    ax.set_facecolor(PAPER)
    ax.tick_params(colors=INK2, labelsize=9)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    for spine in ("left", "bottom"):
        ax.spines[spine].set_color(STONE)
        ax.spines[spine].set_linewidth(0.8)
    ax.title.set_color(INK)
    ax.xaxis.label.set_color(INK2)
    ax.yaxis.label.set_color(INK2)


# --- Load + normalise -----------------------------------------------------
df = pd.read_csv(DATA / "evo-vendas-produto-90d.csv")
df["data"] = pd.to_datetime(df["data"], format="%d-%m-%Y")
df["weekday"] = df["data"].dt.day_name()
df["is_weekend"] = df["data"].dt.weekday >= 5  # Sat/Sun
df["week"] = df["data"].dt.to_period("W-SUN").apply(lambda r: r.start_time)

# Trim noise: the few rows with valor_total <= 0 are voids/corrections.
df = df[df["valor_total"] > 0].copy()

# Drop the incomplete trailing week (otherwise stacked-area charts hit a
# cliff at the right edge). We count days per ISO week and keep only weeks
# with >= 5 days of data.
week_days = df.groupby("data")["data"].first().to_frame()
week_days["week"] = week_days["data"].dt.to_period("W-SUN").apply(lambda r: r.start_time)
days_per_week = week_days.groupby("week").size()
complete_weeks = days_per_week[days_per_week >= 5].index
df = df[
    df["data"].dt.to_period("W-SUN").apply(lambda r: r.start_time).isin(complete_weeks)
].copy()

print(
    f"Loaded {len(df):,} rows | "
    f"{df['data'].min().date()} → {df['data'].max().date()} | "
    f"{df['loja'].nunique()} lojas | "
    f"{df['produto'].nunique()} produtos | "
    f"{df['familia'].nunique()} famílias"
)


# =========================================================================
# 1. Per-family weekly revenue — stacked area
# =========================================================================
family_week = (
    df.groupby(["week", "familia"])["valor_total"].sum().unstack(fill_value=0)
)
# Drop the tiny families (< 1% of total revenue) — they're noise in a chart.
total_by_fam = family_week.sum().sort_values(ascending=False)
significant = total_by_fam[total_by_fam > total_by_fam.sum() * 0.01].index.tolist()
family_week_plot = family_week[significant]

fig, ax = plt.subplots(figsize=(11, 5.5))
fig.patch.set_facecolor(PAPER)

# Brand-aligned palette: paper→ink gradient with one ember accent.
palette = [EMBER, GOLD, INK, INK2, STONE, "#8a3324", "#c7a64e"][: len(significant)]
ax.stackplot(
    family_week_plot.index,
    *[family_week_plot[c] for c in family_week_plot.columns],
    labels=family_week_plot.columns,
    colors=palette,
    alpha=0.92,
)
n_weeks = len(family_week_plot)
ax.set_title(
    f"Receita semanal por família — {n_weeks} semanas "
    f"({df['data'].min().strftime('%d %b')} → {df['data'].max().strftime('%d %b %Y')})",
    pad=14,
    fontsize=13,
)
ax.set_ylabel("€ / semana")
ax.set_xlabel("")
ax.xaxis.set_major_formatter(mdates.DateFormatter("%d %b"))
ax.legend(loc="upper left", frameon=False, fontsize=9, ncol=2)
apply_brand_style(ax)
plt.tight_layout()
plt.savefig(OUT / "01-family-weekly.png", dpi=140, facecolor=PAPER)
plt.close()
print("→ 01-family-weekly.png")


# =========================================================================
# 2. Top-10 products — revenue + a 4-week mini sparkline-style trend each
# =========================================================================
prod_revenue = (
    df.groupby("produto")["valor_total"]
    .sum()
    .sort_values(ascending=False)
)
top10 = prod_revenue.head(10).index.tolist()

# Weekly revenue per top-10 product
prod_week = (
    df[df["produto"].isin(top10)]
    .groupby(["week", "produto"])["valor_total"]
    .sum()
    .unstack(fill_value=0)
)
# Order columns by total revenue (so the legend reads naturally)
prod_week = prod_week[top10]

fig, ax = plt.subplots(figsize=(12, 7))
fig.patch.set_facecolor(PAPER)
palette = [
    EMBER, GOLD, INK, "#8a3324", "#c7a64e",
    INK2, "#9b4431", "#a68a3e", STONE, "#7a6b56",
]
for i, prod in enumerate(prod_week.columns):
    ax.plot(
        prod_week.index,
        prod_week[prod],
        marker="o",
        markersize=4,
        linewidth=1.6,
        color=palette[i],
        label=f"{prod}  (€{prod_revenue[prod]:,.0f} total)",
    )
ax.set_title(
    f"Top-10 produtos — receita semanal "
    f"({df['data'].min().strftime('%d %b')} → {df['data'].max().strftime('%d %b %Y')})",
    pad=14,
    fontsize=13,
)
ax.set_ylabel("€ / semana")
ax.set_xlabel("")
ax.xaxis.set_major_formatter(mdates.DateFormatter("%d %b"))
# Put legend below the plot, two columns wide — leaves the plot area unobstructed.
ax.legend(
    loc="upper center",
    bbox_to_anchor=(0.5, -0.12),
    frameon=False,
    fontsize=9,
    ncol=2,
    columnspacing=2.5,
    handlelength=2,
)
apply_brand_style(ax)
plt.tight_layout()
plt.savefig(OUT / "02-top10-products-weekly.png", dpi=140, facecolor=PAPER, bbox_inches="tight")
plt.close()
print("→ 02-top10-products-weekly.png")


# =========================================================================
# 3. Per-store family mix — horizontal stacked bars
# =========================================================================
loja_fam = (
    df.groupby(["loja", "familia"])["valor_total"].sum().unstack(fill_value=0)
)
# Keep only significant families
loja_fam = loja_fam[[c for c in significant if c in loja_fam.columns]]
# Normalise to % of each loja's revenue
loja_fam_pct = loja_fam.div(loja_fam.sum(axis=1), axis=0) * 100
# Sort lojas by total revenue, biggest on top
order = df.groupby("loja")["valor_total"].sum().sort_values(ascending=True).index
loja_fam_pct = loja_fam_pct.loc[order]

fig, ax = plt.subplots(figsize=(11, 3.6))
fig.patch.set_facecolor(PAPER)
left = pd.Series([0.0] * len(loja_fam_pct), index=loja_fam_pct.index)
for i, fam in enumerate(loja_fam_pct.columns):
    ax.barh(
        loja_fam_pct.index,
        loja_fam_pct[fam],
        left=left,
        color=palette[i % len(palette)],
        label=fam,
        edgecolor=PAPER,
        linewidth=0.8,
    )
    # Label slices >= 6%
    for j, loja in enumerate(loja_fam_pct.index):
        v = loja_fam_pct.loc[loja, fam]
        if v >= 6:
            ax.text(
                left.iloc[j] + v / 2,
                j,
                f"{fam.split(' / ')[0]}\n{v:.0f}%",
                ha="center",
                va="center",
                fontsize=8.5,
                color=PAPER if i < 3 else INK,
            )
    left = left + loja_fam_pct[fam]

ax.set_xlim(0, 100)
ax.set_xlabel("% da receita da loja")
ax.set_title(
    "Composição de receita por loja — qual família domina cada casa",
    pad=14,
    fontsize=13,
)
ax.set_yticks(range(len(loja_fam_pct)))
ax.set_yticklabels(loja_fam_pct.index, fontsize=11)
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.18), ncol=4, frameon=False, fontsize=9)
apply_brand_style(ax)
plt.tight_layout()
plt.savefig(OUT / "03-loja-family-mix.png", dpi=140, facecolor=PAPER, bbox_inches="tight")
plt.close()
print("→ 03-loja-family-mix.png")


# =========================================================================
# 4. ABC analysis — per loja, what % of SKUs deliver 80% of revenue
# =========================================================================
abc_results = {}
for loja in ["Anjos", "Ourique", "Beato"]:
    p = (
        df[df["loja"] == loja]
        .groupby("produto")["valor_total"]
        .sum()
        .sort_values(ascending=False)
    )
    cum = p.cumsum() / p.sum() * 100
    a = (cum <= 80).sum() + 1  # +1 for the SKU that crosses 80%
    b = (cum <= 95).sum() + 1
    total_skus = len(p)
    abc_results[loja] = {
        "total_skus": total_skus,
        "a_skus": a,
        "a_pct_of_skus": a / total_skus * 100,
        "b_skus": b - a,
        "c_skus": total_skus - b,
    }

fig, axes = plt.subplots(1, 3, figsize=(13, 4.2), sharey=True)
fig.patch.set_facecolor(PAPER)
for ax_i, loja in enumerate(["Anjos", "Ourique", "Beato"]):
    ax = axes[ax_i]
    p = (
        df[df["loja"] == loja]
        .groupby("produto")["valor_total"]
        .sum()
        .sort_values(ascending=False)
    )
    cum = p.cumsum() / p.sum() * 100
    x = range(1, len(p) + 1)
    ax.plot(x, cum.values, color=LOJA_COLOR[loja], linewidth=1.8)
    ax.axhline(80, color=STONE, linestyle="--", linewidth=0.8, alpha=0.7)
    a_count = abc_results[loja]["a_skus"]
    ax.axvline(a_count, color=STONE, linestyle="--", linewidth=0.8, alpha=0.7)
    ax.text(
        a_count + 4,
        45,
        f"{a_count} SKUs\n= 80%",
        fontsize=10,
        color=INK,
    )
    ax.set_title(
        f"{loja} — {abc_results[loja]['total_skus']} SKUs",
        fontsize=12,
        pad=10,
    )
    ax.set_xlabel("nº de produtos (rank)")
    if ax_i == 0:
        ax.set_ylabel("% receita cumulativa")
    apply_brand_style(ax)
    ax.set_ylim(0, 102)

plt.suptitle("ABC por loja — quantos produtos sustentam 80% da receita", fontsize=13, color=INK, y=1.02)
plt.tight_layout()
plt.savefig(OUT / "04-abc-per-loja.png", dpi=140, facecolor=PAPER, bbox_inches="tight")
plt.close()
print("→ 04-abc-per-loja.png")


# =========================================================================
# 5. Weekday vs Weekend pattern — by family
# =========================================================================
# Average daily revenue per family, split weekday/weekend.
df["day_kind"] = df["is_weekend"].map({True: "Fim-de-semana", False: "Dia de semana"})
daily_avg = (
    df.groupby(["familia", "day_kind", "data"])["valor_total"]
    .sum()
    .reset_index()
    .groupby(["familia", "day_kind"])["valor_total"]
    .mean()
    .unstack()
)
daily_avg = daily_avg.loc[[c for c in significant if c in daily_avg.index]]
# Compute weekend lift %
daily_avg["lift_%"] = (daily_avg["Fim-de-semana"] / daily_avg["Dia de semana"] - 1) * 100

fig, ax = plt.subplots(figsize=(10, 4.8))
fig.patch.set_facecolor(PAPER)
y = range(len(daily_avg))
w = 0.4
ax.barh(
    [v - w / 2 for v in y],
    daily_avg["Dia de semana"],
    height=w,
    color=INK2,
    label="Dia de semana (média €/dia)",
)
ax.barh(
    [v + w / 2 for v in y],
    daily_avg["Fim-de-semana"],
    height=w,
    color=EMBER,
    label="Fim-de-semana (média €/dia)",
)
# Annotate lift
for i, lift in enumerate(daily_avg["lift_%"]):
    higher = max(daily_avg["Dia de semana"].iloc[i], daily_avg["Fim-de-semana"].iloc[i])
    ax.text(
        higher + 30,
        i,
        f"{lift:+.0f}%",
        va="center",
        fontsize=10,
        color=EMBER if lift > 0 else STONE,
        fontweight="bold",
    )
ax.set_yticks(list(y))
ax.set_yticklabels(daily_avg.index)
ax.invert_yaxis()
ax.set_xlabel("€ média por dia")
ax.set_title(
    "Padrão semana vs fim-de-semana — receita média por dia (Mar 1 → May 12)",
    pad=14,
    fontsize=12,
)
ax.legend(loc="lower right", frameon=False, fontsize=9)
apply_brand_style(ax)
plt.tight_layout()
plt.savefig(OUT / "05-weekday-vs-weekend.png", dpi=140, facecolor=PAPER)
plt.close()
print("→ 05-weekday-vs-weekend.png")


# =========================================================================
# 6. Insights memo
# =========================================================================
total_revenue = df["valor_total"].sum()
total_units = df["quantidade"].sum()
n_days = df["data"].nunique()
avg_daily = total_revenue / n_days

loja_totals = df.groupby("loja")["valor_total"].agg(["sum", "count"]).sort_values("sum", ascending=False)
loja_share = (loja_totals["sum"] / loja_totals["sum"].sum() * 100)

# Brunch (Anjos-only) — match real ZSBMS product names by keyword. The
# system uses English names like "Eggs Benedict" / "Avocado toast" rather
# than the menu PDF spellings. We search case-insensitively for a fixed
# keyword set covering the menu's signature dishes; this catches naming
# variants the client may have ("Granola pequena", "Eggs Florentine", etc).
brunch_pat = (
    r"benedict|florentine|cilbir|avocado|pain perdu|menuet|monsieur|granola|sopa"
)
brunch_match = df[df["produto"].str.lower().str.contains(brunch_pat, regex=True, na=False)]
brunch_rev = brunch_match["valor_total"].sum()
brunch_share_of_anjos = brunch_rev / loja_totals.loc["Anjos", "sum"] * 100 if brunch_rev else 0

# Restaurant-class share of Anjos = Restaurante + Drinks + Snacks. This is
# the "Anjos is a restaurant in disguise" structural metric — independent
# of brunch SKU naming quirks.
anjos_df = df[df["loja"] == "Anjos"]
anjos_total_rev = anjos_df["valor_total"].sum()
anjos_by_fam = anjos_df.groupby("familia")["valor_total"].sum()
anjos_drinks = anjos_by_fam.get("Drinks", 0)
anjos_snacks = anjos_by_fam.get("Snacks", 0)
anjos_rest = anjos_by_fam.get("Restaurante", 0)
anjos_rc = anjos_drinks + anjos_snacks + anjos_rest
anjos_rc_share = anjos_rc / anjos_total_rev * 100
anjos_drinks_pct = anjos_drinks / anjos_total_rev * 100
anjos_snacks_pct = anjos_snacks / anjos_total_rev * 100
anjos_rest_pct = anjos_rest / anjos_total_rev * 100

# Top single SKU per loja
top_per_loja = {}
for loja in loja_totals.index:
    p = df[df["loja"] == loja].groupby("produto")["valor_total"].sum().sort_values(ascending=False)
    top_per_loja[loja] = (p.index[0], p.iloc[0], p.iloc[0] / loja_totals.loc[loja, "sum"] * 100)

memo_path = OUT / "observations.md"
with memo_path.open("w", encoding="utf-8") as f:
    f.write(f"""# Lully 1661 — Análise de vendas

**Período analisado:** {df["data"].min().strftime("%d-%m-%Y")} → {df["data"].max().strftime("%d-%m-%Y")} ({n_days} dias de calendário com registos)
**Fonte:** Export ZSBMS · *Listagem de Evolução de Vendas por Produto*
**Linhas processadas:** {len(df):,}
**Cobertura:** 3 lojas · {df["produto"].nunique()} SKUs · {df["familia"].nunique()} famílias

## Indicadores principais

| Métrica | Valor |
|---|---|
| Receita total | **€{total_revenue:,.0f}** |
| Unidades vendidas | {total_units:,.0f} |
| Receita média/dia (todas as lojas) | €{avg_daily:,.0f} |
| Ticket médio por linha de venda | €{total_revenue/len(df):.2f} |

## Distribuição entre lojas

| Loja | Receita | % do total | Linhas de venda |
|---|---|---|---|
""")
    for loja in loja_totals.index:
        rev = loja_totals.loc[loja, "sum"]
        share = loja_share[loja]
        rows = loja_totals.loc[loja, "count"]
        f.write(f"| **{loja}** | €{rev:,.0f} | {share:.1f}% | {rows:,} |\n")

    f.write(f"""
> **Observação 1.** Anjos é o eixo financeiro da casa: gera {loja_share['Anjos']:.0f}% da receita com apenas uma das três lojas. Beato, apesar de ser onde nasceu a Lully, está em terceiro com {loja_share['Beato']:.0f}% — desvio importante face à narrativa "Beato é o coração". A página `/sobre` do website deve reconhecer este facto sem o esconder.

## Top SKU em cada loja

| Loja | Produto top | Receita | % da loja |
|---|---|---|---|
""")
    for loja, (prod, rev, share) in top_per_loja.items():
        f.write(f"| **{loja}** | {prod} | €{rev:,.0f} | {share:.1f}% |\n")

    f.write(f"""
## Composição por família

Pastelaria domina em todas as lojas, mas o mix é diferente:

| Família | Receita {n_days} dias | % do total | Unidades |
|---|---|---|---|
""")
    fam_summary = (
        df.groupby("familia")
        .agg({"valor_total": "sum", "quantidade": "sum"})
        .sort_values("valor_total", ascending=False)
    )
    for fam, row in fam_summary.iterrows():
        f.write(
            f"| {fam} | €{row['valor_total']:,.0f} | "
            f"{row['valor_total']/total_revenue*100:.1f}% | "
            f"{row['quantidade']:,.0f} |\n"
        )

    f.write(f"""
> **Observação 2.** Pastelaria gera mais receita que Pão+Pão/KG combinados, mas a Pão+Pão/KG vendem mais unidades. O pão é o **driver de tráfego**; a pastelaria é o **driver de margem**. Visto assim, faz sentido manter o pão como herói da homepage e empurrar a pastelaria nas vitrines de loja.

## Brunch — peso real em Anjos

Os SKUs de brunch no sistema chamam-se `Eggs Benedict`, `Eggs Florentine`,
`Avocado toast`, `Le Menuet`, `Le Monsieur`, `Pain Perdu`, `Sopa do Mês`,
`Granola` e variantes. Análise feita por correspondência de palavra-chave
nos nomes de produto.

| Métrica | Valor |
|---|---|
| Receita brunch ({n_days} dias) | **€{brunch_rev:,.0f}** |
| % da receita total de Anjos | **{brunch_share_of_anjos:.1f}%** |
| Unidades vendidas | {brunch_match['quantidade'].sum():,.0f} |

> **Observação 3.** O brunch enquanto categoria explícita representa cerca de {brunch_share_of_anjos:.0f}% da receita de Anjos — é uma faixa significativa mas não dominante. **Este número subestima a operação brunch real**, porque as bebidas, café e snacks pedidos junto do brunch caem em outras famílias. Olhando para o conjunto "Restaurante + Drinks + Snacks" abaixo, vê-se a operação brunch+café-de-manhã na sua escala verdadeira.

## Anjos como restaurante disfarçado

| Família em Anjos | Receita | % de Anjos |
|---|---|---|
| Drinks | €{anjos_drinks:,.0f} | {anjos_drinks_pct:.1f}% |
| Snacks | €{anjos_snacks:,.0f} | {anjos_snacks_pct:.1f}% |
| Restaurante | €{anjos_rest:,.0f} | {anjos_rest_pct:.1f}% |
| **Total "consumo no local"** | **€{anjos_rc:,.0f}** | **{anjos_rc_share:.1f}%** |

> **Observação 4.** **{anjos_rc_share:.0f}% da receita de Anjos vem de consumo no local** (Drinks + Snacks + Restaurante), antes mesmo de contar a pastelaria e o pão consumidos à mesa. Os outros dois lojas combinados (Beato + Ourique) têm um perfil completamente diferente: pão e pastelaria de balcão, com pouca componente de "ficar à mesa". Anjos não é uma padaria com mesas — é um restaurante que coze o seu próprio pão. Vale a pena considerar separar os relatórios e KPIs internos de Anjos vs Beato/Ourique.

## Análise ABC — concentração de SKUs

Quantos produtos sustentam 80% da receita em cada loja:

| Loja | Total SKUs | SKUs que fazem 80% | % dos SKUs |
|---|---|---|---|
""")
    for loja, r in abc_results.items():
        f.write(
            f"| **{loja}** | {r['total_skus']} | {r['a_skus']} | "
            f"{r['a_pct_of_skus']:.1f}% |\n"
        )

    f.write(f"""
> **Observação 5.** O catálogo da casa tem cauda longa: a maioria dos SKUs vende muito pouco. Para um dashboard semanal de operação, o foco deve ser nos ~{abc_results['Anjos']['a_skus']} produtos que fazem 80% em Anjos — uma vista "ranking + variação semana-sobre-semana" desses produtos cobre quase toda a decisão operacional sem ruído.

## Padrão semana-vs-fim-de-semana por família

""")
    f.write("| Família | Média dia útil (€) | Média fim-de-semana (€) | Lift |\n|---|---|---|---|\n")
    for fam, row in daily_avg.iterrows():
        wd = row["Dia de semana"]
        we = row["Fim-de-semana"]
        lift = row["lift_%"]
        f.write(f"| {fam} | €{wd:,.0f} | €{we:,.0f} | {lift:+.0f}% |\n")

    f.write("""
> **Observação 6.** Família com maior lift de fim-de-semana é a oportunidade óbvia para promoção fim-de-semana ou para repensar staffing/produção sábado-domingo.

## Recomendações operacionais (a discutir com o cliente)

1. **Dashboard semanal de SKU "core 80%".** Cerca de 30–50 produtos por loja merecem monitorização semanal (receita, unidades, variação WoW). Os restantes são cauda — visão mensal chega.
2. **Pão como tráfego, pastelaria como margem.** Os preços de pão a peso (Pão/KG) gerem €/unidade alto sem dependerem de novidade. Vale auditar consistência de preço/kg entre lojas.
3. **Tratar Anjos como restaurante, não como padaria.** {anjos_rc_share:.0f}% da receita de Anjos é consumo no local (Drinks + Snacks + Restaurante), antes de contar pastelaria e pão consumidos à mesa. KPIs, staffing e mix de produto deviam ser definidos separadamente de Beato/Ourique — que são padarias de balcão.
4. **Beato precisa de uma decisão consciente.** Com €{beato_rev:,.0f} em {n_days_total} dias (€{beato_daily:.0f}/dia), Beato pode ser: (a) loja-de-produção que vende sub-produto a balcão, (b) candidata a relocalização, (c) força de marca para o ecossistema. Os três têm implicações diferentes para a comunicação no site.
5. **Tipos de família a limpar.** Existem 12 strings família/sub-família distintas, algumas com nomes inconsistentes ("APERITIVO", "Outros"). Antes de qualquer dashboard sério, vale **uma sessão de normalização** das categorias dentro do ZSBMS — caso contrário cada análise vai re-inventar a roda.

---

**Ficheiros desta análise:**
- `01-family-weekly.png` — receita semanal por família, área empilhada
- `02-top10-products-weekly.png` — top 10 produtos, receita semanal
- `03-loja-family-mix.png` — composição da receita por loja
- `04-abc-per-loja.png` — análise ABC (concentração de receita) por loja
- `05-weekday-vs-weekend.png` — padrão semana vs fim-de-semana

Dados brutos: `../evo-vendas-produto-90d.csv` ({rows:,} linhas)

*Gerado por `analyse.py` em {today}*
""".format(
    anjos_rc_share=anjos_rc_share,
    beato_rev=loja_totals.loc["Beato", "sum"],
    beato_daily=loja_totals.loc["Beato", "sum"] / n_days,
    n_days_total=n_days,
    rows=len(df),
    today=pd.Timestamp.today().strftime("%Y-%m-%d"),
))

print(f"→ observations.md")
print(f"\nDone. Output in: {OUT}")

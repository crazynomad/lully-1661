"""Lully 1661 — trilingual HTML sales report (EN / PT / FR).

Reads:  raw-requirements/data/zsbms-extract/sales-canonical.csv
Writes: raw-requirements/data/zsbms-extract/analysis/
            ├── report-en.html
            ├── report-pt.html
            ├── report-fr.html
            ├── index.html
            └── report-data.json

Run:    python3 scripts/build-sales-report.py

Styled with the Lully 1661 design system (paper/ink/gold/ember palette,
Fraunces + Instrument Serif + Instrument Sans typography). References the
PNG charts emitted by scripts/analyse-sales.py — re-run that first if the
charts are stale. Output lives under raw-requirements/data/ (gitignored,
contains client revenue figures).
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

REPO = Path(__file__).resolve().parent.parent
DATA = REPO / "raw-requirements" / "data" / "zsbms-extract"
OUT = DATA / "analysis"
OUT.mkdir(exist_ok=True)


# =========================================================================
# 1. Load and clean the export (same trimming rules as analyse-sales.py)
# =========================================================================
df = pd.read_csv(DATA / "sales-canonical.csv")
df["data"] = pd.to_datetime(df["data"], format="%d-%m-%Y")
df = df[df["valor_total"] > 0].copy()

# Drop incomplete trailing weeks (< 5 days) so totals are honest.
week = df["data"].dt.to_period("W-SUN").apply(lambda r: r.start_time)
df["week"] = week
days_per_week = df[["data", "week"]].drop_duplicates().groupby("week").size()
complete = days_per_week[days_per_week >= 5].index
df = df[df["week"].isin(complete)].copy()


# =========================================================================
# 2. Aggregate metrics
# =========================================================================
total_revenue = float(df["valor_total"].sum())
total_units = int(df["quantidade"].sum())
n_days = int(df["data"].nunique())
avg_daily = total_revenue / n_days
avg_ticket = total_revenue / len(df)

loja_totals = (
    df.groupby("loja")
    .agg(revenue=("valor_total", "sum"), rows=("valor_total", "count"))
    .sort_values("revenue", ascending=False)
)

lojas_data = []
for loja in loja_totals.index:
    loja_df = df[df["loja"] == loja]
    top = loja_df.groupby("produto")["valor_total"].sum().sort_values(ascending=False)
    lojas_data.append({
        "name": loja,
        "revenue": float(loja_totals.loc[loja, "revenue"]),
        "share_pct": float(loja_totals.loc[loja, "revenue"] / total_revenue * 100),
        "rows": int(loja_totals.loc[loja, "rows"]),
        "top_sku": top.index[0],
        "top_sku_revenue": float(top.iloc[0]),
        "top_sku_share": float(top.iloc[0] / loja_totals.loc[loja, "revenue"] * 100),
    })

# Family composition
fam_summary = (
    df.groupby("familia")
    .agg(revenue=("valor_total", "sum"), units=("quantidade", "sum"))
    .sort_values("revenue", ascending=False)
)
families_data = [
    {
        "name": fam,
        "revenue": float(r["revenue"]),
        "share_pct": float(r["revenue"] / total_revenue * 100),
        "units": int(r["units"]),
    }
    for fam, r in fam_summary.iterrows()
]

# Brunch (Anjos-only) — keyword match against the real ZSBMS product names.
brunch_pat = r"benedict|florentine|cilbir|avocado|pain perdu|menuet|monsieur|granola|sopa"
brunch = df[df["produto"].str.lower().str.contains(brunch_pat, regex=True, na=False)]
anjos_rev = float(loja_totals.loc["Anjos", "revenue"])
brunch_data = {
    "revenue": float(brunch["valor_total"].sum()),
    "share_pct": float(brunch["valor_total"].sum() / anjos_rev * 100),
    "units": int(brunch["quantidade"].sum()),
}

# Anjos in-house consumption (Drinks + Snacks + Restaurante).
anjos_df = df[df["loja"] == "Anjos"]
anjos_fam = anjos_df.groupby("familia")["valor_total"].sum()
ih = {
    "drinks": float(anjos_fam.get("Drinks", 0)),
    "snacks": float(anjos_fam.get("Snacks", 0)),
    "restaurant": float(anjos_fam.get("Restaurante", 0)),
}
ih["total"] = ih["drinks"] + ih["snacks"] + ih["restaurant"]
ih_pct = {k: v / anjos_rev * 100 for k, v in ih.items()}

# ABC — number of SKUs to reach 80% of revenue per loja.
abc_data = []
for loja in loja_totals.index:
    sku = df[df["loja"] == loja].groupby("produto")["valor_total"].sum().sort_values(ascending=False)
    cum_share = sku.cumsum() / sku.sum()
    a_skus = int((cum_share < 0.80).sum() + 1)
    abc_data.append({
        "loja": loja,
        "total_skus": int(sku.shape[0]),
        "a_skus": a_skus,
        "pct_of_skus": float(a_skus / sku.shape[0] * 100),
    })

# Weekday vs weekend per family
df["is_weekend"] = df["data"].dt.weekday >= 5
day_buckets = (
    df[["data", "is_weekend"]].drop_duplicates().groupby("is_weekend").size()
)
n_wd = int(day_buckets.get(False, 0))
n_we = int(day_buckets.get(True, 0))
ww_families = ["Pastelaria", "Pão/KG", "Pão", "Drinks", "Snacks", "Restaurante"]
ww_data = []
for fam in ww_families:
    fam_df = df[df["familia"] == fam]
    if fam_df.empty:
        continue
    wd = float(fam_df[~fam_df["is_weekend"]]["valor_total"].sum() / max(n_wd, 1))
    we = float(fam_df[fam_df["is_weekend"]]["valor_total"].sum() / max(n_we, 1))
    lift = (we - wd) / wd * 100 if wd else 0
    ww_data.append({"family": fam, "weekday": wd, "weekend": we, "lift_pct": lift})


# =========================================================================
# 3. Number + date helpers (locale-aware formatting)
# =========================================================================
MONTHS = {
    "en": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
    "pt": ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"],
    "fr": ["jan", "fév", "mar", "avr", "mai", "juin", "juil", "août", "sep", "oct", "nov", "déc"],
}


def fmt_int(value: float, locale: str) -> str:
    """Format an integer with locale-appropriate thousand separator."""
    s = f"{int(round(value)):,}"
    if locale == "pt":
        return s.replace(",", ".")
    if locale == "fr":
        return s.replace(",", " ")  # narrow no-break space
    return s  # en


def fmt_money(value: float, locale: str, decimals: int = 0) -> str:
    """Format money. Symbol position differs by locale."""
    if decimals:
        rounded = round(value, decimals)
        int_part = int(rounded)
        frac = abs(rounded - int_part)
        frac_str = f"{frac:.{decimals}f}"[2:]  # ".61" → "61"
        int_str = fmt_int(int_part, locale)
        if locale == "pt":
            return f"€{int_str},{frac_str}"
        if locale == "fr":
            return f"{int_str},{frac_str} €"
        return f"€{int_str}.{frac_str}"
    int_str = fmt_int(value, locale)
    if locale == "fr":
        return f"{int_str} €"
    return f"€{int_str}"


def fmt_pct(value: float, locale: str, decimals: int = 1) -> str:
    s = f"{value:.{decimals}f}"
    if locale in ("pt", "fr"):
        s = s.replace(".", ",")
    return f"{s}%"


def fmt_date_range(period_from: pd.Timestamp, period_to: pd.Timestamp, locale: str) -> str:
    months = MONTHS[locale]
    f_m, t_m = months[period_from.month - 1], months[period_to.month - 1]
    if locale == "en":
        return f"{period_from.day} {f_m} → {period_to.day} {t_m} {period_to.year}"
    # pt and fr share the day-first convention
    sep = "→"
    return f"{period_from.day} {f_m} {sep} {period_to.day} {t_m} {period_to.year}"


PERIOD_FROM = df["data"].min()
PERIOD_TO = df["data"].max()


# =========================================================================
# 4. Translation tables
# =========================================================================
# Family display names per locale. Original taxonomy stays for PT.
FAMILY_NAMES = {
    "en": {
        "Pastelaria": "Pastry",
        "Pão/KG": "Bread (by weight)",
        "Pão": "Bread",
        "Drinks": "Drinks",
        "Snacks": "Snacks",
        "Restaurante": "Restaurant",
        "Outros": "Other",
        "APERITIVO": "Aperitif",
    },
    "pt": {},  # use names as-is
    "fr": {
        "Pastelaria": "Pâtisserie",
        "Pão/KG": "Pain au poids",
        "Pão": "Pain",
        "Drinks": "Boissons",
        "Snacks": "Snacks",
        "Restaurante": "Restauration",
        "Outros": "Autres",
        "APERITIVO": "Apéritif",
    },
}


STRINGS = {
    "en": {
        "lang_label": "EN",
        "lang_full": "English",
        "doc_title": "Lully 1661 · Sales Operations Report",
        "brand": "Lully 1661",
        "report_eyebrow": "Operations Report",
        "title_pre": "Sales analysis —",
        "title_em": "what the numbers say.",
        "period_label": "Period analysed",
        "period_days": "{n} days of trade",
        "source_label": "Source",
        "source_value": "ZSBMS export · Sales Evolution by Product",
        "rows_label": "Lines processed",
        "coverage_label": "Coverage",
        "coverage_value": "{lojas} stores · {skus} SKUs · {fam} families",

        "kpis_eyebrow": "At a glance",
        "kpi_revenue": "Total revenue",
        "kpi_units": "Units sold",
        "kpi_units_unit": "units",
        "kpi_daily": "Revenue per day",
        "kpi_daily_sub": "across all three stores",
        "kpi_ticket": "Avg line ticket",

        "stores_eyebrow": "Where the revenue comes from",
        "stores_title_pre": "Three houses,",
        "stores_title_em": "three weights.",
        "stores_lead": "The three stores share the same name but not the same scale. Anjos drives most of the business; Beato — the historical hearth — sits last.",
        "th_store": "Store",
        "th_revenue": "Revenue",
        "th_share": "% of total",
        "th_rows": "Sales lines",
        "th_top": "Top product",
        "th_top_share": "% of store",
        "obs1": "Anjos is the financial axis of the house: 66% of revenue from one of three stores. Beato — where Lully was born — sits last with 8%, an important gap with the \"Beato is the heart\" narrative. The About page on the website should acknowledge this honestly rather than smooth it over.",

        "family_eyebrow": "Family composition",
        "family_title_pre": "Pastry leads in revenue.",
        "family_title_em": "Bread leads in units.",
        "th_family": "Family",
        "th_revenue_period": "Revenue ({n} days)",
        "th_units": "Units",
        "obs2": "Pastry generates more revenue than Bread + Bread/KG combined, but Bread sells more units. Bread is the traffic driver; pastry is the margin driver. That framing supports keeping bread as the homepage hero and pushing pastry through the in-store windows.",

        "top_products_eyebrow": "Top SKUs over time",
        "top_products_lead": "The ten products that carry the most revenue, week by week.",

        "brunch_eyebrow": "The brunch question",
        "brunch_title_pre": "Brunch —",
        "brunch_title_em": "its real weight in Anjos.",
        "brunch_intro": "Brunch SKUs in the system are named in English: <em>Eggs Benedict</em>, <em>Eggs Florentine</em>, <em>Avocado toast</em>, <em>Le Menuet</em>, <em>Le Monsieur</em>, <em>Pain Perdu</em>, <em>Sopa do Mês</em>, <em>Granola</em> and variants. We match by keyword across product names.",
        "th_metric": "Metric",
        "th_value": "Value",
        "brunch_revenue_label": "Brunch revenue ({n} days)",
        "brunch_share_label": "% of total Anjos revenue",
        "brunch_units_label": "Units sold",
        "obs3": "Named as a category, brunch is about 7% of Anjos — meaningful but not dominant. <strong>This number understates the real brunch operation</strong>, because drinks, coffee and snacks ordered alongside brunch fall under other families. The next section reconstructs the full in-house operation.",

        "anjos_eyebrow": "The structural finding",
        "anjos_title_pre": "Anjos isn't a bakery.",
        "anjos_title_em": "It's a restaurant that bakes its own bread.",
        "anjos_lead": "If we combine the families that map to <strong>in-house consumption</strong> — Drinks, Snacks and Restaurant — the share of Anjos that lives off people staying at the table becomes clear.",
        "th_family_anjos": "Family in Anjos",
        "th_share_anjos": "% of Anjos",
        "anjos_drinks": "Drinks",
        "anjos_snacks": "Snacks",
        "anjos_rest": "Restaurant",
        "anjos_total": "Total in-house consumption",
        "obs4": "<strong>{pct} of Anjos revenue comes from in-house consumption</strong> (Drinks + Snacks + Restaurant), before counting the pastry and bread eaten at the table. Beato and Ourique combined have a completely different profile: counter sales of bread and pastry, with very little sit-down. Anjos isn't a bakery with tables — it's a restaurant that bakes its own bread. Worth considering separate KPIs and reports for Anjos vs. Beato/Ourique.",

        "chart_loja_caption": "Family mix per store — Anjos is the only one with a structurally large in-house tail (Drinks + Snacks + Restaurant ≈ 36%).",

        "abc_eyebrow": "ABC analysis",
        "abc_title_pre": "Long tail —",
        "abc_title_em": "most SKUs barely sell.",
        "abc_lead": "How many products carry 80% of revenue in each store. The smaller the count, the more concentrated — and easier to monitor week by week.",
        "th_total_skus": "Total SKUs",
        "th_a_skus": "SKUs making 80%",
        "th_pct_skus": "% of SKUs",
        "obs5": "The catalogue has a long tail: most SKUs sell very little. For a weekly operational dashboard, the focus should be on the ~{anjos_a} products that make 80% of Anjos — a \"ranking + week-over-week variation\" view of those covers almost every operational decision without noise.",

        "weekend_eyebrow": "Weekday vs weekend",
        "weekend_title_pre": "Where the weekend",
        "weekend_title_em": "actually shows up.",
        "weekend_lead": "Average revenue per day, weekday vs. weekend, per family. \"Lift\" is the weekend-vs-weekday change.",
        "th_weekday_avg": "Weekday avg (€/day)",
        "th_weekend_avg": "Weekend avg (€/day)",
        "th_lift": "Lift",
        "obs6": "Restaurant lifts +81% on weekends — predictable for a sit-down menu. Snacks <em>drop</em> 13% on weekends, suggesting they're a weekday-only behaviour (workday coffee runs, perhaps). The family with the biggest lift is the obvious candidate for weekend-only promotions or staffing rethinks.",

        "recs_eyebrow": "Operational recommendations",
        "recs_title_pre": "Five moves",
        "recs_title_em": "worth a meeting.",
        "recs_lead": "Concrete suggestions to discuss with the client. None require new software — only new attention.",
        "rec1_title": "Weekly SKU dashboard, focused on the \"core 80%\".",
        "rec1_body": "About 30–50 products per store deserve weekly monitoring (revenue, units, WoW variation). The rest is tail — a monthly view is enough.",
        "rec2_title": "Bread for traffic, pastry for margin.",
        "rec2_body": "Bread-by-weight (Pão/KG) generates a high €/unit without depending on novelty. Worth auditing price/kg consistency across the three stores.",
        "rec3_title": "Treat Anjos as a restaurant, not a bakery.",
        "rec3_body": "{pct} of Anjos revenue is in-house consumption (Drinks + Snacks + Restaurant), before counting pastry and bread at the table. KPIs, staffing and product mix should be defined separately from Beato/Ourique — which are counter bakeries.",
        "rec4_title": "Beato needs a deliberate decision.",
        "rec4_body": "With {beato} over {n} days ({beato_daily}/day), Beato can be: (a) a production house that sells the by-product over the counter, (b) a relocation candidate, (c) a brand-narrative pillar for the ecosystem. The three have different implications for the website's voice.",
        "rec5_title": "Family taxonomy needs a cleanup pass.",
        "rec5_body": "There are inconsistent family/sub-family strings (\"APERITIVO\", \"Outros\"). Before any serious dashboard, a normalisation session inside ZSBMS is worth one afternoon — otherwise every analysis re-invents the wheel.",

        "files_eyebrow": "Methodology",
        "files_title": "Files behind this report.",
        "files_lead": "All five charts plus the underlying CSV live next to this file.",
        "file_chart_01": "Weekly revenue per family, stacked area.",
        "file_chart_02": "Top 10 products, weekly revenue.",
        "file_chart_03": "Family mix per store, stacked bars.",
        "file_chart_04": "ABC concentration of revenue per store.",
        "file_chart_05": "Weekday vs weekend pattern.",
        "footer_credit": "Lully 1661 · operations report",
        "footer_generated": "Generated",
    },

    "pt": {
        "lang_label": "PT",
        "lang_full": "Português",
        "doc_title": "Lully 1661 · Relatório operacional de vendas",
        "brand": "Lully 1661",
        "report_eyebrow": "Relatório operacional",
        "title_pre": "Análise de vendas —",
        "title_em": "o que dizem os números.",
        "period_label": "Período analisado",
        "period_days": "{n} dias de operação",
        "source_label": "Fonte",
        "source_value": "Export ZSBMS · Evolução de vendas por produto",
        "rows_label": "Linhas processadas",
        "coverage_label": "Cobertura",
        "coverage_value": "{lojas} lojas · {skus} SKUs · {fam} famílias",

        "kpis_eyebrow": "Indicadores principais",
        "kpi_revenue": "Receita total",
        "kpi_units": "Unidades vendidas",
        "kpi_units_unit": "unidades",
        "kpi_daily": "Receita por dia",
        "kpi_daily_sub": "agregada às três lojas",
        "kpi_ticket": "Ticket médio por linha",

        "stores_eyebrow": "De onde vem a receita",
        "stores_title_pre": "Três casas,",
        "stores_title_em": "três pesos.",
        "stores_lead": "As três lojas partilham nome e marca, mas não escala. Anjos sustenta a maior parte do negócio; Beato — a casa fundadora — fica em último.",
        "th_store": "Loja",
        "th_revenue": "Receita",
        "th_share": "% do total",
        "th_rows": "Linhas de venda",
        "th_top": "Produto top",
        "th_top_share": "% da loja",
        "obs1": "Anjos é o eixo financeiro da casa: 66% da receita com apenas uma das três lojas. Beato, apesar de ser onde nasceu a Lully, está em terceiro com 8% — desvio importante face à narrativa \"Beato é o coração\". A página /sobre do website deve reconhecer este facto sem o esconder.",

        "family_eyebrow": "Composição por família",
        "family_title_pre": "Pastelaria lidera em receita.",
        "family_title_em": "Pão lidera em unidades.",
        "th_family": "Família",
        "th_revenue_period": "Receita ({n} dias)",
        "th_units": "Unidades",
        "obs2": "Pastelaria gera mais receita do que Pão + Pão/KG combinados, mas o pão vende mais unidades. O pão é o <em>driver de tráfego</em>; a pastelaria é o <em>driver de margem</em>. Visto assim, faz sentido manter o pão como herói da homepage e empurrar a pastelaria nas vitrines de loja.",

        "top_products_eyebrow": "Top SKUs ao longo do tempo",
        "top_products_lead": "Os dez produtos que sustentam mais receita, semana a semana.",

        "brunch_eyebrow": "A pergunta do brunch",
        "brunch_title_pre": "Brunch —",
        "brunch_title_em": "o seu peso real em Anjos.",
        "brunch_intro": "Os SKUs de brunch no sistema chamam-se em inglês: <em>Eggs Benedict</em>, <em>Eggs Florentine</em>, <em>Avocado toast</em>, <em>Le Menuet</em>, <em>Le Monsieur</em>, <em>Pain Perdu</em>, <em>Sopa do Mês</em>, <em>Granola</em> e variantes. Análise feita por correspondência de palavra-chave nos nomes de produto.",
        "th_metric": "Métrica",
        "th_value": "Valor",
        "brunch_revenue_label": "Receita brunch ({n} dias)",
        "brunch_share_label": "% da receita total de Anjos",
        "brunch_units_label": "Unidades vendidas",
        "obs3": "O brunch enquanto categoria explícita representa cerca de 7% da receita de Anjos — é uma faixa significativa, mas não dominante. <strong>Este número subestima a operação brunch real</strong>, porque as bebidas, café e snacks pedidos junto do brunch caem em outras famílias. A próxima secção reconstrói a operação de consumo no local na sua escala verdadeira.",

        "anjos_eyebrow": "O achado estrutural",
        "anjos_title_pre": "Anjos não é uma padaria.",
        "anjos_title_em": "É um restaurante que coze o seu próprio pão.",
        "anjos_lead": "Se juntarmos as famílias que correspondem a <strong>consumo no local</strong> — Drinks, Snacks e Restaurante — fica claro o peso real do \"ficar à mesa\" em Anjos.",
        "th_family_anjos": "Família em Anjos",
        "th_share_anjos": "% de Anjos",
        "anjos_drinks": "Drinks",
        "anjos_snacks": "Snacks",
        "anjos_rest": "Restaurante",
        "anjos_total": "Total consumo no local",
        "obs4": "<strong>{pct} da receita de Anjos vem de consumo no local</strong> (Drinks + Snacks + Restaurante), antes mesmo de contar a pastelaria e o pão consumidos à mesa. As outras duas lojas (Beato + Ourique) têm um perfil completamente diferente: pão e pastelaria de balcão, com pouca componente de \"ficar à mesa\". Anjos não é uma padaria com mesas — é um restaurante que coze o seu próprio pão. Vale a pena considerar separar os relatórios e KPIs internos de Anjos vs. Beato/Ourique.",

        "chart_loja_caption": "Mix por família em cada loja — Anjos é a única com uma cauda estrutural de consumo no local (Drinks + Snacks + Restaurante ≈ 36%).",

        "abc_eyebrow": "Análise ABC",
        "abc_title_pre": "Cauda longa —",
        "abc_title_em": "a maioria dos SKUs quase não vende.",
        "abc_lead": "Quantos produtos sustentam 80% da receita em cada loja. Quanto menor o número, mais concentrada — e mais fácil de monitorizar semana a semana.",
        "th_total_skus": "Total SKUs",
        "th_a_skus": "SKUs que fazem 80%",
        "th_pct_skus": "% dos SKUs",
        "obs5": "O catálogo da casa tem cauda longa: a maioria dos SKUs vende muito pouco. Para um dashboard semanal de operação, o foco deve ser nos ~{anjos_a} produtos que fazem 80% em Anjos — uma vista \"ranking + variação semana-sobre-semana\" desses produtos cobre quase toda a decisão operacional sem ruído.",

        "weekend_eyebrow": "Semana vs fim-de-semana",
        "weekend_title_pre": "Onde o fim-de-semana",
        "weekend_title_em": "realmente aparece.",
        "weekend_lead": "Receita média por dia, dia útil vs. fim-de-semana, por família. \"Lift\" é a variação fim-de-semana vs. dia útil.",
        "th_weekday_avg": "Média dia útil (€/dia)",
        "th_weekend_avg": "Média fim-de-semana (€/dia)",
        "th_lift": "Lift",
        "obs6": "Restaurante sobe +81% ao fim-de-semana — previsível para um menu de mesa. Snacks <em>caem</em> 13% ao fim-de-semana, sugerindo um comportamento de dia útil (cafés de manhã na ida para o trabalho, talvez). A família com maior lift é candidata óbvia a promoção fim-de-semana ou a rever staffing/produção sábado-domingo.",

        "recs_eyebrow": "Recomendações operacionais",
        "recs_title_pre": "Cinco movimentos",
        "recs_title_em": "que valem uma reunião.",
        "recs_lead": "Sugestões concretas a discutir com o cliente. Nenhuma exige novo software — apenas nova atenção.",
        "rec1_title": "Dashboard semanal de SKU \"core 80%\".",
        "rec1_body": "Cerca de 30–50 produtos por loja merecem monitorização semanal (receita, unidades, variação WoW). Os restantes são cauda — visão mensal chega.",
        "rec2_title": "Pão como tráfego, pastelaria como margem.",
        "rec2_body": "Os preços de pão a peso (Pão/KG) gerem €/unidade alto sem dependerem de novidade. Vale auditar a consistência de preço/kg entre as três lojas.",
        "rec3_title": "Tratar Anjos como restaurante, não como padaria.",
        "rec3_body": "{pct} da receita de Anjos é consumo no local (Drinks + Snacks + Restaurante), antes de contar pastelaria e pão consumidos à mesa. KPIs, staffing e mix de produto deviam ser definidos separadamente de Beato/Ourique — que são padarias de balcão.",
        "rec4_title": "Beato precisa de uma decisão consciente.",
        "rec4_body": "Com {beato} em {n} dias ({beato_daily}/dia), Beato pode ser: (a) loja-de-produção que vende sub-produto a balcão, (b) candidata a relocalização, (c) força de marca para o ecossistema. Os três têm implicações diferentes para a comunicação no site.",
        "rec5_title": "Limpar a taxonomia de famílias.",
        "rec5_body": "Existem strings de família/sub-família inconsistentes (\"APERITIVO\", \"Outros\"). Antes de qualquer dashboard sério, vale uma sessão de normalização das categorias dentro do ZSBMS — caso contrário cada análise reinventa a roda.",

        "files_eyebrow": "Metodologia",
        "files_title": "Ficheiros desta análise.",
        "files_lead": "Os cinco gráficos e o CSV bruto estão ao lado deste ficheiro.",
        "file_chart_01": "Receita semanal por família, área empilhada.",
        "file_chart_02": "Top 10 produtos, receita semanal.",
        "file_chart_03": "Mix por família em cada loja, barras empilhadas.",
        "file_chart_04": "Concentração ABC de receita por loja.",
        "file_chart_05": "Padrão semana vs. fim-de-semana.",
        "footer_credit": "Lully 1661 · relatório operacional",
        "footer_generated": "Gerado em",
    },

    "fr": {
        "lang_label": "FR",
        "lang_full": "Français",
        "doc_title": "Lully 1661 · Rapport opérationnel des ventes",
        "brand": "Lully 1661",
        "report_eyebrow": "Rapport opérationnel",
        "title_pre": "Analyse des ventes —",
        "title_em": "ce que disent les chiffres.",
        "period_label": "Période analysée",
        "period_days": "{n} jours d'opération",
        "source_label": "Source",
        "source_value": "Export ZSBMS · Évolution des ventes par produit",
        "rows_label": "Lignes traitées",
        "coverage_label": "Couverture",
        "coverage_value": "{lojas} boutiques · {skus} SKUs · {fam} familles",

        "kpis_eyebrow": "En un coup d'œil",
        "kpi_revenue": "Chiffre d'affaires total",
        "kpi_units": "Unités vendues",
        "kpi_units_unit": "unités",
        "kpi_daily": "CA par jour",
        "kpi_daily_sub": "agrégé sur les trois boutiques",
        "kpi_ticket": "Ticket moyen par ligne",

        "stores_eyebrow": "D'où vient le chiffre d'affaires",
        "stores_title_pre": "Trois maisons,",
        "stores_title_em": "trois poids.",
        "stores_lead": "Les trois boutiques partagent le nom et la marque, mais pas l'échelle. Anjos porte l'essentiel du business ; Beato — la maison fondatrice — arrive en dernier.",
        "th_store": "Boutique",
        "th_revenue": "CA",
        "th_share": "% du total",
        "th_rows": "Lignes de vente",
        "th_top": "Produit phare",
        "th_top_share": "% de la boutique",
        "obs1": "Anjos est l'axe financier de la maison : 66% du chiffre d'affaires sur une seule des trois boutiques. Beato — pourtant la maison-mère de Lully — arrive en dernier avec 8%, un écart important avec le récit \"Beato, c'est le cœur\". La page À propos du site devrait reconnaître ce fait honnêtement plutôt que le lisser.",

        "family_eyebrow": "Composition par famille",
        "family_title_pre": "La pâtisserie domine en CA.",
        "family_title_em": "Le pain domine en unités.",
        "th_family": "Famille",
        "th_revenue_period": "CA ({n} jours)",
        "th_units": "Unités",
        "obs2": "La pâtisserie génère plus de CA que Pain + Pain au poids réunis, mais le pain vend plus d'unités. Le pain est le <em>moteur de trafic</em> ; la pâtisserie est le <em>moteur de marge</em>. Vu ainsi, il est cohérent de garder le pain comme héros de la page d'accueil et de pousser la pâtisserie dans les vitrines en boutique.",

        "top_products_eyebrow": "Top SKUs dans le temps",
        "top_products_lead": "Les dix produits qui portent le plus de CA, semaine après semaine.",

        "brunch_eyebrow": "La question du brunch",
        "brunch_title_pre": "Brunch —",
        "brunch_title_em": "son poids réel à Anjos.",
        "brunch_intro": "Les SKUs de brunch dans le système ont des noms anglais : <em>Eggs Benedict</em>, <em>Eggs Florentine</em>, <em>Avocado toast</em>, <em>Le Menuet</em>, <em>Le Monsieur</em>, <em>Pain Perdu</em>, <em>Sopa do Mês</em>, <em>Granola</em> et variantes. La correspondance se fait par mots-clés sur les noms produit.",
        "th_metric": "Métrique",
        "th_value": "Valeur",
        "brunch_revenue_label": "CA brunch ({n} jours)",
        "brunch_share_label": "% du CA total d'Anjos",
        "brunch_units_label": "Unités vendues",
        "obs3": "Comme catégorie explicite, le brunch représente environ 7% du CA d'Anjos — significatif mais pas dominant. <strong>Ce chiffre sous-estime l'opération brunch réelle</strong>, car les boissons, cafés et snacks commandés avec le brunch tombent dans d'autres familles. La section suivante reconstruit l'opération de consommation sur place à sa vraie échelle.",

        "anjos_eyebrow": "La trouvaille structurelle",
        "anjos_title_pre": "Anjos n'est pas une boulangerie.",
        "anjos_title_em": "C'est un restaurant qui cuit son propre pain.",
        "anjos_lead": "En regroupant les familles qui correspondent à la <strong>consommation sur place</strong> — Boissons, Snacks et Restauration — le poids réel du \"rester à table\" à Anjos devient lisible.",
        "th_family_anjos": "Famille à Anjos",
        "th_share_anjos": "% d'Anjos",
        "anjos_drinks": "Boissons",
        "anjos_snacks": "Snacks",
        "anjos_rest": "Restauration",
        "anjos_total": "Total consommation sur place",
        "obs4": "<strong>{pct} du CA d'Anjos vient de la consommation sur place</strong> (Boissons + Snacks + Restauration), avant même de compter la pâtisserie et le pain consommés à table. Beato et Ourique combinés ont un profil totalement différent : vente au comptoir de pain et pâtisserie, très peu de service à table. Anjos n'est pas une boulangerie avec quelques tables — c'est un restaurant qui cuit son propre pain. Il vaut la peine d'envisager des KPI et reportings séparés pour Anjos vs. Beato/Ourique.",

        "chart_loja_caption": "Mix par famille par boutique — Anjos est la seule avec une queue structurelle de consommation sur place (Boissons + Snacks + Restauration ≈ 36%).",

        "abc_eyebrow": "Analyse ABC",
        "abc_title_pre": "Longue traîne —",
        "abc_title_em": "la plupart des SKUs vendent à peine.",
        "abc_lead": "Combien de produits portent 80% du CA dans chaque boutique. Plus le nombre est petit, plus c'est concentré — et plus c'est simple à suivre semaine après semaine.",
        "th_total_skus": "Total SKUs",
        "th_a_skus": "SKUs faisant 80%",
        "th_pct_skus": "% des SKUs",
        "obs5": "Le catalogue a une longue traîne : la plupart des SKUs vendent très peu. Pour un tableau de bord opérationnel hebdomadaire, l'attention doit aller sur les ~{anjos_a} produits qui font 80% à Anjos — une vue \"classement + variation semaine-sur-semaine\" de ces produits couvre presque toute la décision opérationnelle sans bruit.",

        "weekend_eyebrow": "Semaine vs week-end",
        "weekend_title_pre": "Où le week-end",
        "weekend_title_em": "se voit vraiment.",
        "weekend_lead": "CA moyen par jour, en semaine vs. week-end, par famille. Le \"lift\" est la variation week-end / semaine.",
        "th_weekday_avg": "Moyenne en semaine (€/jour)",
        "th_weekend_avg": "Moyenne week-end (€/jour)",
        "th_lift": "Lift",
        "obs6": "La Restauration monte de +81% le week-end — prévisible pour un menu à table. Les Snacks <em>baissent</em> de 13% le week-end, suggérant un comportement de semaine (café du matin sur le trajet du travail, peut-être). La famille au plus gros lift est la candidate évidente pour des promotions week-end ou un rééquilibrage de staffing/production samedi-dimanche.",

        "recs_eyebrow": "Recommandations opérationnelles",
        "recs_title_pre": "Cinq mouvements",
        "recs_title_em": "qui valent une réunion.",
        "recs_lead": "Suggestions concrètes à discuter avec le client. Aucune n'exige un nouveau logiciel — seulement une nouvelle attention.",
        "rec1_title": "Tableau de bord hebdomadaire des SKU « core 80% ».",
        "rec1_body": "Environ 30–50 produits par boutique méritent un suivi hebdomadaire (CA, unités, variation WoW). Le reste est de la traîne — une vue mensuelle suffit.",
        "rec2_title": "Le pain pour le trafic, la pâtisserie pour la marge.",
        "rec2_body": "Le pain au poids (Pão/KG) génère un €/unité élevé sans dépendre de la nouveauté. Vaut la peine d'auditer la cohérence du prix/kg entre les trois boutiques.",
        "rec3_title": "Traiter Anjos comme un restaurant, pas comme une boulangerie.",
        "rec3_body": "{pct} du CA d'Anjos est de la consommation sur place (Boissons + Snacks + Restauration), avant même de compter la pâtisserie et le pain à table. KPI, staffing et mix produit devraient être définis séparément de Beato/Ourique — qui sont des boulangeries-comptoir.",
        "rec4_title": "Beato a besoin d'une décision consciente.",
        "rec4_body": "Avec {beato} sur {n} jours ({beato_daily}/jour), Beato peut être : (a) une maison de production qui vend le sous-produit au comptoir, (b) une candidate à la relocalisation, (c) un pilier narratif de marque pour l'écosystème. Les trois ont des implications différentes pour le ton du site.",
        "rec5_title": "Nettoyer la taxonomie des familles.",
        "rec5_body": "Il existe des chaînes famille/sous-famille incohérentes (\"APERITIVO\", \"Outros\"). Avant tout tableau de bord sérieux, une session de normalisation des catégories dans ZSBMS vaut bien un après-midi — sinon chaque analyse réinvente la roue.",

        "files_eyebrow": "Méthodologie",
        "files_title": "Fichiers derrière ce rapport.",
        "files_lead": "Les cinq graphiques et le CSV brut se trouvent à côté de ce fichier.",
        "file_chart_01": "CA hebdomadaire par famille, aires empilées.",
        "file_chart_02": "Top 10 produits, CA hebdomadaire.",
        "file_chart_03": "Mix par famille par boutique, barres empilées.",
        "file_chart_04": "Concentration ABC du CA par boutique.",
        "file_chart_05": "Motif semaine vs. week-end.",
        "footer_credit": "Lully 1661 · rapport opérationnel",
        "footer_generated": "Généré le",
    },
}


# =========================================================================
# 5. Inline CSS (design system tokens, paper background, Fraunces + IS + IS)
# =========================================================================
CSS = """
:root {
  --paper: #f4eedf;
  --paper-2: #efe6d4;
  --paper-3: #e9dfc7;
  --ink: #1a1613;
  --ink-2: #3c342e;
  --ink-3: #5a5048;
  --stone: #7a746b;
  --gold: #a68a3e;
  --gold-2: #c2a04a;
  --ember: #b8563d;
  --rule: rgba(26, 22, 19, 0.14);
  --rule-strong: rgba(26, 22, 19, 0.28);
  --font-display: 'Fraunces', Georgia, 'Times New Roman', serif;
  --font-accent: 'Instrument Serif', Georgia, serif;
  --font-body: 'Instrument Sans', system-ui, -apple-system, sans-serif;
  --ease-out: cubic-bezier(0.22, 1, 0.36, 1);
}

* { box-sizing: border-box; }

html, body { background: var(--paper); }

body {
  margin: 0;
  color: var(--ink);
  font-family: var(--font-body);
  font-size: 16px;
  line-height: 1.6;
  font-feature-settings: "ss01", "case";
  -webkit-font-smoothing: antialiased;
}

/* --- Layout primitives ------------------------------------------------- */
.shell { max-width: 980px; margin: 0 auto; padding: 0 32px; }
@media (max-width: 720px) { .shell { padding: 0 20px; } }

section { padding: 88px 0; border-bottom: 1px solid var(--rule); }
section.tight { padding: 56px 0; }
@media (max-width: 720px) { section { padding: 56px 0; } }

/* --- Top bar (brand + language switcher) ------------------------------ */
.topbar {
  display: flex; align-items: center; justify-content: space-between;
  padding: 22px 32px; border-bottom: 1px solid var(--rule);
}
.topbar .brand {
  font-family: var(--font-display);
  font-weight: 400;
  font-variation-settings: "opsz" 144;
  font-size: 22px;
  letter-spacing: 0.04em;
  text-transform: lowercase;
  color: var(--ink);
}
.topbar .brand em { font-style: italic; color: var(--ember); }
.langswitch { display: flex; gap: 14px; font-size: 11px; letter-spacing: 0.22em; text-transform: uppercase; }
.langswitch a { color: var(--stone); text-decoration: none; transition: color 160ms var(--ease-out); }
.langswitch a:hover { color: var(--ember); }
.langswitch a.current { color: var(--ink); border-bottom: 1px solid var(--gold); padding-bottom: 2px; }

/* --- Eyebrow ---------------------------------------------------------- */
.eyebrow {
  font-size: 11px;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  color: var(--gold);
  font-weight: 500;
  display: inline-block;
  margin-bottom: 18px;
}

/* --- Display title ---------------------------------------------------- */
h1.display, h2.display, h3.display {
  font-family: var(--font-display);
  font-weight: 400;
  font-variation-settings: "opsz" 144;
  color: var(--ink);
  letter-spacing: -0.015em;
  margin: 0;
}
h1.display { font-size: clamp(40px, 6vw, 64px); line-height: 1.04; margin-bottom: 24px; }
h2.display { font-size: clamp(32px, 4.5vw, 44px); line-height: 1.08; margin-bottom: 20px; }
h3.display { font-size: clamp(22px, 2.6vw, 28px); line-height: 1.2; margin-bottom: 12px; }
h1.display em, h2.display em, h3.display em {
  font-family: var(--font-accent);
  font-style: italic;
  color: var(--ember);
  font-weight: 400;
}

/* --- Body text -------------------------------------------------------- */
p.lead { font-size: 18px; line-height: 1.6; color: var(--ink-2); max-width: 62ch; margin: 0 0 16px; }
p { color: var(--ink-2); margin: 0 0 14px; max-width: 70ch; }

/* --- Hero -------------------------------------------------------------- */
.hero { padding: 96px 0 72px; }
.hero .meta-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 28px 56px;
  padding-top: 36px;
  border-top: 1px solid var(--rule);
  margin-top: 56px;
  max-width: 760px;
}
.hero .meta-item { font-size: 14px; line-height: 1.5; }
.hero .meta-item .meta-label {
  display: block;
  font-size: 10px;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  color: var(--stone);
  margin-bottom: 6px;
}
.hero .meta-item .meta-value { color: var(--ink); }
.hero .meta-item .meta-value em { font-family: var(--font-accent); font-style: italic; color: var(--ember); }

/* --- KPI cards -------------------------------------------------------- */
.kpis {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 0;
  margin-top: 16px;
  border-top: 1px solid var(--rule);
  border-bottom: 1px solid var(--rule);
}
@media (max-width: 880px) { .kpis { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
.kpi {
  padding: 32px 28px;
  border-right: 1px solid var(--rule);
}
.kpi:last-child { border-right: 0; }
@media (max-width: 880px) {
  .kpi { border-right: 0; border-bottom: 1px solid var(--rule); }
  .kpi:nth-last-child(-n+2) { border-bottom: 0; }
  .kpi:nth-child(odd) { border-right: 1px solid var(--rule); }
}
.kpi .kpi-label {
  font-size: 10px;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  color: var(--stone);
  margin-bottom: 12px;
}
.kpi .kpi-value {
  font-family: var(--font-display);
  font-variation-settings: "opsz" 72;
  font-weight: 400;
  font-size: clamp(28px, 3vw, 36px);
  line-height: 1.1;
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

/* --- Tables ----------------------------------------------------------- */
table.data {
  width: 100%;
  border-collapse: collapse;
  margin: 28px 0 18px;
  font-size: 15px;
}
table.data th, table.data td {
  padding: 14px 16px;
  text-align: left;
  border-bottom: 1px solid var(--rule);
  font-variant-numeric: tabular-nums;
}
table.data th {
  font-size: 10px;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: var(--stone);
  font-weight: 500;
  border-bottom: 1px solid var(--rule-strong);
}
table.data td { color: var(--ink); }
table.data td.muted { color: var(--ink-3); }
table.data td.num, table.data th.num { text-align: right; }
table.data tr.total td { font-weight: 600; color: var(--ink); border-bottom: 0; padding-top: 18px; }
table.data tr.total td:first-child { font-style: italic; font-family: var(--font-accent); font-size: 17px; font-weight: 400; }
table.data tr.total { border-top: 1px solid var(--rule-strong); }
table.data tr td:first-child { color: var(--ink); }
table.data tr td.store-name { font-weight: 500; }
table.data tr td .row-sub { display: block; font-size: 12px; color: var(--stone); font-style: italic; font-family: var(--font-accent); margin-top: 2px; }

/* --- Observation callouts -------------------------------------------- */
.obs {
  background: var(--paper-2);
  border-left: 3px solid var(--gold);
  padding: 22px 26px;
  margin: 28px 0 6px;
  font-family: var(--font-accent);
  font-style: italic;
  font-size: 18px;
  line-height: 1.55;
  color: var(--ink-2);
  break-inside: avoid;
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
.obs em { color: var(--ink); font-style: italic; }

/* --- Charts ----------------------------------------------------------- */
figure.chart {
  margin: 28px 0 14px;
  background: var(--paper);
  border: 1px solid var(--rule);
  padding: 18px;
  break-inside: avoid;
}
figure.chart img { display: block; width: 100%; height: auto; }
figure.chart figcaption {
  margin-top: 14px;
  font-family: var(--font-accent);
  font-style: italic;
  font-size: 14px;
  color: var(--stone);
  text-align: center;
  line-height: 1.5;
}

/* --- Recommendations -------------------------------------------------- */
.recs { display: flex; flex-direction: column; gap: 24px; margin-top: 36px; }
.rec {
  display: grid;
  grid-template-columns: 60px 1fr;
  gap: 24px;
  padding: 24px 0 24px;
  border-bottom: 1px solid var(--rule);
  break-inside: avoid;
}
.rec:last-child { border-bottom: 0; }
.rec .rec-num {
  font-family: var(--font-display);
  font-variation-settings: "opsz" 144;
  font-size: 48px;
  line-height: 1;
  color: var(--gold);
  font-weight: 400;
  font-variant-numeric: tabular-nums;
}
.rec .rec-body h4 {
  font-family: var(--font-display);
  font-variation-settings: "opsz" 72;
  font-weight: 400;
  font-size: 21px;
  line-height: 1.25;
  margin: 0 0 8px;
  color: var(--ink);
}
.rec .rec-body p { margin: 0; color: var(--ink-2); font-size: 15px; }
.rec .rec-body p strong { color: var(--ember); font-weight: 600; }

/* --- Files list ------------------------------------------------------- */
ul.files { list-style: none; padding: 0; margin: 28px 0 0; }
ul.files li {
  padding: 14px 0;
  border-bottom: 1px solid var(--rule);
  display: grid;
  grid-template-columns: 220px 1fr;
  gap: 24px;
  font-size: 14px;
}
ul.files li:last-child { border-bottom: 0; }
ul.files .file-name {
  font-family: var(--font-body);
  color: var(--ink);
  font-feature-settings: "tnum";
  font-size: 13px;
}
ul.files .file-desc {
  color: var(--stone);
  font-family: var(--font-accent);
  font-style: italic;
}

/* --- Footer ----------------------------------------------------------- */
footer.site {
  background: var(--ink);
  color: var(--paper);
  padding: 56px 32px;
}
footer.site .shell { display: flex; flex-direction: column; gap: 16px; }
footer.site .brand {
  font-family: var(--font-display);
  font-variation-settings: "opsz" 144;
  font-size: 22px;
  text-transform: lowercase;
  letter-spacing: 0.04em;
}
footer.site .brand em { color: var(--gold-2); font-family: var(--font-accent); font-style: italic; }
footer.site .credit { font-size: 12px; letter-spacing: 0.18em; text-transform: uppercase; color: rgba(244, 238, 223, 0.5); }
footer.site .generated { font-size: 13px; color: rgba(244, 238, 223, 0.7); font-family: var(--font-accent); font-style: italic; }

/* --- Index page (cross-language landing) ----------------------------- */
.index-hero { padding: 120px 0 40px; }
.index-cards {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 0;
  margin: 56px 0;
  border-top: 1px solid var(--rule);
  border-bottom: 1px solid var(--rule);
}
@media (max-width: 760px) { .index-cards { grid-template-columns: 1fr; } }
.index-cards a {
  display: block;
  padding: 36px 28px;
  text-decoration: none;
  color: var(--ink);
  border-right: 1px solid var(--rule);
  transition: background 200ms var(--ease-out);
}
.index-cards a:last-child { border-right: 0; }
@media (max-width: 760px) {
  .index-cards a { border-right: 0; border-bottom: 1px solid var(--rule); }
  .index-cards a:last-child { border-bottom: 0; }
}
.index-cards a:hover { background: var(--paper-2); }
.index-cards .lang-code {
  font-family: var(--font-display);
  font-variation-settings: "opsz" 144;
  font-size: 56px;
  line-height: 1;
  color: var(--ember);
}
.index-cards .lang-name {
  display: block;
  margin-top: 16px;
  font-family: var(--font-accent);
  font-style: italic;
  font-size: 18px;
  color: var(--ink-2);
}
.index-cards .lang-arrow {
  display: block;
  margin-top: 24px;
  font-size: 11px;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  color: var(--gold);
}

/* --- Print styles ----------------------------------------------------- */
@media print {
  body { background: white; color: black; font-size: 11pt; }
  .topbar, .langswitch, footer.site { display: none; }
  section { padding: 32px 0; break-inside: avoid-page; }
  .recs .rec, figure.chart, .obs, table.data { break-inside: avoid; }
  h1.display, h2.display { break-after: avoid; }
  .kpis { border-color: #888; }
  .kpi { border-color: #888; }
  .obs { background: #f7f3e8; }
}
"""


# =========================================================================
# 6. HTML rendering
# =========================================================================
def fam_label(name: str, locale: str) -> str:
    return FAMILY_NAMES[locale].get(name, name)


def render_report(locale: str) -> str:
    s = STRINGS[locale]
    L = lambda v: fmt_money(v, locale)
    LU = lambda v: fmt_int(v, locale)
    LP = lambda v, d=1: fmt_pct(v, locale, d)
    M = lambda v: fmt_money(v, locale, decimals=2)
    daterange = fmt_date_range(PERIOD_FROM, PERIOD_TO, locale)

    # Language switcher (current locale gets .current class)
    lang_switch = " ".join(
        f'<a href="report-{lc}.html" class="{"current" if lc == locale else ""}">{STRINGS[lc]["lang_label"]}</a>'
        for lc in ("en", "pt", "fr")
    )

    # Coverage line
    coverage = s["coverage_value"].format(
        lojas=LU(3), skus=LU(196), fam=LU(8),
    )

    # KPIs
    kpis_html = f"""
    <div class="kpis">
      <div class="kpi">
        <div class="kpi-label">{s['kpi_revenue']}</div>
        <div class="kpi-value">{L(total_revenue)}</div>
      </div>
      <div class="kpi">
        <div class="kpi-label">{s['kpi_units']}</div>
        <div class="kpi-value">{LU(total_units)}</div>
        <div class="kpi-sub">{s['kpi_units_unit']}</div>
      </div>
      <div class="kpi">
        <div class="kpi-label">{s['kpi_daily']}</div>
        <div class="kpi-value">{L(avg_daily)}</div>
        <div class="kpi-sub">{s['kpi_daily_sub']}</div>
      </div>
      <div class="kpi">
        <div class="kpi-label">{s['kpi_ticket']}</div>
        <div class="kpi-value">{M(avg_ticket)}</div>
      </div>
    </div>
    """

    # Stores table (+ top SKU as row-sub)
    stores_rows = "\n".join(
        f"""
      <tr>
        <td class="store-name">{lo['name']}<span class="row-sub">{s['th_top']}: {lo['top_sku']} · {L(lo['top_sku_revenue'])} · {LP(lo['top_sku_share'])}</span></td>
        <td class="num">{L(lo['revenue'])}</td>
        <td class="num">{LP(lo['share_pct'])}</td>
        <td class="num">{LU(lo['rows'])}</td>
      </tr>"""
        for lo in lojas_data
    )

    # Family composition table
    family_rows = "\n".join(
        f"""
      <tr>
        <td>{fam_label(f['name'], locale)}</td>
        <td class="num">{L(f['revenue'])}</td>
        <td class="num">{LP(f['share_pct'])}</td>
        <td class="num">{LU(f['units'])}</td>
      </tr>"""
        for f in families_data
    )

    # Brunch table
    brunch_html = f"""
    <table class="data">
      <thead><tr>
        <th>{s['th_metric']}</th>
        <th class="num">{s['th_value']}</th>
      </tr></thead>
      <tbody>
        <tr><td>{s['brunch_revenue_label'].format(n=n_days)}</td><td class="num">{L(brunch_data['revenue'])}</td></tr>
        <tr><td>{s['brunch_share_label']}</td><td class="num">{LP(brunch_data['share_pct'])}</td></tr>
        <tr><td>{s['brunch_units_label']}</td><td class="num">{LU(brunch_data['units'])}</td></tr>
      </tbody>
    </table>
    """

    # Anjos in-house table
    anjos_html = f"""
    <table class="data">
      <thead><tr>
        <th>{s['th_family_anjos']}</th>
        <th class="num">{s['th_revenue']}</th>
        <th class="num">{s['th_share_anjos']}</th>
      </tr></thead>
      <tbody>
        <tr><td>{s['anjos_drinks']}</td><td class="num">{L(ih['drinks'])}</td><td class="num">{LP(ih_pct['drinks'])}</td></tr>
        <tr><td>{s['anjos_snacks']}</td><td class="num">{L(ih['snacks'])}</td><td class="num">{LP(ih_pct['snacks'])}</td></tr>
        <tr><td>{s['anjos_rest']}</td><td class="num">{L(ih['restaurant'])}</td><td class="num">{LP(ih_pct['restaurant'])}</td></tr>
        <tr class="total"><td>{s['anjos_total']}</td><td class="num">{L(ih['total'])}</td><td class="num">{LP(ih_pct['total'])}</td></tr>
      </tbody>
    </table>
    """

    # ABC table
    abc_rows = "\n".join(
        f"""
      <tr>
        <td class="store-name">{a['loja']}</td>
        <td class="num">{LU(a['total_skus'])}</td>
        <td class="num">{LU(a['a_skus'])}</td>
        <td class="num">{LP(a['pct_of_skus'])}</td>
      </tr>"""
        for a in abc_data
    )

    # Weekend table
    ww_rows = "\n".join(
        f"""
      <tr>
        <td>{fam_label(w['family'], locale)}</td>
        <td class="num">{L(w['weekday'])}</td>
        <td class="num">{L(w['weekend'])}</td>
        <td class="num">{('+' if w['lift_pct'] >= 0 else '')}{LP(w['lift_pct'], 0)}</td>
      </tr>"""
        for w in ww_data
    )

    # Recommendations
    anjos_a_skus = next(a["a_skus"] for a in abc_data if a["loja"] == "Anjos")
    beato = next(lo for lo in lojas_data if lo["name"] == "Beato")
    beato_daily = beato["revenue"] / n_days
    recs_html = ""
    for i, (title_k, body_k, extra) in enumerate([
        ("rec1_title", "rec1_body", {}),
        ("rec2_title", "rec2_body", {}),
        ("rec3_title", "rec3_body", {"pct": LP(ih_pct["total"], 0)}),
        ("rec4_title", "rec4_body", {
            "beato": L(beato["revenue"]),
            "n": n_days,
            "beato_daily": L(beato_daily),
        }),
        ("rec5_title", "rec5_body", {}),
    ], 1):
        body = s[body_k].format(**extra) if extra else s[body_k]
        recs_html += f"""
        <div class="rec">
          <div class="rec-num">{i}</div>
          <div class="rec-body">
            <h4>{s[title_k]}</h4>
            <p>{body}</p>
          </div>
        </div>"""

    obs5 = s["obs5"].format(anjos_a=anjos_a_skus)
    obs4 = s["obs4"].format(pct=LP(ih_pct["total"], 0))

    return f"""<!doctype html>
<html lang="{locale}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{s['doc_title']}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300..900;1,9..144,300..900&family=Instrument+Serif:ital@0;1&family=Instrument+Sans:ital,wght@0,400..700;1,400..700&display=swap">
  <style>{CSS}</style>
</head>
<body>
  <div class="topbar">
    <div class="brand">lully <em>1661</em></div>
    <nav class="langswitch">{lang_switch}</nav>
  </div>

  <section class="hero">
    <div class="shell">
      <div class="eyebrow">{s['report_eyebrow']}</div>
      <h1 class="display">{s['title_pre']} <em>{s['title_em']}</em></h1>
      <p class="lead">{s['stores_lead']}</p>

      <div class="meta-grid">
        <div class="meta-item">
          <span class="meta-label">{s['period_label']}</span>
          <span class="meta-value">{daterange} <em>· {s['period_days'].format(n=n_days)}</em></span>
        </div>
        <div class="meta-item">
          <span class="meta-label">{s['source_label']}</span>
          <span class="meta-value">{s['source_value']}</span>
        </div>
        <div class="meta-item">
          <span class="meta-label">{s['rows_label']}</span>
          <span class="meta-value">{LU(coverage_rows())}</span>
        </div>
        <div class="meta-item">
          <span class="meta-label">{s['coverage_label']}</span>
          <span class="meta-value">{coverage}</span>
        </div>
      </div>
    </div>
  </section>

  <section>
    <div class="shell">
      <div class="eyebrow">{s['kpis_eyebrow']}</div>
      {kpis_html}
    </div>
  </section>

  <section>
    <div class="shell">
      <div class="eyebrow">{s['stores_eyebrow']}</div>
      <h2 class="display">{s['stores_title_pre']} <em>{s['stores_title_em']}</em></h2>
      <p class="lead">{s['stores_lead']}</p>
      <table class="data">
        <thead><tr>
          <th>{s['th_store']}</th>
          <th class="num">{s['th_revenue']}</th>
          <th class="num">{s['th_share']}</th>
          <th class="num">{s['th_rows']}</th>
        </tr></thead>
        <tbody>{stores_rows}</tbody>
      </table>
      <div class="obs">
        <span class="obs-label">{obs_label(locale, 1)}</span>
        {s['obs1']}
      </div>
    </div>
  </section>

  <section>
    <div class="shell">
      <div class="eyebrow">{s['family_eyebrow']}</div>
      <h2 class="display">{s['family_title_pre']} <em>{s['family_title_em']}</em></h2>
      <figure class="chart">
        <img src="01-family-weekly.png" alt="">
      </figure>
      <table class="data">
        <thead><tr>
          <th>{s['th_family']}</th>
          <th class="num">{s['th_revenue_period'].format(n=n_days)}</th>
          <th class="num">{s['th_share']}</th>
          <th class="num">{s['th_units']}</th>
        </tr></thead>
        <tbody>{family_rows}</tbody>
      </table>
      <div class="obs">
        <span class="obs-label">{obs_label(locale, 2)}</span>
        {s['obs2']}
      </div>
    </div>
  </section>

  <section>
    <div class="shell">
      <div class="eyebrow">{s['top_products_eyebrow']}</div>
      <p class="lead">{s['top_products_lead']}</p>
      <figure class="chart">
        <img src="02-top10-products-weekly.png" alt="">
      </figure>
    </div>
  </section>

  <section>
    <div class="shell">
      <div class="eyebrow">{s['brunch_eyebrow']}</div>
      <h2 class="display">{s['brunch_title_pre']} <em>{s['brunch_title_em']}</em></h2>
      <p class="lead">{s['brunch_intro']}</p>
      {brunch_html}
      <div class="obs">
        <span class="obs-label">{obs_label(locale, 3)}</span>
        {s['obs3']}
      </div>
    </div>
  </section>

  <section>
    <div class="shell">
      <div class="eyebrow">{s['anjos_eyebrow']}</div>
      <h2 class="display">{s['anjos_title_pre']} <em>{s['anjos_title_em']}</em></h2>
      <p class="lead">{s['anjos_lead']}</p>
      {anjos_html}
      <figure class="chart">
        <img src="03-loja-family-mix.png" alt="">
        <figcaption>{s['chart_loja_caption']}</figcaption>
      </figure>
      <div class="obs">
        <span class="obs-label">{obs_label(locale, 4)}</span>
        {obs4}
      </div>
    </div>
  </section>

  <section>
    <div class="shell">
      <div class="eyebrow">{s['abc_eyebrow']}</div>
      <h2 class="display">{s['abc_title_pre']} <em>{s['abc_title_em']}</em></h2>
      <p class="lead">{s['abc_lead']}</p>
      <figure class="chart">
        <img src="04-abc-per-loja.png" alt="">
      </figure>
      <table class="data">
        <thead><tr>
          <th>{s['th_store']}</th>
          <th class="num">{s['th_total_skus']}</th>
          <th class="num">{s['th_a_skus']}</th>
          <th class="num">{s['th_pct_skus']}</th>
        </tr></thead>
        <tbody>{abc_rows}</tbody>
      </table>
      <div class="obs">
        <span class="obs-label">{obs_label(locale, 5)}</span>
        {obs5}
      </div>
    </div>
  </section>

  <section>
    <div class="shell">
      <div class="eyebrow">{s['weekend_eyebrow']}</div>
      <h2 class="display">{s['weekend_title_pre']} <em>{s['weekend_title_em']}</em></h2>
      <p class="lead">{s['weekend_lead']}</p>
      <figure class="chart">
        <img src="05-weekday-vs-weekend.png" alt="">
      </figure>
      <table class="data">
        <thead><tr>
          <th>{s['th_family']}</th>
          <th class="num">{s['th_weekday_avg']}</th>
          <th class="num">{s['th_weekend_avg']}</th>
          <th class="num">{s['th_lift']}</th>
        </tr></thead>
        <tbody>{ww_rows}</tbody>
      </table>
      <div class="obs">
        <span class="obs-label">{obs_label(locale, 6)}</span>
        {s['obs6']}
      </div>
    </div>
  </section>

  <section>
    <div class="shell">
      <div class="eyebrow">{s['recs_eyebrow']}</div>
      <h2 class="display">{s['recs_title_pre']} <em>{s['recs_title_em']}</em></h2>
      <p class="lead">{s['recs_lead']}</p>
      <div class="recs">{recs_html}</div>
    </div>
  </section>

  <section class="tight">
    <div class="shell">
      <div class="eyebrow">{s['files_eyebrow']}</div>
      <h3 class="display">{s['files_title']}</h3>
      <p class="lead">{s['files_lead']}</p>
      <ul class="files">
        <li><span class="file-name">01-family-weekly.png</span><span class="file-desc">{s['file_chart_01']}</span></li>
        <li><span class="file-name">02-top10-products-weekly.png</span><span class="file-desc">{s['file_chart_02']}</span></li>
        <li><span class="file-name">03-loja-family-mix.png</span><span class="file-desc">{s['file_chart_03']}</span></li>
        <li><span class="file-name">04-abc-per-loja.png</span><span class="file-desc">{s['file_chart_04']}</span></li>
        <li><span class="file-name">05-weekday-vs-weekend.png</span><span class="file-desc">{s['file_chart_05']}</span></li>
      </ul>
    </div>
  </section>

  <footer class="site">
    <div class="shell">
      <div class="brand">lully <em>1661</em></div>
      <div class="credit">{s['footer_credit']}</div>
      <div class="generated">{s['footer_generated']} {pd.Timestamp.today().strftime('%Y-%m-%d')}</div>
    </div>
  </footer>
</body>
</html>
"""


def obs_label(locale: str, n: int) -> str:
    base = {"en": "Observation", "pt": "Observação", "fr": "Observation"}[locale]
    return f"{base} {n}"


def coverage_rows() -> int:
    return len(df)


# =========================================================================
# 7. Index page (cross-language landing)
# =========================================================================
def render_index() -> str:
    cards = "\n".join(
        f"""
        <a href="report-{lc}.html">
          <div class="lang-code">{STRINGS[lc]['lang_label']}</div>
          <span class="lang-name">{STRINGS[lc]['lang_full']}</span>
          <span class="lang-arrow">→</span>
        </a>"""
        for lc in ("en", "pt", "fr")
    )
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Lully 1661 · Sales report</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300..900;1,9..144,300..900&family=Instrument+Serif:ital@0;1&family=Instrument+Sans:ital,wght@0,400..700;1,400..700&display=swap">
  <style>{CSS}</style>
</head>
<body>
  <div class="topbar">
    <div class="brand">lully <em>1661</em></div>
    <nav class="langswitch"><a class="current">EN · PT · FR</a></nav>
  </div>

  <section class="index-hero">
    <div class="shell">
      <div class="eyebrow">Operations report · Feb–May 2026</div>
      <h1 class="display">Sales analysis, <em>read in your language.</em></h1>
      <p class="lead">An operational read of the ZSBMS sales export — three stores, 196 SKUs, 78 days. Choose a language to open the full report.</p>

      <div class="index-cards">{cards}</div>

      <p class="lead" style="margin-top:32px; font-family: var(--font-accent); font-style: italic;">
        Each version is fully self-contained and prints cleanly. The five charts and the underlying CSV live in the same folder.
      </p>
    </div>
  </section>

  <footer class="site">
    <div class="shell">
      <div class="brand">lully <em>1661</em></div>
      <div class="credit">Lully 1661 · operations report</div>
      <div class="generated">Generated {pd.Timestamp.today().strftime('%Y-%m-%d')}</div>
    </div>
  </footer>
</body>
</html>
"""


# =========================================================================
# 8. Write outputs
# =========================================================================
for locale in ("en", "pt", "fr"):
    path = OUT / f"report-{locale}.html"
    path.write_text(render_report(locale), encoding="utf-8")
    print(f"→ {path.name}")

(OUT / "index.html").write_text(render_index(), encoding="utf-8")
print(f"→ index.html")

# Also dump the structured data so the script is reproducible without
# loading the CSV in downstream tools.
report_data = {
    "generated": pd.Timestamp.today().strftime("%Y-%m-%d"),
    "period": {
        "from": PERIOD_FROM.strftime("%Y-%m-%d"),
        "to": PERIOD_TO.strftime("%Y-%m-%d"),
        "n_days": n_days,
    },
    "totals": {
        "revenue": round(total_revenue, 2),
        "units": total_units,
        "avg_daily": round(avg_daily, 2),
        "avg_ticket": round(avg_ticket, 2),
    },
    "lojas": lojas_data,
    "families": families_data,
    "brunch": brunch_data,
    "anjos_in_house": {**ih, "_pct": ih_pct},
    "abc": abc_data,
    "weekday_weekend": ww_data,
}
(OUT / "report-data.json").write_text(json.dumps(report_data, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"→ report-data.json")
print(f"\nDone. Output in: {OUT}")

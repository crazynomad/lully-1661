# Sales analytics pipeline

End-to-end pipeline for Lully 1661's POS data: extract from Zone Soft BMS, parse, accumulate into a canonical CSV, render brand-styled charts and trilingual HTML reports.

```
ZSBMS Evolução de Vendas        (browser export, HTML-as-Excel)
        │
        ▼  parse-xls.py  (zsbms-extract skill)
chunks/*.csv                    (one CSV per date window)
        │
        ▼  merge-sales-csvs.py
sales-canonical.csv             (deduped, single source of truth)
        │
        ├─▶ analyse-sales.py        →  analysis/*.png + observations.md
        └─▶ build-sales-report.py   →  analysis/report-{en,pt,fr}.html + index.html
```

Everything under `raw-requirements/data/zsbms-extract/` is **gitignored** — the repo is public; client revenue figures stay local.

---

## Prerequisites

- Python 3 with `pandas`, `matplotlib` (system Python on macOS works as-is)
- Chrome with the `claude-in-chrome` MCP extension, for the ZSBMS browser steps
- The `zsbms-extract` skill installed at `~/.claude/skills/zsbms-extract/`
  - Provides `scripts/parse-xls.py` (HTML-as-Excel → CSV)
  - Documents the Angular date-input setter shim
- An active ZSBMS tenant login (Zone Soft BMS, `zsbmsv2.zonesoft.org`)

No `pnpm install` needed — these are standalone Python scripts.

---

## Weekly sync (the 90% case)

Mondays, in this repo, invoke the project-scoped slash command:

```
/sync-sales
```

It drives ZSBMS to pull the last 14 days of sales (overlap window to catch retroactive voids/corrections), merges into `sales-canonical.csv` deduping on `(data, loja_num, codigo)`. Then re-run analytics + reports:

```bash
python3 scripts/analyse-sales.py        # charts + Portuguese memo
python3 scripts/build-sales-report.py   # EN / PT / FR HTML
```

The merge is idempotent — running `/sync-sales` multiple times on the same window is a no-op. Safe.

---

## First-time backfill (already done; here for reference)

The repo's canonical CSV was assembled from five date chunks pulled by hand:

| Chunk | Rows | Notes |
|---|---:|---|
| 2022 (full year) | 0 | POS wasn't on ZSBMS yet |
| 2023 (full year) | 2,855 | Only Beato + Anjos active |
| 2024 (full year) | 24,649 | Ourique came online 2024-06-26 |
| 2025-01-01 → 2025-05-12 | 11,695 | gap filler |
| 2025-05-13 → 2026-05-13 | 43,180 | rolling 12-month |

Then `merge-sales-csvs.py` was run with all five CSVs to produce `sales-canonical.csv` (82,379 rows after dedupe).

To redo or extend the backfill, repeat the `/sync-sales` recipe with custom date ranges and feed the resulting chunks into the merge. The merge accepts any number of inputs.

---

## File layout

```
lully-1661/
├── .claude/commands/sync-sales.md     ← the /sync-sales recipe (tracked)
├── scripts/
│   ├── README.md                       ← this file
│   ├── analyse-sales.py                ← canonical → charts + memo
│   ├── build-sales-report.py           ← canonical → trilingual HTML
│   └── merge-sales-csvs.py             ← N chunks → canonical (dedupes)
└── raw-requirements/data/zsbms-extract/   ← GITIGNORED
    ├── sales-canonical.csv            ← single source of truth
    ├── chunks/                         ← per-window raw CSVs (+ .xls)
    │   ├── 2023.csv / .xls
    │   ├── 2024.csv / .xls
    │   ├── 2025-01-01_to_2025-05-12.csv / .xls
    │   ├── 2025-05-13_to_2026-05-13.csv / .xls
    │   └── sync-YYYY-MM-DD.csv / .xls (weekly pulls)
    └── analysis/                       ← generated outputs
        ├── 01-family-weekly.png … 05-weekday-vs-weekend.png
        ├── observations.md             ← PT-language insights memo
        ├── report-{en,pt,fr}.html      ← trilingual brand report
        ├── index.html                  ← language-picker landing
        └── report-data.json            ← structured numbers
```

---

## Canonical CSV schema

`sales-canonical.csv`, one row per (date × store × SKU):

| column | type | example | notes |
|---|---|---|---|
| `data` | `DD-MM-YYYY` | `15-04-2025` | string, parse with `format="%d-%m-%Y"` |
| `loja_num` | int | `2` | store number in ZSBMS |
| `loja` | string | `Anjos` | mapped via `{1:"Beato", 2:"Anjos", 3:"Ourique"}` |
| `codigo` | int | `10047` | product SKU code |
| `produto` | string | `Focaccia` | product display name |
| `familia` | string | `Pão` | family (left of slash) |
| `sub_familia` | string | `Especiais` | sub-family (right of slash, often empty) |
| `quantidade` | float | `12.0` | units sold |
| `valor_sem_iva` | float | `45.30` | ex-VAT revenue (€) |
| `valor_total` | float | `54.00` | total revenue (€) |

Dedupe key: `(data, loja_num, codigo)`.

---

## Scripts

### `merge-sales-csvs.py`

Concatenates N chunk CSVs, dedupes on `(data, loja_num, codigo)` keeping the LAST occurrence so retroactive corrections override earlier pulls.

```bash
python3 scripts/merge-sales-csvs.py \
    raw-requirements/data/zsbms-extract/sales-canonical.csv \
    raw-requirements/data/zsbms-extract/chunks/sync-2026-05-20.csv \
    --out raw-requirements/data/zsbms-extract/sales-canonical.csv
```

Argument order matters — pass older inputs first, newer last.

### `analyse-sales.py`

Reads canonical → emits five PNGs and a Portuguese `observations.md`. Filters out incomplete trailing weeks so charts don't cliff at the right edge. Brand-styled with the same paper/ink/gold/ember palette as the website.

```bash
python3 scripts/analyse-sales.py
```

No arguments — paths are baked in (canonical CSV input, `analysis/` output).

### `build-sales-report.py`

Reads the same canonical → emits trilingual HTML reports plus an index landing page. Locale-aware money formatting (`€257,166` EN, `€257.166` PT, `257 166 €` FR), Fraunces + Instrument Serif + Instrument Sans typography, observation callouts, ranked recommendations.

```bash
python3 scripts/build-sales-report.py
```

To preview locally:

```bash
cd raw-requirements/data/zsbms-extract/analysis
python3 -m http.server 8765
# open http://127.0.0.1:8765/
```

---

## Gotchas

1. **The .xls is HTML in disguise.** ZSBMS exports `.xls` files that are actually HTML with a Microsoft Excel namespace, ISO-8859-1 encoded. Always go through `parse-xls.py` — never `pd.read_excel` directly.
2. **PT number format.** Comma is the decimal separator (`5,000` = 5 units, not 5000). The parser handles this.
3. **Angular date inputs.** `el.value = '...'` alone won't update the form model. Use the native setter + dispatch `input`/`change`/`blur` events. The `/sync-sales` recipe has the snippet.
4. **chrome-in-claude tab group.** When the MCP opens a new tab, it's in a fresh browser session — you'll need to log in to ZSBMS again. The login form is at `#!/login`.
5. **Public repo.** `raw-requirements/data/` is gitignored to keep revenue figures out of the public tree. Don't move generated artifacts (CSVs, charts, HTMLs, PDFs) outside that directory.
6. **Loja mapping is tenant-specific.** For Lully: `1=Beato, 2=Anjos, 3=Ourique`. Encoded in the slash command and the `/sync-sales` recipe. If another tenant ever reuses this pipeline, update both.

---

## Adding a new report

If the client asks for a new analytical view:

1. Add the computation to `analyse-sales.py` (chart + observation), OR add an HTML section in `build-sales-report.py` with translations for all three languages in the `STRINGS` dict.
2. Re-run the relevant script — outputs land in `analysis/`.
3. The slash command doesn't need touching; it only handles extraction + merge.

---

## Related

- `~/Github/skills/zsbms-extract/SKILL.md` — generic Zone Soft BMS extraction knowledge (Angular date shim, .xls parsing, when to use)
- `.claude/commands/sync-sales.md` — the weekly recipe Claude follows when invoked

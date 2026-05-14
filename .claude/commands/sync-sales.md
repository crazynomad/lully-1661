# /sync-sales — Lully weekly ZSBMS sales sync

Pull the last ~14 days of sales from ZSBMS in **three reports** and merge each into its canonical CSV (all gitignored):

- `raw-requirements/data/zsbms-extract/sales-canonical.csv` — product-line detail (SKU × date × loja)
- `raw-requirements/data/zsbms-extract/tickets-canonical.csv` — daily aggregates incl. ticket count (Trafic)
- `raw-requirements/data/zsbms-extract/payments-canonical.csv` — daily channel split (Dinheiro / Cartão / **Uber Eats** / **Glovo** / **Bolt Food** per loja per day)

Run the three reports in the same browser session. The first two share the same form; the third has its own page and **must be run once per loja** (no "Todas" option).

## When to run
Mondays — picks up any retroactive corrections, voids, or late entries from the previous week. Safe to run multiple times; the merge dedupes by `(data, loja_num, codigo)` so re-syncing the same window is a no-op.

## Recipe — follow exactly

### 1 — Verify ZSBMS is open and logged in
Call `mcp__claude-in-chrome__tabs_context_mcp`. Look for a tab on `zsbmsv2.zonesoft.org`. If missing:
- Ask the user to open `https://zsbmsv2.zonesoft.org/#!/dashboard` in Chrome and log in
- Then re-check tabs_context. The tab must be in the MCP-managed group (creating a new MCP tab works because `navigate` to zonesoft.org is allowed).

### 2 — Determine the sync window
Read the canonical CSV last date (use whichever canonical you have — they should align):
```bash
python3 -c "
import pandas as pd
df = pd.read_csv('raw-requirements/data/zsbms-extract/sales-canonical.csv')
print(pd.to_datetime(df['data'], format='%d-%m-%Y').max().strftime('%d-%m-%Y'))"
```
That's `LAST_DATE`. Sync window = (`LAST_DATE` - 14 days) → today, in `DD-MM-YYYY` format.

### 3 — Open the FIRST report (product-line) and set the window
Navigate (via `javascript_tool` setting `location.hash`) to `#!/rpt-vv-evolucao-produto`.

Set the date inputs using the native value-setter shim (required for Angular):
```js
const setter = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value').set;
const dispatch = el => ['input','change','blur'].forEach(t => el.dispatchEvent(new Event(t,{bubbles:true})));
const dataI = Array.from(document.querySelectorAll('input')).find(i => i.getAttribute('ng-model') === 'model.dataI');
const dataF = Array.from(document.querySelectorAll('input')).find(i => i.getAttribute('ng-model') === 'model.dataF');
setter.call(dataI, '<WINDOW_START_DD-MM-YYYY>'); dispatch(dataI);
setter.call(dataF, '<WINDOW_END_DD-MM-YYYY>');   dispatch(dataF);
// Ensure all 3 lojas are checked
[1,2,3].forEach(n => { const cb = document.getElementById(`cbStore${n}`); if (cb && !cb.checked) cb.click(); });
```

### 4 — Trigger the report and grab the .xls URL
```js
Array.from(document.querySelectorAll('button')).find(b => b.innerText?.trim() === 'Pré-visualizar')?.click();
```
Wait 15–30 s (the modal opens with a preview). Then read the .xls URL out of the DOM — ZSBMS pre-generates all three formats and stashes them in `href`/`src`/iframe attributes:
```js
Array.from(document.querySelectorAll('*'))
  .map(el => [el.getAttribute('href'), el.getAttribute('src'), el.getAttribute('data-url')])
  .flat()
  .filter(u => u && /\.xls$/.test(u))
```

### 5 — Download and parse
```bash
mkdir -p raw-requirements/data/zsbms-extract/chunks
curl -s -o raw-requirements/data/zsbms-extract/chunks/sync-<TODAY>.xls '<XLS_URL>'
python3 ~/Github/skills/zsbms-extract/scripts/parse-xls.py \
    raw-requirements/data/zsbms-extract/chunks/sync-<TODAY>.xls \
    --lojas '{"1":"Beato","2":"Anjos","3":"Ourique"}' \
    --out raw-requirements/data/zsbms-extract/chunks/sync-<TODAY>.csv
```

### 6 — Merge into canonical (dedupes automatically)
```bash
python3 scripts/merge-sales-csvs.py \
    raw-requirements/data/zsbms-extract/sales-canonical.csv \
    raw-requirements/data/zsbms-extract/chunks/sync-<TODAY>.csv \
    --out raw-requirements/data/zsbms-extract/sales-canonical.csv
```
**Order matters**: pass the canonical FIRST and the new chunk LAST — the merge keeps the later occurrence on conflict, so retroactive corrections from the new pull override the stale canonical row.

### 7 — Pull the SECOND report (daily aggregates with ticket count)
Same form, different route. Navigate to `#!/rpt-vv-evolucao`, repeat steps 3–6 with:

- Same date window
- Same loja checkboxes
- After Pré-visualizar opens the modal, grab the .xls URL the same way
- Download to `raw-requirements/data/zsbms-extract/chunks-tickets/sync-<TODAY>.xls`
- Parse with the **tickets parser**:
  ```bash
  python3 ~/Github/skills/zsbms-extract/scripts/parse-data-hora-xls.py \
      raw-requirements/data/zsbms-extract/chunks-tickets/sync-<TODAY>.xls \
      --lojas '{"1":"Beato","2":"Anjos","3":"Ourique"}' \
      --out raw-requirements/data/zsbms-extract/chunks-tickets/sync-<TODAY>.csv
  ```
- Merge into the tickets canonical:
  ```bash
  python3 scripts/merge-tickets-csvs.py \
      raw-requirements/data/zsbms-extract/tickets-canonical.csv \
      raw-requirements/data/zsbms-extract/chunks-tickets/sync-<TODAY>.csv \
      --out raw-requirements/data/zsbms-extract/tickets-canonical.csv
  ```

### 8 — Pull the THIRD report (payments by channel)
Navigate to `#!/rpt-ve-tipospagamento`. Two filters to set per run:

- **Loja**: this dropdown has no "Todas" — you must run the report **three times**, once for each loja (Beato / Anjos / Ourique).
- **Mode tab**: click **"Informação Diária"** (not "Valores Acumulados") so you get daily rows instead of a period summary.

Date inputs use the same `model.dataI` / `model.dataF` ng-models as the other reports. Click `Pré-visualizar`, grab the .xls URL the usual way:

```js
Array.from(document.querySelectorAll('*'))
  .map(el => [el.getAttribute('href'), el.getAttribute('src'), el.getAttribute('data-url')])
  .flat()
  .filter(u => u && /\.xls$/.test(u))
```

Download to `raw-requirements/data/zsbms-extract/chunks-payments/sync-<TODAY>-<loja>.xls` (one file per loja), then parse with the payments parser:

```bash
python3 ~/Github/skills/zsbms-extract/scripts/parse-payments-xls.py \
    raw-requirements/data/zsbms-extract/chunks-payments/sync-<TODAY>-<loja>.xls \
    --lojas '{"1":"Beato","2":"Anjos","3":"Ourique"}' \
    --out raw-requirements/data/zsbms-extract/chunks-payments/sync-<TODAY>-<loja>.csv
```

After all three lojas, merge into the channel canonical:

```bash
python3 scripts/merge-payments-csvs.py \
    raw-requirements/data/zsbms-extract/payments-canonical.csv \
    raw-requirements/data/zsbms-extract/chunks-payments/sync-<TODAY>-*.csv \
    --out raw-requirements/data/zsbms-extract/payments-canonical.csv
```

### 9 — Report
Tell the user:
- Old canonical date range vs new
- New rows added
- Total revenue / row count after merge
- Flag any anomalies: missing days, negative revenue, family taxonomy drift

## Gotchas — read if something looks off
- The "preset range" dropdown (`Hoje` / `Este Mês` etc.) is just a quick-fill — manually-set `model.dataI`/`model.dataF` win.
- The .xls is HTML-disguised-as-Excel, ISO-8859-1 encoded. `parse-xls.py` handles this — don't try to open it with pandas directly.
- Token URLs (`/rpt/<token>/*.xls`) are session-bound. Don't reuse old ones.
- Loja mapping for Lully: `1=Beato, 2=Anjos, 3=Ourique`. Hardcoded in this recipe; for other tenants use a different mapping.

## Related
- `~/Github/skills/zsbms-extract/SKILL.md` — generic ZSBMS extraction knowledge
- `scripts/merge-sales-csvs.py` — dedupe + merge logic
- `scripts/analyse-sales.py` / `scripts/build-sales-report.py` — re-run analytics on the updated canonical

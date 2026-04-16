# Platform Recommendation — lully 1661 Website

**Status:** Draft v0.1 — internal
**Prepared:** 2026-04-16
**Context:** Client deferred Q3 to us ("open to alternatives"). This document is our recommendation, to present alongside sitemap v1.

## Recommendation (TL;DR)

> **Shopify storefront, with a premium customizable theme, Shopify Markets for PT + EN, and Stripe for Multibanco + credit cards.** Plan a Phase 2 upgrade path to Hydrogen (Shopify's headless front-end) if editorial ambition grows after launch.

Why this, in one paragraph: the client wants to launch **ASAP**, already runs three operating stores with staff-managed inventory, supplies copy and photography themselves, and has no formal brand guidelines beyond illustrations. Shopify collapses everything we need into one platform — multi-language, Multibanco, POS integration, order management, tax rules for Portugal, delivery/marketplace integrations for Phase 2 — and lets us concentrate our effort on visual craft (theme, typography, the Baroque-illustration motif) rather than rebuilding commerce primitives. The two French bakery reference sites the client admires (`liberte-paris.com`, `thefrenchbastards.fr`) run on Shopify-class stacks, which is direct evidence the aesthetic ceiling is high enough.

## Options considered

| # | Stack | Time to launch | Cost shape | Design ceiling | Fit for lully 1661 |
|---|-------|----------------|-----------|----------------|-------------------|
| **A ✅** | **Shopify + premium theme (e.g. Impulse, Pipeline, or a custom Dawn fork)** | 4–6 weeks | Monthly subscription + one-off theme dev + ~2% gateway fees | High — 90% of what a headless stack offers with a skilled designer + developer | **Best overall fit** |
| B | Shopify Hydrogen (headless) with Next/Remix | 10–14 weeks | 2–3× of A in dev, same subscription | Ceiling-free | Overkill for phase 1; sensible phase 2 evolution |
| C | WordPress + WooCommerce | 6–8 weeks | Hosting + WooCommerce + Multibanco plugin licenses | Medium–High | Weaker POS / multi-store inventory, plugin-dependent Multibanco |
| D | Headless commerce (Medusa / Saleor) + Next.js | 14–20 weeks | 3–5× of A | Ceiling-free | Mismatched with timeline and copy-supplied-by-client reality |
| E | Squarespace / Webflow + external commerce | 4 weeks | Flat SaaS | Medium (template-bound) | Weak PT commerce integration; no native Multibanco |

## Why Shopify specifically

### What matches the brief

| Requirement | Shopify answer |
|-------------|----------------|
| PT + EN, PT default, `/pt/` and `/en/` subpaths | Shopify Markets gives native multi-market routing with subpath URLs; translation via Translate & Adapt (free) or Weglot |
| Multibanco (mandatory) | Stripe is certified for Multibanco in PT and integrates natively with Shopify Payments; no custom plugin |
| Credit cards | Shopify Payments or Stripe, same checkout |
| Click & collect, staff-reconciled inventory | "Local pickup" is a built-in fulfillment method; Shopify POS on an iPad lets staff reconcile inventory in-store daily without a custom admin |
| 3 stores already operating | Shopify Locations (multi-location inventory) — store-locator app (e.g. Store Locator Plus) for the frontend |
| Copy + images supplied by client | Native CMS fields + Metafields for editorial page blocks; no separate CMS |
| Phase 2 delivery (Uber Eats, Glovo) | Both have direct Shopify connectors |
| Phase 2 "our own payment system" | Custom payment app route exists when/if needed |
| Website live ASAP | Largest saved-time factor — we skip commerce scaffolding entirely |

### Where Shopify will push back (and our mitigations)

| Friction | Mitigation |
|----------|-----------|
| Themes have a common anatomy — we don't want a "generic Shopify site" | Start from a highly customizable theme (Dawn or Impulse), build 3–4 bespoke sections for Home / Shop / Festive & Bespoke in Liquid; invest design hours here rather than in commerce |
| Shopify checkout is hard to deeply customize (pre-Checkout Extensibility) | Use Checkout Extensibility (2024+) for branded-but-standard checkout; avoid custom checkout pages |
| Editorial / long-form content patterns (journal, story pages) | Use Online Store 2.0 flexible sections + Metaobjects for History / Festive / B2B pages — works well for our scope |
| Locking us into Shopify long-term | Hydrogen is the documented escape hatch: same back-end, new front-end. No migration if we ever go headless |

## Phase 1 (launch) vs Phase 2

### Phase 1 — launch scope

- Shopify plan: **Shopify** ($79/mo tier — enables Shopify Markets and standard reports). Keep Shopify Plus as a phase-3 option.
- Payments: **Stripe** (Multibanco + Visa / Mastercard). Shopify Payments is an alternative if the client prefers single-provider consolidation.
- Languages: PT + EN via Shopify Markets; PT as primary market, EN as secondary.
- Fulfillment: Local pickup from 3 Lisbon stores, **staff-reconciled inventory** (no sync with external POS yet unless the client already runs Shopify POS — to confirm in F3 follow-up).
- Reservations: The Fork embed on a Reservations page (public widget from The Fork's business tools); email-contact fallback section below.
- B2B "Lully Inside": a static editorial page + Shopify form.
- Careers: static page + form that emails HR inbox.
- Content: Home, History, Shop, Festive & Bespoke Orders, Reservations, Lully Inside (B2B), Stores, Careers, Legal.
- Design: custom theme work — ~3 bespoke Home sections, custom product card, custom collection page header, store-locator page.
- Analytics: GA4 + Shopify native analytics. No ad pixels at launch (add when marketing picks up).

### Phase 2 — post-launch (2–6 months after)

- Third-party delivery: Uber Eats and Glovo connectors (both direct Shopify apps). This does **not** require replatforming.
- Integrated payments: either expand Stripe with saved payment methods + subscriptions (for loyalty), or introduce the client's "own payment system" as a Shopify Custom Payment App.
- Loyalty / gift cards (likely a holiday-2026 priority — gift cards are a Shopify native feature).
- Editorial "Journal" / recipe content if content volume grows.
- Optional Hydrogen migration if the team decides the Liquid ceiling is blocking design ambition.

## Timeline — hard deadline 2026-05-15 (brunch menu launch + media event)

**Client confirmed (F2):** the website must be live before the May-15 brunch-menu launch event (media + influencers). Today is 2026-04-16 → **29 days**. This collapses the earlier 4–6 week plan into a fixed 4-week sprint and forces a scope split.

### Scope split for the deadline

| | **v1.0 — live on 2026-05-15** | **v1.1 — 10–14 days after launch** |
|---|---|---|
| Home | ✅ Full design | — |
| About / History | ✅ | — |
| Brunch / menu | ✅ **Priority for event** — readable catalogue with PT + EN, prices, allergens, per-store availability | — |
| Shop — Breads / Pastries / Desserts / Snacks / Drinks | ✅ Readable product pages (browsable catalogue) | — |
| **Cart + checkout + pickup slot selector** | ⚠️ Target for v1.0 if QA allows; fallback to v1.1 | ✅ If pushed, ship as a low-risk add-on with Multibanco + cards |
| Stores (3 locations locator) | ✅ | — |
| Reservations (The Fork embed) | ✅ where The Fork is live; email fallback on the rest | — |
| Festive & Bespoke Orders | ✅ (static + enquiry form) | — |
| Lully Inside (B2B) | ✅ (descriptive-only, partners TBA) | — |
| Careers | ✅ | — |
| Legal / Contact | ✅ | — |
| Analytics + UTM for event traffic | ✅ | — |

Why this split is safe: the event's purpose is to **drive brunch + press coverage**, not to drive e-commerce revenue on day 1. A readable menu + reservations + store locator covers 100% of the event narrative. Click-&-collect adds real commercial value but is not on the event's critical path, and the downside of shipping it broken on Day 1 is much worse than shipping it 10 days later.

### 4-week sprint calendar

| Week | Dates | Milestones |
|------|-------|-----------|
| 1 | 2026-04-16 → 2026-04-22 | Shopify + Markets + Stripe provisioning · Theme base selected · Brand kit (colors / type / vectorized sub-marks) · IA locked · Domain + DNS pointed · Content ingest begins (client brunch copy + product photos) |
| 2 | 2026-04-23 → 2026-04-29 | Home + About + Brunch sections designed and built · Product data model + Shopify collections · Store locator data in from client · The Fork embed(s) verified |
| 3 | 2026-04-30 → 2026-05-06 | Shop collection + product templates · Festive & Bespoke · Lully Inside · Careers · Legal · Full PT translation pass · Cart/checkout spike (for decision on v1.0 vs v1.1) |
| 4 | 2026-05-07 → 2026-05-13 | QA, accessibility pass, Lighthouse pass, multibanco sandbox, analytics wiring, staging freeze **2026-05-13** |
|  | 2026-05-14 | Client sign-off + DNS cutover |
|  | **2026-05-15** | **Go-live + brunch-menu event** |
| +1 | 2026-05-16 → 2026-05-29 | **v1.1** — ship cart + pickup flow if it didn't make v1.0. Post-event content refresh (press coverage, event photos). |

### Risks against the deadline

| Risk | Mitigation |
|------|-----------|
| Client content slips (copy or photos for brunch items) | Hard content deadline **2026-05-01** (end of Week 2). Anything not in by then uses placeholders and updates post-launch. |
| Vectorizing 3 Baroque sub-marks takes longer than expected | Parallel track in Week 1 — either vectorize manually or commission a designer up-front. High-res raster is an acceptable fallback for hero use with careful masking. |
| The Fork integration not live on all 3 stores | Email-fallback block ships for stores without the widget; swap in the widget post-launch per store. |
| Cart/checkout QA incomplete by 2026-05-13 | Ship v1.0 without cart; ship v1.1 on ~2026-05-25 with cart. Event narrative is unaffected. |
| Translation quality (PT) | Use native Portuguese translator on the team for the hero and legal copy; machine translation for shop/product copy as first pass, native reviewer on week 3. |

### Gating content deliveries (client-owned)

| Due date | Deliverable | Owner |
|----------|-------------|-------|
| 2026-04-23 | Final logo pack decision (keep raster sub-marks or commission vector) | Us → client |
| 2026-04-29 | Brunch copy (PT + EN), brunch product photography, 3 store photos | Client |
| 2026-05-01 | All remaining copy (PT + EN), all product photography | Client |
| 2026-05-06 | Legal text (T&Cs, privacy, cookies, complaints book link) | Client / their counsel |
| 2026-05-13 | Client sign-off on staging | Client |

## Estimated cost shape (rough, for internal discussion)

- **Shopify subscription**: ~€79/mo (Shopify plan) + any app subscriptions (The Fork embed free; Weglot €15–49/mo if we don't use Shopify's free Translate & Adapt).
- **Gateway fees**: Stripe Multibanco ~1.5% per transaction (Portugal rate); card rates standard (1.4% + €0.25 EEA).
- **One-time design + build**: quoted separately by our team — main variable is how many bespoke sections we hand-build vs reuse theme defaults.

## Open decisions that would change this

| If client… | …then reconsider |
|-----------|-----------------|
| Already operates Shopify POS in the 3 stores | Tightest fit — no replatform. Verify in F3 follow-up. |
| Already has a different POS (e.g., Lightspeed, SumUp, Square) | Confirm integration — Shopify has connectors for all three, but inventory sync quality varies |
| Moves timeline to 3–4 months | Option B (Hydrogen) becomes plausible |
| Says budget cap makes A infeasible | Option E + a separate commerce widget is the cheap fallback, but we will lose Multibanco native support |
| Decides B2B needs wholesale-ordering portal after all | Shopify B2B (on Shopify Plus) — changes plan tier and adds 2–4 weeks |

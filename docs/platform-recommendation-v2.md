# Platform Recommendation v2 — lully 1661 Website

**Status:** Draft v0.1 — internal
**Prepared:** 2026-05-09
**Supersedes:** [`platform-recommendation.md`](./platform-recommendation.md) for v1 (the v1 doc remains authoritative for Phase-2 commerce trade-offs; do not delete).
**Context:** Client confirmed direction shift on 2026-05-09 — drop e-commerce from v1, prioritize SEO and local marketing, require modular extensibility so features can be added separately later, and need a light CMS so the owner can update weekly products without dev involvement. Original brunch-event deadline (2026-05-15) pushed to TBD; new launch date to be agreed during the v2 sprint plan.

## Recommendation (TL;DR)

> **Next.js 15 (App Router) + Keystatic CMS + Tailwind CSS, deployed on Vercel.** Brochure-first IA with editorial menu, per-store local-SEO pages, and a journal as the content engine. Commerce is out for v1; the documented phase-2 path is **Shopify Storefront API behind the same Next.js front-end** (or Stripe checkout if the client prefers full ownership).

Why this, in one paragraph: the brief inverted on 2026-05-09 — without commerce, Shopify's largest strengths (Multibanco-ready checkout, multi-store inventory, POS integration) are moot for v1, while its weaknesses (Liquid theme ceiling, limited Lighthouse headroom, awkward editorial-page flexibility) become the dominant concern now that **SEO + local marketing is the v1 success metric**. Next.js with static rendering gives us static-quality Core Web Vitals, full control over JSON-LD and per-store URLs (the highest-ROI lever for a multi-location Lisbon bakery), and a feature-folder architecture into which phase-2 commerce drops in cleanly. **Keystatic** covers the "owner updates weekly menu without dev help" requirement with content-in-repo (MD/MDX/YAML in `content/`), a modern admin UI that runs as a Next.js route at `/keystatic`, $0/mo cost, and TypeScript-first schema definition — at the cost of a slower publish flow (git commit → Vercel build, 1–3 min) compared to a hosted-API CMS like Sanity. The trade-off was accepted on 2026-05-09 in favor of full content ownership and zero CMS bills.

## What changed since v1

| Axis | v1 brief (2026-04-16) | v2 brief (2026-05-09) | Effect on stack |
|---|---|---|---|
| Commerce | Click & collect, Multibanco, Stripe in v1 | Deferred to Phase 2 | Removes Shopify's biggest reason to exist for v1 |
| Success metric | "Live before brunch event" | "SEO + local marketing through the website" | Static rendering, schema markup, per-store URLs become first-class concerns |
| Extensibility | Theme customization within Shopify | Modular — add features (commerce, loyalty, ordering) separately later | Feature-folder Next.js codebase; isolated phase-2 modules |
| Content updates | Shopify metaobjects + native CMS | "Light CMS" for weekly product updates | Keystatic (decided 2026-05-09 over Sanity / TinaCMS / Payload / Decap) — see § CMS choice |
| Deadline | 2026-05-15 (hard) | TBD (relaxed) | Time to do the build properly — no compromise on architectural week-1 decisions |

## Options considered (v2)

| # | Stack | Time to v1 | Cost shape | SEO ceiling | Modularity | Fit |
|---|-------|-----------|-----------|-------------|------------|-----|
| **A ✅** | **Next.js 15 + Keystatic + Tailwind on Vercel** | 5–7 weeks | Vercel free/Pro + Keystatic Cloud free | Excellent (full SSG, schema control) | Excellent (feature folders, isolated phase-2 add-ons) | **Best fit for v2 brief** |
| B | Next.js + Sanity + Tailwind on Vercel | 5–7 weeks | Vercel + Sanity free tier | Excellent | Excellent | Strong alternative — sub-second publish via webhook revalidate, best-in-class image CDN, but content lives in vendor cloud and editor introduces a second SaaS to manage. Picked over A only if instant publish or side-by-side bilingual editing become hard requirements. |
| C | Next.js + TinaCMS | 5–7 weeks | TinaCloud free for 2 users / 250MB media; $29/mo above | Excellent | Excellent | Better visual MDX editor than Keystatic, weaker for highly structured content; 250MB media cap is a real constraint for bakery photography |
| D | Next.js + Decap CMS (git-based) | 4–5 weeks | Free | Excellent | Good | Cheapest; editor UX is the weakest; project health is shaky in 2026 — Keystatic dominates it on every axis |
| E | Next.js + Payload CMS (self-hosted) | 6–8 weeks | Hosting bill + Postgres | Excellent | Excellent | Good if client demands no SaaS at all; more infra to babysit than Keystatic |
| F | Astro + Keystatic | 4–5 weeks | Same as A | Excellent | Lower (no React-app upgrade path; phase-2 commerce is harder) | Tempting for pure brochure, but blocks phase-2 cleanly |
| G | WordPress (block editor) | 4 weeks | Hosting + plugins | Medium-High | Low — modular features mean plugins, which mean drift | Mature but the wrong shape for "add features as separate modules" |
| H | Shopify (the v1 recommendation) | 4 weeks | $79/mo + theme dev | Medium | Low for non-commerce features | **Now phase-2-only** — see v1 doc § Phase 2 |

## Why Next.js specifically

### What matches the v2 brief

| Requirement | Next.js answer |
|-------------|----------------|
| SEO + local marketing as v1 metric | App Router metadata API for per-page tags, `generateMetadata` for hreflang alternates, `app/sitemap.ts` + `app/robots.ts` for crawl control, full JSON-LD authoring (no theme abstraction in the way) |
| PT + EN, PT default, `/pt/` and `/en/` subpaths | `next-intl` middleware handles locale-prefixed routing exactly per `sitemap-v1.md` |
| Modular extensibility — add features separately later | Feature-folder layout (`features/menu/`, `features/stores/`, `features/festive-orders/`) keeps phase-2 modules drop-in; commerce returns as `features/checkout/` |
| Light CMS, owner updates weekly | Keystatic admin embedded at `/keystatic`, owner edits → commit to repo → Vercel auto-deploys (1–3 min) |
| Per-store URLs with proper schema | Trivial — three static routes `/lojas/anjos`, `/lojas/campo-de-ourique`, `/lojas/beato`, each with its own `LocalBusiness`/`Bakery` JSON-LD |
| Core Web Vitals headroom | Static rendering by default + `next/image` with built-time optimization → LCP < 2.5s achievable on mobile 4G |
| Phase-2 commerce path | Shopify Storefront API (headless) drops behind the same front-end — same back-office story as v1 doc's Phase 2; or Stripe checkout if client wants no Shopify at all |

### Where Next.js will push back (and our mitigations)

| Friction | Mitigation |
|----------|-----------|
| More moving parts than a managed platform (build tooling, CMS plumbing, image config, deploy config) | Lock conventions in week 1: feature folders, Keystatic schema, image policy, Biome, typed Reader API. Document in `docs/architecture.md`. |
| App Router has rough edges (caching semantics, server components mental model) | Stay on the well-trodden path: static generation for content, server actions only for forms, no streaming/PPR experiments in v1 |
| Keystatic publish latency (git commit → Vercel build, 1–3 min) | Communicate clearly to client: "your edits go live in under 3 minutes, not instantly." If sub-second publish becomes a hard requirement later, the migration to Sanity is contained to `lib/keystatic/` and `data.ts` files (architecture is CMS-agnostic by design). |
| Photography volume could exceed in-repo storage practicality | Image optimization budget enforced in CI; if content volume grows beyond ~500 images, route through Cloudinary as a separate media host (Keystatic supports external image fields) |
| Form handling without Shopify (was free with Shopify) | Server actions → Resend (transactional email) for festive-orders, careers, B2B enquiries. Single vendor, $0 free tier covers v1 volume. |

## Frontend stack — concrete choices

This section is the contract between us and ourselves for week-1 setup. Each row is a *decision*, not a suggestion.

| Layer | Pick | Why |
|---|---|---|
| **Runtime / framework** | Next.js 15.x, **App Router**, TypeScript strict mode | Native to the SSG + ISR + per-page metadata story. Pages Router is legacy. |
| **Node version** | Node 20 LTS (Vercel default) | Matches Vercel runtime; no surprises in CI |
| **Package manager** | `pnpm` | Fast, disk-efficient, deterministic; the de facto Next default in 2026 |
| **Language** | TypeScript, `strict: true`, `noUncheckedIndexedAccess: true` | Catches the array-access bugs that bite editorial CMS code |
| **Styling** | **Tailwind CSS v4** + a small `theme.css` token layer (Lully Baroque palette, type scale) | No CSS-in-JS runtime; tokens live in one file; designers can tweak without touching components |
| **UI primitives** | Hand-rolled + `@radix-ui/react-*` for a11y-critical primitives (dialog, dropdown, tooltip) | Avoid full component libraries (shadcn/ui is fine if we want it as a *starting point*, but treat as templates, not a dependency) |
| **Typography** | Self-hosted webfonts via `next/font/local`, picked to honor the Baroque + contemporary motif (likely a serif display + a clean sans body, exact pairing in design pass) | Self-hosted = zero CLS, no third-party request, no GDPR cookie banner dance for fonts |
| **Icons** | `lucide-react` | Tree-shakeable, consistent stroke weight, free |
| **Internationalization** | `next-intl` v3+ with subpath routing `/pt`, `/en`; PT as `defaultLocale` | Matches `sitemap-v1.md` URL structure 1:1; built-in support for App Router and `generateMetadata` hreflang |
| **CMS** | **Keystatic** — `@keystatic/core` + `@keystatic/next`, admin route at `/keystatic`, content stored in `content/` directory as MD/MDX/YAML | See § CMS choice below for the full rationale |
| **CMS schema** | TypeScript schema in `keystatic.config.ts`, typed reads via `createReader` from `@keystatic/core/reader` | Schema and reads are type-safe end-to-end without a code-gen step |
| **CMS auth** | Keystatic Cloud (free) — handles owner login (Google/email), GitHub App writes to repo on save | Owner doesn't need a GitHub account; we don't host auth infrastructure |
| **Image handling** | `next/image` + repo-hosted images in `content/<collection>/<slug>/images/`, optimized at build by Next.js. If volume grows, route through Cloudinary via Keystatic's URL-based image fields | Build-time optimization is sufficient for v1 volume; Cloudinary is a drop-in escape hatch |
| **Forms** | React Server Actions (App Router native) for submit handlers; `react-hook-form` + `zod` for client-side validation | No separate API route layer; zod schema is shared client + server |
| **Form delivery** | **Resend** for transactional email (`@resend/node`) | $0 free tier covers Lully v1 volume; one-line API; audit log in dashboard |
| **Maps** | Google Maps Embed API (iframe) on per-store pages; static map images for the homepage teaser | No JS library cost on the page; Embed API is free and key-restricted; static map for the home avoids ever loading the maps SDK on the most-visited route |
| **Reservations** | The Fork widget embed on `/reservas` (Anjos only); email fallback in v1.0 (per `sitemap-v1.md:91-95`) | Unchanged from v1 plan |
| **Search** | Deferred to v1.1. When added: **Pagefind** (static, builds at deploy) covers all content (journal + menu) since everything is static at build time | Pagefind is free, fully static, and indexes at build — no ongoing infra |
| **Newsletter** | **Mailchimp** or **Buttondown** signup, server action posts to provider API | Mailchimp if the client already uses it; Buttondown is the lighter-weight pick if not |
| **Analytics** | **Vercel Web Analytics** + **GA4** (server-side via Measurement Protocol where possible) + **Plausible** as a privacy-friendly fallback if client prefers no GA | GA4 is the SEO-attribution standard; Plausible avoids the cookie banner |
| **Cookie consent** | **CookieYes** (free tier) or hand-rolled with `react-cookie-consent`, PT-localized banner | PT requires explicit consent before any non-essential cookie. Mandatory. |
| **Structured data** | Hand-authored JSON-LD per route via `<Script type="application/ld+json">` in metadata; one helper per type (`localBusinessJsonLd`, `menuItemJsonLd`, `articleJsonLd`, `breadcrumbJsonLd`) | Generic schema libraries are heavier than the 30 lines of helpers we'd write |
| **Linting / formatting** | **Biome** (ESLint + Prettier replacement) | One tool, faster, simpler config; if the team prefers ESLint+Prettier, that's fine — pick one and lock it |
| **Testing** | **Vitest** for unit + component tests; **Playwright** for one happy-path E2E (homepage → store page → reservations) | Don't over-invest in v1 — the editorial pages are visually QA'd, not unit-tested |
| **Hosting** | **Vercel** Pro (~$20/mo) | Native ISR, preview URLs per PR, image optimization, Web Analytics included; matches Next.js defaults |
| **CDN / DNS** | Vercel handles CDN; DNS at registrar (Cloudflare DNS optional for advanced rules) | Keep simple |
| **CI** | GitHub Actions: typecheck, lint, build, Lighthouse CI on the homepage and one per-store page | Lighthouse CI is the gate that protects the SEO investment from regressions |
| **Error tracking** | **Sentry** free tier | Catches form-submit errors and CMS-data-shape regressions in production |

### Architectural conventions (the expensive-to-change-later set)

- **Feature-folder layout** — group by domain, not type:
  ```
  app/
    [locale]/
      page.tsx            # Home
      sobre/page.tsx
      menu/page.tsx
      menu/[category]/page.tsx
      lojas/page.tsx
      lojas/[slug]/page.tsx
      diário/page.tsx
      diário/[slug]/page.tsx
      ...
    keystatic/[[...rest]]/page.tsx  # Embedded Keystatic admin
  features/
    menu/                 # CMS reads, types, components specific to menu
    stores/               # store schema, JSON-LD helpers, store card components
    journal/
    festive-orders/
    reservations/
    careers/
    b2b/
  components/             # Cross-feature primitives only (Button, Container, Section)
  content/                # Keystatic content storage (MD/MDX/YAML, git-tracked)
  lib/                    # Cross-cutting utilities (cn, fonts, keystatic reader)
  keystatic.config.ts     # CMS schema (TypeScript)
  ```
- **Keystatic config lives in `keystatic.config.ts`** at the repo root; content lives in `content/` as MD/MDX/YAML files, fully git-tracked. Admin runs at `/keystatic` (embedded) with Keystatic Cloud auth for the owner.
- **Bilingual content modeled as a `fields.object({ pt, en })` shape** on every user-facing field. The Studio shows PT and EN stacked in a single panel per field. One place to add a third language later if the brand expands beyond Lisbon.
- **All routes are statically generated.** Server components fetch from Keystatic's Reader API at build time. Content updates happen via git commit → Vercel auto-deploy. No `revalidateTag` plumbing needed (content is static at build).
- **JSON-LD is not optional.** Every page type has a JSON-LD helper colocated with its feature folder. CI fails if a page route exists without a JSON-LD test.

### Specific package list (for the package.json)

```
next                        ^15
react / react-dom           ^19
typescript                  ^5
@types/node @types/react    latest
tailwindcss                 ^4
next-intl                   ^3
@keystatic/core             latest
@keystatic/next             latest
react-hook-form             latest
zod                         latest
resend                      latest
@radix-ui/react-dialog      latest
@radix-ui/react-dropdown-menu latest
lucide-react                latest
@vercel/analytics           latest
@sentry/nextjs              latest
biome                       latest (devDep)
vitest                      latest (devDep)
@playwright/test            latest (devDep)
```

## CMS choice — Keystatic, picked over Sanity on 2026-05-09

Five options were on the table. Keystatic was picked on 2026-05-09 over Sanity (which had been the v2-doc-draft pick the day before) after the trade-offs were re-examined.

| Axis | **Keystatic ✅** | Sanity | TinaCMS | Decap CMS | Payload CMS 3 |
|---|---|---|---|---|---|
| Editor UX for non-technical owner | Modern React admin, runs as a Next.js route | Excellent — best-in-class side-by-side bilingual fields | Visual MDX editor (best for long-form) | Weak — form-only, dated UI | Excellent — modern admin |
| Where content lives | Repo (MD/MDX/YAML in `content/`) | Sanity Cloud | Repo (MDX) + TinaCloud editor | Repo (MD) | Postgres / MongoDB self-host |
| Vendor / ownership | None (admin can self-host or use free Keystatic Cloud auth) | Vendor cloud (exportable) | TinaCloud editor required for production | None | None (self-host) |
| Bilingual pattern | `fields.object({ pt, en })` — stacked in editor | Side-by-side custom `localizedString` (best UX) | Suffix fields or per-locale files | Per-locale folders/files | Per-block locale field |
| Publish latency | Git commit → Vercel build (1–3 min) | Webhook → revalidateTag (sub-second) | Same as Keystatic | Same | Programmable; instant via Payload hooks |
| Image pipeline | Repo-hosted at build, optional Cloudinary escape | Best-in-class on-the-fly CDN | TinaCloud media (250MB free, then paid) | Repo-hosted, manual | Custom |
| Free tier headroom for Lully | Unlimited (admin auth via Keystatic Cloud free tier or self-hosted GitHub App) | 3 users, 10k docs, 500k API/mo | 2 users, 250MB media (tight for bakery photo) | Unlimited | N/A |
| Project health (2026) | Active (Thinkmill — KeystoneJS team) | Active | Active | Slowing — community-maintained | Active |
| Cost recurring | $0 | $0 (likely) | $0–29/mo | $0 | Self-host hosting bill |

**Pick:** **Keystatic**. Decided on the strength of (1) content-in-repo with full git history per change, (2) zero recurring CMS bill, (3) admin lives as a Next.js route (no second app to deploy), (4) modern editor UX that won't feel dated to the owner, and (5) a healthy maintainer in 2026. Sanity is a superior CMS in absolute terms — its publish-latency, image CDN, and bilingual editor UX are best-in-class — but its strengths weren't worth the trade-off of a second SaaS, vendor-held content, and an editor running outside our Next.js app for *this* project's content cadence (1–2 owner edits per week).

### Trade-offs accepted by picking Keystatic

| Axis | Cost of choosing Keystatic over Sanity |
|---|---|
| Publish-to-live latency | Git commit + Vercel build instead of webhook revalidate. Owner waits 1–3 min instead of seconds for changes to be live. |
| Bilingual editor UX | PT and EN fields are stacked in a single panel, not side-by-side. Workable; less elegant. |
| Image CDN | No on-the-fly transforms. Lighthouse image budget enforced manually via build-time `next/image` + per-page transfer caps. Cloudinary is the documented escape hatch if photo volume grows. |
| Reference resolution | Keystatic relationship reads are slightly more verbose than Sanity's `availableAt[]->` GROQ pattern. |

### Door left open

Keystatic config and content are entirely in our repo — schema is TypeScript, content is plain MD/MDX/YAML, the Reader API is a thin abstraction. If publish-latency becomes a hard requirement later (e.g., during a holiday campaign with daily updates), the migration to Sanity is contained to:
- Replace `keystatic.config.ts` with `sanity/schemas/`
- Replace `lib/keystatic/reader.ts` with `lib/sanity/client.ts`
- Replace `data.ts` reads in each feature folder
- Add the `/api/revalidate` route + Sanity webhook

Roughly a week of work, no layout/page rewrites. The architecture's CMS-agnostic feature-folder design protects this.

## Keystatic content model — sketch

Collections and singletons to design in week 1 (final fields confirmed during the content pass). All defined in `keystatic.config.ts`:

| Name | Kind | Purpose |
|---|---|---|
| `homepage` | singleton | Hero copy, "this week" featured items references, footer slots |
| `aboutPage` | singleton | History narrative, philosophy blocks, optional team |
| `weeklyMenuItem` | collection | Owner-edited weekly products. Fields: name (PT/EN), description (PT/EN), allergens, image, category (relationship), availableAt (relationship[]), weekOf date, featured boolean |
| `product` | collection | Permanent catalogue items — same shape as weekly without `weekOf` |
| `productCategory` | collection | Breads / Pastries / Desserts / Snacks / Brunch / Drinks |
| `store` | collection | One per outlet. Fields: name, slug, neighborhood, address, geo (lat/long), hours (array per weekday), phone, photo, atmosphere (PT/EN), services[], theForkUrl |
| `journalPost` | collection | Editorial content. Fields: title (PT/EN), slug (PT/EN), heroImage, body (MDX, PT/EN), publishedAt, author, tags[] |
| `partner` | collection | B2B logos. Fields: name, logo, sector, testimonial (PT/EN) |
| `openPosition` | collection | Careers listings. Fields: title, department, store (relationship), description, applyEmail, validThrough |
| `seasonalCampaign` | collection | Festive & Bespoke seasonal offer. Fields: name, season, heroImage, description, products (relationship[]), leadTime, enquiryEnabled |
| `legalPage` | collection (slug-keyed) | Terms, privacy, cookies, complaints book |

**Storage layout:**
```
content/
  homepage.yaml
  aboutPage.yaml
  weeklyMenuItem/
    2026-W19-pao-rustico/
      index.yaml
      image.jpg
    ...
  store/
    anjos.yaml
    campo-de-ourique.yaml
    beato.yaml
  journalPost/
    2026-05-15-brunch-launch/
      index.mdx
      hero.jpg
  ...
```

**Bilingual pattern:** every user-facing string field uses `fields.object({ pt: fields.text({...}), en: fields.text({...}) })`. For MDX bodies, two parallel `fields.document(...)` instances. The Keystatic admin shows PT and EN stacked vertically per field — workable; the architecture doc § 4.1 will document the field shape.

**Publish flow:** owner edits at `/keystatic` → Keystatic Cloud commits to GitHub → Vercel auto-deploys (1–3 min) → page is live. No webhook revalidation, no `revalidateTag` plumbing — Vercel's git integration is the entire pipeline.

## Phase 1 (v1) vs Phase 2

### Phase 1 — v1 launch scope (deadline TBD)

- All channels per `sitemap-v2.md` (forthcoming) — `/`, `/sobre`, `/menu` (+ category pages), `/diário`, `/encomendas`, `/reservas`, `/lojas` (+ 3 per-store pages), `/lully-inside`, `/trabalha-connosco`, `/legal`
- Editorial menu (no cart)
- Per-store local-SEO pages with full schema
- Journal — start with 3–4 seed posts, target 1/week thereafter
- The Fork embed on Reservations (Anjos), email fallback per v1 doc
- Festive & Bespoke enquiry form → Resend → bakery sales inbox
- Careers form → Resend → HR inbox
- B2B Lully Inside enquiry form → Resend → sales inbox
- Newsletter signup (Mailchimp or Buttondown)
- Cookie consent (PT-localized)
- Analytics: GA4 + Vercel Web Analytics
- Keystatic admin at `/keystatic` for the owner

### Phase 2 — when commerce returns

- **Path A (recommended):** Shopify Storefront API behind the same Next.js front-end. We model `cart`, `checkout`, `customer` as `features/checkout/` and call Shopify's GraphQL Storefront API server-side. Multibanco + Stripe via Shopify Payments. *No replatform.* This is the same back-office promise that the v1 platform doc made for Hydrogen — we just keep our Next.js front-end.
- **Path B:** Stripe Checkout direct (no Shopify). Cheaper per transaction, but we own inventory, order management, refunds, fulfillment. Recommended only if the client genuinely wants no Shopify dependency.
- Loyalty / gift cards: Shopify-native if Path A; custom Stripe if Path B.
- POS sync to bakery's existing POS: connector-dependent, same as v1 doc § Phase 2.
- Editorial Journal expansion if traffic demands it.

The **trade-off table in v1 doc § Options considered** remains the reference for the Path A vs Path B vs other-headless-commerce decision when commerce returns.

## Estimated cost shape (rough, for internal discussion)

- **Vercel Pro:** ~$20/mo (covers preview URLs, analytics — Hobby is fine for staging-only)
- **Keystatic Cloud:** $0/mo (free tier covers small teams; admin auth + GitHub App for repo writes)
- **Resend:** $0 (3k emails/mo free); $20/mo if volume grows
- **Sentry:** $0 free tier; ~$26/mo if usage grows
- **Domain:** existing
- **Mailchimp / Buttondown:** $0 free tier
- **One-time design + build:** quoted separately

Total recurring v1: **~$20/mo**, vs. Shopify's $79/mo plus app fees. Lower because we removed both the commerce engine *and* the hosted CMS.

## Timeline shape

Now that the deadline relaxed, the recommended sprint shape:

| Week | Milestones |
|------|-----------|
| 1 | Repo scaffold (Next.js + Tailwind + next-intl + Keystatic + biome + CI) · Keystatic schema drafted in `keystatic.config.ts` · Architecture doc · Brand tokens (colors, fonts, sub-marks vectorized) · Per-store data ingest from client |
| 2 | Home + About + Stores hub + per-store pages · LocalBusiness JSON-LD verified in Google Rich Results Test · Keystatic admin live at `/keystatic` · Owner training session 1 (data entry) |
| 3 | Menu hub + category pages + product pages · MenuItem JSON-LD · Brunch section · Festive & Bespoke + enquiry form (Resend integration) |
| 4 | Reservations (The Fork + email fallback) · Lully Inside · Careers · Journal scaffold + 3 seed posts · Newsletter integration |
| 5 | Legal pages · Cookie consent · Analytics · Sentry · Lighthouse CI gates · accessibility pass · PT translation review |
| 6 | QA, performance budget verification, owner training session 2 (publishing weekly menus, journal posts), staging freeze, client sign-off |
| Launch | Go-live + Google Business Profile sync + sitemap submission to Search Console |

Calendar dates pending the new launch date confirmation.

## Risks & mitigations

| Risk | Mitigation |
|------|-----------|
| Owner finds Keystatic admin harder than expected | Two training sessions; record loom walkthroughs; lock the schema to the simplest editor experience (no deeply nested arrays); embed inline help text via `description` on every field |
| Photography volume creates Core Web Vitals regressions | Image budget per page (e.g. ≤ 600KB total transfer on mobile); Lighthouse CI gate on PRs; Cloudinary as documented escape hatch if `content/`-hosted images push repo size past ~1GB |
| Vercel build queue grows with content edit frequency | Each Keystatic save triggers a build; if frequency outpaces build minutes, switch to "draft" mode and batch publishes, or migrate to Sanity (architecture preserved) |
| Phase-2 commerce decision drifts indefinitely | Document the Path A vs Path B decision in v1 doc trade-off table; revisit at +3 months post-launch |
| PT translation quality | Native PT reviewer on team for hero, legal, and store-page copy; machine translation as first pass for the journal only |
| Client wants commerce sooner than Phase 2 plan | Path A (Shopify Storefront API) is a 2–3-week add-on, not a replatform — no week-1 architectural decision blocks it |

## Open decisions that would change this

| If client… | …then reconsider |
|-----------|-----------------|
| Wants commerce in v1 after all | Drop back to v1 platform recommendation (Shopify) — re-platforming Next.js to add commerce inside the original timeline costs more than starting on Shopify |
| Wants sub-second publish flow (e.g. live updates during a holiday campaign) | Migrate Keystatic → Sanity (~1 week of CMS-layer rewrites; pages, JSON-LD, routing, forms unchanged) |
| Wants fully self-hosted admin (no Keystatic Cloud) | Run Keystatic with a self-hosted GitHub App (~2 days extra setup); or migrate to Payload CMS 3 (+1 week) |
| Already has a Mailchimp/Klaviyo account | Use it; otherwise default to Buttondown |
| Wants a multi-language site beyond PT/EN later | The `fields.object({ pt, en, ... })` schema pattern handles new locales; routing additions are mechanical in `next-intl` |
| Decides "demo sites" means a reusable agency template | Re-evaluate against Option A — most decisions hold, but `features/` would be designed as cross-instance modules with externalized brand tokens; ~1.5× the upfront work |

## Next deliverables

1. `docs/sitemap-v2.md` — revised IA reflecting `/menu`, `/diário`, and per-store URLs ✅ (existing — Keystatic terminology pass needed)
2. `docs/architecture.md` — feature-folder conventions, Keystatic schema sketch, JSON-LD policy ✅ (existing — Keystatic rewrite needed)
3. Repo scaffold PR — Next.js + Tailwind + next-intl + Keystatic + biome + CI in a single mergeable starting point

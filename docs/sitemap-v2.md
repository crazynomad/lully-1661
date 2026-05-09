# Sitemap v2 — lully 1661 Website

**Status:** Draft v0.1 — internal
**Prepared:** 2026-05-09
**Supersedes:** [`sitemap-v1.md`](./sitemap-v1.md) for v1 launch (v1 retained for the original commerce-led IA that returns in Phase 2)
**Based on:** `platform-recommendation-v2.md` (Next.js + Keystatic, brochure-first, SEO-led)

> **What changed since v1.** Three structural shifts driven by the 2026-05-09 brief change:
> 1. **`/loja` → `/menu`** — pure editorial catalogue, no cart, schema.org `MenuItem` per product.
> 2. **New `/diário`** (Journal) — SEO content engine; without commerce, content carries the organic-traffic weight.
> 3. **`/lojas` splits into a hub + 3 per-store URLs** — `/lojas/anjos`, `/lojas/campo-de-ourique`, `/lojas/beato`, each with its own `LocalBusiness`/`Bakery` JSON-LD. This is the single highest-ROI local-SEO move.
>
> All other pages keep their v1 structure. The cart drawer, pickup-time selector, and Shopify-specific patterns are removed. Phase-2 commerce is documented in `platform-recommendation-v2.md` § Phase 2.

## Top-level structure

```
/ (Home, PT default — redirect / → /pt)
├─ /pt/sobre                  ├─ /en/about                About / History
├─ /pt/menu                   ├─ /en/menu                 Menu (editorial, no cart)
│   ├─ /pt/menu/paes          │   ├─ /en/menu/breads
│   ├─ /pt/menu/pastelaria    │   ├─ /en/menu/pastries
│   ├─ /pt/menu/sobremesas    │   ├─ /en/menu/desserts
│   ├─ /pt/menu/snacks        │   ├─ /en/menu/snacks
│   ├─ /pt/menu/brunch        │   ├─ /en/menu/brunch        ★ event priority
│   └─ /pt/menu/bebidas       │   └─ /en/menu/drinks
├─ /pt/diário                 ├─ /en/journal              Journal — NEW (SEO engine)
│   └─ /pt/diário/[slug]      │   └─ /en/journal/[slug]
├─ /pt/encomendas             ├─ /en/festive-orders       Festive & Bespoke Orders
├─ /pt/reservas               ├─ /en/reservations         Reservations (Anjos only)
├─ /pt/lully-inside           ├─ /en/lully-inside         B2B
├─ /pt/lojas                  ├─ /en/stores               Stores hub
│   ├─ /pt/lojas/anjos        │   ├─ /en/stores/anjos        ★ own JSON-LD
│   ├─ /pt/lojas/campo-de-…   │   ├─ /en/stores/campo-de-…   ★ own JSON-LD
│   └─ /pt/lojas/beato        │   └─ /en/stores/beato        ★ own JSON-LD
├─ /pt/trabalha-connosco      ├─ /en/careers              Careers
└─ /pt/legal                  └─ /en/legal                Legal / Contact
```

PT slugs are indicative — final wording confirmed in the content pass. EN slugs follow conventional bakery English.

> **Note on `/diário`** — Portuguese accents in URLs are valid (UTF-8, RFC 3986 §2) and Google indexes them, but some sharing surfaces percent-encode them awkwardly. If the client wants to play it safe, fall back to `/pt/jornal` or `/pt/blog`. Confirm in the content pass.

## Per-page brief

### Home — `/` (redirects to `/pt/`)

**Purpose:** first impression; route visitors to the brunch story / menu / stores; establish the Baroque-contemporary tone.

**Blocks, top to bottom:**
1. **Hero** — brand wordmark, seasonal copy line (e.g. the agreed motto), large composition built from the Meunier / Pâtissière / Caffetier illustrations.
2. **Three pillars** — cards for Breads / Pastries / Drinks-&-Brunch (per Q13), each with its Baroque sub-mark. Each links to the matching `/menu/*` category.
3. **This week at lully** — rotating featured items / weekly menu highlights. **Keystatic-driven** (`weeklyMenuItem` entries flagged `featured: true`); rebuilt on next deploy when the owner publishes (~1–3 min after save).
4. **Stores teaser** — minimalist block: 3 locations with neighborhood names, a static map thumbnail, "Visit us" CTA to `/lojas`.
5. **Journal teaser** — single card pulling the latest journal post.
6. **Newsletter signup** — single field; Mailchimp / Buttondown integration.
7. **Footer** — social, hours summary, legal.

**JSON-LD:** `Organization` (Lully 1661 with logo, sameAs links to Instagram / GBPs).

**Phase:** 1.

### About / History — `/sobre` / `/about`

**Purpose:** brand story; the "Renaissance of bakery" narrative.

**Blocks:**
1. **Editorial opening** — adapted from `brief-brand-introduction-2022.docx`, focused on Jean-Baptiste Lully + 1661 + tradition-and-reinvention.
2. **Product philosophy** — organic flours, 48h fermentation, stone-milled wheat from Mâconnais, the oven at the heart of the boutique.
3. **Team / people** — portrait shots + short bios (if client supplies; otherwise skip).
4. **CTAs** — "Explore the Menu" + "Visit a store".

**JSON-LD:** `AboutPage` + breadcrumb.

**Phase:** 1. Content-dependent on client supplying team photos.

### Menu — `/menu` / `/menu`

**Purpose:** editorial catalogue. Browsable, no cart, no pickup. Each item is a *content* page that earns SEO and informs visitors before they walk into a store.

**Top of page (`/menu`):** category tiles (Breads / Pastries / Desserts / Snacks / Brunch / Drinks) with Baroque illustrations.

**Category page (e.g. `/menu/paes`):** grid of products with filters (gluten-free, organic, vegan), per-store availability badges. Filters are URL-state so each filtered view is shareable and indexable.

**Product page (e.g. `/menu/paes/[slug]`):**
- Product photo (repo-hosted, optimized at build by `next/image`)
- Description (PT + EN)
- Ingredients
- Allergens
- Weight / size
- Available at: which of the 3 stores
- "Pairs well with" cross-sell (3 products)
- CTA: "Visit a store" or "Order for an event" (links `/lojas` and `/encomendas` respectively)

**JSON-LD:** `MenuItem` per product page (with `name`, `description`, `nutrition`, `suitableForDiet` where applicable, image), `BreadcrumbList`. The category pages get `CollectionPage` + breadcrumb.

**No cart, no Add-to-bag.** Phase 2 introduces commerce; the page shape is designed so adding "Add to pickup order" is a single component drop-in without disturbing the existing layout.

**Phase:** 1. **Content-dependent** on client photography + copy for products.

### Menu › Brunch — `/menu/brunch` / `/menu/brunch`

**Purpose:** event-priority section. **Anjos-only, dine-in-only** (per `requirements-understanding.md` M2).

**Blocks:**
1. **Hero** — brunch photography + dine-in framing.
2. **Anjos-only callout** — "Brunch is served at our Anjos location" with link to `/lojas/anjos`.
3. **Brunch menu** — readable catalogue (dishes, prices, allergens), grouped by course or by hour-of-day.
4. **Reserve a table CTA** — link to `/reservas`.
5. **Press / event mentions** — once the May launch event covers, this becomes a press strip.

**JSON-LD:** `Menu` (schema.org) referencing the parent `Restaurant` (Anjos store) + `MenuItem` for each dish.

**Phase:** 1.

### Journal (Diário) — `/diário` / `/journal`

**Purpose:** **NEW in v2.** Without commerce, content is the SEO engine. Targets local + topical organic queries ("padaria Anjos Lisboa," "sourdough Lisbon," "best pastéis de nata," "what is 48h fermentation").

**Index page (`/diário`):**
- Latest 12 posts as cards (image, title, excerpt, date, tags)
- Tag filter (URL-state)
- Pagination

**Post page (`/diário/[slug]`):**
- Hero image
- Title (large display)
- Date + reading time + author
- Body (Keystatic MDX — bilingual via parallel PT and EN document fields)
- Related posts (3, by tag)
- Newsletter signup at the bottom

**Seed posts (3–4 at launch, then 1/week target):**
1. "The 48-hour sourdough — why we wait" (technique story; SEO target: "sourdough fermentation Lisbon")
2. "Jean-Baptiste Lully and the year 1661" (brand story; SEO target: brand-name searches)
3. "Pastéis de nata: a Lully take on a Lisbon classic" (local SEO; target: "best pastéis de nata Lisboa")
4. (Post-launch) Recap of the brunch-menu launch event

**JSON-LD:** `Article` (or `BlogPosting`) per post with `headline`, `image`, `datePublished`, `author`, `publisher` (Lully), `mainEntityOfPage`. Index page gets `Blog` + `BreadcrumbList`.

**Phase:** 1 (scaffold + 3–4 seed posts at launch). Editorial cadence post-launch is the client's commitment.

### Festive & Bespoke Orders — `/encomendas` / `/festive-orders`

**Purpose:** per Q15 — showcase **festive products** (seasonal cakes, holiday boxes, gift hampers) *and* **events** (catering, guest-chef luncheons, private tastings).

**Blocks:**
1. **Editorial intro** — "for the moments that matter" positioning.
2. **Seasonal catalogue** — current festive offer (Easter, summer, back-to-school, autumn, Christmas) — Keystatic `seasonalCampaign` entries, swappable by the client.
3. **Events we organize** — gallery of past events (e.g. Gareth × Sezin luncheon).
4. **Events we supply** — "Catering & bespoke" section, with lead-time expectations and minimum-order notes.
5. **Enquiry form** — captures event type / date / guest count / budget range / contact → routes to bakery sales inbox via Resend.

**JSON-LD:** `Service` (catering/bespoke service) + `Event` for each past event in the gallery (with `startDate`, `location`, `image`).

**Phase:** 1.

### Reservations — `/reservas` / `/reservations`

**Purpose:** book a table at **Anjos only** (M2, M4 — only outlet with dine-in + brunch).

**Blocks:**
1. **Brief intro** — Anjos address, hours, "how to book".
2. **Reservation form** — email-fallback in v1.0 (The Fork not live for Anjos yet per M4). Server action → Resend → reservations inbox. Once The Fork is live, swap-in is a one-section replacement.
3. **Groups / private events** — bridges to `/encomendas`.

**JSON-LD:** `Reservation` is for confirmed bookings; the page itself is `WebPage` + breadcrumb.

**Phase:** 1 — ships with email-only fallback. Widget swap-in is v1.1+ when client provides The Fork confirmation link.

### Lully Inside (B2B) — `/lully-inside`

**Purpose:** per Q7 — text + partner showcase + enquiry form.

**Blocks:**
1. **How we work together** — partnership models pitch (co-branded bakery corners inside hotels, restaurant supply, private-label products).
2. **Partners featured** — logos + 2-line testimonials from `partner` entries in Keystatic. *Pending: which partners to feature at launch.*
3. **Enquiry form** — volume, delivery frequency, product categories, contact → sales inbox via Resend.

**JSON-LD:** `Service` + breadcrumb.

**Phase:** 1 — even without featured partners, descriptive content is useful.

### Stores hub — `/lojas` / `/stores`

**Purpose:** entry point for the 3 Lisbon outlets. **The hub does not replace per-store pages — it routes to them.**

**Blocks:**
1. **Map** — three pins, hover/click → store card preview.
2. **Three store cards** — neighborhood, address, hours summary, dominant photo, "View this store" CTA → individual store page.
3. **Quick comparison** — small table: which store has dine-in, which has the visible oven, which is open Sundays, etc. Helps visitors pick.

**JSON-LD:** `ItemList` referencing the 3 store pages.

**Phase:** 1.

### Per-store pages — `/lojas/anjos`, `/lojas/campo-de-ourique`, `/lojas/beato`

**NEW in v2.** Each store gets its own URL, its own `LocalBusiness` + `Bakery` JSON-LD with unique `@id`, `address`, `geo`, `openingHoursSpecification`. This is the structural change that lets Google rank the bakery for "padaria + neighborhood" queries.

**Per-store blocks (template):**
1. **Hero** — store photography (interior or exterior), store name, neighborhood.
2. **Address + map** — full address, embedded Google Maps (Embed API, not the heavy JS SDK), "Get directions" CTA.
3. **Opening hours** — per-weekday table (with `openingHours` microdata).
4. **Services at this store** — chips: dine-in / brunch / pickup / oven-visible / parking / wheelchair access. Drawn from Keystatic `store.services` array.
5. **Atmosphere** — short editorial paragraph (PT/EN), what makes this store distinct (Anjos has the dine-in restaurant; Beato has the visible oven; Campo de Ourique is the neighborhood favorite).
6. **What's available here** — featured products available at this store (filtered Keystatic Reader query on `weeklyMenuItem.availableAt`).
7. **Reservations CTA** (Anjos only) — links `/reservas`.
8. **The Fork link** — once configured per store.
9. **Phone + contact** — click-to-call on mobile.
10. **Reviews / press strip** — Google reviews embed (optional v1.1) or hand-picked press quotes.

**JSON-LD per store:**
```jsonc
{
  "@context": "https://schema.org",
  "@type": ["Bakery", "LocalBusiness"],
  "@id": "https://lully1661.com/pt/lojas/anjos#store",
  "name": "Lully 1661 — Anjos",
  "address": { "@type": "PostalAddress", "...": "..." },
  "geo": { "@type": "GeoCoordinates", "latitude": "...", "longitude": "..." },
  "openingHoursSpecification": [...],
  "servesCuisine": ["French", "Bakery"],
  "priceRange": "€€",
  "telephone": "...",
  "image": "...",
  "url": "https://lully1661.com/pt/lojas/anjos",
  "sameAs": ["https://www.google.com/maps/place/..."]
}
```
Each store's `@id` is unique. NAP (name/address/phone) consistency between this JSON-LD, the Google Business Profile for that store, and the visible page text is **mandatory** — mismatch is the most common local-SEO regression.

**Phase:** 1 (Anjos + Campo de Ourique + Beato all ship together).

### Careers — `/trabalha-connosco` / `/careers`

**Purpose:** per Q8 — email-based applications.

**Blocks:**
1. **Why lully** — short manifesto block.
2. **Open positions** — list (Keystatic `openPosition` entries — owner edits freely).
3. **How to apply** — single form (name, position, CV upload, cover letter) → HR inbox via Resend (with attachment forwarding).

**JSON-LD:** `JobPosting` per open position (with `title`, `hiringOrganization`, `jobLocation` referencing the relevant store, `datePosted`, `validThrough`, `employmentType`).

**Phase:** 1.

### Legal / Contact — `/legal`

**Purpose:** terms, privacy, cookie policy, contact details, **Livro de Reclamações** (Portuguese complaints book — required for Portuguese retail).

**Blocks:**
1. **Terms of service**
2. **Privacy policy** (GDPR + LGPD-style data-subject rights)
3. **Cookie policy** (linked to the cookie consent banner)
4. **Contact** — general inbox + per-store phone + addresses
5. **Livro de Reclamações** — link to the official electronic complaints book

**JSON-LD:** `WebPage` + `Organization` contact info.

**Phase:** 1. Legal text supplied by client / their counsel.

## Global / system pages

- **404** — branded, links back to Home and Menu and the most recent journal post.
- **Search results** — *deferred to v1.1.* When added: Pagefind (static, builds at deploy) covers both journal and menu (all content is static at build time, indexable by Pagefind).
- **Newsletter signup** — single field in footer; Mailchimp or Buttondown.
- **Cookie banner** — PT-localized, tiered consent (necessary / preferences / analytics / marketing). PT requires explicit consent before any non-essential cookie.
- **`sitemap.xml`** — generated by Next.js `app/sitemap.ts` from all routes (including dynamic Keystatic-sourced product/journal/store pages).
- **`robots.txt`** — generated by `app/robots.ts`. Disallow `/keystatic` (CMS admin) and `/api/*` (server actions).

## Navigation & interaction patterns

- **Primary nav (desktop):** Home · Menu · Diário · Encomendas · Lojas · Reservas · Sobre. (Lully Inside, Careers, Legal in footer.)
- **Mobile nav:** hamburger → same items, plus direct CTAs for "Reservar" (book a table at Anjos) and "Visitar uma loja".
- **Language switcher:** top-right corner, shows `PT / EN`. Switching preserves the current path (e.g. `/pt/menu/paes` ↔ `/en/menu/breads`).
- **Cart:** removed (no commerce in v1). Phase-2 commerce reintroduces a cart drawer.
- **Sticky CTA on mobile** when scrolling past Home hero: **"Reservar mesa"** (was "Order for pickup" in v1).
- **Per-store pages have a sticky "Get directions" CTA on mobile** — this is the highest-intent action for someone reading a store page on a phone.

## SEO infrastructure (page-level checklist)

Every route must have:
- `<title>` and `<meta name="description">` via `generateMetadata`
- `<link rel="alternate" hreflang>` for PT ↔ EN counterparts (and `x-default`)
- Open Graph image + Twitter card
- Canonical URL
- JSON-LD appropriate to the page type (table above)
- Breadcrumb JSON-LD on all non-Home pages
- `next/image` for all images with explicit width/height (zero CLS)

CI gate: a Lighthouse SEO score < 95 fails the PR. A Rich Results Test failure on store pages fails the PR.

## Round-2 carryover

Round-2 client answers from `sitemap-v1.md` § Round-2 updates remain valid for v2:
- 3 store addresses confirmed (Anjos flagship, Campo de Ourique, Beato)
- Pickup cutoff (F3) is moot for v1 (no commerce); preserved for Phase 2
- Festive & Bespoke Orders merge confirmed (F4)
- No vector sub-marks available (F5) — design task: vectorize manually or commission
- Press & social: Instagram `@lully1661_lisboa`; press list curated internally
- B2B Lully Inside launches descriptive-only

## What's blocked / pending per page

| Page | Status | Pending input |
|------|--------|---------------|
| Home | 🟢 Can design now | Hero copy, "this week" first batch (client) |
| Menu hub + categories | 🟢 Buildable | Product copy + photography (client) |
| Menu — Brunch | 🟢 Anjos-only, dine-in-only | Brunch copy + photos (client) |
| Diário | 🟢 Scaffold + 3–4 seed posts | Editorial direction + author (us drafting, client approving) |
| Stores hub | 🟢 | Map pin colors + atmosphere copy (client) |
| `/lojas/anjos` | 🟢 | Photos + atmosphere copy + The Fork URL (client, when live) |
| `/lojas/campo-de-ourique` | 🟢 | Photos + atmosphere copy (client) |
| `/lojas/beato` | 🟢 | Photos + atmosphere copy + Tue–Sat hours confirmed (client) |
| Reservations | 🟢 Email fallback ships | Reservations inbox address |
| Festive & Bespoke | 🟢 Structure locked | Client copy + seasonal photos |
| Lully Inside | 🟢 Descriptive ships | Partner logos "later" |
| Careers | 🟢 | List of open positions |
| Legal | 🟢 Template ready | Client / counsel for final text |

## What is *not* in v2 (deferred to v1.1 or Phase 2)

- **Cart, checkout, pickup-time selector** — Phase 2 (Shopify Storefront API or Stripe).
- **Site-wide search** — v1.1 (Pagefind).
- **The Fork live widget on Anjos** — v1.1 (when client confirms).
- **Google Reviews embed on store pages** — v1.1 (low priority; the GBP itself is the primary review surface).
- **Loyalty / gift cards** — Phase 2.
- **Third-party delivery (Uber Eats, Glovo)** — Phase 2.

See `platform-recommendation-v2.md` § Phase 2 for the commerce-return plan.

## Next step

Move to `docs/architecture.md` — codebase conventions (feature folders, Keystatic schema, JSON-LD policy, image policy, form-handling pattern). Then the repo-scaffold PR.

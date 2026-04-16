# Sitemap v1 — lully 1661 Website

**Status:** Draft v0.1 — internal
**Prepared:** 2026-04-16
**Based on:** `brief-website.docx` information tree + Round 1 client answers + platform-recommendation.md

## Top-level structure

```
/ (Home, PT default)
├─ /pt/sobre                  ├─ /en/about               About / History
├─ /pt/loja                   ├─ /en/shop                Shop (commerce)
│    ├─ /pt/loja/paes         │    ├─ /en/shop/breads
│    ├─ /pt/loja/pastelaria   │    ├─ /en/shop/pastries
│    ├─ /pt/loja/sobremesas   │    ├─ /en/shop/desserts
│    ├─ /pt/loja/snacks       │    ├─ /en/shop/snacks
│    ├─ /pt/loja/brunch       │    ├─ /en/shop/brunch
│    └─ /pt/loja/bebidas      │    └─ /en/shop/drinks
├─ /pt/encomendas             ├─ /en/festive-orders       Festive & Bespoke Orders
├─ /pt/reservas               ├─ /en/reservations         Reservations (The Fork)
├─ /pt/lully-inside           ├─ /en/lully-inside         B2B
├─ /pt/lojas                  ├─ /en/stores               Store locator (3 Lisbon outlets)
├─ /pt/trabalha-connosco      ├─ /en/careers              Careers
└─ /pt/legal                  └─ /en/legal                Legal / Contact
```

PT URL slugs are indicative — final wording to be confirmed with the client during content pass.

## Per-page brief

### Home — `/` (redirects to `/pt/`)

**Purpose:** first impression; route visitors to Shop or to the narrative (History / Festive). Establishes the Baroque-contemporary tone on first scroll.

**Blocks, top to bottom:**
1. **Hero** — brand wordmark, seasonal line of copy (e.g. "Maintenant, toujours mieux qu'avant" or the agreed English motto), large composition built from the Meunier / Pâtissière / Caffetier illustrations in the Gareth × Sezin flyer style.
2. **Three pillars** — cards for Breads / Pastries / Drinks-&-Brunch (conventional labels per Q13), each with its Baroque sub-mark as the decorative anchor. Each links to the matching Shop collection.
3. **This week at lully** — rotating featured products / weekly menu highlights (content editable via Shopify metaobjects — maps nicely to the existing "Weekly Menu" PDF).
4. **Stores teaser** — minimalist block: 3 locations, a map thumbnail, "Visit us" CTA to `/lojas`.
5. **Journal / Festive promo** — single card pulling the latest Festive & Bespoke promo or event.
6. **Footer** — newsletter signup, social, hours, legal.

**Phase:** 1.

### About / History — `/sobre` / `/about`

**Purpose:** brand story; the "Renaissance of bakery" narrative.

**Blocks:**
1. **Editorial opening** — the brand story (adapted from `brief-brand-introduction-2022.docx`), focused on Jean-Baptiste Lully + 1661 + commitment to tradition-and-reinvention.
2. **Product philosophy** — organic flours, 48h fermentation, stone-milled wheat from Mâconnais, the oven at the heart of the boutique.
3. **Team / people** — portrait shots + short bios (if client supplies; otherwise skip).
4. **CTAs** — "Explore the Shop" + "Visit a store".

**Phase:** 1. Content-dependent on client supplying team photos.

### Shop — `/loja` / `/shop`

**Purpose:** commercial core. Browsable menu + click & collect.

**Top of page:** category tiles (Breads / Pastries / Desserts / Snacks / Brunch / Drinks) with Baroque illustrations.

**Collection page (e.g. `/loja/paes`):** grid of products, filters (e.g. contains-gluten, organic, vegan), pickup-store selector.

**Product page:** product photo, ingredient list, allergens, weight/size, "add to pickup order", cross-sell module (e.g. "pairs well with").

**Cart / Checkout:** Shopify's standard checkout, branded. Pickup-time selector (tied to F3 cutoff when confirmed).

**Phase:** 1. **Blocked on F3** (pickup cutoff time) before we can finalize pickup-time selector UX.

### Festive & Bespoke Orders — `/encomendas` / `/festive-orders`

**Purpose:** per Q15 client clarification — showcase **festive products** (seasonal cakes, holiday boxes, gift hampers) *and* **events** (catering, guest-chef luncheons, private tastings).

**Blocks:**
1. **Editorial intro** — "for the moments that matter" positioning.
2. **Seasonal catalogue** — current festive offer (Easter, summer, back-to-school, autumn, Christmas) — Shopify Metaobjects per season, swappable by the client.
3. **Events we organize** — gallery of past events (e.g. Gareth × Sezin luncheon), with optional Eventbrite/ticketing links.
4. **Events we supply** — "Catering & bespoke" section, with lead-time expectations and minimum-order notes.
5. **Enquiry form** — captures event type / date / guest count / budget range / contact → routes to the right inbox.

**Phase:** 1 for the page itself; 1.5 for live ticketing if needed.

**Pending:** F4 — client to confirm this merges with old "Special Orders" node (our recommendation).

### Reservations — `/reservas` / `/reservations`

**Purpose:** restaurant reservations across the 3 stores (if more than one has a dine-in restaurant — to clarify).

**Blocks:**
1. **Brief intro** — hours, "how to book".
2. **The Fork widget** — their embeddable reservation widget, one per store.
3. **Fallback** — "No availability via The Fork? Write to reservations@…"

**Phase:** 1. Blocked on The Fork account setup — confirm client has the partnership live, otherwise we launch with email-only and swap in the widget later.

### Lully Inside (B2B) — `/lully-inside`

**Purpose:** per Q7 — text + partner showcase + enquiry form.

**Blocks:**
1. **How we work together** — short pitch on partnership models (e.g. co-branded bakery corners inside hotels, restaurant supply, private-label products).
2. **Partners featured** — logos + 2-line testimonials. *Pending F7: which partners to feature at launch.*
3. **Enquiry form** — volume, delivery frequency, product categories, contact → sales inbox.

**Phase:** 1 — even if we launch without featured partners, the page is still useful with descriptive content.

### Stores — `/lojas` / `/stores`

**Purpose:** store locator for the 3 Lisbon outlets. **New section prompted by Q11 answer.**

**Blocks:**
1. **Map** — one pin per store.
2. **Store cards** — per store: address, neighborhood, opening hours (Tue–Sun per client), phone, Google-Maps link, "order for pickup from this store" CTA.
3. **A note per store** — short atmosphere description (which one has the dine-in restaurant, the oven visible, etc.).

**Phase:** 1. **Blocked on F1** (addresses + hours + per-store differentiation).

### Careers — `/trabalha-connosco` / `/careers`

**Purpose:** per Q8 — email-based applications at this stage.

**Blocks:**
1. **Why lully** — short manifesto block.
2. **Open positions** — list (editable via Shopify metaobjects — client updates freely).
3. **How to apply** — single form (name, position, CV upload, cover letter) → HR inbox.

**Phase:** 1.

### Legal / Contact — `/legal`

**Purpose:** terms, privacy, cookie policy, contact details, complaints book ("Livro de Reclamações" — required for Portuguese retail).

**Phase:** 1. Legal text supplied by client or by their counsel.

## Global / system pages

- **404** — branded, links back to Home and Shop.
- **Search results** — Shopify's predictive search, branded.
- **Order confirmation / pickup email** — branded Shopify transactional emails.
- **Newsletter signup** — single-field block in footer; integrated with Klaviyo or Mailchimp (TBD).
- **Cookie banner** — GDPR-compliant, tiered consent (PT requires explicit consent).

## Round-2 updates (2026-04-16)

All 7 follow-ups answered. Summary of impact on this sitemap:

- **Launch deadline locked: 2026-05-15** (F2) — brunch-menu launch event. Plan is now split into **v1.0 (May 15, event day)** and **v1.1 (10–14 days later)**. See `platform-recommendation.md` for the full timeline + scope split.
- **3 store addresses confirmed** (F1) — Anjos (flagship), Campo de Ourique, Beato. Hours per store still pending; will ask inline.
- **Pickup cutoff**: **14:00 same-day** (F3). Some products have earlier cutoffs (TBD which).
- **Festive & Bespoke Orders merge confirmed** (F4). Section name locked.
- **No vector sub-marks available** (F5) — design task: manually vectorize or commission. Parallel track in Week 1.
- **Press & social**: link Instagram `@lully1661_lisboa`; we curate press list ourselves.
- **B2B "Lully Inside"** launches descriptive-only; partner logos come later.

### Priority for the launch event

The event is a **brunch-menu press & influencer launch**, not an e-commerce push. The site's v1.0 job is to make the brunch experience feel real, the stores findable, and the reservation flow frictionless. Ranked priority:

1. **Home** — brunch hero, story, 3 stores, reservations CTA
2. **Brunch / Shop — brunch collection** — rich product pages for every brunch dish (photo, description, allergens, per-store availability)
3. **Stores** — map + 3 store cards with addresses, hours, and a store-specific reservation CTA
4. **Reservations** — The Fork widget(s); email fallback
5. **About / History** — the Lully story (for press to reference)
6. **Festive & Bespoke** — teaser + enquiry form (press may ask about catering)
7. Everything else (full Shop commerce flow, Lully Inside, Careers, Legal) as time allows

## What's blocked / pending per page

| Page | Status | Pending input |
|------|--------|---------------|
| Home | 🟢 Can design now | Brunch hero copy + photography (client) |
| Brunch / Shop | 🟡 Catalogue buildable; cart/checkout may slip to v1.1 | M3 — per-category cutoffs |
| Stores | 🟡 Addresses in; can build page | M1 — hours per store; M2 — dine-in vs pickup-only per store |
| Reservations | 🟡 Structure clear | M4 — The Fork status per store |
| Hero / Festive sections | 🟡 Need vectorized or re-drawn sub-marks | Design task (our side) |
| Lully Inside | 🟢 Descriptive-only ships now | F7 — partner logos "later" |
| Festive & Bespoke | 🟢 Structure locked | Client copy + seasonal photos |
| Careers | 🟢 Ships | List of open positions |
| Legal | 🟢 Template ready | Client / counsel for final legal text |

Micro-gaps (**M1–M4** — hours per store, dine-in vs pickup, per-category cutoffs, The Fork status per store) go out as a single short ping, not a new Google Doc.

## What is Phase 2 (for clarity)

- Third-party delivery (Uber Eats, Glovo) — Shopify connectors.
- Gift cards / loyalty program.
- Client's own payment system (Shopify Custom Payment App).
- Live POS ↔ website inventory sync (if client moves to Shopify POS or keeps another POS with good connector).
- Editorial Journal / recipe content.
- Optional Hydrogen migration for deeper design ambition.

## Navigation & interaction patterns

- **Primary nav** (desktop): Home · Shop · Festive & Bespoke · Stores · Reservations · About. (Lully Inside, Careers, Legal in footer.)
- **Mobile nav**: hamburger → the same items, plus direct CTAs for "Order for pickup" and "Book a table".
- **Language switcher**: top-right corner, shows `PT / EN`.
- **Cart**: slide-out drawer, shows pickup-store and pickup-time selector.
- **Sticky CTA on mobile** when scrolling past Home hero: "Order for pickup".

## Next step

Wireframe pass on: **Home**, **Shop index**, **Product page**, **Stores**. Four screens carry 80% of the UX risk.

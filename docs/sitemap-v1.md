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

## What's blocked in phase 1

| Page | Waiting on | Follow-up item |
|------|------------|----------------|
| Shop (checkout pickup-time UX) | Same-day cutoff | F3 |
| Stores | 3 store addresses + hours | F1 |
| Lully Inside | Partner names (not strictly blocking — we can launch descriptive-only) | F7 |
| Reservations | The Fork partnership status | (to add to F1 follow-up round) |
| Hero / Festive sections | Vector sub-marks for Meunier / Pâtissière / Caffetier | F5 |
| Timeline | "ASAP" = which month? | F2 |

None of these block the Week-1 setup work. All need to be answered by mid-Week 2 to stay on the 4–6 week timeline.

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

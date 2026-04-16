# Wireframes v0 — Home / Brunch / Stores / Reservations

**Status:** Draft v0.1 — internal, pre-visual-design
**Prepared:** 2026-04-16
**Purpose:** validate information architecture and content blocks before we commit visual design hours. Fidelity is deliberately low (ASCII sketches + written block detail) — any argument about layout vs. content belongs at this fidelity, not at Figma fidelity.

**Screens covered:** the 4 pages that carry 80% of launch-event risk per `sitemap-v1.md`.

**Conventions:**
- 🟢 = v1.0 (ships by 2026-05-15) · 🟡 = v1.0 if time, else v1.1 · 🔵 = v1.1 (post-event)
- **〈placeholder〉** = content we still need from client
- `M1 / M2 / M3 / M4` = micro-gaps the content depends on

---

## Global chrome (all pages)

### Top navigation — sticky, 72px tall, white background, fine 1px black border

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  lully 1661    Brunch  Shop  Stores  Reservations  About      PT | EN  IG  🛒 │
└──────────────────────────────────────────────────────────────────────────────┘
```

- Wordmark left, links center, language + IG + cart-pill right.
- `Brunch` is first in the nav (and linked from logo on event weeks) to match the launch priority.
- Cart pill: shows item count when >0. If cart slips to v1.1, replace with an **[Order for Pickup]** text CTA that scrolls the user to the Shop landing.
- Mobile: hamburger → vertical list, language toggle at the top, sticky [Reserve a table] CTA.

### Footer

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  lully 1661                                                                  │
│                                                                              │
│  Stores          Shop              Info            Follow                    │
│  Anjos           Breads            About           Instagram @lully1661_lisboa│
│  Campo Ourique   Pastries          Lully Inside                              │
│  Beato           Brunch            Careers                                   │
│                  Drinks            Festive & Bespoke                         │
│                                                                              │
│  ─────────────────────────────────────────────────────────────────────────   │
│  Newsletter:  [email field]  [Subscribe]       Livro de Reclamações ↗        │
│  © 2026 lully 1661                  Privacy · T&C · Cookies                  │
└──────────────────────────────────────────────────────────────────────────────┘
```

Notes:
- "Livro de Reclamações" is a legal requirement in Portuguese retail (link to the official e-book).
- Newsletter signup integrated with Klaviyo or Mailchimp (TBD).

---

## 1. Home — `/` (PT default) 🟢

### Sketch (desktop ≥1024px)

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                             [Top nav]                                        │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   ╔══════════════════════════════════════════════════════════════════════╗   │
│   ║  〈brunch hero image〉                                                 ║   │
│   ║                                                                      ║   │
│   ║         OUR BRUNCH HAS ARRIVED                                       ║   │
│   ║         Tuesdays through Sundays · Anjos · Campo de Ourique · Beato  ║   │
│   ║         [ See the menu ]   [ Reserve a table ]                       ║   │
│   ║                                                                      ║   │
│   ╚══════════════════════════════════════════════════════════════════════╝   │
│                                                                              │
├──────────────────────────────────────────────────────────────────────────────┤
│   THREE WAYS TO LULLY                                                        │
│                                                                              │
│    ┌────────────┐       ┌────────────┐       ┌────────────┐                  │
│    │ 〈Meunier〉  │       │〈Pâtissière〉│       │〈Caffetier〉 │                  │
│    │            │       │            │       │            │                  │
│    │  Breads    │       │  Pastries  │       │  Drinks &  │                  │
│    │            │       │            │       │  Brunch    │                  │
│    │  → Shop    │       │  → Shop    │       │  → Brunch  │                  │
│    └────────────┘       └────────────┘       └────────────┘                  │
├──────────────────────────────────────────────────────────────────────────────┤
│   THIS WEEK AT LULLY                                                         │
│                                                                              │
│    ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐                                 │
│    │ P1 │ │ P2 │ │ P3 │ │ P4 │ │ P5 │ │ P6 │   (6 rotating featured items)  │
│    └────┘ └────┘ └────┘ └────┘ └────┘ └────┘                                 │
│                                                                              │
│                           [ See the full menu ]                              │
├──────────────────────────────────────────────────────────────────────────────┤
│   VISIT US IN LISBON                                                         │
│                                                                              │
│    ┌────────────────────────────┐   ┌────────────────────────┐               │
│    │                            │   │ Anjos          →       │               │
│    │       〈map thumbnail〉      │   │ Campo de Ourique →     │               │
│    │       3 pins               │   │ Beato          →       │               │
│    │                            │   │                        │               │
│    └────────────────────────────┘   └────────────────────────┘               │
├──────────────────────────────────────────────────────────────────────────────┤
│   BOULANGERIE RENAISSANCE                                                    │
│                                                                              │
│    〈story image — oven or miller illustration〉                               │
│    "From tradition we kept the best. Here, bread is king…"                   │
│                                                                              │
│                          [ Read our story → ]                                │
├──────────────────────────────────────────────────────────────────────────────┤
│   FOR YOUR SPECIAL OCCASIONS                                                 │
│                                                                              │
│    〈festive product image〉                                                   │
│    Bespoke cakes · catering · event supply                                   │
│                    [ Plan a festive order → ]                                │
├──────────────────────────────────────────────────────────────────────────────┤
│   @lully1661_lisboa                                                          │
│    ┌──┐ ┌──┐ ┌──┐ ┌──┐ ┌──┐ ┌──┐    (Instagram feed, 6 latest posts)         │
│    └──┘ └──┘ └──┘ └──┘ └──┘ └──┘                                             │
├──────────────────────────────────────────────────────────────────────────────┤
│                              [Footer]                                        │
└──────────────────────────────────────────────────────────────────────────────┘
```

### Block-by-block

1. **Hero (≈80vh)** — full-bleed brunch photo; headline + sub + 2 CTAs.
   - Primary CTA: **Reserve a table** → `/reservations`.
   - Secondary CTA: **See the menu** → `/brunch`.
   - On event weeks, a small overlay badge: "Launching May 15".
   - Mobile: stack CTAs; image crops to 60vh.
   - Content needed: brunch hero shot + 2-line headline (PT + EN).

2. **Three ways to lully** — 3 cards, one per pillar.
   - Card art = the vectorized Baroque sub-mark + product photo peeking.
   - Labels conventional (Breads / Pastries / Drinks & Brunch) per Q13.
   - Drinks card leads to Brunch (since brunch is the launch focus), not the Drinks collection.

3. **This week at lully** — rotating 6-product carousel.
   - Driven by a Shopify metaobject so client can update weekly without dev help.
   - Desktop: 6 across · Tablet: 3 across · Mobile: snap-scroll carousel.

4. **Visit us in Lisbon** — map thumbnail + 3 store shortcuts.
   - Thumbnail uses a static map image with 3 pins; clicking opens `/stores`.
   - Each shortcut row: neighborhood name + arrow → scrolls to that store card on `/stores`.

5. **Boulangerie Renaissance** (story teaser) — 1 image + 2 paragraphs + CTA to `/about`.
   - Content: the first paragraph of the brand intro.

6. **Festive & Bespoke** teaser — 1 image + 1 line + CTA → `/festive-orders`.

7. **Instagram feed** — last 6 posts from `@lully1661_lisboa`.
   - Implementation: Shopify's native Instagram section OR a static "@mention + link" block if we want zero third-party dependency for launch.

### Phase notes
- Cart pill (top-right) is 🟡 — if cart slips, replace with "Order for Pickup" linking to the Shop landing.
- Instagram feed is 🟢; if the API-token flow is annoying we ship a static "@lully1661_lisboa" line and add the feed in v1.1.

### Open design questions
- Does the hero run brunch-first only during the launch weeks, then rotate to a seasonal hero later? We assume **yes** and plan the hero as a metaobject.

---

## 2. Brunch — `/pt/loja/brunch` · `/en/shop/brunch` 🟢

The **single most important page** for the 5/15 event. Every press link points here.

**Scope clarification (per M2):** Brunch is served **at Anjos only**, and is **dine-in only** in v1.0 (no pickup for brunch items yet). This page is an editorial menu + reservations bridge, not part of the commerce flow. Shop > Brunch collection does **not** carry "add to pickup order" at launch. Callouts and the hero CTA make "only at Anjos" clear.

### Sketch

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                             [Top nav]                                        │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   ╔══════════════════════════════════════════════════════════════════════╗   │
│   ║  〈brunch hero image — long plate shot〉                               ║   │
│   ║                                                                      ║   │
│   ║           OUR BRUNCH                                                 ║   │
│   ║           Daily — Tuesdays through Sundays                           ║   │
│   ║           Launching May 2026                                         ║   │
│   ║           [ Reserve a table ]                                        ║   │
│   ║                                                                      ║   │
│   ╚══════════════════════════════════════════════════════════════════════╝   │
│                                                                              │
├──────────────────────────────────────────────────────────────────────────────┤
│   EGGS                                                                       │
│                                                                              │
│    ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                      │
│    │ 〈photo〉      │  │〈photo〉       │  │〈photo〉       │                      │
│    │ Ovos Benedict│  │ Ovos Florent.│  │ Çılbır        │                     │
│    │ €12          │  │ €10,50       │  │ €8,50         │                     │
│    │ Poached eggs,│  │ Poached eggs,│  │ Poached eggs,│                     │
│    │ Hollandaise… │  │ spinach…     │  │ chili oil… │                       │
│    │ 🥛 🌾        │  │ 🥛 🌾        │  │ 🥛 🌾 🌶     │                       │
│    │ Anjos·Campo  │  │ Anjos·Campo  │  │ Anjos         │                    │
│    │ [Add to order│  │ [Add to order│  │ [Add to order]                     │
│    └──────────────┘  └──────────────┘  └──────────────┘                      │
│                                                                              │
│   TOASTS & GREENS                                                            │
│                                                                              │
│    ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                      │
│    │ Avocado Toast│  │ Le Monsieur  │  │ Granola Bowl │                      │
│    │ €8,50  (v)   │  │ €11          │  │ €5,50 / €7   │                      │
│    │ …            │  │ …            │  │ …            │                      │
│    └──────────────┘  └──────────────┘  └──────────────┘                      │
│                                                                              │
│   SANDWICHES                                                                 │
│    ┌──────────────┐                                                          │
│    │ Le Menuet    │                                                          │
│    └──────────────┘                                                          │
│                                                                              │
│   SOUPS & SWEETS                                                             │
│    ┌──────────────┐  ┌──────────────┐                                        │
│    │ Sopa do Mês  │  │ Pain Perdu   │                                        │
│    └──────────────┘  └──────────────┘                                        │
├──────────────────────────────────────────────────────────────────────────────┤
│   WHEN & WHERE                                                               │
│                                                                              │
│    Anjos              Tue–Sun     〈hours〉                                   │
│    Campo de Ourique   Tue–Sun     〈hours〉                                   │
│    Beato              Tue–Sun     〈hours〉   (M2 — if brunch served here)   │
│                                                                              │
│                       [ Reserve a table ]                                    │
├──────────────────────────────────────────────────────────────────────────────┤
│   BRING BRUNCH HOME                                                          │
│   Some of the brunch items are available for pickup — order before 14:00     │
│   for same-day pickup (M3 may narrow this for specific items).               │
│                    [ Browse all products for pickup → ]                      │
├──────────────────────────────────────────────────────────────────────────────┤
│                              [Footer]                                        │
└──────────────────────────────────────────────────────────────────────────────┘
```

### Block-by-block

1. **Hero** — long-form plate photograph, "Launching May 2026" badge visible pre-event.
   - Primary CTA: **Reserve a table** → `/reservations`.
   - No "As seen in" / press block (decision 2026-04-16: we don't curate press quotes for v1.0).

2. **Menu grouped by course** — sections match how guests order:
   - Eggs · Toasts & Greens · Sandwiches · Soups & Sweets · Drinks (add at v1.0 if drinks copy ready)
   - Initial product data drawn directly from `menu-weekly-sample.pdf`.
   - Each product card: photo · PT name · price · 1-line description · allergen icons · per-store availability pills · **Add to order** button (🟡 button live only if cart ships in v1.0).
   - **Menuet / Monsieur / Çılbır** — keep the PT original names prominently; the Lully vocabulary is a brand asset.

3. **When & where** — store/hours block, linked to /stores.
   - Waits on M1 (hours) and M2 (brunch-serving stores).
   - If Beato is pickup-only we grey it out here with a "Pickup only" label.

4. **Bring brunch home** — call to action that bridges to the Shop.
   - Cutoff copy uses "14:00" default; M3 will add "Some items require earlier cutoffs — see product page" if needed.

### Product-detail sub-page (one per item)

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  ← Back to brunch                                                            │
│                                                                              │
│   ┌───────────────────────┐    OVOS BENEDICT                                 │
│   │                       │    €12                                           │
│   │      〈photo〉           │                                               │
│   │                       │    Poached eggs, Hollandaise sauce, mustard,     │
│   │                       │    bacon, Urfa chili (İsot) and fresh herbs.     │
│   └───────────────────────┘    Served on our Fâcheux bread.                  │
│                                                                              │
│                                Allergens: 🥚 🥛 🌾                            │
│                                Available at: Anjos · Campo de Ourique        │
│                                                                              │
│                                Pickup cutoff: 14:00 same-day (M3)            │
│                                                                              │
│                                [ Reserve a table ]                           │
│                                [ Add to pickup order — v1.0/v1.1 ]           │
│                                                                              │
│   PAIRS WELL WITH                                                            │
│    ┌────┐ ┌────┐ ┌────┐                                                      │
│    └────┘ └────┘ └────┘                                                      │
└──────────────────────────────────────────────────────────────────────────────┘
```

Content fields per product (Shopify product attributes):
- Title (PT + EN) · Description (PT + EN) · Price · Allergens (multi-select) · Available-at stores (multi-select) · Cutoff override (optional, per-product) · Photo(s) · Pairs-with (product reference × 3).

### Phase notes
- Menu-as-catalogue is 🟢. Cart button 🟡.
- Drinks section: may slip if copy not ready. Fine — brunch story holds without it.

---

## 3. Stores — `/pt/lojas` · `/en/stores` 🟢

Brand-new page prompted by Q11 (3 stores already operating).

### Sketch

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                             [Top nav]                                        │
├──────────────────────────────────────────────────────────────────────────────┤
│   THREE STORES IN LISBON                                                     │
│   Find your nearest lully — or walk between all three.                       │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   ┌──────────────────────────────────────────────────────────────────────┐   │
│   │                                                                      │   │
│   │                        〈Lisbon map with 3 pins〉                      │   │
│   │                        Anjos ● Campo de Ourique ● Beato              │   │
│   │                                                                      │   │
│   └──────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   ┌───────────────────────────────────────────────────────────────── FLAGSHIP│
│   │  ANJOS                                                                   │
│   │  Rua do Forno do Tijolo 46, 1170-134 Lisboa                              │
│   │                                                                          │
│   │  Tue–Sat  08:30 – 19:00                                                  │
│   │  Sunday   08:30 – 17:00                                                  │
│   │  Monday   closed                                                         │
│   │  Bakery · Pastry · Brunch · Dine-in                                      │
│   │                                                                          │
│   │  ┌────┐ ┌────┐ ┌────┐                                                    │
│   │  │〈📷1〉│ │〈📷2〉│ │〈📷3〉│   Atmosphere / a line about the oven           │
│   │  └────┘ └────┘ └────┘                                                    │
│   │                                                                          │
│   │  [ Get directions ]   [ Reserve a table ]                                │
│   └──────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│   ┌──────────────────────────────────────────────────────────────────────┐   │
│   │  CAMPO DE OURIQUE                                                    │   │
│   │  Rua 4 de Infantaria 43, 1350-135 Lisboa                             │   │
│   │  Tue–Sat  08:00 – 19:00                                              │   │
│   │  Sunday   08:00 – 15:00 · Monday closed                              │   │
│   │  Bakery · Pastry                                                     │   │
│   │  〈photos〉                                                            │   │
│   │  [ Get directions ]                                                  │   │
│   └──────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│   ┌──────────────────────────────────────────────────────────────────────┐   │
│   │  BEATO                                                               │   │
│   │  Rua do Grilo 12, 1950-109 Lisboa                                    │   │
│   │  Tue–Sat  08:00 – 15:00 · Sun–Mon closed                             │   │
│   │  Bakery · Pastry                                                     │   │
│   │  〈photos〉                                                            │   │
│   │  [ Get directions ]                                                  │   │
│   └──────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
├──────────────────────────────────────────────────────────────────────────────┤
│   CAN'T COME IN TODAY?                                                       │
│   Order for pickup from any of our three stores.                             │
│                    [ Browse the shop → ]                                     │
├──────────────────────────────────────────────────────────────────────────────┤
│                              [Footer]                                        │
└──────────────────────────────────────────────────────────────────────────────┘
```

### Block-by-block

1. **Hero** — page title + 1-line intro + map.
   - Map: Mapbox or Google Maps static image with 3 pins + one interactive version below on desktop.

2. **Store cards** — 3 stacked (flagship first), each with:
   - Name + **FLAGSHIP** badge (Anjos only).
   - Full address (as given by client, pre-formatted for copy-to-clipboard).
   - Hours — per M1 (Beato is **Tue–Sat only**; Campo de Ourique and Anjos run Tue–Sun, closed Mon).
   - Services tags — per M2: Anjos = Bakery · Pastry · Brunch · Dine-in; Campo de Ourique and Beato = Bakery · Pastry only.
   - 2–3 photographs (client-supplied, per F12).
   - 1–2 lines of atmosphere copy (client or us).
   - CTAs vary per store:
     - **Anjos**: Get directions · Reserve a table (→ /reservations)
     - **Campo de Ourique** and **Beato**: Get directions only (no reservations, no pickup in v1.0 — pickup arrives with cart in v1.1)

3. **Can't come in today?** — bridges to Shop.

### Phase notes
- Page itself is 🟢.
- Interactive map with clickable pins can be 🟡 — static map + list is enough for v1.0.
- Store-scoped pickup (select pickup store on the product page) is 🔵 v1.1 — configured together with cart/checkout, not pre-wired in v1.0.

---

## 4. Reservations — `/pt/reservas` · `/en/reservations` 🟢

### Sketch

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                             [Top nav]                                        │
├──────────────────────────────────────────────────────────────────────────────┤
│   RESERVE A TABLE                                                            │
│   Brunch is served at our Anjos flagship. Write to us to book.               │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   ANJOS   — flagship                                                         │
│   Rua do Forno do Tijolo 46, 1170-134 Lisboa                                 │
│   Tue–Sat 08:30 – 19:00 · Sun 08:30 – 17:00 · Mon closed                     │
│                                                                              │
│   ┌──────────────────────────────────────────────────────────────────────┐   │
│   │                                                                      │   │
│   │   REQUEST A RESERVATION                                              │   │
│   │   ─────────────────────────────                                      │   │
│   │   Name       [____________________]                                  │   │
│   │   Email      [____________________]                                  │   │
│   │   Date       [ 📅 ]    Time  [ 🕐 ]                                  │   │
│   │   Guests     [  ▼ 2 ]                                                │   │
│   │   Note       [____________________]                                  │   │
│   │                                                                      │   │
│   │                     [  Send request  ]                               │   │
│   │                                                                      │   │
│   │   We reply within 24h to confirm. Or email us directly:              │   │
│   │   reservations@lully1661.com                                         │   │
│   └──────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│   (When The Fork is live for Anjos, this block is replaced by the widget.)   │
│                                                                              │
├──────────────────────────────────────────────────────────────────────────────┤
│   OTHER STORES                                                               │
│   Our Campo de Ourique and Beato stores are bakery & pastry retail —         │
│   no reservations needed. Come in during opening hours.                      │
│                    [ See all three stores → ]                                │
├──────────────────────────────────────────────────────────────────────────────┤
│   GROUPS, PRIVATE EVENTS & CATERING                                          │
│   More than 8 guests, a private evening, or catering off-site?               │
│                [ Plan a festive or bespoke event → ]                         │
├──────────────────────────────────────────────────────────────────────────────┤
│   GOOD TO KNOW                                                               │
│   · Please arrive within 15 minutes of your booking.                         │
│   · Cancellations: email us 24h ahead.                                       │
│   · Brunch is served 〈hours〉 — last orders at 〈time〉.                      │
├──────────────────────────────────────────────────────────────────────────────┤
│                              [Footer]                                        │
└──────────────────────────────────────────────────────────────────────────────┘
```

### Block-by-block

1. **Hero** — title + 1-line intro (no image — this is a utility page, keep it fast). Copy makes it explicit: reservations are for **Anjos only**.

2. **Anjos reservation block** — email-backed form in v1.0 (The Fork isn't live yet per M4). Form posts to `reservations@lully1661.com` (or similar; client to confirm). When client finishes The Fork onboarding, the form block swaps out for the widget — structure is designed to make that a single-section replacement.

3. **Other stores note** — small block that redirects to `/stores` for Campo de Ourique + Beato, explaining no reservations are needed there.

4. **Groups / private events** — bridges to `/festive-orders` enquiry form.

5. **Good to know** — short policy notes.

### Phase notes
- All 🟢 (email form + static copy — no external dependency).
- The Fork widget is **not required for v1.0** (client confirmed not set up yet per M4). Planned for v1.1+ once client completes Anjos listing on The Fork.

---

## Cross-cutting decisions (resolved 2026-04-16)

1. **Home third pillar** — "Drinks & Brunch" (keep as drafted). Brunch gets visible weight on Home without a dedicated pillar card.
2. **Store-scoped pickup** — deferred to **v1.1**, shipped together with cart/checkout. v1.0 store cards link to generic `/shop`.
3. **"As seen in" / press block** — dropped. We do not curate press quotes for v1.0; no scraping needed.
4. **Mobile sticky CTA** — **Reserve a table**. Launch event is brunch-focused.

---

## Next

- Share this v0 with you (internal) first for a red-team pass. Nothing to show the client yet — we need the M1–M4 answers first and a visual design layer before it's client-ready.
- Once M1–M4 are in: spot-fill the `〈hours〉 / 〈services〉 / 〈fork-status〉` placeholders, then move to visual design on Home + Brunch first (the two highest-leverage screens).

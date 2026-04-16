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
   - Secondary (small): "See press coverage" → anchors to a small "As seen in" row (if we have any by launch) or omitted.

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
│   │  Tuesday – Sunday   〈hours〉   (M1)                                     │
│   │  Bakery · Pastry · Brunch · Dine-in · Pickup                 (M2)        │
│   │                                                                          │
│   │  ┌────┐ ┌────┐ ┌────┐                                                    │
│   │  │〈📷1〉│ │〈📷2〉│ │〈📷3〉│   Atmosphere / a line about the oven           │
│   │  └────┘ └────┘ └────┘                                                    │
│   │                                                                          │
│   │  [ Get directions ]   [ Reserve a table ]   [ Order for pickup ]         │
│   └──────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│   ┌──────────────────────────────────────────────────────────────────────┐   │
│   │  CAMPO DE OURIQUE                                                    │   │
│   │  Rua 4 de Infantaria 43, 1350-135 Lisboa                             │   │
│   │  〈hours〉 (M1) · 〈services〉 (M2)                                    │   │
│   │  〈photos〉                                                            │   │
│   │  [ Directions ]   [ Reserve ]   [ Pickup ]                           │   │
│   └──────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│   ┌──────────────────────────────────────────────────────────────────────┐   │
│   │  BEATO                                                               │   │
│   │  Rua do Grilo 12, 1950-109 Lisboa                                    │   │
│   │  〈hours〉 (M1) · 〈services〉 (M2)                                    │   │
│   │  〈photos〉                                                            │   │
│   │  [ Directions ]   [ Reserve ]   [ Pickup ]                           │   │
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
   - Hours (M1 pending).
   - Services tags (M2 pending): Bakery · Pastry · Brunch · Dine-in · Pickup.
   - 2–3 photographs (client-supplied, per F12).
   - 1–2 lines of atmosphere copy (client or us).
   - 3 CTAs: **Get directions** (Google Maps URL), **Reserve a table** (The Fork or email — varies per store per M4), **Order for pickup** (Shop landing scoped to that store if we implement store-scoped pickup, or generic /shop in v1.0).

3. **Can't come in today?** — bridges to Shop.

### Phase notes
- Page itself is 🟢.
- Interactive map with clickable pins can be 🟡 — static map + list is enough for v1.0.
- Store-scoped pickup (select pickup store on the product page) depends on Shopify's Local Pickup setup — we configure this by default, so it's 🟢 as long as cart ships.

---

## 4. Reservations — `/pt/reservas` · `/en/reservations` 🟢

### Sketch

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                             [Top nav]                                        │
├──────────────────────────────────────────────────────────────────────────────┤
│   RESERVE A TABLE                                                            │
│   We'd love to feed you. Pick a store, pick a time.                          │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   ANJOS   — flagship                                                         │
│   Rua do Forno do Tijolo 46 · Tue–Sun · 〈hours〉                             │
│                                                                              │
│   ┌──────────────────────────────────────────────────────────────────────┐   │
│   │                                                                      │   │
│   │        〈The Fork reservation widget — iframe〉                        │   │
│   │        Calendar · guest count · time slots · "Book"                  │   │
│   │                                                                      │   │
│   └──────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│   Not available via The Fork? → reservations@lully1661.com                   │
│                                                                              │
├──────────────────────────────────────────────────────────────────────────────┤
│   CAMPO DE OURIQUE                                                           │
│   Rua 4 de Infantaria 43 · Tue–Sun · 〈hours〉                                │
│   〈Fork widget OR email fallback depending on M4〉                            │
├──────────────────────────────────────────────────────────────────────────────┤
│   BEATO                                                                      │
│   Rua do Grilo 12 · Tue–Sun · 〈hours〉                                       │
│   〈Fork widget OR email fallback depending on M4〉                            │
├──────────────────────────────────────────────────────────────────────────────┤
│   GROUPS, PRIVATE EVENTS & CATERING                                          │
│   More than 8 guests, a private evening, or catering off-site?               │
│                [ Plan a festive or bespoke event → ]                         │
├──────────────────────────────────────────────────────────────────────────────┤
│   GOOD TO KNOW                                                               │
│   · Please arrive within 15 minutes of your booking.                         │
│   · To cancel, use The Fork app or email us 24h ahead.                       │
│   · Brunch is served 〈hours〉 — last orders at 〈time〉.                      │
├──────────────────────────────────────────────────────────────────────────────┤
│                              [Footer]                                        │
└──────────────────────────────────────────────────────────────────────────────┘
```

### Block-by-block

1. **Hero** — title + 1-line intro (no image — this is a utility page, keep it fast).

2. **Store block × 3** — one per store, each either:
   - **A.** The Fork embed widget (iframe) + small email fallback link, OR
   - **B.** Email-only fallback block ("Write to reservations@… with your preferred date, time, and guest count; we reply within 24h.") — used for stores where The Fork isn't live.
   - Pending M4 to choose A vs B per store.

3. **Groups / private events** — bridges to `/festive-orders` enquiry form.

4. **Good to know** — short policy notes.

### Phase notes
- All 🟢.
- If The Fork onboarding for a store takes >1 week, that store ships with block B and we swap in block A post-launch.

---

## Cross-cutting open questions for internal review

1. **Pillar naming on Home** — we wrote "Drinks & Brunch" on the third card to acknowledge that brunch is the event priority. Is that the right label, or should the third card be "Brunch" (with drinks rolled under shop) until after the event?
2. **Store-scoped pickup** — do we ship Shopify Local Pickup per store from day 1 (even if cart is v1.1), or wait? Recommendation: configure it now so when cart ships the plumbing is ready.
3. **"As seen in"** — only worth a block on Home/Brunch if we curate 3+ press quotes by 2026-05-10. Deadline to abort: Week 3 end.
4. **Mobile sticky CTA** — "Reserve a table" sticky or "Order for pickup" sticky? Recommendation: **Reserve**, since the launch event is about brunch.

---

## Next

- Share this v0 with you (internal) first for a red-team pass. Nothing to show the client yet — we need the M1–M4 answers first and a visual design layer before it's client-ready.
- Once M1–M4 are in: spot-fill the `〈hours〉 / 〈services〉 / 〈fork-status〉` placeholders, then move to visual design on Home + Brunch first (the two highest-leverage screens).

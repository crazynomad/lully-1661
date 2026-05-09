# lully 1661 — Website Requirements Understanding

**Status:** Draft v0.1 — for client review
**Prepared:** 2026-04-16
**Based on:** `raw-requirements/` (website brief, 2022 brand intro, Jan 2026 motto deck, sample weekly menu, brand marks, moodboard imagery)

> This document is our interpretation of the raw materials the client has shared. Items marked **`[CLARIFY]`** are open questions we would like the client to confirm or correct before we move to scoping and design. Items marked **`[ASSUMPTION]`** are our best reading of the brief — please call out anything wrong.

---

## 1. Brand at a glance

- **Name:** *lully 1661* — cursive lowercase wordmark, double-L (per primary logo file and the `www.Lully1661.com` domain in the website brief).
  - **`[CLARIFY]`** ✅ **Done 2026-05-09:** GitHub repo and local working directory renamed `lullly-1661` → `lully-1661` (triple-L was a transcription error from a verbal spelling). All brand-name references in the docs corrected to double-L on the same date.
- **Category:** Artisanal French bakery + all-day brunch restaurant.
- **Location (first outlet):** Lisbon, Portugal.
- **Ambition:** Pan-European bakery brand, 5-year horizon, starting in Lisbon.
- **Brand story (short):** Named after Jean-Baptiste Lully, the Italian-born French Baroque composer who was granted French citizenship in **1661**. The bakery positions itself as a "Renaissance of bakery" — tradition as the starting point, continuous reinvention as the daily practice. Motto candidate: *"Boulangerie Renaissance — Bread Baked Better."*
- **Tone of voice:** Operatic, sensory, savory, intimate, authentic-yet-affordable.

## 2. Three product pillars

The brand uses three Baroque-engraving sub-marks, one per pillar. We interpret these as navigation/section cues for the site — not separate brands.

| Pillar | Sub-mark | Scope (from brief + menu) |
|---|---|---|
| **Meunier** (Miller) | `logo-sub-meunier.jpeg` | Breads, viennoiserie, sourdoughs; the bread oven as centerpiece |
| **Pâtissière** (Pastry-maker) | `logo-sub-patissiere.jpeg` | Pastries, desserts, viennoiserie |
| **Caffetier** (Coffee vendor) | `logo-sub-caffetier.jpeg` | Drinks, brunch, day-to-day hospitality |

**`[CLARIFY]`** Are *Meunier / Pâtissière / Caffetier* intended as on-site section labels / counter signage, or only as archival illustrations? This affects whether we build the site's primary menu around them.

## 3. Audience (from brand intro)

1. **Primary:** Local residents near each outlet.
2. **Secondary:** Affluent international expats and tourists in Lisbon.
3. **Tertiary:** Influencers and travel / local KOLs.

**`[CLARIFY]`** Do we need the site to serve all three audiences equally at launch, or prioritize locals (PT) with expat/tourist support (EN) second?

## 4. Sitemap — our reading of the brief

Based on the information-tree section of `brief-website.docx`:

```
Home
├─ History — "A commitment based in tradition (who we are)"
├─ Shop (click & collect → later full delivery)
│   ├─ Breads
│   ├─ Pastries
│   ├─ Desserts
│   ├─ Snacks
│   ├─ Brunch
│   └─ Drinks
├─ Special Orders                    (custom bakes, large formats)
├─ Restaurant Reservations           (dine-in booking)
├─ Lully Inside (B2B)                (partnerships with brands & chefs)
├─ Recruitment                       (jobs)
└─ Legal / Contact
```

**`[CLARIFY] / [ASSUMPTION]`**
- The brief mentions a **mood board and music** ("mood board and music" line near the top). We interpret this as a *page or hero treatment*, not a separate site. Should there be a dedicated "Ambience" / audio-visual section showcasing Baroque music + boutique photography?
- **Languages: Portuguese + English** (confirmed 2026-04-16). French brand copy will be translated/adapted into EN; no French on the public site.
- **Default locale at `/`: Portuguese** (confirmed 2026-04-16). Browser-language detection will offer EN when appropriate.
- **URL structure: subpath** — `/pt/…` and `/en/…` (confirmed 2026-04-16). Single domain, simpler SEO.
- Should **events** (e.g. the *Gareth × Sezin* guest-chef luncheon visual we received) have their own section, or live under News / Journal?

## 5. eCommerce scope

Explicitly requested: *"eCommerce enabled / community enhanced."*

**Phase 1 (launch)**
- **Click & Collect** — customer orders online, picks up in-store.
- **Menu browsing** by pillar (Breads, Pastries, Desserts, Snacks, Brunch, Drinks).

**Phase 2 (later)**
- **Integrated payments** via the brand's own payment system.
- **Delivery** via third parties (Uber Eats, Glovo mentioned).

**Platform note from brief:** *"In Portugal most payments happen with a system called Multibanco. Shopify seems to be fully functional in Portugal."*

**`[CLARIFY]`**
- **Is Shopify the chosen platform**, or is it one reference among several? The brief sounds exploratory ("seems to be functional"), not decided. This is the single biggest architectural decision — Shopify vs. headless (e.g. Next.js + a PT-friendly checkout) changes scope, cost, and timeline meaningfully.
- **Multibanco** must be supported at launch. Stripe, SumUp, and Mollie all offer Multibanco on Shopify — any preference?
- **Inventory / fulfillment cutoffs**: how far ahead can a customer place a click-and-collect order (same day? 24h?)? Does bread get a different cutoff than pastries?
- **Do products have SKUs and live stock**, or is it an order-taking form that the store reconciles manually each morning?

## 6. Restaurant reservations

Brief mentions: *"Restaurant reservations — The Fork? Our own system linked with booking platforms."*

**`[CLARIFY]`**
- Is **The Fork** (LaFourchette) the preferred partner, or are we open to alternatives (SevenRooms, OpenTable, Resy, or a custom form)?
- Is table booking needed at launch, or is it acceptable to ship with a "reservations coming soon" placeholder and a phone/email contact?
- Are there multiple outlets with different booking URLs, or a single outlet at launch?

## 7. B2B — "Lully inside"

Brief: *"Discover partnerships with leading brands and chefs."*

**`[ASSUMPTION]`** This is a showcase / lead-gen page (not a B2B ordering portal). Content would be case studies, logos of partner brands, and a contact form for new partnership enquiries.

**`[CLARIFY]`**
- Do partnerships already exist we can feature at launch, or is this a placeholder page until the first few deals close?
- Is a wholesale ordering portal for existing B2B customers part of Phase 1, Phase 2, or out of scope?

## 8. Recruitment

Brief: *"Recruitment."* (one word, no further detail)

**`[ASSUMPTION]`** A simple careers page — open positions listed, with an "apply" button that goes either to email or a short application form (CV upload + motivation).

**`[CLARIFY]`**
- Any existing HR / ATS system (Workable, Teamtailor, etc.) we should integrate with?

## 9. Design direction

From the 2022 brand intro and the 3D shop render:
- **Baroque decorative motifs** (engravings of millers, coffee vendors, pastry-makers, instruments) against a **contemporary** white / marble / tile backdrop.
- **Gentle Baroque music** as part of the in-store experience — **`[CLARIFY]`** should the website have ambient audio? (Considerations: autoplay is blocked by browsers; it should be a user-triggered toggle, and should not play on eCommerce pages.)
- **Color palette:** **`[CLARIFY]`** not formalized in what we've received — we see black wordmark, mustard gold, cream backgrounds, and pink accents in the *Gareth × Sezin* poster. Is there a formal brand guideline PDF we have not received?
- **Typography:** the wordmark uses a hand-drawn cursive. **`[CLARIFY]`** Is there a prescribed body / display typeface? We'll suggest one if not.

### Reference sites (from brief)

> https://www.do-beco.com
> https://www.liberte-paris.com/
> https://loulou-paris.com/
> https://thefrenchbastards.fr/en

**Our reading:** all four are French artisanal-bakery sites with strong typography, editorial product photography, and straightforward menu/shop UX. We'd aim for a similar feel, with the Baroque illustrations as the distinctive layer.

## 10. Timeline — unclear

The 2022 brand intro mentions "Teaser June 2023 → Launch September 2023." The 2026-01 motto deck and the EUR-priced weekly menu strongly suggest **the Lisbon outlet is already open or opening imminently in 2026**.

**`[CLARIFY]`**
- Current status of the first Lisbon outlet — open, soft-launched, or pre-launch?
- Desired website go-live date?
- Is there a marketing event (opening, press tasting) the site needs to be live for?

## 11. Content readiness

**`[CLARIFY]`** — who provides:
- Professional photography of products, interior, team? (We only have one 3D render and vintage engravings.)
- Final copy in PT / EN (/ FR)? Or is copywriting part of the scope?
- Logo in vector format (SVG / AI)? We currently only have a raster PNG of the primary wordmark.
- Final brand guidelines (color, typography, logo usage rules)?

## 12. What we're proposing next

Once the client confirms or corrects this document, we would like to produce:

1. A **scope & sitemap v1** — phase-1 vs phase-2 feature split, explicit.
2. A **platform recommendation** — Shopify vs. headless, with cost/timeline impact.
3. A **wireframe of Home + Shop flow** — to validate the information architecture before visual design.

---

## Appendix — open questions, consolidated

Client answered round 1 in Google Docs on **2026-04-16**. Summary of each answer and status below; follow-up questions for round 2 are listed in the next section.

| # | Status | Client answer (verbatim, trimmed) | Our interpretation |
|---|--------|-----------------------------------|-------------------|
| Q1 | ✅ Resolved | "Brand is Lully 1661 / URL is correct" | Rename GitHub repo `lullly-1661` → `lully-1661`; domain `www.Lully1661.com`. |
| Q2 | ✅ Resolved | Confirmed 2026-04-16 | PT + EN, PT default, `/pt/` + `/en/` subpaths. |
| Q3 | ⚠ Deferred to us | "Open to alternatives" | Client has no preference — **we must recommend**. Default plan: Shopify-powered with headless front-end only if budget/timeline justify. |
| Q4 | ✅ Resolved | "Multibanco is the default… open to others to accept credit cards not linked to multibanco" | Multibanco + standard credit-card (Visa/Mastercard). Gateway choice still ours (Stripe probably best; confirms both). |
| Q5 | 🟡 Partial | "Same day ideal, inventory updated by staff" | Staff-reconciled inventory (option b). **Follow-up:** same-day cutoff time? (e.g. order before 14:00 for same-day pickup, else next-day). |
| Q6 | ✅ Resolved | "The Fork if possible, if not a email exchange would work. The benefit with the Fork is their marketing" | Integrate The Fork; fall back to email if integration blocks. |
| Q7 | ✅ Resolved | "A page with text describing how we work and who we work with on B2B with an email form" | Showcase + enquiry form. No portal. |
| Q8 | ✅ Resolved | "Email at this stage only" | Simple careers page with email-based applications. |
| Q9 | ✅ Resolved (no guidelines) | "Nothing much beside the images I have shared with you" | No formal guidelines; we propose color palette, typography, and logo-usage rules during design. |
| Q10 | ✅ Resolved | "Yes, sending now" — 2 `.ai` files delivered 2026-04-16 | `logo-lully-1661-vector-black.ai` + `…-grey.ai`. Primary wordmark in vector. **Follow-up (minor):** vector of the three sub-marks (Meunier / Pâtissière / Caffetier) still only raster JPEG. |
| Q11 | 🟡 Partial | "We now have 3 stores operating 6 days a week Tue–Sunday included. Website live asap." | Three Lisbon stores already operating — **major change** from our assumption of "first outlet imminent". **Follow-ups:** addresses, neighborhoods, opening hours per store; "ASAP" = target week/month? |
| Q12 | ✅ Resolved | "Copy and images by us" | Client supplies photography and final PT + EN copy. |
| Q13 | ✅ Resolved (with a twist) | "Only for reference as a style for the pages, though these can be used in some, maybe as per the example of the flyer I sent you" | Primary nav uses **conventional labels** (Breads / Pastries / Drinks). Meunier / Pâtissière / Caffetier illustrations are a **design motif** — we can compose them with the wordmark in the Gareth × Sezin flyer style for hero sections, event posters, packaging mock-ups. |
| Q14 | ✅ Resolved | "understood" | Proceed with user-triggered ambient toggle; off during shop/checkout. |
| Q15 | 🟡 Reinterpreted | "A section where we describe the kind of festive products we can offer as well as events we can organize or supply goods for." | Reframes from "Events" to **"Festive & Events"** — catering/festive product catalogue *and* events (both ones Lully hosts and ones Lully supplies). **Follow-up:** is this the same as the "Special Orders" node in the sitemap, or separate? They sound overlapping. |

## Round 2 — follow-up questions, answered 2026-04-16

| # | Status | Client answer (verbatim) | Our interpretation |
|---|--------|-------------------------|-------------------|
| F1 | 🟡 Mostly resolved | "Flagship is **Anjos** — Rua do Forno do Tijolo 46, 1170-134 Lisboa. The other 2: **Campo de Ourique** — Rua 4 de Infantaria 43, 1350-135 Lisboa; **Beato** — Rua do Grilo 12, 1950-109 Lisboa." | 3 stores mapped. **Gap:** opening hours per store and which stores offer dine-in/brunch vs pickup-only. Will ask inline in next review. |
| F2 | 🔴 **Hard constraint** | "**Ideally before May 15** as we will officially launch our brunch menu with a major event with media and influencers." | **Launch on or before 2026-05-15** (29 days from 2026-04-16). Major press / influencer event attached. Compresses our 4–6 week plan into a hard 4-week sprint. |
| F3 | 🟡 Partial | "14:00 works for us for same day pick-up and no all products have the same cut-off" | Default cutoff: **14:00 for same-day pickup**. Not all products share that cutoff (assumed typo "no(t) all products"). **Gap:** which product categories need earlier/different cutoffs, and what are they (likely breads earlier, bespoke orders 24–48h notice). |
| F4 | ✅ Resolved | "Ok for the moment" | Merge confirmed: one "Festive & Bespoke Orders" section. |
| F5 | ✅ Resolved (negative) | "No such files available" | No vector sub-marks. We will either (a) carefully up-res and mask the raster JPEGs, (b) manually vectorize them, or (c) commission a designer to re-draw in SVG. Planning for (b)+(c) to be safe, given their hero-level usage. |
| F6 | ✅ Resolved | "Instagram **@lully1661_lisboa**. Press coverage can be found on Google search typing lully 1661." | Link IG from footer. We'll compile a press shortlist ourselves from Google and propose "as seen in" citations. |
| F7 | 🟡 Deferred | "We have a few, can I provide a list later on?" | Launch the Lully Inside page **descriptive-only** with a "Partners to be announced" slot; client sends logos + names before or after launch. |

## What Round 2 unblocks

- **Stores page**: we can start building now with the 3 confirmed addresses; add hours when client sends.
- **Reservations page**: can start — we still need to verify The Fork partnership status for each of the 3 stores.
- **Sitemap**: locked at v1 (see `sitemap-v1.md`).
- **Festive & Bespoke Orders**: merge confirmed; content block layout can proceed.

## What Round 2 changes

- **Timeline**: our 4–6 week estimate in `platform-recommendation.md` now **collapses to a 4-week sprint** with a fixed deadline of **2026-05-15**. Two implications:
  1. No slack for a separate soft-launch week — go-live IS the event.
  2. Scope at launch should be optimized for the event's focus: **brunch menu discovery, the 3 stores, reservations, and the festive teaser**. Cart / Multibanco checkout / live pickup orders can ship as a **v1.1 two weeks after the event** if QA is under pressure — see updated phase plan in `platform-recommendation.md`.
- **Sub-mark art**: no vectors means a **design task** we now own (vectorizing the 3 Baroque engravings or commissioning new SVGs). Budget implication.
- **B2B page**: launches without featured partners — acceptable per client.

## Remaining micro-gaps — resolved 2026-04-16

All four answered by client via WhatsApp (verbatim quotes preserved).

### M1 — Hours per store

| Store | Tue–Sat | Sun | Mon |
|-------|---------|-----|-----|
| **Anjos** (flagship) | 08:30 – 19:00 | 08:30 – 17:00 | closed |
| **Campo de Ourique** | 08:00 – 19:00 | 08:00 – 15:00 | closed |
| **Beato** | 08:00 – 15:00 | closed | closed |

Note: Beato is a **5-day operation** (Tue–Sat only). Prior sitemap text saying "Tue–Sun all three stores" is wrong and needs correction.

### M2 — Brunch / dine-in / pickup per store

- **Only Anjos serves brunch.** Campo de Ourique and Beato are bakery/pastry retail only.
- **No pickup for brunch items yet.** Brunch is dine-in only at Anjos.
- Implication: brunch is a **single-store, dine-in-only** product in v1.0. Shop > Brunch collection is **editorial/menu-display only** on Day 1 (no "add to pickup order"). Revisit post-launch if client wants to enable brunch-to-go.

### M3 — Per-category cutoffs

Client's verbatim answer: *"no all products have the same cut-off time"* — read as **uniform 14:00 same-day cutoff across all pickup products** (no per-category variation). This slightly contradicts Round 2 F3 ("not all products share that cutoff"); we interpret M3 as the latest word and the simpler policy.

- **Non-blocking for v1.0**: cart/checkout ships in v1.1, so pickup cutoff UX is a v1.1 concern. If per-category cutoffs re-surface during cart implementation we revisit then — no need to re-ask now.

### M4 — The Fork status + reservations scope

- **The Fork is not set up yet.** Client "would only need to list the Anjos store" when they do set it up.
- **Only Anjos needs reservations.** Campo de Ourique and Beato are retail-only — no reservation flow at all.
- Launch behaviour: **v1.0 Reservations page = single Anjos block, email-fallback only.** Swap in The Fork widget for Anjos when (and if) the client completes their The Fork onboarding.

### Combined impact on v1.0 scope

| Before | After M1–M4 |
|--------|-------------|
| Reservations page with 3 store blocks + 3 Fork widgets | **1 Anjos block, email-only** |
| Brunch = Shop collection w/ pickup | **Brunch = Anjos-only dine-in, menu display** |
| 3 stores blocked by "hours per store" | **Hours confirmed, Beato 5-day schedule** |
| M3 cutoff variation → cart UX complication | **Uniform 14:00 (simpler); cart is v1.1 regardless** |

Net effect: Reservations and Brunch both get simpler. One fewer The Fork integration to ship. No new blockers.

## What Round 1 unblocks (we can now proceed with)

- Rename repo to `lully-1661`.
- Draft **scope & sitemap v1** (revised sitemap below, incorporating Q13 and Q15).
- Draft **platform recommendation** (since Q3 deferred to us).
- Begin **wireframes** for Home and Shop flow.

## Revised sitemap (Round 1 applied)

```
Home
├─ History / About
├─ Shop  (click & collect; live-ordering with staff-reconciled inventory)
│   ├─ Breads
│   ├─ Pastries
│   ├─ Desserts
│   ├─ Snacks
│   ├─ Brunch
│   └─ Drinks
├─ Festive & Bespoke Orders         (merged Special Orders + Events + Catering)
├─ Reservations                     (The Fork embed; email fallback)
├─ Lully Inside (B2B)               (text + partner logos + enquiry form)
├─ Stores                           (3 locations: addresses, hours, map)
├─ Careers                          (email applications)
└─ Legal / Contact
```

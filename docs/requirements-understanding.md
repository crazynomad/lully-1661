# lully 1661 — Website Requirements Understanding

**Status:** Draft v0.1 — for client review
**Prepared:** 2026-04-16
**Based on:** `raw-requirements/` (website brief, 2022 brand intro, Jan 2026 motto deck, sample weekly menu, brand marks, moodboard imagery)

> This document is our interpretation of the raw materials the client has shared. Items marked **`[CLARIFY]`** are open questions we would like the client to confirm or correct before we move to scoping and design. Items marked **`[ASSUMPTION]`** are our best reading of the brief — please call out anything wrong.

---

## 1. Brand at a glance

- **Name:** *lully 1661* — cursive lowercase wordmark, double-L (per primary logo file and the `www.Lully1661.com` domain in the website brief).
  - **`[CLARIFY]`** The repo was initially created as `lullly-1661` (triple L) following a verbal spelling. All materials use double-L. We recommend renaming the repo to `lully-1661` before any public link is shared. Please confirm.
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
- The sample menu includes items in Portuguese and English; the brand story is told in French and English. **Is the site trilingual (PT / EN / FR) or bilingual (PT / EN)?**
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

| # | Question | Blocks |
|---|----------|--------|
| Q1 | Confirm brand spelling is *lully* (double L). Rename repo? | Repo rename, all copy |
| Q2 | Target languages: PT / EN / FR, or subset? | Content scoping, CMS setup |
| Q3 | Platform: Shopify (as hinted) or headless alternative? | Architecture, cost, timeline |
| Q4 | Payment providers on launch (Multibanco mandatory — which gateway)? | Checkout setup |
| Q5 | Click-and-collect: ordering cutoffs, live stock vs. form-to-staff? | Backend scope |
| Q6 | Reservations: The Fork, alternative, or placeholder at launch? | Integration |
| Q7 | B2B scope: showcase only, or wholesale ordering portal? | Phase 1/2 split |
| Q8 | Recruitment: integrate an ATS, or email-based? | Scope |
| Q9 | Brand guidelines PDF (color, type, logo variants) available? | Design kickoff |
| Q10 | Vector logo + final asset pack? | Design kickoff |
| Q11 | First-outlet launch status + desired website go-live date? | Timeline |
| Q12 | Who produces product photography and final copy? | Resourcing |
| Q13 | Meunier / Pâtissière / Caffetier — section labels or archival art only? | Navigation |
| Q14 | Ambient audio on the site? | UX decision |
| Q15 | Dedicated Events section (e.g. guest-chef luncheons)? | Sitemap |

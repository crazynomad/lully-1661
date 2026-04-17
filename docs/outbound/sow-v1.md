# Statement of Work — lully 1661 Website

**Version:** v1 — for client signature
**Date:** 2026-04-16
**Prepared for:** lully 1661, Lisboa
**Launch deadline:** 2026-05-15 (brunch-menu press & influencer event, Anjos)

<!--
  Pricing guidance (strip before sending):
    v1.0 build (29-day launch scope)         €TBD · suggested range €12–18k
    v1.1 build (cart/checkout + The Fork)    €TBD · suggested range €4–6k
    Bundled total (v1.0 + v1.1)              €TBD · suggested range €15–22k
    Ongoing support retainer, optional       €TBD/month · suggested €400–800
  Payment: 50% on signature · 30% on v1.0 launch · 20% on v1.1 delivery.
  All figures exclude VAT and any third-party software subscriptions paid by the client.
-->

## 1. Context

The brief (`brief-website.docx`, Round 1 + Round 2 answers, M1–M4 clarifications of 2026-04-16) establishes lully 1661 as an organic Lisboa bakery preparing to launch a new brunch service at its Anjos flagship on **2026-05-15**. The site has two jobs: make the brunch launch feel real for press and influencers attending that event, and give the brand a digital home that reflects the Baroque-contemporary positioning already visible in the sub-marks and the 2022 brand deck.

A visual direction has been prepared ahead of this SOW and is attached at:

> **https://crazynomad.github.io/lully-visual-direction/**

This SOW proposes a two-phase build: **v1.0** shipping on 2026-05-15 for the event, and **v1.1** completing the commerce flow 10–14 days later.

## 2. Scope of work

### 2.1 Platform

- **Shopify** theme, based on the recommendation in `docs/platform-recommendation.md`
- **Shopify Markets** for PT/EN bilingual content with per-language SEO
- **Stripe (Multibanco)** for Portuguese payments
- **Metaobjects** for editorially-controlled content (weekly menu, seasonal festive offer, open careers positions)
- **Klaviyo or Mailchimp** for newsletter (final choice at kick-off)

### 2.2 v1.0 — delivered by 2026-05-15

Pages built in order of event priority:

| # | Page | Notes |
|---|------|-------|
| 1 | **Home** | Brunch hero, three pillars (Pães / Pastelaria & brunch / Bebidas), "This week at lully" module, stores teaser, newsletter footer |
| 2 | **Brunch** | Anjos-only, dine-in-only editorial menu (no pickup in v1.0). Full menu with courses, allergens, pricing |
| 3 | **Stores** | Map + 3 store cards (Anjos / Campo de Ourique / Beato) with confirmed hours + services per store |
| 4 | **Reservations** | Anjos-only, email-fallback form (The Fork is not yet live — widget swap-in in v1.1 if confirmed) |
| 5 | **About / History** | Brand story adapted from the 2022 brand deck |
| 6 | **Festive & Bespoke** | Structure + enquiry form; seasonal content editable by client |
| 7 | **Shop (skeleton)** | Category tiles + product listing pages; **no cart/checkout yet** (moved to v1.1) |
| 8 | **Lully Inside (B2B)** | Descriptive page + enquiry form; partner logos later |
| 9 | **Careers** | Open positions (editable) + email application form |
| 10 | **Legal / Contact** | Terms, privacy, cookies, Livro de Reclamações link |

Plus global: 404, branded Shopify search, branded transactional emails, GDPR cookie banner with tiered consent.

### 2.3 v1.1 — delivered 10–14 days after launch

- **Full Shop commerce** — cart, checkout, pickup-store selector, 14:00 same-day pickup cutoff
- **The Fork widget** for Anjos reservations (swap-in, replacing email fallback) — if the client's The Fork listing is confirmed by 2026-05-29
- **Product-detail pages** for the full catalogue (ingredients, allergens, weight, cross-sell)
- **Bug-fix window** covering anything surfaced during the launch event

### 2.4 Design deliverables (included)

- Shopify theme implementation of the visual direction (typography, colour system, layout grid)
- **Vectorized Pâtissière sub-mark** in the gold-flourish + ink-script treatment to match the existing Meunier and Caffetier marks
- Image-optimized asset set for Home, Brunch, Stores
- Editorial CSS system — enough that the client can publish new blog/journal posts later without bringing us back

### 2.5 Content and technical assistance

- PT/EN content architecture (client supplies copy; we structure, translate labels/UI, migrate)
- SEO metadata + Open Graph + structured data for store locations and menu
- Google Analytics 4 + Search Console setup
- Domain + DNS configuration for `lully1661.com` (or the domain the client confirms)

## 3. Out of scope

To set clear expectations, the following are explicitly **not** part of this engagement:

- **Food and product photography** — we use what the client supplies; new photo shoots are a separate engagement
- **Copywriting in any language** — client supplies PT copy; EN translation of final copy is included, but first-draft writing is not
- **Motion-design specification** beyond what the theme supports out-of-the-box
- **Custom illustration** beyond the three sub-marks
- **POS integration** — v1.1 assumes inventory is manually curated or synced via a standard connector, not a custom POS build
- **Uber Eats / Glovo integration** — Phase 2 after launch
- **Gift cards, loyalty program, custom payment app** — Phase 2
- **Hardware, printed collateral, packaging design** — out of engagement

## 4. Dependencies on client

To hit the 2026-05-15 deadline, the following inputs are needed by the dates indicated:

| Due | Input from client |
|-----|-------------------|
| **2026-04-22** (kick-off) | Domain confirmation, Shopify store admin access, Instagram handle, reservation inbox address, HR inbox address, B2B sales inbox address |
| **2026-04-29** | Brunch menu copy (PT + per-dish descriptions), brunch photography (or authorization to use existing imagery), store photography (3 locations) |
| **2026-05-03** | About / History copy (PT), festive & bespoke intro copy |
| **2026-05-06** | Legal text: Terms, Privacy Policy, Cookie Policy, Livro de Reclamações link |
| **2026-05-29** (for v1.1) | The Fork listing confirmation for Anjos, full product catalogue with ingredients + allergens, pickup-cutoff per product if anything deviates from the 14:00 default |

Delays on client-side dependencies shift the launch in 1-for-1 proportion and may push items from v1.0 into v1.1.

## 5. Timeline

| Week | Dates | Focus |
|------|-------|-------|
| 1 | 2026-04-16 → 04-22 | Kick-off, Shopify setup, theme scaffolding, Pâtissière sub-mark vectorization |
| 2 | 2026-04-23 → 04-29 | Home + Brunch builds (highest-priority launch pages), content ingestion |
| 3 | 2026-04-30 → 05-06 | Stores + Reservations + About; mobile polish; cookie banner; analytics |
| 4 | 2026-05-07 → 05-13 | Festive & Bespoke + Lully Inside + Careers + Legal; SEO; QA pass; staging review |
| Launch | **2026-05-14 → 05-15** | Production cutover, final smoke tests, launch day support |
| v1.1 | 2026-05-18 → 05-29 | Cart, checkout, full Shop, The Fork swap-in, bug fixes from launch week |

## 6. Commercials

### 6.1 Fees

| Item | Fee |
|------|-----|
| v1.0 build — event-ready launch (10 pages, PT/EN, platform setup, visual direction implementation) | **€TBD** |
| v1.1 build — full commerce + The Fork widget + bug-fix window | **€TBD** |
| **Total — bundled** | **€TBD** |

All fees are quoted in euros and exclude Portuguese VAT where applicable. Third-party subscriptions (Shopify, Klaviyo/Mailchimp, The Fork) are paid directly by the client.

### 6.2 Payment schedule

- **50%** on signature of this SOW — unblocks kick-off on 2026-04-22
- **30%** on v1.0 production launch (target 2026-05-15)
- **20%** on v1.1 delivery

Invoices are issued on each milestone and payable within 14 days.

### 6.3 Optional ongoing support

Post-launch, the client may engage an optional monthly retainer covering: minor content/layout changes, performance monitoring, analytics review, security updates, and priority bug-fix SLA. Rate: **€TBD / month**, month-to-month, cancellable with 30 days' notice.

## 7. Change management

Anything outside the scope defined in §2 is a **change request**. Small adjustments are absorbed at our discretion; substantive changes are scoped, priced, and signed off before any work begins. This protects the launch deadline from scope drift and keeps the commercials transparent.

## 8. Intellectual property

- **Client owns** all final deliverables upon full payment: the Shopify theme, the vectorized sub-marks, the content structure, the domain configuration.
- **We retain** the right to include lully 1661 in our portfolio and case-study materials unless the client requests otherwise in writing.
- The visual direction document at the URL above is a working reference and becomes the client's on final payment.

## 9. Acceptance

This SOW is accepted by signature below. Acceptance constitutes authorization to begin work on 2026-04-22 and triggers the first invoice (50%).

---

**For lully 1661**

Name: ______________________
Title: ______________________
Date: ______________________
Signature: ______________________

**For [Burn Wang]**

Name: ______________________
Date: ______________________
Signature: ______________________

---

**Attachment:** Visual Direction v1 — https://crazynomad.github.io/lully-visual-direction/

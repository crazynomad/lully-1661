# Architecture — lully 1661 Website

**Status:** Draft v0.1 — internal
**Prepared:** 2026-05-09
**Companion to:** [`platform-recommendation-v2.md`](./platform-recommendation-v2.md), [`sitemap-v2.md`](./sitemap-v2.md)
**Audience:** any engineer touching this repo

> This is the contract between us and ourselves for how the codebase is laid out and how decisions are made. It exists so the second engineer on the project doesn't re-litigate week-1 choices, and so the phase-2 commerce drop-in lands without a refactor. **If you find yourself disagreeing with a rule below, update this document in the same PR.**

## 1. Goals & non-goals

**Goals**
- Static-quality Core Web Vitals on every page (LCP < 2.5s, CLS < 0.1, INP < 200ms on mobile 4G).
- Owner-edited content updates publish in seconds without a deploy.
- Add a feature later (e.g., commerce, loyalty, ordering) by dropping a folder, not rewriting a layout.
- One source of truth per concept (one `Store` schema, one `localBusinessJsonLd` helper, one `localizedString` shape).
- The repo is readable in an afternoon by a competent Next.js engineer.

**Non-goals**
- No experimental Next.js features in v1 (no PPR, no streaming SSR for content pages, no Server Component caching tricks). All content pages are statically generated.
- No multi-tenant template work (single-instance build per `platform-recommendation-v2.md`).
- No commerce in v1 — but every architectural decision must keep the phase-2 commerce drop-in cheap.

## 2. Repository layout

```
.
├─ app/
│  └─ [locale]/                       # next-intl locale segment ("pt" | "en")
│     ├─ layout.tsx                    # Locale-aware root: fonts, providers, header, footer
│     ├─ page.tsx                      # Home
│     ├─ sobre|about/page.tsx          # About
│     ├─ menu/
│     │  ├─ page.tsx                   # Menu hub (category tiles)
│     │  ├─ [category]/page.tsx        # Category (paes, pastelaria, brunch, …)
│     │  └─ [category]/[slug]/page.tsx # Product detail
│     ├─ diário|journal/
│     │  ├─ page.tsx
│     │  └─ [slug]/page.tsx
│     ├─ encomendas|festive-orders/page.tsx
│     ├─ reservas|reservations/page.tsx
│     ├─ lully-inside/page.tsx
│     ├─ lojas|stores/
│     │  ├─ page.tsx                   # Hub
│     │  └─ [slug]/page.tsx            # Per-store
│     ├─ trabalha-connosco|careers/page.tsx
│     └─ legal/page.tsx
│  ├─ api/
│  │  └─ keystatic/[...params]/route.ts # Keystatic API handler (admin reads/writes)
│  ├─ keystatic/[[...rest]]/page.tsx    # Embedded Keystatic admin (auth-gated)
│  ├─ sitemap.ts                       # Generated from routes + Keystatic Reader
│  ├─ robots.ts
│  └─ globals.css                      # Tailwind entry + tokens
├─ features/                           # Domain modules — see § 3
│  ├─ menu/
│  ├─ stores/
│  ├─ journal/
│  ├─ festive-orders/
│  ├─ reservations/
│  ├─ careers/
│  ├─ b2b/
│  └─ home/
├─ components/                         # Cross-feature primitives ONLY
│  ├─ Container.tsx
│  ├─ Section.tsx
│  ├─ Button.tsx
│  ├─ LocalizedLink.tsx
│  └─ JsonLd.tsx                       # JSON-LD <script> wrapper
├─ lib/
│  ├─ keystatic/
│  │  ├─ reader.ts                     # createReader() instance (typed reads)
│  │  └─ image.ts                      # Image URL helpers (handles repo-hosted + optional Cloudinary)
│  ├─ i18n/
│  │  ├─ routing.ts                    # next-intl routing config (locales, pathnames)
│  │  └─ request.ts
│  ├─ jsonld/                          # JSON-LD helpers — one per schema type
│  │  ├─ organization.ts
│  │  ├─ localBusiness.ts
│  │  ├─ menuItem.ts
│  │  ├─ article.ts
│  │  ├─ event.ts
│  │  └─ breadcrumb.ts
│  ├─ resend/
│  │  └─ client.ts
│  ├─ analytics.ts
│  ├─ seo.ts                           # generateMetadata helpers, hreflang map
│  ├─ fonts.ts                         # next/font/local declarations
│  └─ utils/cn.ts
├─ keystatic.config.ts                  # CMS schema (collections + singletons + fields)
├─ content/                             # All CMS content lives here, git-tracked
│  ├─ homepage.yaml                     # singleton
│  ├─ aboutPage.yaml                    # singleton
│  ├─ store/
│  │  ├─ anjos.yaml
│  │  ├─ campo-de-ourique.yaml
│  │  └─ beato.yaml
│  ├─ productCategory/
│  │  └─ <slug>.yaml
│  ├─ product/
│  │  └─ <slug>/index.yaml + image.jpg
│  ├─ weeklyMenuItem/
│  │  └─ <yyyy-Www-slug>/index.yaml
│  ├─ journalPost/
│  │  └─ <yyyy-mm-dd-slug>/index.mdx + hero.jpg
│  ├─ partner/
│  │  └─ <slug>.yaml
│  ├─ openPosition/
│  │  └─ <slug>.yaml
│  ├─ seasonalCampaign/
│  │  └─ <slug>/index.yaml
│  └─ legalPage/
│     └─ <slug>.mdx
├─ messages/
│  ├─ pt.json                          # next-intl static strings
│  └─ en.json
├─ public/                             # Static assets (favicons, OG fallback, logos)
├─ tests/
│  ├─ unit/                            # Vitest
│  └─ e2e/                             # Playwright
├─ .github/workflows/                  # CI
├─ biome.json
├─ next.config.ts
├─ package.json
├─ tailwind.config.ts                  # (only if v4's CSS-first config doesn't suffice)
└─ tsconfig.json
```

### Path aliases

```jsonc
// tsconfig.json
{
  "compilerOptions": {
    "paths": {
      "@/*":          ["./*"],
      "@/features/*": ["features/*"],
      "@/components/*": ["components/*"],
      "@/lib/*":      ["lib/*"],
      "@/content/*": ["content/*"]
    }
  }
}
```

Imports always use aliases (`@/features/menu/...`), never relative `../../..`. Linted via Biome.

## 3. Feature folder convention

Every domain module under `features/<name>/` follows the same shape:

```
features/menu/
├─ index.ts                # Public API of this feature — all imports from outside go through here
├─ schemas.ts              # Keystatic collection/singleton refs + TypeScript entry types
├─ queries.ts              # Read-side helpers wrapping the Keystatic Reader (filters, joins)
├─ data.ts                 # Server-side fetchers calling the Keystatic Reader at build time
├─ components/             # Components used only inside this feature
│  ├─ MenuCategoryCard.tsx
│  ├─ ProductCard.tsx
│  └─ ProductDetail.tsx
├─ jsonld.ts               # Feature-specific JSON-LD assemblers (composes from lib/jsonld/*)
└─ tests/                  # Unit / component tests for this feature
```

### Hard rules

- **No cross-feature imports below `features/<name>/index.ts`.** A page in `app/[locale]/menu/page.tsx` imports from `@/features/menu` (the index). It does *not* reach into `@/features/menu/components/...`.
- **A feature does not import another feature.** If two features need the same data (e.g., menu + stores both reference `Store`), the shared piece moves to `lib/` or `features/<shared>/`. Cross-feature dependencies are a smell that the boundary is wrong.
- **Components in `components/` are domain-free.** A `Button` is a button. A `ProductCard` lives in `features/menu/`, not in `components/`.
- **One feature, one folder.** Phase-2 commerce becomes `features/checkout/`. Loyalty becomes `features/loyalty/`. No `app/checkout/page.tsx` referencing util files scattered in `lib/`.

### Why this matters

The single largest predictor of "can we add commerce in 2 weeks" vs "we need to refactor for a month" is whether the v1 codebase respects feature boundaries. By-type folders (`components/`, `hooks/`, `utils/`) collapse all features onto a flat namespace; by the time phase-2 ships, the namespace is unsearchable. By-feature folders mean adding `features/checkout/` is a one-folder PR.

## 4. Keystatic content model

The schema is a single TypeScript file at `keystatic.config.ts` at the repo root. Content lives in `content/` as YAML/MDX/image files, fully git-tracked. The owner edits via the embedded admin at `/keystatic`; saves commit to GitHub via Keystatic Cloud's GitHub App and trigger a Vercel deploy.

### 4.1 Bilingual pattern

Every user-facing string field uses a nested `fields.object()` with `pt` and `en` keys:

```ts
// keystatic.config.ts
import { fields } from '@keystatic/core';

const localizedString = ({ label, multiline = false }: { label: string; multiline?: boolean }) =>
  fields.object(
    {
      pt: (multiline ? fields.text({ label: 'PT', multiline: true }) : fields.text({ label: 'PT' })),
      en: (multiline ? fields.text({ label: 'EN', multiline: true }) : fields.text({ label: 'EN' })),
    },
    { label, layout: [6, 6] } // side-by-side at 12-col grid; falls back to stacked on narrow viewports
  );
```

For MDX/rich body content, two parallel `fields.document()` instances (`bodyPt`, `bodyEn`) — Keystatic's document field handles MDX with custom block components.

**Editor experience:** PT and EN appear in a single panel per field (side-by-side on wide screens, stacked on narrow). This is the bilingual ergonomics trade-off accepted on 2026-05-09 vs Sanity's purpose-built `localizedString` UX.

**Required fields:** every `localizedString` field requires both `pt` and `en` to be non-empty before the entry can be saved (`validation: { isRequired: true }` on each leaf). Forbids the half-translated state.

### 4.2 Collection / singleton schemas (sketch)

| Name | Kind | Storage path | Key fields |
|---|---|---|---|
| `homepage` | singleton | `content/homepage.yaml` | hero (`localizedString` multiline), featuredItems (relationship[] → `weeklyMenuItem`), seoOverride |
| `aboutPage` | singleton | `content/aboutPage.yaml` | bodyPt + bodyEn (document), philosophy, team[] |
| `store` | collection | `content/store/<slug>.yaml` | name, slug, neighborhood, address (object), geo (lat/long), hours (array of {weekday, open, close}), phone, photo, atmospherePt + atmosphereEn, services[], theForkUrl |
| `product` | collection | `content/product/<slug>/` | namePt/En, slugPt/En, descriptionPt/En, category (relationship), image, allergens[], availableAt (relationship[] → store), pairsWith (relationship[]) |
| `productCategory` | collection | `content/productCategory/<slug>.yaml` | name (`localizedString`), slug (`localizedString`), illustration (sub-mark image), description |
| `weeklyMenuItem` | collection | `content/weeklyMenuItem/<yyyy-Www-slug>/` | extends `product` shape + `weekOf` (date) + `featured` (boolean) |
| `journalPost` | collection | `content/journalPost/<yyyy-mm-dd-slug>/` | title, slug, heroImage, bodyPt + bodyEn (document), publishedAt, author (string), tags (array of strings) |
| `partner` | collection | `content/partner/<slug>.yaml` | name, logo, sector, testimonial (`localizedString`) |
| `openPosition` | collection | `content/openPosition/<slug>.yaml` | title, department, store (relationship), description (`localizedString` multiline), applyEmail, validThrough |
| `seasonalCampaign` | collection | `content/seasonalCampaign/<slug>/` | name, season, heroImage, description, products (relationship[]), leadTime, enquiryEnabled |
| `legalPage` | collection (slug-keyed) | `content/legalPage/<slug>.mdx` | slug, body (document) |

Collections that include images use a directory-per-entry layout (`<slug>/index.yaml` + image files alongside) so images are colocated with their entry and easy to spot in PR diffs. Collections that are pure metadata (no images) are flat YAML files.

### 4.3 Slug strategy

Slugs are **per-locale** to support locale-matched URLs: `product` has both `slugPt` and `slugEn` text fields. The directory name on disk (e.g., `content/product/pao-de-trigo-rustico/`) is the canonical entry ID; the per-locale slugs are emitted into the routing pages via `generateStaticParams`.

The `next-intl` `pathnames` config maps top-level segments per locale (`/menu` ↔ `/menu`, `/lojas` ↔ `/stores`); dynamic segments inside come from the locale-matched slug fields.

A **CI test** asserts no two entries in a collection share a `slugPt` or `slugEn` (slugs must be unique within a locale to avoid routing collisions).

### 4.4 Querying — typed Reader API

Use `createReader` from `@keystatic/core/reader` for build-time reads:

```ts
// lib/keystatic/reader.ts
import { createReader } from '@keystatic/core/reader';
import config from '@/keystatic.config';
export const reader = createReader(process.cwd(), config);

// features/menu/data.ts
import { reader } from '@/lib/keystatic/reader';

export async function getProductBySlug(slug: string, locale: 'pt' | 'en') {
  const all = await reader.collections.product.all();
  const match = all.find(
    p => p.entry.slugPt === slug || p.entry.slugEn === slug
  );
  if (!match) return null;
  // Resolve relationships
  const stores = await Promise.all(
    match.entry.availableAt.map(s => reader.collections.store.read(s))
  );
  return { ...match.entry, availableAt: stores.filter(Boolean) };
}
```

The Reader API is fully typed — `match.entry.slugPt` is `string`, `match.entry.availableAt` is `string[]` (relationship slugs). No `any`, no codegen step.

Relationship resolution is **explicit** (more verbose than Sanity's `availableAt[]->` GROQ pattern). Helper functions in `features/<feature>/queries.ts` keep the verbosity contained — pages call `getProductBySlug(...)`, not the Reader directly.

CI rule: no `as any` in `features/*/data.ts` or `features/*/queries.ts`.

### 4.5 Admin access

- Admin embedded at `/keystatic` (the `app/keystatic/[[...rest]]/page.tsx` route).
- **Auth via Keystatic Cloud (free tier).** Owner signs in with email/Google. Keystatic Cloud holds a GitHub App that writes to our private repo on save — owner does not need a GitHub account.
- Roles: Keystatic Cloud has team-level permissions (admin / editor). Owner gets `editor`; we get `admin`.
- **Local dev:** the admin runs in `local` mode (writes to local filesystem) when `NODE_ENV !== 'production'`. Production builds run in `github` mode (Keystatic Cloud → GitHub).
- **Branch strategy:** owner edits commit directly to `main` → triggers production deploy. For risky/long edits, owner can use Keystatic's draft branches feature (one branch per draft); we merge via PR after review. Documented in the owner training session.

## 5. Routing & i18n

### 5.1 Locale routing

`next-intl` middleware:
- Default locale: `pt`.
- Locale prefix strategy: `as-needed` is **not** used — we always prefix (`/pt/...` and `/en/...`) for clean SEO and unambiguous canonicals. `/` 308-redirects to `/pt/`.
- Locale detection: on first visit only, optionally use `Accept-Language` to suggest `/en/`; never override an explicit URL.

### 5.2 Pathname mapping

Per-locale path segments are configured once in `lib/i18n/routing.ts`:

```ts
export const pathnames = {
  '/': '/',
  '/sobre':            { pt: '/sobre',                en: '/about' },
  '/menu':             { pt: '/menu',                 en: '/menu' },
  '/menu/[category]':  { pt: '/menu/[category]',      en: '/menu/[category]' },
  '/menu/[category]/[slug]': '/menu/[category]/[slug]',
  '/diário':           { pt: '/diário',               en: '/journal' },
  '/diário/[slug]':    { pt: '/diário/[slug]',        en: '/journal/[slug]' },
  '/encomendas':       { pt: '/encomendas',           en: '/festive-orders' },
  '/reservas':         { pt: '/reservas',             en: '/reservations' },
  '/lully-inside':     '/lully-inside',
  '/lojas':            { pt: '/lojas',                en: '/stores' },
  '/lojas/[slug]':     { pt: '/lojas/[slug]',         en: '/stores/[slug]' },
  '/trabalha-connosco':{ pt: '/trabalha-connosco',    en: '/careers' },
  '/legal':            '/legal',
} as const;
```

Switching language **preserves the current path** by mapping through this table. A `<LocalizedLink>` component wraps `next-intl`'s `Link` with the project's typed routing.

### 5.3 Static strings vs CMS strings

- **`messages/{pt,en}.json`** — UI chrome (buttons, form labels, error messages, navigation labels). Versioned with the code.
- **Keystatic** — anything the owner edits (page bodies, product names, store atmosphere, journal posts).

If a string sits in code that the client wants to edit, it moves to Keystatic. If a string is engineering scaffolding, it stays in `messages/`.

## 6. SEO & JSON-LD

### 6.1 Per-page metadata contract

Every page exports:

```ts
export async function generateMetadata({ params }): Promise<Metadata> {
  return seo({
    title: '...',                         // localized
    description: '...',                   // localized
    canonical: '/menu/paes/pao-rustico',  // current path, locale-prefixed
    alternates: hreflangAlternates(...),  // PT, EN, x-default
    openGraph: { ... },
  });
}
```

Helpers in `lib/seo.ts`. Hreflang generation walks the `pathnames` map and outputs alternates for both locales plus `x-default` (which points to PT).

### 6.2 JSON-LD policy

- Every page type has a JSON-LD helper colocated with its feature folder (e.g., `features/stores/jsonld.ts` calls `lib/jsonld/localBusiness.ts`).
- The page renders `<JsonLd data={...} />` once per type. Multiple types per page are emitted as a single `@graph` array, not separate script tags.
- All JSON-LD passes through `zod` validation in dev (catches missing fields before deploy).
- **CI gate:** for every route added, a unit test must assert the JSON-LD passes a Schema.org sanity check (helper validates required fields per type).

### 6.3 Per-page-type JSON-LD map

| Route | JSON-LD types |
|---|---|
| `/` | `Organization` |
| `/sobre` | `AboutPage`, `BreadcrumbList` |
| `/menu` | `CollectionPage`, `BreadcrumbList` |
| `/menu/[category]` | `CollectionPage`, `BreadcrumbList` |
| `/menu/[category]/[slug]` | `MenuItem` (or `Product` once commerce returns), `BreadcrumbList` |
| `/menu/brunch` | `Menu`, references parent `Restaurant` (Anjos) |
| `/diário` | `Blog`, `BreadcrumbList` |
| `/diário/[slug]` | `Article` (or `BlogPosting`), `BreadcrumbList` |
| `/encomendas` | `Service`, optional `Event[]` for past events |
| `/reservas` | `WebPage`, `BreadcrumbList` |
| `/lojas` | `ItemList` (referencing per-store URLs) |
| `/lojas/[slug]` | `Bakery` + `LocalBusiness` (single combined entity), `BreadcrumbList` |
| `/lully-inside` | `Service`, `BreadcrumbList` |
| `/trabalha-connosco` | `WebPage` + `JobPosting[]` for open positions |
| `/legal` | `WebPage` |

### 6.4 NAP consistency

The same name, address, and phone number appear in:
1. The visible page text on the per-store page.
2. The `LocalBusiness` JSON-LD on that page.
3. The Google Business Profile for that store.

These are sourced from the same Keystatic `store` entry. There is no copy-paste.

## 7. Image policy

- All images render through `next/image`.
- Images live in the repo, colocated with their entry (e.g., `content/product/pao-rustico/main.jpg`). Build-time optimization by Next.js handles WebP / AVIF conversion, responsive sizing, and lazy loading.
- **Width and height are always provided.** Zero CLS is the rule, not the goal. Keystatic stores image dimensions in the entry metadata; pages read them from the entry, not by probing the file.
- `sizes` attribute is mandatory on full-bleed and responsive images. Default `sizes` per breakpoint live in `lib/keystatic/image.ts`.
- **Image budget per page** (Lighthouse CI gate): ≤ 800KB on Home, ≤ 600KB on per-store and product pages, ≤ 200KB on the Home hero alone.
- **Pre-upload sizing rule** (enforced by Keystatic field validation + a CI check): no source image larger than 2400px on the long edge or 500KB on disk. Photography supplied by the client is resized once on ingest, not at every build. A `scripts/optimize-content-images.ts` script runs on `content/**/*.{jpg,png}` to enforce this.
- **Cloudinary escape hatch:** if photo volume exceeds ~500 images or the repo grows past ~1GB, switch image fields from `fields.image()` to `fields.url()` with a Cloudinary uploader. The pages reading them are unaffected (`<Image src={cloudinaryUrl} ...>` works the same as `<Image src={localPath} ...>`). Documented now so the migration is mechanical when the threshold trips.
- **No raw `<img>` tags anywhere in the codebase.** MDX image blocks render through custom Keystatic component serializers that emit `next/image`. CI grep gate fails the PR if a raw `<img` literal appears outside test fixtures.

## 8. Forms & email

### 8.1 Pattern

All forms use the same shape:

1. Client component with `react-hook-form` + `zod` resolver for client-side validation.
2. Server action receives the validated payload, re-validates on the server with the same `zod` schema.
3. Server action calls `lib/resend/client.ts` to dispatch the email.
4. Server action returns `{ ok: true }` or `{ ok: false, message }` consumed by `useFormState`.

The `zod` schema lives in the feature folder and is imported by both sides — single source of truth for validation.

### 8.2 Forms in v1

| Form | Inbox | Special handling |
|---|---|---|
| Festive & Bespoke enquiry | sales@... | Optional date / guest-count / budget fields |
| Reservations (Anjos email fallback) | reservations@... | Date, time, party size, dietary notes |
| B2B Lully Inside | sales@... | Volume, delivery frequency, sector |
| Careers application | hr@... | CV file upload (PDF, ≤ 5MB), cover letter |
| Newsletter signup | Mailchimp / Buttondown API | Double-opt-in (compliance) |

### 8.3 File uploads (Careers)

CVs are uploaded to a temporary Vercel Blob (or S3 bucket) → presigned URL passed to Resend as an attachment, → blob expires in 30 days. We do not retain CVs in our infrastructure beyond the email pipeline.

### 8.4 Spam protection

- All forms gated by **Cloudflare Turnstile** (free, privacy-friendly, no Google reCAPTCHA).
- Honeypot field as a secondary filter.
- Rate-limit by IP at the server action layer (Upstash Redis or Vercel KV — pick in week 1).

## 9. Caching & deploy flow

### 9.1 Default rendering mode

- **All content pages are statically generated at build.** App Router with `generateStaticParams` for dynamic segments (products, journal posts, store slugs).
- **No ISR.** Content lives in the repo; the only way for content to change is a git commit, which triggers a Vercel build, which produces a new fully-static deploy. No `revalidate` constants, no `revalidateTag` calls, no `/api/revalidate` route.
- This makes the production site **fully cacheable at the edge** — every page is a static HTML response.

### 9.2 Publish flow

```
Owner edits at /keystatic
  → Saves an entry
  → Keystatic Cloud commits to GitHub via the configured GitHub App
  → GitHub push to main triggers Vercel auto-deploy
  → Vercel runs `next build` (incremental — only changed pages re-rendered if cache is warm)
  → New deployment promoted to production (~1–3 min from save)
```

The owner sees their changes live within 1–3 minutes of clicking Save. This is the publish-latency trade-off accepted on 2026-05-09 vs Sanity's webhook-revalidate flow (which would be sub-second).

### 9.3 Build performance

Because every owner edit triggers a build, build time matters more here than on a webhook-revalidate stack. Targets:

- **Cold build:** ≤ 4 min on Vercel (current Next.js 15 baseline for ~50 pages + ~100 content entries).
- **Warm build (single content edit):** ≤ 90 seconds (Next.js incremental + Vercel build cache).
- **Lighthouse CI:** runs in parallel with the deploy, not as a build gate (it gates PRs, not production deploys).

If build times grow past these thresholds (roughly when content exceeds ~500 entries), revisit either incremental adoption or migration to the webhook-revalidate model (i.e., Sanity).

### 9.4 Forms

Server actions are uncached. No deploy or revalidation effects — they dispatch email via Resend and return.

### 9.5 Why no ISR

A common instinct is to combine "static at build" with "ISR for content updates," but with Keystatic that combination buys nothing: content updates already trigger a build. ISR would add a second cache layer with its own invalidation story for no win. Keep the model simple: content is static; deploys are the publish primitive.

## 10. Performance budgets & Lighthouse CI

| Metric | Target |
|---|---|
| LCP (mobile 4G) | < 2.5s |
| CLS | < 0.1 |
| INP | < 200ms |
| Total JS (initial) | ≤ 130KB gzipped per route |
| Total transfer (mobile, hero pages) | ≤ 800KB on Home; ≤ 600KB on per-store |
| Lighthouse Performance | ≥ 90 |
| Lighthouse Accessibility | ≥ 95 |
| Lighthouse Best Practices | ≥ 95 |
| Lighthouse SEO | ≥ 95 (gate) |

CI runs Lighthouse against `/`, `/pt/menu`, `/pt/lojas/anjos`, `/pt/diário/<seed-post>`. Below-threshold = failed PR.

## 11. Accessibility

- All interactive primitives use `@radix-ui/react-*` for keyboard + screen-reader behavior.
- Color contrast verified at design-token time (Tailwind palette is checked once); Lighthouse a11y score ≥ 95 in CI.
- All images carry meaningful `alt` text from Keystatic (every image field is paired with a sibling `alt` field shaped as `localizedString` and required by validation). Decorative images explicitly opt in to `alt=""` via a Keystatic boolean field.
- Forms have associated labels, error messages are announced via `aria-live`.
- Keyboard nav: tab order matches visual order on every page; focus rings are visible (Tailwind `focus-visible:ring`).
- PT and EN screen-reader pronunciation: `<html lang>` switches with locale; multi-language regions use `lang` attribute on the element.

## 12. Error handling & observability

- **Sentry** wraps the Next.js app (`@sentry/nextjs`). Free tier suffices.
- Server actions wrap in `try/catch`; errors are reported with the form name as a tag.
- Keystatic Reader failures during build fail the build loudly — CI alerts and the previous deploy stays live (Vercel only promotes successful builds). Production runtime cannot fail on Keystatic reads because all content is baked into the static deploy.
- A global `error.tsx` boundary at `app/[locale]/error.tsx` shows a localized error page, preserves header/footer, and offers links back to Home / Menu / Lojas.
- 404 page (`app/[locale]/not-found.tsx`) is branded and links to the most recent journal post.

## 13. Environment variables

| Variable | Surface | Notes |
|---|---|---|
| `KEYSTATIC_GITHUB_CLIENT_ID` | server only | Keystatic Cloud GitHub App client ID |
| `KEYSTATIC_GITHUB_CLIENT_SECRET` | server only | Keystatic Cloud GitHub App secret |
| `KEYSTATIC_SECRET` | server only | Session signing secret (random 32+ bytes) |
| `NEXT_PUBLIC_KEYSTATIC_GITHUB_APP_SLUG` | client + server | GitHub App slug for the install link in the admin UI |
| `RESEND_API_KEY` | server only |  |
| `RESEND_FROM` | server only | `noreply@lully1661.com` (DKIM-verified) |
| `MAILCHIMP_API_KEY` / `MAILCHIMP_LIST_ID` | server only | (or Buttondown equivalents) |
| `TURNSTILE_SITE_KEY` / `TURNSTILE_SECRET_KEY` | mixed |  |
| `SENTRY_DSN` / `SENTRY_AUTH_TOKEN` | mixed |  |
| `GOOGLE_MAPS_EMBED_KEY` | server only | URL-restricted to lully1661.com |

`.env.local` is git-ignored. `env.example` lives in the repo with placeholder values. Production secrets live in Vercel env vars, scoped per environment.

## 14. Branching & deployment

- `main` is always deployable. Vercel auto-deploys `main` to production.
- Every PR opens a Vercel preview URL with the PR's content (Keystatic content lives in the branch — preview URLs render branch content automatically; no separate dataset).
- PRs require: green CI (typecheck, lint, unit, Lighthouse on key routes), 1 reviewer.
- Squash-merge with conventional-commit-style titles.
- No long-lived feature branches. Behind-flag is for phase-2 work; v1 ships as one continuous merge train.

## 15. Testing

Tests are not the primary quality gate for an editorial site, but the following are non-optional:

- **Unit (Vitest):** `lib/jsonld/*`, `lib/seo.ts`, form `zod` schemas, slug resolution. Aim for 80%+ on these specific files.
- **Component (Vitest + Testing Library):** `<JsonLd>`, `<LocalizedLink>`, form components.
- **E2E (Playwright):** one happy path per release — Home → Menu → category → product → back → store page → reservation form. Runs in CI on `main` only (not per PR).
- **Visual regression:** out of scope for v1 (use design QA instead). Add Chromatic or Percy if regression frequency justifies it.

## 16. Definition of Done — adding a new page

A new route is "done" when:

- [ ] Route exists in `app/[locale]/...` with `generateMetadata`.
- [ ] Hreflang alternates are correct for PT and EN (or reason documented if PT-only).
- [ ] JSON-LD helper exists and the page renders `<JsonLd>`.
- [ ] Schema validates in [Google Rich Results Test](https://search.google.com/test/rich-results).
- [ ] All images use `next/image` with width/height + `sizes` + Keystatic-sourced `alt`.
- [ ] Lighthouse Performance ≥ 90, Accessibility ≥ 95, SEO ≥ 95 (CI gates).
- [ ] Page appears in `app/sitemap.ts` output.
- [ ] If CMS-driven: the relevant Keystatic collection/singleton is read in the page's `data.ts`, an entry exists in `content/`, and editing it via `/keystatic` (in dev) produces the expected change after a rebuild.
- [ ] Localized strings present in both `messages/pt.json` and `messages/en.json` (or a CMS-backed equivalent).
- [ ] Page entry added to the Definition-of-Done table in this doc if it introduces a new pattern.

## 17. Phase-2 commerce readiness checklist

These week-1 decisions exist *because* commerce returns later. Do not violate without a v3 architecture doc:

- [ ] Product page layout has a designated CTA slot (currently "Visit a store" / "Order for an event") that swaps to "Add to pickup order" without layout shift.
- [ ] `product` Keystatic collection has optional commerce fields (`sku`, `price`, `currency`, `availableForSale`) commented out in `keystatic.config.ts` — adding them in phase 2 is non-breaking.
- [ ] `store` Keystatic collection has a `pickupCutoff` field (currently unused in v1) so phase-2 cart UX has the data ready.
- [ ] Header has a designated slot for a future cart icon (rendered as `null` in v1).
- [ ] Routing config has commented-out paths for `/menu/[category]/[slug]/comprar` (PT) / `/menu/[category]/[slug]/buy` (EN) and `/checkout`.
- [ ] No JSON-LD `MenuItem` field clashes with the `Product` schema we'll switch to in phase 2.

When commerce work begins, the diff is concentrated in one new feature folder + a few additive Keystatic fields + commerce-specific routes — not a layout rewrite.

## 18. Open decisions

| Decision | Owner | Due |
|---|---|---|
| Mailchimp vs Buttondown (depends on whether client already has a list) | Client → us | week 1 |
| Cookie consent: CookieYes vs hand-rolled | Eng | week 1 |
| Vercel KV vs Upstash Redis for form rate-limiting | Eng | week 2 |
| `/diário` slug encoding (UTF-8 vs `/jornal` ASCII fallback) | Client | week 1 |
| Keystatic auth: Cloud (free, hosted) vs self-hosted GitHub App | Eng | week 1 — leaning Cloud |
| Image hosting threshold: at what content volume do we move from `content/`-hosted to Cloudinary | Eng | revisit at 200 images |
| Owner workflow: edit-on-main vs draft-branch-then-PR (Keystatic supports both) | Client + us | week 2 (after first training session) |

## 19. Living document

Every PR that introduces a new convention updates this doc in the same commit. If you're tempted to write a comment in code that explains a project-wide pattern, the explanation belongs here instead — link to the section from the code if you must, but keep the patterns centralized.

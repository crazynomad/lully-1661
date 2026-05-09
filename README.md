# lully-1661

Website for **Lully 1661** — a bakery in Lisboa.

## Stack

Next.js 15 (App Router) · TypeScript · Tailwind CSS v4 · next-intl (PT/EN) · Keystatic CMS · Biome · pnpm · Vercel.

See `docs/platform-recommendation-v2.md` and `docs/architecture.md` for the full rationale and codebase contract.

## Prerequisites

- Node 20+ (project tested on 24)
- pnpm 10+
- For local content editing: nothing extra — Keystatic runs in filesystem mode in dev
- For production deploys: Keystatic Cloud GitHub App + Vercel project

## Setup

```bash
pnpm install
cp env.example .env.local       # fill in only what you need locally
pnpm dev                        # starts at http://localhost:3000
```

Default routes after first start:

- `/` — redirects to `/pt` (default locale)
- `/pt` and `/en` — home page
- `/keystatic` — embedded CMS admin (filesystem-backed in dev)

## Scripts

```bash
pnpm dev          # local dev server
pnpm build        # production build (verifies typecheck + lint internally too)
pnpm start        # serve the production build
pnpm typecheck    # tsc --noEmit
pnpm lint         # biome check (replaces ESLint + Prettier)
pnpm lint:fix     # auto-fix lint + format issues
pnpm format       # biome formatter only
pnpm test         # vitest run
pnpm test:e2e     # playwright (none configured yet)
```

## Project layout

```
app/[locale]/...           Locale-aware routes (pt, en)
app/keystatic/...          Embedded CMS admin (separate layout)
app/api/keystatic/...      Keystatic route handler
features/<name>/           Domain modules — public API in index.ts only
components/                Cross-feature primitives (Container, Button, JsonLd, …)
lib/i18n/                  next-intl routing + middleware glue
lib/jsonld/                Per-schema-type JSON-LD helpers
lib/keystatic/             Reader API client
lib/seo.ts                 Per-page Metadata helper (canonical + hreflang)
lib/fonts.ts               Self-hosted webfonts via next/font
messages/{pt,en}.json      UI chrome strings (not CMS-driven content)
content/                   Keystatic content (MD/MDX/YAML, git-tracked)
keystatic.config.ts        CMS schema (TypeScript)
docs/                      Planning + architecture documents
```

The architecture conventions live in `docs/architecture.md` — read it before adding a new feature folder or changing a project-wide pattern.

## Deploy

Vercel auto-deploys `main`. Preview URLs are created per PR.

Required environment variables in Vercel (production):
- `NEXT_PUBLIC_SITE_URL`
- `NEXT_PUBLIC_KEYSTATIC_GITHUB_APP_SLUG`
- `KEYSTATIC_GITHUB_CLIENT_ID`
- `KEYSTATIC_GITHUB_CLIENT_SECRET`
- `KEYSTATIC_SECRET`
- (form/newsletter/analytics keys per `env.example` as features come online)

Without the Keystatic env vars, the admin still works in filesystem-fallback mode but cannot persist edits to GitHub. CI builds run in fallback mode by design — see the workflow.

## Status

This is the v1 brochure-first scaffold (no commerce). Phase-2 commerce will land via Shopify Storefront API behind the same Next.js front-end — see `docs/platform-recommendation-v2.md` § Phase 2 and `docs/architecture.md` § 17.

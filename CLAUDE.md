# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

Bilingual (PT/EN) brochure-first website for **Lully 1661**, a Lisbon bakery. Next.js 15 App Router + TypeScript + Tailwind v4 + next-intl + Keystatic CMS, deployed on Vercel. **v1 is no-commerce by design** — commerce is a planned phase-2 drop-in, and many architectural rules exist to keep that drop-in cheap.

The canonical contract for this codebase is `docs/architecture.md`. Read it before adding a new feature folder, route, or project-wide pattern. Per § 19, **a PR that introduces a new convention updates that doc in the same commit.**

### Repo scope (what is NOT here)

Sales analytics was carved out of this repo on 2026-05-14 — the data pipeline, weekly reports, channel trend analysis, and the `/sync-sales` slash command now live in **`greentrainpodcast/lully-analytics`** (private). If the user asks about ZSBMS extracts, sales canonical CSV, weekly dashboard, Glovo/UberEats/in-store channel splits, or anything under `raw-requirements/data/zsbms-extract/`, that's the other repo — don't try to reproduce it here.

What remains in `scripts/` is **website-only**: `build-{brunch,menu,store}-placeholders.mjs` (content seeding), `build-sow-{html,xlsx}.py` (SOW generators), `build-client-doc{,-round2}.py` (legacy client docs). See commit `868915a` for the full inventory.

## Commands

```bash
pnpm dev          # http://localhost:3000  (Keystatic at /keystatic, filesystem-backed)
pnpm build        # production build
pnpm start        # serve the production build
pnpm typecheck    # tsc --noEmit
pnpm lint         # biome check . (replaces ESLint + Prettier)
pnpm lint:fix     # auto-fix lint + format
pnpm format       # biome format --write
pnpm test         # vitest run (one-shot)
pnpm test:watch   # vitest watch
pnpm test:e2e     # playwright (not configured yet)
```

Run a single Vitest file: `pnpm vitest run path/to/file.test.ts`. Run by name: `pnpm vitest run -t "name fragment"`.

Node 20+ required (project tested on 24). pnpm 10+.

## Big-picture architecture

### Routing & i18n

- All public routes live under `app/[locale]/...`. Locale is **always prefixed** (`/pt/...`, `/en/...`); `/` 308-redirects to `/pt`. Don't introduce `localePrefix: 'as-needed'`.
- The single source of truth for per-locale paths is `lib/i18n/routing.ts` (next-intl `pathnames`). PT segments differ from EN segments (`/sobre` ↔ `/about`, `/lojas` ↔ `/stores`, etc.). Language-switching preserves the current page by mapping through this table — that's why **`<LocalizedLink>` exists and raw `next/link` is wrong** for in-app navigation.
- Slugs are **per-locale**: content entries carry both `slugPt` and `slugEn` and `generateStaticParams` emits both. Routes outside `app/[locale]/...` (Keystatic admin, sitemap, robots, API, static files) are excluded by `middleware.ts`'s matcher.

### Content (Keystatic)

- Schema is `keystatic.config.ts` at the repo root. Content lives in `content/` as YAML/MDX/images, all git-tracked.
- **Bilingual pattern:** every user-facing string uses a nested `fields.object({ pt, en })` (the `localizedString` helper). Both PT and EN are required — no half-translated entries.
- Reads go through `lib/keystatic/reader.ts` (`createReader`, fully typed, no codegen). Feature-level helpers live in `features/<name>/queries.ts` / `data.ts` — **pages never call the Reader directly.**
- Admin is embedded at `/keystatic`. Locally it runs in filesystem mode (writes to `content/`); in production it runs in `github` mode and Keystatic Cloud commits to GitHub. CI builds run in fallback mode by design — missing Keystatic env vars should not break the build.

### Feature folder rule (load-bearing)

Domain code lives in `features/<name>/` and the public API is **only** `features/<name>/index.ts`:

- Pages under `app/[locale]/...` import from `@/features/<name>` (the index), never from inside it.
- **A feature does not import another feature.** If two features share data, the shared piece moves to `lib/` (or a third feature). Cross-feature imports are a smell that the boundary is wrong.
- `components/` is for **domain-free** primitives (`Button`, `Container`, `JsonLd`, `LocalizedLink`). Anything with domain meaning (`ProductCard`, `StoreCard`) lives inside its feature folder.

The aspirational shape per `architecture.md` § 3 is `index.ts / schemas.ts / queries.ts / data.ts / components/ / jsonld.ts / tests/`. Most feature folders today only contain `index.ts + data.ts` — that's fine; grow them into the full shape as needed.

### Rendering & caching

- **All content pages are statically generated at build.** Use `generateStaticParams` for dynamic segments. **No ISR**, no `revalidate`, no `revalidateTag`, no `/api/revalidate` route. Content change = git commit = build = deploy.
- Server actions (forms) are uncached and dispatch via Resend.
- Don't reach for streaming SSR, PPR, or Server Component caching tricks in v1.

### SEO & JSON-LD

- Every page exports `generateMetadata` via the `seo()` helper in `lib/seo.ts` (canonical + hreflang for PT, EN, and `x-default` → PT).
- One JSON-LD helper per schema type in `lib/jsonld/`; feature folders compose them in `features/<name>/jsonld.ts` and render via `<JsonLd>`. Multiple types on one page → single `@graph`, not separate script tags.
- No raw `<img>` anywhere. All images go through `next/image` with explicit width/height and `sizes`; `alt` text comes from the Keystatic entry (also bilingual).

### Path aliases

Always use aliases, never `../../..`:

```
@/*           → ./*
@/features/*  → features/*
@/components/* → components/*
@/lib/*       → lib/*
@/content/*   → content/*
```

## Code style (Biome)

`biome check .` is the single linter+formatter — there is no ESLint or Prettier.

- Single quotes in JS, double quotes in JSX, semicolons always, trailing commas always, 2-space indent, 100-col lines.
- `noExplicitAny: error`, `noUnusedVariables: error`, `noUnusedImports: error`, `useImportType: error` (use `import type { … }` for type-only imports).
- `noConsole: warn` (only `console.warn`/`console.error` allowed).
- TS is strict with `noUncheckedIndexedAccess`, `noUnusedLocals`, `noUnusedParameters`, `noImplicitOverride`. Array/object index access returns `T | undefined` — handle it.
- Biome ignores `docs/`, `raw-requirements/`, `scripts/`, `content/`, `.keystatic/`, and build outputs. Don't be surprised when lint doesn't touch those.

## Definition of Done for a new page

Per `architecture.md` § 16 — when adding a route, ensure: `generateMetadata` set, hreflang correct, JSON-LD helper + `<JsonLd>` rendered, all images via `next/image` with `alt` from Keystatic, page appears in `app/sitemap.ts`, both `messages/pt.json` and `messages/en.json` updated (or content sourced from Keystatic), Lighthouse Performance ≥ 90 / Accessibility ≥ 95 / SEO ≥ 95.

## Phase-2 commerce guardrails

A handful of v1 decisions exist so phase-2 commerce ships as one new feature folder rather than a refactor (`architecture.md` § 17). When in doubt: don't lock layouts that need a future cart slot, don't tile the `product` schema in ways that conflict with a future `Product` JSON-LD, keep the menu detail page CTA swappable.

## Memory & current state

Per project memory: v1 pivoted from Shopify to Next.js on 2026-05-09 — `docs/platform-recommendation.md` is superseded by `docs/platform-recommendation-v2.md` and `docs/architecture.md`. If you find references to commerce/Shopify in v1 code, that's wrong and should be removed or deferred to phase 2.

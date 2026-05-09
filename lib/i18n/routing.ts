import { defineRouting } from 'next-intl/routing';

export const routing = defineRouting({
  locales: ['pt', 'en'] as const,
  defaultLocale: 'pt',
  // Always prefix the URL with the locale ('pt' included), per architecture.md § 5.1 —
  // unambiguous canonicals beat the pretty-URL ergonomics of 'as-needed'.
  localePrefix: 'always',
  // Per-locale pathnames per architecture.md § 5.2. Top-level segments differ
  // between PT and EN; dynamic segments inside (slugs) come from per-locale slug
  // fields in the Keystatic content model.
  pathnames: {
    '/': '/',
    '/sobre': { pt: '/sobre', en: '/about' },
    '/menu': { pt: '/menu', en: '/menu' },
    '/menu/[category]': { pt: '/menu/[category]', en: '/menu/[category]' },
    '/menu/[category]/[slug]': { pt: '/menu/[category]/[slug]', en: '/menu/[category]/[slug]' },
    '/menu/brunch': { pt: '/menu/brunch', en: '/menu/brunch' },
    '/diario': { pt: '/diario', en: '/journal' },
    '/diario/[slug]': { pt: '/diario/[slug]', en: '/journal/[slug]' },
    '/encomendas': { pt: '/encomendas', en: '/festive-orders' },
    '/reservas': { pt: '/reservas', en: '/reservations' },
    '/lully-inside': '/lully-inside',
    '/lojas': { pt: '/lojas', en: '/stores' },
    '/lojas/[slug]': { pt: '/lojas/[slug]', en: '/stores/[slug]' },
    '/trabalha-connosco': { pt: '/trabalha-connosco', en: '/careers' },
    '/legal': '/legal',
  },
});

export type Locale = (typeof routing.locales)[number];

export function isLocale(value: string | undefined): value is Locale {
  return value !== undefined && (routing.locales as readonly string[]).includes(value);
}

// `/diario` is the ASCII fallback for the planned `/diário` (UTF-8) PT slug.
// Decision pending — see `docs/architecture.md` § 18 "Open decisions".

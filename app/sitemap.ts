import { type Locale, routing } from '@/lib/i18n/routing';
import type { MetadataRoute } from 'next';

const SITE_URL = process.env.NEXT_PUBLIC_SITE_URL ?? 'https://lully1661.com';

// Static top-level routes by canonical key. Each key resolves through
// `routing.pathnames` to its locale-specific path, so /sobre maps to
// `/en/about` (not `/en/sobre`) in the EN entry. Dynamic routes
// (per-store, per-product, per-journal-post) will be added when the
// Keystatic content is populated — at that point we read from the
// Reader and emit per-entry URLs alongside these.
const STATIC_KEYS: Array<{
  key: keyof typeof routing.pathnames;
  priority: number;
}> = [
  { key: '/', priority: 1.0 },
  { key: '/sobre', priority: 0.8 },
  { key: '/menu', priority: 0.9 },
  { key: '/menu/brunch', priority: 0.85 },
  { key: '/diario', priority: 0.7 },
  { key: '/encomendas', priority: 0.7 },
  { key: '/reservas', priority: 0.7 },
  { key: '/lojas', priority: 0.9 },
  { key: '/lully-inside', priority: 0.5 },
  { key: '/trabalha-connosco', priority: 0.5 },
  { key: '/legal', priority: 0.3 },
];

function resolvePath(key: keyof typeof routing.pathnames, locale: Locale): string {
  const value = routing.pathnames[key];
  return typeof value === 'string' ? value : value[locale];
}

export default function sitemap(): MetadataRoute.Sitemap {
  const entries: MetadataRoute.Sitemap = [];

  for (const { key, priority } of STATIC_KEYS) {
    for (const locale of routing.locales) {
      const path = resolvePath(key, locale);
      entries.push({
        url: `${SITE_URL}/${locale}${path === '/' ? '' : path}`,
        lastModified: new Date(),
        changeFrequency: 'weekly',
        priority,
      });
    }
  }

  return entries;
}

import { routing } from '@/lib/i18n/routing';
import type { MetadataRoute } from 'next';

const SITE_URL = process.env.NEXT_PUBLIC_SITE_URL ?? 'https://lully1661.com';

// Static top-level routes. Dynamic routes (per-store, per-product,
// per-journal-post) will be added when the Keystatic schema is populated
// in phase 3 — at that point we read from the Reader and emit per-entry URLs.
const STATIC_PATHS: Array<{ path: string; priority: number }> = [
  { path: '/', priority: 1.0 },
  { path: '/sobre', priority: 0.8 },
  { path: '/menu', priority: 0.9 },
  { path: '/menu/brunch', priority: 0.85 },
  { path: '/diario', priority: 0.7 },
  { path: '/encomendas', priority: 0.7 },
  { path: '/reservas', priority: 0.7 },
  { path: '/lojas', priority: 0.9 },
  { path: '/lully-inside', priority: 0.5 },
  { path: '/trabalha-connosco', priority: 0.5 },
  { path: '/legal', priority: 0.3 },
];

export default function sitemap(): MetadataRoute.Sitemap {
  const entries: MetadataRoute.Sitemap = [];

  for (const { path, priority } of STATIC_PATHS) {
    const localePaths = routing.locales.map((locale) => ({
      url: `${SITE_URL}/${locale}${path === '/' ? '' : path}`,
      lastModified: new Date(),
      changeFrequency: 'weekly' as const,
      priority,
    }));
    entries.push(...localePaths);
  }

  return entries;
}

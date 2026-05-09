import { type Locale, routing } from '@/lib/i18n/routing';
import type { Metadata } from 'next';

const SITE_URL = process.env.NEXT_PUBLIC_SITE_URL ?? 'https://lully1661.com';

export type SeoInput = {
  title: string;
  description: string;
  /** Path WITHOUT the locale prefix and WITHOUT a trailing slash. Example: '/menu/paes' */
  path: string;
  locale: Locale;
  ogImage?: string;
};

/**
 * Build per-page Metadata with canonical and hreflang alternates.
 * Per architecture.md § 6.1, every page must call this from generateMetadata.
 */
export function seo(input: SeoInput): Metadata {
  const canonical = `${SITE_URL}/${input.locale}${input.path === '/' ? '' : input.path}`;

  const languages: Record<string, string> = {};
  for (const loc of routing.locales) {
    languages[loc] = `${SITE_URL}/${loc}${input.path === '/' ? '' : input.path}`;
  }
  // x-default points to PT (the primary market) per architecture.md § 6.1.
  languages['x-default'] =
    `${SITE_URL}/${routing.defaultLocale}${input.path === '/' ? '' : input.path}`;

  return {
    title: input.title,
    description: input.description,
    alternates: {
      canonical,
      languages,
    },
    openGraph: {
      title: input.title,
      description: input.description,
      url: canonical,
      locale: input.locale,
      type: 'website',
      ...(input.ogImage ? { images: [{ url: input.ogImage }] } : {}),
    },
    twitter: {
      card: 'summary_large_image',
      title: input.title,
      description: input.description,
      ...(input.ogImage ? { images: [input.ogImage] } : {}),
    },
  };
}

export const SITE = { url: SITE_URL };

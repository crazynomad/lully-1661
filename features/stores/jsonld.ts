import { breadcrumbJsonLd } from '@/lib/jsonld/breadcrumb';
import { localBusinessJsonLd } from '@/lib/jsonld/localBusiness';
import type { Store, WeekdayKey } from './data';
import { weekdayToSchema } from './data';

const SITE_URL = process.env.NEXT_PUBLIC_SITE_URL ?? 'https://lully1661.com';

type StorePageJsonLdInput = {
  store: Store;
  /** Path WITHOUT locale prefix and without trailing slash. Example: '/lojas/anjos' */
  pathFromRoot: string;
  /** Locale segment used for breadcrumb display ('pt' | 'en'). */
  locale: 'pt' | 'en';
  /** Localized labels for breadcrumb ancestors. */
  labels: { home: string; stores: string };
};

/**
 * Combines LocalBusiness + Bakery + BreadcrumbList into a single @graph,
 * per architecture.md § 6.2 (one <JsonLd> per page, multiple types as graph).
 */
export function storePageJsonLd({ store, pathFromRoot, locale, labels }: StorePageJsonLdInput) {
  const url = `${SITE_URL}/${locale}${pathFromRoot}`;
  const heroUrl = `${SITE_URL}/content/store/${store.slug}/hero.jpg`;

  const business = localBusinessJsonLd({
    '@id': `${url}#store`,
    name: store.name,
    url,
    image: heroUrl,
    telephone: store.phone || undefined,
    priceRange: '€€',
    address: {
      streetAddress: store.address.streetAddress,
      addressLocality: store.address.addressLocality,
      postalCode: store.address.postalCode || undefined,
      addressCountry: store.address.addressCountry,
    },
    geo:
      store.geo.latitude && store.geo.longitude
        ? { latitude: store.geo.latitude, longitude: store.geo.longitude }
        : undefined,
    openingHours: store.openingHours.map((h) => ({
      dayOfWeek: weekdayToSchema(h.weekday as WeekdayKey),
      opens: h.opens,
      closes: h.closes,
    })),
    servesCuisine: ['French', 'Bakery'],
    sameAs: ['https://www.instagram.com/lully1661_lisboa/'],
  });

  const breadcrumb = breadcrumbJsonLd([
    { name: labels.home, url: `${SITE_URL}/${locale}` },
    {
      name: labels.stores,
      url: `${SITE_URL}/${locale}${pathFromRoot.split('/').slice(0, -1).join('/')}`,
    },
    { name: store.name, url },
  ]);

  return {
    '@context': 'https://schema.org',
    '@graph': [
      // Strip the @context from each member since we set it on the wrapper.
      stripContext(business),
      stripContext(breadcrumb),
    ],
  };
}

function stripContext<T extends { '@context'?: unknown }>(obj: T): Omit<T, '@context'> {
  const { '@context': _ignored, ...rest } = obj;
  return rest;
}

// schema.org Bakery + LocalBusiness — emitted per per-store URL.
// Each store has a unique @id; NAP must match the visible page text and
// the store's Google Business Profile (architecture.md § 6.4).
// https://schema.org/Bakery   https://schema.org/LocalBusiness

type OpeningHours = {
  dayOfWeek: 'Monday' | 'Tuesday' | 'Wednesday' | 'Thursday' | 'Friday' | 'Saturday' | 'Sunday';
  opens: string; // 'HH:MM'
  closes: string;
};

type LocalBusinessInput = {
  '@id': string;
  name: string;
  url: string;
  image?: string;
  telephone?: string;
  priceRange?: string;
  address: {
    streetAddress: string;
    addressLocality: string;
    postalCode?: string;
    addressCountry: string;
  };
  geo?: { latitude: number; longitude: number };
  openingHours?: OpeningHours[];
  servesCuisine?: string[];
  sameAs?: string[];
};

export function localBusinessJsonLd(input: LocalBusinessInput) {
  return {
    '@context': 'https://schema.org',
    '@type': ['Bakery', 'LocalBusiness'],
    '@id': input['@id'],
    name: input.name,
    url: input.url,
    ...(input.image ? { image: input.image } : {}),
    ...(input.telephone ? { telephone: input.telephone } : {}),
    ...(input.priceRange ? { priceRange: input.priceRange } : {}),
    address: { '@type': 'PostalAddress', ...input.address },
    ...(input.geo
      ? {
          geo: {
            '@type': 'GeoCoordinates',
            latitude: input.geo.latitude,
            longitude: input.geo.longitude,
          },
        }
      : {}),
    ...(input.openingHours && input.openingHours.length > 0
      ? {
          openingHoursSpecification: input.openingHours.map((h) => ({
            '@type': 'OpeningHoursSpecification',
            dayOfWeek: `https://schema.org/${h.dayOfWeek}`,
            opens: h.opens,
            closes: h.closes,
          })),
        }
      : {}),
    ...(input.servesCuisine && input.servesCuisine.length > 0
      ? { servesCuisine: input.servesCuisine }
      : {}),
    ...(input.sameAs && input.sameAs.length > 0 ? { sameAs: input.sameAs } : {}),
  };
}

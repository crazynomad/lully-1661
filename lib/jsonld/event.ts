// schema.org Event — emitted for guest-chef luncheons, brunch launches,
// catering events on /encomendas. https://schema.org/Event

type EventInput = {
  name: string;
  description?: string;
  startDate: string; // ISO 8601
  endDate?: string;
  image?: string;
  locationName: string;
  locationAddress?: {
    streetAddress: string;
    addressLocality: string;
    addressCountry: string;
  };
  url?: string;
};

export function eventJsonLd(input: EventInput) {
  return {
    '@context': 'https://schema.org',
    '@type': 'Event',
    name: input.name,
    ...(input.description ? { description: input.description } : {}),
    startDate: input.startDate,
    ...(input.endDate ? { endDate: input.endDate } : {}),
    ...(input.image ? { image: input.image } : {}),
    location: {
      '@type': 'Place',
      name: input.locationName,
      ...(input.locationAddress
        ? { address: { '@type': 'PostalAddress', ...input.locationAddress } }
        : {}),
    },
    ...(input.url ? { url: input.url } : {}),
  };
}

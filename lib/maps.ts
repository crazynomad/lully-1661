// Cross-platform "Get directions" URL builder.
//
// We always emit the canonical Google Maps universal URL. Apple iOS
// and Android both intercept this URL to launch the installed Google
// Maps app when present, falling back to the mobile web view otherwise
// — so a single href works for desktop click, iOS, and Android with
// no user-agent sniffing on our side.
//
// Per architecture.md § frontend-stack-table — we deliberately avoid
// proprietary URI schemes (geo:, maps://, comgooglemaps://) for the
// demo because they're brittle: an iOS user without Google Maps
// installed gets a "no app can open this URL" prompt for `comgoogle…`.
// The universal URL is the boring, correct default.

type Coords = { latitude: number; longitude: number };

type Address = {
  streetAddress: string;
  postalCode?: string;
  addressLocality: string;
  addressCountry: string;
};

/**
 * "Directions to" URL — preferred for store pages.
 * Uses Google Maps' /dir/?api=1&destination=… deep-link, which:
 *  - opens the Google Maps app on iOS/Android if installed
 *  - falls back to maps.google.com in any browser
 *  - prefers lat/long when available (more reliable than address text)
 */
export function directionsUrl({
  geo,
  address,
}: {
  geo?: Coords;
  address: Address;
}): string {
  const destination = geo
    ? `${geo.latitude},${geo.longitude}`
    : `${address.streetAddress}, ${address.postalCode ?? ''} ${address.addressLocality}, ${address.addressCountry}`;
  const params = new URLSearchParams({
    api: '1',
    destination,
  });
  return `https://www.google.com/maps/dir/?api=1&${params.toString()}`;
}

/**
 * Embed URL for the iframe-based map preview on per-store pages.
 * Uses the public /maps/embed/v1 endpoint — requires no API key for
 * the basic place view, but a key restricted to the production domain
 * is recommended for production (see env.example/GOOGLE_MAPS_EMBED_KEY).
 */
export function embedUrl({
  geo,
  address,
  zoom = 16,
}: {
  geo?: Coords;
  address: Address;
  zoom?: number;
}): string {
  const q = geo
    ? `${geo.latitude},${geo.longitude}`
    : `${address.streetAddress}, ${address.postalCode ?? ''} ${address.addressLocality}, ${address.addressCountry}`;
  // The keyless embed via iframe `q=` works for demo. For production
  // swap to the keyed `https://www.google.com/maps/embed/v1/place` API.
  const params = new URLSearchParams({ q, z: String(zoom), output: 'embed' });
  return `https://maps.google.com/maps?${params.toString()}`;
}

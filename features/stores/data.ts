import { reader } from '@/lib/keystatic/reader';
import type { Locale } from '@/lib/i18n/routing';

// Public read API for the stores feature. Pages outside this feature
// fold call only what's re-exported from index.ts — see architecture.md § 3.

export type WeekdayKey =
  | 'monday'
  | 'tuesday'
  | 'wednesday'
  | 'thursday'
  | 'friday'
  | 'saturday'
  | 'sunday';

export type StoreServiceKey =
  | 'dineIn'
  | 'brunch'
  | 'pickup'
  | 'ovenVisible'
  | 'parking'
  | 'wheelchair';

export type Store = NonNullable<Awaited<ReturnType<typeof reader.collections.store.read>>>;

export async function listStoreSlugs(): Promise<string[]> {
  return reader.collections.store.list();
}

export async function getStore(slug: string): Promise<Store | null> {
  return reader.collections.store.read(slug);
}

export async function getAllStores(): Promise<Array<{ slug: string; entry: Store }>> {
  const slugs = await listStoreSlugs();
  const entries = await Promise.all(
    slugs.map(async (slug) => {
      const entry = await getStore(slug);
      return entry ? { slug, entry } : null;
    }),
  );
  return entries.filter((e): e is { slug: string; entry: Store } => e !== null);
}

export async function getMenuItemsAvailableAt(storeSlug: string) {
  const items = await reader.collections.weeklyMenuItem.all();
  return items
    .filter((item) => item.entry.availableAt.includes(storeSlug))
    .map((item) => ({
      slug: item.slug,
      entry: item.entry,
    }));
}

// The store hero JPG is committed to public/content/store/<slug>/hero.jpg.
// Keystatic's image-field plumbing is wired but we don't yet rely on it
// at runtime — production photography will replace these placeholders and
// the proper Reader image resolution can be wired then. Documented as a
// known demo simplification.
export function storeHeroImagePath(slug: string): string {
  return `/content/store/${slug}/hero.jpg`;
}

// Locale-aware atmosphere accessor.
export function atmosphereFor(store: Store, locale: Locale): string {
  return store.atmosphere[locale];
}

// Schema.org weekday name from our internal weekday key.
const WEEKDAY_TO_SCHEMA: Record<WeekdayKey, 'Monday' | 'Tuesday' | 'Wednesday' | 'Thursday' | 'Friday' | 'Saturday' | 'Sunday'> = {
  monday: 'Monday',
  tuesday: 'Tuesday',
  wednesday: 'Wednesday',
  thursday: 'Thursday',
  friday: 'Friday',
  saturday: 'Saturday',
  sunday: 'Sunday',
};

export function weekdayToSchema(key: WeekdayKey) {
  return WEEKDAY_TO_SCHEMA[key];
}

// Stores feature — public API. Pages outside this folder import only
// from this index per architecture.md § 3.

export {
  type Store,
  type WeekdayKey,
  type StoreServiceKey,
  listStoreSlugs,
  getStore,
  getAllStores,
  getMenuItemsAvailableAt,
  storeHeroImagePath,
  atmosphereFor,
  weekdayToSchema,
} from './data';

export { storePageJsonLd } from './jsonld';

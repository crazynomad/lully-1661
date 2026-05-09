import { collection, config, fields, singleton } from '@keystatic/core';

// =============================================================================
// Storage gating
// =============================================================================
// Use GitHub storage only when Keystatic Cloud env vars are all set.
// Otherwise fall back to local filesystem mode so dev and CI builds don't
// fail on missing secrets. Per `docs/architecture.md` § 4.5.

const hasGithubAuth =
  Boolean(process.env.KEYSTATIC_GITHUB_CLIENT_ID) &&
  Boolean(process.env.KEYSTATIC_GITHUB_CLIENT_SECRET) &&
  Boolean(process.env.KEYSTATIC_SECRET);

// =============================================================================
// Bilingual field helpers
// =============================================================================
// Every user-facing string field uses `fields.object({ pt, en })`. Editors
// see PT and EN stacked in a single panel per field. Both are required —
// the half-translated state is forbidden by validation.
// Per `docs/architecture.md` § 4.1.

const localizedString = (label: string, opts?: { description?: string }) =>
  fields.object(
    {
      pt: fields.text({
        label: 'PT',
        validation: { length: { min: 1 } },
      }),
      en: fields.text({
        label: 'EN',
        validation: { length: { min: 1 } },
      }),
    },
    {
      label,
      ...(opts?.description ? { description: opts.description } : {}),
    },
  );

const localizedText = (label: string, opts?: { description?: string }) =>
  fields.object(
    {
      pt: fields.text({
        label: 'PT',
        multiline: true,
        validation: { length: { min: 1 } },
      }),
      en: fields.text({
        label: 'EN',
        multiline: true,
        validation: { length: { min: 1 } },
      }),
    },
    {
      label,
      ...(opts?.description ? { description: opts.description } : {}),
    },
  );

// Per-locale slugs as a paired object — distinct from `fields.slug`, which
// names the on-disk directory. Routing chooses the matching localized slug
// from the URL segment.
const localizedSlug = (label: string) =>
  fields.object(
    {
      pt: fields.text({
        label: 'PT slug',
        validation: { length: { min: 1 } },
      }),
      en: fields.text({
        label: 'EN slug',
        validation: { length: { min: 1 } },
      }),
    },
    { label },
  );

// Image with required alt text (per architecture.md § 11). Decorative
// images opt out by setting `decorative: true`.
const imageWithAlt = (params: { label: string; directory: string; publicPath: string }) =>
  fields.object(
    {
      file: fields.image({
        label: 'Image',
        directory: params.directory,
        publicPath: params.publicPath,
        validation: { isRequired: true },
      }),
      alt: fields.object(
        {
          pt: fields.text({ label: 'Alt PT' }),
          en: fields.text({ label: 'Alt EN' }),
        },
        { label: 'Alt text (PT/EN)' },
      ),
      decorative: fields.checkbox({
        label: 'Decorative — alt text intentionally empty',
        defaultValue: false,
      }),
    },
    { label: params.label },
  );

// =============================================================================
// Shared sub-schemas
// =============================================================================

const weekdayOptions = [
  { value: 'monday', label: 'Monday' },
  { value: 'tuesday', label: 'Tuesday' },
  { value: 'wednesday', label: 'Wednesday' },
  { value: 'thursday', label: 'Thursday' },
  { value: 'friday', label: 'Friday' },
  { value: 'saturday', label: 'Saturday' },
  { value: 'sunday', label: 'Sunday' },
] as const;

const allergenOptions = [
  { value: 'gluten', label: 'Gluten' },
  { value: 'dairy', label: 'Dairy' },
  { value: 'eggs', label: 'Eggs' },
  { value: 'nuts', label: 'Nuts' },
  { value: 'peanuts', label: 'Peanuts' },
  { value: 'soy', label: 'Soy' },
  { value: 'sesame', label: 'Sesame' },
  { value: 'sulphites', label: 'Sulphites' },
] as const;

const dietOptions = [
  { value: 'vegan', label: 'Vegan' },
  { value: 'vegetarian', label: 'Vegetarian' },
  { value: 'glutenFree', label: 'Gluten-free' },
  { value: 'organic', label: 'Organic' },
] as const;

const storeServiceOptions = [
  { value: 'dineIn', label: 'Dine-in' },
  { value: 'brunch', label: 'Brunch' },
  { value: 'pickup', label: 'Pickup' },
  { value: 'ovenVisible', label: 'Visible oven' },
  { value: 'parking', label: 'Parking nearby' },
  { value: 'wheelchair', label: 'Wheelchair access' },
] as const;

// =============================================================================
// Singletons
// =============================================================================

const homepage = singleton({
  label: 'Homepage',
  path: 'content/homepage',
  format: { data: 'yaml' },
  schema: {
    heroLine: localizedString('Hero line'),
    heroSubline: localizedText('Hero subline', { description: 'Optional — under the wordmark.' }),
    featuredItems: fields.array(
      fields.relationship({
        label: 'Featured weekly item',
        collection: 'weeklyMenuItem',
      }),
      {
        label: 'Featured items (this week at lully)',
        itemLabel: (props) => props.value ?? '—',
      },
    ),
    journalTeaserPost: fields.relationship({
      label: 'Journal teaser post',
      collection: 'journalPost',
      description: 'The journal post shown on the home page. Defaults to the most recent.',
    }),
    seoOverride: fields.object(
      {
        title: fields.object({
          pt: fields.text({ label: 'PT title' }),
          en: fields.text({ label: 'EN title' }),
        }),
        description: fields.object({
          pt: fields.text({ label: 'PT description', multiline: true }),
          en: fields.text({ label: 'EN description', multiline: true }),
        }),
      },
      {
        label: 'SEO override',
        description: 'Optional — overrides the default site title/description for the home page.',
      },
    ),
  },
});

const aboutPage = singleton({
  label: 'About page',
  path: 'content/aboutPage',
  format: { data: 'yaml' },
  schema: {
    heroLine: localizedString('Hero line'),
    bodyPt: fields.document({
      label: 'Body — PT',
      formatting: true,
      dividers: true,
      links: true,
      images: {
        directory: 'public/content/aboutPage',
        publicPath: '/content/aboutPage/',
      },
    }),
    bodyEn: fields.document({
      label: 'Body — EN',
      formatting: true,
      dividers: true,
      links: true,
      images: {
        directory: 'public/content/aboutPage',
        publicPath: '/content/aboutPage/',
      },
    }),
    philosophyPoints: fields.array(
      fields.object({
        title: localizedString('Title'),
        body: localizedText('Body'),
      }),
      {
        label: 'Philosophy points',
        description:
          'Short editorial blocks below the main story (e.g. flour, fermentation, oven).',
        itemLabel: (props) => props.fields.title.fields.pt.value || '—',
      },
    ),
    team: fields.array(
      fields.object({
        name: fields.text({ label: 'Name' }),
        role: localizedString('Role'),
        bio: localizedText('Bio'),
        photo: imageWithAlt({
          label: 'Photo',
          directory: 'public/content/aboutPage/team',
          publicPath: '/content/aboutPage/team/',
        }),
      }),
      {
        label: 'Team',
        description: 'Optional — only displayed if the client supplies portraits.',
        itemLabel: (props) => props.fields.name.value || '—',
      },
    ),
  },
});

// =============================================================================
// Collections
// =============================================================================

const productCategory = collection({
  label: 'Product categories',
  slugField: 'slug',
  path: 'content/productCategory/*',
  format: { data: 'yaml' },
  columns: ['slug'],
  schema: {
    slug: fields.slug({
      name: { label: 'Slug (filesystem name)' },
    }),
    name: localizedString('Name'),
    localizedSlug: localizedSlug('URL slug (PT/EN)'),
    description: localizedText('Description'),
    illustration: imageWithAlt({
      label: 'Baroque sub-mark illustration',
      directory: 'public/content/productCategory',
      publicPath: '/content/productCategory/',
    }),
  },
});

const store = collection({
  label: 'Stores',
  slugField: 'slug',
  path: 'content/store/*',
  format: { data: 'yaml' },
  columns: ['slug'],
  schema: {
    slug: fields.slug({
      name: {
        label: 'Slug',
        description: 'Used as the URL segment: /lojas/<slug> and /stores/<slug>.',
      },
    }),
    name: fields.text({
      label: 'Name',
      description: 'Public name of this outlet (e.g., "Lully 1661 — Anjos").',
      validation: { length: { min: 1 } },
    }),
    neighborhood: fields.text({
      label: 'Neighborhood',
      description: 'For UI labels and SEO meta.',
      validation: { length: { min: 1 } },
    }),
    address: fields.object(
      {
        streetAddress: fields.text({ label: 'Street address' }),
        addressLocality: fields.text({ label: 'City', defaultValue: 'Lisboa' }),
        postalCode: fields.text({ label: 'Postal code' }),
        addressCountry: fields.text({ label: 'Country code', defaultValue: 'PT' }),
      },
      { label: 'Address' },
    ),
    geo: fields.object(
      {
        latitude: fields.number({ label: 'Latitude', validation: { isRequired: true } }),
        longitude: fields.number({ label: 'Longitude', validation: { isRequired: true } }),
      },
      {
        label: 'Geo coordinates',
        description: 'Used by LocalBusiness JSON-LD and the Google Maps embed.',
      },
    ),
    phone: fields.text({ label: 'Phone (E.164, e.g. +351...)' }),
    openingHours: fields.array(
      fields.object({
        weekday: fields.select({
          label: 'Weekday',
          options: weekdayOptions,
          defaultValue: 'tuesday',
        }),
        opens: fields.text({ label: 'Opens (HH:MM)' }),
        closes: fields.text({ label: 'Closes (HH:MM)' }),
      }),
      {
        label: 'Opening hours',
        itemLabel: (props) =>
          `${props.fields.weekday.value} ${props.fields.opens.value}–${props.fields.closes.value}`,
      },
    ),
    photo: imageWithAlt({
      label: 'Hero photo',
      directory: 'public/content/store',
      publicPath: '/content/store/',
    }),
    atmosphere: localizedText('Atmosphere copy'),
    services: fields.multiselect({
      label: 'Services at this store',
      options: storeServiceOptions,
    }),
    theForkUrl: fields.url({
      label: 'The Fork URL',
      description: 'Optional — only set when reservations are live for this store.',
    }),
    // Phase-2 readiness fields per architecture.md § 17 — present in the
    // schema but unused in v1. Adding them now is non-breaking; removing
    // them later would be.
    pickupCutoff: fields.text({
      label: 'Pickup cutoff (HH:MM)',
      description: 'Phase-2 commerce field — leave blank in v1.',
    }),
  },
});

const product = collection({
  label: 'Products (permanent catalogue)',
  slugField: 'slug',
  path: 'content/product/*',
  format: { data: 'yaml' },
  columns: ['slug', 'category'],
  schema: {
    slug: fields.slug({
      name: { label: 'Slug (filesystem name)' },
    }),
    name: localizedString('Name'),
    localizedSlug: localizedSlug('URL slug (PT/EN)'),
    description: localizedText('Description'),
    category: fields.relationship({
      label: 'Category',
      collection: 'productCategory',
    }),
    image: imageWithAlt({
      label: 'Image',
      directory: 'public/content/product',
      publicPath: '/content/product/',
    }),
    allergens: fields.multiselect({
      label: 'Allergens',
      options: allergenOptions,
    }),
    suitableForDiet: fields.multiselect({
      label: 'Suitable for diet',
      options: dietOptions,
    }),
    availableAt: fields.array(
      fields.relationship({
        label: 'Store',
        collection: 'store',
      }),
      {
        label: 'Available at stores',
        itemLabel: (props) => props.value ?? '—',
      },
    ),
    pairsWith: fields.array(
      fields.relationship({
        label: 'Product',
        collection: 'product',
      }),
      {
        label: '"Pairs well with" cross-sell',
        itemLabel: (props) => props.value ?? '—',
      },
    ),
    // Phase-2 commerce stubs — see architecture.md § 17.
    // sku: fields.text({ label: 'SKU' }),
    // price: fields.number({ label: 'Price (cents)' }),
    // currency: fields.text({ label: 'Currency', defaultValue: 'EUR' }),
    // availableForSale: fields.checkbox({ label: 'Available for sale' }),
  },
});

const weeklyMenuItem = collection({
  label: 'Weekly menu items',
  slugField: 'slug',
  path: 'content/weeklyMenuItem/*',
  format: { data: 'yaml' },
  columns: ['slug', 'weekOf', 'featured'],
  schema: {
    slug: fields.slug({
      name: {
        label: 'Slug (filesystem name)',
        description: 'Suggested format: <yyyy-Www-name> e.g. 2026-W19-pao-rustico.',
      },
    }),
    name: localizedString('Name'),
    localizedSlug: localizedSlug('URL slug (PT/EN)'),
    description: localizedText('Description'),
    category: fields.relationship({
      label: 'Category',
      collection: 'productCategory',
    }),
    image: imageWithAlt({
      label: 'Image',
      directory: 'public/content/weeklyMenuItem',
      publicPath: '/content/weeklyMenuItem/',
    }),
    allergens: fields.multiselect({
      label: 'Allergens',
      options: allergenOptions,
    }),
    suitableForDiet: fields.multiselect({
      label: 'Suitable for diet',
      options: dietOptions,
    }),
    availableAt: fields.array(
      fields.relationship({
        label: 'Store',
        collection: 'store',
      }),
      {
        label: 'Available at stores',
        itemLabel: (props) => props.value ?? '—',
      },
    ),
    weekOf: fields.date({
      label: 'Week of',
      description: 'The Monday of the week this item is featured.',
      validation: { isRequired: true },
    }),
    featured: fields.checkbox({
      label: 'Featured on home page',
      defaultValue: false,
    }),
  },
});

const journalPost = collection({
  label: 'Journal posts',
  slugField: 'slug',
  path: 'content/journalPost/*',
  format: { contentField: 'bodyPt' },
  columns: ['slug', 'publishedAt', 'author'],
  schema: {
    slug: fields.slug({
      name: {
        label: 'Slug (filesystem name)',
        description: 'Suggested format: <yyyy-mm-dd-name>.',
      },
    }),
    title: localizedString('Title'),
    localizedSlug: localizedSlug('URL slug (PT/EN)'),
    excerpt: localizedText('Excerpt', {
      description: 'Short — used in cards and the home journal teaser.',
    }),
    heroImage: imageWithAlt({
      label: 'Hero image',
      directory: 'public/content/journalPost',
      publicPath: '/content/journalPost/',
    }),
    bodyPt: fields.document({
      label: 'Body — PT',
      formatting: true,
      dividers: true,
      links: true,
      images: {
        directory: 'public/content/journalPost',
        publicPath: '/content/journalPost/',
      },
    }),
    bodyEn: fields.document({
      label: 'Body — EN',
      formatting: true,
      dividers: true,
      links: true,
      images: {
        directory: 'public/content/journalPost',
        publicPath: '/content/journalPost/',
      },
    }),
    publishedAt: fields.date({
      label: 'Published at',
      validation: { isRequired: true },
    }),
    author: fields.text({
      label: 'Author',
      defaultValue: 'Lully 1661',
    }),
    tags: fields.array(fields.text({ label: 'Tag' }), {
      label: 'Tags',
      itemLabel: (props) => props.value || '—',
    }),
  },
});

const partner = collection({
  label: 'Partners (B2B)',
  slugField: 'slug',
  path: 'content/partner/*',
  format: { data: 'yaml' },
  columns: ['slug', 'sector'],
  schema: {
    slug: fields.slug({ name: { label: 'Slug' } }),
    name: fields.text({ label: 'Name', validation: { length: { min: 1 } } }),
    logo: imageWithAlt({
      label: 'Logo',
      directory: 'public/content/partner',
      publicPath: '/content/partner/',
    }),
    sector: fields.select({
      label: 'Sector',
      options: [
        { value: 'hotel', label: 'Hotel' },
        { value: 'restaurant', label: 'Restaurant' },
        { value: 'retail', label: 'Retail' },
        { value: 'event', label: 'Event' },
        { value: 'other', label: 'Other' },
      ],
      defaultValue: 'restaurant',
    }),
    testimonial: localizedText('Testimonial', {
      description: 'Optional 2-line quote — leave blank to show logo only.',
    }),
  },
});

const openPosition = collection({
  label: 'Open positions',
  slugField: 'slug',
  path: 'content/openPosition/*',
  format: { data: 'yaml' },
  columns: ['slug', 'department', 'employmentType'],
  schema: {
    slug: fields.slug({ name: { label: 'Slug' } }),
    title: localizedString('Title'),
    department: fields.select({
      label: 'Department',
      options: [
        { value: 'bakery', label: 'Bakery' },
        { value: 'pastry', label: 'Pastry' },
        { value: 'frontOfHouse', label: 'Front of house' },
        { value: 'kitchen', label: 'Kitchen' },
        { value: 'management', label: 'Management' },
        { value: 'other', label: 'Other' },
      ],
      defaultValue: 'bakery',
    }),
    store: fields.relationship({
      label: 'Store',
      collection: 'store',
      description: 'Which store this role is based at. Leave blank if cross-store.',
    }),
    employmentType: fields.select({
      label: 'Employment type',
      options: [
        { value: 'fullTime', label: 'Full-time' },
        { value: 'partTime', label: 'Part-time' },
        { value: 'temporary', label: 'Temporary' },
        { value: 'internship', label: 'Internship' },
      ],
      defaultValue: 'fullTime',
    }),
    description: fields.object(
      {
        pt: fields.document({
          label: 'PT',
          formatting: { listTypes: { unordered: true, ordered: true } },
        }),
        en: fields.document({
          label: 'EN',
          formatting: { listTypes: { unordered: true, ordered: true } },
        }),
      },
      { label: 'Description (PT/EN)' },
    ),
    applyEmail: fields.text({
      label: 'Apply email',
      description: 'Where applications are routed (e.g. hr@lully1661.com).',
    }),
    validThrough: fields.date({
      label: 'Listing valid through',
      description: 'Used by JobPosting JSON-LD. Hide the listing after this date.',
    }),
  },
});

const seasonalCampaign = collection({
  label: 'Seasonal campaigns',
  slugField: 'slug',
  path: 'content/seasonalCampaign/*',
  format: { data: 'yaml' },
  columns: ['slug', 'season', 'activeFrom'],
  schema: {
    slug: fields.slug({ name: { label: 'Slug' } }),
    name: localizedString('Campaign name'),
    season: fields.select({
      label: 'Season',
      options: [
        { value: 'easter', label: 'Easter' },
        { value: 'summer', label: 'Summer' },
        { value: 'backToSchool', label: 'Back to school' },
        { value: 'autumn', label: 'Autumn' },
        { value: 'christmas', label: 'Christmas' },
        { value: 'newYear', label: 'New year' },
        { value: 'valentines', label: 'Valentines' },
      ],
      defaultValue: 'easter',
    }),
    heroImage: imageWithAlt({
      label: 'Hero image',
      directory: 'public/content/seasonalCampaign',
      publicPath: '/content/seasonalCampaign/',
    }),
    description: localizedText('Description'),
    products: fields.array(
      fields.relationship({
        label: 'Product',
        collection: 'product',
      }),
      {
        label: 'Featured products',
        itemLabel: (props) => props.value ?? '—',
      },
    ),
    leadTimeDays: fields.number({
      label: 'Lead time (days)',
      description: 'Minimum advance notice for orders during this campaign.',
    }),
    enquiryEnabled: fields.checkbox({
      label: 'Show enquiry form',
      defaultValue: true,
    }),
    activeFrom: fields.date({ label: 'Active from' }),
    activeTo: fields.date({ label: 'Active to' }),
  },
});

const legalPage = collection({
  label: 'Legal pages',
  slugField: 'slug',
  path: 'content/legalPage/*',
  format: { contentField: 'bodyPt' },
  columns: ['slug', 'lastUpdated'],
  schema: {
    slug: fields.slug({
      name: {
        label: 'Slug',
        description: 'e.g. terms, privacy, cookies, complaints-book',
      },
    }),
    title: localizedString('Title'),
    bodyPt: fields.document({
      label: 'Body — PT',
      formatting: true,
      links: true,
    }),
    bodyEn: fields.document({
      label: 'Body — EN',
      formatting: true,
      links: true,
    }),
    lastUpdated: fields.date({
      label: 'Last updated',
      validation: { isRequired: true },
    }),
  },
});

// =============================================================================
// Config
// =============================================================================

export default config({
  storage: hasGithubAuth
    ? {
        kind: 'github',
        repo: {
          owner: process.env.NEXT_PUBLIC_KEYSTATIC_GITHUB_REPO_OWNER ?? 'crazynomad',
          name: process.env.NEXT_PUBLIC_KEYSTATIC_GITHUB_REPO_NAME ?? 'lully-1661',
        },
      }
    : { kind: 'local' },

  ui: {
    brand: { name: 'Lully 1661' },
    navigation: {
      'Owner-edited weekly': ['weeklyMenuItem', 'journalPost'],
      Stores: ['store'],
      Catalogue: ['product', 'productCategory'],
      'Pages (singletons)': ['homepage', 'aboutPage'],
      Operations: ['seasonalCampaign', 'partner', 'openPosition'],
      Legal: ['legalPage'],
    },
  },

  singletons: {
    homepage,
    aboutPage,
  },

  collections: {
    productCategory,
    store,
    product,
    weeklyMenuItem,
    journalPost,
    partner,
    openPosition,
    seasonalCampaign,
    legalPage,
  },
});

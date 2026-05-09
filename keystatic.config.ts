import { collection, config, fields } from '@keystatic/core';

// Phase 2c: minimal schema to verify the admin route works.
// Phase 3 replaces this with the full 11-collection schema per
// `docs/architecture.md` § 4.2.

// Use GitHub storage only when the auth env vars are set (Keystatic Cloud
// is provisioned). Otherwise fall back to local mode so dev and CI builds
// don't fail on missing secrets.
const hasGithubAuth =
  Boolean(process.env.KEYSTATIC_GITHUB_CLIENT_ID) &&
  Boolean(process.env.KEYSTATIC_GITHUB_CLIENT_SECRET) &&
  Boolean(process.env.KEYSTATIC_SECRET);

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
  },

  collections: {
    placeholder: collection({
      label: 'Placeholder (replaced in Phase 3)',
      slugField: 'name',
      path: 'content/placeholder/*',
      format: { contentField: 'note' },
      schema: {
        name: fields.slug({ name: { label: 'Name' } }),
        note: fields.markdoc({ label: 'Note' }),
      },
    }),
  },
});

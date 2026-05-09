// schema.org Organization — used on Home for the brand entity.
// https://schema.org/Organization

type OrganizationInput = {
  name: string;
  url: string;
  logo?: string;
  sameAs?: string[];
};

export function organizationJsonLd(input: OrganizationInput) {
  return {
    '@context': 'https://schema.org',
    '@type': 'Organization',
    name: input.name,
    url: input.url,
    ...(input.logo ? { logo: input.logo } : {}),
    ...(input.sameAs && input.sameAs.length > 0 ? { sameAs: input.sameAs } : {}),
  };
}

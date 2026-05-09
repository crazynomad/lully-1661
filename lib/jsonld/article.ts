// schema.org Article (BlogPosting) — emitted on /diario/[slug] journal posts.
// https://schema.org/Article   https://schema.org/BlogPosting

type ArticleInput = {
  headline: string;
  description?: string;
  image?: string;
  datePublished: string; // ISO 8601
  dateModified?: string;
  author: string;
  publisherName: string;
  publisherLogo?: string;
  mainEntityOfPage: string; // URL of this post
};

export function articleJsonLd(input: ArticleInput) {
  return {
    '@context': 'https://schema.org',
    '@type': 'Article',
    headline: input.headline,
    ...(input.description ? { description: input.description } : {}),
    ...(input.image ? { image: input.image } : {}),
    datePublished: input.datePublished,
    ...(input.dateModified ? { dateModified: input.dateModified } : {}),
    author: { '@type': 'Person', name: input.author },
    publisher: {
      '@type': 'Organization',
      name: input.publisherName,
      ...(input.publisherLogo
        ? { logo: { '@type': 'ImageObject', url: input.publisherLogo } }
        : {}),
    },
    mainEntityOfPage: { '@type': 'WebPage', '@id': input.mainEntityOfPage },
  };
}

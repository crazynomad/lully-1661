import type { Metadata } from 'next';
import Image from 'next/image';
import { notFound } from 'next/navigation';
import { getTranslations, setRequestLocale } from 'next-intl/server';
import { Container } from '@/components/Container';
import { JsonLd } from '@/components/JsonLd';
import { LocalizedLink } from '@/components/LocalizedLink';
import { Section } from '@/components/Section';
import { type Store, getAllStores, storeHeroImagePath } from '@/features/stores';
import { isLocale, type Locale } from '@/lib/i18n/routing';
import { seo } from '@/lib/seo';

const SITE_URL = process.env.NEXT_PUBLIC_SITE_URL ?? 'https://lully1661.com';

export async function generateStaticParams(): Promise<Array<{ locale: Locale }>> {
  return [{ locale: 'pt' }, { locale: 'en' }];
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ locale: string }>;
}): Promise<Metadata> {
  const { locale } = await params;
  if (!isLocale(locale)) return {};
  const t = await getTranslations({ locale });
  return seo({
    title: t('nav.stores'),
    description:
      locale === 'pt'
        ? 'Três casas em Lisboa: Beato, Anjos, Campo de Ourique. Cada uma com a sua hora e o seu carácter.'
        : 'Three houses in Lisbon: Beato, Anjos, Campo de Ourique. Each with its own hours and character.',
    path: '/lojas',
    locale,
  });
}

export default async function StoresHubPage({
  params,
}: {
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  if (!isLocale(locale)) notFound();
  setRequestLocale(locale);

  const t = await getTranslations();
  const stores = await getAllStores();

  // ItemList JSON-LD pointing to the per-store URLs.
  const itemListJsonLd = {
    '@context': 'https://schema.org',
    '@type': 'ItemList',
    name: t('nav.stores'),
    itemListElement: stores.map(({ slug }, index) => ({
      '@type': 'ListItem',
      position: index + 1,
      url: `${SITE_URL}/${locale}/lojas/${slug}`,
    })),
  };

  return (
    <>
      <JsonLd data={itemListJsonLd} />

      <Section spacing="md">
        <Container>
          <h1 className="text-5xl">{t('nav.stores')}</h1>
          <p className="mt-6 max-w-2xl text-lg text-[color:var(--color-muted)]">
            {locale === 'pt'
              ? 'Três casas em Lisboa, três bairros, três horas do dia diferentes. O Beato é onde nasceu o forno; em Anjos servimos o brunch; Campo de Ourique é a loja de bairro.'
              : "Three houses in Lisbon, three neighbourhoods, three different times of day. Beato is where the oven was born; Anjos serves brunch; Campo de Ourique is the neighbourhood store."}
          </p>
        </Container>
      </Section>

      <Section spacing="md" className="border-t border-[color:var(--color-border)]">
        <Container>
          <ul className="grid gap-12 md:grid-cols-3">
            {stores.map(({ slug, entry }) => (
              <li key={slug}>
                <StoreCard slug={slug} store={entry} locale={locale} />
              </li>
            ))}
          </ul>
        </Container>
      </Section>
    </>
  );
}

function StoreCard({ slug, store, locale }: { slug: string; store: Store; locale: Locale }) {
  return (
    <LocalizedLink href={{ pathname: '/lojas/[slug]', params: { slug } }} className="group block">
      <div className="relative aspect-[4/5] overflow-hidden">
        <Image
          src={storeHeroImagePath(slug)}
          alt={store.photo.decorative ? '' : store.photo.alt[locale]}
          fill
          sizes="(min-width: 768px) 33vw, 100vw"
          className="object-cover transition-transform duration-500 group-hover:scale-105"
        />
      </div>
      <div className="mt-4">
        <p className="text-xs uppercase tracking-widest text-[color:var(--color-muted)]">
          {store.neighborhood}
        </p>
        <h2 className="mt-2 text-2xl group-hover:text-[color:var(--color-accent)] transition-colors">
          {store.name}
        </h2>
        <p className="mt-2 text-sm text-[color:var(--color-muted)] line-clamp-3">
          {store.atmosphere[locale].split('\n')[0]}
        </p>
      </div>
    </LocalizedLink>
  );
}

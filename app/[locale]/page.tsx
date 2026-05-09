import { buttonClassName } from '@/components/Button';
import { Container } from '@/components/Container';
import { Eyebrow } from '@/components/Eyebrow';
import { JsonLd } from '@/components/JsonLd';
import { LocalizedLink } from '@/components/LocalizedLink';
import { SectionTitle } from '@/components/SectionTitle';
import { getAllStores, storeHeroImagePath } from '@/features/stores';
import { type Locale, isLocale } from '@/lib/i18n/routing';
import { organizationJsonLd } from '@/lib/jsonld/organization';
import { reader } from '@/lib/keystatic/reader';
import { seo } from '@/lib/seo';
import { getTranslations, setRequestLocale } from 'next-intl/server';
import Image from 'next/image';
import { notFound } from 'next/navigation';

const SITE_URL = process.env.NEXT_PUBLIC_SITE_URL ?? 'https://lully1661.com';

export async function generateMetadata({ params }: { params: Promise<{ locale: string }> }) {
  const { locale } = await params;
  if (!isLocale(locale)) return {};
  return seo({
    title: 'Lully 1661',
    description:
      locale === 'pt'
        ? 'Boulangerie Renaissance — Lisboa. Padaria orgânica, brunch em Anjos, três casas em Lisboa.'
        : 'Boulangerie Renaissance — Lisbon. Organic bakery, brunch at Anjos, three houses in Lisbon.',
    path: '/',
    locale,
  });
}

const PILLARS_PT = [
  {
    img: '/brand/sub-meunier.jpg',
    title: 'Pães',
    body: 'Sourdough, centeio, fermentação 48h, farinha mó-de-pedra.',
    href: '/menu' as const,
    cta: 'Ver os pães →',
  },
  {
    img: '/brand/sub-patissiere.jpg',
    title: 'Pastelaria & brunch',
    body: 'Viennoiserie, tartes, bolos de estação, e agora — brunch em Anjos.',
    href: '/menu/brunch' as const,
    cta: 'Ver o menu →',
  },
  {
    img: '/brand/sub-caffetier.jpg',
    title: 'Bebidas',
    body: 'Espresso, filtro, matcha, chocolate quente — e a mistura da casa.',
    href: '/menu' as const,
    cta: 'Ver as bebidas →',
  },
];

const PILLARS_EN = [
  {
    img: '/brand/sub-meunier.jpg',
    title: 'Breads',
    body: 'Sourdough, rye, 48-hour fermentation, stone-milled flour.',
    href: '/menu' as const,
    cta: 'Shop breads →',
  },
  {
    img: '/brand/sub-patissiere.jpg',
    title: 'Pastry & brunch',
    body: 'Viennoiseries, tarts, seasonal cakes, and now — brunch at Anjos.',
    href: '/menu/brunch' as const,
    cta: 'See the menu →',
  },
  {
    img: '/brand/sub-caffetier.jpg',
    title: 'Drinks',
    body: 'Espresso, filter, matcha, hot chocolate — and the Lully house blend.',
    href: '/menu' as const,
    cta: 'Shop drinks →',
  },
];

export default async function HomePage({ params }: { params: Promise<{ locale: string }> }) {
  const { locale } = await params;
  if (!isLocale(locale)) notFound();
  setRequestLocale(locale);

  const t = await getTranslations({ locale });
  const pillars = locale === 'pt' ? PILLARS_PT : PILLARS_EN;
  const stores = await getAllStores();
  const featuredItems = await getFeaturedThisWeek(locale);

  const orgJsonLd = organizationJsonLd({
    name: 'Lully 1661',
    url: `${SITE_URL}/${locale}`,
    logo: `${SITE_URL}/brand/logo-wordmark.png`,
    sameAs: ['https://www.instagram.com/lully1661_lisboa/'],
  });

  return (
    <>
      <JsonLd data={orgJsonLd} />

      {/* HERO */}
      <Container
        as="section"
        className="grid gap-14 md:grid-cols-[1.15fr_1fr] items-center py-20 border-b border-[rgba(26,22,19,0.14)]"
      >
        <div>
          <p className="kicker mb-6">
            {locale === 'pt'
              ? "Maintenant, toujours mieux qu'avant."
              : "Maintenant, toujours mieux qu'avant."}
          </p>
          <h1 className="display-xl mb-6">
            {locale === 'pt' ? (
              <>
                Padaria, <em>reinventada.</em>
              </>
            ) : (
              <>
                Bakery, <em>reinvented.</em>
              </>
            )}
          </h1>
          <p className="text-[17px] max-w-[50ch] text-[color:var(--color-ink-2)] leading-[1.6] mb-8">
            {locale === 'pt'
              ? 'Uma padaria orgânica nascida em Lisboa em 2022 — farinha mó-de-pedra do Mâconnais, 48 horas de fermentação, um forno no coração de cada loja. Três casas na cidade, uma só filosofia: tradição, re-assinada.'
              : 'An organic bakery born in Lisbon in 2022 — stone-milled flour from the Mâconnais, 48 hours of fermentation, an oven at the heart of every boutique. Three stores across the city, one philosophy: tradition, re-signed.'}
          </p>
          <div className="flex gap-3">
            <LocalizedLink href="/reservas" className={buttonClassName({ variant: 'ember' })}>
              {t('actions.reserveTable')}
            </LocalizedLink>
            <LocalizedLink href="/menu/brunch" className={buttonClassName({ variant: 'ghost' })}>
              {locale === 'pt' ? 'Ver o brunch →' : 'See the brunch →'}
            </LocalizedLink>
          </div>
        </div>
        <figure className="m-0 text-center">
          <Image
            src="/brand/sub-musicien.jpg"
            alt="Le Musicien — sub-marca Lully"
            width={520}
            height={520}
            sizes="(min-width: 768px) 520px, 80vw"
            className="max-h-[520px] w-auto mx-auto"
            priority
          />
        </figure>
      </Container>

      {/* PILLARS */}
      <Container
        as="section"
        className="grid grid-cols-1 md:grid-cols-3 border-b border-[rgba(26,22,19,0.14)] p-0"
      >
        {pillars.map((p, i) => (
          <div
            key={p.title}
            className={`px-8 py-12 text-center ${i < 2 ? 'md:border-r border-[rgba(26,22,19,0.14)]' : ''}`}
          >
            <Image
              src={p.img}
              alt={p.title}
              width={140}
              height={140}
              className="w-[140px] h-auto mx-auto mb-4"
            />
            <h3
              className="text-[28px] mb-2"
              style={{ fontWeight: 400, fontVariationSettings: '"opsz" 72' }}
            >
              {p.title}
            </h3>
            <p className="text-[14px] text-[color:var(--color-ink-2)] mx-auto max-w-[28ch] leading-[1.5] mb-3.5">
              {p.body}
            </p>
            <LocalizedLink
              href={p.href}
              className="text-[11px] tracking-[0.18em] uppercase text-[color:var(--color-gold)] hover:text-[color:var(--color-ember)] transition-colors"
            >
              {p.cta}
            </LocalizedLink>
          </div>
        ))}
      </Container>

      {/* THIS WEEK */}
      <Container as="section" className="py-16 border-b border-[rgba(26,22,19,0.14)]">
        <div className="flex justify-between items-end mb-8 flex-wrap gap-4">
          <SectionTitle>
            {locale === 'pt' ? (
              <>
                Esta semana <em>na Lully</em>
              </>
            ) : (
              <>
                This week <em>at lully</em>
              </>
            )}
          </SectionTitle>
          <span className="meta">
            {locale === 'pt' ? 'Atualizado às segundas' : 'Updated every Monday'}
          </span>
        </div>
        <ul className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5 list-none p-0 m-0">
          {featuredItems.map((item) => (
            <li
              key={item.slug}
              className="bg-[color:var(--color-paper-2)] border border-[rgba(26,22,19,0.14)]"
            >
              <div className="relative w-full aspect-[16/10] overflow-hidden">
                <Image
                  src={`/content/weeklyMenuItem/${item.slug}/image.jpg`}
                  alt={item.entry.image.decorative ? '' : item.entry.image.alt[locale]}
                  fill
                  sizes="(min-width: 1024px) 25vw, 50vw"
                  className="object-cover"
                />
              </div>
              <div className="p-[18px]">
                <Eyebrow className="text-[10px]">{locale === 'pt' ? 'Brunch' : 'Brunch'}</Eyebrow>
                <h4
                  className="mt-2 mb-1.5 text-[20px] leading-tight"
                  style={{ fontWeight: 400, fontVariationSettings: '"opsz" 48' }}
                >
                  {item.entry.name[locale]}
                </h4>
                <p className="text-[13px] m-0 text-[color:var(--color-ink-2)] leading-[1.5]">
                  {item.entry.description[locale]}
                </p>
              </div>
            </li>
          ))}
        </ul>
      </Container>

      {/* STORES TEASER */}
      <Container as="section" className="py-16 border-b border-[rgba(26,22,19,0.14)]">
        <SectionTitle>
          {locale === 'pt' ? (
            <>
              Três casas <em>em Lisboa.</em>
            </>
          ) : (
            <>
              Three stores <em>in Lisbon.</em>
            </>
          )}
        </SectionTitle>
        <ul className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-8 list-none p-0">
          {stores.map(({ slug, entry }) => (
            <li key={slug} className="border border-[rgba(26,22,19,0.14)]">
              <LocalizedLink
                href={{ pathname: '/lojas/[slug]', params: { slug } }}
                className="block group"
              >
                <div className="relative w-full aspect-[16/9] overflow-hidden">
                  <Image
                    src={storeHeroImagePath(slug)}
                    alt={entry.photo.decorative ? '' : entry.photo.alt[locale]}
                    fill
                    sizes="(min-width: 768px) 33vw, 100vw"
                    className="object-cover transition-transform duration-500 ease-[var(--ease-out)] group-hover:scale-[1.05]"
                  />
                </div>
                <div className="p-[22px]">
                  <Eyebrow className="text-[10px]">{entry.neighborhood}</Eyebrow>
                  <h4
                    className="mt-2 mb-1 text-[24px]"
                    style={{ fontWeight: 400, fontVariationSettings: '"opsz" 60' }}
                  >
                    {entry.name}
                  </h4>
                  <p className="text-[13px] text-[color:var(--color-ink-2)] m-0 leading-[1.5]">
                    {entry.address.streetAddress} · {entry.address.postalCode}{' '}
                    {entry.address.addressLocality}
                  </p>
                </div>
              </LocalizedLink>
            </li>
          ))}
        </ul>
      </Container>
    </>
  );
}

async function getFeaturedThisWeek(_locale: Locale) {
  const items = await reader.collections.weeklyMenuItem.all();
  return items.filter((item) => item.entry.featured).slice(0, 4);
}

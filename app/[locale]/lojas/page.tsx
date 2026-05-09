import { buttonClassName } from '@/components/Button';
import { Container } from '@/components/Container';
import { Eyebrow } from '@/components/Eyebrow';
import { JsonLd } from '@/components/JsonLd';
import { LocalizedLink } from '@/components/LocalizedLink';
import { type Store, getAllStores, storeHeroImagePath } from '@/features/stores';
import { type Locale, isLocale } from '@/lib/i18n/routing';
import { seo } from '@/lib/seo';
import type { Metadata } from 'next';
import { getTranslations, setRequestLocale } from 'next-intl/server';
import Image from 'next/image';
import { notFound } from 'next/navigation';

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

// Compose a "tag" string from the services array — Anjos has dineIn+brunch
// → "Flagship · Brunch · Reservations"; Beato/Campo de Ourique are Boutiques.
function tagFor(store: Store, locale: Locale): string {
  const parts: string[] = [];
  if (store.services.includes('dineIn') || store.services.includes('brunch')) {
    parts.push(locale === 'pt' ? 'Flagship' : 'Flagship');
    if (store.services.includes('brunch')) parts.push('Brunch');
    parts.push(locale === 'pt' ? 'Reservas' : 'Reservations');
  } else {
    parts.push(locale === 'pt' ? 'Boutique' : 'Boutique');
  }
  if (store.openingHours.some((h) => h.weekday === 'sunday')) {
    parts.push(locale === 'pt' ? 'Aberto ao domingo' : 'Open Sundays');
  }
  return parts.join(' · ');
}

export default async function StoresHubPage({
  params,
}: {
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  if (!isLocale(locale)) notFound();
  setRequestLocale(locale);

  const stores = await getAllStores();

  const itemListJsonLd = {
    '@context': 'https://schema.org',
    '@type': 'ItemList',
    name: locale === 'pt' ? 'Lojas' : 'Stores',
    itemListElement: stores.map(({ slug }, index) => ({
      '@type': 'ListItem',
      position: index + 1,
      url: `${SITE_URL}/${locale}/lojas/${slug}`,
    })),
  };

  return (
    <>
      <JsonLd data={itemListJsonLd} />

      <Container as="section" className="pt-18 pb-8 border-b border-[rgba(26,22,19,0.14)]">
        <Eyebrow>{locale === 'pt' ? 'Lojas · Stores' : 'Stores · Lojas'}</Eyebrow>
        <h1 className="display-lg mt-3.5 mb-4">
          {locale === 'pt' ? (
            <>
              Três casas <em>em Lisboa.</em>
            </>
          ) : (
            <>
              Three houses <em>in Lisbon.</em>
            </>
          )}
        </h1>
        <p className="lead m-0">
          {locale === 'pt'
            ? 'Três bairros, três horas do dia diferentes. O Beato é onde nasceu o forno; em Anjos servimos o brunch; Campo de Ourique é a loja de bairro.'
            : 'Three neighbourhoods, three different times of day. Beato is where the oven was born; Anjos serves brunch; Campo de Ourique is the neighbourhood store.'}
        </p>
      </Container>

      <Container as="section" className="py-12">
        <div className="grid gap-14">
          {stores.map(({ slug, entry }) => (
            <article key={slug} className="grid gap-12 md:grid-cols-2 items-start">
              <LocalizedLink
                href={{ pathname: '/lojas/[slug]', params: { slug } }}
                className="block group"
              >
                <div className="relative w-full h-[360px] overflow-hidden">
                  <Image
                    src={storeHeroImagePath(slug)}
                    alt={entry.photo.decorative ? '' : entry.photo.alt[locale]}
                    fill
                    sizes="(min-width: 768px) 50vw, 100vw"
                    className="object-cover transition-transform duration-500 ease-[var(--ease-out)] group-hover:scale-[1.04]"
                  />
                </div>
              </LocalizedLink>

              <div>
                <p className="text-[10px] tracking-[0.2em] uppercase text-[color:var(--color-gold)] mb-3">
                  {tagFor(entry, locale)}
                </p>
                <h2 className="display-md mb-1.5">
                  <LocalizedLink
                    href={{ pathname: '/lojas/[slug]', params: { slug } }}
                    className="hover:text-[color:var(--color-ember)] transition-colors"
                  >
                    {entry.name.replace(/^Lully 1661 — /, '')}
                  </LocalizedLink>
                </h2>
                <p className="text-[12px] tracking-[0.14em] uppercase text-[color:var(--color-stone)] mb-4">
                  {entry.neighborhood}
                </p>
                <p className="text-[16px] text-[color:var(--color-ink-2)] leading-[1.6] m-0 mb-5">
                  {entry.atmosphere[locale].split('\n')[0]}
                </p>

                <div className="border-t border-[rgba(26,22,19,0.14)] pt-4 mb-5">
                  <p className="text-[11px] tracking-[0.18em] uppercase text-[color:var(--color-stone)] mb-1">
                    {entry.address.streetAddress} · {entry.address.postalCode}{' '}
                    {entry.address.addressLocality}
                  </p>
                  <dl className="text-[13px] text-[color:var(--color-ink-2)] leading-[2] m-0 max-w-[280px]">
                    {compactHours(entry, locale).map(([d, h]) => (
                      <div key={d} className="flex justify-between">
                        <dt className="text-[color:var(--color-ink)] font-semibold">{d}</dt>
                        <dd>{h}</dd>
                      </div>
                    ))}
                  </dl>
                </div>

                <div className="flex gap-2.5 flex-wrap">
                  <LocalizedLink
                    href={{ pathname: '/lojas/[slug]', params: { slug } }}
                    className={buttonClassName({ variant: 'ghost', size: 'sm' })}
                  >
                    {locale === 'pt' ? 'Ver a loja' : 'See the store'}
                  </LocalizedLink>
                  {(entry.services.includes('dineIn') || entry.services.includes('brunch')) && (
                    <LocalizedLink
                      href="/reservas"
                      className={buttonClassName({ variant: 'ember', size: 'sm' })}
                    >
                      {locale === 'pt' ? 'Reservar mesa' : 'Reserve a table'}
                    </LocalizedLink>
                  )}
                </div>
              </div>
            </article>
          ))}
        </div>
      </Container>
    </>
  );
}

// Collapse the per-day hours into the brand's "Tue–Sat 8:00–19:00 · Sun · Mon Closed"
// short-form. Group consecutive days that share the same opening/closing.
function compactHours(store: Store, locale: Locale): Array<[string, string]> {
  const dayLabelsPt: Record<string, string> = {
    monday: 'Seg',
    tuesday: 'Ter',
    wednesday: 'Qua',
    thursday: 'Qui',
    friday: 'Sex',
    saturday: 'Sáb',
    sunday: 'Dom',
  };
  const dayLabelsEn: Record<string, string> = {
    monday: 'Mon',
    tuesday: 'Tue',
    wednesday: 'Wed',
    thursday: 'Thu',
    friday: 'Fri',
    saturday: 'Sat',
    sunday: 'Sun',
  };
  const closedLabel = locale === 'pt' ? 'Encerrado' : 'Closed';
  const labels = locale === 'pt' ? dayLabelsPt : dayLabelsEn;
  const order = [
    'monday',
    'tuesday',
    'wednesday',
    'thursday',
    'friday',
    'saturday',
    'sunday',
  ] as const;

  const hoursMap = new Map(store.openingHours.map((h) => [h.weekday, `${h.opens} – ${h.closes}`]));

  // Group consecutive days with the same hours (or both closed).
  const groups: Array<{ days: string[]; hours: string }> = [];
  for (const day of order) {
    const hours = hoursMap.get(day) ?? closedLabel;
    const last = groups[groups.length - 1];
    if (last && last.hours === hours) {
      last.days.push(day);
    } else {
      groups.push({ days: [day], hours });
    }
  }

  return groups.map(({ days, hours }) => {
    const range =
      days.length === 1
        ? labels[days[0]!]!
        : `${labels[days[0]!]!} – ${labels[days[days.length - 1]!]!}`;
    return [range, hours] as [string, string];
  });
}

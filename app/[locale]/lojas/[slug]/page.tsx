import { Container } from '@/components/Container';
import { JsonLd } from '@/components/JsonLd';
import { LocalizedLink } from '@/components/LocalizedLink';
import { Section } from '@/components/Section';
import {
  type Store,
  type WeekdayKey,
  atmosphereFor,
  getAllStores,
  getMenuItemsAvailableAt,
  getStore,
  storeHeroImagePath,
  storePageJsonLd,
} from '@/features/stores';
import { type Locale, isLocale } from '@/lib/i18n/routing';
import { seo } from '@/lib/seo';
import type { Metadata } from 'next';
import { getTranslations, setRequestLocale } from 'next-intl/server';
import Image from 'next/image';
import { notFound } from 'next/navigation';

type Params = { locale: string; slug: string };

export async function generateStaticParams(): Promise<Array<{ locale: Locale; slug: string }>> {
  const stores = await getAllStores();
  return stores.flatMap(({ slug }) => [
    { locale: 'pt' as const, slug },
    { locale: 'en' as const, slug },
  ]);
}

export async function generateMetadata({ params }: { params: Promise<Params> }): Promise<Metadata> {
  const { locale, slug } = await params;
  if (!isLocale(locale)) return {};
  const store = await getStore(slug);
  if (!store) return {};

  const description = atmosphereFor(store, locale).slice(0, 160).trim();
  return seo({
    title: `${store.name} · ${store.neighborhood}`,
    description,
    path: `/lojas/${slug}`,
    locale,
    ogImage: `${process.env.NEXT_PUBLIC_SITE_URL ?? 'https://lully1661.com'}${storeHeroImagePath(slug)}`,
  });
}

const WEEKDAY_LABELS_PT: Record<WeekdayKey, string> = {
  monday: 'Segunda',
  tuesday: 'Terça',
  wednesday: 'Quarta',
  thursday: 'Quinta',
  friday: 'Sexta',
  saturday: 'Sábado',
  sunday: 'Domingo',
};

const WEEKDAY_LABELS_EN: Record<WeekdayKey, string> = {
  monday: 'Mon',
  tuesday: 'Tue',
  wednesday: 'Wed',
  thursday: 'Thu',
  friday: 'Fri',
  saturday: 'Sat',
  sunday: 'Sun',
};

const WEEKDAYS_ORDERED: WeekdayKey[] = [
  'monday',
  'tuesday',
  'wednesday',
  'thursday',
  'friday',
  'saturday',
  'sunday',
];

const SERVICE_LABELS_PT = {
  dineIn: 'Esplanada / mesa',
  brunch: 'Brunch',
  pickup: 'Recolha em loja',
  ovenVisible: 'Forno à vista',
  parking: 'Estacionamento',
  wheelchair: 'Acesso para cadeira de rodas',
} as const;

const SERVICE_LABELS_EN = {
  dineIn: 'Dine-in',
  brunch: 'Brunch',
  pickup: 'In-store pickup',
  ovenVisible: 'Visible oven',
  parking: 'Parking nearby',
  wheelchair: 'Wheelchair access',
} as const;

function googleMapsUrl(store: Store): string {
  const q = `${store.address.streetAddress}, ${store.address.postalCode ?? ''} ${store.address.addressLocality}`;
  return `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(q)}`;
}

export default async function StorePage({ params }: { params: Promise<Params> }) {
  const { locale, slug } = await params;
  if (!isLocale(locale)) notFound();
  setRequestLocale(locale);

  const store = await getStore(slug);
  if (!store) notFound();

  const t = await getTranslations();
  const menuItems = await getMenuItemsAvailableAt(slug);

  const weekdayLabels = locale === 'pt' ? WEEKDAY_LABELS_PT : WEEKDAY_LABELS_EN;
  const serviceLabels = locale === 'pt' ? SERVICE_LABELS_PT : SERVICE_LABELS_EN;

  const hoursByDay = new Map(store.openingHours.map((h) => [h.weekday, h]));
  const closedLabel = locale === 'pt' ? 'Encerrado' : 'Closed';
  const featuredOnly = menuItems.filter((item) => item.entry.featured);

  const showReservations = store.services.includes('dineIn') || store.services.includes('brunch');

  const jsonLd = storePageJsonLd({
    store,
    pathFromRoot: `/lojas/${slug}`,
    locale,
    labels: {
      home: t('nav.home'),
      stores: t('nav.stores'),
    },
  });

  return (
    <>
      <JsonLd data={jsonLd} />

      {/* Hero */}
      <Section spacing="sm" className="relative">
        <div className="relative aspect-[16/9] w-full overflow-hidden">
          <Image
            src={storeHeroImagePath(slug)}
            alt={store.photo.decorative ? '' : store.photo.alt[locale]}
            fill
            sizes="100vw"
            priority
            className="object-cover"
          />
        </div>
        <Container className="-mt-20 relative">
          <div className="bg-[color:var(--color-bg)] px-8 py-10 max-w-3xl">
            <p className="text-sm uppercase tracking-widest text-[color:var(--color-muted)]">
              {store.neighborhood}
            </p>
            <h1 className="mt-3 text-5xl">{store.name}</h1>
          </div>
        </Container>
      </Section>

      {/* Info row: address + hours side-by-side on desktop */}
      <Section spacing="md">
        <Container>
          <div className="grid gap-12 md:grid-cols-2">
            {/* Address + actions */}
            <div>
              <h2 className="text-2xl mb-4">
                {locale === 'pt' ? 'Onde estamos' : 'Where to find us'}
              </h2>
              <address className="not-italic text-lg leading-relaxed">
                {store.address.streetAddress}
                <br />
                {store.address.postalCode} {store.address.addressLocality}
                <br />
                {store.address.addressCountry}
              </address>

              {store.phone && (
                <p className="mt-6">
                  <a
                    href={`tel:${store.phone}`}
                    className="text-[color:var(--color-accent)] underline-offset-4 hover:underline"
                  >
                    {formatPhone(store.phone)}
                  </a>
                </p>
              )}

              <div className="mt-8 flex flex-wrap gap-3">
                <a
                  href={googleMapsUrl(store)}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center justify-center px-5 py-2.5 bg-[color:var(--color-fg)] text-[color:var(--color-bg)] hover:bg-[color:var(--color-accent)] transition-colors"
                >
                  {locale === 'pt' ? 'Ver no mapa' : 'Get directions'}
                </a>
                {showReservations && (
                  <LocalizedLink
                    href="/reservas"
                    className="inline-flex items-center justify-center px-5 py-2.5 border border-[color:var(--color-border)] hover:border-[color:var(--color-fg)] transition-colors"
                  >
                    {t('actions.reserveTable')}
                  </LocalizedLink>
                )}
              </div>
            </div>

            {/* Hours */}
            <div>
              <h2 className="text-2xl mb-4">{locale === 'pt' ? 'Horários' : 'Opening hours'}</h2>
              <dl className="text-base">
                {WEEKDAYS_ORDERED.map((day) => {
                  const h = hoursByDay.get(day);
                  return (
                    <div
                      key={day}
                      className="flex justify-between py-2 border-b border-[color:var(--color-border)] last:border-0"
                    >
                      <dt className="text-[color:var(--color-muted)]">{weekdayLabels[day]}</dt>
                      <dd className="font-medium tabular-nums">
                        {h ? `${h.opens} – ${h.closes}` : closedLabel}
                      </dd>
                    </div>
                  );
                })}
              </dl>
            </div>
          </div>
        </Container>
      </Section>

      {/* Services chips */}
      {store.services.length > 0 && (
        <Section spacing="sm" className="border-t border-[color:var(--color-border)]">
          <Container>
            <h2 className="text-sm uppercase tracking-widest text-[color:var(--color-muted)] mb-4">
              {locale === 'pt' ? 'Nesta loja' : 'At this store'}
            </h2>
            <ul className="flex flex-wrap gap-3">
              {store.services.map((s) => (
                <li
                  key={s}
                  className="inline-flex items-center px-4 py-2 border border-[color:var(--color-border)] text-sm"
                >
                  {serviceLabels[s as keyof typeof serviceLabels]}
                </li>
              ))}
            </ul>
          </Container>
        </Section>
      )}

      {/* Atmosphere */}
      <Section spacing="md">
        <Container size="narrow">
          <h2 className="text-2xl mb-6">{locale === 'pt' ? 'A casa' : 'The house'}</h2>
          <div className="text-lg leading-relaxed whitespace-pre-line text-[color:var(--color-fg)]">
            {atmosphereFor(store, locale)}
          </div>
        </Container>
      </Section>

      {/* What's available here */}
      {featuredOnly.length > 0 && (
        <Section spacing="md" className="border-t border-[color:var(--color-border)]">
          <Container>
            <h2 className="text-2xl mb-8">
              {locale === 'pt' ? 'Em destaque esta semana' : 'Featured this week'}
            </h2>
            <ul className="grid gap-8 md:grid-cols-3">
              {featuredOnly.map(({ slug: itemSlug, entry }) => (
                <li key={itemSlug}>
                  <div className="aspect-square relative overflow-hidden bg-[color:var(--color-border)]">
                    <Image
                      src={`/content/weeklyMenuItem/${itemSlug}/image.jpg`}
                      alt={entry.image.decorative ? '' : entry.image.alt[locale]}
                      fill
                      sizes="(min-width: 768px) 33vw, 100vw"
                      className="object-cover"
                    />
                  </div>
                  <h3 className="mt-4 text-xl">{entry.name[locale]}</h3>
                  <p className="mt-2 text-[color:var(--color-muted)] line-clamp-3">
                    {entry.description[locale]}
                  </p>
                </li>
              ))}
            </ul>
          </Container>
        </Section>
      )}
    </>
  );
}

function formatPhone(e164: string): string {
  // +351961816221 -> +351 961 816 221
  const m = e164.match(/^\+(\d{1,3})(\d{3})(\d{3})(\d{3})$/);
  if (!m) return e164;
  return `+${m[1]} ${m[2]} ${m[3]} ${m[4]}`;
}

import { Container } from '@/components/Container';
import { Eyebrow } from '@/components/Eyebrow';
import { ReservationForm } from '@/features/reservations';
import { isLocale } from '@/lib/i18n/routing';
import { seo } from '@/lib/seo';
import type { Metadata } from 'next';
import { setRequestLocale } from 'next-intl/server';
import { notFound } from 'next/navigation';

export async function generateStaticParams() {
  return [{ locale: 'pt' }, { locale: 'en' }];
}

export async function generateMetadata({
  params,
}: { params: Promise<{ locale: string }> }): Promise<Metadata> {
  const { locale } = await params;
  if (!isLocale(locale)) return {};
  return seo({
    title: locale === 'pt' ? 'Reservas' : 'Reservations',
    description:
      locale === 'pt'
        ? 'Reserve uma mesa em Anjos. Brunch servido todas as manhãs, Ter–Dom.'
        : 'Reserve a table at Anjos. Brunch served every morning, Tue–Sun.',
    path: '/reservas',
    locale,
  });
}

export default async function ReservationsPage({
  params,
}: { params: Promise<{ locale: string }> }) {
  const { locale } = await params;
  if (!isLocale(locale)) notFound();
  setRequestLocale(locale);

  return (
    <Container as="main" size="narrow" className="pt-18 pb-24">
      <Eyebrow>{locale === 'pt' ? 'Reservas' : 'Reservations'}</Eyebrow>
      <h1 className="display-lg mt-3.5 mb-4">
        {locale === 'pt' ? (
          <>
            Uma mesa em <em>Anjos.</em>
          </>
        ) : (
          <>
            A table at <em>Anjos.</em>
          </>
        )}
      </h1>
      <p className="lead m-0 mb-9">
        {locale === 'pt'
          ? 'As reservas são feitas apenas em Anjos — as outras duas lojas operam só ao balcão. Ter–Dom, brunch das 8h30 às 12h30.'
          : 'Reservations are taken at Anjos only — the other two stores run counter-only. Tue–Sun, brunch service from 8:30 to 12:30.'}
      </p>

      <ReservationForm locale={locale} />
    </Container>
  );
}

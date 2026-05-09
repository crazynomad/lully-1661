import { buttonClassName } from '@/components/Button';
import { Container } from '@/components/Container';
import { Eyebrow } from '@/components/Eyebrow';
import { LocalizedLink } from '@/components/LocalizedLink';
import { isLocale } from '@/lib/i18n/routing';
import { seo } from '@/lib/seo';
import type { Metadata } from 'next';
import { setRequestLocale } from 'next-intl/server';
import Image from 'next/image';
import { notFound } from 'next/navigation';

const ENQUIRY_EMAIL = 'sales@lully1661.com';

export async function generateStaticParams() {
  return [{ locale: 'pt' }, { locale: 'en' }];
}

export async function generateMetadata({
  params,
}: { params: Promise<{ locale: string }> }): Promise<Metadata> {
  const { locale } = await params;
  if (!isLocale(locale)) return {};
  return seo({
    title: locale === 'pt' ? 'Encomendas festivas e à medida' : 'Festive & Bespoke Orders',
    description:
      locale === 'pt'
        ? 'Bolos sazonais, gift hampers, eventos privados e catering. Lisboa.'
        : 'Seasonal cakes, gift hampers, private events, catering. Lisbon.',
    path: '/encomendas',
    locale,
  });
}

export default async function FestiveOrdersPage({
  params,
}: { params: Promise<{ locale: string }> }) {
  const { locale } = await params;
  if (!isLocale(locale)) notFound();
  setRequestLocale(locale);

  const isPt = locale === 'pt';

  return (
    <>
      {/* HERO */}
      <Container
        as="section"
        className="grid gap-14 md:grid-cols-[1.1fr_1fr] items-center py-18 border-b border-[rgba(26,22,19,0.14)]"
      >
        <div>
          <Eyebrow>{isPt ? 'Encomendas · Festive & Bespoke' : 'Bespoke · Encomendas'}</Eyebrow>
          <h1 className="display-lg mt-3.5 mb-4">
            {isPt ? (
              <>
                Para os momentos <em>que ficam.</em>
              </>
            ) : (
              <>
                For the moments <em>that stay.</em>
              </>
            )}
          </h1>
          <p className="lead m-0">
            {isPt
              ? 'Bolos sazonais, gift hampers, almoços de chef convidado, eventos privados, catering. Trabalhamos com antecedência mínima de uma semana — para o pão, três dias.'
              : 'Seasonal cakes, gift hampers, guest-chef luncheons, private events, catering. Lead time of one week minimum — three days for bread.'}
          </p>
        </div>
        <figure className="m-0 text-center">
          <Image
            src="/content/moodboard/cake-stands.jpg"
            alt={isPt ? 'Estrutura de bolo de inspiração barroca' : 'Baroque cake stand engraving'}
            width={420}
            height={520}
            sizes="(min-width: 768px) 420px, 70vw"
            className="max-h-[500px] w-auto mx-auto"
            priority
          />
        </figure>
      </Container>

      {/* THREE FORMATS */}
      <Container as="section" className="py-16 border-b border-[rgba(26,22,19,0.14)]">
        <Eyebrow>{isPt ? 'Três formatos' : 'Three formats'}</Eyebrow>
        <h2 className="display-md mt-3 mb-10 max-w-[26ch]">
          {isPt ? (
            <>
              Da mesa de família <em>ao palco.</em>
            </>
          ) : (
            <>
              From the family table <em>to the stage.</em>
            </>
          )}
        </h2>
        <div className="grid gap-10 md:grid-cols-3">
          {[
            {
              title: isPt ? 'Sazonal' : 'Seasonal',
              body: isPt
                ? 'Páscoa, S. João, Natal, Ano Novo, Dia dos Namorados. Catálogo rotativo, encomendas com 7 dias de antecedência. Levantamento em qualquer das três lojas.'
                : "Easter, S. João, Christmas, New Year, Valentine's. Rotating catalogue, 7-day lead time. Pickup at any of the three stores.",
              cta: isPt ? 'Pedir o catálogo' : 'Request the catalogue',
            },
            {
              title: isPt ? 'Mesa privada' : 'Private table',
              body: isPt
                ? 'Almoços de chef convidado em Anjos. Mesa única, 12–18 lugares, menu degustação que percorre o forno e a pastelaria. Próxima sessão: ver newsletter.'
                : 'Guest-chef luncheons at Anjos. One table, 12–18 seats, tasting menu that walks through bread and pastry. Next session: newsletter.',
              cta: isPt ? 'Subscrever newsletter' : 'Subscribe to newsletter',
            },
            {
              title: isPt ? 'Catering' : 'Catering',
              body: isPt
                ? 'Eventos corporativos, casamentos, lançamentos. Pão, viennoiserie, brunch box, mesa de pastelaria. Mínimo 30 pessoas, encomenda com 2 semanas.'
                : 'Corporate events, weddings, launches. Bread, viennoiserie, brunch box, pastry table. Minimum 30 guests, 2-week lead time.',
              cta: isPt ? 'Pedir orçamento' : 'Request a quote',
            },
          ].map((format) => (
            <div key={format.title}>
              <h3
                className="text-[26px] mb-3"
                style={{ fontWeight: 400, fontVariationSettings: '"opsz" 60' }}
              >
                {format.title}
              </h3>
              <p className="text-[15px] text-[color:var(--color-ink-2)] m-0 mb-4 leading-[1.6]">
                {format.body}
              </p>
              <a
                href={`mailto:${ENQUIRY_EMAIL}?subject=${encodeURIComponent(format.title)}`}
                className="text-[11px] tracking-[0.18em] uppercase text-[color:var(--color-gold)] hover:text-[color:var(--color-ember)] transition-colors"
              >
                {format.cta} →
              </a>
            </div>
          ))}
        </div>
      </Container>

      {/* PAST EVENT — Gareth × Sezin */}
      <Container
        as="section"
        className="py-16 border-b border-[rgba(26,22,19,0.14)] grid gap-12 md:grid-cols-[1fr_1.2fr] items-center"
      >
        <Image
          src="/content/moodboard/instruments.jpg"
          alt={
            isPt
              ? 'Gravura de instrumentos barrocos — referência'
              : 'Baroque instruments engraving — reference'
          }
          width={500}
          height={550}
          sizes="(min-width: 768px) 500px, 80vw"
          className="w-full max-h-[460px] object-contain"
        />
        <div>
          <Eyebrow>{isPt ? 'Visto recentemente' : 'Recently'}</Eyebrow>
          <h3 className="display-md mt-3 mb-4">
            {isPt ? (
              <>
                Gareth × Sezin, <em>Anjos.</em>
              </>
            ) : (
              <>
                Gareth × Sezin, <em>at Anjos.</em>
              </>
            )}
          </h3>
          <p className="text-[16px] text-[color:var(--color-ink-2)] leading-[1.6] m-0 mb-3">
            {isPt
              ? 'Almoço de chef convidado em Maio de 2026. Mesa única, 16 lugares, menu de cinco tempos construído em conjunto — pão Paillard de centeio puro, queijos curados, frutos vermelhos da serra de Sintra.'
              : 'Guest-chef luncheon, May 2026. One table, 16 seats, five-course menu built together — pure rye Paillard, aged cheeses, red fruits from Serra de Sintra.'}
          </p>
          <p className="text-[16px] text-[color:var(--color-ink-2)] leading-[1.6] m-0">
            {isPt
              ? 'Os almoços rodam três a quatro vezes por ano. As datas seguintes saem na newsletter, sempre com duas semanas de antecedência.'
              : 'The luncheons happen three to four times a year. Future dates go out in the newsletter, two weeks ahead.'}
          </p>
        </div>
      </Container>

      {/* CTA */}
      <Container as="section" className="py-16 text-center">
        <p className="kicker mb-7" style={{ fontSize: '24px' }}>
          {isPt
            ? 'A começar em duas semanas, ou daqui a três meses?'
            : 'Two weeks away, or three months out?'}
        </p>
        <div className="flex gap-3 justify-center flex-wrap">
          <a
            href={`mailto:${ENQUIRY_EMAIL}?subject=${encodeURIComponent(isPt ? 'Pedido de encomenda' : 'Bespoke enquiry')}`}
            className={buttonClassName({ variant: 'ember' })}
          >
            {isPt ? 'Falar connosco' : 'Get in touch'}
          </a>
          <LocalizedLink href="/lojas" className={buttonClassName({ variant: 'ghost' })}>
            {isPt ? 'Ver as lojas →' : 'See the stores →'}
          </LocalizedLink>
        </div>
        <p className="meta mt-6">
          {isPt ? `Ou diretamente para ${ENQUIRY_EMAIL}` : `Or directly at ${ENQUIRY_EMAIL}`}
        </p>
      </Container>
    </>
  );
}

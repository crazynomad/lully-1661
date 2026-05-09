import { Container } from '@/components/Container';
import { Eyebrow } from '@/components/Eyebrow';
import { LocalizedLink } from '@/components/LocalizedLink';
import { isLocale } from '@/lib/i18n/routing';
import { seo } from '@/lib/seo';
import type { Metadata } from 'next';
import { setRequestLocale } from 'next-intl/server';
import Image from 'next/image';
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
    title: locale === 'pt' ? 'Menu' : 'Menu',
    description:
      locale === 'pt'
        ? 'Pães, pastelaria, bebidas, brunch — em quatro pilares. Atualizado todas as segundas-feiras.'
        : 'Breads, pastry, drinks, brunch — in four pillars. Updated every Monday.',
    path: '/menu',
    locale,
  });
}

// v1 menu hub: a small entry-point page. The full /menu/[category] and
// per-product detail pages are tracked for v1.1 — for now we point
// visitors at the brunch sub-page (which is fully implemented) and at
// the three pillars served at the stores.

const PILLARS_PT = [
  {
    img: '/brand/sub-meunier.jpg',
    title: 'Pães',
    body: 'Sourdough, centeio, fermentação 48h, farinha mó-de-pedra do Mâconnais. Cozidos em todas as três lojas, todas as manhãs.',
    cta: 'Em loja',
    soon: true,
  },
  {
    img: '/brand/sub-patissiere.jpg',
    title: 'Pastelaria & brunch',
    body: 'Viennoiserie, tartes, bolos de estação, e o brunch — servido em Anjos, todas as manhãs.',
    cta: 'Ver o brunch →',
    href: '/menu/brunch' as const,
    soon: false,
  },
  {
    img: '/brand/sub-caffetier.jpg',
    title: 'Bebidas',
    body: 'Espresso, filtro, matcha, chocolate quente — e a mistura da casa.',
    cta: 'Em loja',
    soon: true,
  },
];

const PILLARS_EN = [
  {
    img: '/brand/sub-meunier.jpg',
    title: 'Breads',
    body: 'Sourdough, rye, 48-hour fermentation, stone-milled flour from the Mâconnais. Baked at every store, every morning.',
    cta: 'In store',
    soon: true,
  },
  {
    img: '/brand/sub-patissiere.jpg',
    title: 'Pastry & brunch',
    body: 'Viennoiseries, tarts, seasonal cakes, and brunch — served at Anjos, every morning.',
    cta: 'See the brunch →',
    href: '/menu/brunch' as const,
    soon: false,
  },
  {
    img: '/brand/sub-caffetier.jpg',
    title: 'Drinks',
    body: 'Espresso, filter, matcha, hot chocolate — and the Lully house blend.',
    cta: 'In store',
    soon: true,
  },
];

export default async function MenuHubPage({ params }: { params: Promise<{ locale: string }> }) {
  const { locale } = await params;
  if (!isLocale(locale)) notFound();
  setRequestLocale(locale);

  const pillars = locale === 'pt' ? PILLARS_PT : PILLARS_EN;

  return (
    <>
      <Container as="section" className="py-18 border-b border-[rgba(26,22,19,0.14)]">
        <Eyebrow>{locale === 'pt' ? 'Menu' : 'Menu'}</Eyebrow>
        <h1 className="display-lg mt-3.5 mb-4 max-w-[18ch]">
          {locale === 'pt' ? (
            <>
              Quatro pilares, <em>uma só casa.</em>
            </>
          ) : (
            <>
              Four pillars, <em>one house.</em>
            </>
          )}
        </h1>
        <p className="lead m-0">
          {locale === 'pt'
            ? 'O nosso menu de loja muda conforme o que sai do forno. O brunch tem o seu próprio menu, em Anjos.'
            : 'Our in-store menu rotates with what comes out of the oven. Brunch has its own menu, at Anjos.'}
        </p>
      </Container>

      <Container as="section" className="grid grid-cols-1 md:grid-cols-3 p-0">
        {pillars.map((p, i) => (
          <div
            key={p.title}
            className={`px-8 py-12 text-center ${i < 2 ? 'md:border-r border-[rgba(26,22,19,0.14)]' : ''}`}
          >
            <Image
              src={p.img}
              alt={p.title}
              width={140}
              height={196}
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
            {p.soon ? (
              <span className="text-[11px] tracking-[0.18em] uppercase text-[color:var(--color-stone)]">
                {p.cta}
              </span>
            ) : p.href ? (
              <LocalizedLink
                href={p.href}
                className="text-[11px] tracking-[0.18em] uppercase text-[color:var(--color-gold)] hover:text-[color:var(--color-ember)] transition-colors"
              >
                {p.cta}
              </LocalizedLink>
            ) : null}
          </div>
        ))}
      </Container>
    </>
  );
}

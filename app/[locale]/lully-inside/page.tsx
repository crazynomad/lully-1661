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

const B2B_EMAIL = 'partners@lully1661.com';

export async function generateStaticParams() {
  return [{ locale: 'pt' }, { locale: 'en' }];
}

export async function generateMetadata({
  params,
}: { params: Promise<{ locale: string }> }): Promise<Metadata> {
  const { locale } = await params;
  if (!isLocale(locale)) return {};
  return seo({
    title: 'Lully Inside',
    description:
      locale === 'pt'
        ? 'Parcerias B2B — fornecimento a hotéis, restaurantes, retalho. Pão Paillard, viennoiserie, pastelaria de assinatura.'
        : 'B2B partnerships — supplying hotels, restaurants, retail. Paillard bread, viennoiserie, signature pastry.',
    path: '/lully-inside',
    locale,
  });
}

export default async function LullyInsidePage({ params }: { params: Promise<{ locale: string }> }) {
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
          <Eyebrow>Lully Inside · B2B</Eyebrow>
          <h1 className="display-lg mt-3.5 mb-4">
            {isPt ? (
              <>
                O nosso pão, <em>na sua casa.</em>
              </>
            ) : (
              <>
                Our bread, <em>in your house.</em>
              </>
            )}
          </h1>
          <p className="lead m-0">
            {isPt
              ? 'Trabalhamos em silêncio com hotéis, restaurantes, lojas de bairro e marcas que querem servir pão a sério sem o cozer. Encomendas regulares, marca-branca, ou produto co-assinado.'
              : 'We work quietly with hotels, restaurants, neighbourhood shops, and brands that want to serve serious bread without baking it. Regular wholesale, white-label, or co-branded product.'}
          </p>
        </div>
        <figure className="m-0 text-center">
          <Image
            src="/brand/sub-caffetier.jpg"
            alt={isPt ? 'Le Caffetier — sub-marca Lully' : 'Le Caffetier — Lully sub-mark'}
            width={400}
            height={540}
            sizes="(min-width: 768px) 400px, 70vw"
            className="max-h-[480px] w-auto mx-auto"
            priority
          />
        </figure>
      </Container>

      {/* HOW WE WORK */}
      <Container as="section" className="py-16 border-b border-[rgba(26,22,19,0.14)]">
        <Eyebrow>{isPt ? 'Três modelos' : 'Three models'}</Eyebrow>
        <h2 className="display-md mt-3 mb-10 max-w-[26ch]">
          {isPt ? (
            <>
              Da fornada partilhada <em>ao co-assinado.</em>
            </>
          ) : (
            <>
              From shared bake <em>to co-signed.</em>
            </>
          )}
        </h2>
        <div className="grid gap-10 md:grid-cols-3">
          {[
            {
              title: isPt ? 'Fornecimento' : 'Wholesale',
              body: isPt
                ? 'Pão e viennoiserie cozidos no Beato, entregues frescos da manhã em Lisboa. Mínimo 30 unidades por dia, contrato a 6 meses.'
                : 'Bread and viennoiserie baked at Beato, delivered fresh in the morning across Lisbon. Minimum 30 units/day, 6-month contract.',
            },
            {
              title: isPt ? 'Marca-branca' : 'White-label',
              body: isPt
                ? 'O nosso pão e pastelaria, com a sua identidade. Embalagem co-desenhada, ficha técnica completa, formação aos seus colaboradores.'
                : 'Our bread and pastry under your brand. Co-designed packaging, full spec sheet, training for your staff.',
            },
            {
              title: isPt ? 'Co-assinado' : 'Co-signed',
              body: isPt
                ? 'Produto desenvolvido em conjunto, leva os dois nomes. Para projetos editoriais, lançamentos, edições limitadas.'
                : 'Product developed together, carries both names. For editorial projects, launches, limited editions.',
            },
          ].map((model) => (
            <div key={model.title}>
              <h3
                className="text-[26px] mb-3"
                style={{ fontWeight: 400, fontVariationSettings: '"opsz" 60' }}
              >
                {model.title}
              </h3>
              <p className="text-[15px] text-[color:var(--color-ink-2)] m-0 leading-[1.6]">
                {model.body}
              </p>
            </div>
          ))}
        </div>
      </Container>

      {/* PARTNERS — descriptive only, no logos until launch */}
      <Container
        as="section"
        className="py-16 border-b border-[rgba(26,22,19,0.14)] grid gap-12 md:grid-cols-[1fr_1.4fr]"
      >
        <h3
          className="text-[30px] m-0"
          style={{ fontWeight: 400, fontVariationSettings: '"opsz" 72' }}
        >
          {isPt ? (
            <>
              Quem trabalha <em>connosco.</em>
            </>
          ) : (
            <>
              Who works <em>with us.</em>
            </>
          )}
        </h3>
        <div className="text-[16px] text-[color:var(--color-ink-2)] leading-[1.6]">
          <p className="m-0 mb-3">
            {isPt
              ? 'Hotéis em Lisboa que servem o nosso brunch ao quarto. Restaurantes que pedem o Paillard de meio metro para a tábua de queijos. Cafés de bairro em Cascais e Sintra. Lojas gourmet que vendem o nosso panettone no Natal.'
              : 'Lisbon hotels that serve our brunch to room service. Restaurants that order the half-metre Paillard for the cheese board. Neighbourhood cafés in Cascais and Sintra. Gourmet shops that sell our panettone at Christmas.'}
          </p>
          <p className="m-0">
            {isPt
              ? 'A lista pública dos parceiros sai com a próxima newsletter trimestral.'
              : 'The public partner list goes out with the next quarterly newsletter.'}
          </p>
        </div>
      </Container>

      {/* CTA */}
      <Container as="section" className="py-16 text-center">
        <p className="kicker mb-7" style={{ fontSize: '24px' }}>
          {isPt ? 'Tem um projeto em mente?' : 'Got a project in mind?'}
        </p>
        <div className="flex gap-3 justify-center flex-wrap">
          <a
            href={`mailto:${B2B_EMAIL}?subject=${encodeURIComponent(isPt ? 'Lully Inside — proposta' : 'Lully Inside — proposal')}`}
            className={buttonClassName({ variant: 'ember' })}
          >
            {isPt ? 'Escrever-nos' : 'Write to us'}
          </a>
          <LocalizedLink href="/sobre" className={buttonClassName({ variant: 'ghost' })}>
            {isPt ? 'Sobre a casa →' : 'About the house →'}
          </LocalizedLink>
        </div>
        <p className="meta mt-6">
          {isPt ? `Ou diretamente para ${B2B_EMAIL}` : `Or directly at ${B2B_EMAIL}`}
        </p>
      </Container>
    </>
  );
}

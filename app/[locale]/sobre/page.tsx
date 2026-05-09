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

export async function generateStaticParams() {
  return [{ locale: 'pt' }, { locale: 'en' }];
}

export async function generateMetadata({
  params,
}: { params: Promise<{ locale: string }> }): Promise<Metadata> {
  const { locale } = await params;
  if (!isLocale(locale)) return {};
  return seo({
    title: locale === 'pt' ? 'Sobre' : 'About',
    description:
      locale === 'pt'
        ? 'Lully 1661 — uma padaria orgânica nascida em Lisboa em 2022. Nomeada em homenagem ao compositor barroco Jean-Baptiste Lully.'
        : 'Lully 1661 — an organic bakery born in Lisbon in 2022. Named after the Baroque composer Jean-Baptiste Lully.',
    path: '/sobre',
    locale,
  });
}

export default async function AboutPage({ params }: { params: Promise<{ locale: string }> }) {
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
          <p className="kicker mb-5">
            {isPt ? 'Tradição, re-assinada em 2026.' : 'Tradition, re-signed in 2026.'}
          </p>
          <h1 className="display-lg mb-4">
            {isPt ? (
              <>
                Padaria, <em>renascimento.</em>
              </>
            ) : (
              <>
                Bakery, <em>a renaissance.</em>
              </>
            )}
          </h1>
          <p className="lead m-0">
            {isPt
              ? 'Lully 1661 começou em Marvila, em 2022, com um forno e uma ideia: que o pão pode ser feito devagar, com farinha boa, e ainda assim caber no orçamento de um bairro.'
              : 'Lully 1661 began in Marvila, in 2022, with one oven and one idea: that bread can be made slowly, with good flour, and still fit a neighbourhood budget.'}
          </p>
        </div>
        <figure className="m-0 text-center">
          <Image
            src="/brand/sub-meunier.jpg"
            alt={isPt ? 'Le Meunier — sub-marca Lully' : 'Le Meunier — Lully sub-mark'}
            width={400}
            height={564}
            sizes="(min-width: 768px) 400px, 70vw"
            className="max-h-[480px] w-auto mx-auto"
            priority
          />
        </figure>
      </Container>

      {/* THE NAME */}
      <Container
        as="section"
        className="py-14 border-b border-[rgba(26,22,19,0.14)] grid gap-14 md:grid-cols-[1fr_1.4fr]"
      >
        <h3
          className="text-[30px] m-0"
          style={{ fontWeight: 400, fontVariationSettings: '"opsz" 72' }}
        >
          {isPt ? (
            <>
              O nome, <em>e o ano.</em>
            </>
          ) : (
            <>
              The name, <em>and the year.</em>
            </>
          )}
        </h3>
        <div className="text-[16px] text-[color:var(--color-ink-2)] leading-[1.6]">
          <p className="m-0 mb-3">
            {isPt
              ? 'Jean-Baptiste Lully — italiano de nascimento, francês por escolha — foi o compositor da corte de Luís XIV. Em 1661, foi-lhe concedida a cidadania francesa e foi nomeado Superintendente da Música Real. Tinha 28 anos.'
              : 'Jean-Baptiste Lully — Italian-born, French by choice — was the court composer to Louis XIV. In 1661, he was granted French citizenship and made Superintendent of the Royal Music. He was 28.'}
          </p>
          <p className="m-0">
            {isPt
              ? 'Lully empurrou a ópera barroca para um sítio onde ainda não tinha estado. Não rasgou a tradição — re-assinou-a. É essa a ambição da nossa padaria.'
              : "Lully pushed Baroque opera somewhere it hadn't been. He didn't tear up tradition — he re-signed it. That is our bakery's ambition, too."}
          </p>
        </div>
      </Container>

      {/* PHILOSOPHY — three concrete commitments */}
      <Container as="section" className="py-16 border-b border-[rgba(26,22,19,0.14)]">
        <Eyebrow>{isPt ? 'A casa, em três pontos' : 'The house, in three notes'}</Eyebrow>
        <h2 className="display-md mt-3 mb-10 max-w-[24ch]">
          {isPt ? (
            <>
              Específico, <em>nunca superlativo.</em>
            </>
          ) : (
            <>
              Specific, <em>never superlative.</em>
            </>
          )}
        </h2>
        <div className="grid gap-8 md:grid-cols-3">
          {[
            {
              title: isPt ? '48 horas' : '48 hours',
              body: isPt
                ? 'Os nossos pães fermentam 18 horas a temperatura ambiente, 30 horas a frio. Ao todo, dois dias antes de irem ao forno. É o que dá àquela miga que parece renda.'
                : "Our breads ferment 18 hours at room temperature, then 30 hours cold. Two days before they reach the oven. It's what gives the crumb the look of lace.",
            },
            {
              title: isPt ? 'Mâconnais' : 'Mâconnais',
              body: isPt
                ? 'Trazemos a farinha duas vezes por mês de Mâconnais, no centro-leste de França. Trigo orgânico, mó-de-pedra, três moagens (branca, semi-integral, centeio). É a única matéria-prima que importamos.'
                : "Twice a month, our flour comes from Mâconnais, in central-eastern France. Organic wheat, stone-milled, three grinds (white, semi-whole, rye). It's the only raw material we import.",
            },
            {
              title: isPt ? 'Uma família, três casas' : 'One family, three houses',
              body: isPt
                ? 'Yann, Alain e Franck — três franceses, em Lisboa há mais de uma década. Abriram o Beato em 2022, Anjos no ano seguinte, Campo de Ourique no verão de 2025. O forno é em Marvila; sai de lá tudo o que se vende nas três lojas.'
                : 'Yann, Alain and Franck — three Frenchmen, in Lisbon for over a decade. Beato opened in 2022, Anjos the year after, Campo de Ourique in the summer of 2025. The oven is in Marvila; everything sold across the three stores comes out of there.',
            },
          ].map((point) => (
            <div key={point.title}>
              <h4
                className="text-[24px] mb-3"
                style={{ fontWeight: 400, fontVariationSettings: '"opsz" 60' }}
              >
                {point.title}
              </h4>
              <p className="text-[15px] text-[color:var(--color-ink-2)] m-0 leading-[1.6]">
                {point.body}
              </p>
            </div>
          ))}
        </div>
      </Container>

      {/* CTA */}
      <Container as="section" className="py-16 text-center">
        <p
          className="text-[24px] m-0 mb-7"
          style={{
            fontFamily: 'var(--font-serif-accent)',
            fontStyle: 'italic',
            color: 'var(--color-gold)',
          }}
        >
          {isPt
            ? 'A próxima fornada sai dentro de poucas horas.'
            : 'The next bake is a few hours away.'}
        </p>
        <div className="flex gap-3 justify-center flex-wrap">
          <LocalizedLink href="/lojas" className={buttonClassName({ variant: 'primary' })}>
            {isPt ? 'Visitar uma loja' : 'Visit a store'}
          </LocalizedLink>
          <LocalizedLink href="/menu/brunch" className={buttonClassName({ variant: 'ghost' })}>
            {isPt ? 'Ver o brunch →' : 'See the brunch →'}
          </LocalizedLink>
        </div>
      </Container>
    </>
  );
}

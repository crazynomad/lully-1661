import { buttonClassName } from '@/components/Button';
import { Container } from '@/components/Container';
import { Eyebrow } from '@/components/Eyebrow';
import { JsonLd } from '@/components/JsonLd';
import { LocalizedLink } from '@/components/LocalizedLink';
import { SectionTitle } from '@/components/SectionTitle';
import { getBrunchByMovement, menuItemImagePath } from '@/features/menu';
import { isLocale } from '@/lib/i18n/routing';
import { breadcrumbJsonLd } from '@/lib/jsonld/breadcrumb';
import { menuItemJsonLd } from '@/lib/jsonld/menuItem';
import { seo } from '@/lib/seo';
import type { Metadata } from 'next';
import { setRequestLocale } from 'next-intl/server';
import Image from 'next/image';
import { notFound } from 'next/navigation';

const SITE_URL = process.env.NEXT_PUBLIC_SITE_URL ?? 'https://lully1661.com';

export async function generateStaticParams() {
  return [{ locale: 'pt' }, { locale: 'en' }];
}

export async function generateMetadata({
  params,
}: { params: Promise<{ locale: string }> }): Promise<Metadata> {
  const { locale } = await params;
  if (!isLocale(locale)) return {};
  return seo({
    title: 'Brunch · Anjos',
    description:
      locale === 'pt'
        ? 'O nosso brunch — servido apenas em Anjos, todas as manhãs. Ovos, tostas, doces, e o que o mercado nos der esta semana.'
        : 'Our brunch — served only at Anjos, every morning. Eggs, toasts, sweet, and whatever the market gives us this week.',
    path: '/menu/brunch',
    locale,
  });
}

export default async function BrunchPage({ params }: { params: Promise<{ locale: string }> }) {
  const { locale } = await params;
  if (!isLocale(locale)) notFound();
  setRequestLocale(locale);

  const movements = await getBrunchByMovement('anjos', locale);

  // Schema.org Menu + per-item MenuItem entries, plus breadcrumb,
  // composed into a single @graph.
  const menuJsonLd = {
    '@context': 'https://schema.org',
    '@graph': [
      {
        '@type': 'Menu',
        '@id': `${SITE_URL}/${locale}/menu/brunch#menu`,
        name: locale === 'pt' ? 'Brunch — Anjos' : 'Brunch — Anjos',
        provider: { '@id': `${SITE_URL}/${locale}/lojas/anjos#store` },
        hasMenuSection: movements.map((m) => ({
          '@type': 'MenuSection',
          name: m.label,
          hasMenuItem: m.items.map((item) =>
            stripContext(
              menuItemJsonLd({
                name: item.entry.name[locale],
                description: item.entry.description[locale],
                image: `${SITE_URL}${menuItemImagePath(item.slug)}`,
                suitableForDiet: item.entry.suitableForDiet
                  .filter((d): d is 'vegan' | 'vegetarian' | 'glutenFree' =>
                    ['vegan', 'vegetarian', 'glutenFree'].includes(d),
                  )
                  .map((d) =>
                    d === 'vegan'
                      ? 'VeganDiet'
                      : d === 'vegetarian'
                        ? 'VegetarianDiet'
                        : 'GlutenFreeDiet',
                  ),
              }),
            ),
          ),
        })),
      },
      stripContext(
        breadcrumbJsonLd([
          {
            name: locale === 'pt' ? 'Início' : 'Home',
            url: `${SITE_URL}/${locale}`,
          },
          {
            name: locale === 'pt' ? 'Menu' : 'Menu',
            url: `${SITE_URL}/${locale}/menu`,
          },
          {
            name: 'Brunch',
            url: `${SITE_URL}/${locale}/menu/brunch`,
          },
        ]),
      ),
    ],
  };

  return (
    <>
      <JsonLd data={menuJsonLd} />

      {/* HERO */}
      <Container
        as="section"
        className="grid gap-14 md:grid-cols-[1.1fr_1fr] items-center py-18 border-b border-[rgba(26,22,19,0.14)]"
      >
        <div>
          <span
            className="inline-block text-[11px] tracking-[0.22em] uppercase mb-5 px-3 py-1.5"
            style={{ background: 'var(--color-ember)', color: 'var(--color-paper)' }}
          >
            {locale === 'pt' ? 'Lançamento · 15 Maio 2026' : 'Launching · 15 May 2026'}
          </span>
          <h1 className="display-lg mb-4">
            {locale === 'pt' ? (
              <>
                O nosso brunch. <em style={{ color: 'var(--color-gold)' }}>Servido em Anjos,</em>{' '}
                toda a manhã.
              </>
            ) : (
              <>
                Our brunch. <em style={{ color: 'var(--color-gold)' }}>Served at Anjos,</em> all
                morning.
              </>
            )}
          </h1>
          <p className="text-[17px] text-[color:var(--color-ink-2)] max-w-[48ch] leading-[1.6] m-0">
            {locale === 'pt'
              ? 'Um menu construído à volta do nosso pão, das nossas pastelarias, da farinha mó-de-pedra, ovos do campo, e do que o mercado nos dá esta semana. Ter–Dom, das 8h30 às 12h30. Reserva recomendada.'
              : 'A menu built around our own breads and pastries, stone-milled flour, free-range eggs, and what the market gives us that week. Tue–Sun, from 8:30 to 12:30. Reservation recommended.'}
          </p>
          <div className="mt-7 flex gap-3">
            <LocalizedLink href="/reservas" className={buttonClassName({ variant: 'ember' })}>
              {locale === 'pt' ? 'Reservar mesa' : 'Reserve a table'}
            </LocalizedLink>
            <LocalizedLink
              href={{ pathname: '/lojas/[slug]', params: { slug: 'anjos' } }}
              className={buttonClassName({ variant: 'ghost' })}
            >
              {locale === 'pt' ? 'Encontrar Anjos →' : 'Find Anjos →'}
            </LocalizedLink>
          </div>
        </div>
        <figure className="m-0 text-center">
          <Image
            src="/brand/sub-patissiere.jpg"
            alt={
              locale === 'pt' ? 'La Pâtissière — sub-marca Lully' : 'La Pâtissière — Lully sub-mark'
            }
            width={400}
            height={540}
            sizes="(min-width: 768px) 400px, 70vw"
            className="max-h-[480px] w-auto mx-auto"
            priority
          />
        </figure>
      </Container>

      {/* WHY BRUNCH, NOW */}
      <Container
        as="section"
        className="py-14 border-b border-[rgba(26,22,19,0.14)] grid gap-14 md:grid-cols-[1fr_1.4fr]"
      >
        <h3
          className="text-[30px] m-0"
          style={{ fontWeight: 400, fontVariationSettings: '"opsz" 72' }}
        >
          {locale === 'pt' ? (
            <>
              Porquê brunch, <em>agora.</em>
            </>
          ) : (
            <>
              Why brunch, <em>now.</em>
            </>
          )}
        </h3>
        <div>
          <p className="text-[16px] text-[color:var(--color-ink-2)] leading-[1.6] mb-3 m-0">
            {locale === 'pt'
              ? 'Quatro anos de pão e pastelaria. Uma loja em Anjos com cozinha a sério, um pass a sério, e o forno mesmo no centro da sala. O passo natural seguinte.'
              : 'Four years of bread and pastry. A flagship in Anjos with a proper kitchen, a proper pass, and the oven right there at the heart of the room. The next natural step.'}
          </p>
          <p className="text-[16px] text-[color:var(--color-ink-2)] leading-[1.6] m-0">
            {locale === 'pt'
              ? 'O brunch é como queremos que conheças a totalidade do que cozemos — num prato, com um ovo em cima, ao lado de algo que acabou de sair do forno. Cada prato do menu usa algo feito em casa.'
              : 'Brunch is how we want you to meet the full range of what we bake — on a plate, with an egg on top, next to something we just pulled from the oven. Every dish on the menu uses something made in-house.'}
          </p>
        </div>
      </Container>

      {/* THE MENU */}
      <Container as="section" className="py-16">
        <SectionTitle size={40}>
          {locale === 'pt' ? (
            <>
              O menu, <em>em quatro movimentos.</em>
            </>
          ) : (
            <>
              The menu, <em>in four movements.</em>
            </>
          )}
        </SectionTitle>
        <div className="mt-10 grid gap-10">
          {movements.map((movement) => (
            <div key={movement.course}>
              <Eyebrow className="block border-b border-[rgba(26,22,19,0.14)] pb-2 mb-4">
                {movement.label}
              </Eyebrow>
              <ul className="list-none p-0 m-0">
                {movement.items.map((item, idx) => (
                  <li
                    key={item.slug}
                    className="grid gap-5 items-center py-3.5 grid-cols-[90px_1fr_auto]"
                    style={{
                      borderBottom:
                        idx === movement.items.length - 1
                          ? 'none'
                          : '1px dashed rgba(26,22,19,0.14)',
                    }}
                  >
                    <Image
                      src={menuItemImagePath(item.slug)}
                      alt=""
                      width={90}
                      height={70}
                      className="w-[90px] h-[70px] object-cover"
                    />
                    <div>
                      <h4
                        className="text-[21px] m-0 mb-1"
                        style={{ fontWeight: 400, fontVariationSettings: '"opsz" 48' }}
                      >
                        {item.entry.name[locale]}
                      </h4>
                      <p className="text-[14px] text-[color:var(--color-ink-2)] m-0 leading-[1.5]">
                        {item.entry.description[locale]}
                      </p>
                    </div>
                    <div className="price">{item.price}</div>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
        <p className="text-[12px] text-[color:var(--color-stone)] mt-10 m-0">
          {locale === 'pt'
            ? 'Os pratos rodam consoante o mercado e a estação. Pode haver substituições.'
            : 'Dishes rotate with the market and season. Substitutions may apply.'}
        </p>
      </Container>

      {/* DARK CTA */}
      <section
        className="text-center px-10 py-16"
        style={{ background: 'var(--color-ink)', color: 'var(--color-paper)' }}
      >
        <h3 className="display-md m-0 mb-2" style={{ color: 'var(--color-paper)' }}>
          {locale === 'pt' ? (
            <>
              Uma mesa, <em style={{ color: 'var(--color-gold-2)' }}>e depois pequeno-almoço.</em>
            </>
          ) : (
            <>
              A table, <em style={{ color: 'var(--color-gold-2)' }}>then breakfast.</em>
            </>
          )}
        </h3>
        <p
          className="text-[18px] m-0 mb-7"
          style={{
            fontFamily: 'var(--font-serif-accent)',
            fontStyle: 'italic',
            color: 'var(--color-gold-2)',
          }}
        >
          {locale === 'pt' ? 'Ter–Dom · 8h30 – 12h30 · Anjos' : 'Tue–Sun · 8:30 – 12:30 · Anjos'}
        </p>
        <LocalizedLink href="/reservas" className={buttonClassName({ variant: 'ember' })}>
          {locale === 'pt' ? 'Reservar mesa' : 'Reserve a table'}
        </LocalizedLink>
      </section>
    </>
  );
}

function stripContext<T extends { '@context'?: unknown }>(obj: T): Omit<T, '@context'> {
  const { '@context': _ignored, ...rest } = obj;
  return rest;
}

import { buttonClassName } from '@/components/Button';
import { Container } from '@/components/Container';
import { Eyebrow } from '@/components/Eyebrow';
import { LocalizedLink } from '@/components/LocalizedLink';
import { isLocale } from '@/lib/i18n/routing';
import { seo } from '@/lib/seo';
import type { Metadata } from 'next';
import { setRequestLocale } from 'next-intl/server';
import { notFound } from 'next/navigation';

const HR_EMAIL = 'hr@lully1661.com';

export async function generateStaticParams() {
  return [{ locale: 'pt' }, { locale: 'en' }];
}

export async function generateMetadata({
  params,
}: { params: Promise<{ locale: string }> }): Promise<Metadata> {
  const { locale } = await params;
  if (!isLocale(locale)) return {};
  return seo({
    title: locale === 'pt' ? 'Trabalha connosco' : 'Careers',
    description:
      locale === 'pt'
        ? 'Padaria, pastelaria, balcão. Lisboa. Posições recorrentes — falamos sempre que houver pão.'
        : "Bakery, pastry, counter. Lisbon. Recurring positions — we talk whenever there's bread.",
    path: '/trabalha-connosco',
    locale,
  });
}

export default async function CareersPage({ params }: { params: Promise<{ locale: string }> }) {
  const { locale } = await params;
  if (!isLocale(locale)) notFound();
  setRequestLocale(locale);

  const isPt = locale === 'pt';

  return (
    <>
      {/* HERO */}
      <Container
        as="section"
        className="py-18 border-b border-[rgba(26,22,19,0.14)] max-w-[820px] mx-auto"
      >
        <Eyebrow>{isPt ? 'Trabalha connosco' : 'Careers'}</Eyebrow>
        <h1 className="display-lg mt-3.5 mb-4">
          {isPt ? (
            <>
              Há sempre lugar <em>à mesa.</em>
            </>
          ) : (
            <>
              There's always a seat <em>at the bench.</em>
            </>
          )}
        </h1>
        <p className="lead m-0">
          {isPt
            ? 'Procuramos pessoas que gostam de pão a sério, que se interessam pelo que sai do forno às cinco da manhã, que ficam à mesa por mais um café. Não publicamos vagas — falamos sempre que houver alguém certo.'
            : "We look for people who love serious bread, who care about what comes out of the oven at five in the morning, who stay at the table for one more coffee. We don't publish vacancies — we talk whenever someone fits."}
        </p>
      </Container>

      {/* WHAT WE LOOK FOR */}
      <Container
        as="section"
        className="py-16 border-b border-[rgba(26,22,19,0.14)] max-w-[820px] mx-auto"
      >
        <Eyebrow>{isPt ? 'O que importa' : 'What matters'}</Eyebrow>
        <h2 className="display-md mt-3 mb-8 max-w-[24ch]">
          {isPt ? (
            <>
              Específico, <em>nunca genérico.</em>
            </>
          ) : (
            <>
              Specific, <em>never generic.</em>
            </>
          )}
        </h2>
        <div className="text-[16px] text-[color:var(--color-ink-2)] leading-[1.6] space-y-4 max-w-[60ch]">
          <p className="m-0">
            {isPt
              ? 'Mãos limpas. Curiosidade. Vontade de explicar a um cliente, em três frases, porque é que o pão custa cinco euros e meio.'
              : 'Clean hands. Curiosity. Willingness to explain to a customer, in three sentences, why the bread costs €5.50.'}
          </p>
          <p className="m-0">
            {isPt
              ? 'Inglês ou francês são bem-vindos, português é vantagem. A maioria da equipa é multilingue — em Anjos é frequente passar de PT a EN a FR no mesmo turno.'
              : "English or French welcome, Portuguese a plus. Most of the team is multilingual — at Anjos it's common to switch from PT to EN to FR in the same shift."}
          </p>
          <p className="m-0">
            {isPt
              ? 'Salário acima da média da indústria, horários de padaria (cedo), férias decentes. Estágios pagos para pastelaria.'
              : 'Above-industry salary, bakery hours (early), decent vacation. Paid pastry internships.'}
          </p>
        </div>
      </Container>

      {/* RECURRING ROLES */}
      <Container
        as="section"
        className="py-16 border-b border-[rgba(26,22,19,0.14)] max-w-[820px] mx-auto"
      >
        <Eyebrow>{isPt ? 'Posições recorrentes' : 'Recurring positions'}</Eyebrow>
        <h2 className="display-md mt-3 mb-8 max-w-[24ch]">
          {isPt ? (
            <>
              Sem vagas <em>abertas em concreto.</em>
            </>
          ) : (
            <>
              No specific <em>open vacancies.</em>
            </>
          )}
        </h2>
        <ul className="list-none p-0 m-0 grid gap-6 md:grid-cols-2 max-w-[60ch]">
          {[
            {
              title: isPt ? 'Padeiro/a' : 'Baker',
              loc: 'Beato',
              body: isPt
                ? 'Turno da madrugada (4h–12h). Centeio, sourdough, viennoiserie. Falamos sempre.'
                : 'Early shift (4am–12pm). Rye, sourdough, viennoiserie. Always recruiting.',
            },
            {
              title: isPt ? 'Pasteleiro/a' : 'Pastry',
              loc: 'Beato',
              body: isPt
                ? 'Tartes, choux, viennoiserie. Estagiários bem-vindos, formação interna.'
                : 'Tarts, choux, viennoiserie. Interns welcome, internal training.',
            },
            {
              title: isPt ? 'Balcão · Anjos' : 'Counter · Anjos',
              loc: 'Anjos',
              body: isPt
                ? 'Atendimento, café, brunch service. Inglês a sério. Turnos de manhã e tarde.'
                : 'Service, coffee, brunch service. Solid English. Morning and afternoon shifts.',
            },
            {
              title: isPt ? 'Balcão · bairro' : 'Counter · neighbourhood',
              loc: 'Campo de Ourique',
              body: isPt
                ? 'Loja pequena, ritmo lento, clientes regulares. Para quem prefere o bairro à correria.'
                : 'Small shop, slow rhythm, regulars. For those who prefer neighbourhood to rush.',
            },
          ].map((role) => (
            <li key={role.title} className="border border-[rgba(26,22,19,0.14)] p-5">
              <p className="meta m-0 mb-2">{role.loc}</p>
              <h3
                className="text-[22px] m-0 mb-2"
                style={{ fontWeight: 400, fontVariationSettings: '"opsz" 48' }}
              >
                {role.title}
              </h3>
              <p className="text-[14px] text-[color:var(--color-ink-2)] m-0 leading-[1.5]">
                {role.body}
              </p>
            </li>
          ))}
        </ul>
      </Container>

      {/* CTA */}
      <Container as="section" className="py-16 text-center max-w-[640px] mx-auto">
        <p className="kicker mb-3" style={{ fontSize: '24px' }}>
          {isPt
            ? 'Manda CV, três linhas de carta, fotografia se quiseres.'
            : 'Send a CV, three lines of cover letter, a photo if you want.'}
        </p>
        <p className="text-[15px] text-[color:var(--color-ink-2)] leading-[1.6] m-0 mb-7">
          {isPt
            ? 'Lemos tudo. Respondemos em uma semana, mesmo quando é não.'
            : "We read everything. We reply within a week, even when it's no."}
        </p>
        <div className="flex gap-3 justify-center flex-wrap">
          <a
            href={`mailto:${HR_EMAIL}?subject=${encodeURIComponent(isPt ? 'Candidatura espontânea' : 'Open application')}`}
            className={buttonClassName({ variant: 'ember' })}
          >
            {isPt ? 'Enviar candidatura' : 'Send application'}
          </a>
          <LocalizedLink href="/sobre" className={buttonClassName({ variant: 'ghost' })}>
            {isPt ? 'Sobre a casa →' : 'About the house →'}
          </LocalizedLink>
        </div>
        <p className="meta mt-6">
          {isPt ? `Ou diretamente para ${HR_EMAIL}` : `Or directly at ${HR_EMAIL}`}
        </p>
      </Container>
    </>
  );
}

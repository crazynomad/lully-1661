import { Container } from '@/components/Container';
import { Eyebrow } from '@/components/Eyebrow';
import { isLocale } from '@/lib/i18n/routing';
import { seo } from '@/lib/seo';
import type { Metadata } from 'next';
import { setRequestLocale } from 'next-intl/server';
import { notFound } from 'next/navigation';

const COMPLAINTS_URL = 'https://www.livroreclamacoes.pt/';
const PRIVACY_EMAIL = 'privacy@lully1661.com';

export async function generateStaticParams() {
  return [{ locale: 'pt' }, { locale: 'en' }];
}

export async function generateMetadata({
  params,
}: { params: Promise<{ locale: string }> }): Promise<Metadata> {
  const { locale } = await params;
  if (!isLocale(locale)) return {};
  return seo({
    title: locale === 'pt' ? 'Legal' : 'Legal',
    description:
      locale === 'pt'
        ? 'Termos, privacidade, cookies, livro de reclamações.'
        : 'Terms, privacy, cookies, complaints book.',
    path: '/legal',
    locale,
  });
}

export default async function LegalPage({ params }: { params: Promise<{ locale: string }> }) {
  const { locale } = await params;
  if (!isLocale(locale)) notFound();
  setRequestLocale(locale);

  const isPt = locale === 'pt';
  const sections = isPt ? SECTIONS_PT : SECTIONS_EN;

  return (
    <Container as="main" size="narrow" className="py-18">
      <Eyebrow>{isPt ? 'Legal' : 'Legal'}</Eyebrow>
      <h1 className="display-md mt-3 mb-2">
        {isPt ? (
          <>
            O <em>aviso legal.</em>
          </>
        ) : (
          <>
            The <em>fine print.</em>
          </>
        )}
      </h1>
      <p className="meta m-0 mb-10">
        {isPt ? 'Última actualização: 9 Maio 2026' : 'Last updated: 9 May 2026'}
      </p>

      <nav
        aria-label={isPt ? 'Índice' : 'Table of contents'}
        className="mb-12 border-b border-[rgba(26,22,19,0.14)] pb-6"
      >
        <ul className="list-none p-0 m-0 flex flex-wrap gap-x-6 gap-y-2 text-[12px] tracking-[0.18em] uppercase text-[color:var(--color-stone)]">
          {sections.map((s) => (
            <li key={s.id}>
              <a
                href={`#${s.id}`}
                className="hover:text-[color:var(--color-ember)] transition-colors"
              >
                {s.title}
              </a>
            </li>
          ))}
        </ul>
      </nav>

      <div className="space-y-12">
        {sections.map((section) => (
          <section key={section.id} id={section.id}>
            <h2
              className="text-[26px] m-0 mb-4"
              style={{ fontWeight: 400, fontVariationSettings: '"opsz" 60' }}
            >
              {section.title}
            </h2>
            <div className="text-[15px] text-[color:var(--color-ink-2)] leading-[1.7] space-y-3">
              {section.body.map((paragraph) => (
                <p key={paragraph.slice(0, 32)} className="m-0">
                  {paragraph}
                </p>
              ))}
            </div>
          </section>
        ))}
      </div>

      <div className="mt-16 border-t border-[rgba(26,22,19,0.14)] pt-8 text-[14px] text-[color:var(--color-stone)] leading-[1.7]">
        <p className="m-0">
          {isPt ? (
            <>
              Para o livro de reclamações electrónico, consulte{' '}
              <a
                href={COMPLAINTS_URL}
                target="_blank"
                rel="noopener noreferrer"
                className="text-[color:var(--color-accent)] hover:underline underline-offset-4"
              >
                livroreclamacoes.pt
              </a>
              . Para questões de privacidade, escreva para{' '}
              <a
                href={`mailto:${PRIVACY_EMAIL}`}
                className="text-[color:var(--color-accent)] hover:underline underline-offset-4"
              >
                {PRIVACY_EMAIL}
              </a>
              .
            </>
          ) : (
            <>
              For the electronic complaints book, see{' '}
              <a
                href={COMPLAINTS_URL}
                target="_blank"
                rel="noopener noreferrer"
                className="text-[color:var(--color-accent)] hover:underline underline-offset-4"
              >
                livroreclamacoes.pt
              </a>
              . For privacy enquiries, write to{' '}
              <a
                href={`mailto:${PRIVACY_EMAIL}`}
                className="text-[color:var(--color-accent)] hover:underline underline-offset-4"
              >
                {PRIVACY_EMAIL}
              </a>
              .
            </>
          )}
        </p>
      </div>

      <p
        className="meta mt-12 text-[color:var(--color-stone)] italic"
        style={{
          fontFamily: 'var(--font-serif-accent)',
          textTransform: 'none',
          letterSpacing: 'normal',
          fontSize: '13px',
        }}
      >
        {isPt
          ? 'Este texto é o conteúdo de demonstração. A versão final é redigida pelo nosso advogado antes do lançamento.'
          : 'This is demo copy. The final text is drafted by our counsel before launch.'}
      </p>
    </Container>
  );
}

type Section = { id: string; title: string; body: string[] };

const SECTIONS_PT: Section[] = [
  {
    id: 'termos',
    title: 'Termos & condições',
    body: [
      'A Lully 1661 é uma marca comercial detida pela Lully Boulangerie Lda., com sede em Lisboa, Portugal. Estes termos aplicam-se à utilização do site lully1661.com e à compra de produtos e serviços.',
      'Os preços indicados no site incluem IVA à taxa em vigor. Encomendas online são confirmadas por email após processamento do pagamento. As reservas de mesa em Anjos podem ser canceladas até duas horas antes do horário marcado, sem custo.',
      'Os produtos artesanais variam ligeiramente em forma e peso. Imagens no site são ilustrativas. Quando um produto deixar de estar disponível, devolvemos o valor correspondente nas vinte e quatro horas seguintes.',
    ],
  },
  {
    id: 'privacidade',
    title: 'Privacidade',
    body: [
      'Recolhemos dados pessoais apenas quando necessário para servir uma encomenda, processar uma reserva, enviar a newsletter, ou responder a um pedido de candidatura. Não vendemos nem partilhamos dados com terceiros para fins comerciais.',
      'Os direitos do RGPD aplicam-se na íntegra: acesso, rectificação, apagamento, oposição, portabilidade. Para exercer qualquer direito, escreva para privacy@lully1661.com — respondemos no prazo de trinta dias.',
      'Os dados de candidaturas são apagados doze meses após a última interacção, salvo pedido em contrário. Os dados de encomendas são mantidos pelo prazo legal exigido pela autoridade tributária portuguesa.',
    ],
  },
  {
    id: 'cookies',
    title: 'Cookies',
    body: [
      'Usamos cookies essenciais para o funcionamento do site (sessão, idioma, carrinho de compras). Não usamos cookies de rastreio ou de publicidade comportamental.',
      'Os cookies de análise (Vercel Analytics) são anónimos e podem ser desactivados nas preferências do browser sem afectar o uso do site.',
    ],
  },
  {
    id: 'reclamacoes',
    title: 'Livro de reclamações',
    body: [
      'O livro de reclamações electrónico está disponível em livroreclamacoes.pt. Reclamações em loja podem ser feitas no livro físico de cada uma das três casas (Anjos, Campo de Ourique, Beato) — entregamos sempre folha em duplicado.',
      'A entidade de resolução alternativa de litígios competente é o CNIACC — Centro Nacional de Informação e Arbitragem de Conflitos de Consumo.',
    ],
  },
];

const SECTIONS_EN: Section[] = [
  {
    id: 'terms',
    title: 'Terms & conditions',
    body: [
      'Lully 1661 is a trademark owned by Lully Boulangerie Lda., headquartered in Lisbon, Portugal. These terms apply to the use of lully1661.com and to the purchase of products and services.',
      'Prices on the site include VAT at the applicable rate. Online orders are confirmed by email after payment processing. Table reservations at Anjos may be cancelled up to two hours before the booked time, free of charge.',
      'Artisanal products vary slightly in shape and weight. Site images are illustrative. When a product becomes unavailable, we refund the corresponding amount within twenty-four hours.',
    ],
  },
  {
    id: 'privacy',
    title: 'Privacy',
    body: [
      'We collect personal data only when needed to fulfil an order, process a reservation, send the newsletter, or respond to a job application. We do not sell or share data with third parties for commercial purposes.',
      'GDPR rights apply in full: access, rectification, erasure, objection, portability. To exercise any right, write to privacy@lully1661.com — we reply within thirty days.',
      'Application data is deleted twelve months after the last interaction, unless you request otherwise. Order data is kept for the period required by the Portuguese tax authority.',
    ],
  },
  {
    id: 'cookies',
    title: 'Cookies',
    body: [
      'We use essential cookies for site functionality (session, language, cart). We do not use tracking or behavioural advertising cookies.',
      'Analytics cookies (Vercel Analytics) are anonymous and can be disabled in browser preferences without affecting site use.',
    ],
  },
  {
    id: 'complaints',
    title: 'Complaints book',
    body: [
      'The electronic complaints book is available at livroreclamacoes.pt. In-store complaints may be made in the physical book at each of our three houses (Anjos, Campo de Ourique, Beato) — we always provide a duplicate copy.',
      'The competent alternative dispute resolution entity is CNIACC — the Portuguese National Centre for Consumer Information and Arbitration.',
    ],
  },
];

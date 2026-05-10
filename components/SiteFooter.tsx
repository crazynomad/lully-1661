import { Brand } from '@/components/Brand';
import { LocalizedLink } from '@/components/LocalizedLink';
import type { Locale } from '@/lib/i18n/routing';
import { getTranslations } from 'next-intl/server';

// Dark footer per the Lully 1661 design system § Footer: solid Ink
// background, paper text, gold-2 accents, four-column grid (brand /
// visit / discover / newsletter), legal strip below.

export async function SiteFooter({ locale }: { locale: Locale }) {
  const t = await getTranslations({ locale });
  const tagline =
    locale === 'pt' ? 'Tradição, re-assinada em 2026.' : 'Tradition, re-signed in 2026.';

  return (
    <footer className="bg-[color:var(--color-ink)] text-[color:var(--color-paper)] px-5 sm:px-8 md:px-10 pt-14 pb-7">
      <div className="grid gap-10 md:grid-cols-[1.2fr_1fr_1fr_1.2fr] max-w-[1280px] mx-auto mb-8">
        <div>
          <Brand size="lg" surface="on-dark" />
          <p
            className="mt-3 max-w-[28ch] text-[17px]"
            style={{
              fontFamily: 'var(--font-serif-accent)',
              fontStyle: 'italic',
              color: 'var(--color-gold-2)',
            }}
          >
            {tagline}
          </p>
          <a
            href="https://www.instagram.com/lully1661_lisboa/"
            target="_blank"
            rel="noopener noreferrer"
            className="mt-5 inline-flex items-center gap-2 text-[12px] tracking-[0.18em] uppercase text-[color:var(--color-gold-2)] hover:text-[color:var(--color-paper)] transition-colors"
          >
            <InstagramGlyph />
            <span>@lully1661_lisboa</span>
          </a>
        </div>

        <div>
          <FooterHeading>{locale === 'pt' ? 'Visitar' : 'Visit'}</FooterHeading>
          <ul className="list-none p-0 m-0">
            <FooterLi>
              <LocalizedLink href={{ pathname: '/lojas/[slug]', params: { slug: 'anjos' } }}>
                Anjos
              </LocalizedLink>
            </FooterLi>
            <FooterLi>
              <LocalizedLink
                href={{ pathname: '/lojas/[slug]', params: { slug: 'campo-de-ourique' } }}
              >
                Campo de Ourique
              </LocalizedLink>
            </FooterLi>
            <FooterLi>
              <LocalizedLink href={{ pathname: '/lojas/[slug]', params: { slug: 'beato' } }}>
                Beato
              </LocalizedLink>
            </FooterLi>
            <FooterLi>
              <LocalizedLink href="/reservas">{t('nav.reservations')}</LocalizedLink>
            </FooterLi>
          </ul>
        </div>

        <div>
          <FooterHeading>{locale === 'pt' ? 'Descobrir' : 'Discover'}</FooterHeading>
          <ul className="list-none p-0 m-0">
            <FooterLi>
              <LocalizedLink href="/menu">{t('nav.menu')}</LocalizedLink>
            </FooterLi>
            <FooterLi>
              <LocalizedLink href="/menu/brunch">Brunch</LocalizedLink>
            </FooterLi>
            <FooterLi>
              <LocalizedLink href="/encomendas">{t('nav.festiveOrders')}</LocalizedLink>
            </FooterLi>
            <FooterLi>
              <LocalizedLink href="/lully-inside">{t('nav.lullyInside')}</LocalizedLink>
            </FooterLi>
            <FooterLi>
              <LocalizedLink href="/sobre">{t('nav.about')}</LocalizedLink>
            </FooterLi>
          </ul>
        </div>

        <div>
          <FooterHeading>Newsletter</FooterHeading>
          <p className="text-[13px] m-0 text-[rgba(244,238,223,0.75)] leading-relaxed">
            {locale === 'pt'
              ? 'Cartas ocasionais — pães novos, menus de estação, acesso antecipado a encomendas festivas.'
              : 'Occasional letters — new breads, seasonal menus, early access to festive orders.'}
          </p>
          <input
            type="email"
            placeholder={locale === 'pt' ? 'o seu email' : 'your email address'}
            className="bg-transparent border-0 border-b border-[rgba(244,238,223,0.4)] text-[color:var(--color-paper)] py-2 px-0 mt-2 font-[family-name:var(--font-body)] text-[14px] w-full outline-none placeholder:text-[rgba(244,238,223,0.45)] transition-[border-color] duration-[160ms] ease-[var(--ease-out)] focus:border-[color:var(--color-gold-2)]"
            aria-label={
              locale === 'pt' ? 'Endereço de email para newsletter' : 'Email address for newsletter'
            }
          />
        </div>
      </div>

      <div className="border-t border-[rgba(244,238,223,0.14)] pt-5 flex flex-col sm:flex-row sm:justify-between gap-2 max-w-[1280px] mx-auto text-[11px] tracking-[0.1em] text-[rgba(244,238,223,0.45)]">
        <span>
          © 2026 lully 1661 · Lisboa ·{' '}
          <a
            href="https://www.livroreclamacoes.pt/"
            target="_blank"
            rel="noopener noreferrer"
            className="hover:text-[color:var(--color-gold-2)] transition-colors"
          >
            Livro de Reclamações
          </a>
        </span>
        <span>
          <LocalizedLink href="/legal" className="hover:text-[color:var(--color-gold-2)]">
            {t('nav.legal')}
          </LocalizedLink>
        </span>
      </div>
    </footer>
  );
}

function FooterHeading({ children }: { children: React.ReactNode }) {
  return (
    <h5 className="text-[11px] tracking-[0.2em] uppercase text-[color:var(--color-gold-2)] m-0 mb-3.5 font-medium">
      {children}
    </h5>
  );
}

// Inline Instagram glyph — square camera. Stroke 1.5 to match the
// design system § iconography spec for Lucide-style icons.
function InstagramGlyph() {
  return (
    <svg
      width="16"
      height="16"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.5"
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
    >
      <rect x="3" y="3" width="18" height="18" rx="4" />
      <circle cx="12" cy="12" r="4" />
      <circle cx="17.5" cy="6.5" r="0.5" fill="currentColor" />
    </svg>
  );
}

function FooterLi({ children }: { children: React.ReactNode }) {
  return (
    <li className="text-[13px] leading-[1.9] text-[rgba(244,238,223,0.82)] hover:text-[color:var(--color-gold-2)] transition-colors duration-[160ms] ease-[var(--ease-out)]">
      {children}
    </li>
  );
}

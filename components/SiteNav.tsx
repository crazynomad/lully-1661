import { Brand } from '@/components/Brand';
import { LocalizedLink } from '@/components/LocalizedLink';
import type { Locale } from '@/lib/i18n/routing';
import { getTranslations } from 'next-intl/server';

// Top-level site navigation. Per the Lully 1661 design system § Nav:
// flush row with hairline bottom rule, brand wordmark on the left,
// uppercase items in the middle, language switcher on the right.

type NavItem = {
  href: '/menu' | '/menu/brunch' | '/lojas' | '/reservas' | '/sobre';
  labelKey: 'menu' | 'brunch' | 'stores' | 'reservations' | 'about';
};

const NAV_ITEMS: NavItem[] = [
  { href: '/menu', labelKey: 'menu' },
  { href: '/menu/brunch', labelKey: 'brunch' },
  { href: '/lojas', labelKey: 'stores' },
  { href: '/reservas', labelKey: 'reservations' },
  { href: '/sobre', labelKey: 'about' },
];

export async function SiteNav({ locale }: { locale: Locale }) {
  const t = await getTranslations({ locale, namespace: 'nav' });
  const otherLocale: Locale = locale === 'pt' ? 'en' : 'pt';

  return (
    <nav
      className="flex items-center justify-between px-10 py-6 border-b border-[rgba(26,22,19,0.14)]"
      aria-label="Primary"
    >
      <LocalizedLink href="/" className="cursor-pointer">
        <Brand size="md" />
      </LocalizedLink>

      <ul className="flex gap-7 list-none p-0 m-0">
        {NAV_ITEMS.map((item) => (
          <li
            key={item.href}
            className="text-[12px] tracking-[0.16em] uppercase text-[color:var(--color-ink-2)] hover:text-[color:var(--color-ember)] transition-colors duration-[160ms] ease-[var(--ease-out)]"
          >
            <LocalizedLink href={item.href}>{t(item.labelKey)}</LocalizedLink>
          </li>
        ))}
      </ul>

      {/* Language switcher: clicking jumps to the same path in the other locale.
          Implemented as a Link with `locale` prop so next-intl handles the
          per-locale path mapping. */}
      <div className="text-[11px] tracking-[0.18em] uppercase text-[color:var(--color-stone)]">
        <span className="text-[color:var(--color-ink)] font-semibold">{locale.toUpperCase()}</span>
        {' · '}
        <LocalizedLink
          href="/"
          locale={otherLocale}
          className="hover:text-[color:var(--color-ink)]"
        >
          {otherLocale.toUpperCase()}
        </LocalizedLink>
      </div>
    </nav>
  );
}

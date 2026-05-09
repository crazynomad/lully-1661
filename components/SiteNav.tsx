import { Brand } from '@/components/Brand';
import { LocalizedLink } from '@/components/LocalizedLink';
import { MobileMenu, type MobileMenuItem } from '@/components/MobileMenu';
import type { Locale } from '@/lib/i18n/routing';
import { getTranslations } from 'next-intl/server';

// Top-level site navigation. Per the Lully 1661 design system § Nav:
// flush row with hairline bottom rule, brand wordmark on the left,
// uppercase items in the middle, language switcher on the right.
//
// Mobile-first: at < md (< 768px) only Brand + hamburger are visible;
// the inline links and the language switcher hide. The hamburger drives
// a fullscreen overlay component (MobileMenu, client-side island).

const NAV_ITEMS = [
  { href: '/menu', labelKey: 'menu' },
  { href: '/menu/brunch', labelKey: 'brunch' },
  { href: '/lojas', labelKey: 'stores' },
  { href: '/reservas', labelKey: 'reservations' },
  { href: '/sobre', labelKey: 'about' },
] as const satisfies ReadonlyArray<{
  href: MobileMenuItem['href'];
  labelKey: 'menu' | 'brunch' | 'stores' | 'reservations' | 'about';
}>;

export async function SiteNav({ locale }: { locale: Locale }) {
  const t = await getTranslations({ locale, namespace: 'nav' });
  const otherLocale: Locale = locale === 'pt' ? 'en' : 'pt';

  // Pre-translate the labels so the client island doesn't need to
  // re-import the i18n machinery.
  const items: MobileMenuItem[] = NAV_ITEMS.map((item) => ({
    href: item.href,
    label: t(item.labelKey),
  }));

  return (
    <nav
      // Mobile: 20px horizontal padding (matches Container's mobile inset).
      // md+: 40px to match the design-system spec.
      className="flex items-center justify-between px-5 md:px-10 py-5 md:py-6 border-b border-[rgba(26,22,19,0.14)]"
      aria-label="Primary"
    >
      <LocalizedLink href="/" className="cursor-pointer">
        <Brand size="md" />
      </LocalizedLink>

      {/* Desktop: inline link list. Hidden on mobile; the MobileMenu
          replaces it. */}
      <ul className="hidden md:flex gap-7 list-none p-0 m-0">
        {items.map((item) => (
          <li
            key={item.href}
            className="text-[12px] tracking-[0.16em] uppercase text-[color:var(--color-ink-2)] hover:text-[color:var(--color-ember)] transition-colors duration-[160ms] ease-[var(--ease-out)]"
          >
            <LocalizedLink href={item.href}>{item.label}</LocalizedLink>
          </li>
        ))}
      </ul>

      {/* Desktop language switcher: clicking jumps to the same path in
          the other locale. */}
      <div className="hidden md:block text-[11px] tracking-[0.18em] uppercase text-[color:var(--color-stone)]">
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

      {/* Mobile: hamburger button that drives the fullscreen overlay.
          Hidden at md+ where the inline nav is shown instead. */}
      <MobileMenu items={items} locale={locale} otherLocale={otherLocale} />
    </nav>
  );
}

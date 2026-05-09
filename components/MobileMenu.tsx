'use client';

import { LocalizedLink } from '@/components/LocalizedLink';
import type { Locale } from '@/lib/i18n/routing';
import { useEffect, useState } from 'react';

// Mobile drawer for the primary nav. Server component (SiteNav) passes
// translated labels as props so this stays a tiny island of client JS —
// it only owns the open/close state.
//
// Behaviour: tap hamburger → fullscreen overlay slides in from the top,
// items stacked, language switcher at the bottom. Tap a link or the X →
// closes. ESC closes. Body scroll locks while open.

export type MobileMenuItem = {
  href: '/menu' | '/menu/brunch' | '/lojas' | '/reservas' | '/sobre';
  label: string;
};

type MobileMenuProps = {
  items: ReadonlyArray<MobileMenuItem>;
  locale: Locale;
  otherLocale: Locale;
};

export function MobileMenu({ items, locale, otherLocale }: MobileMenuProps) {
  const [open, setOpen] = useState(false);

  // Close on ESC and lock scroll while open.
  useEffect(() => {
    if (!open) return;
    const onKey = (e: KeyboardEvent) => {
      if (e.key === 'Escape') setOpen(false);
    };
    const previousOverflow = document.body.style.overflow;
    document.body.style.overflow = 'hidden';
    document.addEventListener('keydown', onKey);
    return () => {
      document.body.style.overflow = previousOverflow;
      document.removeEventListener('keydown', onKey);
    };
  }, [open]);

  return (
    <>
      <button
        type="button"
        onClick={() => setOpen((v) => !v)}
        aria-label={open ? 'Close menu' : 'Open menu'}
        aria-expanded={open}
        aria-controls="mobile-menu-panel"
        className="md:hidden flex items-center justify-center w-10 h-10 -mr-2 text-[color:var(--color-ink)]"
      >
        {open ? <CloseGlyph /> : <HamburgerGlyph />}
      </button>

      {open && (
        <nav
          id="mobile-menu-panel"
          // Fullscreen overlay sitting above page content. Hidden at
          // md+ where the inline nav is shown instead. Using <nav> with
          // an aria-label is semantically richer than role="dialog" for
          // a navigation menu — it lets screen readers announce "Mobile
          // navigation" rather than treating it as a modal.
          className="fixed inset-0 z-50 md:hidden flex flex-col bg-[color:var(--color-paper)]"
          aria-label="Mobile primary navigation"
        >
          {/* Top row: brand placeholder + close button. We render an
              empty span on the left to mirror the header height — the
              visible Brand stays where the SiteNav put it (DOM is
              outside this overlay). */}
          <div className="flex items-center justify-end px-5 py-6 border-b border-[rgba(26,22,19,0.14)]">
            <button
              type="button"
              onClick={() => setOpen(false)}
              aria-label="Close menu"
              className="flex items-center justify-center w-10 h-10 -mr-2 text-[color:var(--color-ink)]"
            >
              <CloseGlyph />
            </button>
          </div>

          <ul className="flex-1 list-none p-0 m-0 px-5 py-10 flex flex-col gap-6">
            {items.map((item) => (
              <li key={item.href}>
                <LocalizedLink
                  href={item.href}
                  onClick={() => setOpen(false)}
                  className="block text-[28px] font-[family-name:var(--font-display)] tracking-[-0.015em]"
                  style={{ fontWeight: 400, fontVariationSettings: '"opsz" 72' }}
                >
                  {item.label}
                </LocalizedLink>
              </li>
            ))}
          </ul>

          <div className="px-5 py-6 border-t border-[rgba(26,22,19,0.14)] text-[12px] tracking-[0.18em] uppercase text-[color:var(--color-stone)]">
            <span className="text-[color:var(--color-ink)] font-semibold">
              {locale.toUpperCase()}
            </span>
            {' · '}
            <LocalizedLink
              href="/"
              locale={otherLocale}
              onClick={() => setOpen(false)}
              className="hover:text-[color:var(--color-ink)]"
            >
              {otherLocale.toUpperCase()}
            </LocalizedLink>
          </div>
        </nav>
      )}
    </>
  );
}

function HamburgerGlyph() {
  return (
    <svg width="22" height="22" viewBox="0 0 22 22" fill="none" aria-hidden="true">
      <line
        x1="3"
        y1="7"
        x2="19"
        y2="7"
        stroke="currentColor"
        strokeWidth="1.5"
        strokeLinecap="round"
      />
      <line
        x1="3"
        y1="15"
        x2="19"
        y2="15"
        stroke="currentColor"
        strokeWidth="1.5"
        strokeLinecap="round"
      />
    </svg>
  );
}

function CloseGlyph() {
  return (
    <svg width="22" height="22" viewBox="0 0 22 22" fill="none" aria-hidden="true">
      <line
        x1="5"
        y1="5"
        x2="17"
        y2="17"
        stroke="currentColor"
        strokeWidth="1.5"
        strokeLinecap="round"
      />
      <line
        x1="17"
        y1="5"
        x2="5"
        y2="17"
        stroke="currentColor"
        strokeWidth="1.5"
        strokeLinecap="round"
      />
    </svg>
  );
}

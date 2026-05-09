import { cn } from '@/lib/utils/cn';
import { forwardRef } from 'react';

// Three button variants per the Lully 1661 design system:
// - primary  → Ink fill, paper text; hover shifts to ember
// - ember    → Ember fill, paper text; the highest-intent CTA (e.g. "Reserve a table")
// - ghost    → Transparent with Ink border; hover fills to Ink
//
// All variants are square-cornered, uppercase tracked label, no shadow,
// no opacity changes on hover. Press states darken to *-2 down-shades.

export type ButtonVariant = 'primary' | 'ember' | 'ghost';
export type ButtonSize = 'sm' | 'md';

type ButtonProps = React.ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: ButtonVariant;
  size?: ButtonSize;
};

const variantClasses: Record<ButtonVariant, string> = {
  primary:
    'bg-[color:var(--color-ink)] text-[color:var(--color-paper)] border border-[color:var(--color-ink)] hover:bg-[color:var(--color-ember)] hover:border-[color:var(--color-ember)] active:bg-[color:var(--color-ember-2)] active:border-[color:var(--color-ember-2)]',
  ember:
    'bg-[color:var(--color-ember)] text-[color:var(--color-paper)] border border-[color:var(--color-ember)] hover:bg-[color:var(--color-ember-2)] hover:border-[color:var(--color-ember-2)]',
  ghost:
    'bg-transparent text-[color:var(--color-ink)] border border-[color:var(--color-ink)] hover:bg-[color:var(--color-ink)] hover:text-[color:var(--color-paper)]',
};

const sizeClasses: Record<ButtonSize, string> = {
  sm: 'px-[14px] py-[9px] text-[11px]',
  md: 'px-[22px] py-[14px] text-[12px]',
};

const baseClasses =
  'inline-flex items-center justify-center font-[family-name:var(--font-body)] font-semibold uppercase tracking-[0.18em] transition-colors duration-[160ms] ease-[var(--ease-out)] disabled:pointer-events-none disabled:opacity-50 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[color:var(--color-ember)] focus-visible:ring-offset-2 focus-visible:ring-offset-[color:var(--bg)]';

/**
 * Re-usable class builder so anchors / next-intl Links can wear the
 * same look without re-wrapping in a real <button>.
 */
export function buttonClassName({
  variant = 'primary',
  size = 'md',
  className,
}: {
  variant?: ButtonVariant;
  size?: ButtonSize;
  className?: string;
}): string {
  return cn(baseClasses, variantClasses[variant], sizeClasses[size], className);
}

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = 'primary', size = 'md', type = 'button', ...props }, ref) => (
    <button
      ref={ref}
      type={type}
      className={buttonClassName({ variant, size, className })}
      {...props}
    />
  ),
);
Button.displayName = 'Button';

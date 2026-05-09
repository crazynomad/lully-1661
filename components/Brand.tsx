import { cn } from '@/lib/utils/cn';

type BrandProps = {
  size?: 'sm' | 'md' | 'lg';
  /** Use 'on-dark' to flip the gold "1661" italic to the lighter `--color-gold-2` shade. */
  surface?: 'paper' | 'on-dark';
  className?: string;
};

const sizes = {
  sm: 'text-[20px]',
  md: 'text-[26px]',
  lg: 'text-[32px]',
} as const;

export function Brand({ size = 'md', surface = 'paper', className }: BrandProps) {
  const goldColor = surface === 'on-dark' ? 'var(--color-gold-2)' : 'var(--color-gold)';
  return (
    <span
      className={cn('font-[family-name:var(--font-display)]', sizes[size], className)}
      style={{
        fontWeight: 300,
        fontVariationSettings: '"opsz" 96, "SOFT" 80',
        letterSpacing: '-0.01em',
      }}
    >
      lully{' '}
      <em
        style={{
          fontFamily: 'var(--font-serif-accent)',
          fontStyle: 'italic',
          color: goldColor,
          fontWeight: 400,
        }}
      >
        1661
      </em>
    </span>
  );
}

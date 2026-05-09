import { cn } from '@/lib/utils/cn';

type EyebrowProps = React.HTMLAttributes<HTMLSpanElement> & {
  /** 'on-dark' switches gold to the lighter --color-gold-2 shade. */
  surface?: 'paper' | 'on-dark';
};

export function Eyebrow({ className, surface = 'paper', ...props }: EyebrowProps) {
  return (
    <span
      className={cn('eyebrow', className)}
      style={surface === 'on-dark' ? { color: 'var(--color-gold-2)' } : undefined}
      {...props}
    />
  );
}

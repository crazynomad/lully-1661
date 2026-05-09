import { cn } from '@/lib/utils/cn';

type ContainerProps = React.HTMLAttributes<HTMLDivElement> & {
  /** 'wide' = 1280px (default chrome width per design system); 'narrow' = 720px (legal/long-form). */
  size?: 'narrow' | 'default' | 'wide';
};

const sizes = {
  narrow: 'max-w-[720px]',
  default: 'max-w-[1120px]',
  wide: 'max-w-[1280px]',
} as const;

export function Container({ className, size = 'wide', ...props }: ContainerProps) {
  return <div className={cn('mx-auto px-10', sizes[size], className)} {...props} />;
}

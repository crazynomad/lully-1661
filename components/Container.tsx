import { cn } from '@/lib/utils/cn';
import type { ElementType } from 'react';

type ContainerProps<T extends ElementType = 'div'> = {
  /** 'wide' = 1280px (default chrome width per design system); 'narrow' = 720px (legal/long-form). */
  size?: 'narrow' | 'default' | 'wide';
  as?: T;
} & Omit<React.ComponentPropsWithoutRef<T>, 'as'>;

const sizes = {
  narrow: 'max-w-[720px]',
  default: 'max-w-[1120px]',
  wide: 'max-w-[1280px]',
} as const;

export function Container<T extends ElementType = 'div'>({
  as,
  className,
  size = 'wide',
  ...props
}: ContainerProps<T>) {
  const Tag = (as ?? 'div') as ElementType;
  // Mobile-first horizontal padding: 20px on phones, 32px on tablets,
  // 40px on desktop (per the design-system spec for chrome width).
  return <Tag className={cn('mx-auto px-5 sm:px-8 md:px-10', sizes[size], className)} {...props} />;
}

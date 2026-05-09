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
  return <Tag className={cn('mx-auto px-10', sizes[size], className)} {...props} />;
}

import { cn } from '@/lib/utils/cn';

type ContainerProps = React.HTMLAttributes<HTMLDivElement> & {
  size?: 'narrow' | 'default' | 'wide';
};

const sizes = {
  narrow: 'max-w-2xl',
  default: 'max-w-5xl',
  wide: 'max-w-7xl',
} as const;

export function Container({ className, size = 'default', ...props }: ContainerProps) {
  return <div className={cn('mx-auto px-6', sizes[size], className)} {...props} />;
}

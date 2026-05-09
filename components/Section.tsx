import { cn } from '@/lib/utils/cn';

type SectionProps = React.HTMLAttributes<HTMLElement> & {
  spacing?: 'sm' | 'md' | 'lg';
};

const spacings = {
  sm: 'py-12',
  md: 'py-20',
  lg: 'py-32',
} as const;

export function Section({ className, spacing = 'md', ...props }: SectionProps) {
  return <section className={cn(spacings[spacing], className)} {...props} />;
}

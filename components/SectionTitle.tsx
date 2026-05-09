import { cn } from '@/lib/utils/cn';

type SectionTitleProps = React.HTMLAttributes<HTMLHeadingElement> & {
  as?: 'h1' | 'h2' | 'h3';
  size?: number;
};

export function SectionTitle({
  as: Tag = 'h2',
  size = 44,
  className,
  style,
  ...props
}: SectionTitleProps) {
  return (
    <Tag
      className={cn('section-title', className)}
      style={{ fontSize: size, ...style }}
      {...props}
    />
  );
}

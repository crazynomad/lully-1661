// Re-export the typed Link from next-intl/navigation. Use this everywhere
// instead of `next/link` so locale prefixes and per-locale pathnames are
// applied automatically per `lib/i18n/routing.ts`.
export { Link as LocalizedLink } from '@/lib/i18n/navigation';

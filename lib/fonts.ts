// Font loading. Self-hosted via next/font/google for now (zero CLS, no
// runtime third-party request, no GDPR cookie banner dance for fonts —
// per architecture.md § 4 frontend stack table).
//
// Final pairing lands in week-1 design pass. Tinos + Inter are working
// placeholders that won't lock in any visual direction.
import { Inter, Tinos } from 'next/font/google';

export const fontDisplay = Tinos({
  subsets: ['latin'],
  weight: ['400', '700'],
  display: 'swap',
  variable: '--font-display',
});

export const fontBody = Inter({
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-body',
});

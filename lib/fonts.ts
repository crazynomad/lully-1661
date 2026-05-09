// Lully 1661 type stack — three families, all free on Google Fonts:
// - Fraunces (variable opsz + SOFT axes) → display, headlines, product names
// - Instrument Serif Italic → the sentimental "swash" line per page,
//   the italic <em> inside headings, prices, accent labels
// - Instrument Sans → body, UI, eyebrows, metadata
//
// Loaded via `next/font/google` so they self-host at build time (no
// runtime third-party request, zero CLS, no GDPR cookie banner needed
// for fonts). Class names are wired into <body> in app/[locale]/layout.tsx
// and the `--font-*` CSS variables in app/globals.css consume them.

import { Fraunces, Instrument_Sans, Instrument_Serif } from 'next/font/google';

export const fontDisplay = Fraunces({
  subsets: ['latin'],
  axes: ['opsz', 'SOFT'],
  weight: 'variable',
  style: ['normal', 'italic'],
  display: 'swap',
  variable: '--font-display-loaded',
});

export const fontSerifAccent = Instrument_Serif({
  subsets: ['latin'],
  weight: '400',
  style: ['normal', 'italic'],
  display: 'swap',
  variable: '--font-serif-accent-loaded',
});

export const fontBody = Instrument_Sans({
  subsets: ['latin'],
  weight: ['400', '500', '600', '700'],
  display: 'swap',
  variable: '--font-body-loaded',
});

// Class names to apply on <body>. globals.css picks up the CSS vars
// and references them in --font-display / --font-serif-accent / --font-body.
export const fontClassNames = `${fontDisplay.variable} ${fontSerifAccent.variable} ${fontBody.variable}`;

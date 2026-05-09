#!/usr/bin/env node
// One-off: generate branded JPG placeholders for the three store hero
// slots. Sharp renders SVG → JPG so font glyphs come from the OS, which
// works around ImageMagick's missing FreeType on this machine.
//
// Run:  node scripts/build-store-placeholders.mjs
// Output: public/content/store/<slug>/hero.jpg

import sharp from 'sharp';
import { mkdir, writeFile } from 'node:fs/promises';
import { dirname } from 'node:path';

const stores = [
  { slug: 'anjos', name: 'Anjos', tag: 'Brunch &amp; dine-in' },
  { slug: 'campo-de-ourique', name: 'Campo de Ourique', tag: 'Bairro favourite' },
  { slug: 'beato', name: 'Beato', tag: 'Original — production &amp; oven' },
];

const W = 1600;
const H = 1200;

function svg({ name, tag }) {
  return `<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#f4eedf"/>
      <stop offset="100%" stop-color="#e6dcc4"/>
    </linearGradient>
  </defs>
  <rect width="${W}" height="${H}" fill="url(#bg)"/>
  <g text-anchor="middle" font-family="Baskerville, 'Hoefler Text', Georgia, serif">
    <text x="${W / 2}" y="320" font-size="110" fill="#3c342e" font-style="italic">lully 1661</text>
    <text x="${W / 2}" y="500" font-size="90" fill="#3c342e">${name}</text>
    <text x="${W / 2}" y="640" font-size="38" fill="#7a6b56" font-style="italic">${tag}</text>
    <text x="${W / 2}" y="${H - 180}" font-size="26" fill="#a68a3e" font-family="-apple-system, system-ui, sans-serif" letter-spacing="4">PLACEHOLDER · DEMO ONLY</text>
    <text x="${W / 2}" y="${H - 120}" font-size="22" fill="#7a6b56" font-family="-apple-system, system-ui, sans-serif">replace with photography before production</text>
  </g>
</svg>`;
}

for (const store of stores) {
  const out = `public/content/store/${store.slug}/hero.jpg`;
  await mkdir(dirname(out), { recursive: true });

  const buffer = await sharp(Buffer.from(svg(store)))
    .jpeg({ quality: 85, progressive: true, mozjpeg: true })
    .toBuffer();

  await writeFile(out, buffer);
  console.log(`wrote ${out} (${buffer.length} bytes)`);
}

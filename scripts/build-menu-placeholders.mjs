#!/usr/bin/env node
// Generate JPG placeholders for the 9 brunch items extracted from
// raw-requirements/menu-weekly-sample.pdf. Square 1200×1200; same baroque
// cream palette as the store hero placeholders.
//
// Run:  node scripts/build-menu-placeholders.mjs

import sharp from 'sharp';
import { mkdir, writeFile } from 'node:fs/promises';
import { dirname } from 'node:path';

const items = [
  { slug: 'sopa-do-mes', name: 'Sopa do Mês', subtitle: 'Soup of the Month' },
  { slug: 'le-menuet', name: 'Le Menuet', subtitle: 'Fried chicken focaccia' },
  { slug: 'le-monsieur', name: 'Le Monsieur', subtitle: 'Lasagna-style toast' },
  { slug: 'granola', name: 'Granola', subtitle: 'House blend, yogurt, fruit' },
  { slug: 'pain-perdu', name: 'Pain Perdu', subtitle: 'French toast' },
  { slug: 'ovos-benedict', name: 'Ovos Benedict', subtitle: 'Eggs Benedict' },
  { slug: 'ovos-florentine', name: 'Ovos Florentine', subtitle: 'Eggs Florentine' },
  { slug: 'cilbir', name: 'Çılbır', subtitle: 'Turkish poached eggs' },
  { slug: 'avocado-toast', name: 'Avocado Toast', subtitle: 'with pomegranate molasses' },
];

const W = 1200;
const H = 1200;

function escape(s) {
  return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

function svg({ name, subtitle }) {
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
    <text x="${W / 2}" y="${H / 2 - 40}" font-size="80" fill="#3c342e">${escape(name)}</text>
    <text x="${W / 2}" y="${H / 2 + 30}" font-size="32" fill="#7a6b56" font-style="italic">${escape(subtitle)}</text>
    <text x="${W / 2}" y="${H - 80}" font-size="22" fill="#a68a3e" font-family="-apple-system, system-ui, sans-serif" letter-spacing="3">PLACEHOLDER · DEMO ONLY</text>
  </g>
</svg>`;
}

for (const item of items) {
  const out = `public/content/weeklyMenuItem/${item.slug}/image.jpg`;
  await mkdir(dirname(out), { recursive: true });

  const buffer = await sharp(Buffer.from(svg(item)))
    .jpeg({ quality: 85, progressive: true, mozjpeg: true })
    .toBuffer();

  await writeFile(out, buffer);
  console.log(`wrote ${out} (${buffer.length} bytes)`);
}

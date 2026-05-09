#!/usr/bin/env node
// Seed content/weeklyMenuItem/* with the 9 brunch items extracted from
// raw-requirements/menu-weekly-sample.pdf (PT + EN, prices in EUR).
// Each entry references the brunch productCategory and is available at
// the Anjos store only (per architecture.md / requirements M2/M4).
//
// Run: node scripts/build-brunch-content.mjs

import { mkdir, writeFile } from 'node:fs/promises';

const items = [
  {
    slug: 'sopa-do-mes',
    namePt: 'Sopa do Mês',
    nameEn: 'Soup of the Month',
    slugPt: 'sopa-do-mes',
    slugEn: 'soup-of-the-month',
    price: '6,50',
    descPt:
      'Sopa de ervilhas, caldo de legumes, hortelã, sumo de limão e leite de coco. Servida fria ou à temperatura ambiente.',
    descEn:
      'Pea soup with vegetable stock, mint, lemon juice and coconut milk. Served cold or at room temperature.',
    diet: ['vegetarian'],
  },
  {
    slug: 'le-menuet',
    namePt: 'Le Menuet',
    nameEn: 'Le Menuet',
    slugPt: 'le-menuet',
    slugEn: 'le-menuet',
    price: '10,00',
    descPt:
      'Frango frito com aioli caseiro, tomates secos, iogurte, salada e cebola roxa em conserva. Preparado com focaccia.',
    descEn:
      'Fried chicken with house aioli, sun-dried tomatoes, yogurt, salad and conserved red onion. Served on focaccia.',
    diet: [],
  },
  {
    slug: 'le-monsieur',
    namePt: 'Le Monsieur',
    nameEn: 'Le Monsieur',
    slugPt: 'le-monsieur',
    slugEn: 'le-monsieur',
    price: '11,00',
    descPt:
      'Tosta em camadas, estilo lasanha, com fiambre, Comté e salada. Preparada com pão Paillard & Fâcheux fatiado fino.',
    descEn:
      'Lasagna-style layered toast with ham, Comté and salad. Made with thin-sliced Paillard & Fâcheux bread.',
    diet: [],
    allergens: ['gluten', 'dairy'],
  },
  {
    slug: 'granola',
    namePt: 'Granola',
    nameEn: 'Granola',
    slugPt: 'granola',
    slugEn: 'granola',
    price: '5,50 / 7,00',
    descPt:
      'Granola caseira com flocos de aveia, arroz tufado, sementes de abóbora, doce de figo, mel, melaço de romã, canela. Servida com iogurte, manteiga de amendoim, mirtilos e banana.',
    descEn:
      'House-made granola with oats, rice puffs, pumpkin seeds, fig jam, honey, pomegranate molasses and cinnamon. Served with yogurt, peanut butter, blueberries and banana.',
    diet: ['vegetarian'],
    allergens: ['gluten', 'dairy', 'nuts', 'peanuts'],
  },
  {
    slug: 'pain-perdu',
    namePt: 'Pain Perdu',
    nameEn: 'Pain Perdu',
    slugPt: 'pain-perdu',
    slugEn: 'pain-perdu',
    price: '6,50',
    descPt:
      'O nosso French toast — natas batidas, mirtilos e framboesas. Feito com a colecção de pão envelhecido da casa.',
    descEn:
      'Our French toast — chantilly cream, blueberries and raspberries. Made with our aged bread collection.',
    diet: ['vegetarian'],
    allergens: ['gluten', 'dairy', 'eggs'],
  },
  {
    slug: 'ovos-benedict',
    namePt: 'Ovos Benedict',
    nameEn: 'Eggs Benedict',
    slugPt: 'ovos-benedict',
    slugEn: 'eggs-benedict',
    price: '12,00',
    descPt:
      'Ovos escalfados, molho Holandês, mostarda, bacon, pimenta Urfa (İsot) e ervas frescas. Servido no nosso pão Fâcheux.',
    descEn:
      'Poached eggs, Hollandaise sauce, mustard, bacon, Urfa chili (İsot) and fresh herbs. Served on our Fâcheux bread.',
    diet: [],
    allergens: ['gluten', 'dairy', 'eggs'],
  },
  {
    slug: 'ovos-florentine',
    namePt: 'Ovos Florentine',
    nameEn: 'Eggs Florentine',
    slugPt: 'ovos-florentine',
    slugEn: 'eggs-florentine',
    price: '10,50',
    descPt:
      'Ovos escalfados, puré de espinafres, molho Holandês, pimenta preta, raspas de limão e ervas frescas. Servido no nosso pão Fâcheux.',
    descEn:
      'Poached eggs, spinach purée, Hollandaise sauce, black pepper, lemon zest and fresh herbs. Served on our Fâcheux bread.',
    diet: ['vegetarian'],
    allergens: ['gluten', 'dairy', 'eggs'],
  },
  {
    slug: 'cilbir',
    namePt: 'Çılbır',
    nameEn: 'Çılbır',
    slugPt: 'cilbir',
    slugEn: 'cilbir',
    price: '8,50',
    descPt:
      'Ovos escalfados, óleo de chili, iogurte de alho, ervas frescas. Servidos com pão Paillard torrado. O nível de picante e alho ajusta-se a gosto.',
    descEn:
      'Poached eggs, chili oil, garlic yogurt and fresh herbs. Served with toasted Paillard bread. Spice and garlic levels adjusted to taste.',
    diet: ['vegetarian'],
    allergens: ['gluten', 'dairy', 'eggs'],
  },
  {
    slug: 'avocado-toast',
    namePt: 'Avocado Toast',
    nameEn: 'Avocado Toast',
    slugPt: 'avocado-toast',
    slugEn: 'avocado-toast',
    price: '8,50',
    descPt:
      'Purê de abacate, tomates assados, cebola roxa em conserva, melaço de romã e ervas frescas. Servido no nosso pão Fâcheux.',
    descEn:
      'Avocado purée, roasted tomatoes, conserved red onion, pomegranate molasses and fresh herbs. Served on our Fâcheux bread.',
    diet: ['vegan'],
    allergens: ['gluten'],
  },
];

const WEEK_OF = '2026-05-04';
const FEATURED_SLUGS = new Set(['ovos-benedict', 'pain-perdu', 'avocado-toast']);

function yamlEscape(s) {
  return s.replace(/\\/g, '\\\\').replace(/"/g, '\\"');
}

function entryYaml(item) {
  const allergens = item.allergens || [];
  const diet = item.diet || [];
  return `# Brunch item — extracted from raw-requirements/menu-weekly-sample.pdf
# Available at Anjos only. Demo content seeded 2026-05-09.
slug: ${item.slug}
name:
  pt: "${yamlEscape(item.namePt)}"
  en: "${yamlEscape(item.nameEn)}"
localizedSlug:
  pt: ${item.slugPt}
  en: ${item.slugEn}
description:
  pt: |
    ${item.descPt}
  en: |
    ${item.descEn}
category: brunch
image:
  file: image.jpg
  alt:
    pt: "${yamlEscape(item.namePt)} — placeholder demo"
    en: "${yamlEscape(item.nameEn)} — placeholder demo"
  decorative: false
allergens:${allergens.length === 0 ? ' []' : '\n' + allergens.map((a) => '  - ' + a).join('\n')}
suitableForDiet:${diet.length === 0 ? ' []' : '\n' + diet.map((d) => '  - ' + d).join('\n')}
availableAt:
  - anjos
weekOf: ${WEEK_OF}
featured: ${FEATURED_SLUGS.has(item.slug) ? 'true' : 'false'}
# Price (EUR): ${item.price}
`;
}

for (const item of items) {
  const dir = `content/weeklyMenuItem/${item.slug}`;
  await mkdir(dir, { recursive: true });
  await writeFile(`${dir}/index.yaml`, entryYaml(item));
  console.log(`wrote ${dir}/index.yaml`);
}

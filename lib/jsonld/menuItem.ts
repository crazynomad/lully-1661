// schema.org MenuItem — emitted on /menu/[category]/[slug] product pages.
// In phase 2 (commerce returns) this may be paired with or replaced by
// schema.org Product. The phase-2 readiness checklist in architecture.md
// § 17 commits to non-clashing field names.
// https://schema.org/MenuItem

type MenuItemInput = {
  name: string;
  description?: string;
  image?: string;
  suitableForDiet?: Array<'GlutenFreeDiet' | 'VeganDiet' | 'VegetarianDiet'>;
};

export function menuItemJsonLd(input: MenuItemInput) {
  return {
    '@context': 'https://schema.org',
    '@type': 'MenuItem',
    name: input.name,
    ...(input.description ? { description: input.description } : {}),
    ...(input.image ? { image: input.image } : {}),
    ...(input.suitableForDiet && input.suitableForDiet.length > 0
      ? {
          suitableForDiet: input.suitableForDiet.map((d) => `https://schema.org/${d}`),
        }
      : {}),
  };
}

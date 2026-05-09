import type { Locale } from '@/lib/i18n/routing';
import { reader } from '@/lib/keystatic/reader';

// Public read API for the menu feature.

export type WeeklyMenuItem = NonNullable<
  Awaited<ReturnType<typeof reader.collections.weeklyMenuItem.read>>
>;

// Demo: course assignment + price live alongside each weeklyMenuItem
// slug. Promoting to the Keystatic schema is a one-PR move when the
// content model stabilises.
type Course = 'eggs' | 'toasts' | 'sweet' | 'kitchen';

const COURSE_BY_SLUG: Record<string, Course> = {
  'ovos-benedict': 'eggs',
  'ovos-florentine': 'eggs',
  cilbir: 'eggs',
  'avocado-toast': 'toasts',
  'le-monsieur': 'toasts',
  'le-menuet': 'toasts',
  'pain-perdu': 'sweet',
  granola: 'sweet',
  'sopa-do-mes': 'kitchen',
};

const PRICE_BY_SLUG: Record<string, string> = {
  'ovos-benedict': '€11',
  'ovos-florentine': '€10.50',
  cilbir: '€9.50',
  'avocado-toast': '€8.50',
  'le-monsieur': '€10',
  'le-menuet': '€11',
  'pain-perdu': '€8.50',
  granola: '€7',
  'sopa-do-mes': '€6',
};

// Course labels (PT/EN). The "I · II · III · IV" Roman numeral
// prefix is part of the brand voice — see README "menu in four movements".
const COURSE_LABELS: Record<Course, { pt: string; en: string }> = {
  eggs: { pt: 'I · Ovos', en: 'I · Eggs' },
  toasts: { pt: 'II · Tostas', en: 'II · Toasts' },
  sweet: { pt: 'III · Doce', en: 'III · Sweet' },
  kitchen: { pt: 'IV · Da cozinha', en: 'IV · From the kitchen' },
};

const COURSE_ORDER: Course[] = ['eggs', 'toasts', 'sweet', 'kitchen'];

export type BrunchCourseGroup = {
  course: Course;
  label: string;
  items: Array<{
    slug: string;
    entry: WeeklyMenuItem;
    price: string;
  }>;
};

/**
 * Read all weeklyMenuItem entries available at a given store and
 * group them into the four brunch movements per the design system's
 * BrunchPage layout. Items without a course mapping fall through to
 * the kitchen movement so nothing is silently dropped.
 */
export async function getBrunchByMovement(
  storeSlug: string,
  locale: Locale,
): Promise<BrunchCourseGroup[]> {
  const items = await reader.collections.weeklyMenuItem.all();
  const available = items.filter((item) => item.entry.availableAt.includes(storeSlug));

  const byCourse = new Map<Course, BrunchCourseGroup['items']>();
  for (const course of COURSE_ORDER) byCourse.set(course, []);

  for (const item of available) {
    const course = COURSE_BY_SLUG[item.slug] ?? 'kitchen';
    byCourse.get(course)?.push({
      slug: item.slug,
      entry: item.entry,
      price: PRICE_BY_SLUG[item.slug] ?? '',
    });
  }

  return COURSE_ORDER.map((course) => ({
    course,
    label: COURSE_LABELS[course][locale],
    items: byCourse.get(course) ?? [],
  })).filter((group) => group.items.length > 0);
}

export function menuItemImagePath(slug: string): string {
  return `/content/weeklyMenuItem/${slug}/image.jpg`;
}

import { isLocale } from '@/lib/i18n/routing';
import { getTranslations, setRequestLocale } from 'next-intl/server';
import { notFound } from 'next/navigation';

export default async function HomePage({ params }: { params: Promise<{ locale: string }> }) {
  const { locale } = await params;
  if (!isLocale(locale)) notFound();
  setRequestLocale(locale);

  const tSite = await getTranslations('site');
  const tHome = await getTranslations('home');

  return (
    <main className="mx-auto max-w-2xl px-6 py-24">
      <p className="text-sm uppercase tracking-widest text-[color:var(--color-muted)]">
        {tSite('tagline')}
      </p>
      <h1 className="mt-2 text-5xl">{tSite('name')}</h1>
      <p className="mt-8 text-lg text-[color:var(--color-fg)]">{tHome('heroTitle')}</p>
      <p className="mt-12 text-sm text-[color:var(--color-muted)]">{tHome('scaffoldNotice')}</p>
    </main>
  );
}

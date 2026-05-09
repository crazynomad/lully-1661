import { Container } from '@/components/Container';
import { Eyebrow } from '@/components/Eyebrow';

// A discreet Instagram surface — kicker + handle as a link.
//
// Why not embed the actual Instagram feed? Two reasons:
//   1. Instagram's `instgrm.Embeds` script is third-party JS that
//      hammers Core Web Vitals and asks the user to accept cookies
//      (the brand's design-system § Animation says "no parallax /
//      no glass" — third-party feed widgets violate the same restraint).
//   2. The Graph API requires an access token + Facebook Business
//      account, which the demo doesn't have.
// When the client provides Graph API credentials we swap this strip
// for a 6-tile static fetch at build time (the architecture's "no
// runtime third-party JS" rule).

export function InstagramStrip({ locale }: { locale: 'pt' | 'en' }) {
  return (
    <Container as="section" className="py-14 border-t border-[rgba(26,22,19,0.14)] text-center">
      <Eyebrow>{locale === 'pt' ? 'Instagram' : 'Instagram'}</Eyebrow>
      <h2 className="display-md mt-3 mb-3">
        {locale === 'pt' ? (
          <>
            Os bastidores, <em>todas as manhãs.</em>
          </>
        ) : (
          <>
            Behind the counter, <em>every morning.</em>
          </>
        )}
      </h2>
      <a
        href="https://www.instagram.com/lully1661_lisboa/"
        target="_blank"
        rel="noopener noreferrer"
        className="inline-block text-[20px] mt-2 transition-colors hover:text-[color:var(--color-ember)]"
        style={{
          fontFamily: 'var(--font-serif-accent)',
          fontStyle: 'italic',
          color: 'var(--color-gold)',
        }}
      >
        @lully1661_lisboa →
      </a>
    </Container>
  );
}

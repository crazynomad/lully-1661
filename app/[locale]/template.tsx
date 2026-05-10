// Per-navigation wrapper. Unlike layout.tsx, Next.js *remounts* this
// component on every client-side route change — so the
// `[data-page-rise]` element is fresh each time, and the CSS keyframe
// animation defined in app/globals.css fires for every page entry.
//
// This is the right place to hang any "page-load gesture" animation
// you want to repeat across navigation. Per the design system §
// Animation: restrained, no springs, ~240–500ms, ease-out.

export default function LocaleTemplate({ children }: { children: React.ReactNode }) {
  return <div data-page-rise>{children}</div>;
}

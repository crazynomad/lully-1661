// Renders JSON-LD as a non-interactive script tag. Server components can
// emit this directly. Per `docs/architecture.md` § 6.2, multiple types on
// the same page should be combined into a single @graph rather than
// rendering multiple <JsonLd> instances.
//
// Implementation note: we render the stringified JSON as a child of the
// <script> tag rather than via dangerouslySetInnerHTML. Both approaches
// are sanctioned by React for application/ld+json; the children form lets
// React handle escaping of HTML-significant characters as Unicode escapes
// (e.g. `<` → `<`), which remain valid JSON and prevent any markup
// from breaking out of the script tag.
type JsonLdProps = {
  data: Record<string, unknown> | Array<Record<string, unknown>>;
};

export function JsonLd({ data }: JsonLdProps) {
  return <script type="application/ld+json">{JSON.stringify(data)}</script>;
}

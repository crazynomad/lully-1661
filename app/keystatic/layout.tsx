// Keystatic admin uses its own UI shell (no NextIntlClientProvider, no
// site header/footer). This layout escapes the [locale] tree on purpose.
export default function KeystaticLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}

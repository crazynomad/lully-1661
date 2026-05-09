// Required by Next.js. The locale-aware <html> + <body> live in
// app/[locale]/layout.tsx so the lang attribute can switch with the URL.
// This pass-through layout is intentional — do not add markup here.
import './globals.css';

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return children;
}

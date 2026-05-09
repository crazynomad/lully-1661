import createMiddleware from 'next-intl/middleware';
import { routing } from './lib/i18n/routing';

export default createMiddleware(routing);

export const config = {
  // Match all routes except Next.js internals, the Keystatic admin/API,
  // sitemap/robots, and static assets.
  matcher: ['/((?!api|_next|_vercel|keystatic|sitemap.xml|robots.txt|favicon.ico|.*\\..*).*)'],
};

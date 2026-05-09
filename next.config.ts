import type { NextConfig } from 'next';
import createNextIntlPlugin from 'next-intl/plugin';

const withNextIntl = createNextIntlPlugin('./lib/i18n/request.ts');

const nextConfig: NextConfig = {
  reactStrictMode: true,
  poweredByHeader: false,

  images: {
    formats: ['image/avif', 'image/webp'],
    remotePatterns: [
      // Add Cloudinary or other external image hosts here when needed.
      // { protocol: 'https', hostname: 'res.cloudinary.com' },
    ],
  },

  async redirects() {
    return [
      // Bare-domain → default locale handled by next-intl middleware.
      // Place project-specific redirects here.
    ];
  },
};

export default withNextIntl(nextConfig);

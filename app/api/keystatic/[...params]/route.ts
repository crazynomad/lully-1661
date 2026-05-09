import config from '@/keystatic.config';
import { makeRouteHandler } from '@keystatic/next/route-handler';

export const { POST, GET } = makeRouteHandler({
  config,
  // For Keystatic Cloud auth in production, set:
  //   localBaseUrl: process.env.NEXT_PUBLIC_SITE_URL,
  //   secret: process.env.KEYSTATIC_SECRET,
  //   clientId: process.env.KEYSTATIC_GITHUB_CLIENT_ID,
  //   clientSecret: process.env.KEYSTATIC_GITHUB_CLIENT_SECRET,
});

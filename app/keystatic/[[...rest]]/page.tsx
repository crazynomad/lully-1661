import config from '@/keystatic.config';
// Embedded Keystatic admin. Lives at /keystatic; auth-gated by Keystatic
// Cloud in production (GitHub App writes to repo on save) and runs in
// local-filesystem mode in development. Disallowed in robots.txt.
import { makePage } from '@keystatic/next/ui/app';

export default makePage(config);

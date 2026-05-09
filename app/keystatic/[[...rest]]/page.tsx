// Embedded Keystatic admin. Lives at /keystatic; auth-gated by Keystatic
// Cloud in production (GitHub App writes to repo on save) and runs in
// local-filesystem mode in development. Disallowed in robots.txt.
//
// 'use client' is required: the @keystatic/core/ui package ships a
// react-server stub that returns null, so without this directive the
// page renders blank in production. The full UI lives in the client
// bundle.
'use client';

import config from '@/keystatic.config';
import { makePage } from '@keystatic/next/ui/app';

export default makePage(config);

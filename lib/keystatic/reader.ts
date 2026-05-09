import config from '@/keystatic.config';
import { createReader } from '@keystatic/core/reader';

// Server-only Reader. Pages call this at build time to fetch typed content.
// Do not import from a client component — `createReader` reads from the
// filesystem at build time.
export const reader = createReader(process.cwd(), config);

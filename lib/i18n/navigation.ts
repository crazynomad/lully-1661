import { createNavigation } from 'next-intl/navigation';
import { routing } from './routing';

// Typed navigation helpers (Link, redirect, usePathname, useRouter, getPathname)
// that respect the per-locale `pathnames` map in routing.ts.
export const { Link, redirect, usePathname, useRouter, getPathname } = createNavigation(routing);

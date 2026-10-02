import { servedLibrary } from '$lib/server/subject';
import type { RequestHandler } from './$types';

/**
 * The library's counts (docs/design.md §About), for the start screen's About
 * panel when it first opens: counted when the library is built, so grown
 * content counts once its build lands. A read, open like the page.
 */
export const GET: RequestHandler = ({ request }) => servedLibrary('stats', request);

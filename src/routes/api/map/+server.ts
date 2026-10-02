import { servedLibrary } from '$lib/server/subject';
import type { RequestHandler } from './$types';

/**
 * The map's data (docs/design.md §The map): every served subject's frames,
 * connections and marked names, fetched once when the map first opens.
 * Derived when the library is built and sent as stored. A read, open like
 * the page.
 */
export const GET: RequestHandler = ({ request }) => servedLibrary('map', request);

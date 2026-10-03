import { servedLibrary } from '$lib/server/subject';
import type { RequestHandler } from './$types';

/**
 * The Changelog (docs/design.md §What's new, korg 3525, 3526): what was
 * added and what was edited, across subjects, built with the library and the
 * same for every reader. Fetched when the panel first opens; a read, open
 * like the page.
 */
export const GET: RequestHandler = ({ request }) => servedLibrary('changelog', request);

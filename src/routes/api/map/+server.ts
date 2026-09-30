import { json } from '@sveltejs/kit';
import { mapDataOf } from '$engine/map';
import { servedGraph } from '$lib/server/subject';
import type { RequestHandler } from './$types';

/**
 * The map's data (docs/design.md §The map): every served subject's frames,
 * connections and marked names, fetched once when the map first opens. A
 * read, open like the page.
 */
export const GET: RequestHandler = async () => json(mapDataOf(await servedGraph()));

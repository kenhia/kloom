import { error, json } from '@sveltejs/kit';
import { parseExport } from '$engine/reader-data';
import { readerStore } from '$lib/server/reader-store';
import { requireReader } from '$lib/server/reader-data';
import type { RequestHandler } from './$types';

/**
 * Merge an export file (the body) into this reader's data. It is filed under
 * whoever imports it, whatever reader it was exported for; where both hold a
 * record, the newer one wins.
 */
export const POST: RequestHandler = async ({ request, locals }) => {
	const reader = requireReader(locals.reader);
	const parsed = parseExport(await request.json().catch(() => null));
	if ('error' in parsed) error(400, `Not an export kloom can read: ${parsed.error}.`);
	return json(await readerStore().importData(reader.login, parsed));
};

import { json } from '@sveltejs/kit';
import { readerStore } from '$lib/server/reader-store';
import { requireReader } from '$lib/server/reader-data';
import type { RequestHandler } from './$types';

/** Everything the store holds for this reader, as a file to save (docs/design.md §Reader data). */
export const GET: RequestHandler = async ({ locals }) => {
	const data = await readerStore().exportData(requireReader(locals.reader).login);
	return json(data, {
		headers: {
			'content-disposition': `attachment; filename="kloom-reader-data-${data.exported.slice(0, 10)}.json"`
		}
	});
};

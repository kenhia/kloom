import { error, json } from '@sveltejs/kit';
import { RECORD_ID } from '$engine/reader-data';
import { readerStore } from '$lib/server/reader-store';
import { requireReader } from '$lib/server/reader-data';
import { servedSubject } from '$lib/server/subject';
import type { RequestHandler } from '@sveltejs/kit';

/**
 * Other readers' shared answers on one frame (`?subject=&frame=`), oldest
 * first (§Shared answers, korg 3560): only those an agent's review passed,
 * never the asking reader's own, and never who shared them. Both editions
 * have it, for every reader: reading one needs no ask.
 */
export const GET: RequestHandler = async ({ url, locals }) => {
	const reader = requireReader(locals.reader);
	const subject = url.searchParams.get('subject');
	const frame = url.searchParams.get('frame');
	await servedSubject(subject);
	if (!frame || !RECORD_ID.test(frame)) error(400, 'A frame is required.');
	return json(await readerStore().sharedOn(subject!, frame, reader.login), {
		headers: { 'cache-control': 'no-store' }
	});
};

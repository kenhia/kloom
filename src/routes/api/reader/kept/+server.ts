import { error, json } from '@sveltejs/kit';
import { ANSWER_ID } from '$engine/ai/kept';
import { RECORD_ID } from '$engine/reader-data';
import { readerStore } from '$lib/server/reader-store';
import { requireReader } from '$lib/server/reader-data';
import { requireSubjectDir } from '$lib/server/subject';
import type { RequestHandler } from './$types';

/**
 * The answers the reader kept on one frame (`?subject=&frame=`), oldest
 * first, each with what grow made of it. The page carries only the counts;
 * the bodies are fetched when the Q&A section opens.
 */
export const GET: RequestHandler = async ({ url, locals }) => {
	const reader = requireReader(locals.reader);
	const subject = url.searchParams.get('subject');
	const frame = url.searchParams.get('frame');
	await requireSubjectDir(subject);
	if (!frame || !RECORD_ID.test(frame)) error(400, 'A frame is required.');
	return json(await readerStore().keptOn(reader.login, subject!, frame), {
		headers: { 'cache-control': 'no-store' }
	});
};

/** Remove one of the reader's kept answers: `{subject, id}`. */
export const DELETE: RequestHandler = async ({ request, locals }) => {
	const reader = requireReader(locals.reader);
	const body = (await request.json().catch(() => null)) as Record<string, unknown> | null;
	await requireSubjectDir(body?.subject);
	const id = body?.id;
	if (typeof id !== 'string' || !ANSWER_ID.test(id)) error(400, 'A kept answer id is required.');
	if (!(await readerStore().forget(reader.login, body!.subject as string, id)))
		error(404, 'No such kept answer.');
	return json({ ok: true });
};

import { json } from '@sveltejs/kit';
import { readerStore } from '$lib/server/reader-store';
import { requireReader, requireRecord } from '$lib/server/reader-data';
import type { RequestHandler } from './$types';

/** Every bookmark of the reader's, across subjects. */
export const GET: RequestHandler = async ({ locals }) =>
	json(await readerStore().bookmarks(requireReader(locals.reader).login));

/** Bookmark a frame: `{subject, frame, label}`. */
export const POST: RequestHandler = async ({ request, locals }) => {
	const reader = requireReader(locals.reader);
	const mark = await requireRecord(await request.json().catch(() => null));
	await readerStore().bookmark(reader.login, mark);
	return json({ ok: true });
};

/** Remove a bookmark: `{subject, frame, label}` (the label is not needed, but checked like the rest). */
export const DELETE: RequestHandler = async ({ request, locals }) => {
	const reader = requireReader(locals.reader);
	const body = (await request.json().catch(() => null)) as Record<string, unknown> | null;
	const mark = await requireRecord(body && { label: '', ...body });
	await readerStore().unbookmark(reader.login, mark.subject, mark.frame);
	return json({ ok: true });
};

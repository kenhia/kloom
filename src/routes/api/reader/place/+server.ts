import { json } from '@sveltejs/kit';
import { readerStore } from '$lib/server/reader-store';
import { requireReader, requireRecord } from '$lib/server/reader-data';
import type { RequestHandler } from './$types';

/** The reader is on this frame now: `{subject, frame, label}`. Sent as they move. */
export const POST: RequestHandler = async ({ request, locals }) => {
	const reader = requireReader(locals.reader);
	const place = await requireRecord(await request.json().catch(() => null));
	await readerStore().visit(reader.login, place);
	return json({ ok: true });
};

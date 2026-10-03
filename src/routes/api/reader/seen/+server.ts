import { json } from '@sveltejs/kit';
import { readerStore } from '$lib/server/reader-store';
import { requireReader } from '$lib/server/reader-data';
import { requireFrames } from '$lib/server/whats-new';
import type { RequestHandler } from './$types';

/**
 * "Mark all as seen" (korg 3525): `{subject, frames}` are no longer new to
 * the reader. Opening a frame does this already, through the place.
 */
export const POST: RequestHandler = async ({ request, locals }) => {
	const reader = requireReader(locals.reader);
	const { subject, frames } = await requireFrames(await request.json().catch(() => null));
	await readerStore().markSeen(reader.login, subject, frames);
	return json({ ok: true });
};

import { json } from '@sveltejs/kit';
import { readerStore } from '$lib/server/reader-store';
import { requireReader } from '$lib/server/reader-data';
import { servedSubject } from '$lib/server/subject';
import type { RequestHandler } from './$types';

/**
 * "I'm caught up on this subject" (korg 3525): `{subject}`. Nothing added
 * before now is new to the reader there, and the Changelog's "since I caught
 * up" counts from now. Their reading of the subject comes back.
 */
export const POST: RequestHandler = async ({ request, locals }) => {
	const reader = requireReader(locals.reader);
	const body = (await request.json().catch(() => null)) as Record<string, unknown> | null;
	const head = await servedSubject(body?.subject);
	return json(await readerStore().catchUp(reader.login, head.id));
};

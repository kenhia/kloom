import { error, json } from '@sveltejs/kit';
import { readerStore } from '$lib/server/reader-store';
import { requireReader } from '$lib/server/reader-data';
import { servedFrame } from '$lib/server/subject';
import type { RequestHandler } from './$types';

/**
 * The reader stayed on a frame five seconds (docs/design.md §Traffic, korg
 * 3570): `{subject, frame}`. One more visit to it today, and it is opened,
 * no longer new to them (§What's new).
 */
export const POST: RequestHandler = async ({ request, locals }) => {
	const reader = requireReader(locals.reader);
	const b = (await request.json().catch(() => null)) as Record<string, unknown> | null;
	if (!(await servedFrame(b?.subject, b?.frame)))
		error(400, 'A served subject and one of its frames are required.');
	await readerStore().frameVisit(reader.login, b!.subject as string, b!.frame as string);
	return json({ ok: true });
};

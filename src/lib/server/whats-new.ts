import { error } from '@sveltejs/kit';
import { newToYou, type ReaderNews } from '$engine/whats-new';
import type { ReaderStore } from '$engine/reader-data';
import { servedAdded, servedSubject } from './subject';

/**
 * What's new to one reader (docs/design.md §What's new, korg 3525): the
 * subjects they have started, when their last visit ended, and, in every
 * served subject, the frames added since they started it (or caught up on
 * it) that they have not opened.
 */
export async function readerNews(store: ReaderStore, login: string): Promise<ReaderNews> {
	const [readings, seen, lastVisit, added] = await Promise.all([
		store.readings(login),
		store.seenFrames(login),
		store.lastVisit(login),
		servedAdded()
	]);
	const fresh: Record<string, string[]> = {};
	for (const [subject, frames] of Object.entries(added)) {
		const ids = newToYou(frames, readings[subject], seen[subject] ?? []);
		if (ids.length) fresh[subject] = ids;
	}
	return { readings, lastVisit, fresh };
}

/** Most frames one request may mark seen: a subject's worth, many times over. */
const FRAMES_MAX = 2000;

/**
 * A served subject, and frames it has, from a request body (`{subject,
 * frames}`): 404 for an unknown subject, 400 for a frame it does not have.
 */
export async function requireFrames(body: unknown): Promise<{ subject: string; frames: string[] }> {
	const b = body as Record<string, unknown> | null;
	const head = await servedSubject(b?.subject);
	const frames = b?.frames;
	if (!Array.isArray(frames) || frames.length > FRAMES_MAX)
		error(400, 'A list of frames is required.');
	for (const f of frames)
		if (typeof f !== 'string' || !Object.hasOwn(head.frames, f))
			error(400, `No frame "${String(f)}" in ${head.id}.`);
	return { subject: head.id, frames: [...new Set(frames as string[])] };
}

import { access } from 'node:fs/promises';
import { join } from 'node:path';
import { error } from '@sveltejs/kit';
import { recordOf } from '$engine/reader-data';
import type { Reader } from './reader';
import { requireSubjectDir } from './subject';

/** The reader a reader-data route acts for; the hook already refused anonymous writes. */
export function requireReader(reader: Reader | null): Reader {
	if (!reader) error(401, 'Reading data belongs to a signed-in reader, and this request had none.');
	return reader;
}

/**
 * A place or bookmark from a request body: a served subject (404 otherwise)
 * and a frame that subject has on disk (400 otherwise). The label is the
 * reader's own display text, kept short.
 */
export async function requireRecord(body: unknown) {
	const r = recordOf(body);
	const subject = (body as Record<string, unknown> | null)?.subject;
	const dir = await requireSubjectDir(r?.subject ?? subject);
	if (!r) error(400, 'A subject, frame and label are required.');
	const found = await access(join(dir, 'frames', r.frame, 'frame.json')).then(
		() => true,
		() => false
	);
	if (!found) error(400, `No frame "${r.frame}" in ${r.subject}.`);
	return r;
}

/** What a note id looks like: the store makes them (UUIDs). */
export const NOTE_ID = /^[\w-]{1,64}$/;

/** Most notes one request may name: a bulk clear, or answers seen. */
const IDS_MAX = 1000;

/** A body's `ids`, a list of note ids; null when it is not one. */
export function noteIds(body: Record<string, unknown> | null): string[] | null {
	const ids = body?.ids;
	if (!Array.isArray(ids) || ids.length > IDS_MAX) return null;
	return ids.every((id) => typeof id === 'string' && NOTE_ID.test(id)) ? (ids as string[]) : null;
}

import { error, json } from '@sveltejs/kit';
import { anchorOf } from '$engine/anchor';
import { NOTE_MAX } from '$engine/reader-data';
import { readerStore } from '$lib/server/reader-store';
import { NOTE_ID, noteIds, requireReader, requireRecord } from '$lib/server/reader-data';
import { requireSubjectDir } from '$lib/server/subject';
import type { RequestHandler } from './$types';

/** The reader's notes in a subject (`?subject=`), oldest first. */
export const GET: RequestHandler = async ({ url, locals }) => {
	const reader = requireReader(locals.reader);
	const subject = url.searchParams.get('subject');
	await requireSubjectDir(subject);
	return json(await readerStore().notes(reader.login, subject!));
};

/**
 * Write a note: `{subject, frame, label, text, flag}`, plus `id` to edit one
 * of theirs. `flag` is the "Agent review" box, and a new note may carry an
 * `anchor`, the words it is on, which makes it an annotation (an edit keeps
 * the anchor it has). Returns the note as stored.
 */
export const POST: RequestHandler = async ({ request, locals }) => {
	const reader = requireReader(locals.reader);
	const body = (await request.json().catch(() => null)) as Record<string, unknown> | null;
	const record = await requireRecord(body);
	const { id, text, flag } = body!;
	const anchor = body!.anchor == null ? null : anchorOf(body!.anchor);
	if (body!.anchor != null && !anchor) error(400, 'An annotation’s anchor is malformed.');
	if (id !== undefined && (typeof id !== 'string' || !NOTE_ID.test(id)))
		error(400, 'A note id is malformed.');
	if (typeof text !== 'string' || !text.trim()) error(400, 'A note needs some text.');
	if (text.length > NOTE_MAX) error(400, `Notes are limited to ${NOTE_MAX} characters.`);
	const note = await readerStore().saveNote(reader.login, {
		...record,
		...(id === undefined ? {} : { id }),
		text,
		flag: flag === true,
		anchor
	});
	if (!note) error(404, 'No such note.');
	return json(note);
};

/**
 * Tick or untick a note's "Agent review" box, its text untouched: `{id,
 * flag}` (My notes, korg 3481). Returns the note as stored.
 */
export const PATCH: RequestHandler = async ({ request, locals }) => {
	const reader = requireReader(locals.reader);
	const body = (await request.json().catch(() => null)) as Record<string, unknown> | null;
	const id = body?.id;
	if (typeof id !== 'string' || !NOTE_ID.test(id)) error(400, 'A note id is required.');
	if (typeof body?.flag !== 'boolean') error(400, 'Say whether the note is flagged.');
	const note = await readerStore().flagNote(reader.login, id, body.flag);
	if (!note) error(404, 'No such note.');
	return json(note);
};

/**
 * Delete one of the reader's notes, `{id}`, or several, `{ids}` (My notes'
 * bulk clears). Several returns how many were theirs to delete.
 */
export const DELETE: RequestHandler = async ({ request, locals }) => {
	const reader = requireReader(locals.reader);
	const body = (await request.json().catch(() => null)) as Record<string, unknown> | null;
	if (body?.ids !== undefined) {
		const ids = noteIds(body);
		if (!ids) error(400, 'A list of note ids is required.');
		return json({ deleted: await readerStore().deleteNotes(reader.login, ids) });
	}
	const id = body?.id;
	if (typeof id !== 'string' || !NOTE_ID.test(id)) error(400, 'A note id is required.');
	if (!(await readerStore().deleteNote(reader.login, id))) error(404, 'No such note.');
	return json({ ok: true });
};

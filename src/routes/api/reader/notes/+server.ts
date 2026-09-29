import { error, json } from '@sveltejs/kit';
import { NOTE_MAX } from '$engine/reader-data';
import { readerStore } from '$lib/server/reader-store';
import { requireReader, requireRecord } from '$lib/server/reader-data';
import { requireSubjectDir } from '$lib/server/subject';
import type { RequestHandler } from './$types';

/** What a note id looks like: the store makes them (UUIDs). */
const NOTE_ID = /^[\w-]{1,64}$/;

/** The reader's notes in a subject (`?subject=`), oldest first. */
export const GET: RequestHandler = async ({ url, locals }) => {
	const reader = requireReader(locals.reader);
	const subject = url.searchParams.get('subject');
	await requireSubjectDir(subject);
	return json(await readerStore().notes(reader.login, subject!));
};

/**
 * Write a note: `{subject, frame, label, text, flag}`, plus `id` to edit one
 * of theirs. `flag` is the "Agent review" box. Returns the note as stored.
 */
export const POST: RequestHandler = async ({ request, locals }) => {
	const reader = requireReader(locals.reader);
	const body = (await request.json().catch(() => null)) as Record<string, unknown> | null;
	const record = await requireRecord(body);
	const { id, text, flag } = body!;
	if (id !== undefined && (typeof id !== 'string' || !NOTE_ID.test(id)))
		error(400, 'A note id is malformed.');
	if (typeof text !== 'string' || !text.trim()) error(400, 'A note needs some text.');
	if (text.length > NOTE_MAX) error(400, `Notes are limited to ${NOTE_MAX} characters.`);
	const note = await readerStore().saveNote(reader.login, {
		...record,
		...(id === undefined ? {} : { id }),
		text,
		flag: flag === true
	});
	if (!note) error(404, 'No such note.');
	return json(note);
};

/** Delete one of the reader's notes: `{id}`. */
export const DELETE: RequestHandler = async ({ request, locals }) => {
	const reader = requireReader(locals.reader);
	const id = ((await request.json().catch(() => null)) as Record<string, unknown> | null)?.id;
	if (typeof id !== 'string' || !NOTE_ID.test(id)) error(400, 'A note id is required.');
	if (!(await readerStore().deleteNote(reader.login, id))) error(404, 'No such note.');
	return json({ ok: true });
};

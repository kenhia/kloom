import { error, json } from '@sveltejs/kit';
import type { MyNotesData, NoteEntry } from '$engine/my-notes';
import { readerStore } from '$lib/server/reader-store';
import { noteIds, requireReader } from '$lib/server/reader-data';
import { servedSubject, servedSubjects } from '$lib/server/subject';
import type { RequestHandler } from './$types';

/**
 * Every note and annotation of the reader's, across subjects, the last
 * written first, and how many agent answers wait to be seen (My notes, korg
 * 3481). Each says where it is as the library has it now: a subject no longer
 * served, or a frame it no longer has, leaves the note listed, to be cleared,
 * with nowhere to go.
 */
export const GET: RequestHandler = async ({ locals }) => {
	const reader = requireReader(locals.reader);
	const store = readerStore();
	const [notes, unseen, subjects] = await Promise.all([
		store.allNotes(reader.login),
		store.unseenAnswers(reader.login),
		servedSubjects()
	]);
	const titles = new Map(subjects.map((s) => [s.id, s.title]));
	const heads = new Map(
		await Promise.all(
			[...new Set(notes.map((n) => n.subject))]
				.filter((id) => titles.has(id))
				.map(async (id) => [id, await servedSubject(id)] as const)
		)
	);
	const entries: NoteEntry[] = notes.map((n) => {
		const f = heads.get(n.subject)?.frames[n.frame];
		return {
			...n,
			subjectTitle: titles.get(n.subject) ?? null,
			topic: f?.topic ?? null,
			position: f?.position.label ?? null
		};
	});
	return json({ notes: entries, unseen } satisfies MyNotesData);
};

/** The reader has seen these notes' answers: `{ids}`. Returns how many still wait. */
export const POST: RequestHandler = async ({ request, locals }) => {
	const reader = requireReader(locals.reader);
	const ids = noteIds((await request.json().catch(() => null)) as Record<string, unknown> | null);
	if (!ids) error(400, 'A list of note ids is required.');
	const store = readerStore();
	await store.seeNotes(reader.login, ids);
	return json({ unseen: await store.unseenAnswers(reader.login) });
};

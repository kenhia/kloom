import { redirect } from '@sveltejs/kit';
import { aiOffer } from '$edition/offer';
import type { AiOffered } from '$lib/edition/full/offer';
import { readerStore } from '$lib/server/reader-store';
import {
	servedBody,
	servedBuild,
	servedStart,
	servedSubject,
	servedSubjects
} from '$lib/server/subject';
import type { Bookmark, Place } from '$engine/reader-data';
import { around, type ServedBody } from '$engine/served';
import type { PageServerLoad } from './$types';

/** A reader-data record with its subject's title, for lists that span subjects. */
export type Placed<T> = T & { subjectTitle: string };

// From the library (docs/design.md §Serving), current with the files on
// disk; the AI pane's offer comes from the edition (src/lib/edition/). An unknown subject is a 404. `/<subject>/<frame>` is a
// deep link; one to a frame the subject no longer has (a stale bookmark, say)
// opens the subject instead.
//
// The page carries every frame's head and only the bodies around the frame
// it opens on; the shell fetches the rest as the reader moves.
export const load: PageServerLoad = async ({ params, locals }) => {
	const [subject, ai, subjects, build] = await Promise.all([
		servedSubject(params.subject),
		aiOffer() as Promise<AiOffered>,
		servedSubjects(),
		servedBuild()
	]);
	if (params.frame && !subject.frames[params.frame]) redirect(307, `/${subject.id}`);
	const opening = params.frame ?? subject.spine.segments[0].frames[0];
	const [start, ...found] = await Promise.all([
		servedStart(subject.id),
		...around(subject, opening).map(async (id) => [id, await servedBody(subject.id, id)] as const)
	]);
	const bodies: Record<string, ServedBody> = {};
	for (const [id, body] of found) if (body) bodies[id] = JSON.parse(body.json);

	// The reader's own data (korg 3413, 3414, 3409, 3390, 3424). Records naming a
	// subject that is no longer served, or a frame this subject no longer has,
	// are left out. Notes come whole; kept answers only as counts per frame,
	// for the spine's marks, and their bodies when the Q&A section opens.
	// A store that fails costs the reader their places, never the page.
	const titleOf = new Map(subjects.map((s) => [s.id, s.title]));
	const live = <T extends Place | Bookmark>(r: T | null): Placed<T> | null =>
		r && titleOf.has(r.subject) && (r.subject !== subject.id || !!subject.frames[r.frame])
			? { ...r, subjectTitle: titleOf.get(r.subject)! }
			: null;
	let readerData = null;
	if (locals.reader) {
		try {
			const store = readerStore();
			const login = locals.reader.login;
			const [places, last, marks, notes, kept, unseen] = await Promise.all([
				Promise.all(subjects.map((s) => store.lastVisited(login, s.id))),
				store.lastVisited(login),
				store.bookmarks(login),
				store.notes(login, subject.id),
				// Kept answers are the full edition's (korg 3500).
				__KLOOM_EDITION__ === 'reader'
					? Promise.resolve({} as Record<string, number>)
					: store.keptCounts(login, subject.id),
				store.unseenAnswers(login)
			]);
			const onFrame = (id: string) => Object.hasOwn(subject.frames, id);
			readerData = {
				// Each subject's place, for the start screen's subject list.
				places: Object.fromEntries(
					places.map(live).flatMap((p) => (p ? [[p.subject, p] as const] : []))
				),
				last: live(last),
				bookmarks: marks.map(live).filter((b) => b !== null),
				notes: notes.filter((n) => onFrame(n.frame)),
				kept: Object.fromEntries(Object.entries(kept).filter(([id]) => onFrame(id))),
				// Agent answers the reader has not seen, across subjects (§My notes).
				unseen
			};
		} catch (e) {
			console.error('reader data: could not read the store', e);
		}
	}

	return {
		subject,
		subjects,
		start: start!,
		bodies,
		build,
		frame: params.frame ?? null,
		// A signed-in public reader (the reader edition) may sign out.
		reader: locals.reader
			? { name: locals.reader.name, signedIn: locals.reader.via === 'session' }
			: null,
		readerData,
		// The AI pane's offer; null in the reader edition, which has no AI pane.
		ai
	};
};

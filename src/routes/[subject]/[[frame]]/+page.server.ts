import { redirect } from '@sveltejs/kit';
import { loadAppConfig, webMode } from '$lib/server/app-config';
import { listSubjects } from '$lib/server/config';
import { readerStore } from '$lib/server/reader-store';
import { servedSubject } from '$lib/server/subject';
import type { Bookmark, Place } from '$engine/reader-data';
import type { PageServerLoad } from './$types';

/** A reader-data record with its subject's title, for lists that span subjects. */
export type Placed<T> = T & { subjectTitle: string };

// Read per request, so content written to disk, and a model renamed in the
// app config, show without a rebuild. An unknown subject is a 404.
// `/<subject>/<frame>` is a deep link; one to a frame the subject no longer
// has (a stale bookmark, say) opens the subject instead.
export const load: PageServerLoad = async ({ params, locals }) => {
	const [subject, config, subjects] = await Promise.all([
		servedSubject(params.subject),
		loadAppConfig(),
		listSubjects()
	]);
	if (params.frame && !subject.frames[params.frame]) redirect(307, `/${subject.id}`);

	// The reader's own data (korg 3413, 3414, 3409, 3390). Records naming a
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
			const [here, last, marks, notes, kept] = await Promise.all([
				store.lastVisited(login, subject.id),
				store.lastVisited(login),
				store.bookmarks(login),
				store.notes(login, subject.id),
				store.keptCounts(login, subject.id)
			]);
			const onFrame = (id: string) => Object.hasOwn(subject.frames, id);
			readerData = {
				here: live(here),
				last: last?.subject === subject.id ? null : live(last),
				bookmarks: marks.map(live).filter((b) => b !== null),
				notes: notes.filter((n) => onFrame(n.frame)),
				kept: Object.fromEntries(Object.entries(kept).filter(([id]) => onFrame(id)))
			};
		} catch (e) {
			console.error('reader data: could not read the store', e);
		}
	}

	return {
		subject,
		subjects,
		frame: params.frame ?? null,
		reader: locals.reader ? { name: locals.reader.name } : null,
		readerData,
		askModels: {
			choices: config.models.map((m) => ({ value: m.id, label: m.label })),
			default: config.ask.defaultModel
		},
		askWeb: webMode(config),
		growModels: config.grow
			? {
					choices: config.models.map((m) => ({ value: m.id, label: m.label })),
					default: config.grow.defaultModel
				}
			: null
	};
};

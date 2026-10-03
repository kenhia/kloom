/**
 * What's new and what changed (docs/design.md §What's new, korg 3525, 3526):
 * the Changelog's entries, which frames are new to a reader, and the
 * Changelog's filters. Browser-safe; the compiler builds the entries
 * (`engine/content-db.ts`) and the reader store keeps the reader's side.
 *
 * Two ways of reading are served. A reader who browses wants the Changelog,
 * filtered by subject and date. A reader who goes straight through a subject
 * wants "new to you" marks on what appeared after they started it and they
 * have not opened yet.
 */

import type { EditKind, SubjectHead } from './model';
import { stops } from './navigation';

/**
 * An `added` override (a day) as a time: noon UTC, so it reads as the same
 * day in every timezone a reader is likely to be in.
 */
export const dayTime = (day: string) => `${day}T12:00:00.000Z`;

/** An edit's kind in words, where it is listed. */
export const EDIT_WORD: Record<EditKind, string> = {
	correction: 'Correction',
	revision: 'Revision'
};

/** Something the Changelog says arrived: a frame, a trail with its frames, or a subject's first publish. */
export interface AddedEntry {
	subject: string;
	/** When it arrived: an ISO 8601 time. */
	at: string;
	kind: 'frame' | 'trail' | 'subject';
	/** The frame's, the trail's or the subject's id. */
	id: string;
	/** Where the entry goes: the frame, the trail's first frame, the subject's first frame. */
	frame: string;
	/** What it is called: the frame's topic, the trail's title, the subject's title. */
	title: string;
	/** A frame's position label; empty for a trail or a subject. */
	position: string;
	/** For a frame on a trail, the trail's title. */
	trail?: string;
	/** The frames a trail or a subject brought with it. */
	frames?: string[];
}

/** An edit or correction, as the Changelog's second tab lists it (korg 3526). */
export interface EditEntry {
	subject: string;
	frame: string;
	/** The frame's topic and position, to name it in a list that spans subjects. */
	title: string;
	position: string;
	/** `YYYY-MM-DD`. */
	date: string;
	kind: EditKind;
	summary: string;
}

/** A subject as the Changelog names it. */
export interface ChangelogSubject {
	id: string;
	title: string;
	/** Its first publish; null where the content has no history. */
	created: string | null;
}

/** What `/api/changelog` sends: built with the library, the same for every reader. */
export interface ChangelogData {
	subjects: ChangelogSubject[];
	/** Newest first. */
	added: AddedEntry[];
	/** Newest first. */
	edits: EditEntry[];
}

/** A frame or edit as it is written, for building the edits tab. */
export interface FrameEdit {
	subject: string;
	frame: string;
	date: string;
	kind: EditKind;
	summary: string;
}

const newestFirst = (a: string, b: string) => (a < b ? 1 : a > b ? -1 : 0);

/**
 * The Changelog's entries from dated heads (each frame's and trail's `added`
 * in force, the subject's `created`) and every frame's edits. Everything that
 * came with a subject's first publish is one entry, and so is a trail with
 * the frames it came with. An undated frame (not yet committed) is left out.
 */
export function changelogOf(heads: SubjectHead[], edits: FrameEdit[]): ChangelogData {
	const added: AddedEntry[] = [];
	const byId = new Map(heads.map((h) => [h.id, h]));
	for (const h of heads) {
		const onTrail = new Map<string, { id: string; title: string; added?: string }>();
		for (const t of h.trails) for (const s of stops(t.spine)) onTrail.set(s.frameId, t);
		const first = h.spine.segments[0]?.frames[0];
		const initial: string[] = [];
		const withTrail = new Map<string, string[]>();
		const frames: AddedEntry[] = [];
		for (const s of [...stops(h.spine), ...h.trails.flatMap((t) => stops(t.spine))]) {
			const f = h.frames[s.frameId];
			if (!f?.added) continue;
			if (h.created && f.added === h.created) {
				initial.push(f.id);
				continue;
			}
			const t = onTrail.get(f.id);
			if (t && t.added === f.added) {
				withTrail.set(t.id, [...(withTrail.get(t.id) ?? []), f.id]);
				continue;
			}
			frames.push({
				subject: h.id,
				at: f.added,
				kind: 'frame',
				id: f.id,
				frame: f.id,
				title: f.topic,
				position: f.position.label,
				...(t ? { trail: t.title } : {})
			});
		}
		if (h.created && first)
			added.push({
				subject: h.id,
				at: h.created,
				kind: 'subject',
				id: h.id,
				frame: first,
				title: h.title,
				position: '',
				frames: initial
			});
		for (const t of h.trails) {
			const brought = withTrail.get(t.id);
			// A trail that came with its subject is part of the first publish.
			if (!t.added || t.added === h.created) continue;
			added.push({
				subject: h.id,
				at: t.added,
				kind: 'trail',
				id: t.id,
				frame: t.spine.segments[0].frames[0],
				title: t.title,
				position: '',
				frames: brought ?? []
			});
		}
		added.push(...frames);
	}
	added.sort((a, b) => newestFirst(a.at, b.at) || a.subject.localeCompare(b.subject));
	const editEntries = edits
		.filter((e) => byId.get(e.subject)?.frames[e.frame])
		.map((e): EditEntry => {
			const f = byId.get(e.subject)!.frames[e.frame];
			return { ...e, title: f.topic, position: f.position.label };
		})
		.sort((a, b) => newestFirst(a.date, b.date) || a.subject.localeCompare(b.subject));
	return {
		subjects: heads.map((h) => ({ id: h.id, title: h.title, created: h.created ?? null })),
		added,
		edits: editEntries
	};
}

/** A reader's reading of one subject: when they first came to it, and when they last caught up. */
export interface Reading {
	/** Their first visit: an ISO 8601 time. */
	first: string;
	/** When they said "I'm caught up on this subject"; null if never. */
	caughtUp: string | null;
}

/** What a subject's "new to you" counts from: the later of their first visit and their catching up. */
export const readingFrom = (r: Reading): string =>
	r.caughtUp && Date.parse(r.caughtUp) > Date.parse(r.first) ? r.caughtUp : r.first;

/**
 * The frames new to a reader in one subject (korg 3525): added after they
 * started the subject (or last caught up on it), and not opened since. A
 * subject they have never visited has nothing new: all of it is.
 */
export function newToYou(
	added: Record<string, string>,
	reading: Reading | null | undefined,
	seen: Iterable<string>
): string[] {
	if (!reading) return [];
	const from = Date.parse(readingFrom(reading));
	const opened = new Set(seen);
	return Object.entries(added)
		.filter(([id, at]) => Date.parse(at) > from && !opened.has(id))
		.map(([id]) => id)
		.sort();
}

/** A head's `added` in force for each frame. */
export const addedOf = (head: SubjectHead): Record<string, string> =>
	Object.fromEntries(
		Object.values(head.frames).flatMap((f) => (f.added ? [[f.id, f.added] as const] : []))
	);

/**
 * The trails with something new to the reader on them: a trail marker says
 * "new" when any of its frames is.
 */
export const newTrails = (head: SubjectHead, isNew: ReadonlySet<string>): Set<string> =>
	new Set(
		head.trails.filter((t) => stops(t.spine).some((s) => isNew.has(s.frameId))).map((t) => t.id)
	);

/** What the reader's side of the Changelog knows: each subject's reading, and their last visit. */
export interface ReaderNews {
	readings: Record<string, Reading>;
	/** When their previous visit ended; null if this is their first. */
	lastVisit: string | null;
	/** Frames new to them, by subject. */
	fresh: Record<string, string[]>;
}

/** The Changelog's "when" choices. */
export const WHENS = ['all', 'last-visit', 'caught-up', '7', '30', 'between'] as const;
export type When = (typeof WHENS)[number];

export const WHEN_LABEL: Record<When, string> = {
	all: 'All time',
	'last-visit': 'Since my last visit',
	'caught-up': 'Since I caught up',
	'7': 'Last 7 days',
	'30': 'Last 30 days',
	between: 'Between dates'
};

export interface ChangelogFilter {
	/** Subject ids to show; empty shows every one. */
	subjects: string[];
	when: When;
	/** For `between`: local days, `YYYY-MM-DD`, inclusive; either may be empty. */
	from: string;
	to: string;
}

export const ALL: ChangelogFilter = { subjects: [], when: 'all', from: '', to: '' };

export interface FilterContext {
	now: Date;
	/** The reader's side; null with no reader, when the reader's presets match everything. */
	news: ReaderNews | null;
	/** The local day an ISO time falls on, `YYYY-MM-DD`. */
	dayOf: (iso: string) => string;
}

/** The local day an ISO time falls on, in the browser's timezone. */
export function localDay(iso: string): string {
	const d = new Date(iso);
	const pad = (n: number) => String(n).padStart(2, '0');
	return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`;
}

/**
 * Whether something in `subject` that happened at `at` passes the filter.
 * An edit has a day, not a time: it is taken as that day's noon UTC.
 * "Since I caught up" counts from each subject's own mark: the reader's
 * catching up, or, before they have, their first visit; a subject they have
 * never visited shows everything.
 */
export function passes(f: ChangelogFilter, subject: string, at: string, c: FilterContext): boolean {
	if (f.subjects.length && !f.subjects.includes(subject)) return false;
	const t = Date.parse(at);
	switch (f.when) {
		case 'all':
			return true;
		case 'last-visit': {
			const v = c.news?.lastVisit;
			return !v || t > Date.parse(v);
		}
		case 'caught-up': {
			const r = c.news?.readings[subject];
			return !r || t > Date.parse(readingFrom(r));
		}
		case '7':
		case '30':
			return t > c.now.getTime() - Number(f.when) * 86_400_000;
		case 'between': {
			const day = c.dayOf(at);
			return (!f.from || day >= f.from) && (!f.to || day <= f.to);
		}
	}
}

/** The entries passing the filter, as the Changelog lists them. */
export function filterChangelog(
	data: ChangelogData,
	f: ChangelogFilter,
	c: FilterContext
): { added: AddedEntry[]; edits: EditEntry[] } {
	return {
		added: data.added.filter((e) => passes(f, e.subject, e.at, c)),
		edits: data.edits.filter((e) => passes(f, e.subject, dayTime(e.date), c))
	};
}

/** Entries by local day, then by subject, in the order given (newest first). */
export function byDayAndSubject<T extends { subject: string }>(
	entries: T[],
	dayOf: (e: T) => string
): { day: string; subjects: { subject: string; entries: T[] }[] }[] {
	const days: { day: string; subjects: { subject: string; entries: T[] }[] }[] = [];
	for (const e of entries) {
		const day = dayOf(e);
		let d = days[days.length - 1];
		if (d?.day !== day) days.push((d = { day, subjects: [] }));
		let s = d.subjects.find((x) => x.subject === e.subject);
		if (!s) d.subjects.push((s = { subject: e.subject, entries: [] }));
		s.entries.push(e);
	}
	return days;
}

/** A day as the Changelog heads it: "October 3, 2026". */
export function dayLabel(day: string): string {
	const [y, m, d] = day.split('-').map(Number);
	return new Date(Date.UTC(y, m - 1, d, 12)).toLocaleDateString('en-US', {
		year: 'numeric',
		month: 'long',
		day: 'numeric',
		timeZone: 'UTC'
	});
}

/** The frames an entry stands for, as "new to you" counts them. */
export const entryFrames = (e: AddedEntry): string[] =>
	e.kind === 'frame' ? [e.frame] : (e.frames ?? []);

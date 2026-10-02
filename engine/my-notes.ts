/**
 * My notes (docs/design.md §My notes, korg 3481): every note and annotation
 * a reader has, across subjects, in one list. What each one's state is, what
 * the filters keep, and how the list is grouped. Browser-safe; the panel is
 * `engine/ui/MyNotes.svelte`.
 */

import { findQuote } from './anchor';
import type { Note } from './reader-data';

/** A note in the list, with where it is as the library has it now. */
export interface NoteEntry extends Note {
	/** The subject's title; null when the library no longer serves the subject. */
	subjectTitle: string | null;
	/** The frame's topic and position; null when the subject no longer has the frame. */
	topic: string | null;
	position: string | null;
}

/** What the route sends: the list, the last written first, and how many answers wait. */
export interface MyNotesData {
	notes: NoteEntry[];
	unseen: number;
}

export type NotesFilter = 'all' | 'pending' | 'answered' | 'detached';

export const FILTERS: { id: NotesFilter; label: string }[] = [
	{ id: 'all', label: 'All' },
	{ id: 'pending', label: 'Agent review' },
	{ id: 'answered', label: 'Answered' },
	{ id: 'detached', label: 'Detached' }
];

/** Whether a note can be gone to: its subject is served and still has its frame. */
export const isLive = (n: NoteEntry) => n.subjectTitle !== null && n.topic !== null;

/** A note's state, in words, never an icon alone. A note may be answered and detached at once. */
export function statesOf(n: Note, detached: ReadonlySet<string>): string[] {
	const out: string[] = [];
	if (n.review === 'flagged') out.push('Agent review (pending)');
	if (n.review === 'handled') out.push(n.unseen ? 'Answered (new)' : 'Answered');
	if (n.anchor && detached.has(n.id)) out.push('Detached');
	return out;
}

/** Whether a filter keeps a note. */
export function keeps(filter: NotesFilter, n: Note, detached: ReadonlySet<string>): boolean {
	switch (filter) {
		case 'pending':
			return n.review === 'flagged';
		case 'answered':
			return n.review === 'handled';
		case 'detached':
			return !!n.anchor && detached.has(n.id);
		default:
			return true;
	}
}

/** How many notes each filter keeps, for its label. */
export function filterCounts(
	notes: Note[],
	detached: ReadonlySet<string>
): Record<NotesFilter, number> {
	const counts = { all: 0, pending: 0, answered: 0, detached: 0 };
	for (const n of notes) for (const f of FILTERS) if (keeps(f.id, n, detached)) counts[f.id] += 1;
	return counts;
}

/**
 * The list grouped by subject: each group's notes in the list's order (the
 * last written first), and the groups in the order of their newest note.
 */
export function bySubject<N extends NoteEntry>(
	notes: N[]
): { subject: string; title: string; notes: N[] }[] {
	const groups = new Map<string, { subject: string; title: string; notes: N[] }>();
	for (const n of notes) {
		let g = groups.get(n.subject);
		if (!g) {
			g = { subject: n.subject, title: n.subjectTitle ?? n.subject, notes: [] };
			groups.set(n.subject, g);
		}
		g.notes.push(n);
	}
	return [...groups.values()];
}

/** The annotations, one list per frame they are on. */
export function annotatedFrames<N extends Note>(notes: N[]): N[][] {
	const frames = new Map<string, N[]>();
	for (const n of notes) {
		if (!n.anchor) continue;
		const k = `${n.subject}/${n.frame}`;
		frames.set(k, [...(frames.get(k) ?? []), n]);
	}
	return [...frames.values()];
}

/**
 * The annotations on one frame whose words its reading no longer has
 * (§Annotations): `text` is the reading's text, as the narrative's text
 * nodes give it (`engine/ui/reading-text.ts`).
 */
export function detachedIn(text: string, notes: Note[]): string[] {
	return notes.filter((n) => n.anchor && !findQuote(text, n.anchor)).map((n) => n.id);
}

/** What "Clear answered" or "Clear detached" asks before it deletes `n` notes. */
export function clearQuestion(kind: 'answered' | 'detached', n: number): string {
	const what =
		kind === 'answered'
			? n === 1
				? 'the answered note'
				: `all ${n} answered notes`
			: n === 1
				? 'the detached annotation'
				: `all ${n} detached annotations`;
	return `Delete ${what}? This cannot be undone.`;
}

/** What the page offers My notes: the list and the writes, across subjects. Absent with no reader. */
export interface MyNotesOffer {
	/** How many agent answers wait to be seen, for the count on the control. */
	unseen: number;
	/** The list; null when it could not be loaded. */
	load(): Promise<MyNotesData | null>;
	/** A frame's reading as HTML, to find annotations' words in; null when it could not be had. */
	reading(subject: string, frame: string): Promise<string | null>;
	/** The reader has seen these notes' answers. */
	seen(ids: string[]): Promise<void>;
	/** Tick or untick a note's "Agent review" box; the note as stored, or null when that failed. */
	flag(note: NoteEntry, flag: boolean): Promise<Note | null>;
	/** Delete notes; how many went, or null when that failed. */
	clear(ids: string[]): Promise<number | null>;
	/** Go to a note: a jump to its frame, with its Notes tab open on it. */
	go(note: NoteEntry): void;
	/** A frame's address, for each entry's link. */
	hrefOf(subject: string, frame: string): string;
}

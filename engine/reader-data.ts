/**
 * The reader's own data (docs/design.md §Reader data, korg 3413): what one
 * person does while reading, as opposed to the subject's content. Content is
 * files in git, reviewed; reader data belongs to one person, is written
 * often, is never reviewed, and always has an author.
 *
 * Every record carries the reader it belongs to (a login, from the request's
 * `Reader`) and the subject it is about. A frame id alone says where a frame
 * is: each frame sits on exactly one spine, the main one or a trail's, so a
 * record never stores the trail.
 *
 * The store is an interface so that its adapter is a choice: SQLite now
 * (`src/lib/server/reader-store.ts`), Postgres possibly later. Its methods
 * are async for that reason, though SQLite answers at once. Each kind of
 * record (places, bookmarks, notes and annotations, kept answers) has its
 * own methods and table on the same interface, keyed the same way.
 */

import { anchorOf, type Anchor } from './anchor';
import { keptAnswerProblems, type KeptAnswer } from './ai/kept';
import type { Reading } from './whats-new';

export type { Reading } from './whats-new';

/** Where a reader last was in a subject. */
export interface Place {
	subject: string;
	frame: string;
	/** The frame's title when it was visited, for a list that spans subjects. */
	label: string;
	/** ISO 8601, UTC. */
	at: string;
}

/**
 * Each subject's place, the newer of two copies (korg 3432): the page's own,
 * moved as the reader moves, and one loaded fresh from the store, which may
 * not have the last move yet (its write waits for the reader to stop). A tie
 * goes to the load.
 */
export function newerPlaces<P extends Place>(
	page: Record<string, P>,
	loaded: Record<string, P>
): Record<string, P> {
	const out = { ...page };
	for (const [subject, p] of Object.entries(loaded))
		if (!out[subject] || p.at >= out[subject].at) out[subject] = p;
	return out;
}

/** A frame a reader has opened, or marked as seen (korg 3525): never new to them again. */
export interface SeenFrame {
	subject: string;
	frame: string;
	/** When it was first seen. */
	at: string;
}

/** A frame a reader marked to come back to. */
export interface Bookmark {
	subject: string;
	frame: string;
	label: string;
	at: string;
}

/**
 * Whether a note is flagged for an agent to look at (korg 3409): none, flagged
 * by the reader ("Agent review"), or handled by the agent, which says what it
 * did in `response`.
 */
export type Review = 'none' | 'flagged' | 'handled';

/**
 * A reader's note on a frame (docs/design.md §Notes). Plain text, never
 * rendered as markup. With an anchor it is an annotation (§Annotations, korg
 * 3415): a note on some words of the frame's reading.
 */
export interface Note {
	/** Made by the store; unique per reader. */
	id: string;
	subject: string;
	frame: string;
	/** The frame's title when the note was last saved. */
	label: string;
	text: string;
	/** The words it is on, for an annotation; null for a note on the whole frame. */
	anchor: Anchor | null;
	review: Review;
	/** What the agent that handled it did, in its own words; null until then. */
	response: string | null;
	/** The agent's answer is waiting for the reader: handled since they last saw it. */
	unseen: boolean;
	created: string;
	updated: string;
}

/**
 * A note as a reader writes it: no id for a new one. `flag` is the "Agent
 * review" box. An anchor is given when an annotation is made; an edit keeps
 * the one it has.
 */
export interface NoteInput {
	id?: string;
	subject: string;
	frame: string;
	label: string;
	text: string;
	flag: boolean;
	anchor?: Anchor | null;
}

/** A flagged note, for the review skill: which reader it belongs to comes with it. */
export type ReviewNote = Note & { reader: string };

/**
 * A kept answer as the reader's store holds it (korg 3390): the answer in its
 * own format, which grow reads, and the frames grow made of it, if it has.
 */
export interface Kept {
	answer: KeptAnswer;
	/** Frame ids a grow job made from it, in the order it listed them; null until one does. */
	grown: string[] | null;
}

/**
 * Where a suggested subject stands (korg 3459): new until Ken or an agent
 * moves it on. The reader sees it; only the review side changes it.
 */
export type SuggestionStatus = 'new' | 'planned' | 'written' | 'declined';
export const SUGGESTION_STATUSES: readonly SuggestionStatus[] = [
	'new',
	'planned',
	'written',
	'declined'
];

/**
 * A subject a reader would like kloom to have (docs/design.md §Suggestions).
 * A note to Ken, never a job: nothing agentic runs from one. Not in the
 * export, which is reading data; a deleted reader's go with them.
 */
export interface Suggestion {
	/** Made by the store; unique per reader. */
	id: string;
	title: string;
	/** What it should cover, in their words. */
	cover: string;
	/** Why they would like it; may be empty. */
	why: string;
	status: SuggestionStatus;
	created: string;
	updated: string;
}

/** A suggestion as a reader writes it. */
export type SuggestionInput = Pick<Suggestion, 'title' | 'cover' | 'why'>;

/** A suggestion for the review side: who made it, by login and by the name they went by. */
export type ReviewSuggestion = Suggestion & { reader: string; name: string };

/** What the page offers the About panel's Suggest a subject (korg 3459); absent with no reader. */
export interface SuggestOffer {
	/** The reader's own suggestions, newest first; null when they could not be had. */
	list(): Promise<Suggestion[] | null>;
	/** Send one: the stored suggestion, or what was wrong, in words. */
	send(s: SuggestionInput): Promise<Suggestion | { error: string }>;
}

/** A status in words, for the reader. */
export const SUGGESTION_STATUS_WORDS: Record<SuggestionStatus, string> = {
	new: 'Sent',
	planned: 'Planned',
	written: 'Written',
	declined: 'Declined'
};

/** Longest suggested title, and longest of each of its two texts, in characters. */
export const SUGGESTION_TITLE_MAX = 120;
export const SUGGESTION_TEXT_MAX = 2000;
/** Most suggestions one reader may have waiting (new) at once: a note to Ken, not a queue. */
export const SUGGESTIONS_WAITING_MAX = 20;

/** A suggestion from a request, checked and trimmed; null without a title, or with anything too long. */
export function suggestionOf(v: unknown): SuggestionInput | null {
	if (typeof v !== 'object' || v === null) return null;
	const r = v as Record<string, unknown>;
	const text = (x: unknown) => (x === undefined || x === null ? '' : isText(x) ? x.trim() : null);
	const [title, cover, why] = [text(r.title), text(r.cover), text(r.why)];
	if (!title || title.length > SUGGESTION_TITLE_MAX) return null;
	if (cover === null || why === null) return null;
	if (cover.length > SUGGESTION_TEXT_MAX || why.length > SUGGESTION_TEXT_MAX) return null;
	return { title, cover, why };
}

/**
 * The dwell timers (docs/design.md §Reader data, §Traffic; korg 3570). A
 * frame becomes the reader's place this long after they stop on it, so
 * "Continue" keeps even quick moves.
 */
export const PLACE_MS = 800;
/**
 * Staying this long on a frame is a visit: counted for the traffic page, and
 * the frame is opened (§What's new). A glance at the picture is shorter;
 * any reading of the narrative is longer.
 */
export const VISIT_MS = 5000;

/** Longest note accepted, in characters. */
export const NOTE_MAX = 10_000;

export interface ReaderStore {
	/**
	 * Record that `reader` is on this frame now: their place in its subject.
	 * It also starts the subject if this is their first place in it, and
	 * counts as activity, for "since my last visit". It does not open the
	 * frame: `frameVisit` does.
	 */
	visit(reader: string, place: Omit<Place, 'at'>): Promise<void>;
	/**
	 * `reader` stayed on this frame long enough to count (§Traffic, korg
	 * 3570): one more visit to it today, and it is opened (§What's new).
	 */
	frameVisit(reader: string, subject: string, frame: string): Promise<void>;
	/** Every frame anyone has opened: distinct readers, and visits counted (§Traffic). Across readers. */
	traffic(): Promise<FrameTraffic[]>;
	/** Each subject they have started: their first visit, and when they caught up (korg 3525). */
	readings(reader: string): Promise<Record<string, Reading>>;
	/** The frames they have opened or marked seen, by subject. */
	seenFrames(reader: string): Promise<Record<string, string[]>>;
	/** "Mark all as seen": these frames are not new to them any more. */
	markSeen(reader: string, subject: string, frames: string[]): Promise<void>;
	/** "I'm caught up on this subject": its watermark is now. Their reading of it, after. */
	catchUp(reader: string, subject: string): Promise<Reading>;
	/** When their last visit ended, a visit being moves with no long pause; null before one has. */
	lastVisit(reader: string): Promise<string | null>;
	/** Their place in `subject`, or, with no subject, the last place anywhere. */
	lastVisited(reader: string, subject?: string): Promise<Place | null>;
	/** Every bookmark of theirs, across subjects, newest first. */
	bookmarks(reader: string): Promise<Bookmark[]>;
	/** Mark a frame; marking it again only refreshes its label. */
	bookmark(reader: string, mark: Omit<Bookmark, 'at'>): Promise<void>;
	unbookmark(reader: string, subject: string, frame: string): Promise<void>;

	/** Their notes in `subject`, oldest first. */
	notes(reader: string, subject: string): Promise<Note[]>;
	/**
	 * Write a note: a new one without an id, or an edit of theirs with one
	 * (null when they have no such note). An edit keeps the note's frame and
	 * anchor.
	 */
	saveNote(reader: string, note: NoteInput): Promise<Note | null>;
	/** Delete a note of theirs; false when there was none. */
	deleteNote(reader: string, id: string): Promise<boolean>;
	/** Every note of theirs, across subjects, the last written first (My notes, korg 3481). */
	allNotes(reader: string): Promise<Note[]>;
	/**
	 * Tick or untick a note's "Agent review" box without touching its text,
	 * as the editor's box does: ticked flags it afresh, unticked unflags a
	 * flagged note and leaves a handled one handled. Null when they have no
	 * such note.
	 */
	flagNote(reader: string, id: string, flag: boolean): Promise<Note | null>;
	/** Delete several notes of theirs at once; how many there were. */
	deleteNotes(reader: string, ids: string[]): Promise<number>;
	/** How many of their notes have an agent's answer they have not seen. */
	unseenAnswers(reader: string): Promise<number>;
	/** They have seen these notes' answers; how many were waiting. */
	seeNotes(reader: string, ids: string[]): Promise<number>;
	/** Every flagged note, oldest first: one reader's, or, with none named, every reader's. */
	flaggedNotes(reader?: string): Promise<ReviewNote[]>;
	/**
	 * The agent dealt with a flagged note: it is handled, with what was done.
	 * False when it is gone or no longer flagged, and, given `seen` (the
	 * note's `updated` when it was read), when the reader has edited it since:
	 * an answer never lands on words it did not answer.
	 */
	handleNote(reader: string, id: string, response: string, seen?: string): Promise<boolean>;
	/** Every reader's every note, oldest first: for the detached-note check (§Annotations). */
	everyNote(): Promise<ReviewNote[]>;

	/** Suggest a subject (korg 3459), as `name`, the reader's display name now. */
	suggest(reader: string, name: string, s: SuggestionInput): Promise<Suggestion>;
	/** Their own suggestions, the newest first. */
	suggestions(reader: string): Promise<Suggestion[]>;
	/** Every reader's suggestions, oldest first, or only those with `status`: Ken's list. */
	allSuggestions(status?: SuggestionStatus): Promise<ReviewSuggestion[]>;
	/** Ken or an agent moved a suggestion on; false when there is no such suggestion. */
	markSuggestion(reader: string, id: string, status: SuggestionStatus): Promise<boolean>;

	/** Keep an answer for them. Keeping the same answer twice keeps the first. */
	keep(reader: string, answer: KeptAnswer): Promise<void>;
	/** How many answers they kept on each frame of `subject`, for the spine's marks. */
	keptCounts(reader: string, subject: string): Promise<Record<string, number>>;
	/** Their kept answers on one frame, oldest first. */
	keptOn(reader: string, subject: string, frame: string): Promise<Kept[]>;
	/** One of their kept answers, by id (what grow reads), or null. */
	kept(reader: string, subject: string, id: string): Promise<KeptAnswer | null>;
	/** A grow job made frames of a kept answer. */
	grew(reader: string, subject: string, id: string, frames: string[]): Promise<void>;
	/** Remove one of their kept answers; false when there was none. */
	forget(reader: string, subject: string, id: string): Promise<boolean>;

	/** Everything the store holds for `reader`, to back up or carry elsewhere. */
	exportData(reader: string): Promise<ReaderExport>;
	/** Merge an export in as `reader`'s; the newer of two records wins. */
	importData(reader: string, data: ReaderExport): Promise<ImportCounts>;
	/** Remove everything the store holds for `reader` (a deleted account); what there was. */
	deleteReader(reader: string): Promise<DeletedCounts>;
}

/**
 * What `deleteReader` removed: everything an import carries, and suggestions
 * and visits, which it does not.
 */
export interface DeletedCounts extends ImportCounts {
	suggestions: number;
	visits: number;
}

/** One frame's traffic (§Traffic): readers who opened it, and the visits counted to it. */
export interface FrameTraffic {
	subject: string;
	frame: string;
	readers: number;
	visits: number;
}

export interface ImportCounts {
	places: number;
	bookmarks: number;
	notes: number;
	kept: number;
	readings: number;
	seen: number;
}

/**
 * The export format: versioned, so an older file can still be read. Version
 * 2 (sprint 011) added notes and kept answers, version 3 (sprint 012)
 * notes' anchors, and version 4 (sprint 043) what's new to the reader: the
 * subjects they started and the frames they have seen. A version 1 file
 * reads as one with no notes or kept answers, a version 2 file's notes have
 * no anchors, and a file before version 4 has no readings or seen frames.
 */
export interface ReaderExport {
	kloom: 'reader-data';
	version: 4;
	/** Who it was exported for; an import files it under whoever imports it. */
	reader: string;
	exported: string;
	places: Place[];
	bookmarks: Bookmark[];
	notes: Note[];
	kept: Kept[];
	readings: ({ subject: string } & Reading)[];
	seen: SeenFrame[];
}

/** One bookmark in the jump list (`engine/ui/Bookmarks.svelte`); the page resolves where it goes. */
export interface JumpItem {
	key: string;
	label: string;
	/** Where it is: the subject, and the frame's position. */
	context: string;
	href: string;
	/** A frame in the subject being read: jumping moves the shell, not the page. */
	frame?: string;
	subject: string;
}

/** What a subject or frame id may look like: a plain name, never a path. */
export const RECORD_ID = /^[a-z0-9][a-z0-9-]*$/;

/** A label is display text for the reader's own lists; long ones are cut. */
export const LABEL_MAX = 200;

const isText = (v: unknown): v is string => typeof v === 'string';
const isTime = (v: unknown): v is string => isText(v) && !Number.isNaN(Date.parse(v));

/** The part of a place or bookmark every record shares, checked; null if it is not one. */
export function recordOf(v: unknown): { subject: string; frame: string; label: string } | null {
	if (typeof v !== 'object' || v === null) return null;
	const r = v as Record<string, unknown>;
	if (!isText(r.subject) || !RECORD_ID.test(r.subject)) return null;
	if (!isText(r.frame) || !RECORD_ID.test(r.frame)) return null;
	if (!isText(r.label)) return null;
	return { subject: r.subject, frame: r.frame, label: r.label.slice(0, LABEL_MAX) };
}

/**
 * Read an export file, or say what is wrong with it. Every record is checked,
 * and one bad record refuses the whole file rather than half-importing it.
 */
export function parseExport(v: unknown): ReaderExport | { error: string } {
	if (typeof v !== 'object' || v === null) return { error: 'not a JSON object' };
	const d = v as Record<string, unknown>;
	if (d.kloom !== 'reader-data') return { error: 'not a kloom reader-data export' };
	if (d.version !== 1 && d.version !== 2 && d.version !== 3 && d.version !== 4)
		return { error: `unknown version ${String(d.version)}` };
	if (!Array.isArray(d.places) || !Array.isArray(d.bookmarks))
		return { error: 'places and bookmarks must be lists' };
	const records = (list: unknown[], what: string) => {
		const out: Place[] = [];
		for (const [i, item] of list.entries()) {
			const r = recordOf(item);
			const at = (item as Record<string, unknown> | null)?.at;
			if (!r || !isTime(at)) return `${what} ${i} is not a valid record`;
			out.push({ ...r, at: new Date(at).toISOString() });
		}
		return out;
	};
	const places = records(d.places, 'place');
	if (typeof places === 'string') return { error: places };
	const bookmarks = records(d.bookmarks, 'bookmark');
	if (typeof bookmarks === 'string') return { error: bookmarks };
	const notes: Note[] = [];
	const kept: Kept[] = [];
	if (d.version !== 1) {
		if (!Array.isArray(d.notes) || !Array.isArray(d.kept))
			return { error: 'notes and kept must be lists' };
		for (const [i, item] of d.notes.entries()) {
			const n = noteOf(item, d.version >= 3);
			if (!n) return { error: `note ${i} is not a valid note` };
			notes.push(n);
		}
		for (const [i, item] of d.kept.entries()) {
			const k = item as Record<string, unknown> | null;
			const grown = k?.grown;
			if (
				!k ||
				keptAnswerProblems(k.answer).length ||
				!(grown === null || (Array.isArray(grown) && grown.every((f) => isId(f))))
			)
				return { error: `kept answer ${i} is not a valid kept answer` };
			kept.push({ answer: k.answer as KeptAnswer, grown: grown as string[] | null });
		}
	}
	const readings: ReaderExport['readings'] = [];
	const seen: SeenFrame[] = [];
	if (d.version === 4) {
		if (!Array.isArray(d.readings) || !Array.isArray(d.seen))
			return { error: 'readings and seen must be lists' };
		for (const [i, item] of d.readings.entries()) {
			const r = item as Record<string, unknown> | null;
			if (
				!r ||
				!isId(r.subject) ||
				!isTime(r.first) ||
				!(r.caughtUp === null || isTime(r.caughtUp))
			)
				return { error: `reading ${i} is not a valid reading` };
			readings.push({
				subject: r.subject,
				first: new Date(r.first).toISOString(),
				caughtUp: r.caughtUp === null ? null : new Date(r.caughtUp as string).toISOString()
			});
		}
		for (const [i, item] of d.seen.entries()) {
			const r = item as Record<string, unknown> | null;
			if (!r || !isId(r.subject) || !isId(r.frame) || !isTime(r.at))
				return { error: `seen frame ${i} is not a valid record` };
			seen.push({ subject: r.subject, frame: r.frame, at: new Date(r.at).toISOString() });
		}
	}
	return {
		kloom: 'reader-data',
		version: 4,
		reader: isText(d.reader) ? d.reader : '',
		exported: isTime(d.exported) ? d.exported : new Date(0).toISOString(),
		places,
		bookmarks,
		notes,
		kept,
		readings,
		seen
	};
}

const isId = (v: unknown): v is string => isText(v) && RECORD_ID.test(v);
const REVIEWS: Review[] = ['none', 'flagged', 'handled'];

/** A note from an export file, checked; null if it is not one. Anchors came in version 3. */
function noteOf(v: unknown, anchored: boolean): Note | null {
	const r = recordOf(v);
	if (!r) return null;
	const n = v as Record<string, unknown>;
	if (!isText(n.id) || !/^[\w-]{1,64}$/.test(n.id)) return null;
	if (!isText(n.text) || n.text.length > NOTE_MAX) return null;
	if (!REVIEWS.includes(n.review as Review)) return null;
	if (n.response !== null && !isText(n.response)) return null;
	if (!isTime(n.created) || !isTime(n.updated)) return null;
	const anchor = anchored && n.anchor != null ? anchorOf(n.anchor) : null;
	if (anchored && n.anchor != null && !anchor) return null;
	return {
		...r,
		id: n.id,
		text: n.text,
		anchor,
		review: n.review as Review,
		response: n.response as string | null,
		unseen: n.unseen === true,
		created: new Date(n.created).toISOString(),
		updated: new Date(n.updated).toISOString()
	};
}

/**
 * What the page offers the shell for the reader's layer on a frame (korg
 * 3409, 3390): this subject's notes and kept-answer counts, and the calls
 * that change them. Absent when there is no reader to keep them for.
 */
export interface ReaderLayer {
	/** This subject's notes, oldest first. */
	notes: Note[];
	/**
	 * What ticking "Agent review" does, said beside the box; the page says
	 * who reads a flagged note (korg 3502). A plain default when absent.
	 */
	reviewSays?: string;
	/** Kept answers per frame id, in this subject. */
	kept: Record<string, number>;
	/** Write a note (the page fills in the subject); null when it failed. */
	saveNote(note: Omit<NoteInput, 'subject'>): Promise<Note | null>;
	deleteNote(id: string): Promise<boolean>;
	/** The reader has seen these notes' agent answers (§My notes). */
	seen(ids: string[]): void;
	/** The kept answers on a frame, fetched when the Q&A section opens; null when that failed. */
	keptOn(frame: string): Promise<Kept[] | null>;
	forget(frame: string, id: string): Promise<boolean>;
	/** An answer was just kept on this frame. */
	onkept(frame: string): void;
}

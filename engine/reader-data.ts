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
 * are async for that reason, though SQLite answers at once. Notes,
 * annotations and kept answers arrive as their own methods and tables on the
 * same interface, each keyed the same way.
 */

/** Where a reader last was in a subject. */
export interface Place {
	subject: string;
	frame: string;
	/** The frame's title when it was visited, for a list that spans subjects. */
	label: string;
	/** ISO 8601, UTC. */
	at: string;
}

/** A frame a reader marked to come back to. */
export interface Bookmark {
	subject: string;
	frame: string;
	label: string;
	at: string;
}

export interface ReaderStore {
	/** Record that `reader` is on this frame now: their place in its subject. */
	visit(reader: string, place: Omit<Place, 'at'>): Promise<void>;
	/** Their place in `subject`, or, with no subject, the last place anywhere. */
	lastVisited(reader: string, subject?: string): Promise<Place | null>;
	/** Every bookmark of theirs, across subjects, newest first. */
	bookmarks(reader: string): Promise<Bookmark[]>;
	/** Mark a frame; marking it again only refreshes its label. */
	bookmark(reader: string, mark: Omit<Bookmark, 'at'>): Promise<void>;
	unbookmark(reader: string, subject: string, frame: string): Promise<void>;
	/** Everything the store holds for `reader`, to back up or carry elsewhere. */
	exportData(reader: string): Promise<ReaderExport>;
	/** Merge an export in as `reader`'s; the newer of two records wins. */
	importData(reader: string, data: ReaderExport): Promise<{ places: number; bookmarks: number }>;
}

/** The export format: versioned, so an older file can still be read. */
export interface ReaderExport {
	kloom: 'reader-data';
	version: 1;
	/** Who it was exported for; an import files it under whoever imports it. */
	reader: string;
	exported: string;
	places: Place[];
	bookmarks: Bookmark[];
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
	if (d.version !== 1) return { error: `unknown version ${String(d.version)}` };
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
	return {
		kloom: 'reader-data',
		version: 1,
		reader: isText(d.reader) ? d.reader : '',
		exported: isTime(d.exported) ? d.exported : new Date(0).toISOString(),
		places,
		bookmarks
	};
}

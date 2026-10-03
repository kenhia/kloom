import { randomUUID } from 'node:crypto';
import { mkdirSync } from 'node:fs';
import { dirname } from 'node:path';
import { DatabaseSync } from 'node:sqlite';
import type {
	Bookmark,
	Kept,
	Note,
	Place,
	ReaderExport,
	Reading,
	ReaderStore,
	ReviewNote,
	ReviewSuggestion,
	SeenFrame,
	Suggestion
} from '$engine/reader-data';
import type { KeptAnswer } from '$engine/ai/kept';

/**
 * The reader-data store's SQLite adapter (docs/design.md §Reader data): one
 * file, `<dataDir>/reader.db`, on Node's built-in `node:sqlite`, so the store
 * adds no dependency and nothing to compile.
 *
 * This file imports nothing but `node:` modules and types, so plain Node
 * (which strips the types) can load it as well as the app. The review-notes
 * skill's script does that, and so reaches the store through this adapter
 * rather than around it.
 *
 * The schema moves forward by the list below. `PRAGMA user_version` says how
 * many entries a file has had, and opening one runs the rest, each in a
 * transaction. An entry is never edited once shipped; a change is a new one.
 */
const MIGRATIONS = [
	`CREATE TABLE place (
		reader TEXT NOT NULL,
		subject TEXT NOT NULL,
		frame TEXT NOT NULL,
		label TEXT NOT NULL,
		at TEXT NOT NULL,
		PRIMARY KEY (reader, subject)
	);
	CREATE INDEX place_recent ON place (reader, at);
	CREATE TABLE bookmark (
		reader TEXT NOT NULL,
		subject TEXT NOT NULL,
		frame TEXT NOT NULL,
		label TEXT NOT NULL,
		at TEXT NOT NULL,
		PRIMARY KEY (reader, subject, frame)
	);`,
	// Sprint 011: notes (korg 3409) and kept answers (3390).
	`CREATE TABLE note (
		reader TEXT NOT NULL,
		id TEXT NOT NULL,
		subject TEXT NOT NULL,
		frame TEXT NOT NULL,
		label TEXT NOT NULL,
		text TEXT NOT NULL,
		review TEXT NOT NULL DEFAULT 'none' CHECK (review IN ('none', 'flagged', 'handled')),
		response TEXT,
		created TEXT NOT NULL,
		updated TEXT NOT NULL,
		PRIMARY KEY (reader, id)
	);
	CREATE INDEX note_frame ON note (reader, subject, frame);
	CREATE INDEX note_review ON note (review, created);
	CREATE TABLE kept (
		reader TEXT NOT NULL,
		subject TEXT NOT NULL,
		id TEXT NOT NULL,
		frame TEXT NOT NULL,
		answer TEXT NOT NULL,
		grown TEXT,
		kept_at TEXT NOT NULL,
		PRIMARY KEY (reader, id)
	);
	CREATE INDEX kept_frame ON kept (reader, subject, frame);`,
	// Sprint 012: annotations (korg 3415), notes with an anchor (JSON).
	`ALTER TABLE note ADD COLUMN anchor TEXT;`,
	// Sprint 034: whether an agent's answer waits to be seen (korg 3481).
	// Answers given before it are counted as waiting: nothing said they were seen.
	`ALTER TABLE note ADD COLUMN unseen INTEGER NOT NULL DEFAULT 0;
	UPDATE note SET unseen = 1 WHERE review = 'handled';`,
	// Sprint 039: the reader edition's sign-in (korg 3501), in accounts.ts.
	// An account is a login, not a person; session ids and invite tokens are
	// stored as their sha256, never as themselves.
	`CREATE TABLE account (
		username TEXT PRIMARY KEY,
		display_name TEXT NOT NULL,
		password TEXT,
		disabled INTEGER NOT NULL DEFAULT 0,
		created TEXT NOT NULL,
		last_seen TEXT
	);
	CREATE TABLE session (
		id TEXT PRIMARY KEY,
		username TEXT NOT NULL,
		created TEXT NOT NULL,
		seen TEXT NOT NULL,
		expires TEXT NOT NULL
	);
	CREATE INDEX session_account ON session (username);
	CREATE TABLE invite (
		token TEXT PRIMARY KEY,
		username TEXT NOT NULL,
		created TEXT NOT NULL,
		expires TEXT NOT NULL,
		used TEXT
	);
	CREATE INDEX invite_account ON invite (username);`,
	// Sprint 041: subjects readers suggest (korg 3459). `name` is the
	// reader's display name when they suggested it, so the credit survives
	// a rename; the status is only ever changed from the review side.
	`CREATE TABLE suggestion (
		reader TEXT NOT NULL,
		id TEXT NOT NULL,
		name TEXT NOT NULL,
		title TEXT NOT NULL,
		cover TEXT NOT NULL,
		why TEXT NOT NULL,
		status TEXT NOT NULL DEFAULT 'new' CHECK (status IN ('new', 'planned', 'written', 'declined')),
		created TEXT NOT NULL,
		updated TEXT NOT NULL,
		PRIMARY KEY (reader, id)
	);
	CREATE INDEX suggestion_status ON suggestion (status, created);`,
	// Sprint 043: what's new to a reader (korg 3525). Each subject's first
	// visit and the watermark "I'm caught up" sets, the frames they have
	// opened or marked seen, and when they were last active, for "since my
	// last visit". Readers from before it are taken to have started a subject
	// with their earliest record in it, and to have opened every frame they
	// placed, bookmarked, wrote on or kept an answer on.
	`CREATE TABLE reading (
		reader TEXT NOT NULL,
		subject TEXT NOT NULL,
		first TEXT NOT NULL,
		caught_up TEXT,
		PRIMARY KEY (reader, subject)
	);
	CREATE TABLE seen (
		reader TEXT NOT NULL,
		subject TEXT NOT NULL,
		frame TEXT NOT NULL,
		at TEXT NOT NULL,
		PRIMARY KEY (reader, subject, frame)
	);
	CREATE TABLE activity (
		reader TEXT PRIMARY KEY,
		active TEXT NOT NULL,
		previous TEXT
	);
	INSERT INTO reading (reader, subject, first)
		SELECT reader, subject, min(at) FROM (
			SELECT reader, subject, at FROM place
			UNION ALL SELECT reader, subject, at FROM bookmark
			UNION ALL SELECT reader, subject, created FROM note
			UNION ALL SELECT reader, subject, kept_at FROM kept
		) GROUP BY reader, subject;
	INSERT INTO seen (reader, subject, frame, at)
		SELECT reader, subject, frame, min(at) FROM (
			SELECT reader, subject, frame, at FROM place
			UNION ALL SELECT reader, subject, frame, at FROM bookmark
			UNION ALL SELECT reader, subject, frame, created FROM note
			UNION ALL SELECT reader, subject, frame, kept_at FROM kept
		) GROUP BY reader, subject, frame;
	INSERT INTO activity (reader, active) SELECT reader, max(at) FROM place GROUP BY reader;`
];

/**
 * A pause this long between moves ends a visit (korg 3525): "since my last
 * visit" counts from the end of the one before.
 */
export const VISIT_GAP_MS = 2 * 60 * 60 * 1000;

export const SCHEMA_VERSION = MIGRATIONS.length;

/** Bring a database up to the current schema. */
function migrate(db: DatabaseSync) {
	const { user_version: at } = db.prepare('PRAGMA user_version').get() as { user_version: number };
	if (at > MIGRATIONS.length)
		throw new Error(`reader.db is at schema ${at}, newer than this app's ${MIGRATIONS.length}`);
	for (let v = at; v < MIGRATIONS.length; v++) {
		db.exec('BEGIN');
		try {
			db.exec(MIGRATIONS[v]);
			db.exec(`PRAGMA user_version = ${v + 1}`);
			db.exec('COMMIT');
		} catch (e) {
			db.exec('ROLLBACK');
			throw e;
		}
	}
}

export interface SqliteReaderStore extends ReaderStore {
	close(): void;
}

/**
 * Open (creating and migrating) the database at `path`; `:memory:` for a
 * throwaway one. The store and the accounts (accounts.ts) share it.
 */
export function openReaderDb(path: string): DatabaseSync {
	if (path !== ':memory:') mkdirSync(dirname(path), { recursive: true });
	const db = new DatabaseSync(path);
	db.exec('PRAGMA journal_mode = WAL; PRAGMA busy_timeout = 2000;');
	migrate(db);
	return db;
}

/** Open a store at `path` (see `openReaderDb`), or on a database already open. */
export function openReaderStore(
	at: string | DatabaseSync,
	now: () => Date = () => new Date()
): SqliteReaderStore {
	const db = typeof at === 'string' ? openReaderDb(at) : at;

	// Newer wins, so a visit or an import never moves someone back in time.
	const putPlace = db.prepare(
		`INSERT INTO place (reader, subject, frame, label, at) VALUES (?, ?, ?, ?, ?)
		 ON CONFLICT (reader, subject) DO UPDATE
		 SET frame = excluded.frame, label = excluded.label, at = excluded.at
		 WHERE excluded.at >= place.at`
	);
	const putBookmark = db.prepare(
		`INSERT INTO bookmark (reader, subject, frame, label, at) VALUES (?, ?, ?, ?, ?)
		 ON CONFLICT (reader, subject, frame) DO UPDATE SET label = excluded.label
		 WHERE excluded.at >= bookmark.at`
	);
	const cols = 'subject, frame, label, at';
	const placeIn = db.prepare(`SELECT ${cols} FROM place WHERE reader = ? AND subject = ?`);
	const lastPlace = db.prepare(
		`SELECT ${cols} FROM place WHERE reader = ? ORDER BY at DESC LIMIT 1`
	);
	const places = db.prepare(`SELECT ${cols} FROM place WHERE reader = ? ORDER BY at DESC`);
	const marks = db.prepare(`SELECT ${cols} FROM bookmark WHERE reader = ? ORDER BY at DESC`);
	const dropMark = db.prepare(
		'DELETE FROM bookmark WHERE reader = ? AND subject = ? AND frame = ?'
	);

	// Notes. An edit keeps its frame and creation date. The "Agent review" box
	// flags a note (again) when ticked; unticked, a flagged note is unflagged
	// and a handled one stays handled.
	const noteCols =
		'id, subject, frame, label, text, anchor, review, response, unseen, created, updated';
	const notesIn = db.prepare(
		`SELECT ${noteCols} FROM note WHERE reader = ? AND subject = ? ORDER BY created, id`
	);
	const allNotes = db.prepare(`SELECT ${noteCols} FROM note WHERE reader = ? ORDER BY created, id`);
	const newestNotes = db.prepare(
		`SELECT ${noteCols} FROM note WHERE reader = ? ORDER BY updated DESC, id`
	);
	const noteById = db.prepare(`SELECT ${noteCols} FROM note WHERE reader = ? AND id = ?`);
	const addNote = db.prepare(
		`INSERT INTO note (reader, id, subject, frame, label, text, anchor, review, created, updated)
		 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`
	);
	const editNote = db.prepare(
		`UPDATE note SET label = ?, text = ?, updated = ?,
		 review = CASE WHEN ? THEN 'flagged' WHEN review = 'handled' THEN 'handled' ELSE 'none' END,
		 response = CASE WHEN ? THEN NULL ELSE response END,
		 unseen = CASE WHEN ? THEN 0 ELSE unseen END
		 WHERE reader = ? AND id = ?`
	);
	// The same box, from My notes: the flag alone, the text as it is.
	const setFlag = db.prepare(
		`UPDATE note SET
		 review = CASE WHEN ? THEN 'flagged' WHEN review = 'handled' THEN 'handled' ELSE 'none' END,
		 response = CASE WHEN ? THEN NULL ELSE response END,
		 unseen = CASE WHEN ? THEN 0 ELSE unseen END
		 WHERE reader = ? AND id = ?`
	);
	const unseenCount = db.prepare('SELECT count(*) AS n FROM note WHERE reader = ? AND unseen = 1');
	const seeNote = db.prepare(
		'UPDATE note SET unseen = 0 WHERE reader = ? AND id = ? AND unseen = 1'
	);
	const dropNote = db.prepare('DELETE FROM note WHERE reader = ? AND id = ?');
	const flagged = db.prepare(
		`SELECT reader, ${noteCols} FROM note WHERE review = 'flagged' ORDER BY created, id`
	);
	const flaggedBy = db.prepare(
		`SELECT reader, ${noteCols} FROM note WHERE review = 'flagged' AND reader = ? ORDER BY created, id`
	);
	// Given the `updated` the agent read, an edit since then refuses it.
	const handle = db.prepare(
		`UPDATE note SET review = 'handled', response = ?, unseen = 1
		 WHERE reader = ? AND id = ? AND review = 'flagged' AND (? IS NULL OR updated = ?)`
	);
	const everyNote = db.prepare(`SELECT reader, ${noteCols} FROM note ORDER BY created, id`);

	// Suggestions (korg 3459).
	const suggestionCols = 'id, title, cover, why, status, created, updated';
	const addSuggestion = db.prepare(
		`INSERT INTO suggestion (reader, id, name, title, cover, why, created, updated)
		 VALUES (?, ?, ?, ?, ?, ?, ?, ?)`
	);
	const suggestionById = db.prepare(
		`SELECT ${suggestionCols} FROM suggestion WHERE reader = ? AND id = ?`
	);
	const suggestionsOf = db.prepare(
		`SELECT ${suggestionCols} FROM suggestion WHERE reader = ? ORDER BY created DESC, id`
	);
	const allSuggestions = db.prepare(
		`SELECT reader, name, ${suggestionCols} FROM suggestion ORDER BY created, id`
	);
	const suggestionsIn = db.prepare(
		`SELECT reader, name, ${suggestionCols} FROM suggestion WHERE status = ? ORDER BY created, id`
	);
	const markSuggestion = db.prepare(
		'UPDATE suggestion SET status = ?, updated = ? WHERE reader = ? AND id = ?'
	);
	const importNote = db.prepare(
		`INSERT INTO note (reader, id, subject, frame, label, text, anchor, review, response, unseen, created, updated)
		 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
		 ON CONFLICT (reader, id) DO UPDATE SET label = excluded.label, text = excluded.text,
		 review = excluded.review, response = excluded.response, unseen = excluded.unseen,
		 updated = excluded.updated
		 WHERE excluded.updated > note.updated`
	);

	// Kept answers, stored whole in their own format, which grow reads.
	const putKept = db.prepare(
		`INSERT INTO kept (reader, subject, id, frame, answer, grown, kept_at) VALUES (?, ?, ?, ?, ?, ?, ?)
		 ON CONFLICT (reader, id) DO UPDATE SET grown = coalesce(kept.grown, excluded.grown)`
	);
	const keptCount = db.prepare(
		'SELECT frame, count(*) AS n FROM kept WHERE reader = ? AND subject = ? GROUP BY frame'
	);
	const keptOnFrame = db.prepare(
		'SELECT answer, grown FROM kept WHERE reader = ? AND subject = ? AND frame = ? ORDER BY kept_at, id'
	);
	const keptById = db.prepare(
		'SELECT answer FROM kept WHERE reader = ? AND subject = ? AND id = ?'
	);
	const allKept = db.prepare(
		'SELECT answer, grown FROM kept WHERE reader = ? ORDER BY kept_at, id'
	);
	const setGrown = db.prepare(
		'UPDATE kept SET grown = ? WHERE reader = ? AND subject = ? AND id = ?'
	);
	const dropKept = db.prepare('DELETE FROM kept WHERE reader = ? AND subject = ? AND id = ?');

	// What's new (korg 3525): first visits, watermarks, what was opened, and activity.
	const startReading = db.prepare(
		`INSERT INTO reading (reader, subject, first) VALUES (?, ?, ?)
		 ON CONFLICT (reader, subject) DO NOTHING`
	);
	const putReading = db.prepare(
		`INSERT INTO reading (reader, subject, first, caught_up) VALUES (?, ?, ?, ?)
		 ON CONFLICT (reader, subject) DO UPDATE
		 SET first = min(reading.first, excluded.first),
		 caught_up = CASE
			WHEN excluded.caught_up IS NULL THEN reading.caught_up
			WHEN reading.caught_up IS NULL THEN excluded.caught_up
			ELSE max(reading.caught_up, excluded.caught_up) END`
	);
	const readingOf = db.prepare(
		'SELECT first, caught_up AS caughtUp FROM reading WHERE reader = ? AND subject = ?'
	);
	const readingsOf = db.prepare(
		'SELECT subject, first, caught_up AS caughtUp FROM reading WHERE reader = ? ORDER BY subject'
	);
	const catchUp = db.prepare('UPDATE reading SET caught_up = ? WHERE reader = ? AND subject = ?');
	const putSeen = db.prepare(
		`INSERT INTO seen (reader, subject, frame, at) VALUES (?, ?, ?, ?)
		 ON CONFLICT (reader, subject, frame) DO UPDATE SET at = min(seen.at, excluded.at)`
	);
	const seenOf = db.prepare(
		'SELECT subject, frame, at FROM seen WHERE reader = ? ORDER BY subject, frame'
	);
	const activityOf = db.prepare('SELECT active, previous FROM activity WHERE reader = ?');
	const putActivity = db.prepare(
		`INSERT INTO activity (reader, active, previous) VALUES (?, ?, ?)
		 ON CONFLICT (reader) DO UPDATE SET active = excluded.active, previous = excluded.previous`
	);
	/** A move at `at`: a gap long enough since the last one starts a new visit. */
	const touch = (reader: string, at: string) => {
		const a = activityOf.get(reader) as { active: string; previous: string | null } | undefined;
		if (a && Date.parse(at) < Date.parse(a.active)) return;
		const ended = a && Date.parse(at) - Date.parse(a.active) > VISIT_GAP_MS;
		putActivity.run(reader, at, ended ? a.active : (a?.previous ?? null));
	};

	const stamp = () => now().toISOString();
	const row = <T>(r: unknown) => (r ? ({ ...(r as object) } as T) : null);
	/** A note row: its anchor is stored as JSON, and unseen as 0 or 1. */
	const note = <T extends Note>(r: unknown): T | null => {
		const n = row<Omit<T, 'anchor' | 'unseen'> & { anchor: string | null; unseen: number }>(r);
		return n && ({ ...n, anchor: n.anchor ? JSON.parse(n.anchor) : null, unseen: !!n.unseen } as T);
	};
	const anchorText = (a: Note['anchor'] | undefined) => (a ? JSON.stringify(a) : null);
	const kept = (r: unknown): Kept => {
		const { answer, grown } = r as { answer: string; grown: string | null };
		return { answer: JSON.parse(answer), grown: grown ? JSON.parse(grown) : null };
	};
	const storeKept = (reader: string, a: KeptAnswer, grown: string[] | null) =>
		putKept.run(
			reader,
			a.subject,
			a.id,
			a.anchor.frame,
			JSON.stringify(a),
			grown ? JSON.stringify(grown) : null,
			a.keptAt
		);
	const inTransaction = <T>(work: () => T): T => {
		db.exec('BEGIN');
		try {
			const out = work();
			db.exec('COMMIT');
			return out;
		} catch (e) {
			db.exec('ROLLBACK');
			throw e;
		}
	};

	// Everything one reader has, for `deleteReader`.
	const dropAll = {
		place: db.prepare('DELETE FROM place WHERE reader = ?'),
		bookmark: db.prepare('DELETE FROM bookmark WHERE reader = ?'),
		note: db.prepare('DELETE FROM note WHERE reader = ?'),
		kept: db.prepare('DELETE FROM kept WHERE reader = ?'),
		suggestion: db.prepare('DELETE FROM suggestion WHERE reader = ?'),
		reading: db.prepare('DELETE FROM reading WHERE reader = ?'),
		seen: db.prepare('DELETE FROM seen WHERE reader = ?'),
		activity: db.prepare('DELETE FROM activity WHERE reader = ?')
	};

	return {
		async visit(reader, p) {
			const at = stamp();
			inTransaction(() => {
				putPlace.run(reader, p.subject, p.frame, p.label, at);
				// Being on a frame opens it, and the first visit to a subject starts it.
				startReading.run(reader, p.subject, at);
				putSeen.run(reader, p.subject, p.frame, at);
				touch(reader, at);
			});
		},
		async readings(reader) {
			const out: Record<string, Reading> = {};
			for (const r of readingsOf.all(reader) as unknown as ({ subject: string } & Reading)[])
				out[r.subject] = { first: r.first, caughtUp: r.caughtUp };
			return out;
		},
		async seenFrames(reader) {
			const out: Record<string, string[]> = {};
			for (const r of seenOf.all(reader) as { subject: string; frame: string }[])
				(out[r.subject] ??= []).push(r.frame);
			return out;
		},
		async markSeen(reader, subject, frames) {
			const at = stamp();
			inTransaction(() => {
				for (const f of frames) putSeen.run(reader, subject, f, at);
			});
		},
		async catchUp(reader, subject) {
			const at = stamp();
			return inTransaction(() => {
				startReading.run(reader, subject, at);
				catchUp.run(at, reader, subject);
				const r = readingOf.get(reader, subject) as unknown as Reading;
				return { first: r.first, caughtUp: r.caughtUp };
			});
		},
		async lastVisit(reader) {
			const a = activityOf.get(reader) as { active: string; previous: string | null } | undefined;
			if (!a) return null;
			// Away long enough, the visit that ended is the last one; otherwise this one goes on.
			return now().getTime() - Date.parse(a.active) > VISIT_GAP_MS ? a.active : a.previous;
		},
		async lastVisited(reader, subject) {
			return row<Place>(subject ? placeIn.get(reader, subject) : lastPlace.get(reader));
		},
		async bookmarks(reader) {
			return marks.all(reader).map((r) => row<Bookmark>(r)!);
		},
		async bookmark(reader, b) {
			putBookmark.run(reader, b.subject, b.frame, b.label, stamp());
		},
		async unbookmark(reader, subject, frame) {
			dropMark.run(reader, subject, frame);
		},

		async notes(reader, subject) {
			return notesIn.all(reader, subject).map((r) => note<Note>(r)!);
		},
		async saveNote(reader, n) {
			const at = stamp();
			if (n.id === undefined) {
				const id = randomUUID();
				const review = n.flag ? 'flagged' : 'none';
				const anchor = anchorText(n.anchor);
				addNote.run(reader, id, n.subject, n.frame, n.label, n.text, anchor, review, at, at);
				return note<Note>(noteById.get(reader, id));
			}
			const flag = n.flag ? 1 : 0;
			const { changes } = editNote.run(n.label, n.text, at, flag, flag, flag, reader, n.id);
			return changes ? note<Note>(noteById.get(reader, n.id)) : null;
		},
		async deleteNote(reader, id) {
			return dropNote.run(reader, id).changes > 0;
		},
		async allNotes(reader) {
			return newestNotes.all(reader).map((r) => note<Note>(r)!);
		},
		async flagNote(reader, id, flag) {
			const f = flag ? 1 : 0;
			const { changes } = setFlag.run(f, f, f, reader, id);
			return changes ? note<Note>(noteById.get(reader, id)) : null;
		},
		async deleteNotes(reader, ids) {
			return inTransaction(() =>
				ids.reduce((n, id) => n + Number(dropNote.run(reader, id).changes), 0)
			);
		},
		async unseenAnswers(reader) {
			return (unseenCount.get(reader) as { n: number }).n;
		},
		async seeNotes(reader, ids) {
			return inTransaction(() =>
				ids.reduce((n, id) => n + Number(seeNote.run(reader, id).changes), 0)
			);
		},
		async flaggedNotes(reader) {
			return (reader ? flaggedBy.all(reader) : flagged.all()).map((r) => note<ReviewNote>(r)!);
		},
		async handleNote(reader, id, response, seen) {
			const at = seen ?? null;
			return handle.run(response, reader, id, at, at).changes > 0;
		},
		async everyNote() {
			return everyNote.all().map((r) => note<ReviewNote>(r)!);
		},

		async suggest(reader, name, s) {
			const id = randomUUID();
			const at = stamp();
			addSuggestion.run(reader, id, name, s.title, s.cover, s.why, at, at);
			return row<Suggestion>(suggestionById.get(reader, id))!;
		},
		async suggestions(reader) {
			return suggestionsOf.all(reader).map((r) => row<Suggestion>(r)!);
		},
		async allSuggestions(status) {
			return (status ? suggestionsIn.all(status) : allSuggestions.all()).map((r) =>
				row<ReviewSuggestion>(r)!
			);
		},
		async markSuggestion(reader, id, status) {
			return markSuggestion.run(status, stamp(), reader, id).changes > 0;
		},

		async keep(reader, answer) {
			storeKept(reader, answer, null);
		},
		async keptCounts(reader, subject) {
			const counts: Record<string, number> = {};
			for (const r of keptCount.all(reader, subject) as { frame: string; n: number }[])
				counts[r.frame] = r.n;
			return counts;
		},
		async keptOn(reader, subject, frame) {
			return keptOnFrame.all(reader, subject, frame).map(kept);
		},
		async kept(reader, subject, id) {
			const r = keptById.get(reader, subject, id) as { answer: string } | undefined;
			return r ? JSON.parse(r.answer) : null;
		},
		async grew(reader, subject, id, frames) {
			setGrown.run(JSON.stringify(frames), reader, subject, id);
		},
		async forget(reader, subject, id) {
			return dropKept.run(reader, subject, id).changes > 0;
		},

		async exportData(reader): Promise<ReaderExport> {
			return {
				kloom: 'reader-data',
				version: 4,
				reader,
				exported: stamp(),
				places: places.all(reader).map((r) => row<Place>(r)!),
				bookmarks: marks.all(reader).map((r) => row<Bookmark>(r)!),
				notes: allNotes.all(reader).map((r) => note<Note>(r)!),
				kept: allKept.all(reader).map(kept),
				readings: (readingsOf.all(reader) as unknown as ({ subject: string } & Reading)[]).map(
					(r) => ({ subject: r.subject, first: r.first, caughtUp: r.caughtUp })
				),
				seen: seenOf.all(reader).map((r) => row<SeenFrame>(r)!)
			};
		},
		async importData(reader, data) {
			inTransaction(() => {
				for (const p of data.places) putPlace.run(reader, p.subject, p.frame, p.label, p.at);
				for (const b of data.bookmarks) putBookmark.run(reader, b.subject, b.frame, b.label, b.at);
				for (const n of data.notes)
					importNote.run(
						reader,
						n.id,
						n.subject,
						n.frame,
						n.label,
						n.text,
						anchorText(n.anchor),
						n.review,
						n.response,
						n.unseen ? 1 : 0,
						n.created,
						n.updated
					);
				for (const k of data.kept) storeKept(reader, k.answer, k.grown);
				// The earlier first visit and the later watermark win; seen only grows.
				for (const r of data.readings) putReading.run(reader, r.subject, r.first, r.caughtUp);
				for (const f of data.seen) putSeen.run(reader, f.subject, f.frame, f.at);
			});
			return {
				places: data.places.length,
				bookmarks: data.bookmarks.length,
				notes: data.notes.length,
				kept: data.kept.length,
				readings: data.readings.length,
				seen: data.seen.length
			};
		},
		async deleteReader(reader) {
			const n = {
				places: 0,
				bookmarks: 0,
				notes: 0,
				kept: 0,
				readings: 0,
				seen: 0,
				suggestions: 0
			};
			inTransaction(() => {
				n.places = Number(dropAll.place.run(reader).changes);
				n.bookmarks = Number(dropAll.bookmark.run(reader).changes);
				n.notes = Number(dropAll.note.run(reader).changes);
				n.kept = Number(dropAll.kept.run(reader).changes);
				n.readings = Number(dropAll.reading.run(reader).changes);
				n.seen = Number(dropAll.seen.run(reader).changes);
				dropAll.activity.run(reader);
				n.suggestions = Number(dropAll.suggestion.run(reader).changes);
			});
			return n;
		},
		close: () => db.close()
	};
}

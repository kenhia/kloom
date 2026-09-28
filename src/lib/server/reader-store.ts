import { mkdirSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { DatabaseSync } from 'node:sqlite';
import type { Bookmark, Place, ReaderExport, ReaderStore } from '$engine/reader-data';
import { dataDir } from './config';

/**
 * The reader-data store's SQLite adapter (docs/design.md §Reader data): one
 * file, `<dataDir>/reader.db`, on Node's built-in `node:sqlite`, so the store
 * adds no dependency and nothing to compile.
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
	);`
];

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

/** Open (creating and migrating) a store at `path`; `:memory:` for a throwaway one. */
export function openReaderStore(
	path: string,
	now: () => Date = () => new Date()
): SqliteReaderStore {
	if (path !== ':memory:') mkdirSync(dirname(path), { recursive: true });
	const db = new DatabaseSync(path);
	db.exec('PRAGMA journal_mode = WAL; PRAGMA busy_timeout = 2000;');
	migrate(db);

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

	const stamp = () => now().toISOString();
	const row = <T>(r: unknown) => (r ? ({ ...(r as object) } as T) : null);

	return {
		async visit(reader, p) {
			putPlace.run(reader, p.subject, p.frame, p.label, stamp());
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
		async exportData(reader): Promise<ReaderExport> {
			return {
				kloom: 'reader-data',
				version: 1,
				reader,
				exported: stamp(),
				places: places.all(reader).map((r) => row<Place>(r)!),
				bookmarks: marks.all(reader).map((r) => row<Bookmark>(r)!)
			};
		},
		async importData(reader, data) {
			db.exec('BEGIN');
			try {
				for (const p of data.places) putPlace.run(reader, p.subject, p.frame, p.label, p.at);
				for (const b of data.bookmarks) putBookmark.run(reader, b.subject, b.frame, b.label, b.at);
				db.exec('COMMIT');
			} catch (e) {
				db.exec('ROLLBACK');
				throw e;
			}
			return { places: data.places.length, bookmarks: data.bookmarks.length };
		},
		close: () => db.close()
	};
}

let shared: ReaderStore | null = null;

/** The app's store, opened on first use at `<dataDir>/reader.db`. */
export function readerStore(): ReaderStore {
	shared ??= openReaderStore(join(dataDir(), 'reader.db'));
	return shared;
}

/** Put another store in its place: tests use a throwaway one. */
export function useReaderStore(store: ReaderStore) {
	shared = store;
}

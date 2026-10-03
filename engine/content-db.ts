import { createHash, randomBytes } from 'node:crypto';
import {
	copyFileSync,
	existsSync,
	mkdirSync,
	readdirSync,
	renameSync,
	rmSync,
	statSync
} from 'node:fs';
import { dirname, join, relative } from 'node:path';
import { DatabaseSync } from 'node:sqlite';
import { buildGraph, linksByFrame, type Graph, type GraphSubject } from './graph';
import { buildSubject, loadNames, readGraphSubject, readSubject, SubjectError } from './load';
import { mapDataOf } from './map';
import type { Subject, SubjectHead } from './model';
import type { Name } from './names';
import { bodyOf, subjectHeadOf, type FrameSource } from './served';
import { startLook, type StartLook } from './start';
import { libraryStats, plainText, subjectStats, type SubjectStats } from './stats';
import type { RawSubject } from './validate';

/**
 * The compiled library (docs/design.md §Serving, korg 3460): the subjects'
 * files stay the source, and `content.db` is what the app serves from. One
 * SQLite file holds each subject's head, every frame's body, the names, the
 * graph's derived links, the map's data, the library's counts and a
 * full-text index; media stay files beside it, named by path.
 *
 * The compiler validates every subject it builds, so an invalid subject never
 * compiles. It builds into a temporary file and renames it over the old one,
 * so a reader never sees a half-built library. It is incremental: a subject
 * whose files are unchanged since the last build keeps its rows, and only
 * what spans subjects (names, links, map, counts) is derived again.
 *
 * Node only (`node:sqlite`, the binding the reader store uses).
 */

/** The file's layout. A build by another version starts afresh. */
export const CONTENT_SCHEMA = 1;

const SCHEMA = `
	CREATE TABLE meta (key TEXT PRIMARY KEY, value TEXT NOT NULL);
	CREATE TABLE subject (
		id TEXT PRIMARY KEY,
		title TEXT NOT NULL,
		subtitle TEXT,
		digest TEXT NOT NULL,
		head TEXT NOT NULL,
		start TEXT NOT NULL,
		stats TEXT NOT NULL,
		graph TEXT NOT NULL
	);
	CREATE TABLE frame (
		subject TEXT NOT NULL,
		id TEXT NOT NULL,
		body TEXT NOT NULL,
		reading TEXT NOT NULL,
		PRIMARY KEY (subject, id)
	);
	CREATE TABLE media (
		subject TEXT NOT NULL,
		frame TEXT NOT NULL,
		file TEXT NOT NULL,
		PRIMARY KEY (subject, frame, file)
	);
	CREATE TABLE name (id TEXT PRIMARY KEY, body TEXT NOT NULL);
	CREATE TABLE mention (
		name TEXT NOT NULL,
		subject TEXT NOT NULL,
		frame TEXT NOT NULL,
		PRIMARY KEY (name, subject, frame)
	);
	CREATE TABLE connection (
		subject TEXT NOT NULL,
		frame TEXT NOT NULL,
		target TEXT NOT NULL,
		why TEXT NOT NULL
	);
	CREATE INDEX connection_target ON connection (target);
	CREATE TABLE frame_links (
		subject TEXT NOT NULL,
		frame TEXT NOT NULL,
		links TEXT NOT NULL,
		PRIMARY KEY (subject, frame)
	);
	CREATE TABLE library (key TEXT PRIMARY KEY, value TEXT NOT NULL);
	CREATE VIRTUAL TABLE frame_text USING fts5 (
		subject UNINDEXED, frame UNINDEXED, topic, text, tokenize = 'porter unicode61'
	);
`;

/** What a subject id may look like: a plain directory name, never a path. */
export const SUBJECT_ID = /^[a-z0-9][a-z0-9-]*$/;

/** The subjects under `dir`: each directory with a `subject.json`, in id order. */
export function subjectIds(dir: string): string[] {
	let entries;
	try {
		entries = readdirSync(dir, { withFileTypes: true });
	} catch {
		return [];
	}
	return entries
		.filter(
			(e) =>
				e.isDirectory() && SUBJECT_ID.test(e.name) && existsSync(join(dir, e.name, 'subject.json'))
		)
		.map((e) => e.name)
		.sort();
}

/**
 * A directory's state, cheaply: every file's path, size and modified time,
 * hidden entries left out (grow stages a frame as `.grow-<id>`). A file
 * written, added, removed or renamed changes it.
 */
export function treeDigest(dir: string): string {
	const hash = createHash('sha256');
	const walk = (at: string, rel: string) => {
		let entries;
		try {
			entries = readdirSync(at, { withFileTypes: true });
		} catch {
			return;
		}
		for (const e of entries.sort((a, b) => (a.name < b.name ? -1 : a.name > b.name ? 1 : 0))) {
			if (e.name.startsWith('.')) continue;
			const path = join(at, e.name);
			if (e.isDirectory()) walk(path, `${rel}${e.name}/`);
			else if (e.isFile()) {
				const s = statSync(path);
				hash.update(`${rel}${e.name}\0${s.size}\0${s.mtimeMs}\n`);
			}
		}
	};
	walk(dir, '');
	return hash.digest('hex');
}

/** Subjects that failed validation in a strict build; each with every problem found. */
export class ContentError extends Error {
	constructor(readonly failed: { id: string; problems: string[] }[]) {
		super(
			failed.map((f) => `subject ${f.id} is invalid:\n  ${f.problems.join('\n  ')}`).join('\n')
		);
		this.name = 'ContentError';
	}
}

export interface CompileOptions {
	subjectsDir: string;
	namesDir: string;
	/** Where the library goes: `content.db`. */
	out: string;
	/**
	 * What compiled it: the app's build. Rows another compiler made are never
	 * reused, so new rendering code rebuilds every subject.
	 */
	compiler?: string;
	/** Fail on any invalid subject (the gate, the build recipe). Otherwise its old rows stay. */
	strict?: boolean;
	/** The content's commit, recorded with the build. */
	source?: string | null;
	/**
	 * Only these subjects (the public site's `publish.json`); a library built
	 * from a list holds nothing else. Every one must be on disk.
	 */
	only?: string[];
}

export interface CompileReport {
	/** False when nothing had changed, and the old file stands. */
	changed: boolean;
	/** Subjects compiled in this build, and those whose rows were kept. */
	built: string[];
	reused: string[];
	/** Subjects no longer on disk, taken out. */
	dropped: string[];
	/** Subjects that failed validation; served as they were last built, if ever. */
	failed: { id: string; problems: string[] }[];
	/** Name files that were invalid and left out. */
	nameProblems: string[];
	/** The build now standing. */
	build: string | null;
	ms: number;
}

interface Previous {
	compiler: string;
	names: string;
	build: string;
	subjects: Map<string, string>;
}

/** What the library at `path` was built from; null when there is none, or it cannot be read. */
function previous(path: string): Previous | null {
	if (!existsSync(path)) return null;
	let db: DatabaseSync | undefined;
	try {
		db = new DatabaseSync(path, { readOnly: true });
		const meta = metaOf(db);
		if (Number(meta.schema) !== CONTENT_SCHEMA) return null;
		const rows = db.prepare('SELECT id, digest FROM subject').all() as {
			id: string;
			digest: string;
		}[];
		return {
			compiler: meta.compiler ?? '',
			names: meta.names ?? '',
			build: meta.build ?? '',
			subjects: new Map(rows.map((r) => [r.id, r.digest]))
		};
	} catch {
		return null;
	} finally {
		db?.close();
	}
}

const metaOf = (db: DatabaseSync): Record<string, string> =>
	Object.fromEntries(
		(db.prepare('SELECT key, value FROM meta').all() as { key: string; value: string }[]).map(
			(r) => [r.key, r.value]
		)
	);

function dropSubject(db: DatabaseSync, id: string) {
	for (const table of ['subject', 'frame', 'media', 'frame_text'])
		db.prepare(`DELETE FROM ${table} WHERE ${table === 'subject' ? 'id' : 'subject'} = ?`).run(id);
}

function insertSubject(
	db: DatabaseSync,
	digest: string,
	subject: Subject,
	raw: RawSubject,
	graph: GraphSubject
) {
	db.prepare(
		'INSERT INTO subject (id, title, subtitle, digest, head, start, stats, graph) VALUES (?, ?, ?, ?, ?, ?, ?, ?)'
	).run(
		subject.id,
		subject.title,
		subject.subtitle ?? null,
		digest,
		JSON.stringify(subjectHeadOf(subject)),
		JSON.stringify(startLook(subject)),
		JSON.stringify(subjectStats(subject.id, raw)),
		JSON.stringify(graph)
	);
	const frame = db.prepare('INSERT INTO frame (subject, id, body, reading) VALUES (?, ?, ?, ?)');
	const media = db.prepare('INSERT INTO media (subject, frame, file) VALUES (?, ?, ?)');
	const text = db.prepare(
		'INSERT INTO frame_text (subject, frame, topic, text) VALUES (?, ?, ?, ?)'
	);
	for (const [id, f] of Object.entries(subject.frames)) {
		frame.run(subject.id, id, JSON.stringify(bodyOf(f)), raw.frames[id].reading ?? '');
		for (const file of raw.frames[id].media) media.run(subject.id, id, file);
		text.run(subject.id, id, f.topic, plainText(f.readingHtml).replace(/\s+/g, ' ').trim());
	}
}

/**
 * Derive what spans subjects from the rows standing: the graph, each frame's
 * links, the mention and connection tables, the map's data and the counts.
 */
function deriveLibrary(db: DatabaseSync, names: Record<string, Name>) {
	const rows = db.prepare('SELECT graph, stats FROM subject ORDER BY id').all() as {
		graph: string;
		stats: string;
	}[];
	const subjects = rows.map((r) => JSON.parse(r.graph) as GraphSubject);
	const graph = buildGraph(subjects, names);

	for (const table of ['name', 'mention', 'connection', 'frame_links', 'library'])
		db.exec(`DELETE FROM ${table}`);
	const name = db.prepare('INSERT INTO name (id, body) VALUES (?, ?)');
	for (const [id, n] of Object.entries(names)) name.run(id, JSON.stringify(n));
	const mention = db.prepare(
		'INSERT OR IGNORE INTO mention (name, subject, frame) VALUES (?, ?, ?)'
	);
	const connection = db.prepare(
		'INSERT INTO connection (subject, frame, target, why) VALUES (?, ?, ?, ?)'
	);
	for (const s of subjects)
		for (const f of s.frames) {
			for (const n of f.names) mention.run(n, s.id, f.frame);
			for (const c of f.connections) connection.run(s.id, f.frame, c.to, c.why);
		}
	const links = db.prepare('INSERT INTO frame_links (subject, frame, links) VALUES (?, ?, ?)');
	for (const [key, l] of linksByFrame(graph)) {
		const at = key.indexOf('/');
		links.run(key.slice(0, at), key.slice(at + 1), JSON.stringify(l));
	}
	const library = db.prepare('INSERT INTO library (key, value) VALUES (?, ?)');
	library.run('map', JSON.stringify(mapDataOf(graph)));
	library.run(
		'stats',
		JSON.stringify(
			libraryStats(
				rows.map((r) => JSON.parse(r.stats) as SubjectStats),
				Object.keys(names).length
			)
		)
	);
}

/**
 * Compile `subjectsDir` and `namesDir` into the library at `out`, reusing
 * what an earlier build by the same compiler already holds. The new file
 * replaces the old one in a single rename.
 */
export async function compileContent(o: CompileOptions): Promise<CompileReport> {
	const started = performance.now();
	let ids = subjectIds(o.subjectsDir);
	if (o.only) {
		const missing = o.only.filter((id) => !ids.includes(id));
		if (missing.length) throw new Error(`not subjects here:${missing.join(', ')}`);
		ids = ids.filter((id) => o.only!.includes(id));
	}
	const digests = new Map(ids.map((id) => [id, treeDigest(join(o.subjectsDir, id))]));
	const namesDigest = treeDigest(o.namesDir);
	const compiler = o.compiler ?? '';

	const before = previous(o.out);
	const reuse = before && before.compiler === compiler ? before : null;
	const changed = ids.filter((id) => reuse?.subjects.get(id) !== digests.get(id));
	const dropped = reuse ? [...reuse.subjects.keys()].filter((id) => !digests.has(id)) : [];
	const report: CompileReport = {
		changed: true,
		built: [],
		reused: ids.filter((id) => !changed.includes(id)),
		dropped,
		failed: [],
		nameProblems: [],
		build: before?.build ?? null,
		ms: 0
	};
	if (reuse && !changed.length && !dropped.length && reuse.names === namesDigest) {
		report.changed = false;
		report.ms = performance.now() - started;
		return report;
	}

	mkdirSync(dirname(o.out), { recursive: true });
	const tmp = `${o.out}.${process.pid}-${randomBytes(4).toString('hex')}.tmp`;
	if (reuse) copyFileSync(o.out, tmp);
	const db = new DatabaseSync(tmp);
	try {
		if (!reuse) db.exec(SCHEMA);
		const { names, problems } = await loadNames(o.namesDir);
		report.nameProblems = problems;
		const registry = new Set(Object.keys(names));

		// One transaction: the file is private to this build until the rename.
		db.exec('BEGIN');
		for (const id of dropped) dropSubject(db, id);
		for (const id of changed) {
			const dir = join(o.subjectsDir, id);
			try {
				const raw = await readSubject(dir);
				const subject = buildSubject(id, raw, { mediaBase: `/media/${id}`, names: registry });
				const graph = await readGraphSubject(dir, id);
				dropSubject(db, id);
				insertSubject(db, digests.get(id)!, subject, raw, graph);
				report.built.push(id);
			} catch (e) {
				if (!(e instanceof SubjectError)) throw e;
				report.failed.push({ id, problems: e.problems });
			}
		}
		if (o.strict && report.failed.length) throw new ContentError(report.failed);

		deriveLibrary(db, names);
		const build = `${new Date().toISOString()} ${randomBytes(3).toString('hex')}`;
		const meta = db.prepare('INSERT OR REPLACE INTO meta (key, value) VALUES (?, ?)');
		meta.run('schema', String(CONTENT_SCHEMA));
		meta.run('compiler', compiler);
		meta.run('names', namesDigest);
		meta.run('build', build);
		meta.run('source', o.source ?? '');
		db.exec('COMMIT');
		db.close();
		renameSync(tmp, o.out);
		report.build = build;
	} catch (e) {
		if (db.isOpen) {
			if (db.isTransaction) db.exec('ROLLBACK');
			db.close();
		}
		rmSync(tmp, { force: true });
		throw e;
	}
	report.ms = performance.now() - started;
	return report;
}

/** A subject the library serves: its id, title and subtitle. */
export interface SubjectEntry {
	id: string;
	title: string;
	subtitle?: string;
}

/** A full-text match: the frame, and the words around it. */
export interface SearchHit {
	subject: string;
	frame: string;
	topic: string;
	snippet: string;
}

/**
 * The library, opened to read. Every read is one indexed query; what is
 * large and served whole (a frame's body, the map, the counts) is handed back
 * as the JSON text it is stored as, ready to send.
 */
export class ContentDb {
	readonly build: string;
	/** The content's commit when it was built; empty when unknown. */
	readonly commit: string;

	private constructor(private readonly db: DatabaseSync) {
		const meta = metaOf(db);
		this.build = meta.build ?? '';
		this.commit = meta.source ?? '';
	}

	/** The library at `path`; null when there is none, or it is another schema's. */
	static open(path: string): ContentDb | null {
		if (!existsSync(path)) return null;
		const db = new DatabaseSync(path, { readOnly: true });
		try {
			if (Number(metaOf(db).schema) === CONTENT_SCHEMA) return new ContentDb(db);
		} catch {
			// Not a library: treated as none.
		}
		db.close();
		return null;
	}

	close() {
		if (this.db.isOpen) this.db.close();
	}

	subjects(): SubjectEntry[] {
		const rows = this.db.prepare('SELECT id, title, subtitle FROM subject ORDER BY id').all() as {
			id: string;
			title: string;
			subtitle: string | null;
		}[];
		return rows.map((r) => ({
			id: r.id,
			title: r.title,
			...(r.subtitle ? { subtitle: r.subtitle } : {})
		}));
	}

	private subjectColumn(id: string, column: 'head' | 'start'): string | null {
		const row = this.db.prepare(`SELECT ${column} AS v FROM subject WHERE id = ?`).get(id) as
			{ v: string } | undefined;
		return row?.v ?? null;
	}

	head(id: string): SubjectHead | null {
		const v = this.subjectColumn(id, 'head');
		return v === null ? null : JSON.parse(v);
	}

	start(id: string): StartLook | null {
		const v = this.subjectColumn(id, 'start');
		return v === null ? null : JSON.parse(v);
	}

	/** A frame's body with its links, as JSON (`ServedBody`); null for an unknown frame. */
	bodyJson(subject: string, frame: string): string | null {
		const row = this.db
			.prepare(
				`SELECT f.body AS body, l.links AS links FROM frame f
				 LEFT JOIN frame_links l ON l.subject = f.subject AND l.frame = f.id
				 WHERE f.subject = ? AND f.id = ?`
			)
			.get(subject, frame) as { body: string; links: string | null } | undefined;
		if (!row) return null;
		// Both are JSON objects: the links go in as one more key, with no parse.
		return `${row.body.slice(0, -1)},"links":${row.links ?? '{"connections":[],"names":{}}'}}`;
	}

	source(subject: string, frame: string): FrameSource | null {
		const row = this.db
			.prepare('SELECT body, reading FROM frame WHERE subject = ? AND id = ?')
			.get(subject, frame) as { body: string; reading: string } | undefined;
		return row ? { reading: row.reading, citations: JSON.parse(row.body).citations } : null;
	}

	/** Whether a frame of a served subject has this media file. */
	hasMedia(subject: string, frame: string, file: string): boolean {
		return !!this.db
			.prepare('SELECT 1 FROM media WHERE subject = ? AND frame = ? AND file = ?')
			.get(subject, frame, file);
	}

	/** One of the library-wide values, as JSON: `map` (MapData), `stats` (LibraryStats). */
	libraryJson(key: 'map' | 'stats'): string {
		const row = this.db.prepare('SELECT value FROM library WHERE key = ?').get(key) as
			{ value: string } | undefined;
		return row?.value ?? 'null';
	}

	/** The graph index, rebuilt from the stored rows: for grow, which names every frame. */
	graph(): Graph {
		const subjects = (
			this.db.prepare('SELECT graph FROM subject ORDER BY id').all() as { graph: string }[]
		).map((r) => JSON.parse(r.graph) as GraphSubject);
		const names = Object.fromEntries(
			(this.db.prepare('SELECT id, body FROM name').all() as { id: string; body: string }[]).map(
				(r) => [r.id, JSON.parse(r.body) as Name]
			)
		);
		return buildGraph(subjects, names);
	}

	/** Frames whose reading or topic match an FTS5 query, best first. */
	search(query: string, limit = 20): SearchHit[] {
		return this.db
			.prepare(
				`SELECT subject, frame, topic, snippet(frame_text, 3, '', '', '…', 12) AS snippet
				 FROM frame_text WHERE frame_text MATCH ? ORDER BY rank LIMIT ?`
			)
			.all(query, limit) as unknown as SearchHit[];
	}
}

/**
 * What the engine's own code looks like, for `compiler` in a checkout: a
 * change to how content renders rebuilds every subject. Hashes the
 * engine's non-test TypeScript; null where there is no engine source (a
 * deployed build, which names its commit instead).
 */
export function engineDigest(dir: string): string | null {
	const hash = createHash('sha256');
	let found = false;
	const walk = (at: string) => {
		for (const e of readdirSync(at, { withFileTypes: true }).sort((a, b) =>
			a.name < b.name ? -1 : 1
		)) {
			const path = join(at, e.name);
			if (e.isDirectory() && e.name !== 'ui') walk(path);
			else if (e.isFile() && e.name.endsWith('.ts') && !e.name.endsWith('.test.ts')) {
				found = true;
				const s = statSync(path);
				hash.update(`${relative(dir, path)}\0${s.size}\0${s.mtimeMs}\n`);
			}
		}
	};
	try {
		walk(dir);
	} catch {
		return null;
	}
	return found ? hash.digest('hex').slice(0, 16) : null;
}

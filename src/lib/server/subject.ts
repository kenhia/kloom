import { execFile } from 'node:child_process';
import { statSync } from 'node:fs';
import { join, resolve } from 'node:path';
import { promisify } from 'node:util';
import { brotliCompressSync, constants, gzipSync } from 'node:zlib';
import { error } from '@sveltejs/kit';
import { env } from '$env/dynamic/private';
import {
	compileContent,
	ContentDb,
	engineDigest,
	SUBJECT_ID,
	type SubjectEntry
} from '$engine/content-db';
import type { Graph } from '$engine/graph';
import { readMedia } from '$engine/load';
import type { SubjectHead } from '$engine/model';
import type { FrameSource } from '$engine/served';
import type { StartLook } from '$engine/start';
import { dataDir, namesDir, subjectDirFor, subjectsDir } from './config';

/**
 * The served library (docs/design.md §Serving, korg 3460): every read comes
 * from the compiled `content.db`, never from the subjects' files. The files
 * stay the source. This module keeps the library in step with them:
 *
 * - The first read builds it (or finds it current: an unchanged subject is
 *   never compiled twice by the same app).
 * - In the dev server, a change under the subjects or names directories
 *   marks it stale, and the next read rebuilds what changed first.
 * - A grow job holds the gate while it writes, and the library is rebuilt
 *   before the gate opens again, so its frames show at once.
 *
 * A build replaces the file in one rename, and a read that finds a new file
 * opens it, so a library built by `just build-content` is picked up too.
 */

/** Where the library is: `$KLOOM_CONTENT_DB`, or `content.db` in the data directory. */
export const contentDbPath = () => resolve(env.KLOOM_CONTENT_DB ?? join(dataDir(), 'content.db'));

const startedAt = new Date().toISOString();

/**
 * What compiles the library: the engine's own source in a checkout, so a
 * change to how content renders rebuilds it; the build's commit where there
 * is no source; failing both, this process, so it rebuilds once per start.
 */
export const compilerId = () =>
	engineDigest(resolve('engine')) ?? (__KLOOM_BUILD__ || `process ${startedAt}`);

// Made when first used, so a build that never builds (the reader edition) has no git in it.
const sourceCommit = () =>
	promisify(execFile)('git', ['rev-parse', 'HEAD'], { cwd: subjectsDir() }).then(
		(r) => r.stdout.trim(),
		() => ''
	);

/**
 * A gate a grow job holds while it writes new files into a subject: a
 * request that arrives meanwhile waits, so no reader ever sees a library
 * built from a half-written subject. One gate for every subject; grow runs
 * one job at a time anyway.
 */
let gate: Promise<unknown> = Promise.resolve();
/** The sources may have changed since the last build. True at start: the first read checks. */
let stale = true;
let building: Promise<void> | null = null;

async function build() {
	stale = false;
	const report = await compileContent({
		subjectsDir: subjectsDir(),
		namesDir: namesDir(),
		out: contentDbPath(),
		compiler: compilerId(),
		source: await sourceCommit()
	});
	for (const f of report.failed)
		console.error(
			`content: ${f.id} is invalid, so it is served as last built (if ever):\n  ${f.problems.join('\n  ')}`
		);
	if (report.nameProblems.length) console.error(`names: ${report.nameProblems.join('; ')}`);
	if (report.changed)
		console.log(
			`content: built ${report.built.length ? report.built.join(', ') : 'the library'} in ${Math.round(report.ms)} ms` +
				(report.reused.length ? `; ${report.reused.length} subject(s) unchanged` : '')
		);
}

/** Build if the sources may have changed; a build already running is joined. */
async function current() {
	while (stale || building) {
		building ??= build()
			.catch((e) => console.error('content: could not build the library', e))
			.finally(() => (building = null));
		await building;
	}
}

/**
 * The dev server's own watcher says when a source changes (vite.config.ts,
 * `kloomContent`): the next read rebuilds what changed. A service has no
 * watcher; its content moves only at start and in a grow, and both rebuild.
 * Re-registered as the dev server reloads this module, never stacked.
 */
const CHANGED = 'kloom:content-changed';
const listening = globalThis as { kloomContentChanged?: () => void };
if (listening.kloomContentChanged) process.off(CHANGED, listening.kloomContentChanged);
listening.kloomContentChanged = () => (stale = true);
process.on(CHANGED, listening.kloomContentChanged);

/** The open library, and what has been read from it, until another build replaces it. */
let open: { db: ContentDb; path: string; ino: number; mtimeMs: number } | null = null;
let memo = new Map<string, unknown>();

function opened(): ContentDb {
	const path = contentDbPath();
	let s;
	try {
		s = statSync(path);
	} catch {
		error(503, 'The library has not been built.');
	}
	if (open?.path !== path || open.ino !== s.ino || open.mtimeMs !== s.mtimeMs) {
		const db = ContentDb.open(path);
		if (!db) error(503, 'The library could not be opened.');
		// Reads are synchronous, so nothing holds the old file across an await;
		// it is closed a little later all the same.
		const old = open?.db;
		if (old) setTimeout(() => old.close(), 5000).unref();
		open = { db, path, ino: s.ino, mtimeMs: s.mtimeMs };
		memo = new Map();
	}
	return open.db;
}

/**
 * The library, current with the sources and past the gate. The reader
 * edition serves a library built elsewhere and baked in (korg 3500): it
 * opens it as it is and never builds, so none of the building is in it.
 */
export async function library(): Promise<ContentDb> {
	if (__KLOOM_EDITION__ === 'reader') return opened();
	await gate;
	await current();
	return opened();
}

/** Read once per build. */
function once<T>(key: string, read: () => T): T {
	if (!memo.has(key)) memo.set(key, read());
	return memo.get(key) as T;
}

/**
 * The subject's directory, or a 404 for an id the app does not serve: for
 * what writes to a subject's files (grow). Reads ask the library.
 */
export async function requireSubjectDir(id: unknown): Promise<string> {
	const dir = await subjectDirFor(id);
	if (!dir) error(404, 'No such subject.');
	return dir;
}

/** Every subject the library serves, in id order. */
export async function servedSubjects(): Promise<SubjectEntry[]> {
	const db = await library();
	return once('subjects', () => db.subjects());
}

/**
 * Whether a served subject has this frame: what a reader's place, bookmark
 * or note may name. A 404 for an unknown subject.
 */
export async function servedFrame(subject: unknown, frame: unknown): Promise<boolean> {
	const head = await servedSubject(subject);
	return typeof frame === 'string' && Object.hasOwn(head.frames, frame);
}

/**
 * Where the media files are: `$KLOOM_MEDIA_DIR`, laid out as the subjects
 * are (`<subject>/frames/<frame>/<file>`), or the subjects themselves. The
 * reader edition has media beside its library and no subjects.
 */
export const mediaDir = () => resolve(env.KLOOM_MEDIA_DIR ?? subjectsDir());

/** A served frame's media file, or null when the library does not list it. */
export async function servedMedia(subject: string, frame: string, file: string) {
	const db = await library();
	if (!SUBJECT_ID.test(subject) || !db.hasMedia(subject, frame, file)) return null;
	return readMedia(join(mediaDir(), subject), frame, file);
}

/** A served subject's head (every frame's small half); a 404 for an unknown id. */
export async function servedSubject(id: unknown): Promise<SubjectHead> {
	if (typeof id !== 'string' || !SUBJECT_ID.test(id)) error(404, 'No such subject.');
	const db = await library();
	const head = once(`head ${id}`, () => db.head(id));
	if (!head) error(404, 'No such subject.');
	return head;
}

/** A frame's body and links as JSON (`ServedBody`), and the build it is from; null for an unknown frame. */
export async function servedBody(
	subject: string,
	frame: string
): Promise<{ json: string; build: string } | null> {
	const db = await library();
	const json = db.bodyJson(subject, frame);
	return json === null ? null : { json, build: db.build };
}

/** A frame's reading as authored and its citations: what ask gives the model. */
export async function servedSource(subject: string, frame: string): Promise<FrameSource | null> {
	return (await library()).source(subject, frame);
}

/** A subject's start look (the ring of drawings); null for an unknown id. */
export async function servedStart(id: string): Promise<StartLook | null> {
	const db = await library();
	return once(`start ${id}`, () => db.start(id));
}

/**
 * The map's data or the library's counts as a response: the stored JSON,
 * compressed once per build for the encodings the client takes, since the
 * map is large and the same for every reader.
 */
export async function servedLibrary(key: 'map' | 'stats', request: Request): Promise<Response> {
	const db = await library();
	const json = once(key, () => Buffer.from(db.libraryJson(key)));
	const accept = request.headers.get('accept-encoding') ?? '';
	const encoding = /\bbr\b/.test(accept) ? 'br' : /\bgzip\b/.test(accept) ? 'gzip' : null;
	const body = !encoding
		? json
		: once(`${key} ${encoding}`, () =>
				encoding === 'br'
					? brotliCompressSync(json, { params: { [constants.BROTLI_PARAM_QUALITY]: 9 } })
					: gzipSync(json, { level: 9 })
			);
	return new Response(new Uint8Array(body), {
		headers: {
			'content-type': 'application/json',
			...(encoding ? { 'content-encoding': encoding } : {}),
			vary: 'Accept-Encoding',
			'x-kloom-build': db.build
		}
	});
}

/** The graph index across every served subject (docs/design.md §Connections). */
export async function servedGraph(): Promise<Graph> {
	const db = await library();
	return once('graph', () => db.graph());
}

/** The build standing now: what the page's fetched bodies must match. */
export async function servedBuild(): Promise<string> {
	return (await library()).build;
}

/**
 * Run `fn` while the gate is held; readers wait for it. What it wrote is
 * built into the library before the gate opens, whether it succeeded or not.
 */
export function exclusive<T>(fn: () => Promise<T>): Promise<T> {
	const after = async () => {
		stale = true;
		await current();
	};
	const done = gate.then(fn, fn).then(
		async (v) => (await after(), v),
		async (e) => {
			await after();
			throw e;
		}
	);
	gate = done.catch(() => {});
	return done;
}

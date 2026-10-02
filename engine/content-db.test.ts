import {
	cpSync,
	existsSync,
	mkdtempSync,
	readFileSync,
	rmSync,
	statSync,
	writeFileSync
} from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { afterEach, beforeEach, describe, expect, it } from 'vitest';
import { compileContent, ContentDb, ContentError, treeDigest } from './content-db';
import type { MapData } from './map';
import type { ServedBody } from './served';
import type { LibraryStats } from './stats';

const repo = join(import.meta.dirname, '..');

let dir: string;
let subjects: string;
const out = () => join(dir, 'data', 'content.db');
const compile = (extra: Partial<Parameters<typeof compileContent>[0]> = {}) =>
	compileContent({
		subjectsDir: subjects,
		namesDir: join(repo, 'names'),
		out: out(),
		compiler: 'test',
		strict: true,
		...extra
	});
const frameFile = (subject: string, frame: string) =>
	join(subjects, subject, 'frames', frame, 'frame.json');
/** Change a frame's file, and its modified time with it. */
function editFrame(subject: string, frame: string, edit: (f: Record<string, unknown>) => void) {
	const path = frameFile(subject, frame);
	const f = JSON.parse(readFileSync(path, 'utf8'));
	edit(f);
	writeFileSync(path, JSON.stringify(f));
}
const open = () => ContentDb.open(out())!;

beforeEach(() => {
	dir = mkdtempSync(join(tmpdir(), 'kloom-content-test-'));
	subjects = join(dir, 'subjects');
	// Two subjects: western-civ, and a copy of it to connect to.
	cpSync(join(repo, 'subjects', 'western-civ'), join(subjects, 'western-civ'), { recursive: true });
	cpSync(join(repo, 'subjects', 'western-civ'), join(subjects, 'copy'), { recursive: true });
});
afterEach(() => rmSync(dir, { recursive: true, force: true }));

describe('the content compiler', () => {
	it("stores each subject's head, every frame's body, its source and its media", async () => {
		const report = await compile();
		expect(report.built).toEqual(['copy', 'western-civ']);
		const db = open();
		expect(db.subjects().map((s) => s.id)).toEqual(['copy', 'western-civ']);
		const head = db.head('western-civ')!;
		expect(head.title).toBe('The History of Western Civilization');
		// A head carries no body.
		expect(head.frames.prometheus.topic).toBe('The myth of Prometheus');
		expect(Object.keys(head.frames.prometheus)).not.toContain('readingHtml');
		expect(Object.keys(head.frames.prometheus)).not.toContain('citations');
		const body = JSON.parse(db.bodyJson('western-civ', 'prometheus')!) as ServedBody;
		expect(body.readingHtml).toContain('<p>');
		expect(body.svg).toMatch(/^<svg/);
		expect(body.sources.length).toBeGreaterThan(0);
		// Its links: the cards of the names its reading marks.
		expect(body.links.names.hesiod.name).toBe('Hesiod');
		expect(db.bodyJson('western-civ', 'nope')).toBeNull();
		expect(db.source('western-civ', 'prometheus')!.reading).toBe(
			readFileSync(join(subjects, 'western-civ', 'frames', 'prometheus', 'reading.md'), 'utf8')
		);
		expect(db.start('western-civ')!.illustrations.length).toBeGreaterThan(0);
		expect(db.hasMedia('western-civ', 'prometheus', 'scene.svg')).toBe(true);
		expect(db.hasMedia('western-civ', 'prometheus', 'frame.json')).toBe(false);
		db.close();
	});

	it('derives the map, the counts and a full-text index for the library', async () => {
		await compile();
		const db = open();
		const map = JSON.parse(db.libraryJson('map')) as MapData;
		expect(map.subjects.map((s) => s.id)).toEqual(['copy', 'western-civ']);
		expect(map.frames.some((f) => f.key === 'copy/prometheus')).toBe(true);
		const stats = JSON.parse(db.libraryJson('stats')) as LibraryStats;
		expect(stats.subjects.map((s) => s.id)).toEqual(['copy', 'western-civ']);
		expect(stats.words).toBe(stats.subjects[0].words * 2);
		expect(db.search('fennel', 5).map((h) => h.frame)).toContain('prometheus');
		expect(db.graph().frames.has('western-civ/prometheus')).toBe(true);
		db.close();
	});

	it('refuses an invalid subject in a strict build, naming every problem, and leaves the old file', async () => {
		await compile();
		const before = statSync(out()).ino;
		editFrame('copy', 'prometheus', (f) => {
			delete f.topic;
			f.citations = [];
		});
		const failed = await compile().catch((e) => e);
		expect(failed).toBeInstanceOf(ContentError);
		expect((failed as ContentError).failed[0].id).toBe('copy');
		expect((failed as ContentError).failed[0].problems.join('\n')).toMatch(/prometheus.*topic/);
		expect(statSync(out()).ino).toBe(before);
		expect(existsSync(out())).toBe(true);
	});

	it('serves an invalid subject as it was last built, outside a strict build', async () => {
		await compile();
		editFrame('copy', 'prometheus', (f) => delete f.topic);
		const report = await compile({ strict: false });
		expect(report.failed.map((f) => f.id)).toEqual(['copy']);
		expect(open().head('copy')!.frames.prometheus.topic).toBe('The myth of Prometheus');
		// One that was never built is not served at all.
		rmSync(out());
		await compile({ strict: false });
		expect(open().head('copy')).toBeNull();
	});

	it('rebuilds only what changed, and derives the links across subjects again', async () => {
		await compile();
		const prometheus = () =>
			(JSON.parse(open().bodyJson('western-civ', 'prometheus')!) as ServedBody).links.connections;
		expect(prometheus().some((c) => c.subject === 'copy' && c.frame === 'writing')).toBe(false);

		editFrame('copy', 'writing', (f) => {
			f.connections = [{ to: 'western-civ/prometheus', why: 'Fire, then the word.' }];
		});
		const report = await compile();
		expect(report.built).toEqual(['copy']);
		expect(report.reused).toEqual(['western-civ']);
		// Stored on copy's frame, shown on western-civ's, which was not rebuilt.
		expect(prometheus()).toContainEqual(
			expect.objectContaining({ direction: 'in', subject: 'copy', frame: 'writing' })
		);
	});

	it('does nothing when nothing changed, and starts afresh for another compiler', async () => {
		const first = await compile();
		const again = await compile();
		expect(again.changed).toBe(false);
		expect(again.build).toBe(first.build);
		const other = await compile({ compiler: 'another' });
		expect(other.built).toEqual(['copy', 'western-civ']);
	});

	it('takes out a subject that is gone', async () => {
		await compile();
		rmSync(join(subjects, 'copy'), { recursive: true });
		const report = await compile();
		expect(report.dropped).toEqual(['copy']);
		const db = open();
		expect(db.subjects().map((s) => s.id)).toEqual(['western-civ']);
		expect(db.bodyJson('copy', 'prometheus')).toBeNull();
		expect(db.search('fennel', 5).every((h) => h.subject === 'western-civ')).toBe(true);
	});

	it('swaps the new file in with a rename, leaving no temporary file', async () => {
		await compile();
		const reader = open();
		const build = reader.build;
		editFrame('copy', 'writing', (f) => (f.topic = 'Writing, again'));
		await compile();
		// A reader of the old file still reads it whole; a new one sees the new build.
		expect(reader.head('copy')!.frames.writing.topic).not.toBe('Writing, again');
		expect(reader.build).toBe(build);
		expect(open().head('copy')!.frames.writing.topic).toBe('Writing, again');
		expect(open().build).not.toBe(build);
		reader.close();
		const left = (await import('node:fs')).readdirSync(join(dir, 'data'));
		expect(left).toEqual(['content.db']);
	});
});

describe('a tree digest', () => {
	it('changes with a file written, added or removed, and not with a hidden one', () => {
		const at = join(subjects, 'western-civ');
		const d = treeDigest(at);
		expect(treeDigest(at)).toBe(d);
		writeFileSync(join(at, 'frames', '.grow-staging'), 'x');
		expect(treeDigest(at)).toBe(d);
		writeFileSync(join(at, 'frames', 'prometheus', 'note.txt'), 'x');
		expect(treeDigest(at)).not.toBe(d);
	});
});

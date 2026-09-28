import { mkdtempSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { DatabaseSync } from 'node:sqlite';
import { afterEach, describe, expect, it } from 'vitest';
import { parseExport } from '$engine/reader-data';
import { openReaderStore, SCHEMA_VERSION } from './reader-store';

/** A clock the test moves: each call is a second after the last. */
function clock(start = Date.parse('2026-09-28T12:00:00Z')) {
	let t = start;
	return () => new Date((t += 1000));
}

const ken = 'ken@github';
const ada = 'ada@github';
const at = (subject: string, frame: string) => ({ subject, frame, label: `${frame} label` });

describe('last visited', () => {
	it('keeps one place per subject, and the newest overall', async () => {
		const store = openReaderStore(':memory:', clock());
		expect(await store.lastVisited(ken)).toBeNull();
		await store.visit(ken, at('western-civ', 'fire'));
		await store.visit(ken, at('ai', 'turing'));
		await store.visit(ken, at('western-civ', 'printing-press'));
		expect(await store.lastVisited(ken, 'western-civ')).toMatchObject({ frame: 'printing-press' });
		expect(await store.lastVisited(ken, 'ai')).toMatchObject({ frame: 'turing' });
		expect(await store.lastVisited(ken)).toMatchObject({
			subject: 'western-civ',
			frame: 'printing-press',
			label: 'printing-press label',
			at: '2026-09-28T12:00:03.000Z'
		});
		expect(await store.lastVisited(ken, 'nope')).toBeNull();
	});

	it('keeps each reader’s own', async () => {
		const store = openReaderStore(':memory:', clock());
		await store.visit(ken, at('ai', 'turing'));
		await store.visit(ada, at('ai', 'dartmouth'));
		expect(await store.lastVisited(ken, 'ai')).toMatchObject({ frame: 'turing' });
		expect(await store.lastVisited(ada)).toMatchObject({ frame: 'dartmouth' });
	});
});

describe('bookmarks', () => {
	it('lists a reader’s marks across subjects, newest first, and removes one', async () => {
		const store = openReaderStore(':memory:', clock());
		await store.bookmark(ken, at('western-civ', 'fire'));
		await store.bookmark(ken, at('ai', 'turing'));
		await store.bookmark(ada, at('ai', 'dartmouth'));
		expect((await store.bookmarks(ken)).map((b) => b.frame)).toEqual(['turing', 'fire']);
		await store.unbookmark(ken, 'western-civ', 'fire');
		expect((await store.bookmarks(ken)).map((b) => b.frame)).toEqual(['turing']);
		expect((await store.bookmarks(ada)).map((b) => b.frame)).toEqual(['dartmouth']);
	});

	it('marking a frame again keeps one mark and its first date, with the new label', async () => {
		const store = openReaderStore(':memory:', clock());
		await store.bookmark(ken, at('ai', 'turing'));
		await store.bookmark(ken, { subject: 'ai', frame: 'turing', label: 'Renamed' });
		const marks = await store.bookmarks(ken);
		expect(marks).toHaveLength(1);
		expect(marks[0]).toMatchObject({ label: 'Renamed', at: '2026-09-28T12:00:01.000Z' });
	});
});

describe('export and import', () => {
	it('round-trips through the export format into another reader', async () => {
		const from = openReaderStore(':memory:', clock());
		await from.visit(ken, at('ai', 'turing'));
		await from.bookmark(ken, at('western-civ', 'fire'));
		const file = JSON.parse(JSON.stringify(await from.exportData(ken)));
		const parsed = parseExport(file);
		if ('error' in parsed) throw new Error(parsed.error);

		const to = openReaderStore(':memory:', clock(Date.parse('2026-01-01T00:00:00Z')));
		expect(await to.importData(ada, parsed)).toEqual({ places: 1, bookmarks: 1 });
		expect(await to.lastVisited(ada, 'ai')).toMatchObject({
			frame: 'turing',
			at: '2026-09-28T12:00:01.000Z'
		});
		expect(await to.bookmarks(ada)).toMatchObject([{ subject: 'western-civ', frame: 'fire' }]);
	});

	it('never moves a place back in time', async () => {
		const store = openReaderStore(':memory:', clock());
		await store.visit(ken, at('ai', 'transformer'));
		await store.importData(ken, {
			kloom: 'reader-data',
			version: 1,
			reader: ken,
			exported: '2026-01-01T00:00:00.000Z',
			places: [{ ...at('ai', 'turing'), at: '2026-01-01T00:00:00.000Z' }],
			bookmarks: []
		});
		expect(await store.lastVisited(ken, 'ai')).toMatchObject({ frame: 'transformer' });
	});
});

describe('the file', () => {
	let dir: string | undefined;
	afterEach(() => {
		if (dir) rmSync(dir, { recursive: true, force: true });
	});

	it('is created with its directory, migrated, and keeps what it holds across opens', async () => {
		dir = mkdtempSync(join(tmpdir(), 'kloom-reader-'));
		const path = join(dir, 'nested', 'reader.db');
		const first = openReaderStore(path, clock());
		await first.bookmark(ken, at('ai', 'turing'));
		first.close();

		const raw = new DatabaseSync(path);
		expect(raw.prepare('PRAGMA user_version').get()).toEqual({ user_version: SCHEMA_VERSION });
		raw.close();

		const again = openReaderStore(path, clock());
		expect(await again.bookmarks(ken)).toHaveLength(1);
		again.close();
	});

	it('refuses a file from a newer app rather than guess at its schema', () => {
		dir = mkdtempSync(join(tmpdir(), 'kloom-reader-'));
		const path = join(dir, 'reader.db');
		const raw = new DatabaseSync(path);
		raw.exec(`PRAGMA user_version = ${SCHEMA_VERSION + 1}`);
		raw.close();
		expect(() => openReaderStore(path)).toThrow(/newer than this app/);
	});
});

import { describe, expect, it } from 'vitest';
import { LABEL_MAX, parseExport, recordOf } from './reader-data';

const good = {
	kloom: 'reader-data',
	version: 1,
	reader: 'ken@github',
	exported: '2026-09-28T12:00:00.000Z',
	places: [{ subject: 'ai', frame: 'turing', label: 'Turing', at: '2026-09-28T12:00:00Z' }],
	bookmarks: []
};

describe('a record', () => {
	it('takes plain ids and cuts a long label', () => {
		expect(
			recordOf({ subject: 'ai', frame: 'turing', label: 'x'.repeat(500) })?.label
		).toHaveLength(LABEL_MAX);
	});

	it('refuses a path, a missing label or a non-object', () => {
		for (const bad of [
			{ subject: '../ai', frame: 'turing', label: '' },
			{ subject: 'ai', frame: 'a/b', label: '' },
			{ subject: 'ai', frame: 'turing' },
			null,
			'ai'
		])
			expect(recordOf(bad)).toBeNull();
	});
});

describe('an export file', () => {
	it('reads a good one, normalising its times', () => {
		const parsed = parseExport(good);
		expect(parsed).toMatchObject({ places: [{ at: '2026-09-28T12:00:00.000Z' }] });
	});

	it('refuses the whole file for one bad record', () => {
		expect(parseExport({ ...good, bookmarks: [{ subject: 'ai' }] })).toEqual({
			error: 'bookmark 0 is not a valid record'
		});
		expect(parseExport({ ...good, places: [{ ...good.places[0], at: 'yesterday' }] })).toEqual({
			error: 'place 0 is not a valid record'
		});
	});

	it('refuses something that is not an export, or a version it does not know', () => {
		expect(parseExport([])).toMatchObject({ error: 'not a kloom reader-data export' });
		expect(parseExport({ ...good, version: 2 })).toEqual({ error: 'unknown version 2' });
		expect(parseExport({ ...good, places: 'x' })).toMatchObject({ error: /lists/ });
	});
});

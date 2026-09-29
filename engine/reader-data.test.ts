import { describe, expect, it } from 'vitest';
import { LABEL_MAX, newerPlaces, parseExport, recordOf, type Place } from './reader-data';

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

	it('reads a version 1 file as one with no notes or kept answers', () => {
		expect(parseExport(good)).toMatchObject({ version: 3, notes: [], kept: [] });
	});

	it('reads version 2’s notes, and refuses a bad one', () => {
		const n = {
			id: 'a1',
			subject: 'ai',
			frame: 'turing',
			label: 'Turing',
			text: 'look again',
			review: 'flagged',
			response: null,
			created: '2026-09-28T12:00:00Z',
			updated: '2026-09-28T12:00:00Z'
		};
		const v2 = { ...good, version: 2, notes: [n], kept: [] };
		expect(parseExport(v2)).toMatchObject({
			notes: [{ id: 'a1', review: 'flagged', anchor: null }]
		});
		expect(parseExport({ ...v2, notes: [{ ...n, review: 'maybe' }] })).toEqual({
			error: 'note 0 is not a valid note'
		});
		expect(parseExport({ ...v2, kept: [{ answer: {}, grown: null }] })).toEqual({
			error: 'kept answer 0 is not a valid kept answer'
		});
		expect(parseExport({ ...v2, notes: undefined })).toMatchObject({ error: /lists/ });
	});

	it('reads version 3’s anchors, and refuses a bad one', () => {
		const n = {
			id: 'a1',
			subject: 'ai',
			frame: 'turing',
			label: 'Turing',
			text: 'which words?',
			anchor: { exact: 'these words', prefix: 'Of ', suffix: '.', start: 3 },
			review: 'none',
			response: null,
			created: '2026-09-28T12:00:00Z',
			updated: '2026-09-28T12:00:00Z'
		};
		const v3 = { ...good, version: 3, notes: [n, { ...n, id: 'a2', anchor: null }], kept: [] };
		expect(parseExport(v3)).toMatchObject({
			notes: [{ anchor: n.anchor }, { id: 'a2', anchor: null }]
		});
		expect(parseExport({ ...v3, notes: [{ ...n, anchor: { exact: '' } }] })).toEqual({
			error: 'note 0 is not a valid note'
		});
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
		expect(parseExport({ ...good, version: 4 })).toEqual({ error: 'unknown version 4' });
		expect(parseExport({ ...good, places: 'x' })).toMatchObject({ error: /lists/ });
	});
});

describe('places kept on the page', () => {
	const at = (subject: string, frame: string, when: string): Place => ({
		subject,
		frame,
		label: frame,
		at: `2026-09-29T10:00:${when}.000Z`
	});

	it('keeps the newer place per subject, from either copy', () => {
		const page = { a: at('a', 'moved', '30'), b: at('b', 'old', '10') };
		const loaded = { a: at('a', 'stale', '20'), b: at('b', 'new', '40'), c: at('c', 'only', '00') };
		expect(newerPlaces(page, loaded)).toEqual({
			a: page.a,
			b: loaded.b,
			c: loaded.c
		});
	});

	it('prefers the fresh load when the two agree on the time', () => {
		const loaded = { a: { ...at('a', 'x', '30'), label: 'renamed' } };
		expect(newerPlaces({ a: at('a', 'x', '30') }, loaded).a.label).toBe('renamed');
	});
});

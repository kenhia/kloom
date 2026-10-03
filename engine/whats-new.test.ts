import { describe, expect, it } from 'vitest';
import type { SubjectHead } from './model';
import {
	ALL,
	byDayAndSubject,
	changelogOf,
	dayLabel,
	filterChangelog,
	newToYou,
	newTrails,
	readingFrom,
	type ChangelogData,
	type FilterContext
} from './whats-new';

const at = (d: string) => `2026-09-${d}T10:00:00.000Z`;

describe('new to you', () => {
	const added = { a: at('01'), b: at('10'), c: at('12'), d: at('20') };

	it('is what was added after the reader started the subject and they have not opened', () => {
		expect(newToYou(added, { first: at('05'), caughtUp: null }, [])).toEqual(['b', 'c', 'd']);
		expect(newToYou(added, { first: at('05'), caughtUp: null }, ['c'])).toEqual(['b', 'd']);
	});

	it('is nothing in a subject they have never started: all of it is new, so none of it is marked', () => {
		expect(newToYou(added, null, [])).toEqual([]);
		expect(newToYou(added, undefined, [])).toEqual([]);
	});

	it('counts from when they caught up, once they have', () => {
		const r = { first: at('05'), caughtUp: at('15') };
		expect(readingFrom(r)).toBe(at('15'));
		expect(newToYou(added, r, [])).toEqual(['d']);
		// A watermark before the first visit (an import) never widens it.
		expect(readingFrom({ first: at('05'), caughtUp: at('02') })).toBe(at('05'));
	});

	it('marks a trail when any of its frames is new', () => {
		const head = {
			trails: [
				{ id: 't1', spine: { segments: [{ frames: ['x', 'y'] }] } },
				{ id: 't2', spine: { segments: [{ frames: ['z'] }] } }
			]
		} as unknown as SubjectHead;
		expect(newTrails(head, new Set(['y']))).toEqual(new Set(['t1']));
	});
});

/** A subject head, as small as the Changelog needs. */
function subject(): SubjectHead {
	const frame = (id: string, added?: string) => ({
		id,
		topic: `Topic ${id}`,
		position: { label: id.toUpperCase() },
		scene: { headline: 'H', accent: id, palette: 'p', metadata: [] },
		...(added ? { added } : {})
	});
	return {
		id: 's',
		title: 'S',
		palettes: {},
		created: at('01'),
		spine: {
			segments: [{ id: 'g', title: 'G', labelKind: 'category', frames: ['a', 'b', 'c', 'w'] }]
		},
		trails: [
			{
				id: 'old',
				title: 'Old trail',
				anchor: 'a',
				added: at('01'),
				spine: { segments: [{ id: 'o', title: 'O', labelKind: 'category', frames: ['o1'] }] }
			},
			{
				id: 'late',
				title: 'Late trail',
				anchor: 'b',
				added: at('12'),
				spine: { segments: [{ id: 'l', title: 'L', labelKind: 'category', frames: ['l1', 'l2'] }] }
			}
		],
		frames: {
			a: frame('a', at('01')),
			b: frame('b', at('01')),
			c: frame('c', at('10')),
			w: frame('w'),
			o1: frame('o1', at('01')),
			// One came with its trail; one was added to it later.
			l1: frame('l1', at('12')),
			l2: frame('l2', at('15'))
		}
	} as SubjectHead;
}

describe('the Changelog', () => {
	const data = changelogOf(
		[subject()],
		[
			{ subject: 's', frame: 'a', date: '2026-09-14', kind: 'revision', summary: 'Revised.' },
			{ subject: 's', frame: 'c', date: '2026-09-18', kind: 'correction', summary: 'Corrected.' },
			{ subject: 's', frame: 'gone', date: '2026-09-19', kind: 'correction', summary: 'Gone.' }
		]
	);

	it('says a first publish once, a trail with the frames it came with, and every later frame', () => {
		expect(
			data.added.map((e) => [e.kind, e.id, e.frame, e.frames ?? null, e.trail ?? null])
		).toEqual([
			['frame', 'l2', 'l2', null, 'Late trail'],
			['trail', 'late', 'l1', ['l1'], null],
			['frame', 'c', 'c', null, null],
			['subject', 's', 'a', ['a', 'b', 'o1'], null]
		]);
		// An undated frame (not committed yet) is not in it.
		expect(data.added.some((e) => e.id === 'w')).toBe(false);
	});

	it('lists edits newest first, naming each frame, and drops one on a frame that is gone', () => {
		expect(data.edits.map((e) => [e.frame, e.title, e.position, e.kind])).toEqual([
			['c', 'Topic c', 'C', 'correction'],
			['a', 'Topic a', 'A', 'revision']
		]);
	});

	const two: ChangelogData = {
		subjects: [],
		added: [
			{ subject: 'b', at: at('20'), kind: 'frame', id: 'x', frame: 'x', title: 'X', position: '' },
			{ subject: 'a', at: at('20'), kind: 'frame', id: 'y', frame: 'y', title: 'Y', position: '' },
			{ subject: 'a', at: at('08'), kind: 'frame', id: 'z', frame: 'z', title: 'Z', position: '' }
		],
		edits: [
			{
				subject: 'a',
				frame: 'y',
				title: 'Y',
				position: '',
				date: '2026-09-21',
				kind: 'revision',
				summary: ''
			},
			{
				subject: 'b',
				frame: 'x',
				title: 'X',
				position: '',
				date: '2026-09-03',
				kind: 'revision',
				summary: ''
			}
		]
	};
	const ctx: FilterContext = {
		now: new Date(at('25')),
		news: {
			readings: {
				a: { first: at('05'), caughtUp: at('15') },
				b: { first: at('22'), caughtUp: null }
			},
			lastVisit: at('10'),
			fresh: {}
		},
		dayOf: (iso) => iso.slice(0, 10)
	};
	const ids = (f: Partial<typeof ALL>, c = ctx) => {
		const r = filterChangelog(two, { ...ALL, ...f }, c);
		return [...r.added.map((e) => e.id), ...r.edits.map((e) => `edit ${e.frame}`)];
	};

	it('filters by subject, and by when: presets and a range of days', () => {
		expect(ids({})).toEqual(['x', 'y', 'z', 'edit y', 'edit x']);
		expect(ids({ subjects: ['a'] })).toEqual(['y', 'z', 'edit y']);
		expect(ids({ when: 'last-visit' })).toEqual(['x', 'y', 'edit y']);
		expect(ids({ when: '7' })).toEqual(['x', 'y', 'edit y']);
		expect(ids({ when: '30' })).toEqual(['x', 'y', 'z', 'edit y', 'edit x']);
		expect(ids({ when: 'between', from: '2026-09-03', to: '2026-09-08' })).toEqual(['z', 'edit x']);
		expect(ids({ when: 'between', from: '2026-09-21' })).toEqual(['edit y']);
	});

	it('counts "since I caught up" from each subject’s own mark, or its first visit', () => {
		// a: caught up on the 15th; b: first visit on the 22nd.
		expect(ids({ when: 'caught-up' })).toEqual(['y', 'edit y']);
		// With no reader, the reader's presets keep everything.
		expect(ids({ when: 'caught-up' }, { ...ctx, news: null })).toEqual([
			'x',
			'y',
			'z',
			'edit y',
			'edit x'
		]);
		expect(ids({ when: 'last-visit' }, { ...ctx, news: null })).toHaveLength(5);
	});

	it('groups by day, then by subject, keeping the order given', () => {
		const groups = byDayAndSubject(two.added, (e) => e.at.slice(0, 10));
		expect(
			groups.map((d) => [d.day, d.subjects.map((s) => [s.subject, s.entries.length])])
		).toEqual([
			[
				'2026-09-20',
				[
					['b', 1],
					['a', 1]
				]
			],
			['2026-09-08', [['a', 1]]]
		]);
		expect(dayLabel('2026-10-03')).toBe('October 3, 2026');
	});
});

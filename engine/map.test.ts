import { describe, expect, it, vi } from 'vitest';
import { buildGraph, type GraphSubject } from './graph';
import {
	labelLines,
	layoutView,
	mapDataOf,
	MapIndex,
	placeLabels,
	SHARED_CAP,
	stepFrom,
	subjectSlot,
	viewOf,
	type MapView
} from './map';
import type { Name } from './names';

type F = GraphSubject['frames'][number];
const frame = (subject: string, id: string, extra: Partial<F> = {}): F => ({
	subject,
	frame: id,
	title: `We did ${id.toUpperCase()}.`,
	topic: `Topic ${id}`,
	label: id,
	trail: null,
	connections: [],
	names: [],
	...extra
});

const name = (id: string, extra: Partial<Name> = {}): Name => ({
	id,
	wikidata: null,
	name: id.replace(/-/g, ' '),
	kind: 'person',
	description: `About ${id}.`,
	...extra
});

/**
 * a/one connects to a/two and b/one; b/one connects on to b/two. a/one marks
 * `rare` (with b/three alone) and `hub` (with every frame in c).
 */
function fixture() {
	const hubbed = Array.from({ length: SHARED_CAP + 3 }, (_, i) =>
		frame('c', `c${String(i).padStart(2, '0')}`, { names: ['hub'] })
	);
	const subjects: GraphSubject[] = [
		{
			id: 'a',
			title: 'Alpha',
			frames: [
				frame('a', 'one', {
					names: ['rare', 'hub'],
					connections: [
						{ to: 'a/two', why: 'Next door.' },
						{ to: 'b/one', why: 'Across.' },
						{ to: 'z/gone', why: 'Detached.' }
					]
				}),
				frame('a', 'two'),
				frame('a', 'lonely')
			]
		},
		{
			id: 'b',
			title: 'Beta',
			frames: [
				frame('b', 'one', { connections: [{ to: 'b/two', why: 'Further.' }] }),
				frame('b', 'two'),
				frame('b', 'three', { names: ['rare', 'hub'] })
			]
		},
		{ id: 'c', title: 'Gamma', frames: hubbed }
	];
	const names = {
		rare: name('rare', { home: 'b/three' }),
		hub: name('hub'),
		unmarked: name('unmarked')
	};
	return new MapIndex(mapDataOf(buildGraph(subjects, names)));
}

const ids = (v: MapView, ring?: number) =>
	v.nodes.filter((n) => ring === undefined || n.ring === ring).map((n) => n.id);

describe('the map data', () => {
	const index = fixture();
	it('leaves out detached connections and names no frame marks', () => {
		expect(index.data.links.map((l) => l.to)).not.toContain('z/gone');
		expect(Object.keys(index.data.names).sort()).toEqual(['hub', 'rare']);
		expect(index.data.subjects.map((s) => s.id)).toEqual(['a', 'b', 'c']);
	});
});

describe('a neighbourhood', () => {
	const index = fixture();

	it('one step: the frame, its connections and its names', () => {
		const v = viewOf(index, { view: 'frame', key: 'a/one', steps: 1 })!;
		expect(v.center).toBe('f:a/one');
		expect(ids(v, 0)).toEqual(['f:a/one']);
		expect(ids(v, 1).sort()).toEqual(['f:a/two', 'f:b/one', 'n:hub', 'n:rare']);
		expect(v.edges).toContainEqual({
			a: 'f:a/one',
			b: 'f:b/one',
			kind: 'connection',
			why: 'Across.',
			weight: 1
		});
		expect(v.sections.map((s) => s.title)).toEqual(['Connections', 'Names on this frame']);
		expect(v.sections[0].items[1]).toEqual({
			node: 'f:b/one',
			label: 'Topic one',
			detail: 'We did ONE. · one · Beta',
			note: 'Across.'
		});
	});

	it('two steps: connections of connections, and the frames sharing the rarest names, capped', () => {
		const v = viewOf(index, { view: 'frame', key: 'a/one', steps: 2 })!;
		const two = ids(v, 2);
		expect(two).toContain('f:b/two');
		// b/three shares the rare name as well as the hub, so it ranks first.
		const shared = v.sections.find((s) => s.title === 'Shares names')!.items;
		expect(shared[0]).toMatchObject({ node: 'f:b/three', note: 'Shares rare, hub' });
		expect(shared).toHaveLength(SHARED_CAP);
		expect(two).toHaveLength(1 + SHARED_CAP);
		expect(v.note).toMatch(/^4 more frames share a name/);
		// The names reach the frames that mark them.
		expect(v.edges).toContainEqual(expect.objectContaining({ a: 'f:b/three', b: 'n:rare' }));
		expect(v.sections[1]).toEqual({
			title: 'Two steps away',
			items: [expect.objectContaining({ node: 'f:b/two', note: 'Through Topic one: Further.' })]
		});
	});

	it('is null for a frame the map does not have', () => {
		expect(viewOf(index, { view: 'frame', key: 'a/nope', steps: 1 })).toBeNull();
	});
});

describe('the library, a subject and a name', () => {
	const index = fixture();

	it('the library: a node per subject, lines weighted by their connections', () => {
		const v = viewOf(index, { view: 'library' })!;
		expect(ids(v)).toEqual(['s:a', 's:b', 's:c']);
		expect(v.edges).toEqual([{ a: 's:a', b: 's:b', kind: 'between', weight: 1 }]);
		expect(v.sections[0].items[0].note).toBe(
			'Beta: 1 connection, 2 shared names; Gamma: no connections, 1 shared name'
		);
	});

	it('a subject: its connected frames and where they lead, the rest said', () => {
		const v = viewOf(index, { view: 'subject', id: 'a' })!;
		expect(ids(v, 1).sort()).toEqual(['f:a/one', 'f:a/two']);
		expect(ids(v, 2)).toEqual(['f:b/one']);
		expect(v.note).toBe('1 frame of Alpha has no connections yet, and is left off.');
		expect(v.sections.map((s) => s.title)).toEqual(['Frames with connections', 'In Beta']);
	});

	it('a name: the frames that mark it, its home first', () => {
		const v = viewOf(index, { view: 'name', id: 'rare' })!;
		expect(v.center).toBe('n:rare');
		expect(ids(v, 1).sort()).toEqual(['f:a/one', 'f:b/three']);
		expect(v.sections.map((s) => [s.title, s.items.map((i) => i.node)])).toEqual(
			[
				['Chiefly', ['f:b/three']],
				['In Alpha', ['f:a/one']],
				['In Beta', []]
			].filter(([, items]) => (items as string[]).length)
		);
	});
});

describe('the layout', () => {
	const index = fixture();
	const v = viewOf(index, { view: 'frame', key: 'a/one', steps: 2 })!;

	it('is the same every time, with the centre at the origin', () => {
		const a = layoutView(v);
		const b = layoutView(viewOf(fixture(), { view: 'frame', key: 'a/one', steps: 2 })!);
		expect([...a]).toEqual([...b]);
		expect(a.get('f:a/one')).toEqual({ x: 0, y: 0 });
		expect(a.size).toBe(v.nodes.length);
	});

	it('never asks Math.random: a coincidence is broken by the seed, the same way each time', () => {
		const random = vi.spyOn(Math, 'random').mockImplementation(() => {
			throw new Error('Math.random');
		});
		try {
			expect(() => layoutView(v)).not.toThrow();
		} finally {
			random.mockRestore();
		}
	});

	it('keeps nodes apart', () => {
		const at = layoutView(v);
		const pts = v.nodes.map((n) => ({ ...at.get(n.id)!, r: n.size }));
		for (let i = 0; i < pts.length; i++)
			for (let j = i + 1; j < pts.length; j++)
				expect(Math.hypot(pts[i].x - pts[j].x, pts[i].y - pts[j].y)).toBeGreaterThan(
					pts[i].r + pts[j].r
				);
	});
});

describe('labels', () => {
	const box = (id: string, x: number, y: number, priority = 0) => ({
		id,
		x,
		y,
		r: 5,
		width: 60,
		height: 14,
		priority
	});
	const area = { width: 400, height: 300 };

	it('go right when there is room, and elsewhere when there is not', () => {
		const at = placeLabels([box('a', 100, 100, 1), box('b', 130, 100)], area);
		// Right of a would cross b's node, so a's label goes left.
		expect(at.get('a')).toBe('left');
		expect(at.get('b')).toBe('right');
		expect(placeLabels([box('a', 100, 100)], area).get('a')).toBe('right');
		const crowded = placeLabels([box('a', 100, 100, 1), box('b', 100, 110)], area);
		expect(crowded.get('b')).not.toBe('right');
	});

	it('keep inside the area, and give up when nowhere fits', () => {
		expect(placeLabels([box('edge', 390, 150)], area).get('edge')).toBe('left');
		const pile = [
			box('a', 100, 100, 5),
			...['b', 'c', 'd', 'e', 'f'].map((id) => box(id, 100, 100))
		];
		expect([...placeLabels(pile, area).values()]).toContain(null);
	});
});

describe('labels', () => {
	it('name a frame by its topic, whole, with its headline said after it', () => {
		const n = viewOf(fixture(), { view: 'frame', key: 'a/one', steps: 1 })!.nodes[0];
		expect(n).toMatchObject({ lines: ['Topic one'], full: 'Topic one' });
		expect(n.detail).toBe('We did ONE. · one');
	});

	it('break a long one into two even lines at a space, never inside a word', () => {
		expect(labelLines('The transistor')).toEqual(['The transistor']);
		expect(labelLines("Dirac's Lagrangian in quantum mechanics")).toEqual([
			"Dirac's Lagrangian",
			'in quantum mechanics'
		]);
		expect(labelLines('Colossus: secrecy and the rebuild')).toEqual([
			'Colossus: secrecy',
			'and the rebuild'
		]);
		const one = 'Supercalifragilisticexpialidocious';
		expect(labelLines(one)).toEqual([one]);
		for (const s of [
			'Llull, Leibniz and mechanical reasoning',
			'The Morris worm and network security'
		])
			expect(labelLines(s).join(' ')).toBe(s);
	});
});

describe('arrow keys', () => {
	const v: MapView = {
		target: { view: 'library' },
		title: '',
		center: 'm',
		nodes: ['m', 'e', 'far-e', 'n', 'w'].map((id) => ({
			id,
			kind: 'frame' as const,
			lines: [id],
			full: id,
			detail: '',
			subject: null,
			ring: 0,
			size: 5
		})),
		edges: [
			{ a: 'm', b: 'far-e', kind: 'connection', weight: 1 },
			{ a: 'm', b: 'n', kind: 'connection', weight: 1 }
		],
		sections: []
	};
	const at = new Map([
		['m', { x: 0, y: 0 }],
		['e', { x: 50, y: 0 }],
		['far-e', { x: 200, y: 10 }],
		['n', { x: 5, y: -100 }],
		['w', { x: -80, y: 0 }]
	]);

	it('prefer a joined neighbour that way, over a nearer stranger', () => {
		expect(stepFrom(v, at, 'm', 'right')).toBe('far-e');
		expect(stepFrom(v, at, 'm', 'up')).toBe('n');
	});
	it('fall back to the nearest node that way, and stop at the edge', () => {
		expect(stepFrom(v, at, 'm', 'left')).toBe('w');
		expect(stepFrom(v, at, 'm', 'down')).toBeNull();
		expect(stepFrom(v, at, 'far-e', 'right')).toBeNull();
	});
});

describe('subjects', () => {
	it('take a colour slot and a shape in served order', () => {
		const index = fixture();
		expect(subjectSlot(index.data, 'a')).toEqual({ slot: 1, shape: 'circle' });
		expect(subjectSlot(index.data, 'c')).toEqual({ slot: 3, shape: 'diamond' });
		expect(subjectSlot(index.data, 'nope')).toEqual({ slot: null, shape: 'other' });
	});
});

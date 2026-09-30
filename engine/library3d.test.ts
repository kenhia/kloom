import { describe, expect, it } from 'vitest';
import { library3dOf } from './library3d';
import type { MapData, MapFrame } from './map';

const frame = (key: string, trail: string | null = null): MapFrame => ({
	key,
	title: `We did ${key}.`,
	topic: `Topic ${key}`,
	label: '1900',
	trail
});

/** a/one connects to a/two and to b/one; `ada` is marked in a/one and b/one, `solo` in a/two. */
const data: MapData = {
	subjects: [
		{ id: 'a', title: 'Alpha' },
		{ id: 'b', title: 'Beta' }
	],
	frames: [frame('a/one'), frame('a/two'), frame('b/one', 'A trail'), frame('b/lonely')],
	links: [
		{ from: 'a/one', to: 'a/two', why: 'Next door.' },
		{ from: 'a/one', to: 'b/one', why: 'Across.' }
	],
	names: {
		ada: { name: 'Ada', kind: 'person', description: 'A mathematician.', home: null },
		solo: { name: 'Solo', kind: 'person', description: 'Alone.', home: null }
	},
	mentions: { ada: ['a/one', 'b/one'], solo: ['a/two'] }
};

describe('library3dOf', () => {
	const g = library3dOf(data);

	it('draws every frame, the unconnected ones too, and every marked name', () => {
		expect(g.nodes.map((n) => n.id)).toEqual([
			'f:a/one',
			'f:a/two',
			'f:b/one',
			'f:b/lonely',
			'n:ada',
			'n:solo'
		]);
	});

	it('labels a frame by its topic and says where it is', () => {
		const n = g.nodes.find((n) => n.id === 'f:b/one')!;
		expect(n).toMatchObject({ kind: 'frame', subject: 'b', label: 'Topic b/one' });
		expect(n.detail).toBe('We did b/one. · Beta · 1900, A trail');
		expect(g.nodes.find((n) => n.id === 'n:ada')).toMatchObject({
			kind: 'name',
			subject: null,
			label: 'Ada',
			detail: 'A mathematician.'
		});
	});

	it('links connections between frames and each mention of a name', () => {
		expect(g.links).toEqual([
			{ source: 'f:a/one', target: 'f:a/two', kind: 'connection' },
			{ source: 'f:a/one', target: 'f:b/one', kind: 'connection' },
			{ source: 'f:a/one', target: 'n:ada', kind: 'mention' },
			{ source: 'f:b/one', target: 'n:ada', kind: 'mention' },
			{ source: 'f:a/two', target: 'n:solo', kind: 'mention' }
		]);
	});

	it('sizes a node by its links', () => {
		const degree = Object.fromEntries(g.nodes.map((n) => [n.id, n.degree]));
		expect(degree).toEqual({
			'f:a/one': 3,
			'f:a/two': 2,
			'f:b/one': 2,
			'f:b/lonely': 0,
			'n:ada': 2,
			'n:solo': 1
		});
	});

	it('counts each subject for the text summary, a crossing connection in both', () => {
		expect(g.subjects).toEqual([
			{ id: 'a', title: 'Alpha', frames: 2, connections: 2, names: 2 },
			{ id: 'b', title: 'Beta', frames: 2, connections: 1, names: 1 }
		]);
		expect(g.totals).toEqual({ frames: 4, names: 2, connections: 2, mentions: 3 });
	});

	it('leaves out a mention of a name the registry does not have', () => {
		const g = library3dOf({ ...data, mentions: { ...data.mentions, ghost: ['a/one'] } });
		expect(g.nodes.some((n) => n.id === 'n:ghost')).toBe(false);
		expect(g.links.some((l) => l.target === 'n:ghost')).toBe(false);
	});
});

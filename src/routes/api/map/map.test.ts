import { describe, expect, it } from 'vitest';
import type { MapData } from '$engine/map';
import { GET } from './+server';

describe('the map data', () => {
	it('carries every served subject, their frames, connections and names', async () => {
		const res = await GET({} as never);
		const data = (await res.json()) as MapData;
		expect(data.subjects.map((s) => s.id)).toEqual(
			expect.arrayContaining(['ai', 'computing', 'feynman', 'western-civ'])
		);
		const keys = new Set(data.frames.map((f) => f.key));
		expect(keys.has('western-civ/printing-press')).toBe(true);
		for (const l of data.links) expect(keys.has(l.from) && keys.has(l.to)).toBe(true);
		for (const at of Object.values(data.mentions))
			for (const k of at) expect(keys.has(k)).toBe(true);
		expect(data.mentions['alan-turing'].length).toBeGreaterThan(1);
	});
});

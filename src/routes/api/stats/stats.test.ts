import { describe, expect, it } from 'vitest';
import type { LibraryStats } from '$engine/stats';
import { GET } from './+server';

describe('the library stats', () => {
	it('count every served subject, and sum to the library', async () => {
		const res = await GET({ request: new Request('http://x/') } as never);
		const s = (await res.json()) as LibraryStats;
		expect(s.subjects.map((x) => x.id)).toEqual(
			expect.arrayContaining(['ai', 'computing', 'feynman', 'physics', 'western-civ'])
		);
		for (const x of s.subjects) {
			expect(x.frames, x.id).toBeGreaterThan(0);
			expect(x.words, x.id).toBeGreaterThan(x.frames * 100);
		}
		expect(s.words).toBe(s.subjects.reduce((t, x) => t + x.words, 0));
		expect(s.pages).toBe(Math.round(s.words / s.wordsPerPage));
		expect(s.names).toBeGreaterThan(1000);
	});
});

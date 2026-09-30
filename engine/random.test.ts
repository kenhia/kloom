import { describe, expect, it } from 'vitest';
import type { Spine, Subject } from './model';
import { pickOther, walkedFrames } from './random';

const spine = (...segments: string[][]): Spine => ({
	segments: segments.map((frames, i) => ({
		id: `s${i}`,
		title: `S${i}`,
		labelKind: 'date',
		frames
	}))
});

const subject = {
	id: 'x',
	title: 'X',
	palettes: {},
	spine: spine(['a', 'b'], ['c']),
	trails: [
		{ id: 't', title: 'T', anchor: 'b', spine: spine(['t1', 't2']) },
		{ id: 'u', title: 'U', anchor: 'c', spine: spine(['u1']) }
	],
	// A frame on no spine is not one the reader can reach.
	frames: Object.fromEntries(['a', 'b', 'c', 't1', 't2', 'u1', 'stray'].map((id) => [id, {}]))
} as unknown as Subject;

describe('walkedFrames', () => {
	it('is every frame a spine walks, the main one then the trails', () => {
		expect(walkedFrames(subject)).toEqual(['a', 'b', 'c', 't1', 't2', 'u1']);
	});
});

describe('pickOther', () => {
	it('never picks the current one, even when the draw lands on it', () => {
		// Each draw would be `b` in the whole list; with it left out, never.
		for (const r of [0, 0.2, 0.34, 0.5, 0.67, 0.99])
			expect(pickOther(['a', 'b', 'c'], 'b', () => r)).not.toBe('b');
	});

	it('reaches every other item', () => {
		const items = ['a', 'b', 'c', 'd'];
		const got = new Set([0, 0.34, 0.67, 0.99].map((r) => pickOther(items, 'a', () => r)));
		expect(got).toEqual(new Set(['b', 'c', 'd']));
	});

	it('picks from all of them when the current one is not among them', () => {
		expect(pickOther(['a', 'b'], 'z', () => 0)).toBe('a');
		expect(pickOther(['a', 'b'], null, () => 0.99)).toBe('b');
	});

	it('is null when there is nowhere else to go', () => {
		expect(pickOther(['a'], 'a')).toBeNull();
		expect(pickOther([], null)).toBeNull();
	});
});

import { join } from 'node:path';
import { describe, expect, it } from 'vitest';
import { loadSubject } from './load';
import { RING, startLook } from './start';

const dir = (id: string) => join(import.meta.dirname, '..', 'subjects', id);

describe('a subject’s start look', () => {
	it('opens in its first frame’s palette, one the subject defines', async () => {
		const subject = await loadSubject(dir('western-civ'));
		const look = startLook(subject);
		expect(look.palette).toBe(subject.frames[subject.spine.segments[0].frames[0]].scene.palette);
		expect(look.palettes[look.palette]).toBeDefined();
	});

	it('samples a long subject evenly along the spine, first frame first', async () => {
		const subject = await loadSubject(dir('ai'));
		const first = subject.frames[subject.spine.segments[0].frames[0]];
		const look = startLook(subject);
		expect(look.illustrations).toHaveLength(RING);
		expect(look.illustrations[0]).toBe(first.svg);
		expect(new Set(look.illustrations).size).toBe(RING);
		// Spread out, not the first ten: the sample reaches the last tenth.
		const drawn = subject.spine.segments.flatMap((s) => s.frames);
		const at = drawn.findIndex((id) => subject.frames[id].svg === look.illustrations.at(-1));
		expect(at).toBeGreaterThanOrEqual(Math.floor((drawn.length * (RING - 1)) / RING));
	});

	it('shows every illustration of a subject with fewer than the ring holds', async () => {
		const subject = await loadSubject(dir('western-civ'));
		expect(startLook(subject, 1000).illustrations).toHaveLength(
			subject.spine.segments.flatMap((s) => s.frames).length
		);
	});
});

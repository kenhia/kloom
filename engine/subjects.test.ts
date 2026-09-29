import { readdirSync } from 'node:fs';
import { join } from 'node:path';
import { describe, expect, it } from 'vitest';
import { loadSubject, readSubject } from './load';
import { validate } from './validate';

/**
 * Every subject in the repo loads and validates: the gate an author (or a
 * grow job) runs after each segment. Subject-specific checks live beside
 * this, one describe per subject.
 */
// KLOOM_TEST_SUBJECTS points at another directory of subjects: a copy holding only
// finished frames, from subject_plan.py --complete, while authors are mid-write.
const root = process.env.KLOOM_TEST_SUBJECTS || join(import.meta.dirname, '..', 'subjects');
const subjects = readdirSync(root, { withFileTypes: true })
	.filter((d) => d.isDirectory() && !d.name.startsWith('.'))
	.map((d) => d.name);

describe.each(subjects)('the %s subject', (id) => {
	const dir = join(root, id);

	it('is valid', async () => {
		expect(validate(await readSubject(dir))).toEqual([]);
	});

	it('inlines every illustration, and cites every frame with Wikipedia pinned', async () => {
		const subject = await loadSubject(dir);
		for (const frame of Object.values(subject.frames)) {
			expect(frame.svg, frame.id).toMatch(/^<svg/);
			expect(frame.citations?.length, frame.id).toBeGreaterThan(0);
			for (const c of frame.citations!)
				if (c.kind === 'wikipedia') expect(c.url, frame.id).toMatch(/oldid=\d+$/);
		}
	});
});

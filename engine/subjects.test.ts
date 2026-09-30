import { readdirSync } from 'node:fs';
import { join } from 'node:path';
import { beforeAll, describe, expect, it } from 'vitest';
import { buildGraph, graphProblems } from './graph';
import { loadNames, loadSubject, readGraphSubject, readSubject } from './load';
import type { Name } from './names';
import { validate } from './validate';

/**
 * Every subject in the repo loads and validates: the gate an author (or a
 * grow job) runs after each segment. Subject-specific checks live beside
 * this, one describe per subject. The name registry beside the subjects
 * validates too, and so do the links between them.
 */
// KLOOM_TEST_SUBJECTS points at another directory of subjects: a copy holding only
// finished frames, from subject_plan.py --complete, while authors are mid-write.
const root = process.env.KLOOM_TEST_SUBJECTS || join(import.meta.dirname, '..', 'subjects');
// KLOOM_TEST_NAMES is that copy's registry (DIR/.names), with the author's drafts in it.
const namesDir = process.env.KLOOM_TEST_NAMES || join(root, '..', 'names');
const subjects = readdirSync(root, { withFileTypes: true })
	.filter((d) => d.isDirectory() && !d.name.startsWith('.'))
	.map((d) => d.name);

let registry: Record<string, Name>;
beforeAll(async () => {
	({ names: registry } = await loadNames(namesDir));
});

describe('the name registry', () => {
	it('is valid', async () => {
		expect((await loadNames(namesDir)).problems).toEqual([]);
	});
});

describe.each(subjects)('the %s subject', (id) => {
	const dir = join(root, id);

	it('is valid, with no warnings', async () => {
		// Validation only warns about a repeated name mark, which renders as its
		// words; the repository's own content is held to it, as svelte-check's
		// warnings are.
		const warnings: string[] = [];
		const names = new Set(Object.keys(registry));
		expect(validate(await readSubject(dir), { names, warnings })).toEqual([]);
		expect(warnings).toEqual([]);
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

describe('the links between subjects', () => {
	it('all find their frames, and none is stored twice', async () => {
		const graph = buildGraph(
			await Promise.all(subjects.map((id) => readGraphSubject(join(root, id)))),
			registry
		);
		expect(graphProblems(graph)).toEqual([]);
	});
});

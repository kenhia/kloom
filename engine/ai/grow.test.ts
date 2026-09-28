import { cp, mkdtemp, rm, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { beforeEach, describe, expect, it } from 'vitest';
import { readSubject } from '../load';
import type { Spine, Trail } from '../model';
import type { RawSubject } from '../validate';
import { growPrompt, growthProblems, repairPrompt, type GrownFiles } from './grow';
import { editJson, grownFrame, writeFrame } from './grow-fixture';

const source = join(import.meta.dirname, '..', '..', 'subjects', 'western-civ');

let dir: string;
let before: RawSubject;
beforeEach(async () => {
	dir = await mkdtemp(join(tmpdir(), 'kloom-growth-'));
	await cp(source, dir, { recursive: true });
	before = await readSubject(dir);
});

/** Add a frame to the main spine's rebirth segment, before shakespeare. */
async function addMainFrame(id = 'luther-theses', sort = 1540) {
	await writeFrame(dir, id, grownFrame(id, sort));
	await editJson<Spine>(join(dir, 'spine.json'), (s) => {
		const seg = s.segments.find((x) => x.id === 'rebirth')!;
		seg.frames.splice(seg.frames.indexOf('shakespeare'), 0, id);
	});
}

async function addTrail(id: string, anchor: string, frames: string[]) {
	for (const [i, f] of frames.entries()) await writeFrame(dir, f, grownFrame(f, 1520 + i));
	await writeFile(
		join(dir, 'trails', `${id}.json`),
		JSON.stringify({
			id,
			title: 'A trail',
			anchor,
			spine: { segments: [{ id: 'one', title: 'One', labelKind: 'date', frames }] }
		})
	);
}

async function check(verb: 'frames' | 'trail' | 'both', anchor = 'printing-press') {
	const after = await readSubject(dir);
	const files: GrownFiles = {};
	for (const id of Object.keys(after.frames))
		if (!(id in before.frames)) files[id] = { ...grownFrame(id, 0), ...(extra[id] ?? {}) };
	return growthProblems(before, after, files, verb, anchor);
}
let extra: GrownFiles = {};
beforeEach(() => {
	extra = {};
});

describe('what a grow job may change', () => {
	it('takes a new main-spine frame, and reports what it added', async () => {
		await addMainFrame();
		const { problems, growth } = await check('frames');
		expect(problems).toEqual([]);
		expect(growth).toEqual({ frames: ['luther-theses'], trailFrames: [], trails: [] });
	});

	it('takes a trail from the anchor', async () => {
		await addTrail('reformation', 'printing-press', ['wittenberg', 'worms']);
		const { problems, growth } = await check('trail');
		expect(problems).toEqual([]);
		expect(growth).toEqual({
			frames: [],
			trailFrames: ['wittenberg', 'worms'],
			trails: ['reformation']
		});
	});

	it('takes an existing trail extended from the anchor', async () => {
		await writeFrame(dir, 'fust-lawsuit', grownFrame('fust-lawsuit', 1460));
		await editJson<Trail>(join(dir, 'trails', 'printing.json'), (t) =>
			t.spine.segments[0].frames.push('fust-lawsuit')
		);
		const { problems, growth } = await check('trail');
		expect(problems).toEqual([]);
		expect(growth.trails).toEqual(['printing']);
	});

	it('takes a new frame with its own trail', async () => {
		await addMainFrame();
		await addTrail('reformation', 'luther-theses', ['wittenberg']);
		expect((await check('both')).problems).toEqual([]);
	});

	it('refuses a change to an existing frame, the manifest, or the order', async () => {
		await addMainFrame();
		await editJson<{ scene: { accent: string } }>(
			join(dir, 'frames', 'steam', 'frame.json'),
			(f) => (f.scene.accent = 'STEAM.')
		);
		await editJson<{ title: string }>(join(dir, 'subject.json'), (m) => (m.title = 'Other'));
		await editJson<Spine>(join(dir, 'spine.json'), (s) => s.segments[1].frames.reverse());
		expect((await check('frames')).problems).toEqual([
			'subject.json: must not change',
			'frames/steam: an existing frame was changed',
			'spine.json: existing frames must all stay, in their order'
		]);
	});

	it('refuses a removed frame, segment or trail', async () => {
		await addMainFrame();
		await rm(join(dir, 'trails', 'printing.json'));
		await editJson<Spine>(join(dir, 'spine.json'), (s) => s.segments.pop());
		const { problems } = await check('frames');
		expect(problems).toContain('spine.json: existing frames must all stay, in their order');
		expect(problems).toContain('spine.json: segment "code-and-cosmos" was removed');
		expect(problems).toContain('trails/printing.json: an existing trail was removed');
	});

	it('refuses odd files, oversized files and unsafe drawings in a new frame', async () => {
		await addMainFrame();
		extra = {
			'luther-theses': {
				'run.sh': 'rm -rf /',
				'reading.md': 'x'.repeat(200_001),
				'chart.svg': '<svg><script>alert(1)</script></svg>'
			}
		};
		expect((await check('frames')).problems).toEqual([
			'frames/luther-theses/reading.md: is too large',
			'frames/luther-theses: "run.sh" is not a file grow may write (frame.json, reading.md, *.svg)',
			'frames/luther-theses/chart.svg: <script> is not allowed in an illustration'
		]);
	});

	it('holds each verb to what it says', async () => {
		expect((await check('frames')).problems).toEqual(['the job added no frames']);
		await addTrail('reformation', 'printing-press', ['wittenberg']);
		expect((await check('frames')).problems).toEqual([
			'verb frames: no new frame is on the main spine',
			'verb frames: trails must not change'
		]);
		expect((await check('trail', 'steam')).problems).toEqual([
			'verb trail: every trail it adds or extends must branch from "steam"'
		]);
		expect((await check('both')).problems).toEqual([
			'verb both: add exactly one new main-spine frame',
			'verb both: add a trail branching from the new frame'
		]);
		await addMainFrame();
		expect((await check('trail')).problems).toContain('verb trail: the main spine must not change');
	});
});

describe('the grow prompt', () => {
	it('names the verb, the anchor, the kept answer and the request', () => {
		const p = growPrompt(
			{ verb: 'trail', request: 'The Reformation', kept: '20260927T170509Z-0a1b2c3d', web: true },
			'Western Civ',
			{
				id: 'printing-press',
				title: 'Knowledge went VIRAL.',
				position: 'c. AD 1440',
				on: 'the main spine'
			},
			'2026-09-27'
		);
		expect(p).toContain('Verb: trail. Add a side trail');
		expect(p).toContain('Anchor frame: printing-press — "Knowledge went VIRAL."');
		expect(p).toContain('request/kept-answer.json');
		expect(p).toContain('WebSearch and WebFetch');
		expect(p.endsWith('The Reformation')).toBe(true);
		expect(repairPrompt(['a: b'])).toContain('- a: b');
	});
});

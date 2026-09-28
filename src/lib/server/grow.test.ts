import { execFileSync } from 'node:child_process';
import { cp, mkdtemp, readdir, readFile, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { beforeEach, describe, expect, it } from 'vitest';
import { editJson, grownFrame, writeFrame } from '$engine/ai/grow-fixture';
import type { GrowJob } from '$engine/ai/grow';
import type { GrowRequest, Provider, ProviderEvent } from '$engine/ai/provider';
import { loadSubject } from '$engine/load';
import type { Spine } from '$engine/model';
import { commitMessage, GrowQueue, runGrowJob, stripFrontmatter, type GrowHost } from './grow';

const source = join(import.meta.dirname, '..', '..', '..', 'subjects', 'western-civ');
const git = (cwd: string, ...args: string[]) =>
	execFileSync('git', args, { cwd, encoding: 'utf8' }).trim();

let repo: string;
let subject: string;
beforeEach(async () => {
	repo = await mkdtemp(join(tmpdir(), 'kloom-grow-repo-'));
	subject = join(repo, 'subjects', 'western-civ');
	await cp(source, subject, { recursive: true });
	git(repo, 'init', '-q', '-b', 'main');
	git(repo, 'add', '.');
	git(repo, '-c', 'user.name=t', '-c', 'user.email=t@t', 'commit', '-q', '-m', 'start');
});

/** A model that runs `turns[n]` over the working directory on its nth turn. */
function fakeProvider(...turns: ((req: GrowRequest) => Promise<void>)[]) {
	const requests: GrowRequest[] = [];
	const provider: Provider = {
		name: 'fake',
		// eslint-disable-next-line require-yield
		async *ask() {
			throw new Error('grow only');
		},
		async *grow(req): AsyncIterable<ProviderEvent> {
			requests.push(req);
			yield { type: 'status', status: 'writing' };
			await turns[requests.length - 1](req);
			yield { type: 'text', text: 'Added a frame on Luther.' };
		}
	};
	return { provider, requests };
}

/** What a well-behaved model does for "frames": one frame, before shakespeare. */
const addLuther =
	(sort = 1540) =>
	async ({ workDir }: GrowRequest) => {
		await writeFrame(workDir, 'luther-theses', grownFrame('luther-theses', sort));
		await editJson<Spine>(join(workDir, 'spine.json'), (s) => {
			const seg = s.segments.find((x) => x.id === 'rebirth')!;
			seg.frames.splice(seg.frames.indexOf('shakespeare'), 0, 'luther-theses');
		});
	};

const job = (over: Partial<GrowJob> = {}): GrowJob => ({
	kind: 'kloom.grow-job',
	version: 1,
	id: '20260927T180000Z-0a1b2c3d',
	subject: 'western-civ',
	verb: 'frames',
	anchor: 'printing-press',
	request: 'Luther and the theses',
	kept: null,
	provider: 'fake',
	model: 'claude-opus-5-5',
	web: false,
	status: 'running',
	attempts: 1,
	queuedAt: '2026-09-27T18:00:00.000Z',
	...over
});

const host = (provider: Provider, over: Partial<GrowHost> = {}): GrowHost => ({
	subjectDir: subject,
	provider,
	instructions: '---\nname: x\n---\n\n# Growing',
	reference: { 'design.md': join(source, '..', '..', 'docs', 'design.md') },
	timeoutMs: 60_000,
	...over
});

const log = () => git(repo, 'log', '--format=%an <%ae>%n%B', '-1');

describe('a grow job', () => {
	it('works on a copy, then writes and commits only the new content', async () => {
		const { provider, requests } = fakeProvider(addLuther());
		const progress: string[] = [];
		const outcome = await runGrowJob(job(), host(provider), (p) => progress.push(p));
		expect(outcome).toMatchObject({
			ok: true,
			result: { frames: ['luther-theses'], trails: [], summary: 'Added a frame on Luther.' }
		});
		// The model worked elsewhere, with the instructions and the references.
		const req = requests[0];
		expect(req.workDir.startsWith(subject)).toBe(false);
		expect(req.instructions).toBe('# Growing');
		expect(req.prompt).toContain('Anchor frame: printing-press');
		expect(req.model).toBe('claude-opus-5-5');
		// Committed as grow, naming the job and model, with exactly these paths.
		expect(log()).toContain('kloom grow <grow@kloom.local>');
		expect(log()).toContain('grow(western-civ): add luther-theses');
		expect(log()).toContain('Model: claude-opus-5-5 (fake)');
		expect(git(repo, 'show', '--name-only', '--format=', 'HEAD').split('\n').sort()).toEqual([
			'subjects/western-civ/frames/luther-theses/frame.json',
			'subjects/western-civ/frames/luther-theses/reading.md',
			'subjects/western-civ/frames/luther-theses/scene.svg',
			'subjects/western-civ/spine.json'
		]);
		expect(git(repo, 'status', '--porcelain')).toBe('');
		expect(outcome.ok && outcome.result.commit).toBe(git(repo, 'rev-parse', 'HEAD'));
		// And the site serves it.
		expect((await loadSubject(subject)).frames['luther-theses'].scene.accent).toBe('THESES.');
		expect(progress).toEqual(['starting', 'writing', 'committing']);
	});

	it('formats what it writes with the repo’s Prettier config', async () => {
		// The subject's own repo config applies (kloom's: tabs, width 100).
		await writeFile(join(repo, '.prettierrc'), '{"useTabs": true, "printWidth": 100}');
		git(repo, 'add', '.prettierrc');
		git(repo, '-c', 'user.name=t', '-c', 'user.email=t@t', 'commit', '-qm', 'config');
		const { provider } = fakeProvider(async (req) => {
			await addLuther()(req);
			const reading = join(req.workDir, 'frames', 'luther-theses', 'reading.md');
			await writeFile(reading, 'A line that\nwraps early.\n\n* a star bullet\n');
			// Minified JSON, as a model might write it.
			const frame = join(req.workDir, 'frames', 'luther-theses', 'frame.json');
			await writeFile(frame, JSON.stringify(JSON.parse(await readFile(frame, 'utf8'))));
		});
		expect((await runGrowJob(job(), host(provider))).ok).toBe(true);
		const dir = join(subject, 'frames', 'luther-theses');
		expect(await readFile(join(dir, 'reading.md'), 'utf8')).toBe(
			'A line that\nwraps early.\n\n- a star bullet\n'
		);
		expect(await readFile(join(dir, 'frame.json'), 'utf8')).toContain('\n\t"position": {');
	});

	it('gives the model one turn to fix what the validator found', async () => {
		// First turn: out of date order. Second: fixed.
		const { provider, requests } = fakeProvider(addLuther(1400), async ({ workDir }) =>
			editJson<{ position: { sort: number } }>(
				join(workDir, 'frames', 'luther-theses', 'frame.json'),
				(f) => (f.position.sort = 1540)
			)
		);
		const outcome = await runGrowJob(job(), host(provider));
		expect(outcome.ok).toBe(true);
		expect(requests[1].prompt).toContain('is out of order');
	});

	it('leaves no commit and no files when validation still fails', async () => {
		const head = git(repo, 'rev-parse', 'HEAD');
		const { provider } = fakeProvider(addLuther(1400), async () => {});
		const outcome = await runGrowJob(job(), host(provider));
		expect(outcome).toMatchObject({ ok: false, error: expect.stringContaining('did not pass') });
		expect(!outcome.ok && outcome.problems?.join('\n')).toContain('out of order');
		expect(git(repo, 'rev-parse', 'HEAD')).toBe(head);
		expect(git(repo, 'status', '--porcelain')).toBe('');
	});

	it('reports a model error, and writes nothing', async () => {
		const provider: Provider = {
			name: 'fake',
			// eslint-disable-next-line require-yield
			async *ask() {
				throw new Error('grow only');
			},
			async *grow() {
				yield { type: 'error', message: 'The model took longer than 900s.' };
			}
		};
		expect(await runGrowJob(job(), host(provider))).toEqual({
			ok: false,
			error: 'The model took longer than 900s.'
		});
		expect(git(repo, 'status', '--porcelain')).toBe('');
	});

	it('refuses to apply over uncommitted changes, or a subject that changed meanwhile', async () => {
		await writeFile(join(subject, 'frames', 'steam', 'reading.md'), 'edited by hand\n');
		const dirty = await runGrowJob(job(), host(fakeProvider(addLuther()).provider));
		expect(dirty).toMatchObject({ ok: false, error: expect.stringContaining('uncommitted') });
		git(repo, 'checkout', '--', '.');

		const changing = fakeProvider(async (req) => {
			await addLuther()(req);
			// Someone commits to the subject while the model works.
			await writeFile(join(subject, 'frames', 'steam', 'reading.md'), 'a new reading\n');
			git(repo, '-c', 'user.name=t', '-c', 'user.email=t@t', 'commit', '-qam', 'edit');
		});
		const stale = await runGrowJob(job(), host(changing.provider));
		expect(stale).toMatchObject({ ok: false, error: expect.stringContaining('changed while') });
		expect(await readdir(join(subject, 'frames'))).not.toContain('luther-theses');
	});

	it('takes everything back out if the commit fails', async () => {
		const head = git(repo, 'rev-parse', 'HEAD');
		const spine = await readFile(join(subject, 'spine.json'), 'utf8');
		const { provider } = fakeProvider(async (req) => {
			await addLuther()(req);
			// git refuses to add while another process holds the index.
			await writeFile(join(repo, '.git', 'index.lock'), '');
		});
		const outcome = await runGrowJob(job(), host(provider));
		expect(outcome).toMatchObject({ ok: false, error: expect.stringContaining('taken back out') });
		expect(git(repo, 'rev-parse', 'HEAD')).toBe(head);
		expect(await readFile(join(subject, 'spine.json'), 'utf8')).toBe(spine);
		expect(await readdir(join(subject, 'frames'))).not.toContain('luther-theses');
	});

	it('writes the commit message from the job', () => {
		const msg = commitMessage(
			job({ verb: 'both', kept: '20260927T170509Z-0a1b2c3d', web: true }),
			'western-civ',
			{ frames: ['luther-theses'], trailFrames: ['worms'], trails: ['reformation'] },
			'Added Luther.'
		);
		expect(msg.split('\n')[0]).toBe(
			'grow(western-civ): add luther-theses, worms; trail reformation'
		);
		expect(msg).toContain('Kept answer: 20260927T170509Z-0a1b2c3d');
		expect(msg).toContain('Web: yes');
		expect(stripFrontmatter('---\na: b\n---\n\nBody')).toBe('Body');
	});
});

describe('the grow queue', () => {
	const fields = {
		subject: 'western-civ',
		verb: 'frames' as const,
		anchor: 'printing-press',
		request: 'x',
		kept: null,
		provider: 'fake',
		model: 'm',
		web: false
	};

	it('runs jobs one at a time, in order, and records the outcome on disk', async () => {
		const dir = await mkdtemp(join(tmpdir(), 'kloom-grow-jobs-'));
		const order: string[] = [];
		let running = 0;
		const queue = new GrowQueue(dir, async (j, progress) => {
			running++;
			expect(running).toBe(1);
			progress('writing');
			await new Promise((r) => setTimeout(r, 5));
			order.push(j.request);
			running--;
			return j.request === 'b'
				? { ok: false, error: 'no', problems: ['p'] }
				: { ok: true, result: { frames: ['f'], trails: [], commit: 'abc', summary: 's' } };
		});
		const a = await queue.add({ ...fields, request: 'a' });
		await queue.add({ ...fields, request: 'b' });
		await queue.idle();
		expect(order).toEqual(['a', 'b']);
		const saved = JSON.parse(await readFile(join(dir, `${a.id}.json`), 'utf8')) as GrowJob;
		expect(saved).toMatchObject({ status: 'done', attempts: 1, result: { commit: 'abc' } });
		expect(saved).not.toHaveProperty('progress');
		expect(queue.list().map((j) => j.status)).toEqual(['failed', 'done']);
		expect(queue.list()[0]).toMatchObject({ error: 'no', problems: ['p'] });
	});

	it('refuses a job past the limit', async () => {
		const dir = await mkdtemp(join(tmpdir(), 'kloom-grow-jobs-'));
		let release!: () => void;
		const gate = new Promise<void>((r) => (release = r));
		const queue = new GrowQueue(dir, async () => (await gate, { ok: false, error: 'x' }), 1);
		await queue.add(fields); // running
		await queue.add(fields); // waiting
		await expect(queue.add(fields)).rejects.toThrow('Too many');
		release();
		await queue.idle();
	});

	it('picks up after a restart: re-runs a running job once, fails an applying one', async () => {
		const dir = await mkdtemp(join(tmpdir(), 'kloom-grow-jobs-'));
		const persisted = (id: string, status: GrowJob['status'], attempts: number) =>
			writeFile(
				join(dir, `${id}.json`),
				JSON.stringify(job({ id, status, attempts, request: id }))
			);
		await persisted('20260927T180001Z-00000001', 'running', 1);
		await persisted('20260927T180002Z-00000002', 'running', 2);
		await persisted('20260927T180003Z-00000003', 'applying', 1);
		await persisted('20260927T180004Z-00000004', 'queued', 0);
		const ran: string[] = [];
		const queue = new GrowQueue(dir, async (j) => {
			ran.push(j.request);
			return { ok: true, result: { frames: [], trails: [], commit: null, summary: '' } };
		});
		await queue.load();
		await queue.idle();
		expect(ran).toEqual(['20260927T180001Z-00000001', '20260927T180004Z-00000004']);
		const status = (id: string) => queue.get(id)!;
		expect(status('20260927T180001Z-00000001')).toMatchObject({ status: 'done', attempts: 2 });
		expect(status('20260927T180002Z-00000002')).toMatchObject({
			status: 'failed',
			error: expect.stringContaining('twice')
		});
		expect(status('20260927T180003Z-00000003')).toMatchObject({
			status: 'failed',
			error: expect.stringContaining('check git status')
		});
	});
});

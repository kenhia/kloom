import { execFile } from 'node:child_process';
import { randomBytes } from 'node:crypto';
import { cp, mkdir, mkdtemp, readdir, readFile, rename, rm, writeFile } from 'node:fs/promises';
import { homedir, tmpdir } from 'node:os';
import { basename, dirname, join, relative, resolve } from 'node:path';
import { isDeepStrictEqual, promisify } from 'node:util';
import {
	growPrompt,
	growthProblems,
	repairPrompt,
	type GrowAnchor,
	type GrownFiles,
	type Growth,
	type GrowJob
} from '$engine/ai/grow';
import { answerId } from '$engine/ai/kept';
import type { Provider, ProviderStatus } from '$engine/ai/provider';
import { readSubject } from '$engine/load';
import type { Spine, Trail } from '$engine/model';
import { validate, type RawSubject } from '$engine/validate';

/**
 * The host side of grow (docs/design.md §Grow): the persisted queue, the
 * working copy, the model turns, the checks, and the commit.
 *
 * A job never touches the subject until the end. The model works on a copy
 * in a directory of its own, outside the home directory; what it leaves
 * there must be a clean addition (`growthProblems`) and a valid subject
 * (`validate`). Only then are the new files written into the subject and
 * committed. A failure at any point leaves the subject and git as they were.
 */

const run = promisify(execFile);

/** Who grow commits as; a job's requester, when it has one, is the author. */
export const GROW_AUTHOR = { name: 'kloom grow', email: 'grow@kloom.local' };

/** `Name <login>` for git, with nothing in it that could break the ident. */
export const requester = (by: NonNullable<GrowJob['by']>) => {
	const clean = (s: string) => s.replace(/[<>\n\r]/g, '').trim();
	return `${clean(by.name) || clean(by.login)} <${clean(by.login)}>`;
};

/** Status text for the AI pane. */
const DOING: Record<ProviderStatus, string> = {
	searching: 'searching the web',
	reading: 'reading the subject',
	writing: 'writing'
};

/** What a job needs from the host; tests pass their own. */
export interface GrowHost {
	/** The live subject directory, `subjects/<subject>`. */
	subjectDir: string;
	provider: Provider;
	/** skills/grow/SKILL.md, frontmatter included; it is stripped here. */
	instructions: string;
	/** Files copied into the job's `reference/`, by name there. */
	reference: Record<string, string>;
	/** Kept answer JSON, when the job turns one into content. */
	kept?: unknown;
	timeoutMs: number;
	/** Where job directories go; must not be under the home directory. */
	workRoot?: string;
	/** The name registry's ids: a grown reading may mark only these (§Connections). */
	names?: ReadonlySet<string>;
	/** Runs while the subject's files are rewritten, so no reader sees them half-written. */
	exclusive?: <T>(fn: () => Promise<T>) => Promise<T>;
	now?: () => Date;
	signal?: AbortSignal;
}

/** A job's outcome: its result, or why it failed. */
export type GrowOutcome =
	| { ok: true; result: NonNullable<GrowJob['result']> }
	| { ok: false; error: string; problems?: string[] };

export const stripFrontmatter = (md: string) => md.replace(/^---\n[\s\S]*?\n---\n+/, '');

const git = async (cwd: string, args: string[]) =>
	(await run('git', args, { cwd, maxBuffer: 1 << 20 })).stdout.trim();

/** Where the anchor sits: the main spine, or which trail. */
function anchorOf(raw: RawSubject, id: string): GrowAnchor | null {
	const frame = raw.frames[id]?.frame as
		{ position?: { label?: string }; scene?: { headline?: string; accent?: string } } | undefined;
	if (!frame) return null;
	const onTrail = Object.values(raw.trails as Record<string, Trail>).find((t) =>
		t.spine.segments.some((s) => s.frames.includes(id))
	);
	return {
		id,
		title: `${frame.scene?.headline ?? ''} ${frame.scene?.accent ?? ''}`.trim(),
		position: frame.position?.label ?? '',
		on: onTrail ? `the trail "${onTrail.title}"` : 'the main spine'
	};
}

/** The files in each new frame directory of the working copy. */
async function grownFiles(work: string, ids: string[]): Promise<GrownFiles> {
	const out: GrownFiles = {};
	for (const id of ids) {
		out[id] = {};
		for (const e of await readdir(join(work, 'frames', id), { withFileTypes: true }))
			out[id][e.name] = e.isFile() ? await readFile(join(work, 'frames', id, e.name), 'utf8') : '';
	}
	return out;
}

/** Everything wrong with the working copy, and what it added. */
async function check(
	work: string,
	before: RawSubject,
	job: GrowJob,
	names?: ReadonlySet<string>
): Promise<{ problems: string[]; growth: Growth; after: RawSubject | null }> {
	let after: RawSubject;
	try {
		after = await readSubject(work);
	} catch (e) {
		const empty = { frames: [], trailFrames: [], trails: [] };
		return { problems: [(e as Error).message.replace(work + '/', '')], growth: empty, after: null };
	}
	const added = Object.keys(after.frames).filter((id) => !(id in before.frames));
	const { problems, growth } = growthProblems(
		before,
		after,
		await grownFiles(work, added),
		job.verb,
		job.anchor
	);
	// A grown reading may mark only names the registry has (§Connections).
	return {
		problems: [...problems, ...validate(after, { names })],
		growth,
		after
	};
}

/**
 * Run one job to its end: copy the subject, let the model work (with one
 * repair turn if the first leaves problems), check, then apply and commit.
 */
export async function runGrowJob(
	job: GrowJob,
	host: GrowHost,
	progress: (text: string) => void = () => {}
): Promise<GrowOutcome> {
	const root = host.workRoot ?? tmpdir();
	if (!relative(homedir(), resolve(root)).startsWith('..'))
		return { ok: false, error: `The grow work directory ${root} is inside the home directory.` };
	const work = await mkdtemp(join(root, `kloom-grow-${job.id}-`));
	let keep = false;
	try {
		for (const f of ['subject.json', 'spine.json', 'trails', 'frames'])
			await cp(join(host.subjectDir, f), join(work, f), { recursive: true }).catch((e) => {
				if (f !== 'trails' || e.code !== 'ENOENT') throw e;
			});
		for (const [name, from] of Object.entries(host.reference)) {
			await mkdir(dirname(join(work, 'reference', name)), { recursive: true });
			await cp(from, join(work, 'reference', name));
		}
		if (host.kept !== undefined) {
			await mkdir(join(work, 'request'), { recursive: true });
			await writeFile(
				join(work, 'request', 'kept-answer.json'),
				JSON.stringify(host.kept, null, '\t')
			);
		}

		const before = await readSubject(work);
		const anchor = anchorOf(before, job.anchor);
		if (!anchor) return { ok: false, error: `The frame "${job.anchor}" is gone.` };
		const subjectTitle = (before.manifest as { title: string }).title;
		const today = (host.now?.() ?? new Date()).toISOString().slice(0, 10);

		let prompt = growPrompt(job, subjectTitle, anchor, today);
		let summary = '';
		let checked: Awaited<ReturnType<typeof check>> | null = null;
		for (let turn = 1; turn <= 2; turn++) {
			progress(turn === 1 ? 'starting' : 'fixing what the validator found');
			summary = '';
			for await (const event of host.provider.grow({
				workDir: work,
				instructions: stripFrontmatter(host.instructions),
				prompt,
				model: job.model,
				web: job.web,
				timeoutMs: host.timeoutMs,
				signal: host.signal
			})) {
				if (event.type === 'error') {
					keep = true;
					return { ok: false, error: event.message };
				}
				if (event.type === 'status') progress(DOING[event.status]);
				else summary += event.text;
			}
			if (host.signal?.aborted) return { ok: false, error: 'Stopped.' };
			checked = await check(work, before, job, host.names);
			if (checked.problems.length === 0) break;
			prompt = repairPrompt(checked.problems);
		}
		if (!checked || checked.problems.length) {
			keep = true;
			return {
				ok: false,
				error: `What the model wrote did not pass validation, so nothing was kept (work left in ${work}).`,
				problems: checked?.problems.slice(0, 20)
			};
		}

		await formatGrown(work, host.subjectDir, checked.growth);
		progress('committing');
		const apply = () =>
			applyGrowth(job, host.subjectDir, work, before, checked!.after!, checked!.growth, summary);
		const commit = await (host.exclusive ? host.exclusive(apply) : apply());
		return {
			ok: true,
			result: {
				frames: [...checked.growth.frames, ...checked.growth.trailFrames],
				trails: checked.growth.trails,
				commit,
				summary: summary.trim().slice(0, 1000)
			}
		};
	} catch (e) {
		keep = true;
		return { ok: false, error: (e as Error).message };
	} finally {
		if (!keep) await rm(work, { recursive: true, force: true });
	}
}

/** The model's account, trimmed: some models narrate their whole check. */
const clipSummary = (s: string, n = 2000) =>
	s.trim().length > n ? `${s.trim().slice(0, n).trimEnd()}…` : s.trim();

/**
 * Format the JSON and Markdown a job wrote with the repo's own Prettier
 * config, so a grow commit passes the same `just check` as a hand-written
 * one. Prettier is a dev dependency; where it is not installed, this is
 * skipped and the content is still valid.
 */
export async function formatGrown(work: string, subjectDir: string, growth: Growth) {
	let prettier: typeof import('prettier');
	try {
		prettier = await import('prettier');
	} catch {
		return;
	}
	const files = [
		'spine.json',
		...growth.trails.map((id) => join('trails', `${id}.json`)),
		...[...growth.frames, ...growth.trailFrames].flatMap((id) => [
			join('frames', id, 'frame.json'),
			join('frames', id, 'reading.md')
		])
	];
	for (const f of files) {
		const path = join(work, f);
		const text = await readFile(path, 'utf8').catch(() => null);
		if (text === null) continue;
		// Resolved as if the file were already in the subject, so the repo's config applies.
		const options = (await prettier.resolveConfig(join(subjectDir, f))) ?? {};
		await writeFile(path, await prettier.format(text, { ...options, filepath: path }));
	}
}

/** The commit message: what was added, by which job, model and request. */
export function commitMessage(job: GrowJob, subject: string, growth: Growth, summary: string) {
	const added = [...growth.frames, ...growth.trailFrames];
	const title = `grow(${subject}): add ${added.join(', ')}${growth.trails.length ? `; trail ${growth.trails.join(', ')}` : ''}`;
	return [
		title.length > 100 ? `${title.slice(0, 99)}…` : title,
		'',
		clipSummary(summary) || 'A grow job wrote this content.',
		'',
		`Job: ${job.id}`,
		`Verb: ${job.verb}`,
		`Anchor: ${job.anchor}`,
		...(job.request.trim()
			? [`Request: ${job.request.trim().replace(/\s+/g, ' ').slice(0, 500)}`]
			: []),
		...(job.kept ? [`Kept answer: ${job.kept}`] : []),
		`Model: ${job.model} (${job.provider})`,
		`Web: ${job.web ? 'yes' : 'no'}`,
		...(job.by ? [`Requested-by: ${requester(job.by)} (${job.by.via})`] : [])
	].join('\n');
}

/**
 * Write the growth into the live subject and commit exactly those paths.
 * Refuses if the subject changed since the job copied it, or has uncommitted
 * changes of its own; on any failure, puts every file back. Returns the
 * commit's hash.
 */
async function applyGrowth(
	job: GrowJob,
	subjectDir: string,
	work: string,
	before: RawSubject,
	after: RawSubject,
	growth: Growth,
	summary: string
): Promise<string> {
	let repo: string;
	try {
		repo = await git(subjectDir, ['rev-parse', '--show-toplevel']);
	} catch {
		throw new Error('The subject is not in a git repository, so grow cannot commit to it.');
	}
	if (await git(subjectDir, ['status', '--porcelain', '--', '.']))
		throw new Error(
			'The subject has uncommitted changes; commit or discard them, then grow again.'
		);
	if (!isDeepStrictEqual(await readSubject(subjectDir), before))
		throw new Error('The subject changed while this job ran; queue it again.');

	const newFrames = [...growth.frames, ...growth.trailFrames];
	const trailFiles = growth.trails.map((id) => join('trails', `${id}.json`));
	const spineChanged = !isDeepStrictEqual(before.spine, after.spine);
	const files = [...trailFiles, ...(spineChanged ? ['spine.json'] : [])];
	const saved = new Map<string, string | null>();
	for (const f of files)
		saved.set(f, await readFile(join(subjectDir, f), 'utf8').catch(() => null));

	const paths = [...newFrames.map((id) => join('frames', id)), ...files];
	const inRepo = paths.map((p) => relative(repo, join(subjectDir, p)));
	try {
		for (const id of newFrames) {
			// Staged beside the subject, then renamed in: a frame appears whole.
			const staged = join(subjectDir, 'frames', `.grow-${id}`);
			await cp(join(work, 'frames', id), staged, { recursive: true });
			await rename(staged, join(subjectDir, 'frames', id));
		}
		await mkdir(join(subjectDir, 'trails'), { recursive: true });
		for (const f of files) {
			const tmp = join(subjectDir, `${f}.grow-tmp`);
			await cp(join(work, f), tmp);
			await rename(tmp, join(subjectDir, f));
		}
		const who = ['-c', `user.name=${GROW_AUTHOR.name}`, '-c', `user.email=${GROW_AUTHOR.email}`];
		await git(repo, ['add', '--', ...inRepo]);
		await git(repo, [
			...who,
			'commit',
			'--quiet',
			'--no-verify',
			...(job.by ? [`--author=${requester(job.by)}`] : []),
			'-m',
			commitMessage(job, basename(subjectDir), growth, summary),
			'--',
			...inRepo
		]);
		return await git(repo, ['rev-parse', 'HEAD']);
	} catch (e) {
		await git(repo, ['reset', '--quiet', '--', ...inRepo]).catch(() => {});
		for (const id of newFrames) {
			await rm(join(subjectDir, 'frames', id), { recursive: true, force: true });
			await rm(join(subjectDir, 'frames', `.grow-${id}`), { recursive: true, force: true });
		}
		for (const [f, text] of saved)
			if (text === null) await rm(join(subjectDir, f), { force: true });
			else await writeFile(join(subjectDir, f), text);
		throw new Error(
			`Could not commit the new content, so it was taken back out: ${(e as Error).message}`,
			{ cause: e }
		);
	}
}

/** Main-spine frame ids, for checking a trail's anchor. */
export const mainSpineFrames = (spine: Spine) => spine.segments.flatMap((s) => s.frames);

/**
 * Grow jobs, one at a time, persisted as `<jobsDir>/<id>.json` so the queue
 * survives a restart. On load a `queued` job waits again; a `running` one is
 * run again from the start (its working copy is thrown away, and nothing was
 * applied), once; an `applying` one is failed, because the subject may be
 * half-written, and the reader is told to check git.
 */
export class GrowQueue {
	#jobs = new Map<string, GrowJob>();
	#loaded: Promise<void> | null = null;
	#busy = false;
	/** Saves run one after another, so a late progress save never overwrites the outcome. */
	#saving: Promise<void> = Promise.resolve();

	constructor(
		readonly jobsDir: string,
		readonly runner: (job: GrowJob, progress: (text: string) => void) => Promise<GrowOutcome>,
		readonly maxQueued = 10,
		readonly now: () => Date = () => new Date()
	) {}

	/** Read the persisted jobs and recover from a restart; then start the next one. */
	load(): Promise<void> {
		this.#loaded ??= (async () => {
			await mkdir(this.jobsDir, { recursive: true });
			for (const f of (await readdir(this.jobsDir)).filter((f) => f.endsWith('.json'))) {
				try {
					const job = JSON.parse(await readFile(join(this.jobsDir, f), 'utf8')) as GrowJob;
					if (job.kind !== 'kloom.grow-job') continue;
					this.#jobs.set(job.id, job);
					if (job.status === 'running') {
						if (job.attempts >= 2)
							this.#finish(job, 'A server restart interrupted this job twice.');
						else Object.assign(job, { status: 'queued', progress: 'restarted' });
						await this.#save(job);
					} else if (job.status === 'applying') {
						this.#finish(
							job,
							'A server restart interrupted this job while it was writing to the subject; check git status.'
						);
						await this.#save(job);
					}
				} catch (e) {
					console.error(`grow: could not read job ${f}`, e);
				}
			}
			this.#pump();
		})();
		return this.#loaded;
	}

	get queued() {
		return [...this.#jobs.values()].filter((j) => j.status === 'queued').length;
	}

	/** Newest first. */
	list(limit = 10): GrowJob[] {
		return this.#ordered().reverse().slice(0, limit);
	}

	get(id: string) {
		return this.#jobs.get(id);
	}

	/** Oldest first: by when queued, which `add` keeps strictly increasing. */
	#ordered() {
		return [...this.#jobs.values()].sort(
			(a, b) => a.queuedAt.localeCompare(b.queuedAt) || a.id.localeCompare(b.id)
		);
	}

	/** Queue a job; throws when the queue is full. */
	async add(fields: Omit<GrowJob, 'kind' | 'version' | 'id' | 'status' | 'attempts' | 'queuedAt'>) {
		await this.load();
		if (this.queued >= this.maxQueued) throw new Error('Too many grow jobs are waiting.');
		// Two jobs queued in one millisecond still get distinct, ordered times.
		const last = this.#ordered().at(-1)?.queuedAt;
		let at = this.now();
		if (last && at.toISOString() <= last) at = new Date(Date.parse(last) + 1);
		const job: GrowJob = {
			kind: 'kloom.grow-job',
			version: 1,
			id: answerId(at, randomBytes(4).toString('hex')),
			...fields,
			status: 'queued',
			attempts: 0,
			queuedAt: at.toISOString()
		};
		this.#jobs.set(job.id, job);
		await this.#save(job);
		this.#pump();
		return job;
	}

	/** Resolves when no job is running or waiting; for tests and shutdown. */
	async idle() {
		await this.load();
		while (this.#busy) await new Promise((r) => setTimeout(r, 10));
	}

	#finish(job: GrowJob, error: string, problems?: string[]) {
		Object.assign(job, { status: 'failed', error, problems, finishedAt: this.now().toISOString() });
		delete job.progress;
	}

	#save(job: GrowJob): Promise<void> {
		const text = `${JSON.stringify(job, null, '\t')}\n`;
		const tmp = join(this.jobsDir, `.${job.id}.tmp`);
		const write = async () => {
			await writeFile(tmp, text);
			await rename(tmp, join(this.jobsDir, `${job.id}.json`));
		};
		const saved = this.#saving.then(write);
		this.#saving = saved.catch((e) => console.error(`grow: could not save job ${job.id}`, e));
		return saved;
	}

	#pump() {
		if (this.#busy) return;
		const next = this.#ordered().find((j) => j.status === 'queued');
		if (!next) return;
		this.#busy = true;
		(async () => {
			Object.assign(next, {
				status: 'running',
				attempts: next.attempts + 1,
				startedAt: this.now().toISOString()
			});
			await this.#save(next);
			const outcome = await this.runner(next, (text) => {
				next.progress = text;
				if (text === 'committing') next.status = 'applying';
				void this.#save(next).catch(() => {});
			}).catch((e): GrowOutcome => ({ ok: false, error: (e as Error).message }));
			if (outcome.ok) {
				Object.assign(next, {
					status: 'done',
					result: outcome.result,
					finishedAt: this.now().toISOString()
				});
				delete next.progress;
			} else this.#finish(next, outcome.error, outcome.problems);
			await this.#save(next);
		})()
			.catch((e) => console.error('grow: job bookkeeping failed', e))
			.finally(() => {
				this.#busy = false;
				this.#pump();
			});
	}
}

import { readFile } from 'node:fs/promises';
import { homedir, hostname } from 'node:os';
import { basename, join, relative, resolve } from 'node:path';
import { env } from '$env/dynamic/private';
import type { GrowJob } from '$engine/ai/grow';
import { keptAnswerProblems, type KeptAnswer } from '$engine/ai/kept';
import { loadAppConfig } from './app-config';
import { providerFor } from './ask';
import { dataDir, listSubjects, namesDir, subjectDirFor } from './config';
import { contentRepo, growBranch, offBranch, pushGrowBranch } from './content';
import { GrowQueue, runGrowJob } from './grow';
import { devGrowBranch, growWorktree } from './grow-branches';
import { readerStore } from './reader-store';
import { exclusive, servedGraph } from './subject';

/**
 * One grow queue per subject. Jobs are persisted under
 * `<dataDir>/<subject>/grow/`, and every subject's queue is loaded at server
 * start (hooks.server.ts), so a restart picks up where it left off. The
 * queues share one runner slot: the host runs one grow job at a time,
 * whichever subject it is for.
 */

/** Read from the repo, relative to the working directory, like the app config. */
const INSTRUCTIONS = 'skills/grow/SKILL.md';
const REFERENCE: Record<string, string> = {
	'design.md': 'docs/design.md',
	'create-tools/README.md': 'create-tools/README.md',
	'create-tools/draw-plates/README.md': 'create-tools/draw-plates/README.md',
	'create-tools/draw-plates/plates.py': 'create-tools/draw-plates/plates.py',
	'create-tools/wiki-cite/README.md': 'create-tools/wiki-cite/README.md'
};

/**
 * One of a reader's kept answers by id, from their store, checked; null when
 * it is missing or malformed. A reader grows from their own kept answers only.
 */
export async function readKept(
	reader: string,
	subject: string,
	id: string
): Promise<KeptAnswer | null> {
	try {
		const kept = await readerStore().kept(reader, subject, id);
		return kept && keptAnswerProblems(kept).length === 0 && kept.subject === subject ? kept : null;
	} catch (e) {
		console.error('grow: could not read the kept answer', e);
		return null;
	}
}

/**
 * The process's grow state: every subject's queue and the host's one runner
 * slot. It lives on `globalThis`, not in this module, so a dev server that
 * reloads the server modules mid-job keeps the queue that is running it,
 * rather than building a second one that resumes the job and starts a second
 * model process beside the first (korg 3486). The reloaded code takes over
 * at the next restart. The jobs' locks (grow.ts) cover what this cannot: a
 * second process on the same data directory.
 */
interface GrowState {
	queues: Map<string, GrowQueue>;
	/** Each job waits for the one before it, of any subject. */
	slot: Promise<unknown>;
	holders: number;
}

const state: GrowState = ((globalThis as { kloomGrow?: GrowState }).kloomGrow ??= {
	queues: new Map(),
	slot: Promise.resolve(),
	holders: 0
});

function runner(job: GrowJob, progress: (text: string) => void, onSpawn: (pid: number) => void) {
	if (state.holders++ > 0) progress('waiting for another subject’s grow job');
	const run = state.slot.then(() => runOne(job, progress, onSpawn)).finally(() => state.holders--);
	state.slot = run.catch(() => {});
	return run;
}

async function runOne(
	job: GrowJob,
	progress: (text: string) => void,
	onSpawn: (pid: number) => void
) {
	const dir = await subjectDirFor(job.subject);
	if (!dir) return { ok: false as const, error: `The subject "${job.subject}" is not served.` };
	const config = await loadAppConfig();
	if (!config.grow) return { ok: false as const, error: 'Grow is no longer configured.' };
	// A job from before sprint 007 names no reader, and so no store to read.
	const kept = job.kept
		? job.by
			? await readKept(job.by.login, job.subject, job.kept)
			: null
		: undefined;
	if (kept === null) return { ok: false as const, error: 'The kept answer is gone or malformed.' };
	// A service grows only on its content clone's grow branch (content.ts);
	// a dev server, on its own grow branch in a worktree (korg 3442).
	let where: { repo: string; branch: string; subjectDir?: string; namesDir?: string };
	const service = growBranch();
	if (service) {
		where = { repo: await contentRepo(), branch: service };
		const off = await offBranch(where.repo, service);
		if (off) return { ok: false as const, error: off };
	} else
		try {
			where = await devGrow(dir);
		} catch (e) {
			return {
				ok: false as const,
				error: `Could not set up the grow branch: ${(e as Error).message.split('\n')[0]}`
			};
		}
	const { repo, branch } = where;
	const outcome = await runGrowJob(
		job,
		{
			subjectDir: where.subjectDir ?? dir,
			formatAs: where.subjectDir ? dir : undefined,
			provider: providerFor(config),
			instructions: await readFile(resolve(INSTRUCTIONS), 'utf8'),
			reference: Object.fromEntries(
				Object.entries(REFERENCE).map(([to, from]) => [to, resolve(from)])
			),
			kept,
			namesDir: where.namesDir ?? namesDir(),
			frames: framesOf(await servedGraph()),
			timeoutMs: config.grow.timeoutSeconds * 1000,
			exclusive,
			onSpawn
		},
		progress
	);
	// The kept answer now says what it grew into (docs/design.md §Kept answers).
	if (outcome.ok && job.kept && job.by)
		await readerStore()
			.grew(job.by.login, job.subject, job.kept, outcome.result.frames)
			.catch((e) => console.error('grow: could not record what the kept answer grew into', e));
	if (outcome.ok && where.subjectDir) outcome.result.branch = branch;
	if (outcome.ok)
		try {
			await pushGrowBranch(repo, branch);
		} catch (e) {
			console.error(`grow: could not push ${branch}`, e);
			outcome.result.pushError = (e as Error).message.split('\n')[0];
		}
	return outcome;
}

/**
 * Where a dev server grows (korg 3442): `grow/dev-<host>`, in a worktree of
 * the checkout outside it (`$KLOOM_GROW_WORKTREE`, or under `~/.cache/kloom`),
 * so a grow never commits to the branch the author has checked out, and
 * `main` only ever receives reviewed content. The server goes on showing the
 * checkout, so grown frames appear once reviewed and merged.
 */
async function devGrow(subjectDir: string) {
	const repo = await contentRepo();
	const branch = devGrowBranch(hostname());
	const tree = await growWorktree(
		repo,
		env.KLOOM_GROW_WORKTREE ?? join(homedir(), '.cache', 'kloom', `grow-${basename(repo)}`),
		branch
	);
	return {
		repo: tree,
		branch,
		subjectDir: join(tree, relative(repo, subjectDir)),
		namesDir: join(tree, relative(repo, namesDir()))
	};
}

/** Every served frame a grown connection may name, with its topic, title and position. */
const framesOf = (graph: Awaited<ReturnType<typeof servedGraph>>) =>
	Object.fromEntries(
		[...graph.frames].map(([ref, f]) => [
			ref,
			`${f.topic}: ${f.title} (${f.label}${f.trail ? `; trail "${f.trail}"` : ''}; ${graph.subjects[f.subject] ?? f.subject})`
		])
	);

/** A subject's grow queue; the caller has already checked the subject is served. */
export function growQueue(subject: string): GrowQueue {
	const dir = join(dataDir(), subject, 'grow');
	let queue = state.queues.get(subject);
	if (queue?.jobsDir !== dir) state.queues.set(subject, (queue = new GrowQueue(dir, runner)));
	return queue;
}

/** Load every served subject's queue, resuming what a restart interrupted. */
export async function loadGrowQueues() {
	for (const { id } of await listSubjects()) await growQueue(id).load();
}

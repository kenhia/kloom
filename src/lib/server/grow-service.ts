import { readFile } from 'node:fs/promises';
import { join, resolve } from 'node:path';
import type { GrowJob } from '$engine/ai/grow';
import { keptAnswerProblems, type KeptAnswer } from '$engine/ai/kept';
import { loadAppConfig } from './app-config';
import { providerFor } from './ask';
import { dataDir, listSubjects, subjectDirFor } from './config';
import { contentRepo, growBranch, offBranch, pushGrowBranch } from './content';
import { GrowQueue, runGrowJob } from './grow';
import { readerStore } from './reader-store';
import { exclusive } from './subject';

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

/** The host's one grow slot; each job waits for the one before it, of any subject. */
let slot: Promise<unknown> = Promise.resolve();
let holders = 0;

function runner(job: GrowJob, progress: (text: string) => void) {
	if (holders++ > 0) progress('waiting for another subject’s grow job');
	const run = slot.then(() => runOne(job, progress)).finally(() => holders--);
	slot = run.catch(() => {});
	return run;
}

async function runOne(job: GrowJob, progress: (text: string) => void) {
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
	// A service grows only on its content clone's grow branch (content.ts).
	const branch = growBranch();
	const repo = branch ? await contentRepo() : null;
	const off = repo && branch ? await offBranch(repo, branch) : null;
	if (off) return { ok: false as const, error: off };
	const outcome = await runGrowJob(
		job,
		{
			subjectDir: dir,
			provider: providerFor(config),
			instructions: await readFile(resolve(INSTRUCTIONS), 'utf8'),
			reference: Object.fromEntries(
				Object.entries(REFERENCE).map(([to, from]) => [to, resolve(from)])
			),
			kept,
			timeoutMs: config.grow.timeoutSeconds * 1000,
			exclusive
		},
		progress
	);
	// The kept answer now says what it grew into (docs/design.md §Kept answers).
	if (outcome.ok && job.kept && job.by)
		await readerStore()
			.grew(job.by.login, job.subject, job.kept, outcome.result.frames)
			.catch((e) => console.error('grow: could not record what the kept answer grew into', e));
	if (outcome.ok && repo && branch)
		try {
			await pushGrowBranch(repo, branch);
		} catch (e) {
			console.error(`grow: could not push ${branch}`, e);
			outcome.result.pushError = (e as Error).message.split('\n')[0];
		}
	return outcome;
}

const queues = new Map<string, GrowQueue>();

/** A subject's grow queue; the caller has already checked the subject is served. */
export function growQueue(subject: string): GrowQueue {
	const dir = join(dataDir(), subject, 'grow');
	let queue = queues.get(subject);
	if (queue?.jobsDir !== dir) queues.set(subject, (queue = new GrowQueue(dir, runner)));
	return queue;
}

/** Load every served subject's queue, resuming what a restart interrupted. */
export async function loadGrowQueues() {
	for (const { id } of await listSubjects()) await growQueue(id).load();
}

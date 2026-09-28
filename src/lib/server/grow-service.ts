import { readFile } from 'node:fs/promises';
import { join, resolve } from 'node:path';
import type { GrowJob } from '$engine/ai/grow';
import { keptAnswerProblems } from '$engine/ai/kept';
import { loadAppConfig } from './app-config';
import { providerFor } from './ask';
import { dataDir, listSubjects, subjectDirFor } from './config';
import { GrowQueue, runGrowJob } from './grow';
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

/** A kept answer by id, checked; null when it is missing or malformed. */
export async function readKept(subject: string, id: string): Promise<unknown | null> {
	try {
		const kept = JSON.parse(
			await readFile(join(dataDir(), subject, 'kept', `${id}.json`), 'utf8')
		) as { subject?: string };
		return keptAnswerProblems(kept).length === 0 && kept.subject === subject ? kept : null;
	} catch {
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
	const kept = job.kept ? await readKept(job.subject, job.kept) : undefined;
	if (kept === null) return { ok: false as const, error: 'The kept answer is gone or malformed.' };
	return runGrowJob(
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

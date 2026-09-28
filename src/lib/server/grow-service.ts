import { readFile } from 'node:fs/promises';
import { basename, join, resolve } from 'node:path';
import type { GrowJob } from '$engine/ai/grow';
import { keptAnswerProblems } from '$engine/ai/kept';
import { loadAppConfig } from './app-config';
import { providerFor } from './ask';
import { dataDir, subjectDir } from './config';
import { GrowQueue, runGrowJob } from './grow';
import { exclusive } from './subject';

/**
 * The app's one grow queue, for the subject it serves. Jobs are persisted
 * under `<dataDir>/<subject>/grow/`, and the queue is loaded at server start
 * (hooks.server.ts), so a restart picks up where it left off.
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

async function runner(job: GrowJob, progress: (text: string) => void) {
	const config = await loadAppConfig();
	if (!config.grow) return { ok: false as const, error: 'Grow is no longer configured.' };
	const kept = job.kept ? await readKept(job.subject, job.kept) : undefined;
	if (kept === null) return { ok: false as const, error: 'The kept answer is gone or malformed.' };
	return runGrowJob(
		job,
		{
			subjectDir: subjectDir(),
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

let queue: GrowQueue | null = null;

export function growQueue(): GrowQueue {
	const dir = join(dataDir(), basename(subjectDir()), 'grow');
	if (queue?.jobsDir !== dir) queue = new GrowQueue(dir, runner);
	return queue;
}

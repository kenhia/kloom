import { mkdir, readdir, readFile, rename } from 'node:fs/promises';
import { join } from 'node:path';
import { keptAnswerProblems, type KeptAnswer } from '$engine/ai/kept';
import type { ReaderStore } from '$engine/reader-data';

/**
 * Before sprint 011, "keep this" wrote `<dataDir>/<subject>/kept/<id>.json`
 * and only grow read it. Kept answers now live in the reader's store (korg
 * 3390). At server start, any such file moves in, under one reader: the
 * files never said who kept them. Each file moved goes to `kept-migrated/`
 * beside it, so nothing is lost and nothing moves twice. A file that is not
 * a valid kept answer stays where it is and is reported.
 *
 * Grow jobs that used a kept answer already say what it grew into, so that
 * is carried over too.
 */
export async function migrateKeptFiles(
	store: ReaderStore,
	dataDir: string,
	owner: string
): Promise<{ moved: string[]; refused: string[] }> {
	const moved: string[] = [];
	const refused: string[] = [];
	const subjects = await readdir(dataDir, { withFileTypes: true }).catch(() => []);
	for (const s of subjects) {
		if (!s.isDirectory()) continue;
		const dir = join(dataDir, s.name, 'kept');
		const files = (await readdir(dir).catch(() => [])).filter((f) => f.endsWith('.json'));
		if (!files.length) continue;
		const done = join(dataDir, s.name, 'kept-migrated');
		await mkdir(done, { recursive: true });
		const ids = new Set<string>();
		for (const f of files) {
			const path = join(dir, f);
			const kept = await readFile(path, 'utf8')
				.then((t) => JSON.parse(t) as KeptAnswer)
				.catch(() => null);
			if (!kept || keptAnswerProblems(kept).length || kept.subject !== s.name) {
				refused.push(path);
				continue;
			}
			await store.keep(owner, kept);
			await rename(path, join(done, f));
			ids.add(kept.id);
			moved.push(path);
		}
		for (const [id, frames] of await grownFrom(join(dataDir, s.name, 'grow')))
			if (ids.has(id)) await store.grew(owner, s.name, id, frames);
	}
	return { moved, refused };
}

/** Kept answer id → the frames a finished grow job made of it. */
async function grownFrom(jobsDir: string): Promise<Map<string, string[]>> {
	const out = new Map<string, string[]>();
	for (const f of await readdir(jobsDir).catch(() => [])) {
		if (!f.endsWith('.json')) continue;
		const job = await readFile(join(jobsDir, f), 'utf8')
			.then((t) => JSON.parse(t))
			.catch(() => null);
		if (job?.status === 'done' && typeof job.kept === 'string' && job.result?.frames?.length)
			out.set(job.kept, job.result.frames);
	}
	return out;
}

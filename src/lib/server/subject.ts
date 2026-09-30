import { error } from '@sveltejs/kit';
import { buildGraph, type Graph } from '$engine/graph';
import { loadNames, loadSubject, readGraphSubject } from '$engine/load';
import type { Subject } from '$engine/model';
import { readLibraryStats, type LibraryStats } from '$engine/stats';
import { listSubjects, namesDir, subjectDirFor, subjectsDir } from './config';
import { join } from 'node:path';

/**
 * A served subject, read per request, and a gate a grow job holds while it
 * writes new files into one: a request that arrives meanwhile waits, so no
 * reader ever sees (or fails to validate) a half-written subject. One gate
 * for every subject; grow runs one job at a time anyway.
 */
let gate: Promise<unknown> = Promise.resolve();

/** The subject's directory, or a 404 for an id the app does not serve. */
export async function requireSubjectDir(id: unknown): Promise<string> {
	const dir = await subjectDirFor(id);
	if (!dir) error(404, 'No such subject.');
	return dir;
}

/** Load a served subject; its media is served under `/media/<id>/`. A 404 for an unknown id. */
export async function servedSubject(id: unknown): Promise<Subject> {
	const dir = await requireSubjectDir(id);
	await gate;
	return loadSubject(dir, { mediaBase: `/media/${id}` });
}

/**
 * The graph index across every served subject (docs/design.md
 * §Connections), rebuilt per request from a light read of each: content
 * written to disk shows at once, as the subjects themselves do. A name file
 * that is invalid is left out, and said in the log.
 */
export async function servedGraph(): Promise<Graph> {
	await gate;
	const [subjects, { names, problems }] = await Promise.all([
		listSubjects(),
		loadNames(namesDir())
	]);
	if (problems.length) console.error(`names: ${problems.join('; ')}`);
	const read = await Promise.all(
		subjects.map((s) => readGraphSubject(join(subjectsDir(), s.id), s.id))
	);
	return buildGraph(read, names);
}

/**
 * The library's counts (docs/design.md §About), read from disk per request
 * as the subjects are, so grown content counts at once.
 */
export async function servedStats(): Promise<LibraryStats> {
	await gate;
	const subjects = await listSubjects();
	return readLibraryStats(
		subjects.map((s) => ({ id: s.id, dir: join(subjectsDir(), s.id) })),
		namesDir()
	);
}

/** Run `fn` while the gate is held; readers wait for it. */
export function exclusive<T>(fn: () => Promise<T>): Promise<T> {
	const done = gate.then(fn, fn);
	gate = done.catch(() => {});
	return done;
}

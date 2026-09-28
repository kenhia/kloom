import { error } from '@sveltejs/kit';
import { loadSubject } from '$engine/load';
import type { Subject } from '$engine/model';
import { subjectDirFor } from './config';

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

/** Run `fn` while the gate is held; readers wait for it. */
export function exclusive<T>(fn: () => Promise<T>): Promise<T> {
	const done = gate.then(fn, fn);
	gate = done.catch(() => {});
	return done;
}

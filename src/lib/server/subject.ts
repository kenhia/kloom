import { loadSubject } from '$engine/load';
import type { Subject } from '$engine/model';
import { subjectDir } from './config';

/**
 * The served subject, read per request, and a gate a grow job holds while it
 * writes new files into it: a request that arrives meanwhile waits, so no
 * reader ever sees (or fails to validate) a half-written subject.
 */
let gate: Promise<unknown> = Promise.resolve();

export async function servedSubject(): Promise<Subject> {
	await gate;
	return loadSubject(subjectDir());
}

/** Run `fn` while the gate is held; readers wait for it. */
export function exclusive<T>(fn: () => Promise<T>): Promise<T> {
	const done = gate.then(fn, fn);
	gate = done.catch(() => {});
	return done;
}

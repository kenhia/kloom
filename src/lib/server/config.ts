import { readdir, readFile } from 'node:fs/promises';
import { join, resolve } from 'node:path';
import { env } from '$env/dynamic/private';

/**
 * Which subjects this app serves: every directory under `$KLOOM_SUBJECTS_DIR`
 * (default `subjects/`) that holds a `subject.json`. The engine never names
 * one; this is the app's choice. `$KLOOM_SUBJECT` names the landing subject,
 * the one `/` opens on.
 */
export const subjectsDir = () => resolve(env.KLOOM_SUBJECTS_DIR ?? 'subjects');

/**
 * The name registry every subject shares (docs/design.md §Connections):
 * `$KLOOM_NAMES_DIR`, by default `names/` beside the subjects directory, so
 * the service's content clone carries its own.
 */
export const namesDir = () => resolve(env.KLOOM_NAMES_DIR ?? join(subjectsDir(), '..', 'names'));

/** The landing subject's id. */
export const defaultSubject = () => env.KLOOM_SUBJECT ?? 'western-civ';

/** What a subject id may look like: a plain directory name, never a path. */
export const SUBJECT_ID = /^[a-z0-9][a-z0-9-]*$/;

/** A served subject: its id (the directory name), title and subtitle (from `subject.json`). */
export interface SubjectEntry {
	id: string;
	title: string;
	subtitle?: string;
}

/** Every subject served, in id order; one whose `subject.json` is unreadable is left out. */
export async function listSubjects(): Promise<SubjectEntry[]> {
	const root = subjectsDir();
	const dirs = await readdir(root, { withFileTypes: true }).catch(() => []);
	const found: SubjectEntry[] = [];
	for (const d of dirs) {
		if (!d.isDirectory() || !SUBJECT_ID.test(d.name)) continue;
		try {
			const manifest = JSON.parse(await readFile(join(root, d.name, 'subject.json'), 'utf8'));
			found.push({
				id: d.name,
				title: typeof manifest?.title === 'string' ? manifest.title : d.name,
				...(typeof manifest?.subtitle === 'string' && manifest.subtitle.trim()
					? { subtitle: manifest.subtitle }
					: {})
			});
		} catch {
			// Not a subject (or a broken one): nothing to offer.
		}
	}
	return found.sort((a, b) => a.id.localeCompare(b.id));
}

/**
 * A subject's directory, or null when `id` is not one of the served subjects.
 * Checked against the listing, not just the pattern, so no request can name a
 * directory the app does not serve.
 */
export async function subjectDirFor(id: unknown): Promise<string | null> {
	if (typeof id !== 'string' || !SUBJECT_ID.test(id)) return null;
	const known = await listSubjects();
	return known.some((s) => s.id === id) ? join(subjectsDir(), id) : null;
}

/**
 * Where the app keeps what it writes that is not subject content, such as
 * kept answers (`<dataDir>/<subject>/kept/`). Git-ignored.
 */
export const dataDir = () => resolve(env.KLOOM_DATA_DIR ?? 'data');

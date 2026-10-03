import { execFile } from 'node:child_process';
import { promisify } from 'node:util';

/**
 * When each frame and trail first appeared in the content's history
 * (docs/design.md §What's new, korg 3525), read from git. Node only.
 *
 * The history is the first-parent line of the commit checked out: on `main`
 * that is the squash merges, so a frame's date is the merge that reviewed it
 * in (korg 3442). A service's content clone is on its grow branch, so a grown
 * frame dates from its grow commit there, and the public site's library,
 * staged from a commit of `main`, sees nothing after that commit: what it
 * calls added is exactly what was published.
 *
 * A path added, removed and added again keeps its first date, and a renamed
 * frame dates from the rename (renames are not followed). A frame git has
 * never seen (written but not committed) has no date; `added` in its
 * frame.json overrides either way.
 */

/** Each subject's dates: frame and trail ids to an ISO 8601 time, UTC. */
export type AddedDates = Record<
	string,
	{ frames: Record<string, string>; trails: Record<string, string> }
>;

/** `<subject>/frames/<id>/frame.json` and `<subject>/trails/<id>.json`, relative to the subjects directory. */
const FRAME = /^([a-z0-9][a-z0-9-]*)\/frames\/([\w-]+)\/frame\.json$/;
const TRAIL = /^([a-z0-9][a-z0-9-]*)\/trails\/([\w-]+)\.json$/;

/** A commit's start in the log: a byte no path holds, then its committer time. */
const MARK = '\x01';

/**
 * Read `git log`'s additions under `subjectsDir` into dates. The log is
 * newest first, so a path's last addition seen is its first.
 */
export function parseAdditions(log: string): AddedDates {
	const out: AddedDates = {};
	let at: string | null = null;
	for (const line of log.split('\n')) {
		if (line.startsWith(MARK)) {
			const t = new Date(line.slice(1).trim());
			at = Number.isNaN(t.getTime()) ? null : t.toISOString();
			continue;
		}
		if (!at || !line) continue;
		const frame = FRAME.exec(line);
		const trail = frame ? null : TRAIL.exec(line);
		const m = frame ?? trail;
		if (!m) continue;
		const s = (out[m[1]] ??= { frames: {}, trails: {} });
		(frame ? s.frames : s.trails)[m[2]] = at;
	}
	return out;
}

/**
 * The dates git gives for `subjectsDir`'s frames and trails; null when it is
 * not in a repository, or git cannot be run (the reader site's image has no
 * git, and never compiles).
 */
export async function gitAddedDates(subjectsDir: string): Promise<AddedDates | null> {
	try {
		const { stdout } = await promisify(execFile)(
			'git',
			[
				'log',
				'--first-parent',
				'--diff-filter=A',
				'--no-renames',
				'--relative',
				`--format=${MARK}%cI`,
				'--name-only',
				'HEAD',
				'--',
				'.'
			],
			{ cwd: subjectsDir, maxBuffer: 64 * 1024 * 1024 }
		);
		return parseAdditions(stdout);
	} catch {
		return null;
	}
}

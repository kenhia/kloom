import { execFile } from 'node:child_process';
import { existsSync } from 'node:fs';
import { promisify } from 'node:util';

/**
 * Grow branches and what `main` has of them (docs/design.md §Reviewing grown
 * content, korg 3442). Grown content reaches main only through review, so a
 * grow branch is either pending (it holds content main does not) or merged
 * (main has all of it, however it got there: a squash, a rebase, or edits
 * since). That is a git query, not a judgement, and it is what a sprint
 * checks for first (`just grow-pending`).
 *
 * No `$env` here: `just grow-pending` loads this module outside SvelteKit.
 */

const run = promisify(execFile);
export const git = async (cwd: string, args: string[]) =>
	(await run('git', args, { cwd, maxBuffer: 1 << 22 })).stdout.trim();
const succeeds = (cwd: string, args: string[]) =>
	git(cwd, args).then(
		() => true,
		() => false
	);
const lines = (s: string) => s.split('\n').filter(Boolean);

/** A dev server's grow branch: one per host, as the service's is `grow/<host>`. */
export const devGrowBranch = (host: string) => `grow/dev-${host.split('.')[0]}`;

/**
 * The trailer a review's merge commit carries for each grow branch tip it
 * reviewed (skills/review-grown): `Grow-reviewed: <full sha> (<ref>)`.
 */
export const REVIEWED_TRAILER = 'Grow-reviewed';

/** Every grow commit `upstream`'s history says was reviewed in. */
export async function reviewedCommits(repo: string, upstream: string): Promise<Set<string>> {
	const text = await git(repo, [
		'log',
		upstream,
		`--format=%(trailers:key=${REVIEWED_TRAILER},valueonly,separator=%x0A)`
	]);
	return new Set(text.match(/\b[0-9a-f]{40}\b/g) ?? []);
}

/**
 * The newest commit of `base..head` that main already has. Either a review
 * merged it, and says so in a `Grow-reviewed` trailer (its content may have
 * been repaired on the way in), or some commit on main holds every path it
 * and the commits before it touched exactly as it left them. That is how a
 * squash or rebase merge of a grow branch shows up, and it still matches
 * after main edits those files further.
 */
export async function lastMerged(
	repo: string,
	base: string,
	upstream: string,
	head = 'HEAD'
): Promise<string | null> {
	const grown = lines(await git(repo, ['rev-list', '--reverse', `${base}..${head}`]));
	const onMain = lines(await git(repo, ['rev-list', `${base}..${upstream}`]));
	const reviewed = await reviewedCommits(repo, upstream);
	let found: string | null = null;
	for (const commit of grown) {
		if (reviewed.has(commit)) {
			found = commit;
			continue;
		}
		const paths = lines(await git(repo, ['diff', '--name-only', base, commit]));
		for (const m of onMain)
			if (await succeeds(repo, ['diff', '--quiet', commit, m, '--', ...paths])) {
				found = commit;
				break;
			}
	}
	return found;
}

export interface GrowBranchState {
	/** The ref as git names it: `grow/dev-kai`, `origin/grow/kai`. */
	ref: string;
	/** Commits on the branch that main's history does not contain. */
	ahead: number;
	/** Whether main has the branch's content (see `lastMerged`). */
	merged: boolean;
}

/** Whether `main` has all of `ref`'s content. */
export async function contentMerged(repo: string, ref: string, main: string) {
	if (await succeeds(repo, ['merge-base', '--is-ancestor', ref, main])) return true;
	const base = await git(repo, ['merge-base', ref, main]);
	const tip = await git(repo, ['rev-parse', ref]);
	return (await lastMerged(repo, base, main, ref)) === tip;
}

/**
 * Every grow branch, local and on origin (`grow/*`, and the older `grow-*`),
 * with whether main has its content. Pending ones first.
 */
export async function growBranches(repo: string, main = 'origin/main'): Promise<GrowBranchState[]> {
	const refs = lines(
		await git(repo, [
			'for-each-ref',
			'--format=%(refname:short)',
			'refs/heads/grow/',
			'refs/heads/grow-*',
			'refs/remotes/origin/grow/',
			'refs/remotes/origin/grow-*'
		])
	);
	const out: GrowBranchState[] = [];
	for (const ref of refs) {
		const ahead = Number(await git(repo, ['rev-list', '--count', `${main}..${ref}`]));
		out.push({ ref, ahead, merged: ahead === 0 || (await contentMerged(repo, ref, main)) });
	}
	return out.sort((a, b) => Number(a.merged) - Number(b.merged) || a.ref.localeCompare(b.ref));
}

/**
 * A dev server's grow worktree (korg 3442): grow commits to `branch` in a
 * worktree of the checkout at `dir`, never to the branch the author has
 * checked out. Created from `main` the first time; afterwards, when it has
 * no changes of its own and main has all its content (a review merged it,
 * or there was none), moved to `main`, so the next grow starts from what was
 * reviewed. Returns the worktree's top level.
 */
export async function growWorktree(
	repo: string,
	dir: string,
	branch: string,
	main = 'main'
): Promise<string> {
	if (!existsSync(dir)) {
		await git(repo, ['worktree', 'prune']);
		const exists = await succeeds(repo, [
			'rev-parse',
			'--verify',
			'--quiet',
			`refs/heads/${branch}`
		]);
		await git(repo, [
			'worktree',
			'add',
			'--quiet',
			...(exists ? [dir, branch] : ['-b', branch, dir, main])
		]);
		return dir;
	}
	const at = await git(dir, ['branch', '--show-current']);
	if (at !== branch)
		throw new Error(`The grow worktree ${dir} is on "${at}", not the grow branch "${branch}".`);
	if (!(await git(dir, ['status', '--porcelain'])) && (await contentMerged(dir, 'HEAD', main)))
		await git(dir, ['reset', '--quiet', '--hard', main]);
	return dir;
}

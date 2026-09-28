import { execFile } from 'node:child_process';
import { promisify } from 'node:util';
import { env } from '$env/dynamic/private';
import { subjectsDir } from './config';
import { GROW_AUTHOR } from './grow';

/**
 * The service's content clone (korg 3412; docs/deploying.md). A service
 * never grows into the checkout it was built from or developed in: it reads
 * subjects from a clone of its own, checked out on a grow branch
 * (`$KLOOM_GROW_BRANCH`, e.g. `grow/kai`). Grow commits there and pushes the
 * branch; an ordinary PR brings the content back to main. Unset, grow commits
 * wherever the subjects are and pushes nothing, which is the dev setup.
 *
 * At start the clone picks up merged main (`syncContent`). A deploy is a
 * restart, and it replaces only the app, never this clone.
 */

const run = promisify(execFile);
const git = async (cwd: string, args: string[]) =>
	(await run('git', args, { cwd, maxBuffer: 1 << 22 })).stdout.trim();
const succeeds = (cwd: string, args: string[]) =>
	git(cwd, args).then(
		() => true,
		() => false
	);
const lines = (s: string) => s.split('\n').filter(Boolean);
const AS_GROW = ['-c', `user.name=${GROW_AUTHOR.name}`, '-c', `user.email=${GROW_AUTHOR.email}`];

/** The grow branch, or null when this is not a service with a content clone. */
export const growBranch = () => env.KLOOM_GROW_BRANCH || null;

/** The repository the served subjects are in. */
export const contentRepo = () => git(subjectsDir(), ['rev-parse', '--show-toplevel']);

/** Why grow must not commit here, or null when the clone is on its grow branch. */
export async function offBranch(repo: string, branch: string): Promise<string | null> {
	const at = await git(repo, ['branch', '--show-current']);
	return at === branch
		? null
		: `The content clone is on ${at ? `"${at}"` : 'a detached HEAD'}, not the grow branch "${branch}".`;
}

/** Push the grow branch; `force` only after a sync rewrote it. */
export async function pushGrowBranch(repo: string, branch: string, force = false) {
	await git(repo, [
		'push',
		'--quiet',
		...(force ? [`--force-with-lease=${branch}`] : []),
		'origin',
		`${branch}:refs/heads/${branch}`
	]);
}

export type SyncOutcome =
	'up to date' | 'ahead' | 'fast-forwarded' | 'merged' | 'rebased' | 'diverged' | 'dirty';

/**
 * The newest grow commit whose content main already has: some commit on main
 * holds every path it and the commits before it touched exactly as it left
 * them. That is how a squash or rebase merge of the grow branch shows up,
 * and it still matches after main edits those files further.
 */
async function lastMerged(repo: string, base: string, upstream: string): Promise<string | null> {
	const grown = lines(await git(repo, ['rev-list', '--reverse', `${base}..HEAD`]));
	const onMain = lines(await git(repo, ['rev-list', `${base}..${upstream}`]));
	let found: string | null = null;
	for (const commit of grown) {
		const paths = lines(await git(repo, ['diff', '--name-only', base, commit]));
		for (const m of onMain)
			if (await succeeds(repo, ['diff', '--quiet', commit, m, '--', ...paths])) {
				found = commit;
				break;
			}
	}
	return found;
}

/**
 * Bring merged main into the grow branch, and push it. Never loses grown
 * work: anything main does not have yet is rebased onto it, and a rebase
 * that conflicts is abandoned, leaving the clone as it was ("diverged") for
 * a person to sort out. A clone with uncommitted changes is left alone.
 */
export async function syncContent(
	repo: string,
	branch: string,
	main = 'main'
): Promise<{ outcome: SyncOutcome; detail: string }> {
	const off = await offBranch(repo, branch);
	if (off) throw new Error(off);
	if (await git(repo, ['status', '--porcelain']))
		return { outcome: 'dirty', detail: 'the content clone has uncommitted changes; left alone' };
	await git(repo, ['fetch', '--quiet', 'origin']);
	const upstream = `origin/${main}`;
	const [head, up] = [
		await git(repo, ['rev-parse', 'HEAD']),
		await git(repo, ['rev-parse', upstream])
	];

	let outcome: SyncOutcome;
	let detail: string;
	if (head === up) [outcome, detail] = ['up to date', `${branch} is ${upstream}`];
	else if (await succeeds(repo, ['merge-base', '--is-ancestor', 'HEAD', upstream])) {
		await git(repo, ['merge', '--quiet', '--ff-only', upstream]);
		[outcome, detail] = ['fast-forwarded', `${branch} fast-forwarded to ${upstream}`];
	} else if (await succeeds(repo, ['merge-base', '--is-ancestor', upstream, 'HEAD'])) {
		const n = await git(repo, ['rev-list', '--count', `${upstream}..HEAD`]);
		[outcome, detail] = ['ahead', `${branch} has ${n} grow commit(s) waiting for a PR`];
	} else {
		const base = await git(repo, ['merge-base', 'HEAD', upstream]);
		const merged = await lastMerged(repo, base, upstream);
		if (merged === head) {
			await git(repo, ['reset', '--quiet', '--hard', upstream]);
			[outcome, detail] = ['merged', `${upstream} has ${branch}'s content; reset to it`];
		} else {
			const rebase = merged ? ['--onto', upstream, merged] : [upstream];
			try {
				await git(repo, [...AS_GROW, 'rebase', '--quiet', ...rebase]);
				[outcome, detail] = [
					'rebased',
					`${branch}'s unmerged grow commits rebased onto ${upstream}`
				];
			} catch (e) {
				await git(repo, ['rebase', '--abort']).catch(() => {});
				return {
					outcome: 'diverged',
					detail: `${branch} and ${upstream} conflict, so the clone was left as it was: ${(e as Error).message.split('\n')[0]}`
				};
			}
		}
	}
	await pushGrowBranch(repo, branch, outcome === 'merged' || outcome === 'rebased');
	return { outcome, detail };
}

/** At server start: sync the clone if there is one. Never stops the server. */
export async function syncContentAtStart() {
	const branch = growBranch();
	if (!branch) return;
	try {
		const { outcome, detail } = await syncContent(await contentRepo(), branch);
		(outcome === 'diverged' || outcome === 'dirty' ? console.error : console.log)(
			`content: ${detail}`
		);
	} catch (e) {
		console.error('content: could not sync the content clone', e);
	}
}

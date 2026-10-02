import { execFileSync } from 'node:child_process';
import { existsSync } from 'node:fs';
import { mkdir, mkdtemp, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { dirname, join } from 'node:path';
import { beforeEach, describe, expect, it } from 'vitest';
import { devGrowBranch, growBranches, growWorktree } from './grow-branches';

const git = (cwd: string, ...args: string[]) =>
	execFileSync('git', ['-c', 'user.name=t', '-c', 'user.email=t@t', ...args], {
		cwd,
		encoding: 'utf8',
		stdio: ['ignore', 'pipe', 'pipe']
	}).trim();

async function commit(repo: string, files: Record<string, string>, message = 'change') {
	for (const [path, text] of Object.entries(files)) {
		await mkdir(dirname(join(repo, path)), { recursive: true });
		await writeFile(join(repo, path), text);
	}
	git(repo, 'add', '.');
	git(repo, 'commit', '-q', '-m', message);
	return git(repo, 'rev-parse', 'HEAD');
}

/** origin (bare), and ken's checkout of it, on a sprint branch. */
let root: string, origin: string, ken: string;
beforeEach(async () => {
	root = await mkdtemp(join(tmpdir(), 'kloom-grow-branches-'));
	[origin, ken] = ['origin.git', 'ken'].map((d) => join(root, d));
	git(root, 'init', '-q', '--bare', '-b', 'main', origin);
	git(root, 'clone', '-q', origin, ken);
	await commit(ken, { 'subjects/s/spine': 'a\n' }, 'start');
	git(ken, 'push', '-q', 'origin', 'main');
	git(ken, 'checkout', '-q', '-b', '036-sprint');
});

describe('a dev grow branch', () => {
	it('is named for the host', () => {
		expect(devGrowBranch('kai')).toBe('grow/dev-kai');
		expect(devGrowBranch('kai.tail1234.ts.net')).toBe('grow/dev-kai');
	});

	it('lives in a worktree from main, so the checkout and its branch are never touched', async () => {
		await commit(ken, { 'notes.md': 'sprint work' }, 'sprint work');
		const tree = await growWorktree(ken, join(root, 'grow-tree'), 'grow/dev-kai');
		expect(git(tree, 'branch', '--show-current')).toBe('grow/dev-kai');
		expect(existsSync(join(tree, 'notes.md'))).toBe(false); // from main, not the sprint
		await commit(tree, { 'subjects/s/b': 'grown' }, 'grow(s): add b');
		expect(git(ken, 'branch', '--show-current')).toBe('036-sprint');
		expect(git(ken, 'log', '-1', '--format=%s')).toBe('sprint work');
		expect(git(ken, 'status', '--porcelain')).toBe('');
		// Found again on the next job, and not moved: it holds grown work.
		git(ken, 'checkout', '-q', 'main');
		await commit(ken, { 'other.md': 'x' }, 'main moves on');
		expect(await growWorktree(ken, join(root, 'grow-tree'), 'grow/dev-kai')).toBe(
			join(root, 'grow-tree')
		);
		expect(git(tree, 'log', '-1', '--format=%s')).toBe('grow(s): add b');
	});

	it('catches up with main when it holds nothing main lacks', async () => {
		const tree = await growWorktree(ken, join(root, 'grow-tree'), 'grow/dev-kai');
		git(ken, 'checkout', '-q', 'main');
		await commit(ken, { 'other.md': 'x' }, 'main moves on');
		await growWorktree(ken, join(root, 'grow-tree'), 'grow/dev-kai');
		expect(git(tree, 'log', '-1', '--format=%s')).toBe('main moves on');
	});

	it('is set up again on its branch when the worktree was removed', async () => {
		const tree = await growWorktree(ken, join(root, 'grow-tree'), 'grow/dev-kai');
		await commit(tree, { 'subjects/s/b': 'grown' }, 'grow(s): add b');
		git(ken, 'worktree', 'remove', '--force', tree);
		const again = await growWorktree(ken, join(root, 'grow-tree-2'), 'grow/dev-kai');
		expect(git(again, 'log', '-1', '--format=%s')).toBe('grow(s): add b');
	});
});

describe('pending grow branches', () => {
	const pending = async () =>
		(await growBranches(ken, 'origin/main')).filter((b) => !b.merged).map((b) => b.ref);

	it('lists a grow branch whose content main lacks, until a squash merge brings it in', async () => {
		const tree = await growWorktree(ken, join(root, 'grow-tree'), 'grow/dev-kai');
		await commit(tree, { 'subjects/s/b': 'grown', 'subjects/s/spine': 'a\nb\n' }, 'grow(s): add b');
		git(tree, 'push', '-q', 'origin', 'grow/dev-kai');
		git(ken, 'fetch', '-q');
		expect(await pending()).toEqual(['grow/dev-kai', 'origin/grow/dev-kai']);

		// Reviewed and squash-merged, then main edits the grown file further.
		git(ken, 'checkout', '-q', 'main');
		git(ken, 'merge', '-q', '--squash', 'grow/dev-kai');
		git(ken, 'commit', '-q', '-m', 'grow(s): add b (reviewed)');
		await commit(ken, { 'subjects/s/b': 'grown, then edited' }, 'edit b');
		git(ken, 'push', '-q', 'origin', 'main');
		git(ken, 'fetch', '-q');
		expect(await pending()).toEqual([]);
	});

	it('counts a branch a review merged with repairs, by its trailer, and the worktree moves on', async () => {
		const at = join(root, 'grow-tree');
		const tree = await growWorktree(ken, at, 'grow/dev-kai');
		await commit(tree, { 'subjects/s/b': 'grown' }, 'grow(s): add b');
		const tip = git(tree, 'rev-parse', 'HEAD');
		git(ken, 'checkout', '-q', 'main');
		git(ken, 'merge', '-q', '--squash', 'grow/dev-kai');
		await writeFile(join(ken, 'subjects/s/b'), 'grown, repaired');
		git(ken, 'add', '.');
		git(ken, 'commit', '-q', '-m', `review-grown\n\nGrow-reviewed: ${tip} (grow/dev-kai)`);
		git(ken, 'push', '-q', 'origin', 'main');
		git(ken, 'fetch', '-q');
		expect(await pending()).toEqual([]);
		// The next grow starts from what was reviewed.
		await growWorktree(ken, at, 'grow/dev-kai');
		expect(git(tree, 'rev-parse', 'HEAD')).toBe(git(ken, 'rev-parse', 'main'));
	});

	it('counts an older grow-* branch, and one that is only an ancestor of main is merged', async () => {
		git(ken, 'checkout', '-q', 'main');
		git(ken, 'branch', 'grow-old');
		await commit(ken, { 'other.md': 'x' }, 'main moves on');
		git(ken, 'push', '-q', 'origin', 'main', 'grow-old');
		git(ken, 'fetch', '-q');
		const states = await growBranches(ken, 'origin/main');
		expect(states.map((b) => [b.ref, b.merged])).toEqual([
			['grow-old', true],
			['origin/grow-old', true]
		]);
	});
});

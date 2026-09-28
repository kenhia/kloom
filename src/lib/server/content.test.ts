import { execFileSync } from 'node:child_process';
import { mkdtemp, readFile, writeFile, mkdir } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { dirname, join } from 'node:path';
import { beforeEach, describe, expect, it } from 'vitest';
import { offBranch, syncContent } from './content';

const git = (cwd: string, ...args: string[]) =>
	execFileSync('git', ['-c', 'user.name=t', '-c', 'user.email=t@t', ...args], {
		cwd,
		encoding: 'utf8',
		stdio: ['ignore', 'pipe', 'pipe']
	}).trim();

const BRANCH = 'grow/test';

/** Write files and commit them. */
async function commit(repo: string, files: Record<string, string>, message = 'change') {
	for (const [path, text] of Object.entries(files)) {
		await mkdir(dirname(join(repo, path)), { recursive: true });
		await writeFile(join(repo, path), text);
	}
	git(repo, 'add', '.');
	git(repo, 'commit', '-q', '-m', message);
	return git(repo, 'rev-parse', 'HEAD');
}

const read = (repo: string, path: string) => readFile(join(repo, path), 'utf8');
const spine = (...frames: string[]) => frames.map((f) => `${f}\n`).join('');

/** origin (bare), ken (a checkout on main) and clone (the service's, on the grow branch). */
let origin: string, ken: string, clone: string;
beforeEach(async () => {
	const root = await mkdtemp(join(tmpdir(), 'kloom-content-'));
	[origin, ken, clone] = ['origin.git', 'ken', 'clone'].map((d) => join(root, d));
	git(root, 'init', '-q', '--bare', '-b', 'main', origin);
	git(root, 'clone', '-q', origin, ken);
	await commit(ken, { 'subjects/s/spine': spine('a', 'b', 'c') }, 'start');
	git(ken, 'push', '-q', 'origin', 'main');
	git(root, 'clone', '-q', origin, clone);
	git(clone, 'checkout', '-q', '-b', BRANCH);
});

/** What a grow job does: a new frame, and the spine gains it. */
const grow = (frame: string, ...frames: string[]) =>
	commit(clone, { [`subjects/s/${frame}`]: frame, 'subjects/s/spine': spine(...frames) }, frame);

/** Ken brings the grow branch back with a squash merge, then optionally edits. */
async function squashMerge() {
	git(ken, 'fetch', '-q');
	git(ken, 'merge', '-q', '--squash', `origin/${BRANCH}`);
	git(ken, 'commit', '-q', '-m', 'grown content');
	git(ken, 'push', '-q', 'origin', 'main');
}

const remoteGrow = () => git(origin, 'rev-parse', BRANCH);

describe('syncContent', () => {
	it('is up to date, and publishes the branch', async () => {
		expect((await syncContent(clone, BRANCH)).outcome).toBe('up to date');
		expect(remoteGrow()).toBe(git(clone, 'rev-parse', 'HEAD'));
	});

	it('fast-forwards to new main', async () => {
		await commit(ken, { 'subjects/s/spine': spine('a', 'b', 'c', 'd') });
		git(ken, 'push', '-q', 'origin', 'main');
		expect((await syncContent(clone, BRANCH)).outcome).toBe('fast-forwarded');
		expect(await read(clone, 'subjects/s/spine')).toBe(spine('a', 'b', 'c', 'd'));
	});

	it('leaves unmerged grow commits alone and pushes them', async () => {
		const head = await grow('x', 'a', 'x', 'b', 'c');
		const { outcome, detail } = await syncContent(clone, BRANCH);
		expect(outcome).toBe('ahead');
		expect(detail).toContain('1 grow commit');
		expect(remoteGrow()).toBe(head);
	});

	it('fast-forwards after a merge-commit merge', async () => {
		await grow('x', 'a', 'x', 'b', 'c');
		await syncContent(clone, BRANCH);
		git(ken, 'fetch', '-q');
		git(ken, 'merge', '-q', '--no-ff', '-m', 'merge', `origin/${BRANCH}`);
		git(ken, 'push', '-q', 'origin', 'main');
		expect((await syncContent(clone, BRANCH)).outcome).toBe('fast-forwarded');
	});

	it('resets to main after a squash merge, even when main edited the grown files since', async () => {
		await grow('x', 'a', 'x', 'b', 'c');
		await grow('y', 'a', 'x', 'b', 'y', 'c');
		await syncContent(clone, BRANCH);
		await squashMerge();
		await commit(ken, { 'subjects/s/x': 'x, edited in review' });
		git(ken, 'push', '-q', 'origin', 'main');

		expect((await syncContent(clone, BRANCH)).outcome).toBe('merged');
		expect(git(clone, 'rev-parse', 'HEAD')).toBe(git(origin, 'rev-parse', 'main'));
		expect(await read(clone, 'subjects/s/x')).toBe('x, edited in review');
		expect(remoteGrow()).toBe(git(origin, 'rev-parse', 'main'));
	});

	it('keeps a job grown after the PR, rebased onto the squash', async () => {
		await grow('x', 'a', 'x', 'b', 'c');
		await syncContent(clone, BRANCH);
		await squashMerge();
		await grow('y', 'a', 'x', 'b', 'y', 'c'); // after the PR was merged, before a restart

		expect((await syncContent(clone, BRANCH)).outcome).toBe('rebased');
		expect(git(clone, 'rev-list', '--count', 'origin/main..HEAD')).toBe('1');
		expect(await read(clone, 'subjects/s/spine')).toBe(spine('a', 'x', 'b', 'y', 'c'));
		expect(remoteGrow()).toBe(git(clone, 'rev-parse', 'HEAD'));
	});

	it('rebases unmerged work over unrelated changes on main', async () => {
		await grow('x', 'a', 'x', 'b', 'c');
		await commit(ken, { 'docs/readme': 'hello' });
		git(ken, 'push', '-q', 'origin', 'main');
		expect((await syncContent(clone, BRANCH)).outcome).toBe('rebased');
		expect(await read(clone, 'docs/readme')).toBe('hello');
		expect(await read(clone, 'subjects/s/x')).toBe('x');
	});

	it('leaves the clone as it was when main and the grow branch conflict', async () => {
		const head = await grow('x', 'a', 'x', 'b', 'c');
		await commit(ken, { 'subjects/s/spine': spine('a', 'q', 'b', 'c') });
		git(ken, 'push', '-q', 'origin', 'main');
		const { outcome } = await syncContent(clone, BRANCH);
		expect(outcome).toBe('diverged');
		expect(git(clone, 'rev-parse', 'HEAD')).toBe(head);
		expect(git(clone, 'status', '--porcelain')).toBe('');
	});

	it('leaves a dirty clone alone', async () => {
		await writeFile(join(clone, 'subjects/s/spine'), 'hand edit');
		expect((await syncContent(clone, BRANCH)).outcome).toBe('dirty');
	});

	it('refuses a clone that is not on the grow branch', async () => {
		git(clone, 'checkout', '-q', 'main');
		expect(await offBranch(clone, BRANCH)).toContain('"main"');
		await expect(syncContent(clone, BRANCH)).rejects.toThrow('not the grow branch');
	});
});

import { execFileSync } from 'node:child_process';
import { mkdirSync, mkdtempSync, renameSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, join } from 'node:path';
import { afterAll, beforeAll, describe, expect, it } from 'vitest';
import { gitAddedDates, parseAdditions } from './history';

/**
 * A repository shaped like kloom's: work on a branch, squash-merged into
 * main, so each frame's date is its merge's, not its branch commit's.
 */
let repo: string;
const git = (args: string[], date?: string) =>
	execFileSync('git', args, {
		cwd: repo,
		env: {
			...process.env,
			GIT_AUTHOR_NAME: 't',
			GIT_AUTHOR_EMAIL: 't@example.org',
			GIT_COMMITTER_NAME: 't',
			GIT_COMMITTER_EMAIL: 't@example.org',
			...(date ? { GIT_AUTHOR_DATE: date, GIT_COMMITTER_DATE: date } : {})
		},
		encoding: 'utf8'
	});
const put = (path: string, text = '{}') => {
	const at = join(repo, path);
	mkdirSync(dirname(at), { recursive: true });
	writeFileSync(at, text);
};

beforeAll(() => {
	repo = mkdtempSync(join(tmpdir(), 'kloom-history-'));
	git(['init', '-q', '-b', 'main']);
	put('README.md', 'not content');
	put('subjects/s/frames/a/frame.json');
	put('subjects/s/frames/a/reading.md', 'A.');
	git(['add', '-A']);
	git(['commit', '-qm', 'first publish'], '2026-09-01T10:00:00Z');

	// A sprint's branch: two commits, then squash-merged a day later.
	git(['checkout', '-qb', 'sprint']);
	put('subjects/s/frames/b/frame.json');
	git(['add', '-A']);
	git(['commit', '-qm', 'b'], '2026-09-02T10:00:00Z');
	put('subjects/s/trails/t.json');
	put('subjects/s/frames/c/frame.json');
	git(['add', '-A']);
	git(['commit', '-qm', 't and c'], '2026-09-02T11:00:00Z');
	git(['checkout', '-q', 'main']);
	git(['merge', '--squash', '-q', 'sprint']);
	git(['commit', '-qm', 'sprint (#1)'], '2026-09-03T12:00:00-07:00');

	// An edit to a frame is not an addition; a rename is.
	put('subjects/s/frames/a/frame.json', '{"edited": true}');
	git(['add', '-A']);
	git(['commit', '-qm', 'edit a'], '2026-09-04T10:00:00Z');
	renameSync(join(repo, 'subjects/s/frames/c'), join(repo, 'subjects/s/frames/c2'));
	git(['add', '-A']);
	git(['commit', '-qm', 'rename c'], '2026-09-05T10:00:00Z');

	// Written, never committed: git has no date for it.
	put('subjects/s/frames/d/frame.json');
});

afterAll(() => rmSync(repo, { recursive: true, force: true }));

describe('added dates from git', () => {
	it('dates each frame and trail by the merge that brought it to the branch checked out', async () => {
		expect(await gitAddedDates(join(repo, 'subjects'))).toEqual({
			s: {
				frames: {
					a: '2026-09-01T10:00:00.000Z',
					// The squash merge, in UTC: not the branch's own commits.
					b: '2026-09-03T19:00:00.000Z',
					// Gone since, so never asked for; its rename is a new addition.
					c: '2026-09-03T19:00:00.000Z',
					c2: '2026-09-05T10:00:00.000Z'
				},
				trails: { t: '2026-09-03T19:00:00.000Z' }
			}
		});
	});

	it('sees nothing after the commit checked out: a publish of an older commit is capped at it', async () => {
		git(['checkout', '-q', 'HEAD~3']);
		try {
			expect(await gitAddedDates(join(repo, 'subjects'))).toEqual({
				s: { frames: { a: '2026-09-01T10:00:00.000Z' }, trails: {} }
			});
		} finally {
			git(['checkout', '-q', 'main']);
		}
	});

	it('is null outside a repository', async () => {
		const bare = mkdtempSync(join(tmpdir(), 'kloom-nohistory-'));
		try {
			expect(await gitAddedDates(bare)).toBeNull();
		} finally {
			rmSync(bare, { recursive: true, force: true });
		}
	});

	it('keeps a path’s first addition when it was added again later', () => {
		const log = [
			'\x012026-09-10T00:00:00Z',
			's/frames/a/frame.json',
			'',
			'\x012026-09-01T00:00:00Z',
			's/frames/a/frame.json',
			's/frames/a/reading.md',
			'other/notes.txt'
		].join('\n');
		expect(parseAdditions(log)).toEqual({
			s: { frames: { a: '2026-09-01T00:00:00.000Z' }, trails: {} }
		});
	});
});

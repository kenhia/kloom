import { mkdir, mkdtemp, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { afterAll, beforeAll, describe, expect, it } from 'vitest';
import { env } from '$env/dynamic/private';
import { listSubjects, subjectDirFor } from './config';

let root: string;
const saved = env.KLOOM_SUBJECTS_DIR;

beforeAll(async () => {
	root = await mkdtemp(join(tmpdir(), 'kloom-subjects-'));
	for (const [id, manifest] of [
		['beta', '{"title":"Beta"}'],
		['alpha', '{"title":"Alpha","subtitle":"The first"}'],
		['broken', '{'],
		['.hidden', '{"title":"Hidden"}'],
		['Upper', '{"title":"Upper"}'],
		['gamma', '{"title":"Gamma","subtitle":7}']
	]) {
		await mkdir(join(root, id));
		await writeFile(join(root, id, 'subject.json'), manifest);
	}
	await mkdir(join(root, 'empty'));
	await writeFile(join(root, 'stray.json'), '{}');
	env.KLOOM_SUBJECTS_DIR = root;
});
afterAll(() => {
	env.KLOOM_SUBJECTS_DIR = saved;
});

describe('the served subjects', () => {
	it('are the directories holding a readable subject.json, by id, with their titles and subtitles', async () => {
		expect(await listSubjects()).toEqual([
			{ id: 'alpha', title: 'Alpha', subtitle: 'The first' },
			{ id: 'beta', title: 'Beta' },
			{ id: 'gamma', title: 'Gamma' }
		]);
	});

	it('resolve an id to its directory, and nothing else to anything', async () => {
		expect(await subjectDirFor('alpha')).toBe(join(root, 'alpha'));
		for (const id of ['broken', 'empty', '.hidden', 'Upper', '..', 'alpha/..', '', null, 7])
			expect(await subjectDirFor(id)).toBeNull();
	});
});

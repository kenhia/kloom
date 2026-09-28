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
		['alpha', '{"title":"Alpha"}'],
		['broken', '{'],
		['.hidden', '{"title":"Hidden"}'],
		['Upper', '{"title":"Upper"}']
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
	it('are the directories holding a readable subject.json, by id, with their titles', async () => {
		expect(await listSubjects()).toEqual([
			{ id: 'alpha', title: 'Alpha' },
			{ id: 'beta', title: 'Beta' }
		]);
	});

	it('resolve an id to its directory, and nothing else to anything', async () => {
		expect(await subjectDirFor('alpha')).toBe(join(root, 'alpha'));
		for (const id of ['broken', 'empty', '.hidden', 'Upper', '..', 'alpha/..', '', null, 7])
			expect(await subjectDirFor(id)).toBeNull();
	});
});

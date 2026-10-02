import { mkdtemp } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { afterAll, beforeAll, describe, expect, it, vi } from 'vitest';

// korg 3486: a dev server reloads the server modules when their code changes.
// The reloaded grow-service must find the queue that is already running its
// jobs, not build a second one that resumes them beside the first.
describe('grow state across a module reload', () => {
	const before = process.env.KLOOM_DATA_DIR;
	beforeAll(async () => {
		process.env.KLOOM_DATA_DIR = await mkdtemp(join(tmpdir(), 'kloom-grow-reload-'));
	});
	afterAll(() => {
		if (before === undefined) delete process.env.KLOOM_DATA_DIR;
		else process.env.KLOOM_DATA_DIR = before;
	});

	it('keeps one queue per subject when the module is imported afresh', async () => {
		vi.resetModules();
		const first = await import('./grow-service');
		vi.resetModules();
		const reloaded = await import('./grow-service');
		expect(reloaded).not.toBe(first);
		expect(reloaded.growQueue('western-civ')).toBe(first.growQueue('western-civ'));
	});
});

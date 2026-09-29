import { execFileSync } from 'node:child_process';
import { mkdtempSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { afterEach, describe, expect, it } from 'vitest';
import { openReaderStore } from './reader-store';

/**
 * The review-notes skill's script (skills/review-notes/) runs under plain
 * Node, loading the store's SQLite adapter with its types stripped. This runs
 * it for real, so an adapter that stops loading that way fails here.
 */
const script = join(
	import.meta.dirname,
	'..',
	'..',
	'..',
	'skills',
	'review-notes',
	'review-notes.mjs'
);
const run = (data: string, ...args: string[]) =>
	execFileSync(process.execPath, [script, '--data', data, ...args], { encoding: 'utf8' });

let dir: string | undefined;
afterEach(() => {
	if (dir) rmSync(dir, { recursive: true, force: true });
});

describe('the review-notes script', () => {
	it('lists flagged notes across readers, and marks one handled', async () => {
		dir = mkdtempSync(join(tmpdir(), 'kloom-review-'));
		// A clock a second apart per write: notes saved in one millisecond would
		// otherwise tie on `created` and list in their random ids' order.
		let t = Date.parse('2026-09-28T12:00:00Z');
		const store = openReaderStore(join(dir, 'reader.db'), () => new Date((t += 1000)));
		const note = (text: string, flag: boolean) => ({
			subject: 'ai',
			frame: 'alexnet',
			label: 'AlexNet',
			text,
			flag
		});
		const flagged = (await store.saveNote('ken@github', note('Confusing wording.', true)))!;
		await store.saveNote('ada@github', note('Hers.', true));
		await store.saveNote('ken@github', note('Just a note.', false));
		const words = { exact: 'eight layers', prefix: 'It had ', suffix: '.', start: 7 };
		await store.saveNote('ada@github', { ...note('Which eight?', true), anchor: words });
		store.close();

		const listed = JSON.parse(run(dir, 'list', '--json'));
		expect(listed.map((n: { reader: string; text: string }) => [n.reader, n.text])).toEqual([
			['ken@github', 'Confusing wording.'],
			['ada@github', 'Hers.'],
			['ada@github', 'Which eight?']
		]);
		expect(listed[2].anchor).toEqual(words);
		const hers = run(dir, 'list', '--reader', 'ada@github');
		expect(hers).toMatch(/\(annotation\)\n[\s\S]*\n {2}> eight layers\n {2}\| Which eight\?/);
		expect(hers.split('(annotation)')).toHaveLength(2);
		expect(run(dir, 'list', '--reader', 'ken@github')).toContain(
			'content: subjects/ai/frames/alexnet/'
		);

		expect(run(dir, 'handle', 'ken@github', flagged.id, 'Reworded', 'it.')).toContain('Handled');
		expect(JSON.parse(run(dir, 'list', '--reader', 'ken@github', '--json'))).toEqual([]);
		const after = openReaderStore(join(dir, 'reader.db'));
		expect((await after.notes('ken@github', 'ai'))[0]).toMatchObject({
			review: 'handled',
			response: 'Reworded it.'
		});
		after.close();
	});

	it('refuses to handle a note that is not flagged, saying so', () => {
		dir = mkdtempSync(join(tmpdir(), 'kloom-review-'));
		expect(() => run(dir!, 'handle', 'ken@github', 'nope', 'done')).toThrow(/no flagged note/);
	});
});

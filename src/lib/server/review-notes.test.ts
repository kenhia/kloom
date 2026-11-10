import { execFileSync } from 'node:child_process';
import { mkdtempSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { afterEach, describe, expect, it } from 'vitest';
import { keptAnswer } from '$engine/ai/kept';
import { context } from '$engine/ai/fixture';
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

	it('lists kept answers readers asked to share, and passes or declines each (korg 3560)', async () => {
		dir = mkdtempSync(join(tmpdir(), 'kloom-review-'));
		let t = Date.parse('2026-09-28T12:00:00Z');
		const store = openReaderStore(join(dir, 'reader.db'), () => new Date((t += 1000)));
		const kept = (id: string, question: string) =>
			keptAnswer(
				{
					id,
					subject: 'western-civ',
					context,
					question,
					answer: 'Because ink [1].',
					provider: 'anthropic-api',
					model: 'claude-haiku-4-5',
					askedAt: '2026-09-27T17:05:09.000Z'
				},
				new Date('2026-09-27T17:06:00Z')
			);
		const one = '20260927T170509Z-00000001';
		const two = '20260927T170509Z-00000002';
		await store.keep('ken@github', kept(one, 'Why ink?'));
		await store.keep('ada@github', kept(two, 'Why paper?'));
		await store.keep('ada@github', kept('20260927T170509Z-00000003', 'Not shared.'));
		await store.shareKept('ken@github', 'western-civ', one, true);
		await store.shareKept('ada@github', 'western-civ', two, true);
		store.close();

		const listed = JSON.parse(run(dir, 'shares', '--json'));
		expect(
			listed.map((s: { reader: string; answer: { question: string } }) => [
				s.reader,
				s.answer.question
			])
		).toEqual([
			['ken@github', 'Why ink?'],
			['ada@github', 'Why paper?']
		]);
		const text = run(dir, 'shares', '--reader', 'ada@github');
		expect(text).toContain(`frame:   western-civ/${context.frame.id}`);
		expect(text).toContain('Q: Why paper?');
		expect(text).toMatch(/\| Because ink \[1\]\./);
		expect(text).toContain(`--seen ${listed[1].asked}`);

		expect(
			run(dir, 'review-share', 'ken@github', one, 'shared', 'Accurate.', '--seen', listed[0].asked)
		).toContain('Shared');
		expect(
			run(dir, 'review-share', 'ada@github', two, 'declined', 'Off', 'the', 'frame.')
		).toContain('Declined');
		expect(() => run(dir!, 'review-share', 'ken@github', one, 'shared', 'Again.')).toThrow(
			/no longer waiting/
		);
		expect(() => run(dir!, 'review-share', 'ken@github', one, 'maybe', 'Hm.')).toThrow(
			/shared or declined/
		);
		expect(JSON.parse(run(dir, 'shares', '--json'))).toEqual([]);
		const after = openReaderStore(join(dir, 'reader.db'));
		expect((await after.sharedOn('western-civ', context.frame.id)).map((s) => s.answer.id)).toEqual(
			[one]
		);
		expect((await after.keptOn('ada@github', 'western-civ', context.frame.id))[0]).toMatchObject({
			share: 'declined',
			shareResponse: 'Off the frame.'
		});
		after.close();
	});

	it('refuses to handle a note that is not flagged, saying so', () => {
		dir = mkdtempSync(join(tmpdir(), 'kloom-review-'));
		expect(() => run(dir!, 'handle', 'ken@github', 'nope', 'done')).toThrow(/no flagged note/);
	});
});

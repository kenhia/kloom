import { mkdtemp, readdir, readFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { describe, expect, it } from 'vitest';
import { context } from '$engine/ai/fixture';
import { keptAnswerProblems } from '$engine/ai/kept';
import type { AskStreamEvent, Provider, ProviderEvent } from '$engine/ai/provider';
import { TurnQueue } from '$engine/ai/queue';
import { askEvents, keep, ndjson, RecentAnswers } from './ask';

const provider = (events: ProviderEvent[], gate?: Promise<void>): Provider => ({
	name: 'fake',
	async *ask() {
		await gate;
		yield* events;
	}
});

const turn = (p: Provider, queue = new TurnQueue(), answers = new RecentAnswers()) => ({
	subject: 'western-civ',
	context,
	question: 'Why?',
	model: 'claude-sonnet-5',
	provider: p,
	queue,
	answers,
	signal: new AbortController().signal
});

async function collect(it: AsyncIterable<AskStreamEvent>) {
	const out: AskStreamEvent[] = [];
	for await (const e of it) out.push(e);
	return out;
}

describe('an ask turn', () => {
	it('names the answer, streams it, ends with done, and remembers it for keeping', async () => {
		const answers = new RecentAnswers();
		const events = await collect(
			askEvents(
				turn(
					provider([
						{ type: 'text', text: 'A ' },
						{ type: 'text', text: 'B [1]' }
					]),
					undefined,
					answers
				)
			)
		);
		expect(events.map((e) => e.type)).toEqual(['start', 'text', 'text', 'done']);
		const start = events[0] as Extract<AskStreamEvent, { type: 'start' }>;
		expect(start).toMatchObject({ model: 'claude-sonnet-5', frame: 'press' });
		expect(answers.get(start.id)?.answer).toBe('A B [1]');
	});

	it('does not remember a failed or empty answer', async () => {
		const answers = new RecentAnswers();
		const failed = await collect(
			askEvents(turn(provider([{ type: 'error', message: 'no' }]), undefined, answers))
		);
		expect(failed.map((e) => e.type)).toEqual(['start', 'error']);
		const empty = await collect(askEvents(turn(provider([]), undefined, answers)));
		expect(empty.at(-1)).toEqual({ type: 'error', message: 'The model gave an empty answer.' });
		expect(answers.get((failed[0] as { id: string }).id)).toBeUndefined();
	});

	it('says when it is queued behind another turn, and runs once that one finishes', async () => {
		const queue = new TurnQueue(1, 3);
		let open!: () => void;
		const first = collect(
			askEvents(
				turn(provider([{ type: 'text', text: '1' }], new Promise((r) => (open = r))), queue)
			)
		);
		await new Promise((r) => setImmediate(r));
		const second = collect(askEvents(turn(provider([{ type: 'text', text: '2' }]), queue)));
		await new Promise((r) => setImmediate(r));
		open();
		expect((await first).map((e) => e.type)).toEqual(['start', 'text', 'done']);
		expect((await second).map((e) => e.type)).toEqual(['start', 'queued', 'text', 'done']);
	});

	it('forgets answers past the limit or older than an hour', () => {
		const answers = new RecentAnswers(2);
		const at = '2026-09-27T17:00:00.000Z';
		for (const id of ['a', 'b', 'c'])
			answers.add({
				id,
				subject: 's',
				context,
				question: 'q',
				answer: 'x',
				provider: 'p',
				model: 'm',
				askedAt: at
			});
		expect(answers.get('a')).toBeUndefined();
		expect(answers.get('c', Date.parse(at) + 1000)).toBeDefined();
		expect(answers.get('c', Date.parse(at) + 61 * 60 * 1000)).toBeUndefined();
	});

	it('streams NDJSON', async () => {
		const res = new Response(
			ndjson(() => askEvents(turn(provider([{ type: 'text', text: 'x' }]))))
		);
		const lines = (await res.text())
			.trim()
			.split('\n')
			.map((l) => JSON.parse(l).type);
		expect(lines).toEqual(['start', 'text', 'done']);
	});
});

describe('keeping an answer', () => {
	it('writes one valid kept-answer file per answer, under the data directory', async () => {
		const data = await mkdtemp(join(tmpdir(), 'kloom-kept-'));
		const answer = {
			id: '20260927T170509Z-0a1b2c3d',
			subject: 'western-civ',
			context,
			question: 'Why?',
			answer: 'Ink [2].',
			provider: 'claude-cli',
			model: 'claude-sonnet-5',
			askedAt: '2026-09-27T17:05:09.000Z'
		};
		await keep(answer, data);
		await keep({ ...answer, answer: 'changed' }, data);
		const dir = join(data, 'western-civ', 'kept');
		expect(await readdir(dir)).toEqual(['20260927T170509Z-0a1b2c3d.json']);
		const file = JSON.parse(await readFile(join(dir, '20260927T170509Z-0a1b2c3d.json'), 'utf8'));
		expect(keptAnswerProblems(file)).toEqual([]);
		expect(file.answer).toBe('Ink [2].');
		expect(file.citations.map((c: { title: string }) => c.title)).toEqual(['Ink']);
	});
});

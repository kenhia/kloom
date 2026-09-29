import { describe, expect, it } from 'vitest';
import { context } from '$engine/ai/fixture';
import { keptAnswerProblems } from '$engine/ai/kept';
import type { AskStreamEvent, Provider, ProviderEvent } from '$engine/ai/provider';
import { TurnQueue } from '$engine/ai/queue';
import { askEvents, keep, ndjson, RecentAnswers } from './ask';
import { openReaderStore } from './reader-store';

const provider = (events: ProviderEvent[], gate?: Promise<void>): Provider => ({
	name: 'fake',
	// eslint-disable-next-line require-yield
	async *grow() {
		throw new Error('not in these tests');
	},
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

	it('drops text from before a web search, and remembers only the answer after it', async () => {
		const answers = new RecentAnswers();
		const events = await collect(
			askEvents({
				...turn(
					provider([
						{ type: 'text', text: 'Let me look.' },
						{ type: 'status', status: 'searching' },
						{ type: 'text', text: 'Found.' }
					]),
					undefined,
					answers
				),
				web: true
			})
		);
		const id = (events[0] as { id: string }).id;
		expect(answers.get(id)).toMatchObject({ answer: 'Found.', web: true });
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
	it('stores one valid kept answer per answer, in the reader’s store', async () => {
		const store = openReaderStore(':memory:');
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
		await keep(answer, 'ken@github', store);
		await keep({ ...answer, answer: 'changed' }, 'ken@github', store);
		const kept = await store.keptOn('ken@github', 'western-civ', context.frame.id);
		expect(kept).toHaveLength(1);
		const file = kept[0].answer;
		expect(keptAnswerProblems(file)).toEqual([]);
		expect(file.answer).toBe('Ink [2].');
		expect(file.citations.map((c: { title: string }) => c.title)).toEqual(['Ink']);
		expect(file).not.toHaveProperty('webCitations');
	});

	it('carries a web turn’s pages as citations, Wikipedia pinned to a revision', async () => {
		const store = openReaderStore(':memory:');
		const answer = {
			id: '20260927T170509Z-0a1b2c3d',
			subject: 'western-civ',
			context,
			question: 'What is new?',
			answer:
				'New [W1][W2].\n\n[W1] A news page — https://news.test/a\n[W2] Printing press - Wikipedia — https://en.wikipedia.org/wiki/Printing_press',
			provider: 'claude-cli',
			model: 'claude-sonnet-5',
			askedAt: '2026-09-27T17:05:09.000Z',
			web: true
		};
		const wiki = async () =>
			new Response(
				JSON.stringify({
					query: {
						pages: {
							'1': {
								title: 'Printing press',
								revisions: [{ revid: 42, timestamp: '2026-09-25T00:00:00Z' }]
							}
						}
					}
				})
			);
		const kept = await keep(answer, 'ken@github', store, new Date(), wiki);
		expect(keptAnswerProblems(kept)).toEqual([]);
		expect(kept.webCitations).toEqual([
			{ kind: 'web', title: 'A news page', url: 'https://news.test/a', accessed: '2026-09-27' },
			expect.objectContaining({
				kind: 'wikipedia',
				url: 'https://en.wikipedia.org/w/index.php?title=Printing_press&oldid=42'
			})
		]);
		const failing = async () => new Response('', { status: 503 });
		await expect(
			keep({ ...answer, id: '20260927T170509Z-0a1b2c3e' }, 'ken@github', store, new Date(), failing)
		).rejects.toThrow('503');
		expect(await store.keptCounts('ken@github', 'western-civ')).toEqual({ [context.frame.id]: 1 });
	});
});

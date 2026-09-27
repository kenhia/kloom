import { randomBytes } from 'node:crypto';
import { mkdir, writeFile } from 'node:fs/promises';
import { join } from 'node:path';
import { ClaudeCliProvider } from '$engine/ai/claude-cli';
import { answerId, keptAnswer, type Answer, type KeptAnswer } from '$engine/ai/kept';
import type { AskContext, AskStreamEvent, Provider } from '$engine/ai/provider';
import { QueueFull, TurnQueue } from '$engine/ai/queue';
import type { AppConfig } from './app-config';

/**
 * The server side of ask (docs/design.md §Ask): one turn at a time, the
 * answer streamed as NDJSON, and finished answers remembered for a while so
 * "keep this" can name one by id instead of sending its text back.
 */

/** Longest question accepted, in characters. */
export const MAX_QUESTION = 2000;

export const queue = new TurnQueue(1, 3);

let cached: { key: string; provider: Provider } | null = null;

/** The provider the app config names; rebuilt only when that part changes. */
export function providerFor(config: AppConfig): Provider {
	const key = JSON.stringify(config.provider);
	if (cached?.key !== key)
		cached = {
			key,
			provider: new ClaudeCliProvider({
				command: config.provider.command,
				timeoutMs: config.provider.timeoutSeconds * 1000
			})
		};
	return cached.provider;
}

/** Finished answers, newest last; the oldest go first, and after an hour. */
export class RecentAnswers {
	#byId = new Map<string, Answer>();

	constructor(
		readonly limit = 50,
		readonly ttlMs = 60 * 60 * 1000
	) {}

	add(a: Answer) {
		this.#byId.set(a.id, a);
		while (this.#byId.size > this.limit) this.#byId.delete(this.#byId.keys().next().value!);
	}

	get(id: string, now = Date.now()): Answer | undefined {
		const a = this.#byId.get(id);
		if (a && now - Date.parse(a.askedAt) > this.ttlMs) {
			this.#byId.delete(id);
			return undefined;
		}
		return a;
	}
}

export const answers = new RecentAnswers();

export interface AskTurn {
	subject: string;
	context: AskContext;
	question: string;
	model: string;
	provider: Provider;
	queue: TurnQueue;
	answers: RecentAnswers;
	signal: AbortSignal;
	now?: () => Date;
}

/** Run one turn as wire events. A complete answer is remembered for keeping. */
export async function* askEvents(t: AskTurn): AsyncIterable<AskStreamEvent> {
	const askedAt = (t.now ?? (() => new Date()))();
	const id = answerId(askedAt, randomBytes(4).toString('hex'));
	yield { type: 'start', id, model: t.model, frame: t.context.frame.id };

	if (t.queue.busy) yield { type: 'queued' };
	let release: () => void;
	try {
		release = await t.queue.acquire(t.signal);
	} catch (e) {
		if (e instanceof QueueFull) yield { type: 'error', message: e.message };
		return;
	}

	let text = '';
	try {
		for await (const event of t.provider.ask({
			context: t.context,
			question: t.question,
			model: t.model,
			signal: t.signal
		})) {
			yield event;
			if (event.type === 'error') return;
			text += event.text;
		}
	} finally {
		release();
	}
	if (t.signal.aborted) return;
	if (!text.trim()) {
		yield { type: 'error', message: 'The model gave an empty answer.' };
		return;
	}
	t.answers.add({
		id,
		subject: t.subject,
		context: t.context,
		question: t.question,
		answer: text,
		provider: t.provider.name,
		model: t.model,
		askedAt: askedAt.toISOString()
	});
	yield { type: 'done' };
}

/** NDJSON over a byte stream; cancelling it (the reader went away) aborts the turn. */
export function ndjson(events: (signal: AbortSignal) => AsyncIterable<AskStreamEvent>) {
	const abort = new AbortController();
	const encoder = new TextEncoder();
	return new ReadableStream<Uint8Array>({
		async start(controller) {
			try {
				for await (const e of events(abort.signal))
					controller.enqueue(encoder.encode(`${JSON.stringify(e)}\n`));
			} catch (e) {
				console.error('ask failed', e);
				if (!abort.signal.aborted)
					controller.enqueue(
						encoder.encode(`${JSON.stringify({ type: 'error', message: 'Asking failed.' })}\n`)
					);
			}
			if (!abort.signal.aborted) controller.close();
		},
		cancel() {
			abort.abort();
		}
	});
}

/**
 * Write a kept answer to `<dataDir>/<subject>/kept/<id>.json`. Keeping the
 * same answer twice is not an error: the first file stands.
 */
export async function keep(answer: Answer, dataDir: string, now = new Date()): Promise<KeptAnswer> {
	const kept = keptAnswer(answer, now);
	const dir = join(dataDir, answer.subject, 'kept');
	await mkdir(dir, { recursive: true });
	try {
		await writeFile(join(dir, `${answer.id}.json`), `${JSON.stringify(kept, null, '\t')}\n`, {
			flag: 'wx'
		});
	} catch (e) {
		if ((e as NodeJS.ErrnoException).code !== 'EEXIST') throw e;
	}
	return kept;
}

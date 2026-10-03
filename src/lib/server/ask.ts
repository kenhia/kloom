import { randomBytes } from 'node:crypto';
import { makeProvider } from '$edition/providers';
import { answerId, keptAnswer, type Answer, type KeptAnswer } from '$engine/ai/kept';
import { webReferences } from '$engine/ai/prompt';
import { pinWikipedia, wikipediaArticle, type Fetch } from '$engine/ai/wikipedia';
import type { Citation } from '$engine/model';
import type { AskContext, AskStreamEvent, AskUsage, Provider } from '$engine/ai/provider';
import type { ReaderStore } from '$engine/reader-data';
import { QueueFull, TurnQueue } from '$engine/ai/queue';
import { modelId, type AppConfig, type AskCaps, type ModelEntry, type Prices } from './app-config';
import { askCostUsd, standing, usageColumns, type AskLedger } from './ask-ledger';

/**
 * The server side of ask (docs/design.md §Ask): one turn at a time, the
 * answer streamed as NDJSON, and finished answers remembered for a while so
 * "keep this" can name one by id instead of sending its text back.
 */

/** Longest question accepted, in characters. */
export const MAX_QUESTION = 2000;

export const queue = new TurnQueue(1, 3);

const cached = new Map<string, { key: string; provider: Provider }>();

/**
 * The provider that runs a model entry, as the app config describes it;
 * each is rebuilt only when its part of the config changes.
 */
export function providerFor(config: AppConfig, entry: ModelEntry): Provider {
	const p = config.providers.find((x) => x.id === entry.provider)!;
	const fallbacks = config.models.filter((m) => m.provider === p.id && m.fallbacks).map(modelId);
	const key = JSON.stringify([p, fallbacks]);
	let c = cached.get(p.id);
	if (c?.key !== key) cached.set(p.id, (c = { key, provider: makeProvider(p, config) }));
	return c.provider;
}

/** Grow's provider: `claude -p` (the config checks grow's models are on it). */
export function growProvider(config: AppConfig): Provider {
	const id = config.models.find((m) => m.id === config.grow?.defaultModel)?.provider;
	return providerFor(config, { id: '', label: '', provider: id ?? config.providers[0].id });
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
	/** The model id the provider is given. */
	model: string;
	/** Already checked against the app config (`resolveWeb`). */
	web?: boolean;
	provider: Provider;
	queue: TurnQueue;
	answers: RecentAnswers;
	signal: AbortSignal;
	now?: () => Date;
	/**
	 * Where a turn that reports its usage is logged, priced from `prices`
	 * (docs/design.md §Ask costs), and who asked. With `caps`, the reader's
	 * standing follows the answer.
	 */
	cost?: { ledger: AskLedger; prices: Prices; reader: string; caps?: AskCaps };
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
	let usage: AskUsage | null = null;
	let outcome = 'done';
	const started = performance.now();
	try {
		for await (const event of t.provider.ask({
			context: t.context,
			question: t.question,
			model: t.model,
			web: t.web ?? false,
			signal: t.signal
		})) {
			// What it cost stays on the server.
			if (event.type === 'usage') {
				usage = event.usage;
				continue;
			}
			yield event;
			if (event.type === 'error') {
				outcome = event.declined ? 'declined' : 'failed';
				return;
			}
			// Text before a search was thinking aloud; the answer starts after it.
			if (event.type === 'status') text = '';
			else text += event.text;
		}
	} finally {
		release();
		if (t.signal.aborted && outcome === 'done') outcome = 'stopped';
		if (usage && t.cost) logCost(t, askedAt, usage, performance.now() - started, outcome);
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
		askedAt: askedAt.toISOString(),
		web: t.web ?? false
	});
	if (t.cost?.caps) {
		const { state, until } = standing(t.cost.ledger, t.cost.reader, t.cost.caps, t.now?.());
		yield { type: 'budget', budget: { state, until } };
	}
	yield { type: 'done' };
}

/** One row in the cost log; a failure to write it is reported, never the reader's problem. */
function logCost(t: AskTurn, at: Date, usage: AskUsage, ms: number, outcome: string) {
	const { ledger, prices, reader } = t.cost!;
	try {
		ledger.log({
			at: at.toISOString(),
			reader,
			subject: t.subject,
			frame: t.context.frame.id,
			provider: t.provider.name,
			model: t.model,
			web: t.web ?? false,
			...usageColumns(usage),
			ms,
			usd: askCostUsd(usage, prices),
			outcome
		});
	} catch (e) {
		console.error('ask: could not log the cost', e);
	}
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
 * The pages a web turn listed, as citations accessed on the day it was asked.
 * A Wikipedia page is pinned to its current revision, and a failed lookup
 * fails the keep rather than storing an unpinned link. Undefined for a turn
 * that had no web.
 */
export async function webCitations(
	answer: Answer,
	fetcher?: Fetch
): Promise<Citation[] | undefined> {
	if (!answer.web) return undefined;
	const accessed = answer.askedAt.slice(0, 10);
	return Promise.all(
		webReferences(answer.answer).map((r) =>
			wikipediaArticle(r.url)
				? pinWikipedia(r.url, accessed, fetcher)
				: ({ kind: 'web', title: r.title, url: r.url, accessed } satisfies Citation)
		)
	);
}

/**
 * Keep an answer for `reader`, in their store (docs/design.md §Reader data).
 * Keeping the same answer twice is not an error: the first one stands.
 */
export async function keep(
	answer: Answer,
	reader: string,
	store: ReaderStore,
	now = new Date(),
	fetcher?: Fetch
): Promise<KeptAnswer> {
	const kept = keptAnswer(answer, now, await webCitations(answer, fetcher));
	await store.keep(reader, kept);
	return kept;
}

import Anthropic from '@anthropic-ai/sdk';
import type {
	BetaMessage,
	BetaMessageParam,
	BetaRawMessageStreamEvent,
	BetaToolUnion,
	BetaMessageStreamParams
} from '@anthropic-ai/sdk/resources/beta/messages/messages';
import { askPrompt, askSystem } from './prompt';
import type { AskRequest, AskUsage, Provider, ProviderEvent, TokenUse } from './provider';

/**
 * The second provider adapter: the Claude API, through the official SDK, with
 * an API key (korg 3529). Same prompt, same events, as `claude -p`; it adds
 * what a key that is billed per use needs, the turn's usage, which the server
 * prices and logs (docs/design.md §Ask costs). Ask only: grow stays on
 * `claude -p`, whose file tools it needs.
 */

/** The web's caps on a turn (korg 3529, measured 2026-10-03): what keeps a question from costing dollars. */
export interface WebCaps {
	searchMaxUses: number;
	fetchMaxUses: number;
	/** The most of one page a fetch reads, in tokens. */
	fetchMaxContentTokens: number;
}

export const DEFAULT_WEB_CAPS: WebCaps = {
	searchMaxUses: 3,
	fetchMaxUses: 2,
	fetchMaxContentTokens: 8000
};

/** What the adapter needs of the SDK's client: the beta stream (for `fallbacks`). */
export interface StreamingClient {
	beta: {
		messages: {
			stream(
				params: BetaMessageStreamParams,
				options?: { signal?: AbortSignal; timeout?: number }
			): AsyncIterable<BetaRawMessageStreamEvent> & { finalMessage(): Promise<BetaMessage> };
		};
	};
}

export interface AnthropicApiOptions {
	/** The key, read per turn, so a rotated key needs no restart; undefined when there is none. */
	apiKey: () => string | undefined;
	timeoutMs?: number;
	webTimeoutMs?: number;
	web?: WebCaps;
	/**
	 * Model ids whose turns send the server-side refusal fallback (`fallbacks:
	 * "default"`, korg 3529): a declined turn is re-run by the API on a model
	 * that will answer.
	 */
	fallbacks?: (model: string) => boolean;
	/** For tests: the client a key makes. */
	client?: (apiKey: string) => StreamingClient;
}

/** The beta header the `"default"` fallback mode needs. */
export const FALLBACK_BETA = 'server-side-fallback-2026-07-01';

/** The most a turn may write; an ask is short, and thinking counts against it. */
const MAX_TOKENS = 16000;

/** A server-tool turn can pause; it is resumed this many times at most. */
const MAX_CONTINUATIONS = 4;

/**
 * Whether a model takes the web tools' dynamic-filtering versions
 * (`_20260209`): Sonnet and Opus 4.6 and later, and Fable and Mythos. Older
 * models, Haiku 4.5 among them, take the basic ones.
 */
export const DYNAMIC_WEB = /^claude-(opus-(5|4-[6-9])|sonnet-(5|4-[6-9])|fable-|mythos-)/;

/** The web tools for a turn on `model`, capped. */
export function webTools(model: string, caps: WebCaps = DEFAULT_WEB_CAPS): BetaToolUnion[] {
	const dynamic = DYNAMIC_WEB.test(model);
	return [
		{
			type: dynamic ? 'web_search_20260209' : 'web_search_20250305',
			name: 'web_search',
			max_uses: caps.searchMaxUses
		},
		{
			type: dynamic ? 'web_fetch_20260209' : 'web_fetch_20250910',
			name: 'web_fetch',
			max_uses: caps.fetchMaxUses,
			max_content_tokens: caps.fetchMaxContentTokens
		}
	];
}

/**
 * One response's usage, by model. A response that lists its iterations
 * (a server-tool loop, a fallback) is counted from them, each under the
 * model that served it; otherwise from the top-level block.
 */
export function messageUsage(message: BetaMessage): AskUsage {
	const u = message.usage;
	const tokens: TokenUse[] = [];
	const add = (
		model: string,
		x: {
			input_tokens?: number | null;
			output_tokens?: number | null;
			cache_read_input_tokens?: number | null;
			cache_creation_input_tokens?: number | null;
		}
	) => {
		let t = tokens.find((y) => y.model === model);
		if (!t) tokens.push((t = { model, input: 0, output: 0, cacheRead: 0, cacheWrite: 0 }));
		t.input += x.input_tokens ?? 0;
		t.output += x.output_tokens ?? 0;
		t.cacheRead += x.cache_read_input_tokens ?? 0;
		t.cacheWrite += x.cache_creation_input_tokens ?? 0;
	};
	const sampled = (u.iterations ?? []).filter(
		(i) => i.type === 'message' || i.type === 'fallback_message'
	);
	if (sampled.length)
		for (const i of sampled) add(('model' in i && i.model) || message.model, i as never);
	else add(message.model, u);
	return {
		tokens,
		webSearches: u.server_tool_use?.web_search_requests ?? 0,
		webFetches: u.server_tool_use?.web_fetch_requests ?? 0
	};
}

/** Two usages as one. */
export function addUsage(a: AskUsage, b: AskUsage): AskUsage {
	const tokens = a.tokens.map((t) => ({ ...t }));
	for (const t of b.tokens) {
		const same = tokens.find((x) => x.model === t.model);
		if (!same) tokens.push({ ...t });
		else for (const k of ['input', 'output', 'cacheRead', 'cacheWrite'] as const) same[k] += t[k];
	}
	return {
		tokens,
		webSearches: a.webSearches + b.webSearches,
		webFetches: a.webFetches + b.webFetches
	};
}

/** What an API failure says to the reader: plain, and never the key. */
export function apiErrorMessage(e: unknown): string {
	if (e instanceof Anthropic.APIConnectionTimeoutError) return 'The model took too long to answer.';
	if (e instanceof Anthropic.APIConnectionError) return 'Could not reach the Claude API.';
	if (e instanceof Anthropic.AuthenticationError)
		return 'The Claude API refused the key ask is configured with.';
	if (e instanceof Anthropic.PermissionDeniedError)
		return 'The Claude API refused this request (permission).';
	if (e instanceof Anthropic.RateLimitError)
		return 'The Claude API is busy or at its spend limit; try again later.';
	if (e instanceof Anthropic.BadRequestError)
		return 'The Claude API refused the request as malformed.';
	if (e instanceof Anthropic.APIError)
		return `The Claude API answered with an error (${e.status ?? 'no status'}).`;
	return 'Asking the Claude API failed.';
}

export class AnthropicApiProvider implements Provider {
	readonly name = 'anthropic-api';
	readonly #o: Required<Omit<AnthropicApiOptions, 'client' | 'fallbacks'>> &
		Pick<AnthropicApiOptions, 'fallbacks'>;
	readonly #client: (apiKey: string) => StreamingClient;
	#made: { key: string; client: StreamingClient } | null = null;

	constructor(options: AnthropicApiOptions) {
		this.#o = {
			timeoutMs: 120_000,
			webTimeoutMs: 180_000,
			web: DEFAULT_WEB_CAPS,
			...options
		};
		// The SDK retries a 429, a 5xx or a dropped connection twice itself.
		this.#client =
			options.client ?? ((apiKey) => new Anthropic({ apiKey }) as unknown as StreamingClient);
	}

	#clientFor(key: string): StreamingClient {
		if (this.#made?.key !== key) this.#made = { key, client: this.#client(key) };
		return this.#made.client;
	}

	async *ask({ context, question, model, web, signal }: AskRequest): AsyncIterable<ProviderEvent> {
		if (signal?.aborted) return;
		const key = this.#o.apiKey();
		if (!key) {
			yield { type: 'error', message: 'Ask has no Claude API key configured.' };
			return;
		}
		const client = this.#clientFor(key);
		const fallback = this.#o.fallbacks?.(model) ?? false;
		const params: BetaMessageStreamParams = {
			model,
			max_tokens: MAX_TOKENS,
			system: askSystem(web),
			messages: [{ role: 'user', content: askPrompt(context, question, web) }],
			...(web ? { tools: webTools(model, this.#o.web) } : {}),
			...(fallback ? { betas: [FALLBACK_BETA], fallbacks: 'default' as const } : {})
		};
		const timeout = web ? this.#o.webTimeoutMs : this.#o.timeoutMs;

		let usage: AskUsage | null = null;
		let searching = false;
		try {
			for (let turn = 0; turn <= MAX_CONTINUATIONS; turn++) {
				const stream = client.beta.messages.stream(params, { signal, timeout });
				for await (const event of stream) {
					if (event.type === 'content_block_start') {
						const block = event.content_block;
						if (block.type === 'server_tool_use') {
							// Text before a search was the model thinking aloud.
							if (!searching) yield { type: 'status', status: 'searching' };
							searching = true;
						} else if (block.type === 'fallback') {
							// Another model starts the answer again; what came before was declined.
							yield { type: 'status', status: 'retrying' };
						}
					} else if (event.type === 'content_block_delta' && event.delta.type === 'text_delta') {
						if (!event.delta.text) continue;
						searching = false;
						yield { type: 'text', text: event.delta.text };
					}
				}
				const message = await stream.finalMessage();
				const used = messageUsage(message);
				usage = usage ? addUsage(usage, used) : used;
				if (message.stop_reason === 'refusal') {
					yield { type: 'usage', usage };
					yield {
						type: 'error',
						message: 'Claude declined to answer this question. Try asking it another way.',
						declined: true
					};
					return;
				}
				if (message.stop_reason !== 'pause_turn') break;
				// A paused server-tool turn goes on from where it stopped.
				params.messages = [
					...params.messages,
					{ role: 'assistant', content: message.content } as BetaMessageParam
				];
			}
		} catch (e) {
			if (usage) yield { type: 'usage', usage };
			if (signal?.aborted || e instanceof Anthropic.APIUserAbortError) return;
			console.error('anthropic-api: ask failed', e instanceof Error ? e.message : e);
			yield { type: 'error', message: apiErrorMessage(e) };
			return;
		}
		// An empty answer is the server's to report (askEvents), as for any adapter.
		if (usage) yield { type: 'usage', usage };
	}

	async *grow(): AsyncIterable<ProviderEvent> {
		yield { type: 'error', message: 'Grow runs on claude -p, not the API provider.' };
	}
}

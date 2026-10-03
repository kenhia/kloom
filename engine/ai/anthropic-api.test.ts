import Anthropic from '@anthropic-ai/sdk';
import type {
	BetaMessage,
	BetaMessageStreamParams,
	BetaRawMessageStreamEvent
} from '@anthropic-ai/sdk/resources/beta/messages/messages';
import { describe, expect, it } from 'vitest';
import {
	AnthropicApiProvider,
	apiErrorMessage,
	FALLBACK_BETA,
	messageUsage,
	webTools,
	type StreamingClient
} from './anthropic-api';
import { context } from './fixture';
import type { ProviderEvent } from './provider';

/** One response from the fake API: the events it streams and the message it ends with. */
interface Turn {
	events: object[];
	message: Partial<BetaMessage>;
}

const text = (t: string) => ({
	type: 'content_block_delta',
	index: 0,
	delta: { type: 'text_delta', text: t }
});
const block = (type: string) => ({
	type: 'content_block_start',
	index: 0,
	content_block: { type }
});
const usage = (input: number, output: number, extra: object = {}) => ({
	input_tokens: input,
	output_tokens: output,
	cache_read_input_tokens: 0,
	cache_creation_input_tokens: 0,
	...extra
});
const done = (u = usage(100, 20), stop = 'end_turn', model = 'claude-haiku-4-5') => ({
	model,
	stop_reason: stop as BetaMessage['stop_reason'],
	content: [],
	usage: u as BetaMessage['usage']
});

/** A client that replays `turns` in order and records what it was asked. */
function fakeClient(turns: Turn[] | (() => never)) {
	const calls: BetaMessageStreamParams[] = [];
	const client: StreamingClient = {
		beta: {
			messages: {
				stream(params) {
					calls.push(structuredClone(params));
					if (typeof turns === 'function') turns();
					const t = (turns as Turn[])[calls.length - 1];
					return {
						async *[Symbol.asyncIterator]() {
							yield* t.events as BetaRawMessageStreamEvent[];
						},
						finalMessage: async () => t.message as BetaMessage
					};
				}
			}
		}
	};
	return { client, calls };
}

async function run(
	turns: Turn[] | (() => never),
	{ model = 'claude-haiku-4-5', web = false, key = 'k', fallbacks = false } = {}
) {
	const { client, calls } = fakeClient(turns);
	const provider = new AnthropicApiProvider({
		apiKey: () => (key ? key : undefined),
		client: () => client,
		fallbacks: () => fallbacks
	});
	const events: ProviderEvent[] = [];
	for await (const e of provider.ask({ context, question: 'Why?', model, web })) events.push(e);
	return { events, calls };
}

describe('the Claude API adapter (korg 3529)', () => {
	it('streams the answer with ask’s own prompt, then reports its usage', async () => {
		const { events, calls } = await run([
			{ events: [text('Fire '), text('[1]')], message: done() }
		]);
		expect(events).toEqual([
			{ type: 'text', text: 'Fire ' },
			{ type: 'text', text: '[1]' },
			{
				type: 'usage',
				usage: {
					tokens: [
						{ model: 'claude-haiku-4-5', input: 100, output: 20, cacheRead: 0, cacheWrite: 0 }
					],
					webSearches: 0,
					webFetches: 0
				}
			}
		]);
		expect(calls[0]).toMatchObject({ model: 'claude-haiku-4-5', max_tokens: 16000 });
		expect(calls[0].system).toContain('inside kloom');
		expect(JSON.stringify(calls[0].messages)).toContain('--- Question ---');
		expect(calls[0].tools).toBeUndefined();
		expect(calls[0]).not.toHaveProperty('fallbacks');
	});

	it('offers the capped web tools on a web turn, the basic versions to Haiku', async () => {
		const haiku = await run([{ events: [text('x')], message: done() }], { web: true });
		expect(haiku.calls[0].tools).toEqual([
			{ type: 'web_search_20250305', name: 'web_search', max_uses: 3 },
			{ type: 'web_fetch_20250910', name: 'web_fetch', max_uses: 2, max_content_tokens: 8000 }
		]);
		expect(haiku.calls[0].system).toContain('search and read the web');
		expect(webTools('claude-sonnet-5-5').map((t) => t.type)).toEqual([
			'web_search_20260209',
			'web_fetch_20260209'
		]);
		expect(webTools('claude-opus-4-6')[0].type).toBe('web_search_20260209');
		expect(webTools('claude-sonnet-4-5')[0].type).toBe('web_search_20250305');
	});

	it('says it is searching, once, so the text before it is dropped', async () => {
		const { events } = await run(
			[
				{
					events: [
						text('Let me look.'),
						block('server_tool_use'),
						block('web_search_tool_result'),
						block('server_tool_use'),
						text('Found it.')
					],
					message: done(
						usage(9000, 300, { server_tool_use: { web_search_requests: 2, web_fetch_requests: 0 } })
					)
				}
			],
			{ web: true }
		);
		expect(events.slice(0, 3)).toEqual([
			{ type: 'text', text: 'Let me look.' },
			{ type: 'status', status: 'searching' },
			{ type: 'text', text: 'Found it.' }
		]);
		expect(events.at(-1)).toMatchObject({ type: 'usage', usage: { webSearches: 2 } });
	});

	it('resumes a paused server-tool turn, and adds up both requests', async () => {
		const { events, calls } = await run(
			[
				{ events: [block('server_tool_use')], message: done(usage(5000, 50), 'pause_turn') },
				{ events: [text('Answer.')], message: done(usage(6000, 80)) }
			],
			{ web: true }
		);
		expect(calls).toHaveLength(2);
		expect(calls[1].messages.at(-1)?.role).toBe('assistant');
		expect(events.at(-1)).toMatchObject({
			type: 'usage',
			usage: { tokens: [{ input: 11000, output: 130 }] }
		});
	});

	it('sends the refusal fallback where the config asks, and starts again after a switch', async () => {
		const { events, calls } = await run(
			[
				{
					events: [text('I can'), block('fallback'), text('Here is the answer.')],
					message: done(
						usage(10, 10, {
							iterations: [
								{ type: 'message', model: 'claude-sonnet-5-5', ...usage(400, 5) },
								{ type: 'fallback_message', model: 'claude-opus-4-8', ...usage(400, 60) }
							]
						}),
						'end_turn',
						'claude-opus-4-8'
					)
				}
			],
			{ model: 'claude-sonnet-5-5', fallbacks: true }
		);
		expect(calls[0]).toMatchObject({ betas: [FALLBACK_BETA], fallbacks: 'default' });
		expect(events[1]).toEqual({ type: 'status', status: 'retrying' });
		// Each model's tokens under its own name, so each is priced at its own rate.
		expect(events.at(-1)).toMatchObject({
			type: 'usage',
			usage: {
				tokens: [
					{ model: 'claude-sonnet-5-5', input: 400, output: 5 },
					{ model: 'claude-opus-4-8', input: 400, output: 60 }
				]
			}
		});
	});

	it('says plainly when Claude declines, after logging what it cost', async () => {
		const { events } = await run([{ events: [], message: done(usage(300, 2), 'refusal') }]);
		expect(events.map((e) => e.type)).toEqual(['usage', 'error']);
		expect(events[1]).toMatchObject({ declined: true, message: expect.stringMatching(/declined/) });
	});

	it('fails plainly with no key, or when the API refuses one, and never names it', async () => {
		expect((await run([], { key: '' })).events).toEqual([
			{ type: 'error', message: 'Ask has no Claude API key configured.' }
		]);
		const refused = await run(() => {
			throw new Anthropic.AuthenticationError(
				401,
				{ error: {} },
				'invalid x-api-key',
				new Headers()
			);
		});
		expect(refused.events).toEqual([
			{ type: 'error', message: 'The Claude API refused the key ask is configured with.' }
		]);
		expect(apiErrorMessage(new Anthropic.RateLimitError(429, {}, 'slow', new Headers()))).toMatch(
			/busy or at its spend limit/
		);
	});

	it('counts usage from the top level when there are no iterations', () => {
		expect(
			messageUsage(done(usage(10, 2, { cache_read_input_tokens: 7 })) as unknown as BetaMessage)
				.tokens
		).toEqual([{ model: 'claude-haiku-4-5', input: 10, output: 2, cacheRead: 7, cacheWrite: 0 }]);
	});
});

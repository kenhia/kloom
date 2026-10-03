import { error, type RequestEvent } from '@sveltejs/kit';
import { askContext } from '$engine/ai/context';
import type { AskStreamEvent } from '$engine/ai/provider';
import { loadAppConfig, resolveModel, resolveWeb, modelId } from './app-config';
import { answers, askEvents, MAX_QUESTION, ndjson, providerFor, queue } from './ask';
import { standing } from './ask-ledger';
import { askLedger } from './reader-store';
import { servedSource, servedSubject } from './subject';

const NDJSON = { 'content-type': 'application/x-ndjson', 'cache-control': 'no-store' };

/**
 * Ask: `{subject, frame, trail, question, model, web}` in, the answer out as
 * NDJSON (`AskStreamEvent`s), for either edition. The frame's content comes
 * from the library, not the client; the model is honoured only if the app
 * config lists it, and `web` only if the config does not deny it. A turn on
 * a provider that bills by use is priced and logged under the reader who
 * asked (§Ask costs); with caps in the config, a reader at either cap gets
 * a `resting` budget and no turn (§Ask on the reader site).
 */
export async function ask({ request }: RequestEvent, reader: string): Promise<Response> {
	const body = (await request.json().catch(() => null)) as Record<string, unknown> | null;
	const question = typeof body?.question === 'string' ? body.question.trim() : '';
	if (!question) error(400, 'A question is required.');
	if (question.length > MAX_QUESTION)
		error(400, `Questions are limited to ${MAX_QUESTION} characters.`);

	const subject = await servedSubject(body?.subject);
	const frame = typeof body?.frame === 'string' ? body.frame : '';
	const source = Object.hasOwn(subject.frames, frame)
		? await servedSource(subject.id, frame)
		: null;
	const context = source && askContext(subject, frame, body?.trail, source);
	if (!context) error(400, 'Unknown frame or trail.');

	if (queue.busy && queue.waiting >= queue.maxWaiting)
		error(503, 'Too many questions are waiting; try again in a moment.');

	const config = await loadAppConfig();
	const caps = config.ask.caps;
	if (caps) {
		const { state, until } = standing(askLedger(), reader, caps);
		if (state === 'resting') {
			const rest: AskStreamEvent = { type: 'budget', budget: { state, until } };
			return new Response(`${JSON.stringify(rest)}\n`, { headers: NDJSON });
		}
	}
	const entry = resolveModel(config, body?.model);
	const turn = {
		subject: subject.id,
		context,
		question,
		model: modelId(entry),
		web: resolveWeb(config, body?.web),
		provider: providerFor(config, entry),
		queue,
		answers,
		cost: config.prices ? { ledger: askLedger(), prices: config.prices, reader, caps } : undefined
	};
	return new Response(
		ndjson((signal) => askEvents({ ...turn, signal })),
		{ headers: NDJSON }
	);
}

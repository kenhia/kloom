import { error } from '@sveltejs/kit';
import { basename } from 'node:path';
import { askContext } from '$engine/ai/context';
import { loadSubject, readReading } from '$engine/load';
import { loadAppConfig, resolveModel } from '$lib/server/app-config';
import { answers, askEvents, MAX_QUESTION, ndjson, providerFor, queue } from '$lib/server/ask';
import { subjectDir } from '$lib/server/config';
import type { RequestHandler } from './$types';

/**
 * Ask: `{frame, trail, question, model}` in, the answer out as NDJSON
 * (`AskStreamEvent`s). The frame's content comes from disk, not the client,
 * and the model is honoured only if the app config lists it.
 */
export const POST: RequestHandler = async ({ request }) => {
	const body = (await request.json().catch(() => null)) as Record<string, unknown> | null;
	const question = typeof body?.question === 'string' ? body.question.trim() : '';
	if (!question) error(400, 'A question is required.');
	if (question.length > MAX_QUESTION)
		error(400, `Questions are limited to ${MAX_QUESTION} characters.`);

	const dir = subjectDir();
	const subject = await loadSubject(dir);
	const frame = typeof body?.frame === 'string' ? body.frame : '';
	const reading = Object.hasOwn(subject.frames, frame) ? await readReading(dir, frame) : null;
	const context = reading === null ? null : askContext(subject, frame, body?.trail, reading);
	if (!context) error(400, 'Unknown frame or trail.');

	if (queue.busy && queue.waiting >= queue.maxWaiting)
		error(503, 'Too many questions are waiting; try again in a moment.');

	const config = await loadAppConfig();
	const turn = {
		subject: basename(dir),
		context,
		question,
		model: resolveModel(config, body?.model),
		provider: providerFor(config),
		queue,
		answers
	};
	return new Response(
		ndjson((signal) => askEvents({ ...turn, signal })),
		{ headers: { 'content-type': 'application/x-ndjson', 'cache-control': 'no-store' } }
	);
};

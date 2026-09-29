import { error, json } from '@sveltejs/kit';
import { GROW_VERBS, type GrowVerb } from '$engine/ai/grow';
import { ANSWER_ID } from '$engine/ai/kept';
import { loadAppConfig, resolveModel } from '$lib/server/app-config';
import { providerFor } from '$lib/server/ask';
import { growQueue, readKept } from '$lib/server/grow-service';
import { mainSpineFrames } from '$lib/server/grow';
import { requireSubjectDir, servedSubject } from '$lib/server/subject';
import type { RequestHandler } from './$types';

/** Longest request accepted, in characters. */
const MAX_REQUEST = 2000;

/** A subject's recent grow jobs (`?subject=`), newest first; the AI pane polls this while one runs. */
export const GET: RequestHandler = async ({ url }) => {
	const name = url.searchParams.get('subject');
	await requireSubjectDir(name);
	const queue = growQueue(name!);
	await queue.load();
	return json({ jobs: queue.list(10) }, { headers: { 'cache-control': 'no-store' } });
};

/**
 * Queue a grow job: `{subject, verb, frame, request, kept, model}`. The anchor is the
 * frame, or the kept answer's own frame; the model is honoured only if the
 * app config lists it, and is fixed for the job from here on.
 */
export const POST: RequestHandler = async ({ request, locals }) => {
	const config = await loadAppConfig();
	if (!config.grow) error(503, 'Grow is not configured.');
	const body = (await request.json().catch(() => null)) as Record<string, unknown> | null;

	const verb = body?.verb as GrowVerb;
	if (!GROW_VERBS.includes(verb)) error(400, `verb must be one of ${GROW_VERBS.join(', ')}.`);
	const text = typeof body?.request === 'string' ? body.request.trim() : '';
	if (text.length > MAX_REQUEST) error(400, `Requests are limited to ${MAX_REQUEST} characters.`);

	const subject = await servedSubject(body?.subject);
	const name = subject.id;
	let anchor = typeof body?.frame === 'string' ? body.frame : '';
	let kept: string | null = null;
	if (body?.kept !== undefined && body.kept !== null) {
		if (typeof body.kept !== 'string' || !ANSWER_ID.test(body.kept))
			error(400, 'kept must be a kept answer id.');
		// The hook refused a write without a reader, so there is one.
		const file = await readKept(locals.reader!.login, name, body.kept);
		if (!file) error(404, 'That kept answer is gone or malformed.');
		kept = body.kept;
		anchor = file.anchor.frame;
	} else if (!text) error(400, 'Say what to grow.');
	if (!Object.hasOwn(subject.frames, anchor)) error(400, 'Unknown frame.');
	if (verb === 'trail' && !mainSpineFrames(subject.spine).includes(anchor))
		error(400, 'A trail branches from a frame on the main spine.');

	try {
		const job = await growQueue(name).add({
			subject: name,
			verb,
			anchor,
			request: text,
			kept,
			provider: providerFor(config).name,
			model: resolveModel(config, body?.model, config.grow.defaultModel),
			web: config.grow.web,
			// The hook refused a request without a reader, so there is one.
			...(locals.reader ? { by: locals.reader } : {})
		});
		return json({ job }, { status: 202 });
	} catch (e) {
		error(503, (e as Error).message);
	}
};

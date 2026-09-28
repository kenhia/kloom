import { error, json } from '@sveltejs/kit';
import { ANSWER_ID } from '$engine/ai/kept';
import { answers, keep } from '$lib/server/ask';
import { dataDir } from '$lib/server/config';
import type { RequestHandler } from './$types';

/**
 * Keep this: `{subject, id}` of an answer the server streamed in the last
 * hour, about that subject. The server writes what it remembers, never text
 * the client sends back.
 */
export const POST: RequestHandler = async ({ request }) => {
	const body = (await request.json().catch(() => null)) as Record<string, unknown> | null;
	const id = body?.id;
	if (typeof id !== 'string' || !ANSWER_ID.test(id)) error(400, 'An answer id is required.');
	const answer = answers.get(id);
	if (!answer || answer.subject !== body?.subject)
		error(404, 'That answer is no longer held; ask again to keep it.');
	let kept;
	try {
		kept = await keep(answer, dataDir());
	} catch (e) {
		// A web page that could not be pinned (Wikipedia unreachable, say).
		error(502, `Could not keep it: ${(e as Error).message}`);
	}
	return json({
		id: kept.id,
		citations: kept.citations.length,
		sources: kept.sources.length,
		web: kept.webCitations?.length ?? 0
	});
};

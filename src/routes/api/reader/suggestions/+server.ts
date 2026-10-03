import { error, json } from '@sveltejs/kit';
import {
	suggestionOf,
	SUGGESTION_TEXT_MAX,
	SUGGESTION_TITLE_MAX,
	SUGGESTIONS_WAITING_MAX as WAITING_MAX
} from '$engine/reader-data';
import { readerStore } from '$lib/server/reader-store';
import { requireReader } from '$lib/server/reader-data';
import type { RequestHandler } from './$types';

/** The reader's own suggested subjects (korg 3459), the newest first, with where each stands. */
export const GET: RequestHandler = async ({ locals }) =>
	json(await readerStore().suggestions(requireReader(locals.reader).login));

/**
 * Suggest a subject: `{title, cover, why}`, a title required. Kept under the
 * reader's login and their name now, for Ken to read; nothing runs from it.
 */
export const POST: RequestHandler = async ({ request, locals }) => {
	const reader = requireReader(locals.reader);
	const s = suggestionOf(await request.json().catch(() => null));
	if (!s)
		error(
			400,
			`A suggestion needs a title (up to ${SUGGESTION_TITLE_MAX} characters), and its other two parts up to ${SUGGESTION_TEXT_MAX} each.`
		);
	const store = readerStore();
	const waiting = (await store.suggestions(reader.login)).filter((x) => x.status === 'new');
	if (waiting.length >= WAITING_MAX)
		error(429, `You have ${WAITING_MAX} suggestions waiting already; Ken will get to them.`);
	return json(await store.suggest(reader.login, reader.name, s), { status: 201 });
};

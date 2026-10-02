import { json } from '@sveltejs/kit';
import { servedStart, servedSubject } from '$lib/server/subject';
import type { RequestHandler } from './$types';

/**
 * A subject's start look (its palettes and a sample of its illustrations),
 * for the start screen when the reader selects it in the subject list. A
 * read, open like the page; an unknown subject is a 404.
 */
export const GET: RequestHandler = async ({ params }) => {
	const { id } = await servedSubject(params.subject);
	return json(await servedStart(id));
};

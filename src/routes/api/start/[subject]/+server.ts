import { json } from '@sveltejs/kit';
import { servedSubject } from '$lib/server/subject';
import { startLook } from '$engine/start';
import type { RequestHandler } from './$types';

/**
 * A subject's start look (its palettes and a sample of its illustrations),
 * for the start screen when the reader selects it in the subject list. A
 * read, open like the page; an unknown subject is a 404.
 */
export const GET: RequestHandler = async ({ params }) =>
	json(startLook(await servedSubject(params.subject)));

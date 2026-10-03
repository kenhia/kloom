import { error, type RequestHandler } from '@sveltejs/kit';
import { ask } from '$lib/server/ask-route';
import { askLedger } from '$lib/server/reader-store';

/**
 * Ask on the reader site (korg 3530): on the Claude API only, for the
 * readers Ken gave it (`admin.mjs reader-ask`), within their cap and the
 * site's. Anyone else gets the same 404 as a route this edition lacks.
 */
export const POST: RequestHandler = (event) => {
	const reader = event.locals.reader?.login;
	if (!reader || !askLedger().access(reader)) error(404, 'Not found');
	return ask(event, reader);
};

import { error, type RequestHandler } from '@sveltejs/kit';
import { POST as keep } from '../full/keep';
import { askLedger } from '$lib/server/reader-store';

/** Keep this, for a reader with ask (korg 3530); anyone else gets a 404, as before. */
export const POST: RequestHandler = (event) => {
	const reader = event.locals.reader?.login;
	if (!reader || !askLedger().access(reader)) error(404, 'Not found');
	return keep(event);
};

import { error, type RequestHandler } from '@sveltejs/kit';
import { DELETE as forget, GET as list } from '../full/kept';
import { askLedger } from '$lib/server/reader-store';

/**
 * A reader's kept answers (korg 3530): the full edition's routes, keyed by
 * the reader as they are there, for a reader with ask. Anyone else gets the
 * same 404 as a route this edition lacks.
 */
const withAsk =
	(handler: RequestHandler): RequestHandler =>
	(event) => {
		const reader = event.locals.reader?.login;
		if (!reader || !askLedger().access(reader)) error(404, 'Not found');
		return handler(event);
	};

export const GET = withAsk(list);
export const DELETE = withAsk(forget);

import { error, type RequestHandler } from '@sveltejs/kit';

/**
 * What a route an edition does not have answers (korg 3500): the
 * same 404 as a path that was never there. The other edition's handler is
 * not in this build at all; nothing here imports it.
 */
export const absent: RequestHandler = () => error(404, 'Not found');

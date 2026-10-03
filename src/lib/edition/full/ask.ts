import { ask } from '$lib/server/ask-route';
import type { RequestHandler } from '@sveltejs/kit';

/** Ask (src/lib/server/ask-route.ts). The hook refused a write without a reader, so there is one. */
export const POST: RequestHandler = (event) => ask(event, event.locals.reader!.login);

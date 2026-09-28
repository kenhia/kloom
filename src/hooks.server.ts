import { json, type Handle, type ServerInit } from '@sveltejs/kit';
import { dev } from '$app/environment';
import { env } from '$env/dynamic/private';
import { syncContentAtStart } from '$lib/server/content';
import { loadGrowQueues } from '$lib/server/grow-service';
import { doorOf, isWrite, localLogin, readerOf } from '$lib/server/reader';

// The content clone picks up merged main first (a deploy is a restart), then
// grow jobs are loaded: they are persisted, and a restart picks every
// subject's queue up where it left off.
export const init: ServerInit = async () => {
	await syncContentAtStart();
	await loadGrowQueues().catch((e) => console.error('grow: could not load the queues', e));
};

/** Reads are open; ask, keep and grow need a reader (src/lib/server/reader.ts). */
export const handle: Handle = async ({ event, resolve }) => {
	const headers = event.request.headers;
	event.locals.reader = readerOf(headers, doorOf(headers, env.KLOOM_DOOR_KEY), dev, localLogin());
	if (!event.locals.reader && isWrite(event.request.method))
		return json(
			{
				message:
					'Asking, keeping and growing need a signed-in tailnet user, and this request carried none.'
			},
			{ status: 401 }
		);
	return resolve(event);
};

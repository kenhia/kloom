import type { ServerInit } from '@sveltejs/kit';
import { growQueue } from '$lib/server/grow-service';

// Grow jobs are persisted; a restart picks the queue up where it left off.
export const init: ServerInit = async () => {
	await growQueue()
		.load()
		.catch((e) => console.error('grow: could not load the queue', e));
};

import type { ServerInit } from '@sveltejs/kit';
import { loadGrowQueues } from '$lib/server/grow-service';

// Grow jobs are persisted; a restart picks every subject's queue up where it left off.
export const init: ServerInit = async () => {
	await loadGrowQueues().catch((e) => console.error('grow: could not load the queues', e));
};

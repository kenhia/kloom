// The full edition's hooks (kai): content clone, grow queues, and the doors.
import { json, type Handle, type ServerInit } from '@sveltejs/kit';
import { dev } from '$app/environment';
import { env } from '$env/dynamic/private';
import { compress } from '$lib/server/compress';
import { dataDir } from '$lib/server/config';
import { syncContentAtStart } from '$lib/server/content';
import { loadGrowQueues } from '$lib/server/grow-service';
import { migrateKeptFiles } from '$lib/server/kept-files';
import { doorOf, isWrite, localLogin, readerOf } from '$lib/server/reader';
import { readerStore } from '$lib/server/reader-store';
import { library } from '$lib/server/subject';

// The content clone picks up merged main first (a deploy is a restart), and
// the library is built from it (docs/design.md §Serving); then kept-answer
// files from before the reader store move into it, then grow jobs are
// loaded: they are persisted, and a restart picks every subject's queue up
// where it left off.
export const init: ServerInit = async () => {
	await syncContentAtStart();
	await library().catch((e) => console.error('content: could not build the library', e));
	await moveKeptFiles();
	await loadGrowQueues().catch((e) => console.error('grow: could not load the queues', e));
};

/** Kept answers never said who kept them: they go to `$KLOOM_KEPT_OWNER`, or the host's own user. */
async function moveKeptFiles() {
	const owner = env.KLOOM_KEPT_OWNER || localLogin();
	try {
		const { moved, refused } = await migrateKeptFiles(readerStore(), dataDir(), owner);
		if (moved.length) console.log(`kept answers: moved ${moved.length} into ${owner}'s store`);
		for (const f of refused)
			console.error(`kept answers: ${f} is not a valid kept answer; left in place`);
	} catch (e) {
		console.error('kept answers: could not move them into the reader store', e);
	}
}

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
	return compress(event.request, await resolve(event));
};

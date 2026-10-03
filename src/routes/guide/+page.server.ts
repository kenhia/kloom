import type { PageServerLoad } from './$types';

/**
 * The User's Guide (korg 3515), in both editions, linked from the start
 * screen beside Welcome and from Welcome itself. It needs only whether the
 * reader signed in, to say how to sign out.
 */
export const load: PageServerLoad = ({ locals }) => ({
	reader: locals.reader
		? { name: locals.reader.name, signedIn: locals.reader.via === 'session' }
		: null
});

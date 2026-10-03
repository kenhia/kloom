import type { PageServerLoad } from './$types';

/**
 * The Welcome and How-To page (korg 3502), in both editions: where a
 * welcome link lands, and linked from the start screen. It needs only who
 * is reading, to greet them and to say how to sign out.
 */
export const load: PageServerLoad = ({ locals }) => ({
	reader: locals.reader
		? { name: locals.reader.name, signedIn: locals.reader.via === 'session' }
		: null
});

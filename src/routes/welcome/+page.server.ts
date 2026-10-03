import { aiOffer } from '$edition/offer';
import type { PageServerLoad } from './$types';

/**
 * The Welcome and How-To page (korg 3502), in both editions: where a
 * welcome link lands, and linked from the start screen. It needs only who
 * is reading, to greet them and to say how to sign out, and whether they
 * may ask.
 */
export const load: PageServerLoad = async ({ locals }) => {
	// Whether this reader has ask (on the reader site, only those Ken gave it), and grow.
	const ai = await aiOffer(locals.reader?.login ?? null).catch(() => null);
	return {
		reader: locals.reader
			? { name: locals.reader.name, signedIn: locals.reader.via === 'session' }
			: null,
		ask: ai !== null,
		grow: !!ai?.growModels
	};
};

import { aiOffer } from '$edition/offer';
import type { PageServerLoad } from './$types';

/**
 * The User's Guide (korg 3515), in both editions, linked from the start
 * screen beside Welcome and from Welcome itself. It needs whether the
 * reader signed in, to say how to sign out, and whether they may ask.
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

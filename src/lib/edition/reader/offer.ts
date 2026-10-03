import type { AiOffered } from '../full/offer';

/** The reader edition has no AI pane, so nothing to offer it (korg 3500). */
export async function aiOffer(): Promise<AiOffered> {
	return null;
}

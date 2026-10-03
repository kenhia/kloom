import { offerFor } from '$lib/server/offer';

/** The full edition offers the AI pane to every reader (src/lib/server/offer.ts). */
export async function aiOffer(reader: string | null) {
	return offerFor(reader);
}

export type { AiOffered } from '$lib/server/offer';

import { askLedger } from '$lib/server/reader-store';
import { offerFor, type AiOffered } from '$lib/server/offer';

/**
 * The reader edition offers the AI pane to the readers Ken allowed
 * (`admin.mjs reader-ask`, korg 3530), and ask only: grow is not in this
 * build. Everyone else sees no AI pane at all.
 */
export async function aiOffer(reader: string | null): Promise<AiOffered> {
	if (!reader || !askLedger().access(reader)) return null;
	return { ...(await offerFor(reader)), growModels: null };
}

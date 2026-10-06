import { error } from '@sveltejs/kit';
import { admins, readerStore } from '$lib/server/reader-store';
import { servedSubject, servedSubjects } from '$lib/server/subject';
import { trafficRow, type TrafficCount } from '$engine/traffic';
import type { PageServerLoad } from './$types';

/**
 * The traffic page (docs/design.md §Traffic, korg 3570): a row per served
 * subject, a cell per frame, lit by the distinct readers who opened it. Only
 * an admin (`admin.mjs admin enable`) sees it; anyone else, signed out
 * included, gets the same 404 as a route that was never there.
 */
export const load: PageServerLoad = async ({ locals }) => {
	if (!admins().is(locals.reader?.login)) error(404, 'Not found');
	const [subjects, traffic] = await Promise.all([servedSubjects(), readerStore().traffic()]);
	const counts: Record<string, Record<string, TrafficCount>> = {};
	for (const t of traffic)
		(counts[t.subject] ??= {})[t.frame] = { readers: t.readers, visits: t.visits };
	const heads = await Promise.all(subjects.map((s) => servedSubject(s.id)));
	return { rows: heads.map((h) => trafficRow(h, counts[h.id] ?? {})) };
};

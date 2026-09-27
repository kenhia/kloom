import { loadSubject } from '$engine/load';
import { subjectDir } from '$lib/server/config';
import type { PageServerLoad } from './$types';

// Read per request, so content written to disk shows without a rebuild.
export const load: PageServerLoad = async () => ({ subject: await loadSubject(subjectDir()) });

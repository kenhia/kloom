import { redirect } from '@sveltejs/kit';
import { defaultSubject, listSubjects } from '$lib/server/config';
import type { RequestHandler } from './$types';

/** `/` opens the landing subject (`$KLOOM_SUBJECT`), or the first served one. */
export const GET: RequestHandler = async () => {
	const subjects = await listSubjects();
	const landing = subjects.find((s) => s.id === defaultSubject()) ?? subjects[0];
	if (!landing) return new Response('No subjects are served.', { status: 503 });
	redirect(307, `/${landing.id}`);
};

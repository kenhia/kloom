import { redirect, type RequestHandler } from '@sveltejs/kit';
import { accounts } from '$lib/server/reader-store';
import { clearSession, SESSION_COOKIE } from '$lib/server/session';

/** Sign out (the start screen's button): this session ends, the others stay. */
export const POST: RequestHandler = ({ cookies }) => {
	const id = cookies.get(SESSION_COOKIE);
	if (id) accounts().signOut(id);
	clearSession(cookies);
	redirect(303, '/signin');
};

import { json, redirect, type Handle, type ServerInit } from '@sveltejs/kit';
import { compress } from '$lib/server/compress';
import { accounts } from '$lib/server/reader-store';
import { clearSession, SESSION_COOKIE } from '$lib/server/session';
import { library } from '$lib/server/subject';

/**
 * The reader edition's hooks (docs/deploying.md §Signing in, korg 3500,
 * 3501). There is no content clone, no grow queue and no kept file to move:
 * the library is built elsewhere and baked in, so start-up only opens it and
 * the reader database, and says so loudly if either will not open.
 */
export const init: ServerInit = async () => {
	try {
		const db = await library();
		console.log(`content: serving build ${db.build}`);
	} catch (e) {
		console.error('content: the library could not be opened', e);
	}
	accounts();
};

/** What may be asked for without a session: signing in, and a welcome link. */
const OPEN = [/^\/signin\/?$/, /^\/welcome\/[A-Za-z0-9_-]+\/?$/];

/** The site is for invited readers: no search engine is welcome. */
const ROBOTS = 'User-agent: *\nDisallow: /\n';
const NOINDEX = 'noindex, nofollow';

/**
 * Every page needs a signed-in reader, reads included (korg 3501). A page
 * asked for without one is sent to sign in, and back after; anything else
 * (the API, the media) is refused.
 */
export const handle: Handle = async ({ event, resolve }) => {
	const path = event.url.pathname;
	if (path === '/robots.txt')
		return new Response(ROBOTS, {
			headers: { 'content-type': 'text/plain; charset=utf-8', 'x-robots-tag': NOINDEX }
		});

	const id = event.cookies.get(SESSION_COOKIE);
	const who = id ? accounts().session(id) : null;
	if (id && !who) clearSession(event.cookies);
	event.locals.reader = who ? { login: who.login, name: who.displayName, via: 'session' } : null;

	if (!who && !OPEN.some((r) => r.test(path))) {
		const page = ['GET', 'HEAD'].includes(event.request.method) && !path.startsWith('/api/');
		if (page) {
			const back = path.replace(/\/__data\.json$/, '') + event.url.search;
			redirect(303, back === '/' ? '/signin' : `/signin?next=${encodeURIComponent(back)}`);
		}
		return json(
			{ message: 'Sign in to read kloom.' },
			{ status: 401, headers: { 'x-robots-tag': NOINDEX } }
		);
	}

	const response = await resolve(event);
	try {
		response.headers.set('x-robots-tag', NOINDEX);
	} catch {
		// A response whose headers cannot change (none of ours); it goes as it is.
	}
	return compress(event.request, response);
};

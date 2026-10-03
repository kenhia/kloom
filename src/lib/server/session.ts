import type { Cookies, RequestEvent } from '@sveltejs/kit';
import { SESSION_DAYS } from './accounts';

/**
 * The reader edition's session cookie (korg 3501): a random id the accounts
 * store as its sha256. HttpOnly, Secure (SvelteKit relaxes it on
 * `localhost`), SameSite=Lax, and a year long; the year slides as the reader
 * comes back (accounts.ts).
 */
export const SESSION_COOKIE = 'kloom_session';

const options = { path: '/', httpOnly: true, secure: true, sameSite: 'lax' } as const;

export function setSession(cookies: Cookies, id: string) {
	cookies.set(SESSION_COOKIE, id, { ...options, maxAge: SESSION_DAYS * 24 * 3600 });
}

export function clearSession(cookies: Cookies) {
	cookies.delete(SESSION_COOKIE, options);
}

/**
 * Who is asking, for sign-in's backoff: Fly's proxy names the client in
 * `Fly-Client-IP` (korg 3458); elsewhere, the peer.
 */
export function clientAddress(event: RequestEvent): string {
	const fly = event.request.headers.get('fly-client-ip')?.trim();
	if (fly) return fly;
	try {
		return event.getClientAddress();
	} catch {
		return 'unknown';
	}
}

/** Where to go after signing in: a path on this site, never another site. */
export function safeNext(next: string | null | undefined): string {
	return typeof next === 'string' && /^\/(?![/\\])/.test(next) ? next : '/';
}

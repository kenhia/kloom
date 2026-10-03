import { beforeEach, describe, expect, it, vi } from 'vitest';
import { openAccounts, type Accounts } from '$lib/server/accounts';
import { useAccounts } from '$lib/server/reader-store';
import { SESSION_COOKIE } from '$lib/server/session';
import { openReaderDb } from '$lib/server/sqlite-reader-store';
import * as ask from './ask';
import * as grow from './grow';
import { handle } from './hooks';
import * as keep from './keep';
import * as kept from './kept';
import { actions as signInActions, load as signInLoad } from './signin';
import { actions as welcomeActions, load as welcomeLoad } from './welcome-link';

// The reader edition (korg 3500, 3501), tested as its modules: `$edition`
// is the full edition's in the test build, so these are imported directly.

const SITE = 'https://kloom.example';
let accounts: Accounts;

beforeEach(() => {
	accounts = openAccounts(openReaderDb(':memory:'), { domain: 'kloom.example' });
	useAccounts(accounts);
});

/** A cookie jar standing in for SvelteKit's. */
function jar(initial: Record<string, string> = {}) {
	const values = { ...initial };
	return {
		values,
		get: (name: string) => values[name],
		set: (name: string, value: string) => void (values[name] = value),
		delete: (name: string) => void delete values[name]
	};
}

function event(
	path: string,
	{
		method = 'GET',
		cookies = jar(),
		form,
		address = '10.0.0.1'
	}: {
		method?: string;
		cookies?: ReturnType<typeof jar>;
		form?: Record<string, string>;
		address?: string;
	} = {}
) {
	const url = new URL(path, SITE);
	const body = form ? new URLSearchParams(form) : undefined;
	return {
		url,
		params: { token: url.pathname.split('/')[2] ?? '' },
		request: new Request(url, { method, body }),
		cookies,
		locals: {} as App.Locals,
		getClientAddress: () => address
	};
}

/** What a thrown redirect or error says, or the value when nothing was thrown. */
async function outcome<T>(run: () => T | Promise<T>) {
	try {
		return await run();
	} catch (e) {
		return e as { status: number; location?: string };
	}
}

const resolved = () => vi.fn(async () => new Response('page'));

async function signedIn() {
	accounts.add('J-n-K', 'Joel and Kathy');
	const { token } = accounts.invite('j-n-k');
	return (await accounts.accept(token, 'correct horse'))!.session;
}

describe('the reader edition hook', () => {
	it('sends a page asked for without a session to sign in, and back after', async () => {
		const resolve = resolved();
		expect(
			await outcome(() => handle({ event: event('/western-civ/fire?x=1'), resolve } as never))
		).toMatchObject({ status: 303, location: '/signin?next=%2Fwestern-civ%2Ffire%3Fx%3D1' });
		expect(await outcome(() => handle({ event: event('/'), resolve } as never))).toMatchObject({
			status: 303,
			location: '/signin'
		});
		expect(
			await outcome(() => handle({ event: event('/welcome'), resolve } as never))
		).toMatchObject({
			status: 303
		});
		expect(resolve).not.toHaveBeenCalled();
	});

	it('refuses everything else without a session, reads included', async () => {
		const resolve = resolved();
		for (const [path, method] of [
			['/api/frame/western-civ/fire', 'GET'],
			['/api/map', 'GET'],
			['/api/reader/notes', 'POST'],
			['/western-civ', 'POST']
		]) {
			const res = (await handle({ event: event(path, { method }), resolve } as never)) as Response;
			expect(res.status).toBe(401);
		}
		expect(resolve).not.toHaveBeenCalled();
	});

	it('lets sign-in and a welcome link through without one', async () => {
		const resolve = resolved();
		for (const path of ['/signin', '/welcome/abcDEF_-123'])
			expect(((await handle({ event: event(path), resolve } as never)) as Response).status).toBe(
				200
			);
		expect(resolve).toHaveBeenCalledTimes(2);
	});

	it('asks no search engine in', async () => {
		const res = (await handle({
			event: event('/robots.txt'),
			resolve: resolved()
		} as never)) as Response;
		expect(await res.text()).toBe('User-agent: *\nDisallow: /\n');
		const page = (await handle({
			event: event('/signin'),
			resolve: resolved()
		} as never)) as Response;
		expect(page.headers.get('x-robots-tag')).toBe('noindex, nofollow');
	});

	it('takes the reader from their session, and ignores door marks and tailnet headers', async () => {
		const session = await signedIn();
		const e = event('/western-civ', { cookies: jar({ [SESSION_COOKIE]: session }) });
		e.request.headers.set('x-kloom-door', 'guess local');
		e.request.headers.set('tailscale-user-login', 'ken@github');
		const res = (await handle({ event: e, resolve: resolved() } as never)) as Response;
		expect(res.status).toBe(200);
		expect(e.locals.reader).toEqual({
			login: 'j-n-k@kloom.example',
			name: 'Joel and Kathy',
			via: 'session'
		});
	});

	it('drops a cookie that names no session', async () => {
		const cookies = jar({ [SESSION_COOKIE]: 'made-up' });
		await outcome(() =>
			handle({ event: event('/western-civ', { cookies }), resolve: resolved() } as never)
		);
		expect(cookies.values[SESSION_COOKIE]).toBeUndefined();
	});
});

describe('what the reader edition does not have', () => {
	it('answers ask, grow, keep and kept answers with a 404', async () => {
		for (const handler of [ask.POST, grow.GET, grow.POST, keep.POST, kept.GET, kept.DELETE])
			expect(await outcome(() => handler({} as never))).toMatchObject({ status: 404 });
	});
});

describe('signing in', () => {
	const signIn = (form: Record<string, string>, cookies = jar(), address = '10.0.0.1') =>
		outcome(() =>
			signInActions.default(event('/signin', { method: 'POST', form, cookies, address }) as never)
		);

	it('opens a session and goes where the reader was headed, never off the site', async () => {
		await signedIn();
		const cookies = jar();
		expect(
			await signIn(
				{ username: 'J-N-K', password: 'correct horse', next: '/western-civ/fire' },
				cookies
			)
		).toMatchObject({ status: 303, location: '/western-civ/fire' });
		expect(accounts.session(cookies.values[SESSION_COOKIE])?.username).toBe('j-n-k');
		for (const next of ['//evil.example', 'https://evil.example', '/\\evil.example'])
			expect(await signIn({ username: 'j-n-k', password: 'correct horse', next })).toMatchObject({
				location: '/'
			});
	});

	it('refuses a wrong password, and backs off after five', async () => {
		await signedIn();
		const statuses = [];
		for (let i = 0; i < 6; i++)
			statuses.push(
				(
					(await signIn({ username: 'j-n-k', password: 'wrong' }, jar(), `10.0.1.${i}`)) as {
						status: number;
					}
				).status
			);
		expect(statuses).toEqual([400, 400, 400, 400, 400, 429]);
		// The right password waits too, until the lockout is over.
		expect(
			await signIn({ username: 'j-n-k', password: 'correct horse' }, jar(), '10.0.2.1')
		).toMatchObject({
			status: 429
		});
	});

	it('sends a reader already signed in on', async () => {
		const e = event('/signin?next=/ai');
		e.locals.reader = { login: 'x@y', name: 'X', via: 'session' };
		expect(await outcome(() => signInLoad(e as never))).toMatchObject({
			status: 303,
			location: '/ai'
		});
	});
});

describe('a welcome link', () => {
	const choose = (token: string, password: string, confirm = password, cookies = jar()) =>
		outcome(() =>
			welcomeActions.default(
				event(`/welcome/${token}`, {
					method: 'POST',
					form: { password, confirm },
					cookies
				}) as never
			)
		);

	it('greets the reader by display name, and lands them on the Welcome page signed in', async () => {
		accounts.add('j-n-k', 'Joel and Kathy');
		const { token } = accounts.invite('j-n-k');
		expect(welcomeLoad(event(`/welcome/${token}`) as never)).toMatchObject({
			invited: { name: 'Joel and Kathy' }
		});
		const cookies = jar();
		expect(await choose(token, 'correct horse', 'correct horse', cookies)).toMatchObject({
			status: 303,
			location: '/welcome'
		});
		expect(accounts.session(cookies.values[SESSION_COOKIE])?.username).toBe('j-n-k');
		expect(welcomeLoad(event(`/welcome/${token}`) as never)).toMatchObject({ invited: null });
		expect(await choose(token, 'correct horse')).toMatchObject({ status: 410 });
	});

	it('says what is wrong with a password, and keeps the link', async () => {
		accounts.add('j-n-k', 'Joel and Kathy');
		const { token } = accounts.invite('j-n-k');
		expect(await choose(token, 'short')).toMatchObject({ status: 400 });
		expect(await choose(token, 'correct horse', 'correct horsf')).toMatchObject({ status: 400 });
		expect(accounts.invited(token)).not.toBeNull();
	});
});

import { beforeEach, describe, expect, it, vi } from 'vitest';
import { openAccounts, type Accounts } from '$lib/server/accounts';
import { useConfigPath } from '$lib/server/app-config';
import { openAskLedger, type AskLedger } from '$lib/server/ask-ledger';
import { useAccounts, useAskLedger } from '$lib/server/reader-store';
import { SESSION_COOKIE } from '$lib/server/session';
import { openReaderDb } from '$lib/server/sqlite-reader-store';
import * as ask from './ask';
import * as grow from './grow';
import { handle } from './hooks';
import * as keep from './keep';
import * as kept from './kept';
import { aiOffer } from './offer';
import { actions as signInActions, load as signInLoad } from './signin';
import { actions as welcomeActions, load as welcomeLoad } from './welcome-link';

// The reader edition (korg 3500, 3501), tested as its modules: `$edition`
// is the full edition's in the test build, so these are imported directly.

const SITE = 'https://kloom.example';
let accounts: Accounts;
let ledger: AskLedger;

beforeEach(() => {
	const db = openReaderDb(':memory:');
	accounts = openAccounts(db, { domain: 'kloom.example' });
	ledger = openAskLedger(db);
	useAccounts(accounts);
	useAskLedger(ledger);
	// The reader edition's own config: the API only, with caps (kloom.reader.json).
	useConfigPath('kloom.reader.json');
	return () => useConfigPath(null);
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
		const sent = async (path: string) => {
			const res = (await handle({ event: event(path), resolve } as never)) as Response;
			return { status: res.status, location: res.headers.get('location') };
		};
		expect(await sent('/western-civ/fire?x=1')).toEqual({
			status: 303,
			location: '/signin?next=%2Fwestern-civ%2Ffire%3Fx%3D1'
		});
		expect(await sent('/')).toEqual({ status: 303, location: '/signin' });
		expect(await sent('/welcome')).toEqual({ status: 303, location: '/signin?next=%2Fwelcome' });
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

	it('keeps browsers to https on every response, and leaves the other hosts of the domain alone', async () => {
		const session = await signedIn();
		const asked = [
			event('/robots.txt'),
			event('/western-civ'),
			event('/api/map'),
			event('/signin'),
			event('/western-civ', { cookies: jar({ [SESSION_COOKIE]: session }) })
		];
		for (const e of asked) {
			const res = (await handle({ event: e, resolve: resolved() } as never)) as Response;
			expect(res.headers.get('strict-transport-security'), e.url.pathname).toBe('max-age=31536000');
		}
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
	it('answers grow with a 404, for everyone', async () => {
		for (const handler of [grow.GET, grow.POST])
			expect(await outcome(() => handler({} as never))).toMatchObject({ status: 404 });
	});
});

describe('ask on the reader site (korg 3530)', () => {
	const jkh = { login: 'jkh@kloom.example', name: 'Joel and Kathy', via: 'session' as const };
	const asking = (reader: typeof jkh | null, body: object) => ({
		request: new Request(`${SITE}/api/ask`, { method: 'POST', body: JSON.stringify(body) }),
		locals: { reader } as App.Locals
	});
	const question = { subject: 'western-civ', frame: 'prometheus', question: 'Why fire?' };

	it('answers ask, keep and kept answers with a 404 for a reader Ken has not given ask', async () => {
		for (const reader of [null, jkh]) {
			const e = asking(reader, question);
			for (const handler of [ask.POST, keep.POST, kept.GET, kept.DELETE])
				expect(await outcome(() => handler({ ...e, url: new URL(SITE) } as never))).toMatchObject({
					status: 404
				});
			expect(await aiOffer(reader?.login ?? null)).toBeNull();
		}
	});

	it('lets a reader with ask through to the question, and offers the API’s models and no grow', async () => {
		ledger.allow(jkh.login, null);
		expect(
			await outcome(() => ask.POST(asking(jkh, { ...question, frame: 'no-such-frame' }) as never))
		).toMatchObject({ status: 400 });
		const offer = await aiOffer(jkh.login);
		expect(offer).toMatchObject({
			askModels: { default: 'api:claude-haiku-4-5' },
			askWeb: 'allow',
			growModels: null,
			budget: { state: 'open' }
		});
		expect(offer!.askModels.choices.map((c) => c.label)).toEqual(['Haiku 4.5', 'Sonnet 5.5']);
	});

	const spend = (reader: string, usd: number) =>
		ledger.log({
			at: new Date().toISOString(),
			reader,
			subject: 'western-civ',
			frame: 'fire',
			provider: 'anthropic-api',
			model: 'claude-haiku-4-5',
			web: true,
			inputTokens: 1,
			outputTokens: 1,
			cacheReadTokens: 0,
			cacheWriteTokens: 0,
			webSearches: 0,
			webFetches: 0,
			ms: 1,
			usd,
			outcome: 'done'
		});

	it('rests ask at the reader’s cap, gracefully: a budget event and no turn', async () => {
		ledger.allow(jkh.login, 0.01);
		spend(jkh.login, 0.011);
		const res = (await ask.POST(asking(jkh, question) as never)) as Response;
		expect(res.status).toBe(200);
		const events = (await res.text())
			.trim()
			.split('\n')
			.map((l) => JSON.parse(l));
		expect(events).toEqual([
			{ type: 'budget', budget: { state: 'resting', until: expect.stringMatching(/-01$/) } }
		]);
		expect((await aiOffer(jkh.login))?.budget?.state).toBe('resting');
	});

	it('rests it for everyone at the site’s cap, and says near past 80% of either', async () => {
		ledger.allow(jkh.login, null);
		spend(jkh.login, 4.1);
		expect((await aiOffer(jkh.login))?.budget?.state).toBe('near');
		spend('someone@kloom.example', 11);
		expect((await aiOffer(jkh.login))?.budget?.state).toBe('resting');
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

import { describe, expect, it } from 'vitest';
import { AccountError, INVITE_DAYS, MIN_PASSWORD, openAccounts, SESSION_DAYS } from './accounts';
import { openReaderDb, openReaderStore } from './sqlite-reader-store';

const DAY = 24 * 3600 * 1000;
const PASSWORD = 'correct horse';

/** Accounts over a throwaway database, on a clock the test moves. */
function setup() {
	let t = Date.parse('2026-10-02T12:00:00Z');
	const clock = {
		now: () => new Date(t),
		pass: (ms: number) => (t += ms)
	};
	const db = openReaderDb(':memory:');
	const accounts = openAccounts(db, { now: clock.now });
	return { db, accounts, clock };
}

/** A reader who has used their welcome link: their first session. */
async function welcomed(accounts: ReturnType<typeof setup>['accounts'], username = 'J-n-K') {
	accounts.add(username, 'Joel and Kathy');
	const { token } = accounts.invite(username);
	const accepted = await accounts.accept(token, PASSWORD);
	return accepted!.session;
}

describe('adding readers', () => {
	it('keeps the username lower-case, the display name as given, and the login namespaced', () => {
		const { accounts } = setup();
		const a = accounts.add('J-n-K', '  Joel and Kathy ');
		expect(a).toMatchObject({
			username: 'j-n-k',
			displayName: 'Joel and Kathy',
			hasPassword: false
		});
		expect(accounts.loginOf('j-n-k')).toBe('j-n-k@kloom.kenhiatt.us');
		expect(accounts.get('J-N-K')?.username).toBe('j-n-k');
	});

	it('refuses a username that is not one, a second reader by the same name, and no display name', () => {
		const { accounts } = setup();
		accounts.add('ada', 'Ada');
		for (const [u, n] of [
			['ada_l', 'Ada'],
			['a da', 'Ada'],
			['../x', 'X'],
			['', 'X'],
			['ADA', 'Another Ada'],
			['bob', '  ']
		])
			expect(() => accounts.add(u, n)).toThrow(AccountError);
	});
});

describe('welcome links', () => {
	it('work once: the second use, or a look after it, finds nothing', async () => {
		const { accounts } = setup();
		accounts.add('j-n-k', 'Joel and Kathy');
		const { token } = accounts.invite('j-n-k');
		expect(accounts.invited(token)).toMatchObject({
			username: 'j-n-k',
			displayName: 'Joel and Kathy'
		});
		const first = await accounts.accept(token, PASSWORD);
		expect(first?.holder.login).toBe('j-n-k@kloom.kenhiatt.us');
		expect(accounts.session(first!.session)?.username).toBe('j-n-k');
		expect(await accounts.accept(token, PASSWORD)).toBeNull();
		expect(accounts.invited(token)).toBeNull();
	});

	it('are not used up by looking at them (a message preview)', async () => {
		const { accounts } = setup();
		accounts.add('j-n-k', 'Joel and Kathy');
		const { token } = accounts.invite('j-n-k');
		accounts.invited(token);
		accounts.invited(token);
		expect(await accounts.accept(token, PASSWORD)).not.toBeNull();
	});

	it('run out after a week', async () => {
		const { accounts, clock } = setup();
		accounts.add('j-n-k', 'Joel and Kathy');
		const { token } = accounts.invite('j-n-k');
		clock.pass(INVITE_DAYS * DAY - 1000);
		expect(accounts.invited(token)).not.toBeNull();
		clock.pass(2000);
		expect(accounts.invited(token)).toBeNull();
		expect(await accounts.accept(token, PASSWORD)).toBeNull();
	});

	it('refuse a short password without using the link', async () => {
		const { accounts } = setup();
		accounts.add('j-n-k', 'Joel and Kathy');
		const { token } = accounts.invite('j-n-k');
		expect(await accounts.accept(token, 'x'.repeat(MIN_PASSWORD - 1))).toBeNull();
		expect(accounts.invited(token)).not.toBeNull();
	});

	it('are refused for a token never minted', async () => {
		const { accounts } = setup();
		accounts.add('j-n-k', 'Joel and Kathy');
		accounts.invite('j-n-k');
		expect(accounts.invited('made-up')).toBeNull();
		expect(await accounts.accept('made-up', PASSWORD)).toBeNull();
	});

	it('are stored only as their hash', () => {
		const { accounts, db } = setup();
		accounts.add('j-n-k', 'Joel and Kathy');
		const { token } = accounts.invite('j-n-k');
		const rows = db.prepare('SELECT token FROM invite').all() as { token: string }[];
		expect(rows).toHaveLength(1);
		expect(rows[0].token).not.toContain(token);
		expect(rows[0].token).toMatch(/^[0-9a-f]{64}$/);
	});
});

describe('a reset (a new link for a reader who has one)', () => {
	it('ends every session, voids the earlier link and the password', async () => {
		const { accounts } = setup();
		const session = await welcomed(accounts);
		const second = (await accounts.signIn('j-n-k', PASSWORD))!.session;
		const stale = accounts.invite('j-n-k');
		const { token } = accounts.invite('j-n-k');
		expect(accounts.session(session)).toBeNull();
		expect(accounts.session(second)).toBeNull();
		expect(accounts.invited(stale.token)).toBeNull();
		expect(await accounts.signIn('j-n-k', PASSWORD)).toBeNull();
		const back = await accounts.accept(token, 'a new password');
		expect(accounts.session(back!.session)?.username).toBe('j-n-k');
		expect(await accounts.signIn('j-n-k', 'a new password')).not.toBeNull();
	});
});

describe('signing in', () => {
	it('takes the username in any case, and only the right password', async () => {
		const { accounts } = setup();
		await welcomed(accounts);
		expect(await accounts.signIn('J-N-K', PASSWORD)).toMatchObject({
			holder: { username: 'j-n-k', displayName: 'Joel and Kathy' }
		});
		expect(await accounts.signIn('j-n-k', 'wrong password')).toBeNull();
		expect(await accounts.signIn('nobody', PASSWORD)).toBeNull();
	});

	it('is refused for a reader who has not chosen a password yet', async () => {
		const { accounts } = setup();
		accounts.add('j-n-k', 'Joel and Kathy');
		accounts.invite('j-n-k');
		expect(await accounts.signIn('j-n-k', '')).toBeNull();
	});

	it('ends one session at sign-out and leaves the others', async () => {
		const { accounts } = setup();
		const phone = await welcomed(accounts);
		const laptop = (await accounts.signIn('j-n-k', PASSWORD))!.session;
		accounts.signOut(phone);
		expect(accounts.session(phone)).toBeNull();
		expect(accounts.session(laptop)).not.toBeNull();
	});
});

describe('sessions', () => {
	it('last a year, and the year slides from the last use', async () => {
		const { accounts, clock } = setup();
		const session = await welcomed(accounts);
		clock.pass((SESSION_DAYS - 10) * DAY);
		expect(accounts.session(session)).not.toBeNull();
		clock.pass(300 * DAY);
		expect(accounts.session(session)).not.toBeNull();
		clock.pass((SESSION_DAYS + 1) * DAY);
		expect(accounts.session(session)).toBeNull();
	});

	it('say when the reader was last seen', async () => {
		const { accounts, clock } = setup();
		const session = await welcomed(accounts);
		clock.pass(3 * DAY);
		accounts.session(session);
		expect(accounts.get('j-n-k')).toMatchObject({
			lastSeen: '2026-10-05T12:00:00.000Z',
			sessions: 1,
			hasPassword: true
		});
	});
});

describe('a disabled reader', () => {
	it('is refused every way in, and their sessions end', async () => {
		const { accounts } = setup();
		const session = await welcomed(accounts);
		expect(accounts.setDisabled('j-n-k', true)).toBe(true);
		expect(accounts.session(session)).toBeNull();
		expect(await accounts.signIn('j-n-k', PASSWORD)).toBeNull();
		const { token } = accounts.invite('j-n-k');
		expect(accounts.invited(token)).toBeNull();
		expect(await accounts.accept(token, PASSWORD)).toBeNull();
		expect(accounts.list()).toMatchObject([{ username: 'j-n-k', disabled: true, sessions: 0 }]);
	});

	it('comes back when enabled, with a new link', async () => {
		const { accounts } = setup();
		await welcomed(accounts);
		accounts.setDisabled('j-n-k', true);
		accounts.setDisabled('j-n-k', false);
		const { token } = accounts.invite('j-n-k');
		expect(await accounts.accept(token, PASSWORD)).not.toBeNull();
	});
});

describe('deleting a reader', () => {
	it('removes the account and, through the store, everything they wrote', async () => {
		const { accounts, db } = setup();
		const store = openReaderStore(db);
		await welcomed(accounts);
		const login = accounts.loginOf('j-n-k');
		await store.visit(login, { subject: 'western-civ', frame: 'fire', label: 'Fire' });
		await store.frameVisit(login, 'western-civ', 'fire');
		await store.bookmark(login, { subject: 'western-civ', frame: 'fire', label: 'Fire' });
		await store.saveNote(login, {
			subject: 'western-civ',
			frame: 'fire',
			label: 'Fire',
			text: 'a note',
			flag: true
		});
		await store.visit('ken@github', { subject: 'western-civ', frame: 'fire', label: 'Fire' });
		expect(await store.deleteReader(login)).toEqual({
			places: 1,
			bookmarks: 1,
			notes: 1,
			kept: 0,
			readings: 1,
			seen: 1,
			visits: 1,
			suggestions: 0
		});
		expect(accounts.remove('j-n-k')).toBe(true);
		expect(accounts.get('j-n-k')).toBeNull();
		expect(await store.lastVisited('ken@github')).not.toBeNull();
		expect(db.prepare('SELECT count(*) AS n FROM session').get()).toEqual({ n: 0 });
	});
});

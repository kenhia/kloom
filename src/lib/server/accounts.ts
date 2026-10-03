import { createHash, randomBytes, scrypt, timingSafeEqual } from 'node:crypto';
import type { DatabaseSync } from 'node:sqlite';

/**
 * The reader edition's accounts (docs/deploying.md §Signing in, korg 3501).
 * Invite only: Ken adds a reader with the admin CLI (`admin.mjs`) and texts
 * them a welcome link, on which they choose a password. There is no admin on
 * the site and no email.
 *
 * An account is a login, not a person: two people may share one (Ken's
 * parents do). It has a username, which is what is typed (case-insensitive,
 * kept lower-case), a display name, which is what the site shows, and a
 * store login, `<username>@<domain>`, which keys the reader's data so that a
 * public reader never meets a tailnet one (`ken@github`) when notes come back
 * to be reviewed.
 *
 * Session ids and invite tokens are stored as their sha256, so a copy of
 * `reader.db` (`just pull-notes`) signs nobody in. Passwords are scrypt with
 * a salt of their own.
 *
 * Like the store's adapter, this imports nothing but `node:` modules, so the
 * admin CLI loads it with plain Node.
 */

/** What a username may be: what is typed, before it is lower-cased. */
export const USERNAME = /^[A-Za-z0-9-]{1,32}$/;
/** The shortest password accepted. */
export const MIN_PASSWORD = 8;
/** The longest: scrypt takes anything, but nobody types more. */
export const MAX_PASSWORD = 256;
/** The longest display name. */
export const MAX_DISPLAY = 60;
/** A welcome link lasts a week. */
export const INVITE_DAYS = 7;
/** A session lasts a year from its last use. */
export const SESSION_DAYS = 365;
/** The store's logins for public readers are `<username>@` this. */
export const DEFAULT_DOMAIN = 'kloom.kenhiatt.us';

/** A session is moved forward at most once a day, so reading is not a write per request. */
const SLIDE_MS = 24 * 3600 * 1000;
const DAY_MS = 24 * 3600 * 1000;

/** scrypt's cost: about 50 ms and 16 MB a hash. */
const SCRYPT = { N: 16384, r: 8, p: 1, keylen: 32 };

export interface Account {
	username: string;
	displayName: string;
	disabled: boolean;
	/** Whether a password is set: false until the welcome link is used, and after a reset. */
	hasPassword: boolean;
	created: string;
	lastSeen: string | null;
	/** Sessions not yet expired. */
	sessions: number;
}

/** Who a session or a link belongs to. */
export interface Holder {
	username: string;
	displayName: string;
	/** The store's key for this reader's data. */
	login: string;
}

/** Why an account change was refused, in words for the CLI. */
export class AccountError extends Error {}

const sha256 = (s: string) => createHash('sha256').update(s).digest('hex');
const token = () => randomBytes(32).toString('base64url');

function hashPassword(password: string, salt = randomBytes(16)): Promise<string> {
	const { N, r, p, keylen } = SCRYPT;
	return new Promise((resolve, reject) =>
		scrypt(password, salt, keylen, { N, r, p, maxmem: 64 * 1024 * 1024 }, (e, key) =>
			e
				? reject(e)
				: resolve(
						`scrypt$${N}$${r}$${p}$${salt.toString('base64url')}$${key.toString('base64url')}`
					)
		)
	);
}

async function passwordMatches(password: string, stored: string): Promise<boolean> {
	const [kind, n, r, p, salt, key] = stored.split('$');
	if (kind !== 'scrypt' || !key) return false;
	const want = Buffer.from(key, 'base64url');
	const got = await new Promise<Buffer>((resolve, reject) =>
		scrypt(
			password,
			Buffer.from(salt, 'base64url'),
			want.length,
			{ N: Number(n), r: Number(r), p: Number(p), maxmem: 64 * 1024 * 1024 },
			(e, k) => (e ? reject(e) : resolve(k))
		)
	);
	return timingSafeEqual(got, want);
}

/** A password's problem in words, or null when it will do. */
export function passwordProblem(password: unknown): string | null {
	if (typeof password !== 'string' || password.length < MIN_PASSWORD)
		return `A password needs at least ${MIN_PASSWORD} characters.`;
	if (password.length > MAX_PASSWORD)
		return `A password can have at most ${MAX_PASSWORD} characters.`;
	return null;
}

/** A username as stored, or null when it is not one. */
export function usernameOf(typed: unknown): string | null {
	return typeof typed === 'string' && USERNAME.test(typed.trim())
		? typed.trim().toLowerCase()
		: null;
}

export interface Accounts {
	/** Add a reader with no password; they get one from their welcome link. */
	add(username: string, displayName: string): Account;
	/**
	 * Mint a welcome link's token for a reader. For a reader who already has
	 * a password this is the reset: earlier links and every session are void,
	 * and the password with them, so the new link is the one way in.
	 */
	invite(username: string): { token: string; expires: string };
	/** Whose link this is, while it may still be used; null otherwise. */
	invited(token: string): Holder | null;
	/** Use a welcome link: set the password and open a session. Null when the link will not do. */
	accept(token: string, password: string): Promise<{ holder: Holder; session: string } | null>;
	/** Sign in with a password: a session, or null. */
	signIn(username: string, password: string): Promise<{ holder: Holder; session: string } | null>;
	/** Whose session this is, moving its expiry forward; null for none, an expired one, or a disabled reader. */
	session(id: string): Holder | null;
	/** End one session. */
	signOut(id: string): void;
	/** Refuse a reader every way in (their sessions end), or let them back. False for no such reader. */
	setDisabled(username: string, disabled: boolean): boolean;
	/** Every reader, by username. */
	list(): Account[];
	/** One reader, or null. */
	get(username: string): Account | null;
	/** Remove a reader's account, sessions and links (their data is the store's: `deleteReader`). */
	remove(username: string): boolean;
	/** The store's key for a username. */
	loginOf(username: string): string;
}

/** The accounts in a reader database already opened and migrated (`openReaderDb`). */
export function openAccounts(
	db: DatabaseSync,
	{ domain = DEFAULT_DOMAIN, now = () => new Date() } = {}
): Accounts {
	const iso = (d: Date) => d.toISOString();
	const after = (days: number) => iso(new Date(now().getTime() + days * DAY_MS));
	const loginOf = (username: string) => `${username}@${domain}`;

	type Row = {
		username: string;
		display_name: string;
		password: string | null;
		disabled: number;
		created: string;
		last_seen: string | null;
		sessions: number;
	};
	const accountCols = `a.username, a.display_name, a.password, a.disabled, a.created, a.last_seen,
		(SELECT count(*) FROM session s WHERE s.username = a.username AND s.expires > ?) AS sessions`;
	const one = db.prepare(`SELECT ${accountCols} FROM account a WHERE a.username = ?`);
	const all = db.prepare(`SELECT ${accountCols} FROM account a ORDER BY a.username`);
	const insert = db.prepare(
		'INSERT INTO account (username, display_name, created) VALUES (?, ?, ?)'
	);
	const setPassword = db.prepare('UPDATE account SET password = ? WHERE username = ?');
	const setDisabledRow = db.prepare('UPDATE account SET disabled = ? WHERE username = ?');
	const seen = db.prepare('UPDATE account SET last_seen = ? WHERE username = ?');
	const dropAccount = db.prepare('DELETE FROM account WHERE username = ?');

	const addSession = db.prepare(
		'INSERT INTO session (id, username, created, seen, expires) VALUES (?, ?, ?, ?, ?)'
	);
	const sessionRow = db.prepare(
		`SELECT s.username, s.seen, s.expires, a.display_name, a.disabled
		 FROM session s JOIN account a ON a.username = s.username WHERE s.id = ?`
	);
	const slide = db.prepare('UPDATE session SET seen = ?, expires = ? WHERE id = ?');
	const dropSession = db.prepare('DELETE FROM session WHERE id = ?');
	const dropSessions = db.prepare('DELETE FROM session WHERE username = ?');
	const dropExpired = db.prepare('DELETE FROM session WHERE expires <= ?');

	const addInvite = db.prepare(
		'INSERT INTO invite (token, username, created, expires) VALUES (?, ?, ?, ?)'
	);
	const inviteRow = db.prepare(
		`SELECT i.username, i.expires, i.used, a.display_name, a.disabled
		 FROM invite i JOIN account a ON a.username = i.username WHERE i.token = ?`
	);
	const useInvite = db.prepare('UPDATE invite SET used = ? WHERE token = ? AND used IS NULL');
	const dropInvites = db.prepare('DELETE FROM invite WHERE username = ?');

	const inTransaction = <T>(work: () => T): T => {
		db.exec('BEGIN IMMEDIATE');
		try {
			const r = work();
			db.exec('COMMIT');
			return r;
		} catch (e) {
			db.exec('ROLLBACK');
			throw e;
		}
	};

	const account = (r: Row): Account => ({
		username: r.username,
		displayName: r.display_name,
		disabled: !!r.disabled,
		hasPassword: !!r.password,
		created: r.created,
		lastSeen: r.last_seen,
		sessions: Number(r.sessions)
	});
	const holder = (username: string, displayName: string): Holder => ({
		username,
		displayName,
		login: loginOf(username)
	});
	const rowOf = (username: string) => one.get(iso(now()), username) as Row | undefined;

	function openSession(username: string): string {
		const id = token();
		const at = iso(now());
		dropExpired.run(at);
		addSession.run(sha256(id), username, at, at, after(SESSION_DAYS));
		seen.run(at, username);
		return id;
	}

	/** Who holds a link that may still be used, or null. */
	function validInvite(t: string) {
		if (typeof t !== 'string' || !t) return null;
		const r = inviteRow.get(sha256(t)) as
			| {
					username: string;
					expires: string;
					used: string | null;
					display_name: string;
					disabled: number;
			  }
			| undefined;
		if (!r || r.used || r.disabled || r.expires <= iso(now())) return null;
		return r;
	}

	// One password checked against when there is no such reader, so a wrong
	// username takes as long as a wrong password.
	let decoy: Promise<string> | null = null;

	return {
		loginOf,

		add(username, displayName) {
			const u = usernameOf(username);
			if (!u)
				throw new AccountError(`"${username}" is not a username: letters, digits and hyphens.`);
			const name = typeof displayName === 'string' ? displayName.trim() : '';
			if (!name || name.length > MAX_DISPLAY)
				throw new AccountError(`A display name is needed, at most ${MAX_DISPLAY} characters.`);
			if (rowOf(u)) throw new AccountError(`There is already a reader "${u}".`);
			insert.run(u, name, iso(now()));
			return account(rowOf(u)!);
		},

		invite(username) {
			const u = usernameOf(username);
			if (!u || !rowOf(u)) throw new AccountError(`There is no reader "${username}".`);
			const t = token();
			const expires = after(INVITE_DAYS);
			inTransaction(() => {
				dropInvites.run(u);
				dropSessions.run(u);
				setPassword.run(null, u);
				addInvite.run(sha256(t), u, iso(now()), expires);
			});
			return { token: t, expires };
		},

		invited(t) {
			const r = validInvite(t);
			return r ? holder(r.username, r.display_name) : null;
		},

		async accept(t, password) {
			if (passwordProblem(password)) return null;
			if (!validInvite(t)) return null;
			const hash = await hashPassword(password);
			// Checked again inside the write: a link is used once, however fast it is opened twice.
			return inTransaction(() => {
				const r = validInvite(t);
				if (!r || useInvite.run(iso(now()), sha256(t)).changes === 0) return null;
				dropInvites.run(r.username);
				setPassword.run(hash, r.username);
				return { holder: holder(r.username, r.display_name), session: openSession(r.username) };
			});
		},

		async signIn(username, password) {
			const u = usernameOf(username);
			const r = u ? rowOf(u) : undefined;
			if (typeof password !== 'string' || password.length > MAX_PASSWORD) return null;
			if (!r?.password) {
				decoy ??= hashPassword('not a password');
				await passwordMatches(password, await decoy);
				return null;
			}
			if (!(await passwordMatches(password, r.password)) || r.disabled) return null;
			return { holder: holder(r.username, r.display_name), session: openSession(r.username) };
		},

		session(id) {
			if (typeof id !== 'string' || !id) return null;
			const key = sha256(id);
			const r = sessionRow.get(key) as
				| {
						username: string;
						seen: string;
						expires: string;
						display_name: string;
						disabled: number;
				  }
				| undefined;
			const at = now();
			if (!r || r.disabled || r.expires <= iso(at)) return null;
			if (at.getTime() - Date.parse(r.seen) >= SLIDE_MS) {
				slide.run(iso(at), after(SESSION_DAYS), key);
				seen.run(iso(at), r.username);
			}
			return holder(r.username, r.display_name);
		},

		signOut(id) {
			if (typeof id === 'string' && id) dropSession.run(sha256(id));
		},

		setDisabled(username, disabled) {
			const u = usernameOf(username);
			if (!u || !rowOf(u)) return false;
			inTransaction(() => {
				setDisabledRow.run(disabled ? 1 : 0, u);
				if (disabled) {
					dropSessions.run(u);
					dropInvites.run(u);
				}
			});
			return true;
		},

		list() {
			return (all.all(iso(now())) as Row[]).map(account);
		},

		get(username) {
			const u = usernameOf(username);
			const r = u ? rowOf(u) : undefined;
			return r ? account(r) : null;
		},

		remove(username) {
			const u = usernameOf(username);
			if (!u || !rowOf(u)) return false;
			inTransaction(() => {
				dropSessions.run(u);
				dropInvites.run(u);
				dropAccount.run(u);
			});
			return true;
		}
	};
}

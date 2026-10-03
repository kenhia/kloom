#!/usr/bin/env node
// The reader edition's admin (docs/deploying.md §Signing in, korg 3501).
// There is no admin on the site: Ken runs this where reader.db is, on Fly
// through `fly ssh console -C`, so Fly's own sign-in is the admin's. Plain
// Node 24+, which strips the types of the modules it opens; it reaches
// reader.db through the accounts module and the reader store, never around
// them.
//
//   node admin.mjs [--data DIR] add USERNAME DISPLAY NAME...
//   node admin.mjs [--data DIR] invite USERNAME [DISPLAY NAME...] [--base URL]
//   node admin.mjs [--data DIR] disable USERNAME
//   node admin.mjs [--data DIR] enable USERNAME
//   node admin.mjs [--data DIR] list [--json]
//   node admin.mjs [--data DIR] delete USERNAME --yes
//
// `invite` prints a welcome link, good once for a week; a display name adds
// the reader first if there is none. For a reader who already has a password
// it is the reset: their earlier links, sessions and password are void, and
// the link is the way back in. DIR is the app's data directory:
// $KLOOM_DATA_DIR, else ./data. URL is the site, $KLOOM_PUBLIC_URL, else
// https://kloom.kenhiatt.us. Logins are `<username>@$KLOOM_LOGIN_DOMAIN`.

import { join, resolve } from 'node:path';
import { AccountError, DEFAULT_DOMAIN, openAccounts } from './src/lib/server/accounts.ts';
import { openReaderDb, openReaderStore } from './src/lib/server/sqlite-reader-store.ts';

const usage = `usage:
  admin.mjs [--data DIR] add USERNAME DISPLAY NAME...
  admin.mjs [--data DIR] invite USERNAME [DISPLAY NAME...] [--base URL]
  admin.mjs [--data DIR] disable USERNAME
  admin.mjs [--data DIR] enable USERNAME
  admin.mjs [--data DIR] list [--json]
  admin.mjs [--data DIR] delete USERNAME --yes`;

const args = process.argv.slice(2);
/** Take `--name value` out of the arguments. */
function option(name) {
	const i = args.indexOf(name);
	if (i < 0) return undefined;
	const [, value] = args.splice(i, 2);
	if (value === undefined) fail(`${name} needs a value`);
	return value;
}
/** Take `--name` out of the arguments: whether it was there. */
function flag(name) {
	const i = args.indexOf(name);
	if (i < 0) return false;
	args.splice(i, 1);
	return true;
}
function fail(message) {
	console.error(message);
	process.exit(1);
}

const dataDir = resolve(option('--data') ?? process.env.KLOOM_DATA_DIR ?? 'data');
const base = (
	option('--base') ??
	process.env.KLOOM_PUBLIC_URL ??
	'https://kloom.kenhiatt.us'
).replace(/\/+$/, '');
const json = flag('--json');
const yes = flag('--yes');
const [command, username, ...rest] = args;
if (!command) fail(usage);

const db = openReaderDb(join(dataDir, 'reader.db'));
const accounts = openAccounts(db, { domain: process.env.KLOOM_LOGIN_DOMAIN || DEFAULT_DOMAIN });
const store = openReaderStore(db);

const needUser = () => username ?? fail(usage);
const when = (iso) => (iso ? iso.replace('T', ' ').replace(/:\d\d\.\d+Z$/, 'Z') : 'never');

try {
	switch (command) {
		case 'add': {
			const a = accounts.add(needUser(), rest.join(' '));
			console.log(
				`added ${a.username} ("${a.displayName}"); \`invite ${a.username}\` makes their link`
			);
			break;
		}
		case 'invite': {
			const u = needUser();
			const existing = accounts.get(u);
			if (!existing) {
				if (!rest.length) fail(`There is no reader "${u}". Give a display name to add them.`);
				accounts.add(u, rest.join(' '));
			} else if (existing.disabled)
				fail(`${existing.username} is disabled; \`enable\` them first.`);
			const reset = existing?.hasPassword || (existing?.sessions ?? 0) > 0;
			const { token, expires } = accounts.invite(u);
			const a = accounts.get(u);
			if (reset) console.error(`${a.username}: password, sessions and earlier links voided`);
			console.error(
				`welcome link for ${a.username} ("${a.displayName}"), good once until ${when(expires)}:`
			);
			console.log(`${base}/welcome/${token}`);
			break;
		}
		case 'disable':
		case 'enable': {
			const u = needUser();
			if (!accounts.setDisabled(u, command === 'disable')) fail(`There is no reader "${u}".`);
			console.log(
				`${u.toLowerCase()} ${command}d${command === 'disable' ? '; their sessions ended' : ''}`
			);
			break;
		}
		case 'list': {
			const all = accounts.list();
			if (json) {
				console.log(
					JSON.stringify(
						all.map((a) => ({ ...a, login: accounts.loginOf(a.username) })),
						null,
						2
					)
				);
				break;
			}
			if (!all.length) console.log('no readers');
			for (const a of all)
				console.log(
					[
						a.username.padEnd(16),
						`"${a.displayName}"`.padEnd(24),
						(a.disabled ? 'disabled' : a.hasPassword ? 'active' : 'invited').padEnd(9),
						`last seen ${when(a.lastSeen)}`.padEnd(30),
						`${a.sessions} session${a.sessions === 1 ? '' : 's'}`
					].join(' ')
				);
			break;
		}
		case 'delete': {
			const u = needUser();
			const a = accounts.get(u);
			if (!a) fail(`There is no reader "${u}".`);
			if (!yes)
				fail(
					`This deletes ${a.username}'s account and everything they wrote. Run again with --yes.`
				);
			const removed = await store.deleteReader(accounts.loginOf(a.username));
			accounts.remove(a.username);
			console.log(
				`deleted ${a.username}: ${removed.notes} notes, ${removed.bookmarks} bookmarks, ` +
					`${removed.places} places, ${removed.kept} kept answers`
			);
			break;
		}
		default:
			fail(usage);
	}
} catch (e) {
	if (e instanceof AccountError) fail(e.message);
	throw e;
} finally {
	db.close();
}

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
//   node admin.mjs [--data DIR] flagged [--reader READER] [--json]
//   node admin.mjs [--data DIR] handle-note READER NOTE_ID RESPONSE... [--seen UPDATED]
//   node admin.mjs [--data DIR] handle-notes JSON
//   node admin.mjs [--data DIR] detached [--library FILE] [--json]
//   node admin.mjs [--data DIR] suggestions [--status STATUS] [--json]
//   node admin.mjs [--data DIR] mark-suggestion READER SUGGESTION_ID STATUS
//   node admin.mjs [--data DIR] --args-b64 BASE64
//
// `invite` prints a welcome link, good once for a week; a display name adds
// the reader first if there is none. For a reader who already has a password
// it is the reset: their earlier links, sessions and password are void, and
// the link is the way back in. DIR is the app's data directory:
// $KLOOM_DATA_DIR, else ./data. URL is the site, $KLOOM_PUBLIC_URL, else
// https://kloom.kenhiatt.us. Logins are `<username>@$KLOOM_LOGIN_DOMAIN`.
//
// The notes return trip (korg 3504; skills/review-notes, which calls these
// over `fly ssh console`): `flagged` lists the notes readers ticked Agent
// review on, each with its reader's display name, and `handle-note` answers
// one in the live store, refusing a note that is gone, no longer flagged, or
// (given `--seen`, the `updated` it was read at) edited since. `handle-notes`
// answers several in one call: a JSON list of {reader, id, response, seen?},
// printing a JSON result per note. A database is never pushed back. READER
// is a login or a username. `detached` lists every note whose frame, or
// annotation whose words, the library (FILE: $KLOOM_CONTENT_DB, else
// DIR/content.db) no longer has; they are reported, never dropped.
// `suggestions` and `mark-suggestion` are the subjects readers suggested
// (korg 3459) and their status: new, planned, written or declined.
//
// `--args-b64` stands for arguments given as a base64 JSON list, so text
// passes `fly ssh console -C`, which splits on spaces and keeps no quotes,
// whole.

import { join, resolve } from 'node:path';
import { DatabaseSync } from 'node:sqlite';
import { detachment } from './engine/anchor.ts';
import { AccountError, DEFAULT_DOMAIN, openAccounts } from './src/lib/server/accounts.ts';
import { openReaderDb, openReaderStore } from './src/lib/server/sqlite-reader-store.ts';

const usage = `usage:
  admin.mjs [--data DIR] add USERNAME DISPLAY NAME...
  admin.mjs [--data DIR] invite USERNAME [DISPLAY NAME...] [--base URL]
  admin.mjs [--data DIR] disable USERNAME
  admin.mjs [--data DIR] enable USERNAME
  admin.mjs [--data DIR] list [--json]
  admin.mjs [--data DIR] delete USERNAME --yes
  admin.mjs [--data DIR] flagged [--reader READER] [--json]
  admin.mjs [--data DIR] handle-note READER NOTE_ID RESPONSE... [--seen UPDATED]
  admin.mjs [--data DIR] handle-notes JSON
  admin.mjs [--data DIR] detached [--library FILE] [--json]
  admin.mjs [--data DIR] suggestions [--status STATUS] [--json]
  admin.mjs [--data DIR] mark-suggestion READER SUGGESTION_ID STATUS
  admin.mjs [--data DIR] --args-b64 BASE64`;

const STATUSES = ['new', 'planned', 'written', 'declined'];

const args = process.argv.slice(2);
// The arguments it stands for go in its place.
const b64 = args.indexOf('--args-b64');
if (b64 >= 0) {
	let decoded;
	try {
		decoded = JSON.parse(Buffer.from(args[b64 + 1] ?? '', 'base64').toString('utf8'));
	} catch {
		decoded = null;
	}
	if (!Array.isArray(decoded) || !decoded.every((a) => typeof a === 'string'))
		fail('--args-b64 needs a base64 JSON list of strings');
	args.splice(b64, 2, ...decoded);
}
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
const readerOpt = option('--reader');
const seen = option('--seen');
const statusOpt = option('--status');
const libraryOpt = option('--library');
const [command, username, ...rest] = args;
if (!command) fail(usage);

const db = openReaderDb(join(dataDir, 'reader.db'));
const accounts = openAccounts(db, { domain: process.env.KLOOM_LOGIN_DOMAIN || DEFAULT_DOMAIN });
const store = openReaderStore(db);

const needUser = () => username ?? fail(usage);
/** A login from a login or a username. */
const loginFor = (r) => (r.includes('@') ? r : accounts.loginOf(r.toLowerCase()));
/** A login's display name, or the login when it is not one of this site's accounts. */
function nameOf(login) {
	const [user] = login.split('@');
	return (accounts.loginOf(user) === login && accounts.get(user)?.displayName) || login;
}
/**
 * Answer one flagged note, or say why not: it is gone, no longer flagged, or
 * edited since `seenAt` (the `updated` it was read at).
 */
async function handleOne(login, id, response, seenAt) {
	if (!response?.trim()) return 'there is no response';
	if (await store.handleNote(login, id, response.trim(), seenAt)) return null;
	const n = (await store.allNotes(login)).find((x) => x.id === id);
	if (!n) return 'there is no such note: the reader deleted it, or it never was';
	if (n.review !== 'flagged') return `it is no longer flagged (${n.review})`;
	return `the reader edited it at ${n.updated}, after it was read (${seenAt}): read it again`;
}
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
					`${removed.places} places, ${removed.kept} kept answers, ${removed.suggestions} suggestions`
			);
			break;
		}
		case 'flagged': {
			const notes = (await store.flaggedNotes(readerOpt && loginFor(readerOpt))).map((n) => ({
				...n,
				readerName: nameOf(n.reader)
			}));
			if (json) console.log(JSON.stringify(notes, null, 2));
			else if (!notes.length) console.log('No flagged notes.');
			else
				for (const n of notes)
					console.log(
						`${n.readerName} (${n.reader})  ${n.id}  ${n.subject}/${n.frame}${n.anchor ? '  (annotation)' : ''}\n` +
							`  ${n.text.replace(/\n/g, '\n  ')}\n`
					);
			break;
		}
		case 'handle-note': {
			const [id, ...words] = rest;
			if (!username || !id) fail(usage);
			const why = await handleOne(loginFor(username), id, words.join(' '), seen);
			if (why) fail(`Not handled: ${id}: ${why}.`);
			console.log(`Handled ${id}.`);
			break;
		}
		case 'handle-notes': {
			let batch;
			try {
				batch = JSON.parse(username ?? '');
			} catch {
				fail('handle-notes needs a JSON list of {reader, id, response, seen?}');
			}
			if (!Array.isArray(batch)) fail('handle-notes needs a JSON list');
			const results = [];
			for (const b of batch) {
				const why =
					typeof b?.reader === 'string' && typeof b?.id === 'string'
						? await handleOne(loginFor(b.reader), b.id, b.response, b.seen)
						: 'it names no reader and note';
				results.push({ reader: b?.reader, id: b?.id, ok: !why, ...(why ? { why } : {}) });
			}
			console.log(JSON.stringify(results, null, 2));
			if (results.some((r) => !r.ok)) process.exitCode = 1;
			break;
		}
		case 'detached': {
			const library = new DatabaseSync(
				resolve(libraryOpt ?? process.env.KLOOM_CONTENT_DB ?? join(dataDir, 'content.db')),
				{ readOnly: true }
			);
			const frame = library.prepare('SELECT body FROM frame WHERE subject = ? AND id = ?');
			const html = (subject, id) => {
				const r = frame.get(subject, id);
				return r ? JSON.parse(r.body).readingHtml : null;
			};
			const notes = await store.everyNote();
			const lost = [];
			for (const n of notes) {
				const why = detachment(n.anchor, html(n.subject, n.frame));
				if (why) lost.push({ ...n, readerName: nameOf(n.reader), detached: why });
			}
			library.close();
			if (json) {
				console.log(JSON.stringify({ notes: notes.length, detached: lost }, null, 2));
				break;
			}
			console.log(`${notes.length} notes, ${lost.length} detached`);
			for (const n of lost)
				console.log(
					`  ${n.readerName} (${n.reader})  ${n.id}  ${n.subject}/${n.frame}: ` +
						(n.detached === 'frame'
							? 'the library has no such frame'
							: `its words are gone: "${n.anchor.exact}"`)
				);
			break;
		}
		case 'suggestions': {
			if (statusOpt && !STATUSES.includes(statusOpt))
				fail(`A status is one of ${STATUSES.join(', ')}.`);
			const all = await store.allSuggestions(statusOpt);
			if (json) console.log(JSON.stringify(all, null, 2));
			else if (!all.length) console.log('No suggestions.');
			else
				for (const s of all)
					console.log(
						[
							`${s.name} (${s.reader})  ${s.id}  ${s.status}  ${when(s.created)}`,
							`  ${s.title}`,
							...(s.cover ? [`  covers: ${s.cover.replace(/\n/g, '\n          ')}`] : []),
							...(s.why ? [`  why:    ${s.why.replace(/\n/g, '\n          ')}`] : []),
							''
						].join('\n')
					);
			break;
		}
		case 'mark-suggestion': {
			const [id, status] = rest;
			if (!username || !id || !STATUSES.includes(status))
				fail(`mark-suggestion needs a reader, a suggestion id and one of ${STATUSES.join(', ')}`);
			if (!(await store.markSuggestion(loginFor(username), id, status)))
				fail(`There is no suggestion ${id} of ${username}'s.`);
			console.log(`${id}: ${status}`);
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

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
//   node admin.mjs [--data DIR] reader-ask enable READER [--cap USD]
//   node admin.mjs [--data DIR] reader-ask disable READER
//   node admin.mjs [--data DIR] reader-ask list [--json]
//   node admin.mjs [--data DIR] ask-usage [--month YYYY-MM] [--config FILE] [--json]
//   node admin.mjs [--data DIR] ask-costs [--since DATE] [--until DATE] [--reader READER] [--model MODEL] [--json]
//   node admin.mjs [--data DIR] admin enable|disable READER
//   node admin.mjs [--data DIR] admin list [--json]
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
// Ask's costs and the reader site's allow-list (korg 3529, 3530; the ask
// ledger, src/lib/server/ask-ledger.ts). `reader-ask enable` gives a reader
// ask, at the configured monthly cap or `--cap` dollars of their own;
// `disable` takes it away (their kept answers stay theirs). `ask-usage` is
// the month's spend, site-wide and per reader, each with its cap (FILE's
// `ask.caps`: $KLOOM_CONFIG, else ./kloom.config.json), as kmon collects it
// with --json. `ask-costs` is the cost per ask over any span: count, total,
// mean, p50, p90, per 1k output tokens and the web's share, per model.
//
// The site's admins (korg 3570; src/lib/server/admins.ts): `admin enable`
// lets a reader see the traffic page (/admin/traffic), `disable` stops it.
// It is the only way an admin is made; the site has no page for it.
//
// `--args-b64` stands for arguments given as a base64 JSON list, so text
// passes `fly ssh console -C`, which splits on spaces and keeps no quotes,
// whole.

import { readFileSync } from 'node:fs';
import { join, resolve } from 'node:path';
import { DatabaseSync } from 'node:sqlite';
import { detachment } from './engine/anchor.ts';
import { AccountError, DEFAULT_DOMAIN, openAccounts } from './src/lib/server/accounts.ts';
import { openAdmins } from './src/lib/server/admins.ts';
import { openReaderDb, openReaderStore } from './src/lib/server/sqlite-reader-store.ts';
import {
	costReport,
	monthOf,
	openAskLedger,
	summarize,
	usageReport
} from './src/lib/server/ask-ledger.ts';

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
  admin.mjs [--data DIR] reader-ask enable READER [--cap USD]
  admin.mjs [--data DIR] reader-ask disable READER
  admin.mjs [--data DIR] reader-ask list [--json]
  admin.mjs [--data DIR] ask-usage [--month YYYY-MM] [--config FILE] [--json]
  admin.mjs [--data DIR] ask-costs [--since DATE] [--until DATE] [--reader READER] [--model MODEL] [--json]
  admin.mjs [--data DIR] admin enable|disable READER
  admin.mjs [--data DIR] admin list [--json]
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
const capOpt = option('--cap');
const monthOpt = option('--month');
const sinceOpt = option('--since');
const untilOpt = option('--until');
const modelOpt = option('--model');
const configOpt = option('--config');
const [command, username, ...rest] = args;
if (!command) fail(usage);

const db = openReaderDb(join(dataDir, 'reader.db'));
const accounts = openAccounts(db, { domain: process.env.KLOOM_LOGIN_DOMAIN || DEFAULT_DOMAIN });
const store = openReaderStore(db);
const ledger = openAskLedger(db);
const admins = openAdmins(db);

/** The ask caps in the app config, or undefined (uncapped). */
function askCaps() {
	const path = resolve(configOpt ?? process.env.KLOOM_CONFIG ?? 'kloom.config.json');
	try {
		return JSON.parse(readFileSync(path, 'utf8')).ask?.caps;
	} catch (e) {
		fail(`Could not read the app config ${path}: ${e.message}`);
	}
}
const usd = (n) => `$${n.toFixed(2)}`;

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
			// Their ask goes; what they spent stays in the cost log, which holds no words of theirs.
			ledger.revoke(accounts.loginOf(a.username));
			admins.disable(accounts.loginOf(a.username));
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
		case 'reader-ask': {
			const [who] = rest;
			if (username === 'list') {
				const all = ledger.allowed().map((a) => ({ ...a, name: nameOf(a.reader) }));
				if (json) console.log(JSON.stringify(all, null, 2));
				else if (!all.length) console.log('No reader has ask.');
				else
					for (const a of all)
						console.log(
							`${a.name} (${a.reader})  cap ${a.capUsd === null ? 'the default' : usd(a.capUsd)}  since ${when(a.enabled)}`
						);
				break;
			}
			if (!['enable', 'disable'].includes(username) || !who) fail(usage);
			if (!who.includes('@') && !accounts.get(who)) fail(`There is no reader "${who}".`);
			const login = loginFor(who);
			if (username === 'disable') {
				if (!ledger.revoke(login)) fail(`${who} does not have ask.`);
				console.log(`${who}: ask taken away; their kept answers stay theirs`);
				break;
			}
			let cap = null;
			if (capOpt !== undefined) {
				cap = Number(capOpt);
				if (!(cap > 0)) fail('--cap is a number of dollars a month, above 0');
			}
			const a = ledger.allow(login, cap);
			console.log(
				`${who}: ask enabled, capped at ${a.capUsd === null ? 'the default' : usd(a.capUsd)} a month`
			);
			break;
		}
		case 'ask-usage': {
			const month = monthOpt ?? monthOf(new Date()).month;
			if (!/^\d{4}-\d\d$/.test(month)) fail('--month is YYYY-MM');
			const report = usageReport(ledger, askCaps(), month);
			if (json) {
				console.log(JSON.stringify(report, null, 2));
				break;
			}
			const cap = (c) => (c === null ? 'uncapped' : `of ${usd(c)}`);
			console.log(
				`${report.month}: ${usd(report.site.spentUsd)} ${cap(report.site.capUsd)} site-wide, ${report.site.asks} asks`
			);
			for (const r of report.readers)
				console.log(
					`  ${nameOf(r.reader)} (${r.reader})  ${usd(r.spentUsd)} ${cap(r.capUsd)}, ${r.asks} asks${r.allowed ? '' : '  (no longer has ask)'}`
				);
			break;
		}
		case 'ask-costs': {
			const rows = ledger.rows({
				since: sinceOpt,
				until: untilOpt,
				reader: readerOpt && loginFor(readerOpt),
				model: modelOpt
			});
			if (json) console.log(JSON.stringify(summarize(rows), null, 2));
			else console.log(costReport(rows));
			break;
		}
		case 'admin': {
			const [who] = rest;
			if (username === 'list') {
				const all = admins.list().map((a) => ({ ...a, name: nameOf(a.reader) }));
				if (json) console.log(JSON.stringify(all, null, 2));
				else if (!all.length) console.log('No admins.');
				else for (const a of all) console.log(`${a.name} (${a.reader})  since ${when(a.enabled)}`);
				break;
			}
			if (!['enable', 'disable'].includes(username) || !who) fail(usage);
			if (!who.includes('@') && !accounts.get(who)) fail(`There is no reader "${who}".`);
			const login = loginFor(who);
			if (username === 'disable') {
				if (!admins.disable(login)) fail(`${who} is not an admin.`);
				console.log(`${who}: no longer an admin`);
				break;
			}
			admins.enable(login);
			console.log(`${who}: admin; /admin/traffic is theirs to see`);
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

#!/usr/bin/env node
// Flagged notes (korg 3409): list the notes readers ticked "Agent review" on,
// annotations (3415) with the words they are on, and mark one handled with
// what was done; and the subjects readers suggested (3459). Run from the repo
// with plain Node 24+. See SKILL.md beside this file.
//
//   node skills/review-notes/review-notes.mjs [TARGET] list [--reader READER] [--json]
//   node skills/review-notes/review-notes.mjs [TARGET] handle READER NOTE_ID RESPONSE... [--seen UPDATED]
//   node skills/review-notes/review-notes.mjs [TARGET] handle --file RESULTS.json
//   node skills/review-notes/review-notes.mjs [TARGET] suggestions [--status STATUS] [--json]
//   node skills/review-notes/review-notes.mjs [TARGET] mark-suggestion READER SUGGESTION_ID STATUS
//
// TARGET is where the notes are: `--data DIR`, an app's data directory
// ($KLOOM_DATA_DIR, else ./data, the dev server's; the service on kai keeps
// its own in ~/.local/share/kloom/data), or `--public`, the public reader
// site's live store on Fly (korg 3504). Either way the work is the admin
// CLI's (admin.mjs), which opens the store through its adapter: here, or on
// the Fly machine through `fly ssh console` (deploy/fly.sh), with the
// arguments base64'd so a response passes whole. Nothing is ever pushed back
// whole: each answer is one guarded write, refused when the note is gone, no
// longer flagged, or edited since it was listed (`--seen`, the `updated` the
// listing gave). `handle --file` sends a JSON list of {reader, id, response,
// seen?} in one call.

import { spawnSync } from 'node:child_process';
import { readFileSync } from 'node:fs';
import { join, resolve } from 'node:path';

const usage = `usage:
  review-notes.mjs [--data DIR | --public] list [--reader READER] [--json]
  review-notes.mjs [--data DIR | --public] handle READER NOTE_ID RESPONSE... [--seen UPDATED]
  review-notes.mjs [--data DIR | --public] handle --file RESULTS.json
  review-notes.mjs [--data DIR | --public] suggestions [--status STATUS] [--json]
  review-notes.mjs [--data DIR | --public] mark-suggestion READER SUGGESTION_ID STATUS`;

const repo = resolve(import.meta.dirname, '..', '..');
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
	console.error(`${message}\n${usage}`);
	process.exit(2);
}

const isPublic = flag('--public');
const dataOpt = option('--data');
if (isPublic && dataOpt) fail('--data or --public, not both');
const data = resolve(dataOpt ?? process.env.KLOOM_DATA_DIR ?? 'data');
const reader = option('--reader');
const seen = option('--seen');
const file = option('--file');
const status = option('--status');
const asJson = flag('--json');
const [command, ...rest] = args;

/** The Fly app, from fly.toml. */
function flyApp() {
	const m = /^app\s*=\s*["']([^"']+)["']/m.exec(readFileSync(join(repo, 'fly.toml'), 'utf8'));
	if (!m) fail('fly.toml names no app');
	return m[1];
}

/** Run the admin CLI on the target: its stdout, or the reason it failed. */
function admin(...argv) {
	const r = isPublic
		? spawnSync(
				join(repo, 'deploy', 'fly.sh'),
				[
					'ssh',
					'console',
					'-a',
					flyApp(),
					'-q',
					'-C',
					'node --disable-warning=ExperimentalWarning /app/admin.mjs --data /data --args-b64 ' +
						Buffer.from(JSON.stringify(argv)).toString('base64')
				],
				{ encoding: 'utf8' }
			)
		: spawnSync(process.execPath, [join(repo, 'admin.mjs'), '--data', data, ...argv], {
				encoding: 'utf8'
			});
	if (r.error) return { ok: false, out: '', err: r.error.message };
	return { ok: r.status === 0, out: r.stdout, err: r.stderr.trim() };
}

/** The admin CLI's JSON answer, or a failure with what it said. */
function adminJson(...argv) {
	const r = admin(...argv);
	try {
		// flyctl may end the output with a carriage return.
		return { ...r, value: JSON.parse(r.out.trim()) };
	} catch {
		console.error(r.err || r.out || 'the admin CLI gave no answer');
		process.exit(1);
	}
}

const where = isPublic ? 'the public site' : data;

if (command === 'list') {
	if (rest.length) fail(`unexpected: ${rest.join(' ')}`);
	const { value: notes } = adminJson('flagged', '--json', ...(reader ? ['--reader', reader] : []));
	if (asJson) console.log(JSON.stringify(notes, null, '\t'));
	else if (!notes.length) console.log(`No flagged notes (${where}).`);
	else
		for (const n of notes)
			console.log(
				[
					`${n.readerName === n.reader ? n.reader : `${n.readerName} (${n.reader})`}  ${n.id}${n.anchor ? '  (annotation)' : ''}`,
					`  frame:   ${n.subject}/${n.frame} — ${n.label}`,
					`  content: subjects/${n.subject}/frames/${n.frame}/`,
					`  written: ${n.created}${n.updated !== n.created ? ` (edited ${n.updated})` : ''}`,
					`  seen:    --seen ${n.updated}`,
					...(n.anchor ? [`  on the words, in reading.md:`, `  > ${n.anchor.exact}`] : []),
					...n.text.split('\n').map((l) => `  | ${l}`),
					''
				].join('\n')
			);
} else if (command === 'handle') {
	let batch;
	if (file) {
		if (rest.length) fail('handle --file takes nothing else');
		try {
			batch = JSON.parse(readFileSync(file, 'utf8'));
		} catch (e) {
			fail(`${file}: ${e.message}`);
		}
		if (!Array.isArray(batch)) fail(`${file}: not a JSON list`);
	} else {
		const [login, id, ...words] = rest;
		const response = words.join(' ').trim();
		if (!login || !id || !response) fail('handle needs a reader, a note id and a response');
		batch = [{ reader: login, id, response, ...(seen ? { seen } : {}) }];
	}
	const { value: results } = adminJson('handle-notes', JSON.stringify(batch));
	let refused = 0;
	for (const r of results) {
		if (r.ok) console.log(`Handled ${r.id}.`);
		else {
			refused += 1;
			console.error(`no flagged note ${r.id} of ${r.reader}'s answered: ${r.why}`);
		}
	}
	if (refused) process.exit(1);
} else if (command === 'suggestions') {
	if (rest.length) fail(`unexpected: ${rest.join(' ')}`);
	if (asJson) {
		const { value } = adminJson('suggestions', '--json', ...(status ? ['--status', status] : []));
		console.log(JSON.stringify(value, null, '\t'));
	} else {
		const r = admin('suggestions', ...(status ? ['--status', status] : []));
		if (!r.ok) fail(r.err);
		process.stdout.write(r.out);
	}
} else if (command === 'mark-suggestion') {
	const r = admin('mark-suggestion', ...rest);
	if (!r.ok) {
		console.error(r.err);
		process.exit(1);
	}
	process.stdout.write(r.out);
} else fail(command ? `unknown command: ${command}` : 'no command');

#!/usr/bin/env node
// Flagged notes (korg 3409): list the notes readers ticked "Agent review" on,
// annotations (3415) with the words they are on, and mark one handled with
// what was done. Run from the repo with plain Node
// 24+, which strips the adapter's types; it opens the reader store through
// that adapter, never around it. See SKILL.md beside this file.
//
//   node skills/review-notes/review-notes.mjs [--data DIR] list [--reader LOGIN] [--json]
//   node skills/review-notes/review-notes.mjs [--data DIR] handle LOGIN NOTE_ID RESPONSE...
//
// DIR is the app's data directory: $KLOOM_DATA_DIR, else ./data (the dev
// server's). The service on kai keeps its own in ~/.local/share/kloom/data.

import { join, resolve } from 'node:path';
import { openReaderStore } from '../../src/lib/server/sqlite-reader-store.ts';

const usage = `usage:
  review-notes.mjs [--data DIR] list [--reader LOGIN] [--json]
  review-notes.mjs [--data DIR] handle LOGIN NOTE_ID RESPONSE...`;

const args = process.argv.slice(2);
/** Take `--name value` out of the arguments. */
function option(name) {
	const i = args.indexOf(name);
	if (i < 0) return undefined;
	const [, value] = args.splice(i, 2);
	if (value === undefined) fail(`${name} needs a value`);
	return value;
}
function fail(message) {
	console.error(`${message}\n${usage}`);
	process.exit(2);
}

const data = resolve(option('--data') ?? process.env.KLOOM_DATA_DIR ?? 'data');
const reader = option('--reader');
const asJson = args.includes('--json') && args.splice(args.indexOf('--json'), 1);
const [command, ...rest] = args;

const store = openReaderStore(join(data, 'reader.db'));
try {
	if (command === 'list') {
		if (rest.length) fail(`unexpected: ${rest.join(' ')}`);
		const notes = await store.flaggedNotes(reader);
		if (asJson) console.log(JSON.stringify(notes, null, '\t'));
		else if (!notes.length) console.log('No flagged notes.');
		else
			for (const n of notes)
				console.log(
					[
						`${n.reader}  ${n.id}${n.anchor ? '  (annotation)' : ''}`,
						`  frame:   ${n.subject}/${n.frame} — ${n.label}`,
						`  content: subjects/${n.subject}/frames/${n.frame}/`,
						`  written: ${n.created}${n.updated !== n.created ? ` (edited ${n.updated})` : ''}`,
						...(n.anchor ? [`  on the words, in reading.md:`, `  > ${n.anchor.exact}`] : []),
						...n.text.split('\n').map((l) => `  | ${l}`),
						''
					].join('\n')
				);
	} else if (command === 'handle') {
		const [login, id, ...words] = rest;
		const response = words.join(' ').trim();
		if (!login || !id || !response) fail('handle needs a reader, a note id and a response');
		if (!(await store.handleNote(login, id, response)))
			fail(`no flagged note ${id} of ${login}'s (already handled, or not flagged)`);
		console.log(`Handled ${id}.`);
	} else fail(command ? `unknown command: ${command}` : 'no command');
} finally {
	store.close();
}

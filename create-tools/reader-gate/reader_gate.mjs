#!/usr/bin/env node
// The reader edition's gate (korg 3500): build it, then fail if the build
// holds anything the public site must not have. "Stripped from the build,
// not just switched off" is checked here, not trusted.
//
//   node create-tools/reader-gate/reader_gate.mjs [--no-build] [--out DIR]
//
// It looks by category, not by route: `claude -p` (the CLI provider), grow,
// and editor-only (building the library, syncing the content clone, moving
// kept-answer files). Ask and keep are in the reader edition since sprint
// 046, on the Claude API only, for readers Ken allows (korg 3530). Each category is a list of markers, a string
// that one module's source holds and its build output keeps. A marker no
// longer in its source fails the gate too, so a rename cannot quietly turn
// a check into one that always passes. A new editor-only control adds its
// marker here.
//
// Beyond the markers, no server file may import `node:child_process`: the
// reader edition runs nothing, `claude` least of all.
//
// After building it runs `svelte-kit sync`, so the generated types are the
// full edition's again (the build left them pointing at the reader's).

import { execFileSync } from 'node:child_process';
import { existsSync, readdirSync, readFileSync } from 'node:fs';
import { join, relative, resolve } from 'node:path';

const root = resolve(import.meta.dirname, '../..');
const args = process.argv.slice(2);
const noBuild = args.includes('--no-build');
const outAt = args.indexOf('--out');
const out = resolve(root, outAt >= 0 ? args[outAt + 1] : 'build-reader');

/**
 * What the reader edition must not hold: category → [source file, marker].
 * Since sprint 046 (korg 3530) it holds ask and keep, on the Claude API, for
 * the readers Ken gives them; `claude -p`, grow and the editor's tools stay
 * out, and so does the full edition's way of choosing a provider.
 */
export const MARKERS = {
	'claude -p': [
		['engine/ai/claude-cli.ts', '--output-format'],
		['engine/ai/claude-cli.ts', '--strict-mcp-config']
	],
	grow: [
		['src/lib/server/grow.ts', 'grow@kloom.local'],
		['src/lib/server/grow-service.ts', 'grow: could not read the kept answer']
	],
	'editor-only': [
		['src/lib/server/subject.ts', 'content: built '],
		['src/lib/server/content.ts', 'the content clone has uncommitted changes'],
		['src/lib/server/kept-files.ts', 'kept-migrated']
	]
};

/** What the reader's browser must never be sent: the AI pane's grow requests. */
export const CLIENT_MARKERS = [['engine/ui/AiPane.svelte', "'/api/grow'", '/api/grow']];

const problems = [];

// The markers must still be in their sources, or they check nothing.
for (const [category, list] of Object.entries(MARKERS))
	for (const [file, marker] of list) {
		const path = join(root, file);
		if (!existsSync(path) || !readFileSync(path, 'utf8').includes(marker))
			problems.push(`${category}: "${marker}" is no longer in ${file}; give the gate a new marker`);
	}
for (const [file, inSource] of CLIENT_MARKERS) {
	const path = join(root, file);
	if (!existsSync(path) || !readFileSync(path, 'utf8').includes(inSource))
		problems.push(`client: ${inSource} is no longer in ${file}; give the gate a new marker`);
}

if (!noBuild) {
	try {
		execFileSync(join(root, 'node_modules/.bin/vite'), ['build', '--logLevel', 'error'], {
			cwd: root,
			env: { ...process.env, KLOOM_EDITION: 'reader' },
			stdio: ['ignore', 'ignore', 'inherit']
		});
	} finally {
		execFileSync(join(root, 'node_modules/.bin/svelte-kit'), ['sync'], {
			cwd: root,
			env: { ...process.env, KLOOM_EDITION: '' },
			stdio: 'inherit'
		});
	}
}
if (!existsSync(join(out, 'handler.js'))) {
	console.error(`reader-gate: no reader build at ${relative(root, out)}`);
	process.exit(1);
}

/** Every built file under `dir` (source maps aside: they quote sources the build left out). */
function files(dir) {
	return readdirSync(dir, { recursive: true, withFileTypes: true })
		.filter((e) => e.isFile() && /\.(js|mjs|html|json)$/.test(e.name))
		.map((e) => join(e.parentPath, e.name));
}

const server = files(out).filter((f) => !f.startsWith(join(out, 'client')));
const client = files(join(out, 'client'));
const texts = new Map([...server, ...client].map((f) => [f, readFileSync(f, 'utf8')]));
const where = (f) => relative(root, f);

for (const [category, list] of Object.entries(MARKERS))
	for (const [file, marker] of list)
		for (const f of [...server, ...client])
			if (texts.get(f).includes(marker))
				problems.push(`${category}: ${where(f)} holds "${marker}" (from ${file})`);

for (const [file, , built] of CLIENT_MARKERS)
	for (const f of client)
		if (texts.get(f).includes(built))
			problems.push(`client: ${where(f)} holds "${built}" (from ${file})`);

for (const f of server)
	if (
		/\bfrom\s*["']node:child_process["']|\bimport\s*["']node:child_process["']|require\(["'](node:)?child_process["']\)/.test(
			texts.get(f)
		)
	)
		problems.push(`spawn: ${where(f)} imports node:child_process`);

if (problems.length) {
	console.error(
		`reader-gate: the reader edition holds what it must not:\n  ${problems.join('\n  ')}`
	);
	process.exit(1);
}
const n = Object.values(MARKERS).flat().length + CLIENT_MARKERS.length;
console.log(
	`reader-gate: ${server.length + client.length} files clean of ${n} markers in ${Object.keys(MARKERS).length + 1} categories, and no child_process`
);

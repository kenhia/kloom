#!/usr/bin/env node
// What the public site's image carries besides the app (docs/deploying.md
// §Public reader site, korg 3503): `build-public/content.db`, the library
// compiled from this checkout's subjects/ and names/ for the subjects
// `publish.json` lists, and `build-public/media/`, exactly the media files
// that library lists, laid out as the subjects are. The Dockerfile copies
// both in as its last layers, so a content-only publish pushes only them.
//
// `just stage-public` runs this; `just publish-public` runs it from a clean
// `main`, so the library records that commit as its source.
//
//   node deploy/stage-public.mjs [--out DIR]

import { execFileSync } from 'node:child_process';
import { copyFileSync, mkdirSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { DatabaseSync } from 'node:sqlite';
import { dirname, join, resolve } from 'node:path';
import { runnerImport } from 'vite';

const repo = resolve(import.meta.dirname, '..');
const i = process.argv.indexOf('--out');
const out = resolve(i > 0 ? process.argv[i + 1] : join(repo, 'build-public'));

const { subjects } = JSON.parse(readFileSync(join(repo, 'publish.json'), 'utf8'));
if (!Array.isArray(subjects) || !subjects.length) {
	console.error('publish.json lists no subjects');
	process.exit(1);
}
const source = execFileSync('git', ['rev-parse', 'HEAD'], { cwd: repo, encoding: 'utf8' }).trim();

const { module: m } = await runnerImport(join(repo, 'engine/content-db.ts'), {
	configFile: false,
	logLevel: 'error'
});

// Built afresh every time: a public library is never an edit of the last one.
rmSync(out, { recursive: true, force: true });
mkdirSync(out, { recursive: true });
const db = join(out, 'content.db');
let report;
try {
	report = await m.compileContent({
		subjectsDir: join(repo, 'subjects'),
		namesDir: join(repo, 'names'),
		out: db,
		compiler: m.engineDigest(join(repo, 'engine')) ?? '',
		strict: true,
		source,
		only: subjects,
		// Capped at this commit: nothing after it is in its history (korg 3525).
		added: await m.gitAddedDates(join(repo, 'subjects'))
	});
} catch (e) {
	console.error(e.message);
	process.exit(1);
}
for (const p of report.nameProblems) console.error('names: ' + p);

const rows = new DatabaseSync(db, { readOnly: true })
	.prepare('SELECT subject, frame, file FROM media ORDER BY subject, frame, file')
	.all();
for (const { subject, frame, file } of rows) {
	const to = join(out, 'media', subject, 'frames', frame, file);
	mkdirSync(dirname(to), { recursive: true });
	copyFileSync(join(repo, 'subjects', subject, 'frames', frame, file), to);
}

// What the publish record names (`just publish-public`, public/publishes.log).
writeFileSync(join(out, 'LIBRARY'), `library ${report.build} source ${source}\n`);
console.log(
	`staged ${out}: ${subjects.length} subjects, build ${report.build}, source ${source.slice(0, 9)}, ${rows.length} media files`
);

import { execFileSync, spawnSync } from 'node:child_process';
import { mkdtempSync, readFileSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { basename, dirname, join, relative, resolve } from 'node:path';
import { DatabaseSync } from 'node:sqlite';
import { afterEach, describe, expect, it } from 'vitest';
import { openAccounts } from './accounts';
import { openReaderDb, openReaderStore } from './sqlite-reader-store';

/**
 * The admin CLI (admin.mjs) and the review-notes script over it, run for real
 * under plain Node: the notes return trip (korg 3504) and suggestions (3459),
 * which the public site is answered through.
 */
const repo = join(import.meta.dirname, '..', '..', '..');
const run = (data: string, ...args: string[]) =>
	spawnSync(process.execPath, [join(repo, 'admin.mjs'), '--data', data, ...args], {
		encoding: 'utf8'
	});
const review = (data: string, ...args: string[]) =>
	execFileSync(
		process.execPath,
		[join(repo, 'skills', 'review-notes', 'review-notes.mjs'), '--data', data, ...args],
		{ encoding: 'utf8' }
	);

let dir: string | undefined;
afterEach(() => {
	if (dir) rmSync(dir, { recursive: true, force: true });
});

const domain = 'kloom.example';
const login = `kt@${domain}`;
const note = (frame: string, text: string, flag = true) => ({
	subject: 'ai',
	frame,
	label: frame,
	text,
	flag
});

/** A data directory with one public reader, "Kloom Test", and a clock a second a write. */
function setup() {
	dir = mkdtempSync(join(tmpdir(), 'kloom-admin-'));
	const db = openReaderDb(join(dir, 'reader.db'));
	let t = Date.parse('2026-10-02T12:00:00Z');
	openAccounts(db, { domain }).add('kt', 'Kloom Test');
	const store = openReaderStore(db, () => new Date((t += 1000)));
	return { dir, store, done: () => db.close() };
}

process.env.KLOOM_LOGIN_DOMAIN = domain;

describe('the notes return trip', () => {
	it('lists flagged notes with their reader named, and answers one by username', async () => {
		const { dir, store, done } = setup();
		const n = (await store.saveNote(login, note('alexnet', 'Which year?')))!;
		await store.saveNote('ken@github', note('turing', 'Mine.'));
		done();
		const listed = JSON.parse(run(dir, 'flagged', '--json').stdout);
		expect(listed.map((x: { readerName: string }) => x.readerName)).toEqual([
			'Kloom Test',
			'ken@github'
		]);
		expect(review(dir, 'list', '--reader', login)).toMatch(/^Kloom Test \(kt@kloom\.example\)/);

		const r = run(dir, 'handle-note', 'kt', n.id, 'It', 'was', '2012.', '--seen', n.updated);
		expect(r.stdout).toContain(`Handled ${n.id}`);
		const after = openReaderStore(join(dir, 'reader.db'));
		expect((await after.notes(login, 'ai'))[0]).toMatchObject({
			review: 'handled',
			response: 'It was 2012.',
			unseen: true
		});
		after.close();
	});

	it('refuses an answer to a note that is gone, no longer flagged, or edited since it was read', async () => {
		const { dir, store, done } = setup();
		const edited = (await store.saveNote(login, note('alexnet', 'first')))!;
		await store.saveNote(login, { ...note('alexnet', 'first, then more'), id: edited.id });
		const unflagged = (await store.saveNote(login, note('turing', 'plain', false)))!;
		done();
		const refused = (...a: string[]) => {
			const r = run(dir, 'handle-note', ...a);
			expect(r.status).toBe(1);
			return r.stderr;
		};
		expect(refused('kt', 'nope', 'x')).toMatch(/no such note/);
		expect(refused('kt', unflagged.id, 'x')).toMatch(/no longer flagged \(none\)/);
		expect(refused('kt', edited.id, 'x', '--seen', edited.updated)).toMatch(/edited it at/);
	});

	it('answers several in one call, saying which were refused', async () => {
		const { dir, store, done } = setup();
		const a = (await store.saveNote(login, note('alexnet', 'one')))!;
		const b = (await store.saveNote(login, note('turing', 'two')))!;
		done();
		const batch = [
			{ reader: login, id: a.id, response: 'Fixed.', seen: a.updated },
			{ reader: 'kt', id: b.id, response: 'Answered.' },
			{ reader: 'kt', id: 'gone', response: 'x' }
		];
		const r = run(dir, 'handle-notes', JSON.stringify(batch));
		expect(r.status).toBe(1);
		expect(JSON.parse(r.stdout).map((x: { ok: boolean }) => x.ok)).toEqual([true, true, false]);
	});

	it("takes its arguments base64'd, so a response passes fly ssh whole", async () => {
		const { dir, store, done } = setup();
		const n = (await store.saveNote(login, note('alexnet', 'quote?')))!;
		done();
		const response = `It's "AlexNet" — and  two spaces; $HOME stays.`;
		const b64 = Buffer.from(JSON.stringify(['handle-note', 'kt', n.id, response])).toString(
			'base64'
		);
		expect(run(dir, '--args-b64', b64).status).toBe(0);
		const after = openReaderStore(join(dir, 'reader.db'));
		expect((await after.notes(login, 'ai'))[0].response).toBe(response);
		after.close();
	});
});

describe('the detached-note check', () => {
	it('names the notes whose frame, or annotation whose words, the library no longer has', async () => {
		const { dir, store, done } = setup();
		const reading = '<p>AlexNet had eight layers and ran on two GPUs.</p>';
		const words = { exact: 'eight layers', prefix: 'AlexNet had ', suffix: ' and ran', start: 12 };
		await store.saveNote(login, { ...note('alexnet', 'fine', false), anchor: words });
		const lost = (await store.saveNote(login, {
			...note('alexnet', 'reworded', false),
			anchor: { ...words, exact: 'two GPUs and a fan', suffix: '.' }
		}))!;
		const gone = (await store.saveNote(login, note('dropped-frame', 'orphan', false)))!;
		await store.saveNote(login, note('alexnet', 'on the frame', false));
		done();
		const library = join(dir, 'content.db');
		const db = new DatabaseSync(library);
		db.exec('CREATE TABLE frame (subject TEXT, id TEXT, body TEXT, reading TEXT)');
		db.prepare('INSERT INTO frame VALUES (?, ?, ?, ?)').run(
			'ai',
			'alexnet',
			JSON.stringify({ readingHtml: reading }),
			''
		);
		db.close();

		const r = JSON.parse(run(dir, 'detached', '--library', library, '--json').stdout);
		expect(r.notes).toBe(4);
		expect(r.detached.map((n: { id: string; detached: string }) => [n.id, n.detached])).toEqual([
			[lost.id, 'words'],
			[gone.id, 'frame']
		]);
		expect(run(dir, 'detached', '--library', library).stdout).toMatch(
			/^4 notes, 2 detached\n {2}Kloom Test/
		);
	});
});

describe('suggestions', () => {
	it('are listed for review, moved on, and go with a deleted reader', async () => {
		const { dir, store, done } = setup();
		const s = await store.suggest(login, 'Kloom Test', {
			title: 'Music',
			cover: 'Plainchant to synths.',
			why: 'I play.'
		});
		done();
		expect(review(dir, 'suggestions')).toContain('Kloom Test (kt@kloom.example)');
		expect(run(dir, 'mark-suggestion', 'kt', s.id, 'maybe').status).toBe(1);
		expect(review(dir, 'mark-suggestion', 'kt', s.id, 'planned')).toContain('planned');
		expect(JSON.parse(review(dir, 'suggestions', '--status', 'planned', '--json'))).toMatchObject([
			{ id: s.id, name: 'Kloom Test', status: 'planned' }
		]);
		expect(run(dir, 'delete', 'kt', '--yes').stdout).toContain('1 suggestions');
		expect(JSON.parse(run(dir, 'suggestions', '--json').stdout)).toEqual([]);
	});
});

describe('admins (korg 3570)', () => {
	it('are given, listed and taken away by login or username, and go with a deleted reader', async () => {
		const { dir, done } = setup();
		done();
		expect(run(dir, 'admin', 'enable', 'nobody').stderr).toMatch(/no reader "nobody"/);
		expect(run(dir, 'admin', 'enable', 'kt').stdout).toContain('kt: admin');
		expect(run(dir, 'admin', 'enable', 'ken@github').status).toBe(0);
		expect(
			JSON.parse(run(dir, 'admin', 'list', '--json').stdout).map(
				(a: { reader: string }) => a.reader
			)
		).toEqual(['ken@github', login]);
		expect(run(dir, 'admin', 'disable', 'ken@github').stdout).toContain('no longer an admin');
		expect(run(dir, 'admin', 'disable', 'ken@github').status).toBe(1);
		expect(run(dir, 'delete', 'kt', '--yes').status).toBe(0);
		expect(run(dir, 'admin', 'list').stdout).toBe('No admins.\n');
	});
});

describe('the public image', () => {
	/** Every repo file admin.mjs loads, following relative imports. */
	function loaded(file: string, seen = new Set<string>()): Set<string> {
		if (seen.has(file)) return seen;
		seen.add(file);
		const text = readFileSync(join(repo, file), 'utf8');
		for (const [, spec] of text.matchAll(
			/^\s*(?:import|export)\b(?!\s+type\b)[^'"]*?from\s+'(\.{1,2}\/[^']+)'/gm
		))
			loaded(relative(repo, resolve(dirname(join(repo, file)), spec)), seen);
		return seen;
	}

	it('copies every file admin.mjs loads, so it runs on Fly (sprint 054 shipped without one)', () => {
		const copied = new Set<string>();
		for (const [, line] of readFileSync(join(repo, 'Dockerfile'), 'utf8').matchAll(
			/^COPY (?!--from)(.+)$/gm
		)) {
			const parts = line.trim().split(/\s+/);
			const dest = parts.pop()!;
			for (const p of parts)
				copied.add(dest.endsWith('/') && dest !== './' ? join(dest, basename(p)) : p);
		}
		const missing = [...loaded('admin.mjs')].filter((f) => !copied.has(f));
		expect(missing).toEqual([]);
	});
});

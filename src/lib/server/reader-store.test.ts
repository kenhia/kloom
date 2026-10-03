import { mkdtempSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { DatabaseSync } from 'node:sqlite';
import { afterEach, describe, expect, it } from 'vitest';
import { mkdir, readdir, writeFile } from 'node:fs/promises';
import { keptAnswer } from '$engine/ai/kept';
import { context } from '$engine/ai/fixture';
import { parseExport } from '$engine/reader-data';
import { migrateKeptFiles } from './kept-files';
import { openReaderStore, SCHEMA_VERSION } from './reader-store';

/** A clock the test moves: each call is a second after the last. */
function clock(start = Date.parse('2026-09-28T12:00:00Z')) {
	let t = start;
	return () => new Date((t += 1000));
}

const ken = 'ken@github';
const ada = 'ada@github';
const at = (subject: string, frame: string) => ({ subject, frame, label: `${frame} label` });

describe('last visited', () => {
	it('keeps one place per subject, and the newest overall', async () => {
		const store = openReaderStore(':memory:', clock());
		expect(await store.lastVisited(ken)).toBeNull();
		await store.visit(ken, at('western-civ', 'fire'));
		await store.visit(ken, at('ai', 'turing'));
		await store.visit(ken, at('western-civ', 'printing-press'));
		expect(await store.lastVisited(ken, 'western-civ')).toMatchObject({ frame: 'printing-press' });
		expect(await store.lastVisited(ken, 'ai')).toMatchObject({ frame: 'turing' });
		expect(await store.lastVisited(ken)).toMatchObject({
			subject: 'western-civ',
			frame: 'printing-press',
			label: 'printing-press label',
			at: '2026-09-28T12:00:03.000Z'
		});
		expect(await store.lastVisited(ken, 'nope')).toBeNull();
	});

	it('keeps each reader’s own', async () => {
		const store = openReaderStore(':memory:', clock());
		await store.visit(ken, at('ai', 'turing'));
		await store.visit(ada, at('ai', 'dartmouth'));
		expect(await store.lastVisited(ken, 'ai')).toMatchObject({ frame: 'turing' });
		expect(await store.lastVisited(ada)).toMatchObject({ frame: 'dartmouth' });
	});
});

describe('what is new to a reader (korg 3525)', () => {
	/** A clock the test sets. */
	const settable = (start: string) => {
		let t = Date.parse(start);
		const now = () => new Date(t);
		now.set = (iso: string) => (t = Date.parse(iso));
		return now;
	};

	it('starts a subject on the first visit to it, and opens each frame visited', async () => {
		const now = settable('2026-10-01T09:00:00Z');
		const store = openReaderStore(':memory:', now);
		expect(await store.readings(ken)).toEqual({});
		await store.visit(ken, at('nursing', 'nightingale'));
		now.set('2026-10-02T09:00:00Z');
		await store.visit(ken, at('nursing', 'navy-pow'));
		await store.visit(ada, at('blood', 'harvey'));
		expect(await store.readings(ken)).toEqual({
			nursing: { first: '2026-10-01T09:00:00.000Z', caughtUp: null }
		});
		expect(await store.seenFrames(ken)).toEqual({ nursing: ['navy-pow', 'nightingale'] });
		expect(await store.seenFrames(ada)).toEqual({ blood: ['harvey'] });
	});

	it('marks frames seen, and catching up sets the watermark to now', async () => {
		const now = settable('2026-10-01T09:00:00Z');
		const store = openReaderStore(':memory:', now);
		await store.markSeen(ken, 'blood', ['harvey', 'landsteiner']);
		await store.markSeen(ken, 'blood', ['harvey']);
		expect(await store.seenFrames(ken)).toEqual({ blood: ['harvey', 'landsteiner'] });
		// Catching up on a subject never visited starts it too.
		now.set('2026-10-03T09:00:00Z');
		expect(await store.catchUp(ken, 'blood')).toEqual({
			first: '2026-10-03T09:00:00.000Z',
			caughtUp: '2026-10-03T09:00:00.000Z'
		});
		now.set('2026-10-04T09:00:00Z');
		await store.visit(ken, at('blood', 'harvey'));
		expect((await store.readings(ken)).blood).toEqual({
			first: '2026-10-03T09:00:00.000Z',
			caughtUp: '2026-10-03T09:00:00.000Z'
		});
	});

	it('says when the last visit ended: the previous run of moves, after a long pause', async () => {
		const now = settable('2026-10-01T09:00:00Z');
		const store = openReaderStore(':memory:', now);
		expect(await store.lastVisit(ken)).toBeNull();
		await store.visit(ken, at('ai', 'turing'));
		now.set('2026-10-01T09:30:00Z');
		await store.visit(ken, at('ai', 'dartmouth'));
		// Still the first visit: there was none before it.
		expect(await store.lastVisit(ken)).toBeNull();
		// Back the next day: the visit that ended at 09:30 is the last one, before and after a move.
		now.set('2026-10-02T08:00:00Z');
		expect(await store.lastVisit(ken)).toBe('2026-10-01T09:30:00.000Z');
		await store.visit(ken, at('ai', 'turing'));
		now.set('2026-10-02T08:20:00Z');
		await store.visit(ken, at('ai', 'transformer'));
		expect(await store.lastVisit(ken)).toBe('2026-10-01T09:30:00.000Z');
	});

	it('carries readings and seen frames through an export: earlier first visits, later watermarks', async () => {
		const from = openReaderStore(':memory:', settable('2026-10-01T09:00:00Z'));
		await from.visit(ken, at('ai', 'turing'));
		await from.catchUp(ken, 'ai');
		const parsed = parseExport(JSON.parse(JSON.stringify(await from.exportData(ken))));
		if ('error' in parsed) throw new Error(parsed.error);
		expect(parsed.readings).toEqual([
			{ subject: 'ai', first: '2026-10-01T09:00:00.000Z', caughtUp: '2026-10-01T09:00:00.000Z' }
		]);
		const now = settable('2026-10-05T09:00:00Z');
		const to = openReaderStore(':memory:', now);
		await to.visit(ada, at('ai', 'dartmouth'));
		await to.catchUp(ada, 'ai');
		await to.importData(ada, parsed);
		expect((await to.readings(ada)).ai).toEqual({
			first: '2026-10-01T09:00:00.000Z',
			caughtUp: '2026-10-05T09:00:00.000Z'
		});
		expect(await to.seenFrames(ada)).toEqual({ ai: ['dartmouth', 'turing'] });
		// One bad record refuses the file.
		expect(parseExport({ ...parsed, seen: [{ subject: 'ai', frame: '../x', at: 'x' }] })).toEqual({
			error: 'seen frame 0 is not a valid record'
		});
	});

	it('takes readers from before it to have started a subject with their first record in it', async () => {
		dir = mkdtempSync(join(tmpdir(), 'kloom-reader-'));
		const path = join(dir, 'reader.db');
		const before = openReaderStore(path, settable('2026-09-20T09:00:00Z'));
		await before.saveNote(ken, note('turing', 'early'));
		before.close();
		const later = openReaderStore(path, settable('2026-10-01T09:00:00Z'));
		await later.visit(ken, at('ai', 'dartmouth'));
		await later.bookmark(ken, at('western-civ', 'fire'));
		later.close();
		// Back to sprint 041's schema, with the records kept.
		const raw = new DatabaseSync(path);
		raw.exec(
			`DROP TABLE reading; DROP TABLE seen; DROP TABLE activity; DROP TABLE ask_cost; DROP TABLE ask_access; PRAGMA user_version = 6;`
		);
		raw.close();
		const store = openReaderStore(path, settable('2026-10-03T09:00:00Z'));
		expect(await store.readings(ken)).toEqual({
			ai: { first: '2026-09-20T09:00:00.000Z', caughtUp: null },
			'western-civ': { first: '2026-10-01T09:00:00.000Z', caughtUp: null }
		});
		expect(await store.seenFrames(ken)).toEqual({
			ai: ['dartmouth', 'turing'],
			'western-civ': ['fire']
		});
		expect(await store.lastVisit(ken)).toBe('2026-10-01T09:00:00.000Z');
		store.close();
	});
	let dir: string | undefined;
	afterEach(() => {
		if (dir) rmSync(dir, { recursive: true, force: true });
		dir = undefined;
	});
});

describe('bookmarks', () => {
	it('lists a reader’s marks across subjects, newest first, and removes one', async () => {
		const store = openReaderStore(':memory:', clock());
		await store.bookmark(ken, at('western-civ', 'fire'));
		await store.bookmark(ken, at('ai', 'turing'));
		await store.bookmark(ada, at('ai', 'dartmouth'));
		expect((await store.bookmarks(ken)).map((b) => b.frame)).toEqual(['turing', 'fire']);
		await store.unbookmark(ken, 'western-civ', 'fire');
		expect((await store.bookmarks(ken)).map((b) => b.frame)).toEqual(['turing']);
		expect((await store.bookmarks(ada)).map((b) => b.frame)).toEqual(['dartmouth']);
	});

	it('marking a frame again keeps one mark and its first date, with the new label', async () => {
		const store = openReaderStore(':memory:', clock());
		await store.bookmark(ken, at('ai', 'turing'));
		await store.bookmark(ken, { subject: 'ai', frame: 'turing', label: 'Renamed' });
		const marks = await store.bookmarks(ken);
		expect(marks).toHaveLength(1);
		expect(marks[0]).toMatchObject({ label: 'Renamed', at: '2026-09-28T12:00:01.000Z' });
	});
});

const note = (frame: string, text: string, flag = false) => ({
	subject: 'ai',
	frame,
	label: `${frame} label`,
	text,
	flag
});

describe('notes', () => {
	it('are kept per reader and subject, oldest first, and edited in place', async () => {
		const store = openReaderStore(':memory:', clock());
		const a = (await store.saveNote(ken, note('turing', 'first')))!;
		await store.saveNote(ken, note('alexnet', 'second'));
		await store.saveNote(ken, { ...note('fire', 'elsewhere'), subject: 'western-civ' });
		await store.saveNote(ada, note('turing', 'ada’s'));
		expect((await store.notes(ken, 'ai')).map((n) => n.text)).toEqual(['first', 'second']);

		const edited = await store.saveNote(ken, { ...note('alexnet', 'first, edited'), id: a.id });
		// An edit keeps its frame and creation, and moves its update.
		expect(edited).toMatchObject({ frame: 'turing', text: 'first, edited', created: a.created });
		expect(edited!.updated > a.updated).toBe(true);
		expect(await store.saveNote(ada, { ...note('turing', 'not hers'), id: a.id })).toBeNull();
		expect(await store.deleteNote(ada, a.id)).toBe(false);
		expect(await store.deleteNote(ken, a.id)).toBe(true);
		expect((await store.notes(ken, 'ai')).map((n) => n.text)).toEqual(['second']);
	});

	it('are flagged for review, handled by the agent, and flagged again on request', async () => {
		const store = openReaderStore(':memory:', clock());
		const n = (await store.saveNote(ken, note('turing', 'confusing wording', true)))!;
		await store.saveNote(ada, note('turing', 'hers', true));
		await store.saveNote(ken, note('alexnet', 'fine'));
		expect(n.review).toBe('flagged');
		expect((await store.flaggedNotes()).map((f) => [f.reader, f.text])).toEqual([
			[ken, 'confusing wording'],
			[ada, 'hers']
		]);
		expect((await store.flaggedNotes(ken)).map((f) => f.text)).toEqual(['confusing wording']);

		expect(await store.handleNote(ada, n.id, 'not hers')).toBe(false);
		expect(await store.handleNote(ken, n.id, 'Reworded the second paragraph.')).toBe(true);
		expect(await store.handleNote(ken, n.id, 'twice')).toBe(false);
		expect(await store.flaggedNotes(ken)).toEqual([]);

		// Unticked, a handled note stays handled, with what was done.
		const kept = await store.saveNote(ken, { ...note('turing', 'still odd'), id: n.id });
		expect(kept).toMatchObject({ review: 'handled', response: 'Reworded the second paragraph.' });
		// Ticked again, it asks afresh.
		const again = await store.saveNote(ken, { ...note('turing', 'still odd', true), id: n.id });
		expect(again).toMatchObject({ review: 'flagged', response: null });
		// Unticking a flagged note unflags it.
		const off = await store.saveNote(ken, { ...note('turing', 'never mind'), id: n.id });
		expect(off).toMatchObject({ review: 'none' });
	});
});

describe('answering a note read from a copy (the public site, korg 3504)', () => {
	it('refuses an answer to a note edited since it was read, and takes one that was not', async () => {
		const store = openReaderStore(':memory:', clock());
		const n = (await store.saveNote(ken, note('turing', 'is this right?', true)))!;
		const read = n.updated;
		await store.saveNote(ken, {
			...note('turing', 'is this right? I mean the year', true),
			id: n.id
		});
		expect(await store.handleNote(ken, n.id, 'Yes.', read)).toBe(false);
		const now = (await store.flaggedNotes(ken))[0];
		expect(await store.handleNote(ken, n.id, 'Yes, 1936.', now.updated)).toBe(true);
		expect((await store.notes(ken, 'ai'))[0]).toMatchObject({ review: 'handled', unseen: true });
	});

	it("lists every reader's every note, flagged or not, for the detached check", async () => {
		const store = openReaderStore(':memory:', clock());
		await store.saveNote(ken, note('turing', 'one'));
		await store.saveNote(ada, note('alexnet', 'two', true));
		expect((await store.everyNote()).map((n) => [n.reader, n.frame])).toEqual([
			[ken, 'turing'],
			[ada, 'alexnet']
		]);
	});
});

describe('suggestions', () => {
	const idea = { title: 'Music', cover: 'From plainchant to the synthesiser.', why: '' };

	it('are kept per reader, newest first, and listed for review oldest first', async () => {
		const store = openReaderStore(':memory:', clock());
		const first = await store.suggest(ken, 'Ken', idea);
		expect(first).toMatchObject({ ...idea, status: 'new' });
		await store.suggest(ada, 'Ada', { ...idea, title: 'Astronomy' });
		await store.suggest(ken, 'Ken', { ...idea, title: 'Geology' });
		expect((await store.suggestions(ken)).map((s) => s.title)).toEqual(['Geology', 'Music']);
		expect((await store.allSuggestions()).map((s) => [s.name, s.title])).toEqual([
			['Ken', 'Music'],
			['Ada', 'Astronomy'],
			['Ken', 'Geology']
		]);
	});

	it('move on from the review side, and a status narrows the list', async () => {
		const store = openReaderStore(':memory:', clock());
		const s = await store.suggest(ken, 'Ken', idea);
		expect(await store.markSuggestion(ada, s.id, 'planned')).toBe(false);
		expect(await store.markSuggestion(ken, s.id, 'planned')).toBe(true);
		const [now] = await store.suggestions(ken);
		expect(now.status).toBe('planned');
		expect(now.updated > s.updated).toBe(true);
		expect(await store.allSuggestions('new')).toEqual([]);
		expect((await store.allSuggestions('planned')).map((x) => x.id)).toEqual([s.id]);
	});

	it('go with a deleted reader, and are not in the export', async () => {
		const store = openReaderStore(':memory:', clock());
		await store.suggest(ken, 'Ken', idea);
		expect(Object.keys(await store.exportData(ken))).not.toContain('suggestions');
		expect((await store.deleteReader(ken)).suggestions).toBe(1);
		expect(await store.suggestions(ken)).toEqual([]);
	});
});

describe('every note, for My notes', () => {
	it('lists a reader’s notes across subjects, newest first', async () => {
		const store = openReaderStore(':memory:', clock());
		await store.saveNote(ken, note('turing', 'first'));
		await store.saveNote(ken, { ...note('fire', 'elsewhere'), subject: 'western-civ' });
		const c = (await store.saveNote(ken, note('alexnet', 'third')))!;
		await store.saveNote(ada, note('turing', 'ada’s'));
		expect((await store.allNotes(ken)).map((n) => n.text)).toEqual(['third', 'elsewhere', 'first']);
		// An edit brings a note forward: newest is the last written.
		await store.saveNote(ken, {
			...note('turing', 'first, edited'),
			id: (await store.allNotes(ken))[2].id
		});
		expect((await store.allNotes(ken)).map((n) => n.text)).toEqual([
			'first, edited',
			'third',
			'elsewhere'
		]);
		expect(c.unseen).toBe(false);
	});

	it('counts an agent’s answer as unseen until the reader has seen it', async () => {
		const store = openReaderStore(':memory:', clock());
		const a = (await store.saveNote(ken, note('turing', 'one', true)))!;
		const b = (await store.saveNote(ken, note('alexnet', 'two', true)))!;
		await store.saveNote(ada, note('turing', 'hers', true));
		expect(await store.unseenAnswers(ken)).toBe(0);
		await store.handleNote(ken, a.id, 'Fixed.');
		await store.handleNote(ken, b.id, 'Answered.');
		expect(await store.unseenAnswers(ken)).toBe(2);
		expect(await store.unseenAnswers(ada)).toBe(0);
		expect((await store.allNotes(ken)).every((n) => n.unseen)).toBe(true);

		// Seeing one of them, or someone else's id, changes only what is theirs.
		expect(await store.seeNotes(ada, [a.id])).toBe(0);
		expect(await store.seeNotes(ken, [a.id])).toBe(1);
		expect(await store.unseenAnswers(ken)).toBe(1);
		// Flagged afresh, an answer is no longer waiting to be seen.
		await store.saveNote(ken, { ...note('alexnet', 'two again', true), id: b.id });
		expect(await store.unseenAnswers(ken)).toBe(0);
		await store.handleNote(ken, b.id, 'Answered again.');
		expect(await store.unseenAnswers(ken)).toBe(1);
		expect(await store.seeNotes(ken, [a.id, b.id])).toBe(1);
		expect(await store.unseenAnswers(ken)).toBe(0);
	});

	it('flags and unflags a note without its text, as the editor’s box does', async () => {
		const store = openReaderStore(':memory:', clock());
		const n = (await store.saveNote(ken, note('turing', 'look')))!;
		expect(await store.flagNote(ada, n.id, true)).toBeNull();
		expect(await store.flagNote(ken, n.id, true)).toMatchObject({
			review: 'flagged',
			text: 'look'
		});
		expect(await store.flagNote(ken, n.id, false)).toMatchObject({ review: 'none' });
		await store.flagNote(ken, n.id, true);
		await store.handleNote(ken, n.id, 'Done.');
		// Unflagged, a handled note stays handled; flagged, it asks afresh.
		expect(await store.flagNote(ken, n.id, false)).toMatchObject({
			review: 'handled',
			response: 'Done.'
		});
		expect(await store.flagNote(ken, n.id, true)).toMatchObject({
			review: 'flagged',
			response: null,
			unseen: false
		});
	});

	it('deletes several of a reader’s notes at once, and only theirs', async () => {
		const store = openReaderStore(':memory:', clock());
		const a = (await store.saveNote(ken, note('turing', 'one')))!;
		const b = (await store.saveNote(ken, note('alexnet', 'two')))!;
		const c = (await store.saveNote(ada, note('turing', 'hers')))!;
		await store.saveNote(ken, note('turing', 'kept'));
		expect(await store.deleteNotes(ken, [a.id, b.id, c.id, 'nope'])).toBe(2);
		expect((await store.allNotes(ken)).map((n) => n.text)).toEqual(['kept']);
		expect(await store.allNotes(ada)).toHaveLength(1);
		expect(await store.deleteNotes(ken, [])).toBe(0);
	});
});

const words = { exact: 'the second paragraph', prefix: 'Read ', suffix: ' again.', start: 5 };

describe('annotations', () => {
	it('keep the words they are on, through edits, flags and the review list', async () => {
		const store = openReaderStore(':memory:', clock());
		const a = (await store.saveNote(ken, { ...note('turing', 'which?', true), anchor: words }))!;
		expect(a).toMatchObject({ anchor: words, review: 'flagged' });
		expect((await store.saveNote(ken, note('turing', 'a plain note')))!.anchor).toBeNull();

		// An edit keeps the anchor it has, whatever it is sent.
		const moved = { ...words, exact: 'other words' };
		const edited = await store.saveNote(ken, {
			...note('turing', 'now clear'),
			id: a.id,
			anchor: moved
		});
		expect(edited).toMatchObject({ text: 'now clear', anchor: words });

		await store.saveNote(ken, { ...note('turing', 'still?', true), id: a.id });
		expect((await store.flaggedNotes(ken)).map((f) => [f.text, f.anchor])).toEqual([
			['still?', words]
		]);
		expect((await store.notes(ken, 'ai')).map((n) => n.anchor)).toEqual([words, null]);
	});
});

const answer = (id: string, frame = context.frame.id) => ({
	...keptAnswer(
		{
			id,
			subject: 'western-civ',
			context,
			question: 'Why?',
			answer: 'Ink [2].',
			provider: 'claude-cli',
			model: 'claude-sonnet-5',
			askedAt: '2026-09-27T17:05:09.000Z'
		},
		new Date('2026-09-27T17:06:00Z')
	),
	anchor: { frame, trail: null }
});

describe('kept answers', () => {
	it('are counted per frame, listed per frame, grown and forgotten, per reader', async () => {
		const store = openReaderStore(':memory:', clock());
		await store.keep(ken, answer('20260927T170509Z-00000001', 'printing-press'));
		await store.keep(ken, answer('20260927T170509Z-00000002', 'printing-press'));
		await store.keep(ken, answer('20260927T170509Z-00000003', 'fire'));
		await store.keep(ken, answer('20260927T170509Z-00000003', 'fire'));
		await store.keep(ada, answer('20260927T170509Z-00000004', 'fire'));
		expect(await store.keptCounts(ken, 'western-civ')).toEqual({ 'printing-press': 2, fire: 1 });
		expect(await store.keptCounts(ken, 'ai')).toEqual({});

		const id = '20260927T170509Z-00000001';
		expect(await store.kept(ken, 'western-civ', id)).toMatchObject({ id, question: 'Why?' });
		expect(await store.kept(ada, 'western-civ', id)).toBeNull();
		expect(await store.kept(ken, 'ai', id)).toBeNull();

		await store.grew(ken, 'western-civ', id, ['luther-theses']);
		const on = await store.keptOn(ken, 'western-civ', 'printing-press');
		expect(on.map((k) => [k.answer.id, k.grown])).toEqual([
			[id, ['luther-theses']],
			['20260927T170509Z-00000002', null]
		]);
		// Keeping it again keeps what it grew into.
		await store.keep(ken, answer(id, 'printing-press'));
		expect((await store.keptOn(ken, 'western-civ', 'printing-press'))[0].grown).toEqual([
			'luther-theses'
		]);

		expect(await store.forget(ada, 'western-civ', id)).toBe(false);
		expect(await store.forget(ken, 'western-civ', id)).toBe(true);
		expect(await store.keptCounts(ken, 'western-civ')).toEqual({ 'printing-press': 1, fire: 1 });
	});
});

describe('export and import', () => {
	it('carries notes and kept answers through the export format', async () => {
		const from = openReaderStore(':memory:', clock());
		const n = (await from.saveNote(ken, note('turing', 'look again', true)))!;
		const a = (await from.saveNote(ken, { ...note('turing', 'these words'), anchor: words }))!;
		await from.keep(ken, answer('20260927T170509Z-00000001'));
		await from.grew(ken, 'western-civ', '20260927T170509Z-00000001', ['luther-theses']);
		const parsed = parseExport(JSON.parse(JSON.stringify(await from.exportData(ken))));
		if ('error' in parsed) throw new Error(parsed.error);

		const to = openReaderStore(':memory:', clock());
		expect(await to.importData(ada, parsed)).toMatchObject({ notes: 2, kept: 1 });
		expect(await to.notes(ada, 'ai')).toEqual([n, a]);
		expect(await to.keptOn(ada, 'western-civ', context.frame.id)).toMatchObject([
			{ grown: ['luther-theses'] }
		]);
		// An older copy of a note does not overwrite a newer one.
		await to.saveNote(ada, { ...note('turing', 'newer'), id: n.id });
		await to.importData(ada, parsed);
		expect((await to.notes(ada, 'ai'))[0].text).toBe('newer');
	});

	it('round-trips through the export format into another reader', async () => {
		const from = openReaderStore(':memory:', clock());
		await from.visit(ken, at('ai', 'turing'));
		await from.bookmark(ken, at('western-civ', 'fire'));
		const file = JSON.parse(JSON.stringify(await from.exportData(ken)));
		const parsed = parseExport(file);
		if ('error' in parsed) throw new Error(parsed.error);

		const to = openReaderStore(':memory:', clock(Date.parse('2026-01-01T00:00:00Z')));
		expect(await to.importData(ada, parsed)).toEqual({
			places: 1,
			bookmarks: 1,
			notes: 0,
			kept: 0,
			readings: 1,
			seen: 1
		});
		expect(await to.lastVisited(ada, 'ai')).toMatchObject({
			frame: 'turing',
			at: '2026-09-28T12:00:01.000Z'
		});
		expect(await to.bookmarks(ada)).toMatchObject([{ subject: 'western-civ', frame: 'fire' }]);
	});

	it('never moves a place back in time', async () => {
		const store = openReaderStore(':memory:', clock());
		await store.visit(ken, at('ai', 'transformer'));
		await store.importData(ken, {
			kloom: 'reader-data',
			version: 4,
			reader: ken,
			exported: '2026-01-01T00:00:00.000Z',
			places: [{ ...at('ai', 'turing'), at: '2026-01-01T00:00:00.000Z' }],
			bookmarks: [],
			notes: [],
			kept: [],
			readings: [],
			seen: []
		});
		expect(await store.lastVisited(ken, 'ai')).toMatchObject({ frame: 'transformer' });
	});
});

describe('the file', () => {
	let dir: string | undefined;
	afterEach(() => {
		if (dir) rmSync(dir, { recursive: true, force: true });
	});

	it('is created with its directory, migrated, and keeps what it holds across opens', async () => {
		dir = mkdtempSync(join(tmpdir(), 'kloom-reader-'));
		const path = join(dir, 'nested', 'reader.db');
		const first = openReaderStore(path, clock());
		await first.bookmark(ken, at('ai', 'turing'));
		first.close();

		const raw = new DatabaseSync(path);
		expect(raw.prepare('PRAGMA user_version').get()).toEqual({ user_version: SCHEMA_VERSION });
		raw.close();

		const again = openReaderStore(path, clock());
		expect(await again.bookmarks(ken)).toHaveLength(1);
		again.close();
	});

	it('moves a file made at schema 1 forward, keeping what it held', async () => {
		dir = mkdtempSync(join(tmpdir(), 'kloom-reader-'));
		const path = join(dir, 'reader.db');
		// Sprint 009's schema, as it shipped.
		const raw = new DatabaseSync(path);
		raw.exec(`CREATE TABLE place (reader TEXT NOT NULL, subject TEXT NOT NULL, frame TEXT NOT NULL,
			label TEXT NOT NULL, at TEXT NOT NULL, PRIMARY KEY (reader, subject));
		CREATE INDEX place_recent ON place (reader, at);
		CREATE TABLE bookmark (reader TEXT NOT NULL, subject TEXT NOT NULL, frame TEXT NOT NULL,
			label TEXT NOT NULL, at TEXT NOT NULL, PRIMARY KEY (reader, subject, frame));
		INSERT INTO bookmark VALUES ('ken@github', 'ai', 'turing', 'Turing', '2026-09-28T12:00:00.000Z');
		PRAGMA user_version = 1;`);
		raw.close();
		const store = openReaderStore(path, clock());
		expect(await store.bookmarks(ken)).toHaveLength(1);
		expect(await store.saveNote(ken, note('turing', 'new table'))).toMatchObject({
			text: 'new table'
		});
		store.close();
	});

	it('moves a file made at schema 2 forward: its notes are notes on the whole frame', async () => {
		dir = mkdtempSync(join(tmpdir(), 'kloom-reader-'));
		const path = join(dir, 'reader.db');
		// Sprint 011's schema, as it shipped (indexes left out).
		const raw = new DatabaseSync(path);
		raw.exec(`CREATE TABLE place (reader TEXT NOT NULL, subject TEXT NOT NULL, frame TEXT NOT NULL,
			label TEXT NOT NULL, at TEXT NOT NULL, PRIMARY KEY (reader, subject));
		CREATE TABLE bookmark (reader TEXT NOT NULL, subject TEXT NOT NULL, frame TEXT NOT NULL,
			label TEXT NOT NULL, at TEXT NOT NULL, PRIMARY KEY (reader, subject, frame));
		CREATE TABLE kept (reader TEXT NOT NULL, subject TEXT NOT NULL, id TEXT NOT NULL,
			frame TEXT NOT NULL, answer TEXT NOT NULL, grown TEXT, kept_at TEXT NOT NULL,
			PRIMARY KEY (reader, id));
		CREATE TABLE note (reader TEXT NOT NULL, id TEXT NOT NULL, subject TEXT NOT NULL,
			frame TEXT NOT NULL, label TEXT NOT NULL, text TEXT NOT NULL,
			review TEXT NOT NULL DEFAULT 'none' CHECK (review IN ('none', 'flagged', 'handled')),
			response TEXT, created TEXT NOT NULL, updated TEXT NOT NULL, PRIMARY KEY (reader, id));
		INSERT INTO note VALUES ('ken@github', 'n1', 'ai', 'turing', 'Turing', 'old', 'flagged', NULL,
			'2026-09-28T12:00:00.000Z', '2026-09-28T12:00:00.000Z');
		PRAGMA user_version = 2;`);
		raw.close();
		const store = openReaderStore(path, clock());
		expect(await store.notes(ken, 'ai')).toMatchObject([{ id: 'n1', text: 'old', anchor: null }]);
		expect((await store.flaggedNotes())[0]).toMatchObject({ id: 'n1', anchor: null });
		store.close();
	});

	it('moves a file made at schema 3 forward: answers already given count as unseen', async () => {
		dir = mkdtempSync(join(tmpdir(), 'kloom-reader-'));
		const path = join(dir, 'reader.db');
		const before = openReaderStore(path, clock());
		const n = (await before.saveNote(ken, note('turing', 'old', true)))!;
		await before.handleNote(ken, n.id, 'Fixed.');
		await before.saveNote(ken, note('turing', 'plain'));
		before.close();
		// Back to sprint 012's schema, as a file from before this one would be.
		const raw = new DatabaseSync(path);
		raw.exec(`ALTER TABLE note DROP COLUMN unseen;
			DROP TABLE account; DROP TABLE session; DROP TABLE invite; DROP TABLE suggestion;
			DROP TABLE reading; DROP TABLE seen; DROP TABLE activity; DROP TABLE ask_cost; DROP TABLE ask_access;
			PRAGMA user_version = 3;`);
		raw.close();
		const store = openReaderStore(path, clock());
		expect(await store.unseenAnswers(ken)).toBe(1);
		expect((await store.allNotes(ken)).map((x) => [x.text, x.unseen])).toEqual([
			['plain', false],
			['old', true]
		]);
		store.close();
	});

	it('moves a file made at schema 4 forward: the accounts arrive, the notes stay', async () => {
		dir = mkdtempSync(join(tmpdir(), 'kloom-reader-'));
		const path = join(dir, 'reader.db');
		const before = openReaderStore(path, clock());
		await before.saveNote(ken, note('turing', 'kept'));
		before.close();
		// Back to sprint 034's schema, before the reader edition's sign-in.
		const raw = new DatabaseSync(path);
		raw.exec(`DROP TABLE account; DROP TABLE session; DROP TABLE invite; DROP TABLE suggestion;
			DROP TABLE reading; DROP TABLE seen; DROP TABLE activity; DROP TABLE ask_cost; DROP TABLE ask_access;
			PRAGMA user_version = 4;`);
		raw.close();
		const store = openReaderStore(path, clock());
		expect((await store.allNotes(ken)).map((x) => x.text)).toEqual(['kept']);
		store.close();
		const after = new DatabaseSync(path);
		expect(after.prepare('SELECT count(*) AS n FROM account').get()).toEqual({ n: 0 });
		expect(after.prepare('PRAGMA user_version').get()).toEqual({ user_version: SCHEMA_VERSION });
		after.close();
	});

	it('moves a file made at schema 5 forward: suggestions arrive, the readers stay', async () => {
		dir = mkdtempSync(join(tmpdir(), 'kloom-reader-'));
		const path = join(dir, 'reader.db');
		const before = openReaderStore(path, clock());
		await before.saveNote(ken, note('turing', 'kept'));
		before.close();
		// Back to sprint 039's schema, the one the public site first shipped with.
		const raw = new DatabaseSync(path);
		raw.exec(`DROP TABLE suggestion;
			DROP TABLE reading; DROP TABLE seen; DROP TABLE activity; DROP TABLE ask_cost; DROP TABLE ask_access; PRAGMA user_version = 5;`);
		raw.close();
		const store = openReaderStore(path, clock());
		expect((await store.allNotes(ken)).map((x) => x.text)).toEqual(['kept']);
		expect(await store.suggestions(ken)).toEqual([]);
		store.close();
	});

	it('moves a file made at schema 7 forward: the ask ledger arrives, the readers stay (sprint 046)', async () => {
		dir = mkdtempSync(join(tmpdir(), 'kloom-reader-'));
		const path = join(dir, 'reader.db');
		const before = openReaderStore(path, clock());
		await before.saveNote(ken, note('turing', 'kept'));
		before.close();
		// Back to sprint 043's schema, the one the public site ran before ask.
		const raw = new DatabaseSync(path);
		raw.exec(`DROP TABLE ask_cost; DROP TABLE ask_access; PRAGMA user_version = 7;`);
		raw.close();
		const store = openReaderStore(path, clock());
		expect((await store.allNotes(ken)).map((x) => x.text)).toEqual(['kept']);
		store.close();
		const after = new DatabaseSync(path);
		expect(after.prepare('SELECT count(*) AS n FROM ask_cost').get()).toEqual({ n: 0 });
		expect(after.prepare('SELECT count(*) AS n FROM ask_access').get()).toEqual({ n: 0 });
		expect(after.prepare('PRAGMA user_version').get()).toEqual({ user_version: SCHEMA_VERSION });
		after.close();
	});

	it('refuses a file from a newer app rather than guess at its schema', () => {
		dir = mkdtempSync(join(tmpdir(), 'kloom-reader-'));
		const path = join(dir, 'reader.db');
		const raw = new DatabaseSync(path);
		raw.exec(`PRAGMA user_version = ${SCHEMA_VERSION + 1}`);
		raw.close();
		expect(() => openReaderStore(path)).toThrow(/newer than this app/);
	});
});

describe('kept-answer files from before the store', () => {
	let dir: string | undefined;
	afterEach(() => {
		if (dir) rmSync(dir, { recursive: true, force: true });
	});

	it('move in once, under one reader, with what grow made of them', async () => {
		dir = mkdtempSync(join(tmpdir(), 'kloom-kept-files-'));
		const kept = join(dir, 'western-civ', 'kept');
		const grow = join(dir, 'western-civ', 'grow');
		await mkdir(kept, { recursive: true });
		await mkdir(grow, { recursive: true });
		const id = '20260927T170509Z-00000001';
		await writeFile(join(kept, `${id}.json`), JSON.stringify(answer(id)));
		await writeFile(join(kept, 'broken.json'), '{"kind": "nope"}');
		await writeFile(
			join(grow, 'job.json'),
			JSON.stringify({ status: 'done', kept: id, result: { frames: ['luther-theses'] } })
		);
		const store = openReaderStore(':memory:', clock());

		const first = await migrateKeptFiles(store, dir, ken);
		expect(first.moved).toHaveLength(1);
		expect(first.refused).toEqual([join(kept, 'broken.json')]);
		expect(await store.keptOn(ken, 'western-civ', context.frame.id)).toMatchObject([
			{ answer: { id }, grown: ['luther-theses'] }
		]);
		expect(await readdir(kept)).toEqual(['broken.json']);
		expect(await readdir(join(dir, 'western-civ', 'kept-migrated'))).toEqual([`${id}.json`]);

		const again = await migrateKeptFiles(store, dir, ken);
		expect(again.moved).toEqual([]);
	});
});

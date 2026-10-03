import { beforeEach, describe, expect, it } from 'vitest';
import type { Reader } from '$lib/server/reader';
import { openReaderStore, useReaderStore } from '$lib/server/reader-store';
import { DELETE as unmark, GET as marks, POST as mark } from './bookmarks/+server';
import { GET as exportData } from './export/+server';
import { POST as importData } from './import/+server';
import { DELETE as forget, GET as keptOn } from './kept/+server';
import { GET as myNotes, POST as seeNotes } from './my-notes/+server';
import {
	DELETE as dropNote,
	GET as notes,
	PATCH as flagNote,
	POST as saveNote
} from './notes/+server';
import { POST as visit } from './place/+server';
import { POST as catchUp } from './caught-up/+server';
import { POST as markSeen } from './seen/+server';
import { readerNews } from '$lib/server/whats-new';
import { GET as suggestions, POST as suggest } from './suggestions/+server';
import { keptAnswer } from '$engine/ai/kept';
import { context } from '$engine/ai/fixture';
import { SUGGESTIONS_WAITING_MAX as WAITING_MAX } from '$engine/reader-data';
import { readerStore } from '$lib/server/reader-store';

/** A handler's response, or the error it threw (SvelteKit's `error()` throws). */
const call = (handler: (e: never) => unknown, event: object) =>
	Promise.resolve()
		.then(() => handler(event as never))
		.catch((e: { status: number }) => e);

const ken: Reader = { login: 'ken@github', name: 'Ken', via: 'tailscale-serve' };
const ada: Reader = { login: 'ada@github', name: 'Ada', via: 'tailscale-serve' };

const send = (method: string, body: unknown, reader: Reader | null = ken) => ({
	request: new Request('http://x/', { method, body: JSON.stringify(body) }),
	locals: { reader }
});
const read = (reader: Reader | null = ken) => ({ locals: { reader } });
const get = (query: string, reader: Reader | null = ken) => ({
	url: new URL(`http://x/${query}`),
	locals: { reader }
});
const body = async (r: unknown) => (r as Response).json();

const first = { subject: 'western-civ', frame: 'prometheus', label: 'We stole FIRE.' };

beforeEach(() => useReaderStore(openReaderStore(':memory:')));

describe('reader data needs a reader', () => {
	it('refuses every route with none, reads included', async () => {
		expect(await call(visit, send('POST', first, null))).toMatchObject({ status: 401 });
		expect(await call(mark, send('POST', first, null))).toMatchObject({ status: 401 });
		expect(await call(unmark, send('DELETE', first, null))).toMatchObject({ status: 401 });
		expect(await call(marks, read(null))).toMatchObject({ status: 401 });
		expect(await call(exportData, read(null))).toMatchObject({ status: 401 });
		expect(await call(importData, send('POST', {}, null))).toMatchObject({ status: 401 });
		expect(await call(notes, get('?subject=ai', null))).toMatchObject({ status: 401 });
		expect(await call(saveNote, send('POST', {}, null))).toMatchObject({ status: 401 });
		expect(await call(dropNote, send('DELETE', {}, null))).toMatchObject({ status: 401 });
		expect(await call(flagNote, send('PATCH', {}, null))).toMatchObject({ status: 401 });
		expect(await call(myNotes, read(null))).toMatchObject({ status: 401 });
		expect(await call(suggestions, read(null))).toMatchObject({ status: 401 });
		expect(await call(suggest, send('POST', { title: 'x' }, null))).toMatchObject({ status: 401 });
		expect(await call(seeNotes, send('POST', { ids: [] }, null))).toMatchObject({ status: 401 });
		expect(await call(keptOn, get('?subject=ai&frame=turing', null))).toMatchObject({
			status: 401
		});
		expect(await call(forget, send('DELETE', {}, null))).toMatchObject({ status: 401 });
		expect(await call(markSeen, send('POST', {}, null))).toMatchObject({ status: 401 });
		expect(await call(catchUp, send('POST', {}, null))).toMatchObject({ status: 401 });
	});
});

describe('what is new to a reader (korg 3525)', () => {
	it('is, in a subject they started, what was added after and not opened; opening or marking clears it', async () => {
		const store = readerStore();
		// Started western-civ before anything was added: every dated frame since is new.
		await store.importData(ken.login, {
			kloom: 'reader-data',
			version: 4,
			reader: ken.login,
			exported: '2000-01-01T00:00:00.000Z',
			places: [],
			bookmarks: [],
			notes: [],
			kept: [],
			readings: [{ subject: 'western-civ', first: '2000-01-01T00:00:00.000Z', caughtUp: null }],
			seen: []
		});
		const before = (await readerNews(store, ken.login)).fresh['western-civ'] ?? [];
		// The gate's library is dated from this repository's own history.
		expect(before).toContain('prometheus');
		expect((await readerNews(store, ada.login)).fresh).toEqual({});

		await call(visit, send('POST', first));
		expect((await readerNews(store, ken.login)).fresh['western-civ']).not.toContain('prometheus');
		expect(
			await body(
				await call(
					markSeen,
					send('POST', { subject: 'western-civ', frames: ['writing', 'writing'] })
				)
			)
		).toEqual({ ok: true });
		expect((await readerNews(store, ken.login)).fresh['western-civ']).not.toContain('writing');

		const r = await body(await call(catchUp, send('POST', { subject: 'western-civ' })));
		expect(r.first).toBe('2000-01-01T00:00:00.000Z');
		expect(Date.parse(r.caughtUp)).toBeGreaterThan(Date.parse(r.first));
		expect((await readerNews(store, ken.login)).fresh['western-civ']).toBeUndefined();
	});

	it('refuses frames a subject does not have, and a subject the app does not serve', async () => {
		expect(
			await call(markSeen, send('POST', { subject: 'western-civ', frames: ['nope'] }))
		).toMatchObject({ status: 400 });
		expect(
			await call(markSeen, send('POST', { subject: 'western-civ', frames: 'writing' }))
		).toMatchObject({ status: 400 });
		expect(await call(markSeen, send('POST', { subject: 'nope', frames: [] }))).toMatchObject({
			status: 404
		});
		expect(await call(catchUp, send('POST', { subject: '../x' }))).toMatchObject({ status: 404 });
	});
});

describe('a place or bookmark names a served subject and one of its frames', () => {
	it('refuses a subject the app does not serve', async () => {
		for (const subject of [undefined, 'nope', '../western-civ'])
			expect(await call(visit, send('POST', { ...first, subject }))).toMatchObject({
				status: 404
			});
	});

	it('refuses a frame the subject does not have, or a path for one', async () => {
		for (const frame of ['no-such-frame', '../ai', undefined])
			expect(await call(mark, send('POST', { ...first, frame }))).toMatchObject({ status: 400 });
	});
});

describe('bookmarks', () => {
	it('are kept per reader and removed on request', async () => {
		await call(mark, send('POST', first));
		await call(mark, send('POST', { subject: 'ai', frame: 'alexnet', label: 'AlexNet' }));
		expect((await body(await call(marks, read()))).map((b: { frame: string }) => b.frame)).toEqual(
			expect.arrayContaining(['prometheus', 'alexnet'])
		);
		expect(await body(await call(marks, read(ada)))).toEqual([]);
		await call(unmark, send('DELETE', { subject: 'western-civ', frame: 'prometheus' }));
		expect(await body(await call(marks, read()))).toMatchObject([{ frame: 'alexnet' }]);
	});
});

describe('export and import', () => {
	it('exports a reader’s data as a file, and imports it under another', async () => {
		await call(visit, send('POST', first));
		await call(mark, send('POST', first));
		const res = (await call(exportData, read())) as Response;
		expect(res.headers.get('content-disposition')).toMatch(
			/^attachment; filename="kloom-reader-data-\d{4}-\d{2}-\d{2}\.json"$/
		);
		const file = await res.json();
		expect(file).toMatchObject({ kloom: 'reader-data', version: 4, reader: 'ken@github' });

		expect(await body(await call(importData, send('POST', file, ada)))).toEqual({
			places: 1,
			bookmarks: 1,
			notes: 0,
			kept: 0,
			readings: 1,
			seen: 1
		});
		expect(await body(await call(marks, read(ada)))).toMatchObject([{ frame: 'prometheus' }]);
	});

	it('refuses a file it cannot read, saying why', async () => {
		expect(await call(importData, send('POST', { kloom: 'other' }))).toMatchObject({
			status: 400,
			body: { message: 'Not an export kloom can read: not a kloom reader-data export.' }
		});
	});
});

const aNote = { subject: 'ai', frame: 'alexnet', label: 'AlexNet', text: 'Why GPUs?', flag: true };

describe('notes', () => {
	it('are written, listed, edited and deleted, each reader their own', async () => {
		const saved = await body(await call(saveNote, send('POST', aNote)));
		expect(saved).toMatchObject({ frame: 'alexnet', text: 'Why GPUs?', review: 'flagged' });
		expect(await body(await call(notes, get('?subject=ai')))).toEqual([saved]);
		expect(await body(await call(notes, get('?subject=ai', ada)))).toEqual([]);

		const edit = { ...aNote, id: saved.id, text: 'Why GPUs, really?', flag: false };
		expect(await body(await call(saveNote, send('POST', edit)))).toMatchObject({
			id: saved.id,
			text: 'Why GPUs, really?',
			review: 'none'
		});
		expect(await call(saveNote, send('POST', edit, ada))).toMatchObject({ status: 404 });
		expect(await call(dropNote, send('DELETE', { id: saved.id }, ada))).toMatchObject({
			status: 404
		});
		await call(dropNote, send('DELETE', { id: saved.id }));
		expect(await body(await call(notes, get('?subject=ai')))).toEqual([]);
	});

	it('refuse an empty or oversized note, a bad id, and a frame the subject lacks', async () => {
		for (const bad of [
			{ ...aNote, text: '  ' },
			{ ...aNote, text: 'x'.repeat(10_001) },
			{ ...aNote, id: '../x' },
			{ ...aNote, frame: 'no-such-frame' },
			{ ...aNote, anchor: { exact: '', prefix: '', suffix: '', start: 0 } },
			{ ...aNote, anchor: 'the words' }
		])
			expect(await call(saveNote, send('POST', bad))).toMatchObject({ status: 400 });
		expect(await call(notes, get('?subject=nope'))).toMatchObject({ status: 404 });
	});
});

describe('annotations', () => {
	it('are notes that keep the words they are on', async () => {
		const anchor = { exact: 'on GPUs', prefix: 'trained ', suffix: '.', start: 20 };
		const saved = await body(await call(saveNote, send('POST', { ...aNote, anchor })));
		expect(saved).toMatchObject({ text: 'Why GPUs?', anchor, review: 'flagged' });
		expect(await body(await call(notes, get('?subject=ai')))).toEqual([saved]);
		const edit = { ...aNote, id: saved.id, text: 'Now I see.' };
		expect(await body(await call(saveNote, send('POST', edit)))).toMatchObject({ anchor });
	});
});

describe('my notes', () => {
	it('lists every note across subjects, with where each is now, and the answers waiting', async () => {
		const a = await body(await call(saveNote, send('POST', aNote)));
		const b = await body(
			await call(saveNote, send('POST', { ...first, text: 'On fire', flag: false }))
		);
		await call(saveNote, send('POST', { ...aNote, text: 'hers' }, ada));
		await readerStore().handleNote(ken.login, a.id, 'Answered.');
		// A note whose frame went away (an import from elsewhere) is listed, with nowhere to go.
		await readerStore().importData(ken.login, {
			kloom: 'reader-data',
			version: 4,
			reader: ken.login,
			exported: '2026-10-01T00:00:00.000Z',
			places: [],
			bookmarks: [],
			notes: [{ ...b, id: 'gone', frame: 'no-such-frame', updated: '2020-01-01T00:00:00.000Z' }],
			kept: [],
			readings: [],
			seen: []
		});
		const got = await body(await call(myNotes, read()));
		expect(got.unseen).toBe(1);
		// The last written first: the two written now, in either order within a millisecond.
		const ids = got.notes.map((n: { id: string }) => n.id);
		expect(ids.slice(0, 2).sort()).toEqual([a.id, b.id].sort());
		expect(ids[2]).toBe('gone');
		expect(got.notes.find((n: { id: string }) => n.id === a.id)).toMatchObject({
			review: 'handled',
			unseen: true,
			subjectTitle: expect.any(String),
			topic: expect.any(String),
			position: expect.any(String)
		});
		expect(got.notes[2]).toMatchObject({ subject: 'western-civ', topic: null, position: null });
		expect((await body(await call(myNotes, read(ada)))).notes).toHaveLength(1);

		expect(await body(await call(seeNotes, send('POST', { ids: [a.id] })))).toEqual({ unseen: 0 });
		expect(await call(seeNotes, send('POST', { ids: ['../x'] }))).toMatchObject({ status: 400 });
		expect(await call(seeNotes, send('POST', {}))).toMatchObject({ status: 400 });
	});

	it('flags a note without its text, and clears several at once, only the reader’s own', async () => {
		const a = await body(await call(saveNote, send('POST', { ...aNote, flag: false })));
		const b = await body(await call(saveNote, send('POST', aNote)));
		const c = await body(await call(saveNote, send('POST', aNote, ada)));
		expect(await body(await call(flagNote, send('PATCH', { id: a.id, flag: true })))).toMatchObject(
			{ id: a.id, review: 'flagged', text: aNote.text }
		);
		expect(await call(flagNote, send('PATCH', { id: a.id, flag: true }, ada))).toMatchObject({
			status: 404
		});
		expect(await call(flagNote, send('PATCH', { id: a.id }))).toMatchObject({ status: 400 });

		expect(await body(await call(dropNote, send('DELETE', { ids: [a.id, b.id, c.id] })))).toEqual({
			deleted: 2
		});
		expect((await body(await call(myNotes, read()))).notes).toEqual([]);
		expect((await body(await call(myNotes, read(ada)))).notes).toHaveLength(1);
		expect(await call(dropNote, send('DELETE', { ids: 'all' }))).toMatchObject({ status: 400 });
	});
});

describe('kept answers', () => {
	const id = '20260927T170509Z-0a1b2c3d';
	beforeEach(() =>
		readerStore().keep(
			ken.login,
			keptAnswer(
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
				new Date()
			)
		)
	);
	const where = `?subject=western-civ&frame=${context.frame.id}`;

	it('are listed per frame for their reader only, and forgotten on request', async () => {
		expect(await body(await call(keptOn, get(where)))).toMatchObject([
			{ answer: { id, question: 'Why?' }, grown: null }
		]);
		expect(await body(await call(keptOn, get(where, ada)))).toEqual([]);
		expect(await call(keptOn, get('?subject=western-civ&frame=../x'))).toMatchObject({
			status: 400
		});
		expect(await call(forget, send('DELETE', { subject: 'western-civ', id }, ada))).toMatchObject({
			status: 404
		});
		await call(forget, send('DELETE', { subject: 'western-civ', id }));
		expect(await body(await call(keptOn, get(where)))).toEqual([]);
	});
});

describe('suggestions', () => {
	const idea = { title: '  Music  ', cover: 'From plainchant to the synthesiser.' };

	it('are kept under the reader, with their name, and listed back to them alone', async () => {
		const made = await call(suggest, send('POST', idea));
		expect(made).toMatchObject({ status: 201 });
		expect(await body(made)).toMatchObject({ title: 'Music', why: '', status: 'new' });
		expect(await body(await call(suggestions, read()))).toMatchObject([{ title: 'Music' }]);
		expect(await body(await call(suggestions, read(ada)))).toEqual([]);
		expect((await readerStore().allSuggestions())[0]).toMatchObject({
			reader: ken.login,
			name: 'Ken'
		});
	});

	it('refuses one with no title, or too long', async () => {
		expect(await call(suggest, send('POST', { cover: 'no title' }))).toMatchObject({ status: 400 });
		expect(await call(suggest, send('POST', { title: 'x'.repeat(121) }))).toMatchObject({
			status: 400
		});
		expect(await call(suggest, send('POST', { title: 'ok', why: 7 }))).toMatchObject({
			status: 400
		});
	});

	it(`stops at ${WAITING_MAX} waiting`, async () => {
		for (let i = 0; i < WAITING_MAX; i++) await call(suggest, send('POST', { title: `s${i}` }));
		expect(await call(suggest, send('POST', { title: 'one more' }))).toMatchObject({ status: 429 });
		const [last] = await readerStore().suggestions(ken.login);
		await readerStore().markSuggestion(ken.login, last.id, 'planned');
		expect(await call(suggest, send('POST', { title: 'one more' }))).toMatchObject({ status: 201 });
	});
});

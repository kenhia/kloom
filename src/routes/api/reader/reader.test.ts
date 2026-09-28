import { beforeEach, describe, expect, it } from 'vitest';
import type { Reader } from '$lib/server/reader';
import { openReaderStore, useReaderStore } from '$lib/server/reader-store';
import { DELETE as unmark, GET as marks, POST as mark } from './bookmarks/+server';
import { GET as exportData } from './export/+server';
import { POST as importData } from './import/+server';
import { POST as visit } from './place/+server';

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
		expect(file).toMatchObject({ kloom: 'reader-data', version: 1, reader: 'ken@github' });

		expect(await body(await call(importData, send('POST', file, ada)))).toEqual({
			places: 1,
			bookmarks: 1
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

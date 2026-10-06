import { beforeEach, describe, expect, it } from 'vitest';
import type { Reader } from '$lib/server/reader';
import { openAdmins, type Admins } from '$lib/server/admins';
import { openReaderStore, useAdmins, useReaderStore } from '$lib/server/reader-store';
import { openReaderDb } from '$lib/server/sqlite-reader-store';
import type { ReaderStore } from '$engine/reader-data';
import { load } from './+page.server';

const ken: Reader = { login: 'ken@kloom.example', name: 'Ken', via: 'session' };
const ada: Reader = { login: 'ada@kloom.example', name: 'Ada', via: 'session' };

/** The load's data, or the error it threw (SvelteKit's `error()` throws). */
const run = (reader: Reader | null) =>
	Promise.resolve()
		.then(() => load({ locals: { reader } } as never))
		.catch((e: { status: number }) => e) as Promise<
		{ rows: { subject: string; cells: { id: string; readers: number; level: number }[] }[] } & {
			status?: number;
		}
	>;

let store: ReaderStore;
let admins: Admins;
beforeEach(() => {
	const db = openReaderDb(':memory:');
	store = openReaderStore(db);
	admins = openAdmins(db);
	useReaderStore(store);
	useAdmins(admins);
	admins.enable(ken.login);
});

describe('the traffic page (korg 3570)', () => {
	it('is a 404 to a reader who is not an admin, and to no reader at all', async () => {
		expect(await run(ada)).toMatchObject({ status: 404 });
		expect(await run(null)).toMatchObject({ status: 404 });
		admins.disable(ken.login);
		expect(await run(ken)).toMatchObject({ status: 404 });
	});

	it('gives an admin a row per served subject, lit by distinct readers 0/1/2/3/4+', async () => {
		const readers = ['a', 'b', 'c', 'd', 'e'].map((r) => `${r}@kloom.example`);
		const lit: Record<string, number> = { prometheus: 1, writing: 2, 'printing-press': 3 };
		for (const [frame, n] of Object.entries(lit))
			for (const r of readers.slice(0, n)) await store.frameVisit(r, 'western-civ', frame);
		for (const r of readers) await store.markSeen(r, 'western-civ', ['alexander']);
		const data = await run(ken);
		expect(data.status).toBeUndefined();
		const civ = data.rows.find((r) => r.subject === 'western-civ')!;
		const level = (id: string) => civ.cells.find((c) => c.id === id)!.level;
		expect([
			level('prometheus'),
			level('writing'),
			level('printing-press'),
			level('alexander')
		]).toEqual([1, 2, 3, 4]);
		expect(civ.cells.find((c) => c.id === 'alexander')!.readers).toBe(5);
		expect(civ.cells.filter((c) => c.level === 0).length).toBe(civ.cells.length - 4);
		expect(data.rows.map((r) => r.subject)).toContain('ai');
	});
});

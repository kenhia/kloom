import { describe, expect, it } from 'vitest';
import { POST as ask } from './ask/+server';
import { GET as jobs, POST as grow } from './grow/+server';
import { POST as keep } from './keep/+server';
import { GET as startLook } from './start/[subject]/+server';
import { answers } from '$lib/server/ask';

/** A handler's response, or the error it threw (SvelteKit's `error()` throws). */
const call = (handler: (e: never) => unknown, event: object) =>
	Promise.resolve()
		.then(() => handler(event as never))
		.catch((e: { status: number }) => e);

const post = (body: object) => ({
	request: new Request('http://x/', { method: 'POST', body: JSON.stringify(body) }),
	// The hook has let a write through, so there is a reader.
	locals: { reader: { login: 'ken@test', name: 'Ken', via: 'ssh' } }
});

describe('every API names its subject', () => {
	const unknown = [undefined, 'nope', '..', '../western-civ', 'western-civ/..'];

	it('ask refuses a subject the app does not serve', async () => {
		for (const subject of unknown)
			expect(
				await call(ask, post({ subject, frame: 'printing-press', question: 'Why?' }))
			).toMatchObject({ status: 404 });
	});

	it('grow refuses one, for queueing and for listing', async () => {
		for (const subject of unknown) {
			expect(
				await call(grow, post({ subject, verb: 'frames', frame: 'printing-press', request: 'x' }))
			).toMatchObject({ status: 404 });
			const url = new URL('http://x/api/grow');
			if (subject) url.searchParams.set('subject', subject);
			expect(await call(jobs, { url })).toMatchObject({ status: 404 });
		}
	});

	it('keep will not keep an answer under another subject', async () => {
		const id = '20260927T170911Z-bdded89b';
		answers.add({
			id,
			subject: 'western-civ',
			context: {} as never,
			question: 'Why?',
			answer: 'Because.',
			provider: 'test',
			model: 'm',
			askedAt: new Date().toISOString()
		});
		for (const subject of ['ai', undefined])
			expect(await call(keep, post({ subject, id }))).toMatchObject({ status: 404 });
	});

	it('the start look refuses one, and serves a served subject’s', async () => {
		for (const subject of unknown)
			expect(await call(startLook, { params: { subject } })).toMatchObject({ status: 404 });
		const res = (await call(startLook, { params: { subject: 'ai' } })) as Response;
		const look = await res.json();
		expect(look.illustrations.length).toBeGreaterThan(0);
		expect(look.palettes[look.palette]).toBeDefined();
	});

	it('ask takes a served subject past the subject check', async () => {
		expect(
			await call(ask, post({ subject: 'western-civ', frame: 'no-such-frame', question: 'Why?' }))
		).toMatchObject({ status: 400 });
	});
});

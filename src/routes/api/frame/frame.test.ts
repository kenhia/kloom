import { describe, expect, it } from 'vitest';
import type { ServedBody } from '$engine/served';
import { GET } from './[subject]/[frame]/+server';

const get = (subject: string, frame: string, headers: Record<string, string> = {}) =>
	Promise.resolve(
		GET({ params: { subject, frame }, request: new Request('http://x/', { headers }) } as never)
	).catch((e: { status: number }) => e);

describe('the frame endpoint', () => {
	it("sends a frame's body and its links, tagged with the build", async () => {
		const res = (await get('western-civ', 'prometheus')) as Response;
		expect(res.status).toBe(200);
		expect(res.headers.get('content-type')).toBe('application/json');
		const body = (await res.json()) as ServedBody;
		expect(body.readingHtml).toContain('<p>');
		expect(body.svg).toMatch(/^<svg/);
		expect(body.links.names.hesiod.name).toBe('Hesiod');
		const etag = res.headers.get('etag')!;
		expect(etag).toMatch(/^"\w+"$/);
		const again = (await get('western-civ', 'prometheus', { 'if-none-match': etag })) as Response;
		expect(again.status).toBe(304);
	});

	it("carries connections stored on another subject's frames", async () => {
		const res = (await get('western-civ', 'faraday-induction')) as Response;
		const { links } = (await res.json()) as ServedBody;
		expect(links.connections).toContainEqual(
			expect.objectContaining({ direction: 'in', subject: 'chemistry' })
		);
	});

	it('refuses an unknown subject or frame', async () => {
		for (const [s, f] of [
			['nope', 'prometheus'],
			['..', 'prometheus'],
			['western-civ', 'nope'],
			['western-civ', '../ai']
		])
			expect(await get(s, f)).toMatchObject({ status: 404 });
	});
});

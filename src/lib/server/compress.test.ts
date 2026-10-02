import { brotliDecompressSync, gunzipSync } from 'node:zlib';
import { describe, expect, it } from 'vitest';
import { compress } from './compress';

const page = '<!doctype html><p>' + 'A reading, long enough to be worth compressing. '.repeat(60);
const req = (encoding: string | null, method = 'GET') =>
	new Request('http://x/', { method, headers: encoding ? { 'accept-encoding': encoding } : {} });
const res = (body: string, type = 'text/html', headers: Record<string, string> = {}) =>
	new Response(body, { headers: { 'content-type': type, ...headers } });
const bytes = async (r: Response) => Buffer.from(await r.arrayBuffer());

describe('compressing a response', () => {
	it('sends Brotli when the client takes it, else gzip, and says it varies', async () => {
		const br = compress(req('gzip, deflate, br'), res(page));
		expect(br.headers.get('content-encoding')).toBe('br');
		expect(br.headers.get('vary')).toContain('Accept-Encoding');
		expect(brotliDecompressSync(await bytes(br)).toString()).toBe(page);
		const gz = compress(req('gzip'), res(page, 'application/json'));
		expect(gz.headers.get('content-encoding')).toBe('gzip');
		expect(gunzipSync(await bytes(gz)).toString()).toBe(page);
	});

	it('weakens a strong tag, since the bytes depend on the encoding', () => {
		const r = compress(req('br'), res(page, 'application/json', { etag: '"b1"' }));
		expect(r.headers.get('etag')).toBe('W/"b1"');
	});

	it("leaves alone what it should: ask's stream, small bodies, encoded ones and a client that takes none", async () => {
		const stream = res(page, 'application/x-ndjson');
		expect(compress(req('br'), stream)).toBe(stream);
		const small = res('{}', 'application/json', { 'content-length': '2' });
		expect(compress(req('br'), small)).toBe(small);
		const done = res(page, 'application/json', { 'content-encoding': 'br' });
		expect(compress(req('br'), done)).toBe(done);
		const plain = compress(req(null), res(page));
		expect(plain.headers.get('content-encoding')).toBeNull();
		expect((await bytes(plain)).toString()).toBe(page);
		const head = res(page);
		expect(compress(req('br', 'HEAD'), head)).toBe(head);
	});
});

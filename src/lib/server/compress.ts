import { Readable } from 'node:stream';
import type { ReadableStream as NodeReadableStream } from 'node:stream/web';
import { constants, createBrotliCompress, createGzip } from 'node:zlib';

/** What is worth compressing: pages, JSON, drawings, styles and scripts. Never ask's NDJSON stream. */
const COMPRESSIBLE =
	/^(text\/(html|css|javascript|plain)|application\/(json|javascript)|image\/svg\+xml)\b/;

/**
 * Compress a response the client can take compressed (docs/design.md
 * §Serving): Brotli, or gzip. Small and already-encoded bodies go as they
 * are. The app's own static files are compressed at build and never come here.
 */
export function compress(request: Request, response: Response): Response {
	const type = response.headers.get('content-type') ?? '';
	const length = Number(response.headers.get('content-length') ?? Infinity);
	if (
		!response.body ||
		request.method === 'HEAD' ||
		response.headers.has('content-encoding') ||
		!COMPRESSIBLE.test(type) ||
		length < 1024
	)
		return response;
	const accept = request.headers.get('accept-encoding') ?? '';
	const encoding = /\bbr\b/.test(accept) ? 'br' : /\bgzip\b/.test(accept) ? 'gzip' : null;
	const headers = new Headers(response.headers);
	headers.append('vary', 'Accept-Encoding');
	if (!encoding) return new Response(response.body, { status: response.status, headers });
	const squeeze =
		encoding === 'br'
			? createBrotliCompress({ params: { [constants.BROTLI_PARAM_QUALITY]: 5 } })
			: createGzip({ level: 6 });
	headers.set('content-encoding', encoding);
	headers.delete('content-length');
	// The bytes differ by encoding; what they say does not.
	const etag = headers.get('etag');
	if (etag && !etag.startsWith('W/')) headers.set('etag', `W/${etag}`);
	const body = Readable.toWeb(
		Readable.fromWeb(response.body as NodeReadableStream).pipe(squeeze)
	) as ReadableStream;
	return new Response(body, { status: response.status, statusText: response.statusText, headers });
}

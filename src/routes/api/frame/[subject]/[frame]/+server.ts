import { error } from '@sveltejs/kit';
import { servedBody, servedSubject } from '$lib/server/subject';
import type { RequestHandler } from './$types';

/**
 * One frame's body (docs/design.md §Serving): its reading, drawing,
 * citations and links, as `ServedBody`. The shell fetches it as the reader
 * comes to the frame, and its neighbours ahead. Tagged with the library's
 * build, so a fetch that has it already costs a 304. A read, open like the page.
 */
export const GET: RequestHandler = async ({ params, request }) => {
	await servedSubject(params.subject);
	const body = await servedBody(params.subject, params.frame);
	if (!body) error(404, 'No such frame.');
	const etag = `"${body.build.replace(/\W/g, '')}"`;
	const headers = {
		'content-type': 'application/json',
		etag,
		'cache-control': 'no-cache',
		'x-kloom-build': body.build
	};
	// Compression weakens the tag (hooks.server.ts); either form is this build.
	const asked = request.headers.get('if-none-match')?.replace(/^W\//, '');
	if (asked === etag) return new Response(null, { status: 304, headers });
	return new Response(body.json, { headers });
};

import { error } from '@sveltejs/kit';
import { servedMedia } from '$lib/server/subject';
import type { RequestHandler } from './$types';

/**
 * A frame's images and charts, for the reading pane: a file the library
 * lists for that frame, read from the media directory. An SVG opened on its own
 * is a document, so the policy forbids script and every other fetch.
 */
export const GET: RequestHandler = async ({ params }) => {
	const media = await servedMedia(params.subject, params.frame, params.file);
	if (!media) error(404, 'Not found');
	return new Response(new Uint8Array(media.body), {
		headers: {
			'content-type': media.type,
			'content-security-policy': "default-src 'none'; style-src 'unsafe-inline'; sandbox",
			'x-content-type-options': 'nosniff',
			'cache-control': 'public, max-age=300'
		}
	});
};

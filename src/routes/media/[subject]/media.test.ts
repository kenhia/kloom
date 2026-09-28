import { describe, expect, it } from 'vitest';
import { GET } from './[frame]/[file]/+server';

const get = (frame: string, file: string, subject = 'western-civ') =>
	Promise.resolve(GET({ params: { subject, frame, file } } as never)).catch(
		(e: { status: number }) => e
	);

describe('the media route', () => {
	it('refuses names that could leave the frame directory', async () => {
		for (const [frame, file] of [
			['..', 'subject.json'],
			['printing-press', '../../subject.json'],
			['printing-press', 'frame.json'],
			['printing-press', '.hidden.png']
		])
			expect(await get(frame, file)).toMatchObject({ status: 404 });
	});

	it('refuses a subject the app does not serve', async () => {
		for (const subject of ['..', 'nope', '.git', 'Western-Civ', 'western-civ/..'])
			expect(await get('printing-press', 'scene.svg', subject)).toMatchObject({ status: 404 });
	});

	it('serves a frame image with a locked-down policy', async () => {
		const res = (await get('printing-press', 'scene.svg')) as Response;
		expect(res.headers.get('content-type')).toBe('image/svg+xml');
		expect(res.headers.get('content-security-policy')).toContain("default-src 'none'");
		expect(res.headers.get('x-content-type-options')).toBe('nosniff');
	});
});

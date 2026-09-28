import { mkdir, readFile, writeFile } from 'node:fs/promises';
import { join } from 'node:path';

/** A small, valid grown frame, for the grow tests: what a well-behaved model writes. */
export const grownFrame = (id: string, sort: number, palette = 'parchment') => ({
	'frame.json': JSON.stringify(
		{
			id,
			position: { label: `AD ${sort}`, sort },
			scene: {
				headline: 'We nailed',
				accent: 'THESES.',
				palette,
				illustration: 'scene.svg',
				metadata: ['WITTENBERG']
			},
			citations: [
				{
					kind: 'web',
					title: 'A source',
					url: 'https://example.org/source',
					accessed: '2026-09-27',
					key: true
				}
			]
		},
		null,
		'\t'
	),
	'reading.md': 'A reading.\n\n## A section\n\nMore of it.\n',
	'scene.svg':
		'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" fill="none" stroke="currentColor"><g stroke-width="0.6" opacity="0.55"><path pathLength="1" d="M10 272 L390 272"/></g><g><path pathLength="1" d="M70 272 L70 22"/></g></svg>\n'
});

/** Write a frame directory into a subject directory. */
export async function writeFrame(dir: string, id: string, files: Record<string, string>) {
	await mkdir(join(dir, 'frames', id), { recursive: true });
	for (const [name, text] of Object.entries(files))
		await writeFile(join(dir, 'frames', id, name), text);
}

/** Edit a JSON file in place. */
export async function editJson<T>(path: string, edit: (value: T) => void) {
	const value = JSON.parse(await readFile(path, 'utf8')) as T;
	edit(value);
	await writeFile(path, `${JSON.stringify(value, null, '\t')}\n`);
}

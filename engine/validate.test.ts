import { join } from 'node:path';
import { beforeAll, describe, expect, it } from 'vitest';
import { buildSubject, loadSubject, SubjectError } from './load';
import type { RawSubject } from './validate';
import { validate } from './validate';

// A small subject built in memory, so each test breaks exactly one thing.
const raw = (): RawSubject => {
	const frame = (id: string, sort: number, palette = 'night') => ({
		frame: {
			id,
			position: { label: String(sort), sort },
			scene: { headline: 'We did', accent: `${id.toUpperCase()}.`, palette, metadata: [] },
			sources: [{ title: 'A source', url: 'https://example.org/' }]
		},
		reading: `Reading for ${id}.`,
		svgs: {},
		media: [] as string[]
	});
	return {
		manifest: {
			title: 'Test',
			palettes: {
				night: {
					scheme: 'dark',
					background: '#000',
					ink: '#fff',
					muted: '#888',
					accent: '#fc0',
					line: '#fc0'
				}
			}
		},
		spine: {
			segments: [{ id: 's', title: 'S', labelKind: 'date', frames: ['a', 'b'] }]
		},
		trails: {
			t: {
				id: 't',
				title: 'T',
				anchor: 'a',
				spine: { segments: [{ id: 'ts', title: 'TS', labelKind: 'date', frames: ['c'] }] }
			}
		},
		frames: { a: frame('a', 1), b: frame('b', 2), c: frame('c', 3) }
	};
};

// Deliberately loose: tests reach into the raw JSON to break it.
// eslint-disable-next-line @typescript-eslint/no-explicit-any
type Loose = any;

describe('validate', () => {
	it('accepts a well-formed subject', () => {
		expect(validate(raw())).toEqual([]);
	});

	it('takes an asOf month or day on a time-sensitive frame, and nothing else', () => {
		const r = raw();
		(r.frames.a.frame as Loose).asOf = '2026-09';
		(r.frames.b.frame as Loose).asOf = '2026-09-27';
		expect(validate(r)).toEqual([]);
		for (const bad of ['2026', 'September 2026', '2026-13', '2026-09-32', 20260927]) {
			(r.frames.c.frame as Loose).asOf = bad;
			expect(validate(r)).toEqual(['frames/c: asOf must be YYYY-MM or YYYY-MM-DD']);
		}
	});

	it('fails an accent word another frame already has, whatever its case or stop', () => {
		const r = raw();
		(r.frames.b.frame as Loose).scene.accent = 'a!';
		expect(validate(r)).toEqual(['frames/b: accent "A" is already frames/a\'s']);
	});

	it('fails a frame with no sources', () => {
		const r = raw();
		(r.frames.b.frame as Loose).sources = [];
		expect(validate(r)).toEqual([
			'frames/b: sources are required — every frame carries at least one'
		]);
	});

	it('fails a frame whose sources key is missing', () => {
		const r = raw();
		delete (r.frames.b.frame as Loose).sources;
		expect(validate(r).join('\n')).toMatch(/frames\/b: sources are required/);
	});

	it('fails a trail anchored to an unknown frame', () => {
		const r = raw();
		(r.trails.t as Loose).anchor = 'nowhere';
		expect(validate(r)).toEqual([
			'trails/t.json: unknown anchor "nowhere" (must be a main-spine frame)'
		]);
	});

	it('fails a trail anchored to a frame that is not on the main spine', () => {
		const r = raw();
		(r.trails.t as Loose).anchor = 'c';
		expect(validate(r).join('\n')).toMatch(/unknown anchor "c"/);
	});

	it('fails a date segment whose frames are out of order', () => {
		const r = raw();
		(r.spine as Loose).segments[0].frames = ['b', 'a'];
		expect(validate(r)).toEqual(['spine.json segment 0: frame "a" (1) is out of order after 2']);
	});

	it('does not order a segment that is not dates', () => {
		const r = raw();
		(r.spine as Loose).segments[0] = {
			id: 's',
			title: 'S',
			labelKind: 'technology',
			frames: ['b', 'a']
		};
		delete (r.frames.a.frame as Loose).position.sort;
		expect(validate(r)).toEqual([]);
	});

	it('requires a sort key in a date segment', () => {
		const r = raw();
		delete (r.frames.a.frame as Loose).position.sort;
		expect(validate(r)).toEqual([
			'spine.json segment 0: frame "a" needs a numeric position.sort in a date segment'
		]);
	});

	it('fails an unknown frame, a frame on two spines and an orphan', () => {
		const r = raw();
		(r.spine as Loose).segments[0].frames = ['a', 'c', 'ghost'];
		expect(validate(r)).toEqual([
			'spine.json segment 0: unknown frame "ghost"',
			'trails/t.json segment 0: frame "c" is already on spine.json',
			'frames/b: is not on any spine'
		]);
	});

	it('fails an unknown palette and an unknown label kind', () => {
		const r = raw();
		(r.frames.a.frame as Loose).scene.palette = 'neon';
		(r.spine as Loose).segments[0].labelKind = 'mood';
		expect(validate(r)).toEqual([
			'spine.json segment 0: labelKind must be one of date, category, technology',
			'frames/a: unknown palette "neon"'
		]);
	});

	it('fails a palette counterpart that is unknown or of the same scheme', () => {
		const r = raw();
		const palettes = (r.manifest as Loose).palettes;
		palettes.day = { ...palettes.night, scheme: 'light', counterpart: 'night' };
		palettes.dusk = { ...palettes.night, counterpart: 'night' };
		palettes.night.counterpart = 'noon';
		expect(validate(r)).toEqual([
			'subject.json palette night: unknown counterpart "noon"',
			'subject.json palette dusk: counterpart "night" must be of the other scheme'
		]);
	});

	it('fails an illustration that is missing or scripted', () => {
		const r = raw();
		(r.frames.a.frame as Loose).scene.illustration = 'gone.svg';
		(r.frames.b.frame as Loose).scene.illustration = 'x.svg';
		r.frames.b.svgs['x.svg'] = '<svg onload="alert(1)"></svg>';
		expect(validate(r)).toEqual([
			'frames/a: illustration "gone.svg" is not in the directory',
			'frames/b: illustration: <svg> attribute onload is not allowed'
		]);
	});

	// Bypasses of the first regex found in pre-ship review (korg 3362), now
	// regression tests for the allowlist that replaced it (korg 3365).
	it.each([
		['a slash before the handler', '<svg><g/onclick=alert(1)></g></svg>', 'a malformed attribute'],
		[
			'an entity-spelled scheme',
			'<svg><a href="java&#x73;cript:alert(1)"><path/></a></svg>',
			'<a> is not allowed'
		],
		['a style element', '<svg><style>body{display:none}</style></svg>', '<style> is not allowed'],
		['an embed', '<svg><embed src="https://example.org/x"/></svg>', '<embed> is not allowed'],
		['a use reference', '<svg><use href="https://example.org/x.svg#a"/></svg>', '<use> is not']
	])('refuses %s', (_, svg, problem) => {
		const r = raw();
		(r.frames.a.frame as Loose).scene.illustration = 'x.svg';
		r.frames.a.svgs['x.svg'] = svg;
		const errors = validate(r);
		expect(errors.length).toBeGreaterThan(0);
		expect(errors.join('\n')).toContain(problem);
		expect(errors.every((e) => e.startsWith('frames/a: illustration: '))).toBe(true);
	});

	it('fails a missing reading and a non-http source url', () => {
		const r = raw();
		r.frames.a.reading = null;
		(r.frames.b.frame as Loose).sources[0].url = 'javascript:alert(1)';
		expect(validate(r)).toEqual([
			'frames/a: reading.md is missing or empty',
			'frames/b: source 0 url must be http(s)'
		]);
	});

	const pd = {
		kind: 'media',
		title: 'A map',
		url: 'https://commons.wikimedia.org/wiki/File:Map.png',
		accessed: '2026-09-26',
		licence: 'Public domain',
		file: 'map.png'
	};

	it('accepts a credited image and names each citation problem', () => {
		const r = raw();
		r.frames.a.reading = 'See ![a map](map.png).';
		r.frames.a.media = ['map.png'];
		(r.frames.a.frame as Loose).citations = [pd];
		expect(validate(r)).toEqual([]);

		(r.frames.b.frame as Loose).citations = [
			{
				kind: 'wikipedia',
				title: 'X',
				url: 'https://en.wikipedia.org/wiki/X',
				accessed: '2026-09-26'
			}
		];
		expect(validate(r)).toEqual([
			'frames/b citation 0: a Wikipedia citation needs a permanent revision url (oldid=)'
		]);
	});

	it('fails an image without a media citation, or not in the directory', () => {
		const r = raw();
		r.frames.a.reading = '![one](map.png) ![two](https://example.org/x.png) ![three](../b/x.png)';
		r.frames.a.media = ['map.png'];
		expect(validate(r)).toEqual([
			'frames/a: image "map.png" needs a media citation with a licence',
			'frames/a: image "https://example.org/x.png" must be an image file in the frame\'s directory',
			'frames/a: image "../b/x.png" must be an image file in the frame\'s directory'
		]);
	});

	it('fails a media citation for a file that is not there, or without a licence', () => {
		const r = raw();
		r.frames.a.reading = '![a map](map.png)';
		r.frames.a.media = ['map.png'];
		const { licence, ...unlicensed } = pd;
		void licence;
		(r.frames.a.frame as Loose).citations = [unlicensed, { ...pd, file: 'gone.png' }];
		expect(validate(r)).toEqual([
			'frames/a citation 0: a media citation needs a licence',
			'frames/a citation 1: credits "gone.png", which is not in the directory',
			'frames/a: image "map.png" needs a media citation with a licence'
		]);
	});

	it('refuses to build an invalid subject, listing every problem', () => {
		const r = raw();
		(r.frames.a.frame as Loose).sources = [];
		r.frames.b.reading = '';
		expect(() => buildSubject('test', r)).toThrow(SubjectError);
		try {
			buildSubject('test', r);
		} catch (e) {
			expect((e as SubjectError).problems).toHaveLength(2);
		}
	});
});

describe('the western-civ subject', () => {
	const dir = join(import.meta.dirname, '..', 'subjects', 'western-civ');
	let subject: Awaited<ReturnType<typeof loadSubject>>;
	beforeAll(async () => {
		subject = await loadSubject(dir);
	});

	// Validity, illustrations and citations for every subject: subjects.test.ts.
	it('spans both palettes, opens on a myth and carries its trails', () => {
		const palettes = new Set(Object.values(subject.frames).map((f) => f.scene.palette));
		expect([...palettes].sort()).toEqual(['night', 'parchment']);
		expect(subject.spine.segments[0].labelKind).toBe('category');
		expect(subject.trails.map((t) => `${t.id}@${t.anchor}`).sort()).toEqual([
			'measure@eratosthenes',
			'printing@printing-press'
		]);
	});

	it('renders reading markdown', () => {
		expect(subject.frames.writing.readingHtml).toContain('<strong>cuneiform</strong>');
	});

	it('serves reading images from the frame, crediting the chart', () => {
		const html = subject.frames['printing-press'].readingHtml;
		expect(html).toContain('<img src="/media/printing-press/printing-shop-1499.jpg"');
		// Public domain: no caption. The chart's MIT licence asks for one.
		expect(html).toMatch(
			/<span class="figure"><img src="\/media\/printing-press\/book-output.svg"[^>]*><span class="credit">kloom contributors \/ MIT<\/span>/
		);
	});
});

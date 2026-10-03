import { join } from 'node:path';
import { beforeAll, describe, expect, it } from 'vitest';
import { buildSubject, loadSubject, SubjectError } from './load';
import type { RawSubject } from './validate';
import { SUBTITLE_MAX, TOPIC_MAX, validate } from './validate';

// Every frame's one key source.
const source = {
	kind: 'web',
	key: true,
	title: 'A source',
	url: 'https://example.org/',
	accessed: '2026-09-26'
};

// A small subject built in memory, so each test breaks exactly one thing.
const raw = (): RawSubject => {
	const frame = (id: string, sort: number, palette = 'night') => ({
		frame: {
			id,
			topic: `Topic ${id}`,
			position: { label: String(sort), sort },
			scene: { headline: 'We did', accent: `${id.toUpperCase()}.`, palette, metadata: [] },
			citations: [{ ...source }]
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

	it('takes an optional subtitle: a short line of plain text', () => {
		const r = raw();
		(r.manifest as Loose).subtitle = 'creating the objects around us';
		expect(validate(r)).toEqual([]);
		(r.manifest as Loose).subtitle = 'x'.repeat(SUBTITLE_MAX);
		expect(validate(r)).toEqual([]);
		(r.manifest as Loose).subtitle = 'x'.repeat(SUBTITLE_MAX + 1);
		expect(validate(r)).toEqual([
			`subject.json: subtitle is ${SUBTITLE_MAX + 1} characters; at most ${SUBTITLE_MAX}`
		]);
		for (const bad of ['', '  ', 7, ['a']]) {
			(r.manifest as Loose).subtitle = bad;
			expect(validate(r)).toEqual(['subject.json: subtitle, when given, is a line of text']);
		}
	});

	it('takes an optional dedication: a name with a line above it and, optionally, one below', () => {
		const r = raw();
		const scene = (r.frames.b.frame as Loose).scene;
		scene.dedication = {
			kicker: 'Dedicated to',
			name: 'Colonel A. B. Smith, USA',
			note: 'Retired'
		};
		expect(validate(r)).toEqual([]);
		delete scene.dedication.note;
		expect(validate(r)).toEqual([]);
		for (const bad of [
			'Smith',
			{ name: 'Smith' },
			{ kicker: 'To', name: '  ' },
			{ kicker: 'To', name: 'Smith', note: 3 }
		]) {
			scene.dedication = bad;
			expect(validate(r)).toEqual([
				'frames/b: scene.dedication needs a kicker and a name, and a note only as text'
			]);
		}
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

	it('requires a plain topic: short, not a sentence, not the accent, not another frame’s', () => {
		const r = raw();
		const a = r.frames.a.frame as Loose;
		delete a.topic;
		expect(validate(r)).toEqual(['frames/a: topic is required']);
		a.topic = '  ';
		expect(validate(r)).toEqual(['frames/a: topic is required']);
		a.topic = 'x'.repeat(TOPIC_MAX + 1);
		expect(validate(r)).toEqual([
			`frames/a: topic is ${TOPIC_MAX + 1} characters; at most ${TOPIC_MAX}`
		]);
		a.topic = 'x'.repeat(TOPIC_MAX);
		expect(validate(r)).toEqual([]);
		a.topic = 'It played along.';
		expect(validate(r)).toEqual(['frames/a: topic is a title: no closing "." or "!"']);
		a.scene.accent = 'ALONG.';
		a.topic = 'Played ALONG';
		expect(validate(r)).toEqual([
			'frames/a: topic must say what the frame is about, not repeat its accent "ALONG"'
		]);
		// The accent's word in plain case is the thing's name, and is fine.
		a.topic = 'Playing along';
		expect(validate(r)).toEqual([]);
		a.topic = ' Topic b ';
		expect(validate(r)).toEqual(['frames/b: topic "Topic b" is already frames/a\'s']);
	});

	it('fails an accent word another frame already has, whatever its case or stop', () => {
		const r = raw();
		(r.frames.b.frame as Loose).scene.accent = 'a!';
		expect(validate(r)).toEqual(['frames/b: accent "A" is already frames/a\'s']);
	});

	it('takes connections to a frame anywhere, each with a why', () => {
		const r = raw();
		(r.frames.a.frame as Loose).connections = [
			{ to: 'other/some-frame', why: 'Because.' },
			{ to: 'test/b', why: 'Within the subject too.' }
		];
		expect(validate(r)).toEqual([]);
	});

	it('fails a connection without a why, to no frame ref, or named twice', () => {
		const r = raw();
		(r.frames.a.frame as Loose).connections = [
			{ to: 'other/x', why: ' ' },
			{ to: 'just-a-frame', why: 'Why.' },
			{ to: 'other/x', why: 'Again.' }
		];
		(r.frames.b.frame as Loose).connections = { to: 'other/x' };
		expect(validate(r)).toEqual([
			'frames/a connection 0: why is required: a sentence on what connects them',
			'frames/a connection 1: to must be "<subject>/<frame>"',
			'frames/a connection 2: other/x is already a connection of this frame',
			'frames/b: connections must be a list'
		]);
	});

	it('fails a mark on a name the registry lacks, or a kloom: link that is not a mark', () => {
		const r = raw();
		r.frames.a.reading = '[Turing](kloom:e/alan-turing) and [Hopper](kloom:e/grace-hopper).';
		r.frames.b.reading = 'See [there](kloom:ai/turing-machine).';
		const names = new Set(['alan-turing']);
		expect(validate(r, { names })).toEqual([
			'frames/a: "grace-hopper" is not in the name registry',
			'frames/b: "kloom:ai/turing-machine" is not a name mark (kloom:e/<name id>)'
		]);
		// Without a registry, a mark is checked for its form only.
		expect(validate(r)).toEqual([
			'frames/b: "kloom:ai/turing-machine" is not a name mark (kloom:e/<name id>)'
		]);
	});

	it('warns, and does not fail, when a name is marked twice in a frame', () => {
		const r = raw();
		r.frames.a.reading = '[Turing](kloom:e/alan-turing), then [Turing](kloom:e/alan-turing).';
		const warnings: string[] = [];
		expect(validate(r, { names: new Set(['alan-turing']), warnings })).toEqual([]);
		expect(warnings).toEqual([
			'frames/a: "alan-turing" is marked again; only its first mention needs it'
		]);
	});

	it('fails a frame that flags no key source', () => {
		const r = raw();
		delete (r.frames.b.frame as Loose).citations[0].key;
		(r.frames.c.frame as Loose).citations = [];
		expect(validate(r)).toEqual([
			'frames/b: every frame flags at least one key-source citation ("key": true)',
			'frames/c: every frame flags at least one key-source citation ("key": true)'
		]);
	});

	it('fails a frame with no citations, or a hand-kept sources list', () => {
		const r = raw();
		delete (r.frames.b.frame as Loose).citations;
		(r.frames.c.frame as Loose).sources = [{ title: 'A source', url: 'https://example.org/' }];
		expect(validate(r)).toEqual([
			'frames/b: citations are required, as a list',
			'frames/c: sources is not written any more: flag the key citations with "key": true'
		]);
	});

	it("lists the key citations as the frame's sources", () => {
		const r = raw();
		(r.frames.a.frame as Loose).citations.push({ ...source, key: false, url: 'https://x.test/' });
		expect(buildSubject('test', r).frames.a.sources).toEqual([
			{ title: 'A source', url: 'https://example.org/' }
		]);
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

	it('takes a section palette the subject defines, and fails one it does not (korg 3495)', () => {
		const r = raw();
		(r.spine as Loose).segments[0].palette = 'night';
		expect(validate(r)).toEqual([]);
		(r.spine as Loose).segments[0].palette = 'neon';
		expect(validate(r)).toEqual(['spine.json segment 0: unknown palette "neon"']);
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
		(r.frames.b.frame as Loose).citations[0].url = 'javascript:alert(1)';
		expect(validate(r)).toEqual([
			'frames/a: reading.md is missing or empty',
			'frames/b citation 0: url must be http(s)'
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
		(r.frames.a.frame as Loose).citations.push(pd);
		expect(validate(r)).toEqual([]);

		(r.frames.b.frame as Loose).citations.push({
			kind: 'wikipedia',
			title: 'X',
			url: 'https://en.wikipedia.org/wiki/X',
			accessed: '2026-09-26'
		});
		expect(validate(r)).toEqual([
			'frames/b citation 1: a Wikipedia citation needs a permanent revision url (oldid=)'
		]);
	});

	it('takes a source seen only in another work when the frame cites that work with a link', () => {
		const r = raw();
		const seen = {
			kind: 'book',
			title: 'History of the Royal Society',
			citedIn: 'Farr, “A Source” (1980), note 6'
		};
		(r.frames.a.frame as Loose).citations.push(seen);
		expect(validate(r)).toEqual([]);

		(r.frames.b.frame as Loose).citations.push({ ...seen, citedIn: 'Farr, “Not Here” (1980)' });
		expect(validate(r)).toEqual([
			'frames/b citation 1: has no url or doi, so its citedIn must name, by title, a work this frame cites with one'
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

	it('fails an SVG image the illustration sanitiser refuses: it is inlined', () => {
		const r = raw();
		r.frames.a.reading = '![a chart](chart.svg)';
		r.frames.a.media = ['chart.svg'];
		r.frames.a.svgs = { 'chart.svg': '<svg xmlns="http://www.w3.org/2000/svg"><rect/></svg>' };
		(r.frames.a.frame as Loose).citations.push({ ...pd, file: 'chart.svg', licence: 'MIT' });
		expect(validate(r)).toEqual([]);
		r.frames.a.svgs['chart.svg'] = '<svg><script>alert(1)</script><path style="x"/></svg>';
		expect(validate(r)).toEqual([
			'frames/a: image "chart.svg": <script> is not allowed in an illustration',
			'frames/a: image "chart.svg": <path> attribute style is not allowed'
		]);
	});

	it('fails a media citation for a file that is not there, or without a licence', () => {
		const r = raw();
		r.frames.a.reading = '![a map](map.png)';
		r.frames.a.media = ['map.png'];
		const { licence, ...unlicensed } = pd;
		void licence;
		(r.frames.a.frame as Loose).citations.push(unlicensed, { ...pd, file: 'gone.png' });
		expect(validate(r)).toEqual([
			'frames/a citation 1: a media citation needs a licence',
			'frames/a citation 2: credits "gone.png", which is not in the directory',
			'frames/a: image "map.png" needs a media citation with a licence'
		]);
	});

	it('refuses to build an invalid subject, listing every problem', () => {
		const r = raw();
		(r.frames.a.frame as Loose).citations = [];
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

	it('renders reading markdown, with its names marked (§Connections)', () => {
		expect(subject.frames.writing.readingHtml).toMatch(
			/<strong><button type="button" class="name" data-name="cuneiform"[^>]*>cuneiform<\/button><\/strong>/
		);
	});

	it('serves reading images from the frame, and inlines the chart, crediting it', () => {
		const html = subject.frames['printing-press'].readingHtml;
		expect(html).toContain('<img src="/media/printing-press/printing-shop-1499.jpg"');
		// Public domain: no caption. The chart's MIT licence asks for one, with
		// its data's DOI (sprint 033). The chart is inlined, named by the
		// reading's alt text, its own ids prefixed.
		expect(html).toMatch(
			/<span class="figure chart" role="img" aria-label="[^"]+"><svg [^>]*aria-hidden="true"[^>]*>.*<\/svg><\/span><span class="credit">kloom contributors \/ MIT \/ data doi:10\.1017\/S0022050709000837<\/span>/s
		);
		expect(html).toContain('<title id="printing-press-book-output-t">');
		expect(html).not.toContain('<img src="/media/printing-press/book-output.svg"');
	});

	it('derives the Sources list from the key citations', () => {
		expect(subject.frames['printing-press'].sources[0]).toEqual({
			title: 'Printing press — Wikipedia',
			url: expect.stringContaining('oldid=')
		});
	});
});

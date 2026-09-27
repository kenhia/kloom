import { join } from 'node:path';
import { beforeAll, describe, expect, it } from 'vitest';
import { buildSubject, loadSubject, readSubject, SubjectError } from './load';
import type { RawSubject } from './validate';
import { validate } from './validate';

// A small subject built in memory, so each test breaks exactly one thing.
const raw = (): RawSubject => {
	const frame = (id: string, sort: number, palette = 'night') => ({
		frame: {
			id,
			position: { label: String(sort), sort },
			scene: { headline: 'We did', accent: 'THINGS.', palette, metadata: [] },
			sources: [{ title: 'A source', url: 'https://example.org/' }]
		},
		reading: `Reading for ${id}.`,
		svgs: {}
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

	it('fails an illustration that is missing or scripted', () => {
		const r = raw();
		(r.frames.a.frame as Loose).scene.illustration = 'gone.svg';
		(r.frames.b.frame as Loose).scene.illustration = 'x.svg';
		r.frames.b.svgs['x.svg'] = '<svg onload="alert(1)"></svg>';
		expect(validate(r)).toEqual([
			'frames/a: illustration "gone.svg" is not in the directory',
			'frames/b: illustration contains script, styles, links or event handlers'
		]);
	});

	// Bypasses of the first regex found in pre-ship review (korg 3362).
	it.each([
		['a slash before the handler', '<svg><g/onclick=alert(1)></g></svg>'],
		['an entity-spelled scheme', '<svg><a href="java&#x73;cript:alert(1)"><path/></a></svg>'],
		['a style element', '<svg><style>body{display:none}</style></svg>'],
		['an embed', '<svg><embed src="https://example.org/x"></svg>'],
		['a use reference', '<svg><use href="https://example.org/x.svg#a"/></svg>']
	])('trips on %s', (_, svg) => {
		const r = raw();
		(r.frames.a.frame as Loose).scene.illustration = 'x.svg';
		r.frames.a.svgs['x.svg'] = svg;
		expect(validate(r)).toEqual([
			'frames/a: illustration contains script, styles, links or event handlers'
		]);
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

	it('is valid', async () => {
		expect(validate(await readSubject(dir))).toEqual([]);
	});

	it('spans both palettes and carries one trail', () => {
		const palettes = new Set(Object.values(subject.frames).map((f) => f.scene.palette));
		expect([...palettes].sort()).toEqual(['night', 'parchment']);
		expect(subject.trails.map((t) => `${t.id}@${t.anchor}`)).toEqual(['printing@printing-press']);
	});

	it('renders reading markdown and inlines illustrations', () => {
		expect(subject.frames.writing.readingHtml).toContain('<strong>cuneiform</strong>');
		expect(subject.frames.writing.svg).toMatch(/^<svg/);
		expect(subject.frames['gutenberg-bible'].svg).toBeNull();
	});
});

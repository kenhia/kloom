import { describe, expect, it } from 'vitest';
import { libraryStats, pages, readingStats, subjectStats, wordCount } from './stats';
import type { RawFrame, RawSubject } from './validate';

const frame = (reading: string, file: object = {}): RawFrame => ({
	frame: {
		scene: { headline: 'Many words in a headline', accent: 'Accent', metadata: ['a b c'] },
		citations: [],
		...file
	},
	reading,
	svgs: {},
	media: []
});

describe('wordCount', () => {
	it('counts the words a reader sees, not the markup', () => {
		expect(wordCount('<p>One <em>two</em> three.</p>\n<p>Four</p>')).toBe(4);
		// A word split by inline markup is still one word; blocks never run together.
		expect(wordCount('<p><em>cathode</em>s</p><p>end</p>')).toBe(2);
		expect(wordCount('<ul><li>a</li><li>b</li></ul>')).toBe(2);
	});

	it('leaves out attributes, drawings and bare punctuation', () => {
		expect(wordCount('<p><img src="x.png" alt="a long alt text"> — seen</p>')).toBe(1);
		expect(wordCount('<p>Before <svg><text>label words</text></svg> after</p>')).toBe(2);
		expect(wordCount('<p>Tom &amp; Jerry&#39;s</p>')).toBe(2);
	});
});

describe('readingStats', () => {
	it('counts tables, captions and headings, and tells pictures from charts', () => {
		const md = [
			'Opening words here.',
			'',
			'## A heading',
			'',
			'![A picture of a loom](loom.jpg)',
			'',
			'_The caption under it._',
			'',
			'![A chart of growth](growth.svg)',
			'',
			'| Year | Event |',
			'| ---- | ----- |',
			'| 1897 | Electron |'
		].join('\n');
		expect(readingStats(md)).toEqual({ words: 13, images: 1, charts: 1, tables: 1 });
	});

	it('counts a marked name by its words', () => {
		expect(readingStats('[J. J. Thomson](kloom:e/j-j-thomson) measured it.').words).toBe(5);
	});
});

describe('subjectStats', () => {
	const raw: RawSubject = {
		manifest: { title: 'A Subject' },
		spine: { segments: [{ frames: ['a', 'b'] }, { frames: ['c'] }] },
		trails: { t: { spine: { segments: [{ frames: ['d'] }] } } },
		frames: {
			a: frame('one two three', {
				citations: [{ kind: 'book', title: 'A very long book title indeed', key: true }],
				connections: [{ to: 'other/x', why: 'because of many reasons' }]
			}),
			b: frame('four five'),
			// A citation-heavy frame: its bibliography is not its words.
			c: frame('six', {
				citations: Array.from({ length: 12 }, (_, i) => ({
					kind: 'web',
					title: `Source number ${i} with many words in it`
				}))
			}),
			d: frame('seven eight nine ten'),
			// On no spine: not a frame the reader can reach.
			stray: frame('never counted at all')
		}
	};

	it('counts frames on the main spine and trails, and only narrative words', () => {
		expect(subjectStats('s', raw)).toEqual({
			id: 's',
			title: 'A Subject',
			frames: 4,
			trailFrames: 1,
			trails: 1,
			words: 10,
			pages: 0,
			images: 0,
			charts: 0,
			tables: 0,
			citations: 13,
			connections: 1
		});
	});

	it('sums a library, with pages of the whole', () => {
		const s = subjectStats('s', raw);
		const big = { ...s, id: 't', words: 550 };
		const lib = libraryStats([s, big], 7);
		expect(lib).toMatchObject({ frames: 8, trails: 2, words: 560, pages: 2, names: 7 });
		expect(lib.wordsPerPage).toBe(275);
	});
});

describe('pages', () => {
	it('is words over 275, rounded', () => {
		expect([pages(0), pages(137), pages(138), pages(231_000)]).toEqual([0, 0, 1, 840]);
	});
});

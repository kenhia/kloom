import { describe, expect, it } from 'vitest';
import { citationProblems } from '../citation';
import { pinWikipedia, wikipediaArticle, type Fetch } from './wikipedia';

const api = (pages: unknown, status = 200): { fetcher: Fetch; urls: string[] } => {
	const urls: string[] = [];
	return {
		urls,
		fetcher: async (url) => {
			urls.push(url);
			return new Response(JSON.stringify({ query: { pages } }), { status });
		}
	};
};

describe('Wikipedia links', () => {
	it('knows an article URL, on any language or mobile site', () => {
		expect(wikipediaArticle('https://en.wikipedia.org/wiki/Printing_press')).toEqual({
			host: 'en.wikipedia.org',
			title: 'Printing press'
		});
		expect(wikipediaArticle('https://de.m.wikipedia.org/wiki/Buchdruck')?.host).toBe(
			'de.wikipedia.org'
		);
		expect(
			wikipediaArticle('https://en.wikipedia.org/w/index.php?title=Johannes_Gutenberg&oldid=1')
				?.title
		).toBe('Johannes Gutenberg');
		expect(wikipediaArticle('https://en.wikipedia.org.evil.test/wiki/X')).toBeNull();
		expect(wikipediaArticle('https://example.org/wiki/X')).toBeNull();
	});

	it('pins an article to its current revision, as a valid citation', async () => {
		const { fetcher, urls } = api({
			'1': {
				title: "Gutenberg's press",
				revisions: [{ revid: 1376640142, timestamp: '2026-09-25T10:00:00Z' }]
			}
		});
		const c = await pinWikipedia(
			'https://en.wikipedia.org/wiki/Gutenberg%27s_press',
			'2026-09-27',
			fetcher
		);
		expect(urls[0]).toContain('https://en.wikipedia.org/w/api.php?');
		expect(urls[0]).toContain('titles=Gutenberg%27s+press');
		expect(c).toMatchObject({
			kind: 'wikipedia',
			title: "Gutenberg's press",
			url: "https://en.wikipedia.org/w/index.php?title=Gutenberg's_press&oldid=1376640142",
			accessed: '2026-09-27',
			published: '2026-09-25'
		});
		expect(citationProblems(c)).toEqual([]);
	});

	it('refuses a missing article or a failed lookup rather than keep it unpinned', async () => {
		const url = 'https://en.wikipedia.org/wiki/Nope';
		await expect(
			pinWikipedia(url, '2026-09-27', api({ '-1': { title: 'Nope', missing: '' } }).fetcher)
		).rejects.toThrow('no Wikipedia article');
		await expect(pinWikipedia(url, '2026-09-27', api({}, 503).fetcher)).rejects.toThrow('503');
	});
});

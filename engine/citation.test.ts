import { describe, expect, it } from 'vitest';
import {
	bibliography,
	captionCredit,
	chicago,
	chicagoAuthors,
	chicagoDate,
	chicagoText,
	citationProblems,
	needsCaption,
	type Citation
} from './citation';

const wikipedia: Citation = {
	kind: 'wikipedia',
	title: 'Printing press',
	url: 'https://en.wikipedia.org/w/index.php?title=Printing_press&oldid=1376640142',
	accessed: '2026-09-26',
	authors: [{ name: 'Wikipedia contributors' }],
	container: 'Wikipedia, The Free Encyclopedia',
	publisher: 'Wikimedia Foundation',
	published: '2026-09-25'
};

const web: Citation = {
	kind: 'web',
	title: 'Apollo 11 Mission Overview',
	url: 'https://www.nasa.gov/mission/apollo-11/',
	accessed: '2026-09-26',
	container: 'NASA',
	published: '2019-07-15'
};

const book: Citation = {
	kind: 'book',
	title: 'The Printing Press as an Agent of Change',
	url: 'https://archive.org/details/printingpressasa0000eise',
	accessed: '2026-09-26',
	authors: [{ family: 'Eisenstein', given: 'Elizabeth L.' }],
	place: 'Cambridge',
	publisher: 'Cambridge University Press',
	published: '1979'
};

const article: Citation = {
	kind: 'article',
	title: 'Molecular Structure of Nucleic Acids: A Structure for Deoxyribose Nucleic Acid',
	url: 'https://doi.org/10.1038/171737a0',
	accessed: '2026-09-26',
	authors: [
		{ family: 'Watson', given: 'J. D.' },
		{ family: 'Crick', given: 'F. H. C.' }
	],
	container: 'Nature',
	volume: '171',
	issue: '4356',
	pages: '737–38',
	published: '1953-04-25'
};

const image: Citation = {
	kind: 'media',
	title: 'Modern Loose Reed Power Loom',
	url: 'https://commons.wikimedia.org/wiki/File:Modern_Loose_Reed_Power_Loom-marsden.png',
	accessed: '2026-09-26',
	authors: [{ family: 'Marsden', given: 'Richard' }],
	published: '1895',
	container: 'Wikimedia Commons',
	licence: 'Public domain',
	file: 'loom.svg'
};

describe('chicago', () => {
	it('formats a Wikipedia article with its revision link', () => {
		expect(chicagoText(wikipedia)).toBe(
			'Wikipedia contributors. “Printing press.” Wikipedia, The Free Encyclopedia. ' +
				'Wikimedia Foundation. Last modified September 25, 2026. Accessed September 26, 2026. ' +
				'https://en.wikipedia.org/w/index.php?title=Printing_press&oldid=1376640142.'
		);
	});

	it('formats an ordinary web page', () => {
		expect(chicagoText(web)).toBe(
			'“Apollo 11 Mission Overview.” NASA. July 15, 2019. Accessed September 26, 2026. ' +
				'https://www.nasa.gov/mission/apollo-11/.'
		);
	});

	it('formats a book, title in italics', () => {
		expect(chicagoText(book)).toBe(
			'Eisenstein, Elizabeth L. The Printing Press as an Agent of Change. ' +
				'Cambridge: Cambridge University Press, 1979. Accessed September 26, 2026. ' +
				'https://archive.org/details/printingpressasa0000eise.'
		);
		expect(chicago(book).filter((p) => p.italic)).toEqual([
			{ text: 'The Printing Press as an Agent of Change', italic: true }
		]);
	});

	it('formats a journal article, journal in italics', () => {
		expect(chicagoText(article)).toBe(
			'Watson, J. D., and F. H. C. Crick. “Molecular Structure of Nucleic Acids: A Structure ' +
				'for Deoxyribose Nucleic Acid.” Nature 171, no. 4356 (April 25, 1953): 737–38. ' +
				'Accessed September 26, 2026. https://doi.org/10.1038/171737a0.'
		);
		expect(chicago(article).filter((p) => p.italic)).toEqual([{ text: 'Nature', italic: true }]);
	});

	it('formats a public-domain image with its licence', () => {
		expect(chicagoText(image)).toBe(
			'Marsden, Richard. Modern Loose Reed Power Loom. 1895. Wikimedia Commons. ' +
				'Public domain. Accessed September 26, 2026. ' +
				'https://commons.wikimedia.org/wiki/File:Modern_Loose_Reed_Power_Loom-marsden.png.'
		);
	});

	it('marks only the URL as a link, and never emits markup', () => {
		const parts = chicago(wikipedia);
		expect(parts.filter((p) => p.href).map((p) => p.href)).toEqual([wikipedia.url]);
		const hostile = { ...web, title: '<img src=x onerror=alert(1)>' };
		// Text runs only: the renderer escapes them like any other text.
		expect(chicago(hostile).every((p) => typeof p.text === 'string')).toBe(true);
		expect(chicagoText(hostile)).toContain('“<img src=x onerror=alert(1)>.”');
	});

	it('turns quotation marks inside a quoted title to single ones', () => {
		expect(chicagoText({ ...web, title: 'Charting the “Rise of the West”' })).toContain(
			'“Charting the ‘Rise of the West.’”'
		);
	});

	it('does not double a title’s own punctuation', () => {
		expect(chicagoText({ ...web, title: 'Who Built the Pantheon?' })).toContain(
			'“Who Built the Pantheon?” NASA.'
		);
	});
});

describe('chicago parts', () => {
	it('orders a bibliography alphabetically', () => {
		expect(bibliography([wikipedia, web, image, book]).map((c) => c.kind)).toEqual([
			'web',
			'book',
			'media',
			'wikipedia'
		]);
	});

	it.each([
		['2026-09-26', 'September 26, 2026'],
		['1969-07', 'July 1969'],
		['1895', '1895']
	])('dates %s as %s', (iso, out) => expect(chicagoDate(iso)).toBe(out));

	it('inverts only the first author', () => {
		const a = { family: 'Buringh', given: 'Eltjo' };
		const b = { family: 'van Zanden', given: 'Jan Luiten' };
		const c = { family: 'Smith', given: 'Ann' };
		expect(chicagoAuthors([a])).toBe('Buringh, Eltjo');
		expect(chicagoAuthors([a, b])).toBe('Buringh, Eltjo, and Jan Luiten van Zanden');
		expect(chicagoAuthors([a, b, c])).toBe('Buringh, Eltjo, Jan Luiten van Zanden, and Ann Smith');
		expect(chicagoAuthors([{ name: 'NASA' }])).toBe('NASA');
	});

	it('asks for a caption credit only where the licence needs one', () => {
		expect(needsCaption('Public domain')).toBe(false);
		expect(needsCaption('CC0 1.0')).toBe(false);
		expect(needsCaption('CC BY-SA 4.0')).toBe(true);
		expect(captionCredit({ ...image, licence: 'CC BY 4.0' })).toBe('Richard Marsden / CC BY 4.0');
	});
});

describe('citationProblems', () => {
	it('accepts every example', () => {
		for (const c of [wikipedia, web, book, article, image]) expect(citationProblems(c)).toEqual([]);
	});

	it('requires title, url and accessed date', () => {
		expect(citationProblems({ kind: 'web' })).toEqual([
			'title is required',
			'url is required',
			'accessed date is required, as YYYY-MM-DD'
		]);
	});

	it('requires a revision link for any Wikipedia url', () => {
		const url = 'https://en.wikipedia.org/wiki/Printing_press';
		const want = ['a Wikipedia citation needs a permanent revision url (oldid=)'];
		expect(citationProblems({ ...wikipedia, url })).toEqual(want);
		// Filed as an ordinary web page, it is still Wikipedia.
		expect(citationProblems({ ...web, url })).toEqual(want);
	});

	it('requires a licence and a file on media', () => {
		const { licence, file, ...bare } = image;
		void licence;
		void file;
		expect(citationProblems(bare)).toEqual([
			'a media citation needs a licence',
			'a media citation needs the file it credits'
		]);
	});

	it('rejects a bad kind, url, dates and authors', () => {
		expect(
			citationProblems({
				...web,
				kind: 'tweet',
				url: 'javascript:alert(1)',
				accessed: 'yesterday',
				published: '15 July 2019',
				authors: ['NASA']
			})
		).toEqual([
			'kind must be one of web, wikipedia, book, article, media',
			'url must be http(s)',
			'accessed date is required, as YYYY-MM-DD',
			'published must be YYYY, YYYY-MM or YYYY-MM-DD',
			'authors must each have a family name or a name'
		]);
	});
});

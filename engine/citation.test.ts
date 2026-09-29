import { describe, expect, it } from 'vitest';
import {
	bibliography,
	captionCredit,
	chicago,
	chicagoAuthors,
	chicagoDate,
	chicagoText,
	citationProblems,
	keySource,
	keySources,
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
	doi: '10.1038/171737a0',
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

const chapter: Citation = {
	kind: 'chapter',
	title: 'Artificial Intelligence: A General Survey',
	url: 'https://www.chilton-computing.org.uk/inf/literature/reports/lighthill_report/p001.htm',
	accessed: '2026-09-27',
	authors: [{ family: 'Lighthill', given: 'James' }],
	container: 'Artificial Intelligence: A Paper Symposium',
	editors: [
		{ family: 'Smith', given: 'Ann' },
		{ family: 'Jones', given: 'Bo' }
	],
	pages: '1–21',
	place: 'London',
	publisher: 'Science Research Council',
	published: '1973'
};

const report: Citation = {
	kind: 'report',
	title: 'Mark I Perceptron Operators’ Manual (Project PARA)',
	url: 'https://apps.dtic.mil/sti/tr/pdf/AD0236965.pdf',
	accessed: '2026-09-27',
	authors: [
		{ family: 'Hay', given: 'John C.' },
		{ family: 'Murray', given: 'Albert E.' }
	],
	number: 'Report VG-1196-G-5',
	place: 'Buffalo, NY',
	publisher: 'Cornell Aeronautical Laboratory',
	published: '1960-02-15'
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

	it("names an edited book's editors after its title", () => {
		const edited: Citation = {
			kind: 'book',
			title: 'Feynman Lectures on Computation',
			url: 'https://openlibrary.org/works/OL514615W',
			accessed: '2026-09-28',
			authors: [{ family: 'Feynman', given: 'Richard P.' }],
			editors: [
				{ family: 'Hey', given: 'Anthony J. G.' },
				{ family: 'Allen', given: 'Robin W.' }
			],
			place: 'Reading, MA',
			publisher: 'Addison-Wesley',
			published: '1996'
		};
		expect(chicagoText(edited)).toBe(
			'Feynman, Richard P. Feynman Lectures on Computation. ' +
				'Edited by Anthony J. G. Hey and Robin W. Allen. ' +
				'Reading, MA: Addison-Wesley, 1996. Accessed September 28, 2026. ' +
				'https://openlibrary.org/works/OL514615W.'
		);
	});

	it('formats a journal article, journal in italics', () => {
		expect(chicagoText(article)).toBe(
			'Watson, J. D., and F. H. C. Crick. “Molecular Structure of Nucleic Acids: A Structure ' +
				'for Deoxyribose Nucleic Acid.” Nature 171, no. 4356 (April 25, 1953): 737–38. ' +
				'Accessed September 26, 2026. https://doi.org/10.1038/171737a0.'
		);
		expect(chicago(article).filter((p) => p.italic)).toEqual([{ text: 'Nature', italic: true }]);
	});

	it('formats a chapter in a proceedings or symposium volume, volume in italics', () => {
		expect(chicagoText(chapter)).toBe(
			'Lighthill, James. “Artificial Intelligence: A General Survey.” In Artificial ' +
				'Intelligence: A Paper Symposium, edited by Ann Smith and Bo Jones, 1–21. London: ' +
				'Science Research Council, 1973. Accessed September 27, 2026. ' +
				'https://www.chilton-computing.org.uk/inf/literature/reports/lighthill_report/p001.htm.'
		);
		expect(chicago(chapter).filter((p) => p.italic)).toEqual([
			{ text: 'Artificial Intelligence: A Paper Symposium', italic: true }
		]);
		const { editors, pages, ...plain } = chapter;
		void editors;
		void pages;
		expect(chicagoText(plain)).toContain(
			'In Artificial Intelligence: A Paper Symposium. London: Science Research Council, 1973.'
		);
	});

	it('formats a report, title in italics, with its number', () => {
		expect(chicagoText(report)).toBe(
			'Hay, John C., and Albert E. Murray. Mark I Perceptron Operators’ Manual (Project PARA). ' +
				'Report VG-1196-G-5. Buffalo, NY: Cornell Aeronautical Laboratory, February 15, 1960. ' +
				'Accessed September 27, 2026. https://apps.dtic.mil/sti/tr/pdf/AD0236965.pdf.'
		);
		expect(chicago(report).filter((p) => p.italic).length).toBe(1);
	});

	it('links a DOI at doi.org, in place of the url', () => {
		const withBoth = { ...article, url: 'https://www.nature.com/articles/171737a0' };
		expect(chicago(withBoth).filter((p) => p.href)).toEqual([
			{ text: 'https://doi.org/10.1038/171737a0', href: 'https://doi.org/10.1038/171737a0' }
		]);
	});

	it('dates an approximate date "ca."', () => {
		expect(chicagoDate('1951', true)).toBe('ca. 1951');
		expect(chicagoText({ ...image, circa: true })).toContain('Power Loom. ca. 1895. Wikimedia');
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
		// A suffix after the given names stays there inverted, and goes last in natural order.
		const edwards = { family: 'Edwards', given: 'Mark U., Jr.' };
		expect(chicagoAuthors([edwards, a])).toBe('Edwards, Mark U., Jr., and Eltjo Buringh');
		expect(chicagoAuthors([a, edwards])).toBe('Buringh, Eltjo, and Mark U. Edwards Jr.');
	});

	it('ends a long author list with et al., without doubling the full stop', () => {
		const radford = { family: 'Radford', given: 'Alec' };
		expect(chicagoAuthors([radford], true)).toBe('Radford, Alec, et al.');
		expect(chicagoAuthors([radford, { family: 'Wu', given: 'Jeffrey' }], true)).toBe(
			'Radford, Alec, Jeffrey Wu, et al.'
		);
		const text = chicagoText({
			kind: 'article',
			title: 'Language Models are Unsupervised Multitask Learners',
			url: 'https://example.org/gpt2.pdf',
			accessed: '2026-09-27',
			authors: [radford],
			etAl: true
		});
		expect(text.startsWith('Radford, Alec, et al. “Language')).toBe(true);
	});

	it('asks for a caption credit only where the licence needs one', () => {
		expect(needsCaption('Public domain')).toBe(false);
		expect(needsCaption('CC0 1.0')).toBe(false);
		expect(needsCaption('CC BY-SA 4.0')).toBe(true);
		expect(captionCredit({ ...image, licence: 'CC BY 4.0' })).toBe('Richard Marsden / CC BY 4.0');
		expect(captionCredit({ ...image, licence: 'CC BY 4.0', etAl: true })).toBe(
			'Richard Marsden et al. / CC BY 4.0'
		);
	});
});

describe('key sources', () => {
	it('names a key citation the way the Sources list always read', () => {
		expect(keySource(wikipedia)).toEqual({
			title: 'Printing press — Wikipedia',
			url: wikipedia.url
		});
		expect(keySource(article)).toEqual({
			title:
				'J. D. Watson and F. H. C. Crick, Molecular Structure of Nucleic Acids: A Structure for Deoxyribose Nucleic Acid',
			url: 'https://doi.org/10.1038/171737a0',
			note: 'Nature, April 25, 1953'
		});
		expect(keySource({ ...book, note: 'The standard history' })).toEqual({
			title: 'Elizabeth L. Eisenstein, The Printing Press as an Agent of Change',
			url: book.url,
			note: 'Cambridge University Press, 1979. The standard history'
		});
		expect(
			keySource({ ...web, title: 'A page', container: undefined, published: undefined })
		).toEqual({ title: 'A page', url: web.url });
	});

	it('shortens more than three authors, or a list that runs on, to et al.', () => {
		const four = ['A', 'B', 'C', 'D'].map((family) => ({ family }));
		expect(keySource({ ...web, authors: four }).title).toBe('A et al., Apollo 11 Mission Overview');
		expect(keySource({ ...web, authors: four.slice(0, 3) }).title).toBe(
			'A, B, and C, Apollo 11 Mission Overview'
		);
		expect(keySource({ ...web, authors: four.slice(0, 1), etAl: true }).title).toBe(
			'A et al., Apollo 11 Mission Overview'
		);
	});

	it('lists only the key citations, in the order they are written', () => {
		const list = keySources([web, { ...book, key: true }, image, { ...wikipedia, key: true }]);
		expect(list.map((s) => s.url)).toEqual([book.url, wikipedia.url]);
	});
});

describe('citationProblems', () => {
	it('accepts every example', () => {
		for (const c of [wikipedia, web, book, article, chapter, report, image])
			expect(citationProblems(c)).toEqual([]);
	});

	it('requires title, url or doi, and accessed date', () => {
		expect(citationProblems({ kind: 'web' })).toEqual([
			'title is required',
			'url is required, unless there is a doi',
			'accessed date is required, as YYYY-MM-DD'
		]);
	});

	it('takes a bare DOI, and wants a doi.org link written as one', () => {
		expect(citationProblems({ ...article, doi: 'https://doi.org/10.1038/171737a0' })).toEqual([
			'doi must be a bare DOI, like 10.1109/5.58323'
		]);
		expect(citationProblems({ ...web, url: 'https://doi.org/10.1038/171737a0' })).toEqual([
			'a doi.org url goes in doi, as the bare DOI'
		]);
	});

	it('takes circa only with a date, and key only as a flag', () => {
		expect(citationProblems({ ...web, circa: true, key: true })).toEqual([]);
		expect(citationProblems({ ...web, published: undefined, circa: true, key: 'yes' })).toEqual([
			'circa must be true or false, with a published date',
			'key must be true or false'
		]);
	});

	it('needs a chapter’s volume, and well-formed editors, number and note', () => {
		expect(
			citationProblems({ ...chapter, container: undefined, editors: ['X'], number: 5, note: '' })
		).toEqual([
			'editors must each have a family name or a name',
			'number must be text',
			'note must be text',
			'a chapter needs its container: the volume or proceedings it appears in'
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

	it('takes etAl only as a flag on a listed author', () => {
		expect(citationProblems({ ...web, authors: [{ name: 'A' }], etAl: true })).toEqual([]);
		for (const bad of [{ etAl: 'yes', authors: [{ name: 'A' }] }, { etAl: true }])
			expect(citationProblems({ ...web, authors: undefined, ...bad })).toEqual([
				'etAl must be true or false, with at least one author listed'
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
			'kind must be one of web, wikipedia, book, article, chapter, report, media',
			'url must be http(s)',
			'accessed date is required, as YYYY-MM-DD',
			'published must be YYYY, YYYY-MM or YYYY-MM-DD',
			'authors must each have a family name or a name'
		]);
	});
});

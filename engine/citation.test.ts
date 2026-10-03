import { describe, expect, it } from 'vitest';
import {
	bibliography,
	captionCredit,
	chicago,
	chicagoAuthors,
	chicagoDate,
	chicagoText,
	citationProblems,
	citedInProblems,
	keySource,
	keySources,
	legalText,
	needsCaption,
	publishedYear,
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
			'url is required, unless there is a doi, or a citedIn naming a work cited with one',
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
			'a media citation needs a `licence`',
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
			'kind must be one of web, wikipedia, book, article, chapter, report, media, letter, encyclopedia, diary, case, statute',
			'url must be http(s)',
			'accessed date is required, as YYYY-MM-DD',
			'published must be YYYY, YYYY-MM or YYYY-MM-DD, a shorter year (888), or a year BC (1550 BC)',
			'authors must each have a family name or a name'
		]);
	});
});

describe('the schema for older, translated and second-hand sources (sprint 027)', () => {
	const galen: Citation = {
		kind: 'book',
		title: 'On the Natural Faculties',
		url: 'https://www.gutenberg.org/ebooks/43771',
		accessed: '2026-10-01',
		authors: [{ name: 'Galen' }],
		translators: [{ family: 'Brock', given: 'Arthur John' }],
		edition: 'Loeb Classical Library ed.',
		place: 'London',
		publisher: 'William Heinemann',
		published: '1916'
	};

	it('dates a work before AD 1000, and BC, with or without circa', () => {
		expect(chicagoDate('888')).toBe('888');
		expect(chicagoDate('1550 BC', true)).toBe('ca. 1550 BC');
		const papyrus = { ...image, published: '1550 BC', circa: true };
		expect(citationProblems(papyrus)).toEqual([]);
		expect(chicagoText(papyrus)).toContain('Power Loom. ca. 1550 BC. Wikimedia');
		expect(citationProblems({ ...image, published: '888' })).toEqual([]);
		for (const bad of ['0', '0 BC', '1550 B.C.', '1550BC', '-1550', '1550 BC-03'])
			expect(citationProblems({ ...image, published: bad })).toEqual([
				'published must be YYYY, YYYY-MM or YYYY-MM-DD, a shorter year (888), or a year BC (1550 BC)'
			]);
	});

	it('sorts a published date as a signed year', () => {
		expect(publishedYear('1550 BC')).toBe(-1550);
		expect(publishedYear('888')).toBe(888);
		expect(publishedYear('2017-03-04')).toBe(2017);
		expect(publishedYear('nonsense')).toBeUndefined();
	});

	it('names translators and an edition after the title', () => {
		expect(chicagoText(galen)).toBe(
			'Galen. On the Natural Faculties. Translated by Arthur John Brock. ' +
				'Loeb Classical Library ed. London: William Heinemann, 1916. ' +
				'Accessed October 1, 2026. https://www.gutenberg.org/ebooks/43771.'
		);
		const { translators, edition, ...rest } = galen;
		void translators;
		void edition;
		expect(
			chicagoText({ ...rest, editors: [{ family: 'Kühn', given: 'C. G.' }], translators })
		).toContain('Edited by C. G. Kühn. Translated by Arthur John Brock. London');
	});

	it('names the engraver of a plate', () => {
		expect(chicagoText({ ...image, engravers: [{ family: 'Basire', given: 'James' }] })).toContain(
			'Modern Loose Reed Power Loom. Engraved by James Basire. 1895.'
		);
	});

	it('gives a journal volume its own year when it came out later', () => {
		expect(chicagoText({ ...article, volumeYear: '1952' })).toContain(
			'Nature 171, no. 4356 (1952; published April 25, 1953): 737–38.'
		);
		expect(citationProblems({ ...article, volumeYear: '1954' })).toEqual([
			'volumeYear is the year the volume is for, so no later than published'
		]);
		expect(citationProblems({ ...web, volumeYear: '2016' })).toEqual([
			'volumeYear is for an article, with a published date'
		]);
	});

	it('says what language a source is in, and which Wikipedia', () => {
		const de: Citation = {
			...wikipedia,
			title: 'Buchdruck',
			url: 'https://de.wikipedia.org/w/index.php?title=Buchdruck&oldid=250000000',
			language: 'de'
		};
		expect(citationProblems(de)).toEqual([]);
		expect(chicagoText(de)).toContain('Last modified September 25, 2026. In German. Accessed');
		expect(keySource(de).title).toBe('Buchdruck — German Wikipedia');
		expect(citationProblems({ ...de, language: undefined })).toEqual([
			'a de.wikipedia.org article needs "language": "de"'
		]);
		expect(citationProblems({ ...de, language: 'German' })).toEqual([
			'language must be a language code, like "de" or "grc"'
		]);
	});

	it('formats a letter, to its recipients', () => {
		const letter: Citation = {
			kind: 'letter',
			title: 'Account of Flint Weapons Discovered at Hoxne in Suffolk',
			url: 'https://archive.org/details/archaeologiaormi13soci/page/204',
			accessed: '2026-10-01',
			authors: [{ family: 'Frere', given: 'John' }],
			recipients: [{ name: 'the Society of Antiquaries of London' }],
			written: '1797-06-22',
			container: 'Archaeologia',
			volume: '13',
			pages: '204–5',
			place: 'London',
			publisher: 'Society of Antiquaries of London',
			published: '1800'
		};
		expect(citationProblems(letter)).toEqual([]);
		expect(chicagoText(letter)).toBe(
			'Frere, John. “Account of Flint Weapons Discovered at Hoxne in Suffolk.” Letter to ' +
				'the Society of Antiquaries of London, June 22, 1797. In Archaeologia, vol. 13, 204–5. ' +
				'London: Society of Antiquaries of London, 1800. Accessed October 1, 2026. ' +
				'https://archive.org/details/archaeologiaormi13soci/page/204.'
		);
		expect(citationProblems({ ...letter, recipients: undefined, written: 'June' })).toEqual([
			'written must be YYYY, YYYY-MM or YYYY-MM-DD, a shorter year (888), or a year BC (1550 BC)',
			'a letter needs its recipients'
		]);
	});

	it('formats an encyclopedia entry, in its encyclopedia', () => {
		const entry: Citation = {
			kind: 'encyclopedia',
			title: 'Galen',
			url: 'https://plato.stanford.edu/archives/sum2020/entries/galen/',
			accessed: '2026-10-01',
			authors: [{ family: 'Hankinson', given: 'R. J.' }],
			container: 'Stanford Encyclopedia of Philosophy',
			editors: [{ family: 'Zalta', given: 'Edward N.' }],
			edition: 'Summer 2020 ed.',
			publisher: 'Stanford University',
			published: '2020'
		};
		expect(citationProblems(entry)).toEqual([]);
		expect(chicagoText(entry)).toBe(
			'Hankinson, R. J. “Galen.” In Stanford Encyclopedia of Philosophy, edited by ' +
				'Edward N. Zalta, Summer 2020 ed. Stanford University, 2020. Accessed October 1, 2026. ' +
				'https://plato.stanford.edu/archives/sum2020/entries/galen/.'
		);
		expect(keySource(entry).note).toBe('Stanford Encyclopedia of Philosophy, 2020');
		expect(citationProblems({ ...entry, container: undefined })).toEqual([
			'an encyclopedia entry needs its container: the encyclopedia'
		]);
	});

	it('puts a chapter of a numbered report in its report', () => {
		expect(chicagoText({ ...chapter, number: 'Report 1234' })).toContain(
			'In Artificial Intelligence: A Paper Symposium, Report 1234, edited by Ann Smith and Bo Jones, 1–21.'
		);
	});

	it('says where a source was seen when it was not read: cited in a work, or in part', () => {
		const seen = { ...article, citedIn: 'Gleick, Genius, p. 247' };
		expect(chicagoText(seen)).toContain('737–38. Cited in Gleick, Genius, p. 247. Accessed');
		expect(chicagoText({ ...article, read: 'abstract' })).toContain(
			'737–38. Read in its abstract. Accessed'
		);
		expect(chicagoText({ ...article, read: 'first-page' })).toContain(
			'737–38. Read in its first page. Accessed'
		);
		expect(chicagoText({ ...article, read: 'excerpt' })).toContain(
			'737–38. Read in an excerpt. Accessed'
		);
		expect(keySource({ ...seen, read: 'abstract', note: 'The method' }).note).toBe(
			'Nature, April 25, 1953. Cited in Gleick, Genius, p. 247. Read in its abstract. The method'
		);
		expect(citationProblems({ ...article, citedIn: '', read: 'yes' })).toEqual([
			'citedIn must be text',
			'read must be one of abstract, first-page, excerpt, record'
		]);
		expect(citationProblems({ ...article, abstractOnly: true })).toEqual([
			'abstractOnly is now read: "abstract"'
		]);
	});

	describe('a source seen only in another work (sprint 029)', () => {
		const farr: Citation = {
			kind: 'article',
			title: 'The First Human Blood Transfusion',
			doi: '10.1017/S0025727300040138',
			accessed: '2026-10-01',
			authors: [{ family: 'Farr', given: 'A. D.' }],
			container: 'Medical History',
			published: '1980'
		};
		const sprat: Citation = {
			kind: 'book',
			title: 'The History of the Royal-Society of London',
			authors: [{ family: 'Sprat', given: 'Thomas' }],
			place: 'London',
			publisher: 'J. Martyn and J. Allestry',
			published: '1667',
			pages: '317',
			citedIn: 'Farr, “The First Human Blood Transfusion” (1980), note 6'
		};

		it('stands without a url, doi or access date when its citedIn has one', () => {
			expect(citationProblems(sprat)).toEqual([]);
			expect(citedInProblems([farr, sprat])).toEqual([]);
			expect(chicago(sprat).some((p) => p.href)).toBe(false);
			expect(chicagoText(sprat)).toBe(
				'Sprat, Thomas. The History of the Royal-Society of London. London: J. Martyn and ' +
					'J. Allestry, 1667. Cited in Farr, “The First Human Blood Transfusion” (1980), note 6.'
			);
		});

		it('checks the chain: the citing work is cited in the frame, with a link', () => {
			expect(citedInProblems([sprat])).toEqual([
				{
					index: 0,
					problem:
						'has no url or doi, so its citedIn must name, by title, a work this frame cites with one'
				}
			]);
			const unlinked = { ...farr, doi: undefined, citedIn: 'Somewhere else' };
			expect(citedInProblems([unlinked, sprat]).map((p) => p.index)).toEqual([0, 1]);
		});

		it('is never a key source, and needs a citedIn', () => {
			expect(citationProblems({ ...sprat, key: true })).toEqual([
				'a key source links what was read: one seen only in another work cannot be key'
			]);
			expect(citationProblems({ ...sprat, citedIn: undefined })).toEqual([
				'url is required, unless there is a doi, or a citedIn naming a work cited with one',
				'accessed date is required, as YYYY-MM-DD'
			]);
		});

		it('still needs an access date when it has a link', () => {
			expect(citationProblems({ ...farr, accessed: undefined })).toEqual([
				'accessed date is required, as YYYY-MM-DD'
			]);
		});
	});

	it('sets a diary entry in its edition', () => {
		const entry: Citation = {
			kind: 'diary',
			title: 'The Diary of Samuel Pepys',
			authors: [{ family: 'Pepys', given: 'Samuel' }],
			written: '1666-11-14',
			editors: [{ family: 'Wheatley', given: 'Henry B.' }],
			place: 'London',
			publisher: 'George Bell & Sons',
			published: '1893',
			url: 'https://www.pepysdiary.com/diary/1666/11/14/',
			accessed: '2026-10-01'
		};
		expect(citationProblems(entry)).toEqual([]);
		expect(chicagoText(entry)).toBe(
			'Pepys, Samuel. Diary entry, November 14, 1666, in The Diary of Samuel Pepys, edited by ' +
				'Henry B. Wheatley. London: George Bell & Sons, 1893. Accessed October 1, 2026. ' +
				'https://www.pepysdiary.com/diary/1666/11/14/.'
		);
		expect(chicago(entry).find((p) => p.italic)?.text).toBe('The Diary of Samuel Pepys');
		expect(keySource(entry)).toEqual({
			title: 'Samuel Pepys, The Diary of Samuel Pepys',
			url: entry.url,
			note: 'entry of November 14, 1666, George Bell & Sons, 1893'
		});
		expect(citationProblems({ ...entry, written: undefined })).toEqual([
			'a diary entry needs the date it was written'
		]);
	});

	it('cites a copy where no official one exists, and says whose', () => {
		const handbook: Citation = {
			...report,
			url: 'https://www.generalstaff.org/BBOW/handbook.pdf',
			mirror: true
		};
		expect(citationProblems(handbook)).toEqual([]);
		expect(chicagoText(handbook)).toMatch(
			/https:\/\/www\.generalstaff\.org\/BBOW\/handbook\.pdf \(copy at generalstaff\.org\)\.$/
		);
		expect(keySource({ ...handbook, key: true }).note).toContain('Copy at generalstaff.org');
		expect(citationProblems({ ...handbook, doi: '10.1000/x' })).toEqual([
			'mirror is for a url copying a work with no official copy, so not with a doi'
		]);
		expect(citationProblems({ ...handbook, mirror: 'yes' })).toEqual([
			'mirror must be true or false'
		]);
	});

	it('takes a JSTOR article by its stable url, with no DOI to check', () => {
		const jstor = { ...article, doi: undefined, url: 'https://www.jstor.org/stable/2265097' };
		expect(citationProblems(jstor)).toEqual([]);
		expect(
			citationProblems({ ...jstor, url: 'https://www.jstor.org/stable/pdf/2265097.pdf' })
		).toEqual(['a JSTOR article is cited by its stable url, https://www.jstor.org/stable/N']);
		expect(citationProblems({ ...jstor, url: 'https://daily.jstor.org/a-story/' })).toEqual([]);
	});

	it('takes an en.wikipedia.org file page as a media source, without a revision', () => {
		const file = {
			...image,
			url: 'https://en.wikipedia.org/wiki/File:Rhind_Mathematical_Papyrus.jpg'
		};
		expect(citationProblems(file)).toEqual([]);
		expect(citationProblems({ ...web, url: file.url })).toEqual([
			'a Wikipedia citation needs a permanent revision url (oldid=)'
		]);
	});

	it('checks the roles like the authors', () => {
		expect(citationProblems({ ...book, translators: ['X'], engravers: [{}], edition: 2 })).toEqual([
			'translators must each have a family name or a name',
			'engravers must each have a family name or a name',
			'edition must be text'
		]);
	});
});

describe('the forms from Keeping Watch (sprint 033)', () => {
	const frank: Citation = {
		kind: 'case',
		title: 'Frank v. South',
		reporter: { volume: '175', name: 'Ky.', page: '416' },
		published: '1917-05-04',
		container: 'Caselaw Access Project',
		publisher: 'Harvard Law School Library',
		url: 'https://static.case.law/ky/175/html/0416-01.html',
		accessed: '2026-10-01'
	};
	const nursesAct: Citation = {
		kind: 'statute',
		title: 'Army-Navy Nurses Act of 1947',
		publicLaw: '80-36',
		code: { volume: '61', name: 'Stat.', page: '41' },
		published: '1947-04-16',
		container: 'United States Statutes at Large',
		url: 'https://www.govinfo.gov/content/pkg/STATUTE-61/pdf/STATUTE-61-Pg41.pdf',
		accessed: '2026-10-01'
	};

	it('sets a case in legal form, its name in italics', () => {
		expect(chicagoText(frank)).toBe(
			'Frank v. South, 175 Ky. 416 (1917). Caselaw Access Project. Harvard Law School Library. ' +
				'Accessed October 1, 2026. https://static.case.law/ky/175/html/0416-01.html.'
		);
		expect(chicago(frank)[0]).toEqual({ text: 'Frank v. South', italic: true });
		expect(
			legalText({
				...frank,
				title: 'Sparger v. Worley Hospital, Inc.',
				reporter: { volume: '547', name: 'S.W.2d', page: '582' },
				court: 'Tex.',
				published: '1977-03-02'
			})
		).toBe('Sparger v. Worley Hospital, Inc., 547 S.W.2d 582 (Tex. 1977)');
		// A neutral citation carries its own year and court.
		expect(
			legalText({
				...frank,
				reporter: undefined,
				title: 'Getty Images v Stability AI',
				neutral: '[2025] EWHC 2863 (Ch)',
				published: '2025-11-04'
			})
		).toBe('Getty Images v Stability AI [2025] EWHC 2863 (Ch)');
	});

	it('sets a statute in legal form, its year where the cite does not already say it', () => {
		expect(chicagoText(nursesAct)).toBe(
			'Army-Navy Nurses Act of 1947, Pub. L. No. 80-36, 61 Stat. 41. United States Statutes at Large. ' +
				'Accessed October 1, 2026. https://www.govinfo.gov/content/pkg/STATUTE-61/pdf/STATUTE-61-Pg41.pdf.'
		);
		expect(chicago(nursesAct)[0]).toEqual({ text: 'Army-Navy Nurses Act of 1947' });
		const act = { ...nursesAct, title: 'An Act to grant military rank', publicLaw: '78-238' };
		expect(legalText(act)).toBe(
			'An Act to grant military rank, Pub. L. No. 78-238, 61 Stat. 41 (1947)'
		);
		// A session law's chapter and section come before its volume; a code's section after it.
		expect(
			legalText({
				...act,
				publicLaw: undefined,
				chapter: '192',
				section: '§ 19',
				code: { volume: '31', name: 'Stat.', page: '753' },
				published: '1901-02-02'
			})
		).toBe('An Act to grant military rank, ch. 192, § 19, 31 Stat. 753 (1901)');
		expect(
			legalText({
				...act,
				title: 'Condition of Participation: Nursing Services',
				publicLaw: undefined,
				code: { volume: '42', name: 'C.F.R.' },
				section: '§ 482.23',
				published: undefined
			})
		).toBe('Condition of Participation: Nursing Services, 42 C.F.R. § 482.23');
		expect(
			legalText({
				...act,
				title: 'House Bill 2697',
				publicLaw: undefined,
				code: { volume: '2023', name: 'Or. Laws' },
				chapter: '507',
				published: '2023-08-01'
			})
		).toBe('House Bill 2697, 2023 Or. Laws ch. 507');
	});

	it('lists a case or a statute under Sources by its legal form', () => {
		expect(keySource({ ...frank, key: true, note: 'The opinion' })).toEqual({
			title: 'Frank v. South, 175 Ky. 416 (1917)',
			url: 'https://static.case.law/ky/175/html/0416-01.html',
			note: 'Caselaw Access Project. The opinion'
		});
	});

	it('checks a case and a statute have what their legal form needs', () => {
		expect(citationProblems(frank)).toEqual([]);
		expect(citationProblems(nursesAct)).toEqual([]);
		expect(
			citationProblems({
				...frank,
				reporter: { volume: '175', name: 'Ky.' },
				published: undefined,
				authors: [{ name: 'Court of Appeals of Kentucky' }],
				publicLaw: '80-36'
			})
		).toEqual([
			'publicLaw is for a statute',
			'reporter needs its volume, name and first page as text: {"volume": "175", "name": "Ky.", "page": "416"}',
			'a case needs the date it was decided, in published',
			'a case names no authors: a case is named by its parties and its court goes in court, a law by its own name'
		]);
		expect(citationProblems({ ...frank, neutral: '[1917] KY 1' })).toEqual([
			'a case needs its reporter or its neutral citation, one of the two'
		]);
		expect(
			citationProblems({ ...nursesAct, publicLaw: '36', code: { volume: 61 }, court: 'Ky.' })
		).toEqual([
			'court is for a case',
			'publicLaw is the number as Congress and law: "80-36"',
			'code needs its name, and its volume and page as text when it has them'
		]);
		expect(citationProblems({ ...nursesAct, publicLaw: undefined, code: undefined })).toEqual([
			'a statute needs its publicLaw number, or the code or session laws it is in'
		]);
		expect(citationProblems({ ...web, reporter: frank.reporter, section: '§ 1' })).toEqual([
			'reporter is for a case or a statute',
			'section is for a case or a statute'
		]);
	});

	it('says when only a work’s catalogue record was read', () => {
		expect(chicagoText({ ...article, read: 'record' })).toContain(
			'737–38. Read in its catalog record only. Accessed'
		);
	});

	it('credits a chart’s data source by its DOI, apart from where the chart is', () => {
		const chart: Citation = {
			kind: 'media',
			title: 'Blood lead in US children',
			doi: '10.1289/EHP7932',
			accessed: '2026-09-30',
			authors: [{ name: 'kloom contributors' }],
			container: 'Chart drawn for kloom from Egan et al. (2021), Table 2',
			licence: 'MIT',
			file: 'blood-lead.svg'
		};
		expect(chicagoText(chart)).toBe(
			'kloom contributors. Blood lead in US children. Chart drawn for kloom from Egan et al. (2021), ' +
				'Table 2. MIT. Data: https://doi.org/10.1289/EHP7932. Accessed September 30, 2026.'
		);
		const both = { ...chart, url: 'https://example.org/chart-page' };
		expect(chicago(both).filter((p) => p.href)).toEqual([
			{ text: 'https://doi.org/10.1289/EHP7932', href: 'https://doi.org/10.1289/EHP7932' },
			{ text: 'https://example.org/chart-page', href: 'https://example.org/chart-page' }
		]);
		expect(captionCredit(chart)).toBe('kloom contributors / MIT / data doi:10.1289/EHP7932');
		expect(citationProblems(chart)).toEqual([]);
	});
});

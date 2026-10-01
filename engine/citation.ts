/**
 * Citations: stored as structured data, rendered in Chicago
 * notes-bibliography style (docs/design.md §Citations). Because the storage
 * is structured, another house style later is a new renderer here, not a
 * content rewrite.
 */

/**
 * What is being cited. `chapter` is a chapter or a paper in an edited volume,
 * a proceedings or a symposium; `report` a technical or institutional report
 * (sprint 008). `media` credits an image or chart a frame uses. `letter` is a
 * letter to its `recipients`, and `encyclopedia` an entry in one (sprint 027).
 */
export const CITATION_KINDS = [
	'web',
	'wikipedia',
	'book',
	'article',
	'chapter',
	'report',
	'media',
	'letter',
	'encyclopedia'
] as const;
export type CitationKind = (typeof CITATION_KINDS)[number];

/** A person (`family`, optionally `given`) or an organisation (`name`). */
export type Author = { family: string; given?: string } | { name: string };

export interface Citation {
	kind: CitationKind;
	title: string;
	/**
	 * Where it was read. Required unless there is a `doi`. For Wikipedia, a
	 * permanent revision link (`oldid=`): articles change.
	 */
	url?: string;
	/** The bare DOI (`10.1109/5.58323`); the entry links it at doi.org. */
	doi?: string;
	/**
	 * A key source: listed under Sources, the frame's short list, as well as
	 * in the bibliography. Every frame flags at least one (sprint 008).
	 */
	key?: boolean;
	/** A key source's remark in the Sources list: a page, why it matters. */
	note?: string;
	/** `YYYY-MM-DD`: when the page was read. */
	accessed: string;
	/** Authors, or for media the creator. Wikipedia: "Wikipedia contributors". */
	authors?: Author[];
	/**
	 * More authors than are listed: the entry ends the list with "et al.". A
	 * paper with dozens or hundreds of authors lists the first (Chicago lists
	 * up to ten, then the first seven).
	 */
	etAl?: boolean;
	/**
	 * The site, journal, book series or collection the item sits in; for a
	 * chapter, the volume or proceedings it appears in.
	 */
	container?: string;
	/** A chapter's editors (the volume's), or an edited book's. */
	editors?: Author[];
	/** Who translated it: "Translated by …" (sprint 027). */
	translators?: Author[];
	/** Who engraved a plate: "Engraved by …" (sprint 027). */
	engravers?: Author[];
	/** A letter's recipients: "Letter to …". Required on a letter. */
	recipients?: Author[];
	/** When a letter was written; `published` is when it was printed. Same forms as `published`. */
	written?: string;
	/** The edition, as it reads: "2nd ed.", "Loeb Classical Library ed.", "Summer 2020 ed.". */
	edition?: string;
	/** A report's number: "Technical Report 1234", "AD0236965"; for a chapter, its report's. */
	number?: string;
	publisher?: string;
	/** Place of publication, for books. */
	place?: string;
	/** Journal articles: where in the journal. */
	volume?: string;
	issue?: string;
	pages?: string;
	/**
	 * `YYYY`, `YYYY-MM` or `YYYY-MM-DD`; a shorter year without leading zeros
	 * (`888`); or a year BC (`1550 BC`). For Wikipedia, the revision's date.
	 */
	published?: string;
	/** The date is approximate: rendered "ca. 1951". Needs `published`. */
	circa?: boolean;
	/** An article's volume year, when the volume came out later: "(2016; published 2017)". */
	volumeYear?: string;
	/** The source's language, as a code (`de`, `grc`): "In German.". Required on a non-English Wikipedia. */
	language?: string;
	/** The work in whose references or quotation this one was seen, not read itself: "Cited in …". */
	citedIn?: string;
	/** Only its abstract was read: "Read in its abstract.". */
	abstractOnly?: boolean;
	/** Media only: "Public domain", "CC BY-SA 4.0", … */
	licence?: string;
	/** Media only: the file this credits, in the frame's directory. */
	file?: string;
}

/** One run of formatted text; the renderer decides the markup. */
export interface Part {
	text: string;
	italic?: boolean;
	/** Set on the URL run, so it can be a link. */
	href?: string;
}

const MONTHS = [
	'January',
	'February',
	'March',
	'April',
	'May',
	'June',
	'July',
	'August',
	'September',
	'October',
	'November',
	'December'
];

const DOI = /^10\.\d{4,9}\/\S+$/;
const DATE = /^(\d{4})(?:-(0[1-9]|1[0-2])(?:-(0[1-9]|[12]\d|3[01]))?)?$/;
/** A year AD shorter than four digits, or a year BC (sprint 027): no month or day, no leading zero. */
const EARLY = /^([1-9]\d{0,2})$|^([1-9]\d{0,5}) BC$/;
const PUBLISHED = 'YYYY, YYYY-MM or YYYY-MM-DD, a shorter year (888), or a year BC (1550 BC)';
const isPublished = (v: string) => DATE.test(v) || EARLY.test(v);
/** A language code: two or three letters, then any subtags ("de", "grc", "zh-Hant"). */
const LANGUAGE = /^[a-z]{2,3}(-[A-Za-z0-9]{2,8})*$/;

/**
 * A published date as a signed year, for sorting and comparing: "1550 BC" is
 * -1550, as a frame's `position.sort` writes it; "888" is 888.
 */
export function publishedYear(published: string): number | undefined {
	const d = DATE.exec(published);
	if (d) return Number(d[1]);
	const e = EARLY.exec(published);
	if (!e) return undefined;
	return e[1] ? Number(e[1]) : -Number(e[2]);
}

/** "2026-09-26" → "September 26, 2026"; "1895" stays "1895", as do "888" and "1550 BC"; approximate, "ca. 1895". */
export function chicagoDate(iso: string, circa = false): string {
	const m = DATE.exec(iso);
	if (!m) return circa && EARLY.test(iso) ? `ca. ${iso}` : iso;
	const [, y, mo, d] = m;
	const month = mo && MONTHS[Number(mo) - 1];
	const date = !month ? y : d ? `${month} ${Number(d)}, ${y}` : `${month} ${y}`;
	return circa ? `ca. ${date}` : date;
}

/** "de" → "German"; an unknown code stays as written. */
export function languageName(code: string): string {
	try {
		return new Intl.DisplayNames(['en'], { type: 'language' }).of(code) ?? code;
	} catch {
		return code;
	}
}

/** The language of a Wikipedia at `url`'s host ("de" for de.wikipedia.org), or undefined for another site. */
const wikipediaLanguage = (url: string) =>
	/^https?:\/\/([a-z][a-z-]*)\.(?:m\.)?wikipedia\.org\//.exec(url)?.[1];

/** The link an entry carries: the DOI at doi.org when there is one, else the url. */
export const citationHref = (c: Citation) => (c.doi ? `https://doi.org/${c.doi}` : c.url!);

const inverted = (a: Author) =>
	'name' in a ? a.name : a.given ? `${a.family}, ${a.given}` : a.family;
/** Natural order; a suffix written after the given names ("Mark U., Jr.") goes last. */
function natural(a: Author): string {
	if ('name' in a) return a.name;
	if (!a.given) return a.family;
	const [given, suffix] = a.given.split(/,\s*(?=(?:Jr|Sr)\.?$|[IVX]+$)/);
	return suffix ? `${given} ${a.family} ${suffix}` : `${a.given} ${a.family}`;
}

/** "A", "A and B", "A, B, and C". */
function series(names: string[]): string {
	if (names.length < 3) return names.join(' and ');
	return `${names.slice(0, -1).join(', ')}, and ${names[names.length - 1]}`;
}

/** Bibliography order: the first author inverted, the rest as written; `etAl` for more unlisted. */
export function chicagoAuthors(authors: Author[], etAl = false): string {
	const [first, ...rest] = authors;
	if (!first) return '';
	if (etAl) return [inverted(first), ...rest.map(natural), 'et al.'].join(', ');
	if (rest.length === 0) return inverted(first);
	const others = rest.map(natural);
	const last = others.pop()!;
	return `${[inverted(first), ...others].join(', ')}, and ${last}`;
}

/** End an element with a period unless it already ends in punctuation. */
const stop = (s: string) => (/[.?!]$/.test(s) ? s : `${s}.`);

/**
 * A title set in quotation marks: quotes inside it become single ones, and
 * the period goes inside them too ("…the ‘Rise of the West.’").
 */
function quoted(title: string): string {
	const inner = title.replace(/“/g, '‘').replace(/”/g, '’');
	const closing = /’$/.test(inner) ? '’' : '';
	return `“${stop(closing ? inner.slice(0, -1) : inner)}${closing}”`;
}

/**
 * A bibliography entry in Chicago notes-bibliography style (17th ed.):
 *
 * - web: Author. "Title." Site. Publisher, Date. Accessed Date. URL.
 * - wikipedia: Wikipedia contributors. "Title." Wikipedia. Wikimedia
 *   Foundation. Last modified Date. Accessed Date. URL.
 * - book: Author. _Title_. Edited by Editor. Place: Publisher, Year.
 *   Accessed Date. URL.
 * - article: Author. "Title." _Journal_ Volume, no. Issue (Date): Pages.
 *   Accessed Date. URL.
 * - chapter: Author. "Title." In _Volume_, edited by Editor, Pages. Place:
 *   Publisher, Year. Accessed Date. URL.
 * - report: Author. _Title_. Number. Series. Place: Publisher, Date.
 *   Accessed Date. URL.
 * - media: Creator. _Title_. Date. Collection. Licence. Accessed Date. URL.
 *
 * With a `doi`, the URL is the DOI at doi.org. An approximate date reads
 * "ca. 1951".
 */
export function chicago(c: Citation): Part[] {
	const parts: Part[] = [];
	const add = (text: string, italic = false) => parts.push(italic ? { text, italic } : { text });

	if (c.authors?.length) add(`${stop(chicagoAuthors(c.authors, c.etAl))} `);

	const italicTitle = c.kind === 'book' || c.kind === 'report' || c.kind === 'media';
	if (italicTitle) {
		add(c.title, true);
		add('. ');
	} else add(`${quoted(c.title)} `);

	// Who else made it, after the title: an edited book's editors first, as a title page reads.
	const by = (role: string, people?: Author[]) => {
		if (people?.length) add(`${role} ${stop(series(people.map(natural)))} `);
	};
	if (c.kind === 'book') by('Edited by', c.editors);
	by('Translated by', c.translators);
	by('Engraved by', c.engravers);
	const inVolume = c.kind === 'chapter' || c.kind === 'encyclopedia';
	if (c.edition && !inVolume) add(`${stop(c.edition)} `);

	const date = c.published ? chicagoDate(c.published, c.circa) : undefined;
	const imprint = () => {
		const where = [c.place, c.publisher].filter(Boolean).join(': ');
		const facts = [where, date].filter(Boolean).join(', ');
		if (facts) add(`${stop(facts)} `);
	};
	switch (c.kind) {
		case 'book':
			if (c.container) add(`${stop(c.container)} `);
			imprint();
			break;
		case 'letter': {
			const to = c.recipients?.length ? series(c.recipients.map(natural)) : '';
			const sent = c.written ? chicagoDate(c.written) : '';
			if (to) add(`${stop(`Letter to ${to}${sent ? `, ${sent}` : ''}`)} `);
			const rest = [c.volume && `vol. ${c.volume}`, c.pages].filter(Boolean);
			if (c.container) {
				add('In ');
				add(c.container, true);
				add(rest.length ? `, ${stop(rest.join(', '))} ` : '. ');
			}
			imprint();
			break;
		}
		case 'chapter':
		case 'encyclopedia': {
			const rest = [
				c.number,
				c.editors?.length && `edited by ${series(c.editors.map(natural))}`,
				c.edition,
				c.pages
			].filter(Boolean);
			if (c.container) {
				add('In ');
				add(c.container, true);
				add(rest.length ? `, ${stop(rest.join(', '))} ` : '. ');
			} else if (rest.length) add(`${stop(rest.join(', '))} `);
			imprint();
			break;
		}
		case 'report':
			if (c.number) add(`${stop(c.number)} `);
			if (c.container) add(`${stop(c.container)} `);
			imprint();
			break;
		case 'media':
			if (date) add(`${stop(date)} `);
			if (c.container) add(`${stop(c.container)} `);
			if (c.publisher) add(`${stop(c.publisher)} `);
			if (c.licence) add(`${stop(c.licence)} `);
			break;
		case 'article': {
			if (c.container) add(c.container, true);
			let where = [c.volume, c.issue && `no. ${c.issue}`].filter(Boolean).join(', ');
			if (date) where += c.volumeYear ? ` (${c.volumeYear}; published ${date})` : ` (${date})`;
			if (c.pages) where += `: ${c.pages}`;
			add(where ? ` ${stop(where.trim())} ` : '. ');
			break;
		}
		case 'wikipedia':
			if (c.container) add(`${stop(c.container)} `);
			if (c.publisher) add(`${stop(c.publisher)} `);
			if (date) add(`Last modified ${date}. `);
			break;
		case 'web': {
			if (c.container) add(`${stop(c.container)} `);
			const facts = [c.publisher, date].filter(Boolean).join(', ');
			if (facts) add(`${stop(facts)} `);
		}
	}

	if (c.language) add(`In ${languageName(c.language)}. `);
	for (const seen of seenAs(c)) add(`${seen} `);
	add(`Accessed ${chicagoDate(c.accessed)}. `);
	const href = citationHref(c);
	parts.push({ text: href, href });
	add('.');
	return parts;
}

/** How a source was seen when it was not read whole: in another work, or as an abstract. */
const seenAs = (c: Citation) =>
	[c.citedIn && `Cited in ${stop(c.citedIn)}`, c.abstractOnly && 'Read in its abstract.'].filter(
		(s): s is string => typeof s === 'string'
	);

/** The entry as plain text, for tests and screen-reader-friendly titles. */
export const chicagoText = (c: Citation) =>
	chicago(c)
		.map((p) => p.text)
		.join('');

/** A licence that needs a credit beside the image, not only in the list. */
export const needsCaption = (licence: string) => !/^(public domain|cc0\b|pd\b)/i.test(licence);

/** The short caption credit: "Jane Doe / CC BY-SA 4.0". */
export const captionCredit = (c: Citation) =>
	[
		c.authors?.length ? c.authors.map(natural).join(', ') + (c.etAl ? ' et al.' : '') : undefined,
		c.licence
	]
		.filter(Boolean)
		.join(' / ');

/** One entry of a frame's Sources list: derived from a key citation, never authored. */
export interface Source {
	title: string;
	url: string;
	note?: string;
}

/** Authors as the Sources list names them: "A and B", or "A et al." past three. */
function shortAuthors(c: Citation): string | undefined {
	const names = (c.authors ?? []).map(natural);
	if (!names.length || (c.kind === 'wikipedia' && names.length === 1)) return undefined;
	if (c.etAl || names.length > 3) return `${names[0]} et al.`;
	return series(names);
}

/**
 * A key citation as its Sources entry: "Authors, Title", linked, with where
 * and when it appeared and the citation's own note. Wikipedia reads
 * "Title — Wikipedia", as the curated frames always wrote it.
 */
export function keySource(c: Citation): Source {
	const url = citationHref(c);
	if (c.kind === 'wikipedia') {
		const lang = c.language && c.language !== 'en' ? `${languageName(c.language)} ` : '';
		return { title: `${c.title} — ${lang}Wikipedia`, url };
	}
	const where =
		c.kind === 'book' || c.kind === 'report' ? c.publisher : (c.container ?? c.publisher);
	// An organisation that is also the site says so once: "Introducing X | Anthropic".
	const who = where && shortAuthors(c) === where ? undefined : shortAuthors(c);
	const date = c.published && chicagoDate(c.published, c.circa);
	const facts = [where, date].filter(Boolean).join(', ');
	const note = [facts, ...seenAs(c).map((s) => s.replace(/\.$/, '')), c.note]
		.filter(Boolean)
		.join('. ');
	return { title: who ? `${who}, ${c.title}` : c.title, url, ...(note ? { note } : {}) };
}

/** A frame's Sources list: its key citations, in the order they are written. */
export const keySources = (citations: Citation[]) => citations.filter((c) => c.key).map(keySource);

type Obj = Record<string, unknown>;
const isObj = (v: unknown): v is Obj => typeof v === 'object' && v !== null && !Array.isArray(v);
const isText = (v: unknown): v is string => typeof v === 'string' && v.trim() !== '';

const isAuthor = (a: unknown) =>
	isObj(a) && (isText(a.name) || (isText(a.family) && (a.given === undefined || isText(a.given))));

/** Every problem with one citation, as bare messages (the caller adds where). */
export function citationProblems(c: unknown): string[] {
	if (!isObj(c)) return ['is not an object'];
	const out: string[] = [];
	if (!CITATION_KINDS.includes(c.kind as never))
		out.push(`kind must be one of ${CITATION_KINDS.join(', ')}`);
	if (!isText(c.title)) out.push('title is required');
	if (c.doi !== undefined && !(isText(c.doi) && DOI.test(c.doi)))
		out.push('doi must be a bare DOI, like 10.1109/5.58323');
	if (c.url === undefined) {
		if (c.doi === undefined) out.push('url is required, unless there is a doi');
	} else if (!isText(c.url) || !/^https?:\/\//.test(c.url)) out.push('url must be http(s)');
	else if (/^https?:\/\/(dx\.)?doi\.org\//i.test(c.url))
		out.push('a doi.org url goes in doi, as the bare DOI');
	else if (
		(c.kind === 'wikipedia' || /^https?:\/\/[^/]*\bwikipedia\.org\//.test(c.url)) &&
		!/[?&]oldid=\d+/.test(c.url) &&
		// An image's file page is not an article: a media citation credits it as it is (sprint 027).
		!(c.kind === 'media' && /\/wiki\/(File|Image):|[?&]title=(File|Image):/.test(c.url))
	)
		out.push('a Wikipedia citation needs a permanent revision url (oldid=)');
	if (!isText(c.accessed) || !/^\d{4}-\d{2}-\d{2}$/.test(c.accessed) || !DATE.test(c.accessed))
		out.push('accessed date is required, as YYYY-MM-DD');
	for (const k of ['published', 'written'] as const)
		if (c[k] !== undefined && !(isText(c[k]) && isPublished(c[k])))
			out.push(`${k} must be ${PUBLISHED}`);
	if (c.circa !== undefined && (typeof c.circa !== 'boolean' || c.published === undefined))
		out.push('circa must be true or false, with a published date');
	if (c.key !== undefined && typeof c.key !== 'boolean') out.push('key must be true or false');
	for (const k of ['authors', 'editors', 'translators', 'engravers', 'recipients'] as const)
		if (c[k] !== undefined && !(Array.isArray(c[k]) && c[k].every(isAuthor)))
			out.push(`${k} must each have a family name or a name`);
	if (c.etAl !== undefined && (typeof c.etAl !== 'boolean' || !Array.isArray(c.authors)))
		out.push('etAl must be true or false, with at least one author listed');
	for (const k of [
		'container',
		'publisher',
		'place',
		'volume',
		'issue',
		'pages',
		'number',
		'note',
		'edition',
		'citedIn'
	] as const)
		if (c[k] !== undefined && !isText(c[k])) out.push(`${k} must be text`);
	if (c.abstractOnly !== undefined && typeof c.abstractOnly !== 'boolean')
		out.push('abstractOnly must be true or false');
	if (c.volumeYear !== undefined) {
		const year = isText(c.volumeYear) ? publishedYear(c.volumeYear) : undefined;
		const published = isText(c.published) ? publishedYear(c.published) : undefined;
		if (c.kind !== 'article' || published === undefined)
			out.push('volumeYear is for an article, with a published date');
		else if (year === undefined || year > published)
			out.push('volumeYear is the year the volume is for, so no later than published');
	}
	if (c.language !== undefined && !(isText(c.language) && LANGUAGE.test(c.language)))
		out.push('language must be a language code, like "de" or "grc"');
	else if (c.kind === 'wikipedia' && isText(c.url)) {
		const lang = wikipediaLanguage(c.url);
		if (lang && lang !== 'en' && c.language !== lang)
			out.push(`a ${lang}.wikipedia.org article needs "language": "${lang}"`);
	}
	if (c.kind === 'chapter' && !isText(c.container))
		out.push('a chapter needs its container: the volume or proceedings it appears in');
	if (c.kind === 'encyclopedia' && !isText(c.container))
		out.push('an encyclopedia entry needs its container: the encyclopedia');
	if (c.kind === 'letter' && !(Array.isArray(c.recipients) && c.recipients.length))
		out.push('a letter needs its recipients');
	if (c.kind === 'media') {
		if (!isText(c.licence)) out.push('a media citation needs a licence');
		if (!isText(c.file)) out.push('a media citation needs the file it credits');
	}
	return out;
}

/** A bibliography's order: alphabetical by the entry as written. */
export const bibliography = (citations: Citation[]) =>
	[...citations].sort((a, b) =>
		chicagoText(a).localeCompare(chicagoText(b), 'en', { sensitivity: 'base' })
	);

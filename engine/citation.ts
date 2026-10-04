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
 * `diary` is a dated entry in a named edition of a diary (sprint 029).
 * `case` is a court's opinion and `statute` a law or a regulation, each
 * rendered in legal form (sprint 033); `treaty` an agreement between states,
 * in legal form too (sprint 050).
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
	'encyclopedia',
	'diary',
	'case',
	'statute',
	'treaty'
] as const;
export type CitationKind = (typeof CITATION_KINDS)[number];

/**
 * How much of a source was read, when not all of it (sprint 029). `record`
 * is a work whose own bibliographic record was reached (Crossref, a
 * publisher's landing page) but not its text (sprint 033).
 */
export const READ_EXTENTS = ['abstract', 'first-page', 'excerpt', 'record'] as const;
export type ReadExtent = (typeof READ_EXTENTS)[number];
const READ_TEXT: Record<ReadExtent, string> = {
	abstract: 'Read in its abstract.',
	'first-page': 'Read in its first page.',
	excerpt: 'Read in an excerpt.',
	record: 'Read in its catalog record only.'
};

/**
 * Where a case or a law is printed, as the legal form cites it: a reporter
 * ("175 Ky. 416"), a session-law volume ("61 Stat. 41") or a code ("42
 * C.F.R."), each `volume name page`, with any part a code has not left out.
 */
export interface LegalCite {
	volume?: string;
	name: string;
	page?: string;
}

/** A person (`family`, optionally `given`) or an organisation (`name`). */
export type Author = { family: string; given?: string } | { name: string };

export interface Citation {
	kind: CitationKind;
	title: string;
	/**
	 * Where it was read. Required unless there is a `doi`, or a `citedIn`
	 * naming a work this frame cites with a link (sprint 029). For Wikipedia,
	 * a permanent revision link (`oldid=`): articles change. A JSTOR article
	 * by its stable url (`https://www.jstor.org/stable/N`).
	 */
	url?: string;
	/**
	 * The url is a copy of the work on another site, because no official copy
	 * exists anywhere: "(copy at host)" (sprint 029).
	 */
	mirror?: boolean;
	/** The bare DOI (`10.1109/5.58323`); the entry links it at doi.org. */
	doi?: string;
	/**
	 * A key source: listed under Sources, the frame's short list, as well as
	 * in the bibliography. Every frame flags at least one (sprint 008).
	 */
	key?: boolean;
	/** A key source's remark in the Sources list: a page, why it matters. */
	note?: string;
	/** `YYYY-MM-DD`: when the page was read. Only a citation with no link, seen in another work, goes without. */
	accessed?: string;
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
	/**
	 * When a letter was written, or a diary's entry; `published` is when it
	 * was printed. Same forms as `published`. Required on a diary.
	 */
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
	/**
	 * How much of it was read, when not all of it: its `abstract`, its
	 * `first-page` (an old letter a site shows only the opening of), or an
	 * `excerpt` (sprint 029; replaces `abstractOnly`).
	 */
	read?: ReadExtent;
	/** A case's reporter: volume, reporter and first page, all three ("175 Ky. 416"). */
	reporter?: LegalCite;
	/** A case's neutral citation, in place of a reporter: "[2025] EWHC 2863 (Ch)". */
	neutral?: string;
	/** A case's court, as the parenthetical abbreviates it ("Tex."), when the reporter does not say it. */
	court?: string;
	/** A statute's public law number: "80-36" ("Pub. L. No. 80-36"). */
	publicLaw?: string;
	/** A statute's chapter in its session laws: "192" ("ch. 192"). */
	chapter?: string;
	/** A statute's section, as written: "§ 19", "§§ 640.20–640.25". */
	section?: string;
	/**
	 * A statute's session laws or code: "61 Stat. 41", "42 C.F.R."; a treaty's series: "1 Consol. T.S. 271".
	 * An English act's regnal year ("1 Will. & Mar. Sess. 2"), a foreign law's gazette, with `citeAs`.
	 */
	code?: LegalCite;
	/**
	 * A statute that is not a US one (sprint 050): `regnal`, an English act by regnal year and chapter
	 * ("1 Will. & Mar. Sess. 2, c. 2"); `gazette`, a foreign law by the gazette that printed it
	 * ("Reichsgesetzblatt 1935, Teil I, p. 1146").
	 */
	citeAs?: 'regnal' | 'gazette';
	/**
	 * A treaty's parties, as its title page names them: ["Holy Roman Empire", "France"]. Left out for
	 * a treaty among many states, as legal form leaves them out (the Geneva Convention of 1864).
	 */
	parties?: string[];
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

/**
 * The link an entry carries: the DOI at doi.org when there is one, else the
 * url; none for a source seen only in another work. A media citation's DOI
 * is its chart's data source, not where the chart is (sprint 033), so its
 * link is its url.
 */
export const citationHref = (c: Citation): string | undefined =>
	c.kind === 'media' ? c.url : c.doi ? `https://doi.org/${c.doi}` : c.url;

/** "175 Ky. 416", "61 Stat. 41", "42 C.F.R.". */
const legalCite = (l: LegalCite) => [l.volume, l.name, l.page].filter(Boolean).join(' ');

/**
 * A case or a statute in legal form, after its name (sprint 033):
 *
 * - a case: ", 175 Ky. 416 (1917)", ", 547 S.W.2d 582 (Tex. 1977)", or its
 *   neutral citation, " [2025] EWHC 2863 (Ch)", which carries its own year;
 * - a statute: ", Pub. L. No. 80-36, 61 Stat. 41 (1947)". A session law's
 *   chapter and section come before the volume they are printed in ("ch.
 *   192, § 19, 31 Stat. 753"); a code cited by section, or a state's session
 *   laws cited by chapter, take theirs after it ("42 C.F.R. § 482.23",
 *   "2023 Or. Laws ch. 507"). The year is left out where the cite already
 *   says it: in the name ("…Act of 1947") or as the volume ("2023 Or. Laws").
 *   An English act by regnal year: ", 1 Will. & Mar. Sess. 2, c. 2", the
 *   regnal year its year; a foreign law by its gazette: ", Reichsgesetzblatt
 *   1935, Teil I, p. 1146" (sprint 050);
 * - a treaty: ", Holy Roman Empire–France, October 24, 1648", and its
 *   series when it has one (", 1 Consol. T.S. 271"; sprint 050).
 *
 * Undefined for any other kind.
 */
export function legalForm(c: Citation): string | undefined {
	const year = c.published ? (DATE.exec(c.published)?.[1] ?? c.published) : undefined;
	if (c.kind === 'case') {
		if (c.neutral) return ` ${c.neutral}`;
		const when = [c.court, year].filter(Boolean).join(' ');
		return `${c.reporter ? `, ${legalCite(c.reporter)}` : ''}${when ? ` (${when})` : ''}`;
	}
	if (c.kind === 'treaty') {
		const signed = c.published ? chicagoDate(c.published) : undefined;
		const cite = [(c.parties ?? []).join('–'), signed, c.code && legalCite(c.code)];
		return `, ${cite.filter(Boolean).join(', ')}`;
	}
	if (c.kind !== 'statute') return undefined;
	if (c.citeAs === 'regnal') {
		const cite = [c.code && legalCite(c.code), c.chapter && `c. ${c.chapter}`, c.section];
		return `, ${cite.filter(Boolean).join(', ')}`;
	}
	if (c.citeAs === 'gazette') {
		const cite = [c.code?.name, c.code?.volume, c.code?.page && `p. ${c.code.page}`, c.section];
		const said = !year || c.title.includes(year) || (c.code?.name ?? '').includes(year);
		return `, ${cite.filter(Boolean).join(', ')}${said ? '' : ` (${year})`}`;
	}
	const at = [c.chapter && `ch. ${c.chapter}`, c.section];
	const parts = [c.publicLaw && `Pub. L. No. ${c.publicLaw}`];
	if (!c.code) parts.push(...at);
	else if (c.code.page) parts.push(...at, legalCite(c.code));
	else
		parts.push(
			[legalCite(c.code), c.section, c.chapter && `ch. ${c.chapter}`].filter(Boolean).join(' ')
		);
	const cite = parts.filter(Boolean).join(', ');
	const said = !year || c.title.includes(year) || c.code?.volume === year;
	return `${cite ? `, ${cite}` : ''}${said ? '' : ` (${year})`}`;
}

/** A case or a statute as one line of plain text: "Frank v. South, 175 Ky. 416 (1917)". */
export const legalText = (c: Citation) => {
	const form = legalForm(c);
	return form === undefined ? undefined : `${c.title}${form}`;
};

/** A mirror's host, for "(copy at host)". */
const mirrorHost = (c: Citation) =>
	c.mirror && c.url ? /^https?:\/\/(?:www\.)?([^/:]+)/.exec(c.url)?.[1] : undefined;

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
 * - diary: Author. Diary entry, Date, in _Title_, edited by Editor.
 *   Container. Place: Publisher, Year. Accessed Date. URL.
 *
 * With a `doi`, the URL is the DOI at doi.org. An approximate date reads
 * "ca. 1951". A mirror's URL is followed by "(copy at host)"; a source seen
 * only in another work has no URL and no access date.
 */
export function chicago(c: Citation): Part[] {
	const parts: Part[] = [];
	const add = (text: string, italic = false) => parts.push(italic ? { text, italic } : { text });

	if (c.authors?.length) add(`${stop(chicagoAuthors(c.authors, c.etAl))} `);

	const italicTitle = c.kind === 'book' || c.kind === 'report' || c.kind === 'media';
	const legal = legalForm(c);
	if (legal !== undefined) {
		// A case's name is italic, a statute's is not; the cite follows either.
		add(c.title, c.kind === 'case');
		add(`${stop(legal)} `);
	} else if (c.kind === 'diary') {
		// The entry is the item, the diary its edition: "Diary entry, date, in _Diary_, edited by …".
		const rest = [
			c.editors?.length && `edited by ${series(c.editors.map(natural))}`,
			c.edition,
			c.volume && `vol. ${c.volume}`,
			c.pages
		].filter(Boolean);
		add(`Diary entry${c.written ? `, ${chicagoDate(c.written)}` : ''}, in `);
		add(c.title, true);
		add(rest.length ? `, ${stop(rest.join(', '))} ` : '. ');
	} else if (italicTitle) {
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
	const inVolume = c.kind === 'chapter' || c.kind === 'encyclopedia' || c.kind === 'diary';
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
		case 'diary':
			if (c.container) add(`${stop(c.container)} `);
			imprint();
			break;
		case 'report':
			if (c.number) add(`${stop(c.number)} `);
			if (c.container) add(`${stop(c.container)} `);
			imprint();
			break;
		case 'media':
			if (date) add(`${stop(date)} `);
			if (c.container) add(`${stop(c.container)} `);
			if (c.number) add(`${stop(c.number)} `);
			if (c.publisher) add(`${stop(c.publisher)} `);
			if (c.licence) add(`${stop(c.licence)} `);
			break;
		case 'case':
		case 'statute':
		case 'treaty':
			// Where it was read: the date is in the cite already.
			if (c.container) add(`${stop(c.container)} `);
			if (c.publisher) add(`${stop(c.publisher)} `);
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
	// A chart's data source, by its DOI (sprint 033).
	const data = c.kind === 'media' && c.doi ? `https://doi.org/${c.doi}` : undefined;
	if (data) {
		add('Data: ');
		parts.push({ text: data, href: data });
		add('. ');
	}
	const href = citationHref(c);
	if (!href && data && c.accessed) add(`Accessed ${chicagoDate(c.accessed)}.`);
	if (href) {
		if (c.accessed) add(`Accessed ${chicagoDate(c.accessed)}. `);
		parts.push({ text: href, href });
		const host = mirrorHost(c);
		add(host ? ` (copy at ${host}).` : '.');
	}
	// An entry with no link ends at its last element, which `stop` closed.
	const last = parts[parts.length - 1];
	if (!href && last) last.text = last.text.trimEnd();
	return parts;
}

/**
 * How much was read. A kept answer saved before sprint 029 may carry the old
 * `abstractOnly` flag on a frame's citation it copied, and still says so.
 */
const readExtent = (c: Citation): ReadExtent | undefined =>
	c.read ?? ((c as { abstractOnly?: unknown }).abstractOnly === true ? 'abstract' : undefined);

/** How a source was seen when it was not read whole: in another work, or in part. */
const seenAs = (c: Citation) =>
	[c.citedIn && `Cited in ${stop(c.citedIn)}`, readExtent(c) && READ_TEXT[readExtent(c)!]].filter(
		(s): s is string => typeof s === 'string'
	);

/** The entry as plain text, for tests and screen-reader-friendly titles. */
export const chicagoText = (c: Citation) =>
	chicago(c)
		.map((p) => p.text)
		.join('');

/** A licence that needs a credit beside the image, not only in the list. */
export const needsCaption = (licence: string) => !/^(public domain|cc0\b|pd\b)/i.test(licence);

/**
 * The short caption credit: "Jane Doe / CC BY-SA 4.0"; a chart's with its
 * data's DOI, "kloom contributors / MIT / data doi:10.1289/EHP7932".
 */
export const captionCredit = (c: Citation) =>
	[
		c.authors?.length ? c.authors.map(natural).join(', ') + (c.etAl ? ' et al.' : '') : undefined,
		c.licence,
		c.kind === 'media' && c.doi ? `data doi:${c.doi}` : undefined
	]
		.filter(Boolean)
		.join(' / ');

/** One entry of a frame's Sources list: derived from a key citation, never authored. */
export interface Source {
	title: string;
	/** Always set: a key source links what was read, and validation refuses one without a link. */
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
	const url = citationHref(c) ?? (c.doi ? `https://doi.org/${c.doi}` : '');
	const legal = legalText(c);
	if (legal) {
		// The legal form names it and dates it; where it was read follows.
		const host = mirrorHost(c);
		const seen = [...seenAs(c), host && `Copy at ${host}`];
		const note = [c.container ?? c.publisher, ...seen.map((s) => s && s.replace(/\.$/, '')), c.note]
			.filter(Boolean)
			.join('. ');
		return { title: legal, url, ...(note ? { note } : {}) };
	}
	if (c.kind === 'wikipedia') {
		const lang = c.language && c.language !== 'en' ? `${languageName(c.language)} ` : '';
		return { title: `${c.title} — ${lang}Wikipedia`, url };
	}
	const where =
		c.kind === 'book' || c.kind === 'report' ? c.publisher : (c.container ?? c.publisher);
	// An organisation that is also the site says so once: "Introducing X | Anthropic".
	const who = where && shortAuthors(c) === where ? undefined : shortAuthors(c);
	const date = c.published && chicagoDate(c.published, c.circa);
	const entry = c.kind === 'diary' && c.written && `entry of ${chicagoDate(c.written)}`;
	const facts = [entry, where, date].filter(Boolean).join(', ');
	const host = mirrorHost(c);
	const seen = [...seenAs(c), host && `Copy at ${host}`];
	const note = [facts, ...seen.map((s) => s && s.replace(/\.$/, '')), c.note]
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

/**
 * Every problem with one citation, as bare messages (the caller adds where).
 * `legacy` accepts what reader data saved before a field was renamed: a kept
 * answer's copy of a citation with `abstractOnly` (sprint 029).
 */
export function citationProblems(c: unknown, options: { legacy?: boolean } = {}): string[] {
	if (!isObj(c)) return ['is not an object'];
	const out: string[] = [];
	if (!CITATION_KINDS.includes(c.kind as never))
		out.push(`kind must be one of ${CITATION_KINDS.join(', ')}`);
	if (!isText(c.title)) out.push('title is required');
	if (c.doi !== undefined && !(isText(c.doi) && DOI.test(c.doi)))
		out.push('doi must be a bare DOI, like 10.1109/5.58323');
	if (c.url === undefined) {
		if (c.doi === undefined && !isText(c.citedIn))
			out.push('url is required, unless there is a doi, or a citedIn naming a work cited with one');
		if (c.doi === undefined && c.key === true)
			out.push('a key source links what was read: one seen only in another work cannot be key');
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
	else if (
		/^https?:\/\/(www\.)?jstor\.org\//.test(c.url) &&
		!/^https?:\/\/(www\.)?jstor\.org\/stable\/\d+\/?$/.test(c.url)
	)
		out.push('a JSTOR article is cited by its stable url, https://www.jstor.org/stable/N');
	// A source seen only in another work was never opened, so has no access date to give.
	const seenOnly = c.url === undefined && c.doi === undefined && isText(c.citedIn);
	if (
		c.accessed === undefined
			? !seenOnly
			: !(isText(c.accessed) && /^\d{4}-\d{2}-\d{2}$/.test(c.accessed) && DATE.test(c.accessed))
	)
		out.push('accessed date is required, as YYYY-MM-DD');
	if (c.mirror !== undefined) {
		if (typeof c.mirror !== 'boolean') out.push('mirror must be true or false');
		else if (c.mirror && (c.url === undefined || c.doi !== undefined))
			out.push('mirror is for a url copying a work with no official copy, so not with a doi');
	}
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
	if (c.abstractOnly !== undefined && !(options.legacy && typeof c.abstractOnly === 'boolean'))
		out.push('abstractOnly is now read: "abstract"');
	if (c.read !== undefined && !READ_EXTENTS.includes(c.read as never))
		out.push(`read must be one of ${READ_EXTENTS.join(', ')}`);
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
	if (c.kind === 'diary' && c.written === undefined)
		out.push('a diary entry needs the date it was written');
	if (c.kind === 'media') {
		if (!isText(c.licence)) out.push('a media citation needs a `licence`');
		if (!isText(c.file)) out.push('a media citation needs the file it credits');
	}
	out.push(...legalProblems(c));
	return out;
}

/** The fields only a case, or only a statute, carries (sprint 033); `code` a treaty's too (sprint 050). */
const CASE_FIELDS = ['reporter', 'neutral', 'court'] as const;
const STATUTE_FIELDS = ['publicLaw', 'chapter', 'section', 'code'] as const;

/** A reporter or a code: a name, and a volume and page as text; `whole` needs both. */
const isLegalCite = (v: unknown, whole: boolean) =>
	isObj(v) &&
	isText(v.name) &&
	(['volume', 'page'] as const).every((k) =>
		whole ? isText(v[k]) : v[k] === undefined || isText(v[k])
	);

function legalProblems(c: Obj): string[] {
	const out: string[] = [];
	const misplaced = (fields: readonly string[], belongs: string) => {
		for (const k of fields) if (c[k] !== undefined) out.push(`${k} is for ${belongs}`);
	};
	if (c.kind !== 'statute') misplaced(['citeAs'], 'a statute');
	if (c.kind !== 'treaty') misplaced(['parties'], 'a treaty');
	if (c.kind === 'case') {
		misplaced(STATUTE_FIELDS, 'a statute');
		if ((c.reporter === undefined) === (c.neutral === undefined))
			out.push('a case needs its reporter or its neutral citation, one of the two');
		if (c.reporter !== undefined && !isLegalCite(c.reporter, true))
			out.push(
				'reporter needs its volume, name and first page as text: {"volume": "175", "name": "Ky.", "page": "416"}'
			);
		for (const k of ['neutral', 'court'] as const)
			if (c[k] !== undefined && !isText(c[k])) out.push(`${k} must be text`);
		if (c.published === undefined) out.push('a case needs the date it was decided, in published');
	} else if (c.kind === 'statute' && c.citeAs !== undefined) {
		misplaced(CASE_FIELDS, 'a case');
		if (c.publicLaw !== undefined)
			out.push(
				'publicLaw is a US statute’s: an English act is cited by regnal year, a foreign law by its gazette'
			);
		if (c.citeAs === 'regnal') {
			if (!(isLegalCite(c.code, false) && isText((c.code as Obj).volume) && isText(c.chapter)))
				out.push(
					'an act cited by regnal year needs its code ({"volume": "1", "name": "Will. & Mar. Sess. 2"}) and chapter'
				);
		} else if (c.citeAs === 'gazette') {
			if (!(isLegalCite(c.code, false) && isText((c.code as Obj).page)))
				out.push(
					'a law cited by its gazette needs the gazette and its page in code: {"name": "…", "page": "1146"}'
				);
		} else
			out.push(
				'citeAs is "regnal" (an English act) or "gazette" (a foreign law); a US statute leaves it out'
			);
		for (const k of ['chapter', 'section'] as const)
			if (c[k] !== undefined && !isText(c[k])) out.push(`${k} must be text`);
	} else if (c.kind === 'treaty') {
		misplaced([...CASE_FIELDS, 'publicLaw', 'chapter', 'section'], 'a case or a statute');
		if (
			c.parties !== undefined &&
			!(Array.isArray(c.parties) && c.parties.length >= 2 && c.parties.every(isText))
		)
			out.push('parties are two or more, as text; a treaty among many states leaves them out');
		if (c.published === undefined) out.push('a treaty needs the date it was signed, in published');
		if (c.code !== undefined && !isLegalCite(c.code, false))
			out.push('code needs its name, and its volume and page as text when it has them');
	} else if (c.kind === 'statute') {
		misplaced(CASE_FIELDS, 'a case');
		if (c.publicLaw === undefined && c.code === undefined)
			out.push('a statute needs its publicLaw number, or the code or session laws it is in');
		if (c.publicLaw !== undefined && !(isText(c.publicLaw) && /^\d+-\d+$/.test(c.publicLaw)))
			out.push('publicLaw is the number as Congress and law: "80-36"');
		if (c.code !== undefined && !isLegalCite(c.code, false))
			out.push('code needs its name, and its volume and page as text when it has them');
		for (const k of ['chapter', 'section'] as const)
			if (c[k] !== undefined && !isText(c[k])) out.push(`${k} must be text`);
	} else misplaced([...CASE_FIELDS, ...STATUTE_FIELDS], 'a case or a statute');
	if (c.kind === 'treaty' && c.authors !== undefined)
		out.push('a treaty names no authors: its parties go in parties');
	if ((c.kind === 'case' || c.kind === 'statute') && c.authors !== undefined)
		out.push(
			`a ${c.kind} names no authors: a case is named by its parties and its court goes in court, a law by its own name`
		);
	return out;
}

/** Text compared loosely: case, quotation marks and punctuation set aside. */
const loose = (s: string) =>
	s
		.toLowerCase()
		.replace(/[^\p{L}\p{N}]+/gu, ' ')
		.trim();

/**
 * A frame's citations taken together (sprint 029): one with no url or doi
 * stands on its `citedIn`, which must name a work the frame also cites,
 * with a link, by that work's title.
 */
export function citedInProblems(citations: unknown[]): { index: number; problem: string }[] {
	const linked = citations
		.filter((c): c is Obj => isObj(c) && (isText(c.url) || isText(c.doi)) && isText(c.title))
		.map((c) => loose(c.title as string));
	const out: { index: number; problem: string }[] = [];
	citations.forEach((c, index) => {
		if (!isObj(c) || c.url !== undefined || c.doi !== undefined || !isText(c.citedIn)) return;
		const cited = loose(c.citedIn);
		if (!linked.some((title) => title && cited.includes(title)))
			out.push({
				index,
				problem:
					'has no url or doi, so its citedIn must name, by title, a work this frame cites with one'
			});
	});
	return out;
}

/** A bibliography's order: alphabetical by the entry as written. */
export const bibliography = (citations: Citation[]) =>
	[...citations].sort((a, b) =>
		chicagoText(a).localeCompare(chicagoText(b), 'en', { sensitivity: 'base' })
	);

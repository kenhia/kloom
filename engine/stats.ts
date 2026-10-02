import { loadNames, readSubject } from './load';
import { imageRefs, renderMarkdown } from './markdown';
import type { RawSubject } from './validate';

/**
 * How big the library is (docs/design.md §About): the words a reader reads,
 * the book they would make, and what else the subjects hold. Only the
 * narratives count: a reading's text as the reader sees it, tables and
 * captions included; markup, citations and the Sources list, the scene's
 * headline, accent and metadata, and anything of the reader's own (notes,
 * kept answers, annotations) do not.
 *
 * Read from the raw subjects, nothing validated or sanitised. The library
 * counts each subject as it compiles it (docs/design.md §Serving), and
 * `just stats` counts straight from the files.
 */

/** Words to a printed page (Ken, 2026-09-30). */
export const WORDS_PER_PAGE = 275;

/** The book `words` would make, in whole pages. */
export const pages = (words: number) => Math.round(words / WORDS_PER_PAGE);

/** What a reading holds. */
export interface ReadingStats {
	words: number;
	/** Pictures: every image the reading shows that is not a chart. */
	images: number;
	/** Charts: the SVGs a reading inlines (docs/design.md §Charts). */
	charts: number;
	tables: number;
}

export interface SubjectStats extends ReadingStats {
	id: string;
	title: string;
	subtitle?: string;
	/** Every frame, on the main spine or a trail. */
	frames: number;
	/** Of those, the ones on a trail. */
	trailFrames: number;
	trails: number;
	pages: number;
	citations: number;
	/** Connections stored on this subject's frames (each is stored on one end). */
	connections: number;
}

export interface LibraryStats extends ReadingStats {
	subjects: SubjectStats[];
	frames: number;
	trails: number;
	pages: number;
	citations: number;
	connections: number;
	/** Names in the registry every subject shares. */
	names: number;
	wordsPerPage: number;
}

/** Tags a reader sees as a break between words; every other tag sits inside one. */
const BREAK =
	/<\/?(?:p|li|ul|ol|h[1-6]|table|thead|tbody|tr|td|th|blockquote|pre|br|hr|figcaption|dd|dt|dl)\b[^>]*>/gi;
const ENTITIES: Record<string, string> = { amp: '&', lt: '<', gt: '>', quot: '"', nbsp: ' ' };

/**
 * A rendered reading's text as a reader sees it: the markup and inlined
 * drawings gone, entities decoded, and a space wherever a block or line
 * breaks. Alt text lives in attributes, which go with the tags.
 */
export function plainText(html: string): string {
	return html
		.replace(/<svg\b[\s\S]*?<\/svg>/gi, ' ')
		.replace(BREAK, ' ')
		.replace(/<[^>]*>/g, '')
		.replace(/&(#x[0-9a-f]+|#\d+|\w+);/gi, (m, e: string) =>
			e[0] === '#'
				? String.fromCodePoint(e[1] === 'x' ? parseInt(e.slice(2), 16) : Number(e.slice(1)))
				: (ENTITIES[e] ?? m)
		);
}

/**
 * A rendered reading's words: its plain text split on whitespace. Image
 * credits never reach here (see `readingStats`).
 */
export function wordCount(html: string): number {
	return plainText(html)
		.split(/\s+/)
		.filter((w) => /[\p{L}\p{N}]/u.test(w)).length;
}

/**
 * A reading's words, pictures, charts and tables. It is rendered as the
 * reader gets it, less what is not narrative: a chart's labels are drawing,
 * and a picture's credit is a citation.
 */
export function readingStats(source: string): ReadingStats {
	const refs = imageRefs(source);
	const charts = refs.filter((r) => r.toLowerCase().endsWith('.svg')).length;
	const html = renderMarkdown(source, {
		image: (href) => ({ src: href, ...(href.toLowerCase().endsWith('.svg') ? { svg: '' } : {}) })
	});
	return {
		words: wordCount(html),
		images: refs.length - charts,
		charts,
		tables: (html.match(/<table\b/gi) ?? []).length
	};
}

type Obj = Record<string, unknown>;
const isObj = (v: unknown): v is Obj => typeof v === 'object' && v !== null && !Array.isArray(v);
const list = (v: unknown): unknown[] => (Array.isArray(v) ? v : []);

/** The frame ids a spine walks, from its segments. */
const spineFrames = (spine: unknown): string[] =>
	list(isObj(spine) ? spine.segments : undefined).flatMap((s) =>
		list(isObj(s) ? s.frames : undefined).filter((f): f is string => typeof f === 'string')
	);

/**
 * One subject's counts. A frame counts when a spine (the main one or a
 * trail's) walks it and its directory has a reading, which a served subject's
 * always do; the rest of a frame's file is read leniently.
 */
export function subjectStats(id: string, raw: RawSubject): SubjectStats {
	const trails = Object.values(raw.trails).filter(isObj);
	const main = new Set(spineFrames(raw.spine));
	const onTrails = new Set(trails.flatMap((t) => spineFrames(t.spine)).filter((f) => !main.has(f)));
	const s: SubjectStats = {
		id,
		title: isObj(raw.manifest) && typeof raw.manifest.title === 'string' ? raw.manifest.title : id,
		...(isObj(raw.manifest) && typeof raw.manifest.subtitle === 'string' && raw.manifest.subtitle
			? { subtitle: raw.manifest.subtitle }
			: {}),
		frames: 0,
		trailFrames: 0,
		trails: trails.length,
		words: 0,
		pages: 0,
		images: 0,
		charts: 0,
		tables: 0,
		citations: 0,
		connections: 0
	};
	for (const frame of [...main, ...onTrails]) {
		const r = Object.hasOwn(raw.frames, frame) ? raw.frames[frame] : undefined;
		if (!r || r.reading === null) continue;
		s.frames++;
		if (onTrails.has(frame)) s.trailFrames++;
		const reading = readingStats(r.reading);
		s.words += reading.words;
		s.images += reading.images;
		s.charts += reading.charts;
		s.tables += reading.tables;
		const file = isObj(r.frame) ? r.frame : {};
		s.citations += list(file.citations).length;
		s.connections += list(file.connections).length;
	}
	s.pages = pages(s.words);
	return s;
}

/** The library's counts: its subjects', summed, and the name registry's size. */
export function libraryStats(subjects: SubjectStats[], names: number): LibraryStats {
	const sum = (k: keyof ReadingStats | 'frames' | 'trails' | 'citations' | 'connections') =>
		subjects.reduce((n, s) => n + s[k], 0);
	const words = sum('words');
	return {
		subjects,
		frames: sum('frames'),
		trails: sum('trails'),
		words,
		pages: pages(words),
		images: sum('images'),
		charts: sum('charts'),
		tables: sum('tables'),
		citations: sum('citations'),
		connections: sum('connections'),
		names,
		wordsPerPage: WORDS_PER_PAGE
	};
}

/** Read and count every subject given, and the name registry at `names`. */
export async function readLibraryStats(
	subjects: { id: string; dir: string }[],
	names: string
): Promise<LibraryStats> {
	const [counted, registry] = await Promise.all([
		Promise.all(subjects.map(async (s) => subjectStats(s.id, await readSubject(s.dir)))),
		loadNames(names)
	]);
	return libraryStats(counted, Object.keys(registry.names).length);
}

const n = (v: number) => v.toLocaleString('en-US');

/** The counts as a Markdown table and a line of totals: `just stats`, for sprint records. */
export function statsReport(lib: LibraryStats): string {
	const row = (cells: (string | number)[]) =>
		`| ${cells.map((c) => (typeof c === 'number' ? n(c) : c)).join(' | ')} |`;
	return [
		row(['Subject', 'Frames', 'On trails', 'Trails', 'Words', 'Pages']),
		'| --- | ---: | ---: | ---: | ---: | ---: |',
		...lib.subjects.map((s) => row([s.id, s.frames, s.trailFrames, s.trails, s.words, s.pages])),
		row([
			'**Library**',
			lib.frames,
			lib.subjects.reduce((t, s) => t + s.trailFrames, 0),
			lib.trails,
			lib.words,
			lib.pages
		]),
		'',
		`A book of about ${n(lib.pages)} pages at ${lib.wordsPerPage} words a page, narratives only. ` +
			`${n(lib.images)} images, ${n(lib.charts)} charts, ${n(lib.tables)} tables; ` +
			`${n(lib.citations)} citations, ${n(lib.connections)} connections, ${n(lib.names)} names.`
	].join('\n');
}

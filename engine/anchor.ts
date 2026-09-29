/**
 * Anchoring an annotation to the words it is about (docs/design.md
 * §Annotations, korg 3415), so it finds them again after grow or an edit
 * changes the reading, and says so when it cannot.
 *
 * An anchor is the W3C Web Annotation text-quote selector: the quoted text
 * (`exact`) with some text before and after it (`prefix`, `suffix`), plus
 * where it was (`start`) as a hint. Never character offsets alone: one
 * inserted paragraph would move every annotation below it onto the wrong
 * words.
 *
 * All of it works on the reading's text, as its text nodes give it, with
 * runs of whitespace collapsed to one space: a re-wrapped paragraph reads the
 * same. `start` counts in that collapsed text. Offsets in and out are in the
 * raw text, which is what the page's DOM ranges need.
 */

export interface Anchor {
	/** The quoted words, whitespace collapsed; never empty, never padded. */
	exact: string;
	/** Up to CONTEXT characters before them, and after. */
	prefix: string;
	suffix: string;
	/** Where they started, in the collapsed text: the tie-breaker. */
	start: number;
}

/** A stretch of the raw text, end exclusive. */
export interface Span {
	start: number;
	end: number;
}

/** How much context an anchor keeps on each side, in characters. */
export const CONTEXT = 32;

/** Longest quote kept, in characters: a long paragraph, not a whole reading. */
export const QUOTE_MAX = 4000;

/**
 * How much context must still agree before a quote found in the text is taken
 * to be the same one, unless the quote is distinctive on its own.
 */
const AGREE = 8;
/** A quote at least this long, found exactly once, is itself the evidence. */
const DISTINCT = 24;

/** The text with runs of whitespace collapsed, and where each character came from. */
function collapse(raw: string): { text: string; from: number[] } {
	let text = '';
	const from: number[] = [];
	for (let i = 0; i < raw.length; i++) {
		if (/\s/.test(raw[i])) {
			if (text.endsWith(' ')) continue;
			text += ' ';
		} else text += raw[i];
		from.push(i);
	}
	return { text, from };
}

/** Where raw offset `at` falls in the collapsed text. */
const collapsedAt = (from: number[], at: number) => {
	const i = from.findIndex((r) => r >= at);
	return i < 0 ? from.length : i;
};

/** Anchor the words at `start`..`end` of `raw`; null when there are none. */
export function quoteOf(raw: string, start: number, end: number): Anchor | null {
	while (start < end && /\s/.test(raw[start])) start++;
	while (end > start && /\s/.test(raw[end - 1])) end--;
	if (start >= end) return null;
	const { text, from } = collapse(raw);
	const s = collapsedAt(from, start);
	let e = Math.min(collapsedAt(from, end), s + QUOTE_MAX);
	while (text[e - 1] === ' ') e--;
	return {
		exact: text.slice(s, e),
		prefix: text.slice(Math.max(0, s - CONTEXT), s),
		suffix: text.slice(e, e + CONTEXT),
		start: s
	};
}

/** How far two contexts agree, reading away from the quote; whole agreement counts full. */
function agreement(had: string, has: string, before: boolean): number {
	if (had === has) return CONTEXT;
	let n = 0;
	const max = Math.min(had.length, has.length);
	while (
		n < max &&
		(before ? had[had.length - 1 - n] === has[has.length - 1 - n] : had[n] === has[n])
	)
		n++;
	return n;
}

/**
 * Find an anchor's words in `raw`, or null: the annotation is detached. The
 * quote must be there exactly, give or take whitespace. Of several places it
 * appears, the one whose context agrees most wins, and then the nearest to
 * where it was. A place is taken only when enough of its context agrees, or
 * the quote is long and appears once: a short quote in new surroundings is
 * detached rather than pinned to words that happen to match.
 */
export function findQuote(raw: string, a: Anchor): Span | null {
	const { text, from } = collapse(raw);
	const places: number[] = [];
	for (let i = text.indexOf(a.exact); i >= 0; i = text.indexOf(a.exact, i + 1)) places.push(i);
	if (!places.length) return null;
	const scored = places.map((at) => ({
		at,
		score:
			agreement(a.prefix, text.slice(Math.max(0, at - CONTEXT), at), true) +
			agreement(a.suffix, text.slice(at + a.exact.length, at + a.exact.length + CONTEXT), false)
	}));
	scored.sort((x, y) => y.score - x.score || Math.abs(x.at - a.start) - Math.abs(y.at - a.start));
	const best = scored[0];
	if (best.score < AGREE && !(places.length === 1 && a.exact.length >= DISTINCT)) return null;
	const end = best.at + a.exact.length;
	return { start: from[best.at], end: from[end - 1] + 1 };
}

const segmenter = (granularity: 'sentence' | 'word') =>
	new Intl.Segmenter(undefined, { granularity });

/**
 * The sentences in each block of the reading (a paragraph, heading, list
 * item), trimmed. A line break inside a block is a soft wrap, not a break.
 */
export function sentences(raw: string, blocks: Span[]): Span[] {
	const out: Span[] = [];
	const seg = segmenter('sentence');
	for (const b of blocks) {
		// \s is one character, so replacing each keeps every offset.
		const block = raw.slice(b.start, b.end).replace(/\s/g, ' ');
		for (const { segment, index } of seg.segment(block)) {
			const lead = segment.length - segment.trimStart().length;
			const body = segment.trim();
			if (body)
				out.push({ start: b.start + index + lead, end: b.start + index + lead + body.length });
		}
	}
	return out;
}

/** The words in `raw`: letters and numbers, not the spaces and punctuation between. */
export function words(raw: string): Span[] {
	const out: Span[] = [];
	for (const { segment, index, isWordLike } of segmenter('word').segment(raw))
		if (isWordLike) out.push({ start: index, end: index + segment.length });
	return out;
}

/**
 * Move a choice's start back (-1) a word, taking in the word before it, or on
 * (1) a word, letting go of its first. It never passes the end.
 */
export function moveStart(ws: Span[], sel: Span, dir: -1 | 1): Span {
	let w: Span | undefined;
	if (dir < 0) w = ws.findLast((w) => w.start < sel.start);
	else {
		const first = ws.find((w) => w.end > sel.start);
		w = first && ws.find((w) => w.start >= first.end && w.start < sel.end);
	}
	return w ? { start: w.start, end: sel.end } : sel;
}

/**
 * Move a choice's end on (1) a word, taking in the word after it, or back
 * (-1) a word, letting go of its last. It never passes the start.
 */
export function moveEnd(ws: Span[], sel: Span, dir: -1 | 1): Span {
	let w: Span | undefined;
	if (dir > 0) w = ws.find((w) => w.end > sel.end);
	else {
		const last = ws.findLast((w) => w.start < sel.end);
		w = last && ws.findLast((w) => w.end <= last.start && w.end > sel.start);
	}
	return w ? { start: sel.start, end: w.end } : sel;
}

const isText = (v: unknown): v is string => typeof v === 'string';

/** An anchor from a request or an export file, checked; null if it is not one. */
export function anchorOf(v: unknown): Anchor | null {
	if (typeof v !== 'object' || v === null) return null;
	const { exact, prefix, suffix, start } = v as Record<string, unknown>;
	if (!isText(exact) || !exact || exact !== exact.trim() || exact.length > QUOTE_MAX) return null;
	if (!isText(prefix) || !isText(suffix)) return null;
	if (prefix.length > CONTEXT || suffix.length > CONTEXT) return null;
	if (typeof start !== 'number' || !Number.isInteger(start) || start < 0) return null;
	return { exact, prefix, suffix, start };
}

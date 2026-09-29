import { join } from 'node:path';
import { beforeAll, describe, expect, it } from 'vitest';
import {
	anchorOf,
	CONTEXT,
	findQuote,
	moveEnd,
	moveStart,
	quoteOf,
	sentences,
	words,
	type Anchor,
	type Span
} from './anchor';
import { loadSubject } from './load';
import type { Frame } from './model';

/** Visible text of rendered HTML, as the reading's text nodes would give it. */
const textOf = (html: string) =>
	html
		.replace(/<svg[\s\S]*?<\/svg>/g, '')
		.replace(/<[^>]*>/g, '')
		.replace(/&amp;/g, '&')
		.replace(/&quot;/g, '"')
		.replace(/&#39;/g, "'")
		.replace(/&lt;/g, '<')
		.replace(/&gt;/g, '>');

/** Anchor the first occurrence of `quote` in `text`. */
function anchorAt(text: string, quote: string): Anchor {
	const at = text.indexOf(quote);
	expect(at, `"${quote}" is in the text`).toBeGreaterThanOrEqual(0);
	return quoteOf(text, at, at + quote.length)!;
}
const found = (text: string, a: Anchor) => {
	const at = findQuote(text, a);
	return at && text.slice(at.start, at.end);
};

describe('quoteOf', () => {
	const text = 'One sentence here.\n  Another\nsentence, wrapped.  And a third.';

	it('takes the quote with its context, whitespace collapsed', () => {
		const a = anchorAt(text, 'Another\nsentence');
		expect(a.exact).toBe('Another sentence');
		expect(a.prefix).toBe('One sentence here. ');
		expect(a.suffix).toBe(', wrapped. And a third.');
		expect(a.start).toBe('One sentence here. '.length);
	});

	it('trims whitespace from the ends of a selection, and refuses an empty one', () => {
		const at = text.indexOf('  And');
		expect(quoteOf(text, at, at + 5)!.exact).toBe('And');
		expect(quoteOf(text, 18, 21)).toBeNull();
		expect(quoteOf(text, 5, 5)).toBeNull();
	});

	it('keeps no more context than CONTEXT characters on each side', () => {
		const long = 'x'.repeat(100) + ' target ' + 'y'.repeat(100);
		const a = anchorAt(long, 'target');
		expect(a.prefix).toHaveLength(CONTEXT);
		expect(a.suffix).toHaveLength(CONTEXT);
	});
});

describe('findQuote', () => {
	const text = 'The cat sat. The dog sat. The cat ran away from the dog.';

	it('re-finds a quote where it was', () => {
		expect(findQuote(text, anchorAt(text, 'dog sat'))).toEqual({
			start: text.indexOf('dog sat'),
			end: text.indexOf('dog sat') + 7
		});
	});

	it('picks the occurrence whose context matches, not the first', () => {
		const at = text.lastIndexOf('The cat');
		const a = quoteOf(text, at, at + 7)!;
		expect(findQuote(text, a)!.start).toBe(at);
	});

	it('re-finds across a re-wrapped paragraph', () => {
		const a = anchorAt(text, 'dog sat');
		const rewrapped = text.replace('The dog sat.', 'The dog\n  sat.');
		expect(found(rewrapped, a)).toBe('dog\n  sat');
	});

	it('detaches when the quoted words are gone', () => {
		expect(findQuote(text, anchorAt(text, 'dog sat'))).not.toBeNull();
		expect(findQuote(text.replace('dog sat', 'dog stood'), anchorAt(text, 'dog sat'))).toBeNull();
	});

	it('detaches a short quote whose surroundings all changed, rather than guess', () => {
		const a = anchorAt(text, 'cat');
		expect(findQuote('A cat is here, and that is all.', a)).toBeNull();
	});

	it('keeps a long quote found once even when its surroundings changed', () => {
		const quote = 'cat ran away from the dog';
		const a = anchorAt(text, quote);
		expect(found(`Something else entirely: it ${quote}, it did.`, a)).toBe(quote);
	});

	it('finds a quote that is the whole text, or at its very start or end', () => {
		expect(found('Only this.', anchorAt('Only this.', 'Only this.'))).toBe('Only this.');
		expect(found(text, anchorAt(text, 'The cat sat'))).toBe('The cat sat');
		expect(found(text, anchorAt(text, 'from the dog.'))).toBe('from the dog.');
	});
});

describe('annotations on a real reading survive the edits grow makes', () => {
	let frame: Frame;
	beforeAll(async () => {
		const subject = await loadSubject(join(import.meta.dirname, '..', 'subjects', 'western-civ'));
		frame = subject.frames['printing-press'];
	});

	const quotes = {
		// Kept through an inserted paragraph above it.
		inserted: 'None of the pieces was new on\nits own.',
		// Kept though the sentence after it is reworded.
		reworded: 'Movable type had been made in China by the eleventh century',
		// Its sentence is deleted: it detaches.
		deleted: 'Korean printers were casting it in metal before Gutenberg was born.'
	};

	it('re-finds, re-finds and detaches', () => {
		const before = textOf(frame.readingHtml);
		const a = Object.fromEntries(
			Object.entries(quotes).map(([k, q]) => [k, anchorAt(before, q)])
		) as Record<keyof typeof quotes, Anchor>;

		const after = textOf(frame.readingHtml)
			.replace(
				'Johannes Gutenberg worked',
				'A new paragraph, as grow might add one, sits here now.\n\nJohannes Gutenberg worked'
			)
			.replace(', and\nKorean printers were casting it in metal before Gutenberg was born.', '.')
			.replace('What\nGutenberg put together was', 'What Gutenberg assembled was');
		expect(after).not.toBe(before);

		expect(found(after, a.inserted)).toBe(quotes.inserted);
		expect(found(after, a.reworded)).toBe(quotes.reworded);
		expect(findQuote(after, a.deleted)).toBeNull();
	});
});

describe('sentences and words, for choosing text with the keyboard', () => {
	const text = 'Heading\nFirst one. Second\none!\nA list item';
	// Three blocks: a heading, a paragraph, a list item.
	const blocks: Span[] = [
		{ start: 0, end: 7 },
		{ start: 8, end: 30 },
		{ start: 31, end: 42 }
	];
	const slices = (spans: Span[]) => spans.map((s) => text.slice(s.start, s.end));

	it('splits each block into sentences, a soft line break being no break', () => {
		expect(slices(sentences(text, blocks))).toEqual([
			'Heading',
			'First one.',
			'Second\none!',
			'A list item'
		]);
	});

	it('lists the words', () => {
		const line = 'It is, as ever, 42.';
		expect(words(line).map((s) => line.slice(s.start, s.end))).toEqual([
			'It',
			'is',
			'as',
			'ever',
			'42'
		]);
	});

	const ws = words(text);
	const sel = (quote: string): Span => {
		const start = text.indexOf(quote);
		return { start, end: start + quote.length };
	};
	const q = (s: Span) => text.slice(s.start, s.end);

	it('moves the start of a choice by a word, never past its end', () => {
		expect(q(moveStart(ws, sel('Second\none!'), -1))).toBe('one. Second\none!');
		expect(q(moveStart(ws, sel('First one.'), 1))).toBe('one.');
		expect(q(moveStart(ws, sel('one.'), 1))).toBe('one.');
	});

	it('moves the end of a choice by a word, never before its start', () => {
		expect(q(moveEnd(ws, sel('First'), 1))).toBe('First one');
		expect(q(moveEnd(ws, sel('First one.'), -1))).toBe('First');
		expect(q(moveEnd(ws, sel('First'), -1))).toBe('First');
	});
});

describe('anchorOf', () => {
	const good = { exact: 'words', prefix: 'the ', suffix: ' here', start: 4 };

	it('accepts an anchor and returns only its fields', () => {
		expect(anchorOf({ ...good, extra: 1 })).toEqual(good);
	});

	it('refuses what is not one', () => {
		expect(anchorOf(null)).toBeNull();
		expect(anchorOf({ ...good, exact: '' })).toBeNull();
		expect(anchorOf({ ...good, exact: ' padded' })).toBeNull();
		expect(anchorOf({ ...good, exact: 'x'.repeat(5000) })).toBeNull();
		expect(anchorOf({ ...good, prefix: 'x'.repeat(CONTEXT + 1) })).toBeNull();
		expect(anchorOf({ ...good, start: -1 })).toBeNull();
		expect(anchorOf({ ...good, start: 1.5 })).toBeNull();
		expect(anchorOf({ ...good, suffix: 3 })).toBeNull();
	});
});

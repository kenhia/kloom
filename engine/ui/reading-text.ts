/**
 * The reading pane's text, for annotations (docs/design.md §Annotations):
 * its text nodes laid end to end, so `engine/anchor.ts` can work on a string
 * and the page can turn the offsets it answers with back into DOM ranges and
 * highlights. Browser only.
 *
 * Inlined charts are left out: their labels are drawing, not reading.
 */

import type { Span } from '../anchor';

/** One text node and where it starts in the text. */
interface Piece {
	node: Text;
	start: number;
}

export interface ReadingText {
	text: string;
	pieces: Piece[];
	/** Runs of text in one paragraph, heading, list item or cell. */
	blocks: Span[];
}

const BLOCK = 'p, li, h1, h2, h3, h4, h5, h6, td, th, blockquote, pre, figcaption, dd, dt';
const SKIP = 'svg, style, script, .annotation-ref';

export function readingText(root: HTMLElement): ReadingText {
	const pieces: Piece[] = [];
	const blocks: Span[] = [];
	let text = '';
	let block: Element | null | undefined;
	const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, {
		acceptNode: (n) =>
			n.parentElement?.closest(SKIP) ? NodeFilter.FILTER_REJECT : NodeFilter.FILTER_ACCEPT
	});
	for (let n = walker.nextNode() as Text | null; n; n = walker.nextNode() as Text | null) {
		const start = text.length;
		pieces.push({ node: n, start });
		text += n.data;
		const b = n.parentElement?.closest(BLOCK);
		if (!n.data.trim()) continue;
		if (b && b === block) blocks[blocks.length - 1].end = text.length;
		else blocks.push({ start, end: text.length });
		block = b;
	}
	return { text, pieces, blocks };
}

/** Where a DOM range falls in the text; null when it is not in it. */
export function spanOf(t: ReadingText, range: Range): Span | null {
	let start = -1;
	let end = -1;
	for (const { node, start: at } of t.pieces) {
		if (!range.intersectsNode(node)) continue;
		if (start < 0) start = at + (node === range.startContainer ? range.startOffset : 0);
		end = at + (node === range.endContainer ? range.endOffset : node.length);
	}
	return start < 0 || end <= start ? null : { start, end };
}

/** The DOM range for a span of the text. */
export function rangeOf(t: ReadingText, span: Span): Range | null {
	const at = (offset: number, end: boolean) => {
		const p = t.pieces.findLast((p) => (end ? p.start < offset : p.start <= offset));
		return p && { node: p.node, offset: Math.min(offset - p.start, p.node.length) };
	};
	const s = at(span.start, false);
	const e = at(span.end, true);
	if (!s || !e) return null;
	const range = document.createRange();
	range.setStart(s.node, s.offset);
	range.setEnd(e.node, e.offset);
	return range;
}

/**
 * Wrap a span of the text in `<mark>`s, one per text node it touches, and
 * return them. Whitespace between blocks is left alone, and so is any text
 * directly in `root`: the page owns those nodes.
 */
export function highlight(root: HTMLElement, span: Span, id: string): HTMLElement[] {
	const marks: HTMLElement[] = [];
	for (const { node, start } of readingText(root).pieces) {
		const from = Math.max(span.start, start) - start;
		const to = Math.min(span.end, start + node.length) - start;
		if (to <= from || !node.data.slice(from, to).trim() || node.parentNode === root) continue;
		const part = node.splitText(from);
		part.splitText(to - from);
		const mark = document.createElement('mark');
		mark.className = 'annotation';
		mark.dataset.note = id;
		part.replaceWith(mark);
		mark.append(part);
		marks.push(mark);
	}
	return marks;
}

/** Take every highlight and annotation button out again, leaving the text as it was. */
export function clearHighlights(root: HTMLElement) {
	for (const ref of root.querySelectorAll('.annotation-ref')) ref.remove();
	for (const mark of root.querySelectorAll('mark.annotation')) {
		const parent = mark.parentNode!;
		mark.replaceWith(...mark.childNodes);
		parent.normalize();
	}
}

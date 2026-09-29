import { Marked } from 'marked';
import { NAME_HREF } from './names';

const escape = (s: string) =>
	s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');

const NAMED: Record<string, string> = { colon: ':', tab: '\t', newline: '\n' };

/**
 * Whether a link or image URL may be emitted: http(s), or no scheme at all
 * (relative paths, in-page anchors). The scheme is read the way a browser
 * would read it, after entities are decoded and the ASCII controls and
 * whitespace it ignores are removed, so `java\tscript:` is still javascript.
 */
export function safeUrl(url: string): boolean {
	const normal = url
		.replace(/&#x([0-9a-f]+);?/gi, (_, h) => String.fromCodePoint(parseInt(h, 16)))
		.replace(/&#(\d+);?/g, (_, d) => String.fromCodePoint(Number(d)))
		.replace(/&(colon|tab|newline);/gi, (_, n: string) => NAMED[n.toLowerCase()])
		// eslint-disable-next-line no-control-regex
		.replace(/[\u0000-\u0020\u007f]/g, '');
	const scheme = /^([a-z][\w+.-]*):/i.exec(normal)?.[1].toLowerCase();
	return !scheme || scheme === 'http' || scheme === 'https';
}

/** Where a reading's image lives and what credit, if any, sits beside it. */
export interface ResolvedImage {
	src: string;
	credit?: string;
	/**
	 * Sanitised SVG markup to inline in place of an `<img>`, so a chart
	 * takes the page's palette (docs/design.md §Charts). The caller must have
	 * run it through the allowlist sanitiser.
	 */
	svg?: string;
}

/** Maps an image reference in the markdown to its served URL, or null. */
export type ImageResolver = (href: string) => ResolvedImage | null;

export interface RenderOptions {
	/**
	 * Resolves image references. Without one, an image keeps its own URL
	 * (subject to `safeUrl`); with one, an unresolved image falls back to its
	 * alt text.
	 */
	image?: ImageResolver;
}

/**
 * A name's mark (docs/design.md §Connections): a button that opens the name's
 * card, never a navigation link. The reading's own words are its label.
 */
const nameButton = (id: string, label: string) =>
	`<button type="button" class="name" data-name="${escape(id)}" aria-haspopup="dialog" aria-expanded="false">${label}</button>`;

const img = (src: string, text: string, title: string | null | undefined) =>
	`<img src="${escape(src)}" alt="${escape(text)}"${title ? ` title="${escape(title)}"` : ''}>`;

/**
 * Markdown for the reading pane. Content will be written by a model, so raw
 * HTML is shown as text rather than passed through, and links and images go
 * only to http(s), in-page anchors or relative paths.
 */
function markdown(options: RenderOptions) {
	// Only a name's first mention in a reading is marked; a later mark is
	// its words alone (validation warns about it).
	const named = new Set<string>();
	return new Marked({
		gfm: true,
		renderer: {
			html: ({ text }) => escape(text),
			// The frame's title is the pane's h2, so the reading nests under it.
			heading({ tokens, depth }) {
				const h = Math.min(depth + 1, 6);
				return `<h${h}>${this.parser.parseInline(tokens)}</h${h}>\n`;
			},
			// A scheme other than http(s) (javascript:, data:, …) drops the link,
			// keeping its text. `kloom:e/<id>` marks a name.
			link({ href, title, tokens }) {
				const label = this.parser.parseInline(tokens);
				const name = NAME_HREF.exec(href)?.[1];
				if (name) {
					if (named.has(name)) return label;
					named.add(name);
					return nameButton(name, label);
				}
				if (!safeUrl(href)) return label;
				const t = title ? ` title="${escape(title)}"` : '';
				const external = /^https?:/i.test(href) ? ' rel="noopener noreferrer"' : '';
				return `<a href="${escape(href)}"${t}${external}>${label}</a>`;
			},
			// Images follow the same rule, falling back to their alt text. A
			// licence that needs attribution gets its credit beside the image.
			image({ href, title, text }) {
				if (!options.image) return safeUrl(href) ? img(href, text, title) : escape(text);
				const found = options.image(href);
				if (!found || !safeUrl(found.src)) return escape(text);
				const credit = found.credit ? `<span class="credit">${escape(found.credit)}</span>` : '';
				// An inlined drawing is named by the reading's alt text, as an <img> would be.
				if (found.svg !== undefined)
					return `<span class="figure chart" role="img" aria-label="${escape(text)}"${title ? ` title="${escape(title)}"` : ''}>${found.svg}</span>${credit}`;
				if (!credit) return img(found.src, text, title);
				return `<span class="figure">${img(found.src, text, title)}${credit}</span>`;
			}
		}
	});
}

const plain = markdown({});

/** A reading as HTML. Each call renders afresh, so first mentions are counted per reading. */
export function renderMarkdown(source: string, options: RenderOptions = {}): string {
	return markdown(options).parse(source, { async: false });
}

/** Every name a reading marks, in order, repeats included, for validation and the graph. */
export function nameRefs(source: string): string[] {
	const refs: string[] = [];
	plain.walkTokens(plain.lexer(source), (t) => {
		const id = t.type === 'link' ? NAME_HREF.exec(t.href)?.[1] : undefined;
		if (id) refs.push(id);
	});
	return refs;
}

/** Every link in a reading that uses the `kloom:` scheme, for validation. */
export function kloomRefs(source: string): string[] {
	const refs: string[] = [];
	plain.walkTokens(plain.lexer(source), (t) => {
		if ((t.type === 'link' || t.type === 'image') && /^\s*kloom:/i.test(t.href)) refs.push(t.href);
	});
	return refs;
}

/** Every image reference in a reading, in order, for validation. */
export function imageRefs(source: string): string[] {
	const refs: string[] = [];
	plain.walkTokens(plain.lexer(source), (t) => {
		if (t.type === 'image') refs.push(t.href);
	});
	return refs;
}

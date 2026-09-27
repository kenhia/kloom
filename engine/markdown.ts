import { Marked } from 'marked';

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

/**
 * Markdown for the reading pane. Content will be written by a model, so raw
 * HTML is shown as text rather than passed through, and links and images go
 * only to http(s), in-page anchors or relative paths.
 */
const marked = new Marked({
	gfm: true,
	renderer: {
		html: ({ text }) => escape(text),
		// A scheme other than http(s) (javascript:, data:, …) drops the link,
		// keeping its text.
		link({ href, title, tokens }) {
			const label = this.parser.parseInline(tokens);
			if (!safeUrl(href)) return label;
			const t = title ? ` title="${escape(title)}"` : '';
			const external = /^https?:/i.test(href) ? ' rel="noopener noreferrer"' : '';
			return `<a href="${escape(href)}"${t}${external}>${label}</a>`;
		},
		// Images follow the same rule, falling back to their alt text.
		image({ href, title, text }) {
			if (!safeUrl(href)) return escape(text);
			const t = title ? ` title="${escape(title)}"` : '';
			return `<img src="${escape(href)}" alt="${escape(text)}"${t}>`;
		}
	}
});

export function renderMarkdown(source: string): string {
	return marked.parse(source, { async: false });
}

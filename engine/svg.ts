/**
 * The illustration sanitiser (docs/design.md §Illustrations, korg 3365).
 *
 * An illustration is inlined into the page so it can draw itself on, and
 * grow writes illustrations with a model, so what reaches the page must be a
 * line drawing and nothing more. This is an allowlist, not a filter: the
 * source is parsed as XML, every element and attribute must be on a list,
 * and the markup that is inlined is re-serialised from the parse. Nothing the
 * author wrote reaches the page as text we did not emit ourselves, so a
 * spelling a browser would read differently from this parser (an entity, a
 * stray slash, odd case) has nowhere to hide.
 *
 * Hand-written and model-written drawings take the same path: validation
 * reports the problems and the loader inlines the re-serialised markup.
 */

/** Elements a line drawing may use. SVG is case-sensitive, and so is this. */
const ELEMENTS = new Set([
	'svg',
	'g',
	'defs',
	'title',
	'desc',
	'path',
	'line',
	'polyline',
	'polygon',
	'rect',
	'circle',
	'ellipse',
	'text',
	'tspan',
	'clipPath',
	'marker',
	'linearGradient',
	'radialGradient',
	'stop'
]);

/** Geometry, presentation and accessibility attributes; nothing that loads or runs. */
const ATTRIBUTES = new Set([
	// the root
	'xmlns',
	'viewBox',
	'preserveAspectRatio',
	'width',
	'height',
	'version',
	// geometry
	'd',
	'x',
	'y',
	'x1',
	'y1',
	'x2',
	'y2',
	'cx',
	'cy',
	'r',
	'rx',
	'ry',
	'fx',
	'fy',
	'dx',
	'dy',
	'points',
	'transform',
	'pathLength',
	'rotate',
	'textLength',
	'lengthAdjust',
	'offset',
	'gradientUnits',
	'gradientTransform',
	'spreadMethod',
	'clipPathUnits',
	'markerWidth',
	'markerHeight',
	'markerUnits',
	'refX',
	'refY',
	'orient',
	// presentation
	'fill',
	'fill-opacity',
	'fill-rule',
	'stroke',
	'stroke-width',
	'stroke-opacity',
	'stroke-linecap',
	'stroke-linejoin',
	'stroke-dasharray',
	'stroke-dashoffset',
	'stroke-miterlimit',
	'opacity',
	'color',
	'stop-color',
	'stop-opacity',
	'vector-effect',
	'clip-path',
	'clip-rule',
	'marker-start',
	'marker-mid',
	'marker-end',
	'visibility',
	'display',
	'font-family',
	'font-size',
	'font-style',
	'font-weight',
	'letter-spacing',
	'word-spacing',
	'text-anchor',
	'dominant-baseline',
	'alignment-baseline',
	'baseline-shift',
	// identity and accessibility
	'id',
	'class',
	'role',
	'lang',
	'aria-hidden',
	'aria-label',
	'aria-labelledby',
	'aria-describedby'
]);

const SVG_NS = 'http://www.w3.org/2000/svg';
const NAME = /^[A-Za-z_][\w.:-]*/;
const ID = /^[A-Za-z][\w-]*$/;

interface Element {
	name: string;
	attributes: [string, string][];
	children: Node[];
}
type Node = Element | string;

export interface SanitisedSvg {
	/** The drawing, re-serialised from the parse; null when there are problems. */
	svg: string | null;
	/** Everything wrong, in document order. Empty means the drawing is safe to inline. */
	problems: string[];
}

const PREDEFINED: Record<string, string> = { lt: '<', gt: '>', amp: '&', quot: '"', apos: "'" };

/** Decode XML character references; null names the first one XML does not define. */
function decode(raw: string, fail: (what: string) => void): string {
	return raw.replace(/&([^;\s&<]*);?/g, (whole, ref: string) => {
		if (!whole.endsWith(';')) {
			fail('a bare "&" (write &amp;)');
			return '';
		}
		const hex = /^#x([0-9a-f]{1,6})$/i.exec(ref);
		const dec = /^#(\d{1,7})$/.exec(ref);
		const code = hex ? parseInt(hex[1], 16) : dec ? Number(dec[1]) : null;
		if (code !== null) {
			if (code === 0 || code > 0x10ffff) {
				fail(`an invalid character reference &${ref};`);
				return '';
			}
			return String.fromCodePoint(code);
		}
		if (ref in PREDEFINED) return PREDEFINED[ref];
		fail(`an undefined entity &${ref};`);
		return '';
	});
}

const escapeText = (s: string) =>
	s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const escapeAttr = (s: string) => escapeText(s).replace(/"/g, '&quot;');

/** Parse XML into elements and text. Comments and the XML declaration are dropped. */
function parse(source: string, fail: (what: string) => void): Element | null {
	let i = 0;
	const root: Element = { name: '#root', attributes: [], children: [] };
	const stack: Element[] = [root];
	const at = () => `at offset ${i}`;
	const bad = (what: string): null => {
		fail(what);
		return null;
	};

	while (i < source.length) {
		const top = stack[stack.length - 1];
		if (source.startsWith('<!--', i)) {
			const end = source.indexOf('-->', i + 4);
			if (end < 0) return bad(`an unclosed comment ${at()}`);
			i = end + 3;
		} else if (source.startsWith('<?', i)) {
			const end = source.indexOf('?>', i);
			if (end < 0 || i !== source.search(/\S/) || !/^<\?xml[\s?]/.test(source.slice(i)))
				return bad(`a processing instruction ${at()}`);
			i = end + 2;
		} else if (source.startsWith('<!', i)) {
			return bad(`a DOCTYPE or CDATA section ${at()}`);
		} else if (source.startsWith('</', i)) {
			const m = /^<\/([A-Za-z_][\w.:-]*)\s*>/.exec(source.slice(i));
			if (!m) return bad(`a malformed end tag ${at()}`);
			if (stack.length === 1 || top.name !== m[1])
				return bad(`</${m[1]}> does not close an open <${m[1]}> ${at()}`);
			stack.pop();
			i += m[0].length;
		} else if (source[i] === '<') {
			i++;
			const name = NAME.exec(source.slice(i))?.[0];
			if (!name) return bad(`a malformed start tag ${at()}`);
			i += name.length;
			const el: Element = { name, attributes: [], children: [] };
			for (;;) {
				const space = /^\s*/.exec(source.slice(i))![0];
				i += space.length;
				if (source.startsWith('/>', i)) {
					i += 2;
					top.children.push(el);
					break;
				}
				if (source[i] === '>') {
					i++;
					top.children.push(el);
					stack.push(el);
					break;
				}
				// An attribute needs whitespace before it: `<g/onclick=…>` is not one.
				const attr = /^([A-Za-z_:][\w.:-]*)\s*=\s*(?:"([^"<]*)"|'([^'<]*)')/.exec(source.slice(i));
				if (!space || !attr) return bad(`a malformed attribute in <${name}> ${at()}`);
				const [whole, key, dq, sq] = attr;
				if (el.attributes.some(([k]) => k === key))
					return bad(`a repeated attribute ${key} in <${name}>`);
				el.attributes.push([key, decode(dq ?? sq, fail)]);
				i += whole.length;
			}
		} else {
			const end = source.indexOf('<', i);
			const raw = source.slice(i, end < 0 ? undefined : end);
			i += raw.length;
			const text = decode(raw, fail);
			if (stack.length > 1) top.children.push(text);
			else if (text.trim()) return bad('text outside the <svg> element');
		}
	}
	if (stack.length > 1) return bad(`<${stack[stack.length - 1].name}> is never closed`);
	const elements = root.children.filter((c): c is Element => typeof c !== 'string');
	if (elements.length !== 1 || elements[0].name !== 'svg')
		return bad('an illustration is exactly one <svg> element');
	return elements[0];
}

/** What is wrong with an attribute's value, or null. */
function valueProblem(el: string, key: string, value: string): string | null {
	if (key === 'xmlns') return value === SVG_NS ? null : `xmlns must be ${SVG_NS}`;
	if (key === 'id' && !ID.test(value)) return `id "${value}" must be a plain name`;
	// A paint or marker may point into the drawing, and nowhere else.
	for (const m of value.matchAll(/url\s*\(([^)]*)\)?/gi))
		if (!/^\s*['"]?#[A-Za-z][\w-]*['"]?\s*$/.test(m[1] ?? ''))
			return `<${el}> ${key} may only use url(#id) inside the drawing`;
	// eslint-disable-next-line no-control-regex
	if (/[\u0000-\u0008\u000b\u000c\u000e-\u001f]/.test(value))
		return `<${el}> ${key} contains a control character`;
	return null;
}

function check(el: Element, fail: (what: string) => void) {
	if (!ELEMENTS.has(el.name)) fail(`<${el.name}> is not allowed in an illustration`);
	for (const [key, value] of el.attributes) {
		if (!ATTRIBUTES.has(key)) fail(`<${el.name}> attribute ${key} is not allowed`);
		else {
			const problem = valueProblem(el.name, key, value);
			if (problem) fail(problem);
		}
	}
	for (const c of el.children) if (typeof c !== 'string') check(c, fail);
}

type Rewrite = (key: string, value: string) => string;

function serialise(el: Element, rewrite: Rewrite): string {
	const attrs = el.attributes.map(([k, v]) => ` ${k}="${escapeAttr(rewrite(k, v))}"`).join('');
	if (el.children.length === 0) return `<${el.name}${attrs}/>`;
	const inner = el.children.map((c) =>
		typeof c === 'string' ? escapeText(c) : serialise(c, rewrite)
	);
	return `<${el.name}${attrs}>${inner.join('')}</${el.name}>`;
}

export interface InlineOptions {
	/**
	 * Prefixed to every id and to every reference to one (`url(#id)`,
	 * `aria-labelledby`), so two drawings inlined in one page cannot collide.
	 */
	idPrefix?: string;
	/**
	 * Hide the drawing from assistive technology: the root gets
	 * `aria-hidden="true"` and loses its role and labels, because the page
	 * names it (a chart's wrapper carries the reading's alt text).
	 */
	decorative?: boolean;
}

const REFERENCES = new Set(['aria-labelledby', 'aria-describedby']);

/**
 * Check an SVG against the allowlist, and return the markup to inline: the
 * parse, re-serialised. Problems are collected rather than thrown, so an
 * author (or a grow job) sees all of them at once.
 */
export function sanitiseSvg(source: string, options: InlineOptions = {}): SanitisedSvg {
	const problems: string[] = [];
	const fail = (what: string) => {
		if (!problems.includes(what)) problems.push(what);
	};
	const root = parse(source, fail);
	if (root) check(root, fail);
	if (!root || problems.length) return { svg: null, problems };

	const prefix = options.idPrefix ?? '';
	if (options.decorative) {
		root.attributes = root.attributes.filter(([k]) => k !== 'role' && !k.startsWith('aria-'));
		root.attributes.push(['aria-hidden', 'true']);
	}
	const rewrite: Rewrite = !prefix
		? (_, v) => v
		: (key, value) =>
				key === 'id'
					? prefix + value
					: REFERENCES.has(key)
						? value
								.split(/\s+/)
								.filter(Boolean)
								.map((id) => prefix + id)
								.join(' ')
						: value.replace(/url\(\s*(['"]?)#/gi, `url($1#${prefix}`);
	return { svg: serialise(root, rewrite), problems };
}

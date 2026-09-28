import { readdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';
import { describe, expect, it } from 'vitest';
import { sanitiseSvg } from './svg';

const frames = join(import.meta.dirname, '..', 'subjects', 'western-civ', 'frames');
const curated = readdirSync(frames).flatMap((dir) =>
	readdirSync(join(frames, dir))
		.filter((f) => f.endsWith('.svg'))
		.map((f) => [`${dir}/${f}`, readFileSync(join(frames, dir, f), 'utf8')] as const)
);

describe('the illustration sanitiser', () => {
	it.each(curated)('passes the curated %s, and its output is stable', (_, svg) => {
		const once = sanitiseSvg(svg);
		expect(once.problems).toEqual([]);
		// Re-serialising the output changes nothing: the page gets a fixed point.
		expect(sanitiseSvg(once.svg!).svg).toBe(once.svg);
		// Every drawn path keeps what the draw-on animation needs.
		expect(once.svg!.match(/<path /g)?.length).toBe(svg.match(/<path /g)?.length);
	});

	it('keeps the drawing and drops comments and the XML declaration', () => {
		const { svg, problems } = sanitiseSvg(
			'<?xml version="1.0"?>\n<!-- drawn by hand --><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 4 3"><g stroke="currentColor"><path pathLength="1" d="M0 0L4 3"/><text x="1" y="2">A &amp; B &lt; C</text></g></svg>'
		);
		expect(problems).toEqual([]);
		expect(svg).toBe(
			'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 4 3"><g stroke="currentColor"><path pathLength="1" d="M0 0L4 3"/><text x="1" y="2">A &amp; B &lt; C</text></g></svg>'
		);
	});

	it('re-escapes what an entity spelled, so it stays text', () => {
		const { svg } = sanitiseSvg('<svg><text>&#60;script&#62;x&#60;/script&#62;</text></svg>');
		expect(svg).toBe('<svg><text>&lt;script&gt;x&lt;/script&gt;</text></svg>');
	});

	it.each([
		['a script', '<svg><script>alert(1)</script></svg>', '<script> is not allowed'],
		['a namespaced script', '<svg><svg:script>x</svg:script></svg>', '<svg:script> is not'],
		['a capitalised script', '<svg><Script>x</Script></svg>', '<Script> is not allowed'],
		['foreign content', '<svg><foreignObject/></svg>', '<foreignObject> is not allowed'],
		['an image', '<svg><image href="https://x.test/a.png"/></svg>', '<image> is not allowed'],
		['an animation', '<svg><set attributeName="x" to="1"/></svg>', '<set> is not allowed'],
		['an event handler', '<svg><path onclick="x()"/></svg>', 'attribute onclick is not'],
		['a style attribute', '<svg><path style="fill:url(//x.test)"/></svg>', 'attribute style'],
		['an xlink href', '<svg><path xlink:href="#a"/></svg>', 'attribute xlink:href is not'],
		['an external paint', '<svg><path fill="url(https://x.test/#a)"/></svg>', 'url(#id)'],
		['an entity-spelled paint', '<svg><path fill="&#117;rl(//x.test)"/></svg>', 'url(#id)'],
		['a foreign namespace', '<svg xmlns="http://www.w3.org/1999/xhtml"></svg>', 'xmlns must'],
		['a DOCTYPE', '<!DOCTYPE svg [<!ENTITY a "b">]><svg/>', 'DOCTYPE'],
		['CDATA', '<svg><text><![CDATA[<script>]]></text></svg>', 'CDATA'],
		['an undefined entity', '<svg><text>&nbsp;</text></svg>', 'undefined entity'],
		['a bare ampersand', '<svg><text>a & b</text></svg>', 'bare "&"'],
		['an unquoted attribute', '<svg><path d=M0/></svg>', 'malformed attribute'],
		['a slash before an attribute', '<svg><g/onclick="x()"></g></svg>', 'malformed attribute'],
		['a repeated attribute', '<svg><path d="M0" d="M1"/></svg>', 'repeated attribute'],
		['an unclosed element', '<svg><g></svg>', 'does not close'],
		['a stray end tag', '<svg></g></svg>', 'does not close'],
		['two roots', '<svg/><svg/>', 'exactly one <svg>'],
		['a non-svg root', '<html></html>', 'exactly one <svg>'],
		['text outside', 'hello<svg/>', 'text outside'],
		['a late processing instruction', '<svg><?php x ?></svg>', 'processing instruction'],
		['an odd id', '<svg><g id="a b"/></svg>', 'must be a plain name']
	])('refuses %s', (_, source, problem) => {
		const result = sanitiseSvg(source);
		expect(result.svg).toBeNull();
		expect(result.problems.join('\n')).toContain(problem);
	});

	it('allows an in-drawing url(#id) reference', () => {
		const { problems } = sanitiseSvg(
			'<svg><defs><marker id="tip"><path d="M0 0"/></marker></defs><path marker-end="url(#tip)" d="M0 0"/></svg>'
		);
		expect(problems).toEqual([]);
	});

	it('reports every problem in one pass', () => {
		expect(sanitiseSvg('<svg onload="x"><script/><path style="a"/></svg>').problems).toEqual([
			'<svg> attribute onload is not allowed',
			'<script> is not allowed in an illustration',
			'<path> attribute style is not allowed'
		]);
	});
});

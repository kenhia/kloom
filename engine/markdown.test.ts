import { describe, expect, it } from 'vitest';
import { imageRefs, renderMarkdown } from './markdown';

describe('renderMarkdown', () => {
	it('renders ordinary markdown', () => {
		expect(renderMarkdown('Some **bold** text.')).toBe('<p>Some <strong>bold</strong> text.</p>\n');
	});

	it('shows raw HTML as text instead of passing it through', () => {
		const html = renderMarkdown('<script>alert(1)</script>\n\nHi <img src=x onerror=alert(1)>');
		expect(html).not.toMatch(/<script|<img/);
		expect(html).toContain('&lt;script&gt;');
	});

	it('keeps http(s) links and drops other schemes', () => {
		expect(renderMarkdown('[a](https://example.org/)')).toContain(
			'<a href="https://example.org/" rel="noopener noreferrer">a</a>'
		);
		expect(renderMarkdown('[b](javascript:alert(1))')).toBe('<p>b</p>\n');
		expect(renderMarkdown('[c](#sources)')).toContain('<a href="#sources">c</a>');
	});

	// Browsers strip ASCII tab/newline from URLs and ignore leading controls,
	// so a scheme split by them still runs (review on korg 3362).
	it.each([
		['a tab', '[x](<java\tscript:alert(1)>)'],
		['a newline', '[x](<java\nscript:alert(1)>)'],
		['a leading control character', '[x](<\u0001javascript:alert(1)>)'],
		['an entity', '[x](java&#x73;cript:alert(1))'],
		['upper case', '[x](JAVASCRIPT:alert(1))']
	])('emits no javascript: link hidden by %s', (_, md) => {
		expect(renderMarkdown(md)).not.toMatch(/href=|src=/);
	});

	it('applies the same scheme rule to images', () => {
		expect(renderMarkdown('![alt](javascript:alert(1))')).toBe('<p>alt</p>\n');
		expect(renderMarkdown('![a map](data:image/svg+xml,<svg/>)')).not.toContain('<img');
		expect(renderMarkdown('![a map](https://example.org/m.png)')).toContain(
			'<img src="https://example.org/m.png" alt="a map">'
		);
		expect(renderMarkdown('![a map](map.png)')).toContain('<img src="map.png" alt="a map">');
	});

	// The frame's title is the pane's h2, so the reading's sections nest under it.
	it('sets reading headings one level below the frame title', () => {
		expect(renderMarkdown('# A\n\n## B\n\n###### C')).toBe('<h2>A</h2>\n<h3>B</h3>\n<h6>C</h6>\n');
	});

	it('resolves images through the resolver, with a credit when one is due', () => {
		const image = (href: string) =>
			href === 'pd.jpg'
				? { src: '/media/f/pd.jpg' }
				: href === 'by.jpg'
					? { src: '/media/f/by.jpg', credit: 'A <b>Person</b> / CC BY 4.0' }
					: null;
		expect(renderMarkdown('![one](pd.jpg)', { image })).toBe(
			'<p><img src="/media/f/pd.jpg" alt="one"></p>\n'
		);
		expect(renderMarkdown('![two](by.jpg)', { image })).toBe(
			'<p><span class="figure"><img src="/media/f/by.jpg" alt="two">' +
				'<span class="credit">A &lt;b&gt;Person&lt;/b&gt; / CC BY 4.0</span></span></p>\n'
		);
		expect(renderMarkdown('![three](gone.jpg)', { image })).toBe('<p>three</p>\n');
	});
});

describe('imageRefs', () => {
	it('lists every image, including ones inside other blocks', () => {
		expect(imageRefs('![a](one.png)\n\n> quote ![b](two.svg)\n\n- [![c](three.jpg)](x)')).toEqual([
			'one.png',
			'two.svg',
			'three.jpg'
		]);
	});
});

describe('markdown with images turned off', () => {
	it('shows an image’s alt text instead of fetching it', () => {
		const html = renderMarkdown('![a pixel](https://tracker.test/p.gif) text', {
			image: () => null
		});
		expect(html).not.toContain('<img');
		expect(html).toContain('a pixel text');
	});
});

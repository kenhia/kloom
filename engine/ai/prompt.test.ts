import { describe, expect, it } from 'vitest';
import { askPrompt, citedNumbers, references, webReferences } from './prompt';
import { context } from './fixture';

describe('the ask prompt', () => {
	it('numbers citations first, then only the sources no citation covers', () => {
		const refs = references(context.frame);
		expect(refs).toHaveLength(3);
		expect('citation' in refs[0] && refs[0].citation.title).toBe('Press article');
		expect('citation' in refs[1] && refs[1].citation.title).toBe('Ink');
		expect('source' in refs[2] && refs[2].source.title).toBe('A book with no link');
	});

	it('carries where the reader is, the reading, the numbered sources and the question', () => {
		const p = askPrompt({ ...context, trail: { id: 't', title: 'Ink trail' } }, '  Why?  ');
		expect(p).toContain('Subject: A Subject');
		expect(p).toContain('Renaissance › AD 1440 (on the side trail "Ink trail")');
		expect(p).toContain('Frame: We printed WORDS.');
		expect(p).toContain('Gutenberg built a press.');
		expect(p).toMatch(/\[1\] .*Press article/);
		expect(p).toContain('[3] A book with no link');
		expect(p.endsWith('--- Question ---\nWhy?')).toBe(true);
	});

	it('tells the model when a frame is dated, and says nothing when it is not', () => {
		const dated = { ...context, frame: { ...context.frame, asOf: '2026-09' } };
		expect(askPrompt(dated, 'Is this still true?')).toContain(
			'the state of things as of 2026-09; say so if the answer may have changed since.'
		);
		expect(askPrompt(context, 'Why?')).not.toContain('as of');
	});

	it('reads the reference numbers an answer marks, in first-use order and in range', () => {
		expect(citedNumbers('A [2]. B [1, 3]. C [2]. D [9]. E [1–2].', 3)).toEqual([2, 1, 3]);
		expect(citedNumbers('No markers; [x] and [] too.', 3)).toEqual([]);
		expect(citedNumbers('Range [1-3].', 3)).toEqual([1, 2, 3]);
	});

	it('reads the web pages a web answer lists, each once, http(s) only', () => {
		const answer = [
			'Svelte is at 5.57 [W1], per its site [W2].',
			'',
			'**Sources:**',
			'[W1] Svelte | endoflife.date — https://endoflife.date/svelte',
			'- [W2] Svelte - Wikipedia – <https://en.wikipedia.org/wiki/Svelte>',
			'[W1] Again — https://example.org/again',
			'[W3] A script — javascript:alert(1)'
		].join('\n');
		expect(webReferences(answer)).toEqual([
			{ n: 1, title: 'Svelte | endoflife.date', url: 'https://endoflife.date/svelte' },
			{ n: 2, title: 'Svelte - Wikipedia', url: 'https://en.wikipedia.org/wiki/Svelte' }
		]);
	});
});

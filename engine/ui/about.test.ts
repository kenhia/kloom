import { render } from 'svelte/server';
import { describe, expect, it } from 'vitest';
import type { SuggestOffer } from '../reader-data';
import type { LibraryStats } from '../stats';
import About from './About.svelte';

/** About's Suggest a subject (korg 3459): offered to a reader, absent with none. */
const stats = () => new Promise<LibraryStats>(() => {});
const offer: SuggestOffer = { list: async () => [], send: async () => ({ error: 'no' }) };

describe('About, suggesting a subject', () => {
	it('offers a reader a closed form, every field labelled', () => {
		const { body } = render(About, { props: { stats, suggest: offer } });
		expect(body).toMatch(/<button[^>]*aria-expanded="false"[^>]*>Suggest a subject…<\/button>/);
		expect(body).toMatch(/<form[^>]*hidden/);
		for (const label of ['Subject', 'What should it cover?', 'Why you would like it'])
			expect(body).toMatch(new RegExp(`<label for="[^"]+-(title|cover|why)"[^>]*>${label}`));
		expect(body).toMatch(/<input[^>]*required/);
		expect(body).toContain('role="status"');
	});

	it('has none of it with no reader', () => {
		const { body } = render(About, { props: { stats } });
		expect(body).not.toContain('Suggest a subject');
	});
});

import { render } from 'svelte/server';
import { describe, expect, it } from 'vitest';
import Page from './+page.svelte';

const page = (reader: { name: string; signedIn: boolean } | null) =>
	render(Page, { props: { data: { reader } } as never }).body;
const text = (html: string) => html.replace(/<[^>]*>/g, ' ').replace(/\s+/g, ' ');

// The Welcome and How-To page (korg 3502). Its words are Ken's to review;
// these hold the promises it must keep.
describe('the Welcome and How-To page', () => {
	it('greets a signed-in reader by display name, and says how to sign out', () => {
		const body = text(page({ name: 'Joel and Kathy', signedIn: true }));
		expect(body).toContain('Welcome, Joel and Kathy');
		expect(body).toContain('Sign out');
	});

	it('says plainly, before the box is ticked, who reads a note flagged for Agent review', () => {
		const body = text(page({ name: 'Joel and Kathy', signedIn: true }));
		expect(body).toMatch(/sends that note to Ken and to the AI agents Ken works with/i);
		expect(body).toContain('how mistakes in kloom get fixed');
		expect(body).toContain('private to your login');
	});

	it("is the first visit, handing off to the User's Guide (korg 3515)", () => {
		const html = page({ name: 'Joel and Kathy', signedIn: true });
		expect(html).toContain('href="/guide"');
		expect(text(html)).toContain("User's Guide");
	});

	it('never writes to one person: a login may be two', () => {
		const body = text(page({ name: 'Joel and Kathy', signedIn: true }));
		expect(body).toContain('If two of you share a login');
		expect(body).not.toMatch(/\b(he or she|his or her|yourself)\b/i);
	});

	it('has no sign-out section for a reader the tailnet names, and says what ask and grow are there', () => {
		const body = text(page({ name: 'Ken', signedIn: false }));
		expect(body).not.toContain('Signing in and out');
		expect(body).toContain('Asking and growing');
	});
});

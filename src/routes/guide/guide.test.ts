import { render } from 'svelte/server';
import { describe, expect, it } from 'vitest';
import { FIXED_KEYS, SHORTCUTS } from '$engine/keys';
import { darkBrightness, lightBrightness, readingColours, sceneColours } from '$engine/settings';
import Icon, { type IconName } from '$engine/ui/Icon.svelte';
import Page from './+page.svelte';

const page = (reader: { name: string; signedIn: boolean } | null) =>
	render(Page, { props: { data: { reader } } as never }).body;
const text = (html: string) =>
	html
		.replace(/<[^>]*>/g, ' ')
		.replace(/&#39;|&apos;/g, "'")
		.replace(/\s+/g, ' ');

/** Every icon the shell draws, each as a control in the shell has it. */
const ICONS: IconName[] = [
	'contents',
	'map',
	'bookmark',
	'bookmarks',
	'my-notes',
	'random',
	'anywhere',
	'home',
	'settings',
	'about'
];
const drawn = (name: IconName, filled = false) =>
	render(Icon, { props: { name, filled } }).body.replace(/<!--.*?-->/g, '');

// The User's Guide (korg 3515). Its words are Ken's to review; these hold
// the promises it must keep.
describe("the User's Guide", () => {
	const html = page({ name: 'Joel and Kathy', signedIn: true }).replace(/<!--.*?-->/g, '');
	const body = text(html);

	it('shows every icon as the shell draws it, from the same component', () => {
		for (const name of ICONS) expect(html, name).toContain(drawn(name));
		expect(html).toContain(drawn('bookmark', true));
	});

	it('covers every control, the map and notes', () => {
		for (const words of [
			'Random frame in this subject',
			'Random frame anywhere',
			'Contents',
			'Map',
			'Bookmark this frame',
			'Bookmarks',
			'My notes',
			'Home',
			'Settings',
			'About',
			'Back to…',
			'Trails from here',
			'Main story',
			'Show as list',
			'3D',
			'A solid line',
			'Annotate',
			'detached',
			'Export my reading data',
			'Suggest a subject',
			'Keyboard shortcuts…',
			'Phones and tablets'
		])
			expect(body, words).toContain(words);
	});

	it('explains the colors: both settings, every choice, both sliders and the sides colored apart', () => {
		for (const s of [sceneColours, readingColours, lightBrightness, darkBrightness]) {
			expect(body).toContain(s.label);
			if (s.control !== 'range')
				for (const c of s.choices) expect(body, c.label).toContain(c.label);
		}
		expect(body).toContain('As designed');
		expect(body).toContain('The two sides are colored apart.');
	});

	it('is written in American English, naming controls as they are labeled', () => {
		const labels = /Scene colours|Reading colours|Centre on it/g;
		const prose = body.replace(labels, '');
		expect(prose).not.toMatch(/colour|centre|neighbour|behaviour|favour|grey/i);
	});

	it('lists every shortcut at its letter out of the box, and the keys that never change', () => {
		for (const s of SHORTCUTS) expect(body).toContain(`${s.key.toUpperCase()} ${s.label}`);
		for (const k of FIXED_KEYS) expect(body).toContain(`${k.keys} ${k.does}`);
	});

	it('says plainly who reads a note flagged for Agent review, as Welcome does', () => {
		expect(body).toMatch(/sends that note to Ken and to the AI agents Ken works with/i);
		expect(body).toContain('A note you leave unticked stays private.');
		expect(body).toContain('private to your login');
	});

	it('links each part it lists to a heading on the page', () => {
		const links = [...html.matchAll(/href="#([a-z]+)"/g)].map((m) => m[1]);
		expect(links.length).toBeGreaterThan(10);
		for (const id of links) expect(html, id).toContain(`id="${id}"`);
	});

	it('never writes to one person: a login may be two', () => {
		expect(body).toContain('If two of you share a login');
		expect(body).not.toMatch(/\b(he or she|his or her|yourself)\b/i);
	});

	it('says how to sign out only to a signed-in reader, and what ask and grow are in the full edition', () => {
		expect(body).toContain('Signing in and out');
		const tailnet = text(page({ name: 'Ken', signedIn: false }));
		expect(tailnet).not.toContain('Signing in and out');
		expect(tailnet).toContain('Asking and growing');
	});
});

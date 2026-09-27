import { join } from 'node:path';
import { render } from 'svelte/server';
import { beforeAll, describe, expect, it } from 'vitest';
import { loadSubject } from '$engine/load';
import type { Subject } from '$engine/model';
import { paletteMode } from '$engine/settings';
import Shell from '$engine/ui/Shell.svelte';
import { UserSettings } from '$engine/user-settings.svelte';
import Page from './+page.svelte';

let subject: Subject;
beforeAll(async () => {
	subject = await loadSubject(join(import.meta.dirname, '..', '..', 'subjects', 'western-civ'));
});

const page = () => render(Page, { props: { data: { subject } } as never });

/** Visible text: tags dropped, spaces collapsed. */
const text = (html: string) => html.replace(/<[^>]*>/g, ' ').replace(/\s+/g, ' ');

describe('the shell', () => {
	it('titles the page after the subject', () => {
		expect(page().head).toContain('<title>kloom · The History of Western Civilization</title>');
	});

	it('opens on the first frame with the HUD filled in', () => {
		const body = text(page().body);
		expect(body).toContain('Myth');
		expect(body).toContain('01 / 16');
		expect(body).toContain('We stole FIRE.');
		expect(body).toContain('~1,000,000 years of kept fire');
	});

	it('has the three panes, labelled for assistive technology', () => {
		const { body } = page();
		expect(body).toContain('aria-label="Spine"');
		expect(body).toContain('aria-label="Narrative"');
		expect(body).toContain('aria-labelledby="ai-title"');
		expect(body).toMatch(/role="slider"[^>]*aria-valuenow="1"/);
		expect(body).toMatch(/aria-live="polite"/);
	});

	it('shows the reading with its sources', () => {
		const body = text(page().body);
		expect(body).toContain('Wonderwerk Cave');
		expect(body).toContain('Sources');
		expect(page().body).toContain('href="https://en.wikipedia.org/wiki/Prometheus"');
	});

	it('keeps citations in a closed control under Sources, in Chicago style', () => {
		const { body } = page();
		const citations = body.slice(body.indexOf('<details class="citations'));
		expect(citations).toMatch(/^<details class="citations[^"]*">/);
		expect(citations).not.toMatch(/^<details[^>]*\bopen\b/);
		expect(text(citations)).toContain('Citations (4)');
		expect(text(citations)).toContain(
			'Wikipedia contributors. “Prometheus.” Wikipedia, The Free Encyclopedia.'
		);
		expect(citations).toContain('<i>Theogony</i>');
		// Between the sources and the AI pane in document (and so tab) order.
		expect(body.indexOf('Sources')).toBeLessThan(body.indexOf('<details'));
		expect(body.indexOf('<details')).toBeLessThan(body.indexOf('id="ai-input"'));
	});

	it('paints the first frame’s palette', () => {
		expect(page().body).toContain(`--background: ${subject.palettes.night.background}`);
	});

	it('offers a Sync Narrative control and a placeholder AI input', () => {
		const body = text(page().body);
		expect(body).toContain('Sync Narrative');
		expect(body).toContain('Follow the spine');
		expect(page().body).toContain('id="ai-input"');
	});

	it('opens on a start screen, with the shell inert behind it', () => {
		const { body } = page();
		expect(body).toMatch(/role="dialog"[^>]*aria-modal="true"/);
		expect(text(body)).toContain('Begin Enter');
		expect(text(body)).toContain('Image credit');
		expect(body).toMatch(/class="shell[^"]*"[^>]*inert/);
		expect(body.indexOf('The History of Western Civilization</h2>')).toBeGreaterThan(0);
	});
});

describe('the settings control', () => {
	it('is a named disclosure button controlling a closed panel', () => {
		const { body } = page();
		const gear = body.match(/<button[^>]*class="gear[^"]*"[^>]*>[\s\S]*?<\/button>/)![0];
		expect(gear).toContain('type="button"');
		expect(gear).toContain('aria-expanded="false"');
		expect(text(gear).trim()).toBe('Settings');
		const panel = gear.match(/aria-controls="([^"]+)"/)![1];
		const at = body.match(new RegExp(`<div[^>]*id="${panel}"[^>]*>`))![0];
		expect(at).toContain('hidden');
		expect(at).toContain('data-own-keys');
		expect(at).toMatch(/role="group"/);
	});

	it('sits in the narrative toolbar, after Follow the spine, before the reading', () => {
		const { body } = page();
		expect(body.indexOf('Follow the spine')).toBeLessThan(body.indexOf('class="gear'));
		expect(body.indexOf('class="gear')).toBeLessThan(body.indexOf('<article'));
	});

	it('renders each setting as a labelled select, starting at its default', () => {
		const { body } = page();
		const id = body.match(/<select[^>]*id="([^"]+)"/)![1];
		expect(body).toMatch(new RegExp(`<label for="${id}"[^>]*>Palette</label>`));
		expect(body).toMatch(/<option value="mixed"[^>]*selected/);
		expect(text(body)).toContain('Dark');
		expect(text(body)).toContain('Light');
	});
});

describe('the palette mode', () => {
	const shell = (mode: string) => {
		const settings = new UserSettings([paletteMode], () => null);
		settings.set('palette', mode);
		return render(Shell, { props: { subject, settings } }).body;
	};

	it('paints the first frame (night) as itself in Mixed and Dark', () => {
		expect(shell('mixed')).toContain(`--background: ${subject.palettes.night.background}`);
		expect(shell('dark')).toContain(`--background: ${subject.palettes.night.background}`);
	});

	it('paints the first frame in its light counterpart in Light', () => {
		const body = shell('light');
		expect(body).toContain(`--background: ${subject.palettes.parchment.background}`);
		expect(body).toContain('color-scheme: light');
	});

	it('gives every palette of the subject a counterpart of the other scheme', () => {
		for (const p of Object.values(subject.palettes))
			expect(subject.palettes[p.counterpart!].scheme).not.toBe(p.scheme);
	});
});

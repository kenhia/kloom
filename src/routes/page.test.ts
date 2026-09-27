import { join } from 'node:path';
import { render } from 'svelte/server';
import { beforeAll, describe, expect, it } from 'vitest';
import { loadSubject } from '$engine/load';
import type { Subject } from '$engine/model';
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
		expect(body).toContain('Antiquity');
		expect(body).toContain('01 / 03');
		expect(body).toContain('c. 3200 BC');
		expect(body).toContain('We learned to WRITE.');
		expect(body).toContain('5,000+ years of written record');
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
		expect(body).toContain('cuneiform');
		expect(body).toContain('Sources');
		expect(page().body).toContain('href="https://en.wikipedia.org/wiki/Cuneiform"');
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
});

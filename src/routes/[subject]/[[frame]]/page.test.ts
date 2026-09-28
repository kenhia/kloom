import { join } from 'node:path';
import { render } from 'svelte/server';
import { beforeAll, describe, expect, it } from 'vitest';
import { loadSubject } from '$engine/load';
import type { Subject } from '$engine/model';
import { followSpine, paletteMode } from '$engine/settings';
import Shell from '$engine/ui/Shell.svelte';
import { UserSettings } from '$engine/user-settings.svelte';
import Page from './+page.svelte';

let subject: Subject;
beforeAll(async () => {
	subject = await loadSubject(
		join(import.meta.dirname, '..', '..', '..', '..', 'subjects', 'western-civ')
	);
});

const askModels = {
	choices: [
		{ value: 'claude-sonnet-5', label: 'Sonnet 5' },
		{ value: 'claude-opus-5-5', label: 'Opus 5.5' }
	],
	default: 'claude-sonnet-5'
};
const growModels = { ...askModels, default: 'claude-opus-5-5' };
const page = (askWeb = 'allow', grow: typeof growModels | null = growModels) =>
	render(Page, {
		props: { data: { subject, subjects, askModels, askWeb, growModels: grow } } as never
	});
const subjects = [
	{ id: 'ai', title: 'History and Current State of AI' },
	{ id: 'western-civ', title: 'The History of Western Civilization' }
];

/** Visible text: tags dropped, spaces collapsed. */
const text = (html: string) => html.replace(/<[^>]*>/g, ' ').replace(/\s+/g, ' ');

describe('the shell', () => {
	it('titles the page after the subject', () => {
		expect(page().head).toContain('<title>kloom · The History of Western Civilization</title>');
	});

	it('opens on the first frame with the HUD filled in', () => {
		const body = text(page().body);
		expect(body).toContain('Myth');
		// Derived, not written in: every grown frame lengthens the spine.
		const total = subject.spine.segments.reduce((n, s) => n + s.frames.length, 0);
		expect(body).toContain(`01 / ${String(total).padStart(2, '0')}`);
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
		// Derived from the key citations (sprint 008): the revision that was read.
		expect(page().body).toMatch(
			/<ol class="sources[^"]*">.*href="https:\/\/en\.wikipedia\.org\/w\/index\.php\?title=Prometheus&amp;oldid=\d+"/s
		);
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

	it('has no Sync Narrative button, says it follows the spine, and offers the Ask input', () => {
		const body = text(page().body);
		expect(body).not.toContain('Sync Narrative');
		expect(body).toContain('Following the spine.');
		expect(page().body).toMatch(/<textarea[^>]*id="ai-input"/);
		expect(page().body).toMatch(/<label for="ai-input"[^>]*>Ask a question about this frame</);
		expect(body).toContain('Send');
	});

	it('says in the hint bar that S, T and B act from the spine or narrative only', () => {
		const hint = text(page().body.match(/<p id="ai-hint"[\s\S]*?<\/p>/)![0]);
		expect(hint).toContain('S sync, T trail and B bookmark, in the spine or narrative');
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

describe('the subject chooser', () => {
	it('links every other subject from the start screen, and not this one', () => {
		const { body } = page();
		const nav = body.match(
			/<nav class="others[^"]*" aria-label="Other subjects">[\s\S]*?<\/nav>/
		)![0];
		expect(nav).toContain('href="/ai"');
		expect(text(nav)).toContain('History and Current State of AI');
		expect(nav).not.toContain('href="/western-civ"');
		// Inside the dialog, after Begin in tab order.
		expect(body.indexOf('class="begin')).toBeLessThan(body.indexOf('aria-label="Other subjects"'));
	});

	it('is absent when the app serves one subject', () => {
		const one = render(Page, {
			props: {
				data: { subject, subjects: [subjects[1]], askModels, askWeb: 'allow', growModels }
			} as never
		});
		expect(one.body).not.toContain('Other subjects');
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

	it('sits in the narrative toolbar, after the sync state, before the reading', () => {
		const { body } = page();
		expect(body.indexOf('id="sync-state"')).toBeLessThan(body.indexOf('class="gear'));
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

	it('offers the ask model as a drop-down of the app config’s models, Sonnet 5 by default', () => {
		const { body } = page();
		const id = /<label for="([^"]+)"[^>]*>Ask model<\/label>/.exec(body)![1];
		const select = body.slice(
			body.indexOf(`id="${id}"`),
			body.indexOf('</select>', body.indexOf(`id="${id}"`))
		);
		expect(select).toMatch(/<option value="claude-sonnet-5"[^>]*selected[^>]*>Sonnet 5</);
		expect(select).toMatch(/<option value="claude-opus-5-5"[^>]*>Opus 5.5</);
	});
});

describe('narrative following', () => {
	it('is a setting, on by default', () => {
		const { body } = page();
		const id = /<label for="([^"]+)"[^>]*>Narrative<\/label>/.exec(body)?.[1];
		expect(id).toBeDefined();
		expect(body).toMatch(
			new RegExp(`<select id="${id}"[^>]*>[\\s\\S]*?<option value="follow"[^>]*selected`)
		);
		expect(text(body)).toContain('Stays until S');
	});

	it('says the reading is in step when the reader has turned following off', () => {
		const settings = new UserSettings([followSpine], () => null);
		settings.set('followSpine', 'manual');
		expect(text(render(Shell, { props: { subject, settings } }).body)).toContain(
			'In step with the spine.'
		);
	});
});

describe('grow in the AI pane', () => {
	it('adds a Grow model drop-down, Opus 5.5 by default', () => {
		const { body } = page();
		const id = /<label for="([^"]+)"[^>]*>Grow model<\/label>/.exec(body)?.[1];
		expect(id).toBeDefined();
		expect(body).toMatch(
			new RegExp(`<select id="${id}"[^>]*>[\\s\\S]*?<option value="claude-opus-5-5"[^>]*selected`)
		);
	});

	it('offers the three verbs, a labelled request and Queue', () => {
		const { body } = page();
		expect(body).toContain('<label for="grow-verb" class="visually-hidden">What to grow</label>');
		expect(body).toContain(
			'<label for="grow-input" class="visually-hidden">What grow should write</label>'
		);
		for (const label of [
			'New frames on the main spine',
			'A side trail from this frame',
			'A new frame with its own trail'
		])
			expect(text(body)).toContain(label);
		expect(text(body)).toContain('Queue');
	});

	it('is absent when the app config has no grow', () => {
		const { body } = page('allow', null);
		expect(body).not.toContain('grow-verb');
		expect(body).not.toContain('Grow model');
	});
});

describe('the web switch in the AI pane', () => {
	const box = (body: string) => /<label class="web[^"]*"><input type="checkbox"([^>]*)>/.exec(body);

	it('offers "Include web", checked, when the app allows the web', () => {
		const { body } = page('allow');
		expect(text(body)).toContain('Include web');
		expect(box(body)?.[1]).toContain('checked');
	});

	it('offers it unchecked under offer, and not at all under deny', () => {
		expect(box(page('offer').body)?.[1]).not.toContain('checked');
		expect(text(page('deny').body)).not.toContain('Include web');
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

describe('reader data on the page', () => {
	const at = '2026-09-28T12:00:00.000Z';
	const title = 'The History of Western Civilization';
	const withReader = (readerData: object, frame: string | null = null) =>
		render(Page, {
			props: {
				data: {
					subject,
					subjects,
					askModels,
					askWeb: 'allow',
					growModels,
					frame,
					reader: { name: 'Ken' },
					readerData: { here: null, last: null, bookmarks: [], ...readerData }
				}
			} as never
		}).body;
	const mark = (frame: string, s = 'western-civ', subjectTitle = title) => ({
		subject: s,
		frame,
		label: `${frame} label`,
		at,
		subjectTitle
	});

	it('offers no bookmark controls without a reader', () => {
		expect(page().body).not.toContain('Bookmark this frame');
		expect(text(page().body)).not.toContain('Where you left off');
	});

	it('offers a bookmark toggle and a closed jump list to a reader, in the spine', () => {
		const body = withReader({});
		const toggle = body.match(/<button[^>]*aria-pressed="false"[^>]*>[\s\S]*?<\/button>/)![0];
		expect(text(toggle)).toContain('Bookmark this frame');
		expect(toggle).toContain('title="Bookmark this frame (B)"');
		const list = body.match(/<button[^>]*aria-expanded="false"[^>]*>[\s\S]*?Bookmarks \(0\)/)![0];
		const panel = list.match(/aria-controls="([^"]+)"/)![1];
		expect(body).toMatch(new RegExp(`<div[^>]*id="${panel}"[^>]*data-own-keys[^>]*hidden`));
		// Inside the spine pane, before the narrative.
		const spine = body.indexOf('aria-label="Spine"');
		expect(body.indexOf('Bookmark this frame')).toBeGreaterThan(spine);
		expect(body.indexOf('Bookmark this frame')).toBeLessThan(
			body.indexOf('aria-label="Narrative"')
		);
		expect(body).toContain('href="/api/reader/export"');
	});

	it('marks a bookmarked frame on the spine, in words as well as the mark', () => {
		const body = withReader({ bookmarks: [mark('prometheus'), mark('alexnet', 'ai', 'AI')] });
		expect(body).toMatch(/<button[^>]*aria-pressed="true"/);
		expect(body).toMatch(/role="slider"[^>]*aria-valuetext="[^"]*, bookmarked"/);
		expect(body).toMatch(/class="tick[^"]*\bmarked\b[^"]*"[^>]*title="[^"]*\(bookmarked\)"/);
		expect(body).toContain('Bookmarks (2)');
		// This subject's bookmark moves the shell; the other subject's is a link to it.
		expect(body).toContain('href="/western-civ/prometheus"');
		expect(body).toContain('href="/ai/alexnet"');
		expect(text(body)).toContain('Remove bookmark: alexnet label');
	});

	it('offers to continue in this subject and to go back to the last one elsewhere', () => {
		const body = withReader({
			here: mark('printing-press'),
			last: mark('alexnet', 'ai', 'History and Current State of AI')
		});
		const offers = body.match(
			/<ul class="resume[^"]*" aria-label="Where you left off">[\s\S]*?<\/ul>/
		)![0];
		expect(text(offers)).toContain('Continue where you were');
		expect(text(offers)).toContain(subject.frames['printing-press'].scene.headline);
		expect(text(offers)).toContain('Last read · History and Current State of AI');
		expect(offers).toContain('href="/ai/alexnet"');
		// Offered, not forced: Begin is still first.
		expect(body.indexOf('class="begin')).toBeLessThan(body.indexOf('class="resume'));
	});

	it('opens a deep link on its frame, past the start screen, and a trail frame on its trail', () => {
		const body = withReader({}, 'printing-press');
		expect(body).not.toMatch(/role="dialog"/);
		expect(text(body)).toContain(subject.frames['printing-press'].scene.headline);
		const trail = subject.trails[0];
		const inTrail = withReader({}, trail.spine.segments[0].frames[0]);
		expect(text(inTrail)).toContain('Main story');
		expect(text(inTrail)).toContain(trail.title);
	});
});

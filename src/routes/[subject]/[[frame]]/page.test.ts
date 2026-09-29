import { join } from 'node:path';
import { render } from 'svelte/server';
import { beforeAll, describe, expect, it } from 'vitest';
import { loadSubject } from '$engine/load';
import type { Subject } from '$engine/model';
import { followSpine, keySettings, layout, paletteMode } from '$engine/settings';
import type { Note, ReaderLayer } from '$engine/reader-data';
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
const text = (html: string) =>
	html
		.replace(/<[^>]*>/g, ' ')
		.replace(/&nbsp;/g, ' ')
		.replace(/\s+/g, ' ');
/** Visible text as it reads: a tag boundary before punctuation adds no space. */
const said = (html: string) => text(html).replace(/ ([,:.;])/g, '$1');

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
		expect(page().body).toMatch(/<button type="submit"[^>]*>\s*Ask\s*<\/button>/);
	});

	it('says in the hint bar that S, T and C act from the spine or narrative only', () => {
		const hint = said(page().body.match(/<p id="ai-hint"[\s\S]*?<\/p>/)![0]);
		expect(hint).toContain('S sync, T trail and C contents, in the spine or narrative');
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

describe('the subject list', () => {
	it('lists every subject as a listbox in the dialog, this one selected', () => {
		const { body } = page();
		const at = body.indexOf('<div class="subjects');
		const list = body.slice(at, body.indexOf('<h2', at));
		expect(list).toMatch(/^<div class="subjects[^"]*" role="listbox"/);
		expect(list).toContain('aria-label="Subjects"');
		expect(list).toContain('tabindex="0"');
		const options = [...list.matchAll(/<div id="([^"]+)" role="option" aria-selected="(\w+)"/g)];
		expect(options).toHaveLength(2);
		const chosen = options.find((o) => o[2] === 'true')!;
		expect(chosen[1]).toMatch(/-western-civ$/);
		expect(list).toContain(`aria-activedescendant="${chosen[1]}"`);
		expect(text(list)).toContain('History and Current State of AI');
		// Above the title, and the title is the selection's.
		expect(body.indexOf('role="listbox"')).toBeLessThan(
			body.indexOf('The History of Western Civilization</h2>')
		);
	});

	it('draws the selected subject’s illustrations in a ring around the loom', () => {
		const { body } = page();
		const ring = body.slice(body.indexOf('class="ring'), body.indexOf('class="copy'));
		expect(ring.match(/class="thumb/g)!.length).toBeGreaterThan(1);
		expect(ring).toContain('<svg');
		expect(body.slice(0, body.indexOf('class="ring'))).toMatch(
			/class="stage[^"]*" aria-hidden="true"/
		);
	});

	it('is absent when the app serves one subject', () => {
		const one = render(Page, {
			props: {
				data: { subject, subjects: [subjects[1]], askModels, askWeb: 'allow', growModels }
			} as never
		});
		expect(one.body).not.toContain('role="listbox"');
	});
});

describe('the Home control', () => {
	it('is a named button left of the gear, in the gear’s style', () => {
		const { body } = page();
		const home = body.match(
			/<button[^>]*class="icon-button home[^"]*"[^>]*>[\s\S]*?<\/button>/
		)![0];
		expect(home).toContain('type="button"');
		expect(text(home).trim()).toBe('Home');
		expect(home).toContain('aria-hidden="true"');
		expect(body).toMatch(/class="icon-button gear/);
		expect(body.indexOf('class="icon-button home')).toBeLessThan(
			body.indexOf('class="icon-button gear')
		);
	});

	it('is not offered by a shell with nowhere to go home to', () => {
		const settings = new UserSettings([layout], () => null);
		expect(render(Shell, { props: { subject, settings } }).body).not.toContain('Home');
	});
});

describe('the settings control', () => {
	it('is a named disclosure button controlling a closed panel', () => {
		const { body } = page();
		const gear = body.match(
			/<button[^>]*class="icon-button gear[^"]*"[^>]*>[\s\S]*?<\/button>/
		)![0];
		expect(gear).toContain('type="button"');
		expect(gear).toContain('aria-expanded="false"');
		expect(text(gear).trim()).toBe('Settings');
		const panel = gear.match(/aria-controls="([^"]+)"/)![1];
		const at = body.match(new RegExp(`<div[^>]*id="${panel}"[^>]*>`))![0];
		expect(at).toContain('hidden');
		expect(at).toContain('data-own-keys');
		expect(at).toMatch(/role="group"/);
	});

	it('sits in the tab row, after the tabs, in the tabs layout (the default)', () => {
		const { body } = page();
		expect(body.indexOf('role="tablist"')).toBeLessThan(body.indexOf('icon-button gear'));
		expect(body.indexOf('icon-button gear')).toBeLessThan(body.indexOf('id="sync-state"'));
	});

	it('sits in the row heading the right-hand pane in the other layouts too', () => {
		const settings = new UserSettings([layout], () => null);
		settings.set('layout', 'columns');
		const { body } = render(Shell, { props: { subject, settings } });
		expect(body.indexOf('class="tab-row')).toBeLessThan(body.indexOf('icon-button gear'));
		expect(body.indexOf('icon-button gear')).toBeLessThan(body.indexOf('id="sync-state"'));
	});

	it('gathers the shortcut keys under Keys, each a letter or off (korg 3363)', () => {
		const { body } = page();
		expect(body).toMatch(/<p class="group[^"]*">Keys<\/p>/);
		for (const label of ['Sync the narrative', 'Enter a trail', 'Bookmark', 'Add a note'])
			expect(body).toMatch(new RegExp(`<label for="[^"]+"[^>]*>${label}</label>`));
		const id = /<label for="([^"]+)"[^>]*>Add a note<\/label>/.exec(body)![1];
		const select = body.slice(
			body.indexOf(`id="${id}"`),
			body.indexOf('</select>', body.indexOf(`id="${id}"`))
		);
		expect(select).toMatch(/<option value="n"[^>]*selected[^>]*>N</);
		expect(select).toMatch(/<option value="off"[^>]*>Off</);
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
		expect(text(body)).toContain('Stays until synced');
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

	it('is one control: a verb, a labelled text box and a send button', () => {
		const { body } = page();
		expect(body).toContain('<label for="ai-verb" class="visually-hidden">What to do</label>');
		const at = body.indexOf('id="ai-verb"');
		const select = body.slice(at, body.indexOf('</select>', at));
		expect(select).toMatch(
			/^id="ai-verb"[^>]*>(<!--\[-->)?<option value="ask"[^>]*selected[^>]*>Ask a question</
		);
		for (const label of [
			'Grow: new frames on the main spine',
			'Grow: a side trail from this frame',
			'Grow: a new frame with its own trail'
		])
			expect(text(select)).toContain(label);
		expect(text(body)).toContain('Ask a question about this frame');
		expect(body).toMatch(/<button type="submit"[^>]*>\s*Ask\s*<\/button>/);
		expect(body).not.toContain('grow-verb');
	});

	it('is absent when the app config has no grow', () => {
		const { body } = page('allow', null);
		expect(body).not.toContain('ai-verb');
		expect(body).not.toContain('Grow:');
		expect(body).not.toContain('Grow model');
		expect(body).toMatch(/<textarea id="ai-input"/);
	});
});

describe('the web switch in the AI pane', () => {
	const box = (body: string) =>
		/<label class="web[^"]*"[^>]*><input type="checkbox"([^>]*)>/.exec(body);

	it('offers "Web", checked, when the app allows the web', () => {
		const { body } = page('allow');
		expect(box(body)).not.toBeNull();
		expect(text(body)).toMatch(/ Web /);
		expect(box(body)?.[1]).toContain('checked');
	});

	it('offers it unchecked under offer, and not at all under deny', () => {
		expect(box(page('offer').body)?.[1]).not.toContain('checked');
		expect(box(page('deny').body)).toBeNull();
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
					readerData: { places: {}, last: null, bookmarks: [], ...readerData }
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
		expect(body).toMatch(
			/class="tick[^"]*"[^>]*title="[^"]*, bookmarked"[^>]*>(<!--[^>]*-->)*<span class="marks[^"]*" aria-hidden="true">(<!--[^>]*-->)*<span class="mark bookmark/
		);
		expect(body).toContain('Bookmarks (2)');
		// This subject's bookmark moves the shell; the other subject's is a link to it.
		expect(body).toContain('href="/western-civ/prometheus"');
		expect(body).toContain('href="/ai/alexnet"');
		expect(text(body)).toContain('Remove bookmark: alexnet label');
	});

	it('offers to continue where the reader was in the selected subject, and marks the last read', () => {
		const body = withReader({
			places: { 'western-civ': mark('printing-press'), ai: mark('alexnet', 'ai', 'AI') },
			last: mark('alexnet', 'ai', 'History and Current State of AI')
		});
		const offers = body.match(
			/<ul class="resume[^"]*" aria-label="Where you left off">[\s\S]*?<\/ul>/
		)![0];
		expect(text(offers)).toContain('Continue where you were');
		expect(text(offers)).toContain(subject.frames['printing-press'].scene.headline);
		// Only the selection's place: the other subject's waits for its selection.
		expect(offers).not.toContain('href="/ai/alexnet"');
		const at = body.indexOf('role="listbox"');
		const list = body.slice(at, body.indexOf('<h2', at));
		expect(text(list)).toMatch(/History and Current State of AI\s*Last read/);
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

describe('the table of contents', () => {
	const panelOf = (body: string) => {
		const button = body.match(/<button[^>]*title="Contents \(C\)"[^>]*>/)![0];
		const id = button.match(/aria-controls="([^"]+)"/)![1];
		const at = body.indexOf(`id="${id}"`);
		return {
			button,
			panel: body.slice(body.lastIndexOf('<div', at), body.indexOf('</ul></div>', at))
		};
	};

	it('is a closed pop-up in the spine, left of the bookmark, with or without a reader', () => {
		const { body } = page();
		const { button, panel } = panelOf(body);
		expect(button).toContain('aria-expanded="false"');
		expect(panel).toMatch(/^<div[^>]*role="group"[^>]*data-own-keys[^>]*hidden/);
		const spine = body.indexOf('aria-label="Spine"');
		expect(body.indexOf('title="Contents (C)"')).toBeGreaterThan(spine);
		expect(body.indexOf('title="Contents (C)"')).toBeLessThan(body.indexOf('class="index'));
		const reader = render(Page, {
			props: {
				data: {
					subject,
					subjects,
					askModels,
					askWeb: 'allow',
					growModels,
					frame: null,
					reader: { name: 'Ken' },
					readerData: { places: {}, last: null, bookmarks: [] }
				}
			} as never
		}).body;
		expect(reader.indexOf('title="Contents (C)"')).toBeLessThan(
			reader.indexOf('Bookmark this frame')
		);
	});

	it('lists every frame under its segment, linked, with the current one marked', () => {
		const { panel } = panelOf(page().body);
		for (const seg of subject.spine.segments) expect(text(panel)).toContain(seg.title);
		for (const id of Object.keys(subject.frames))
			expect(panel).toContain(`href="/western-civ/${id}"`);
		const first = subject.spine.segments[0].frames[0];
		expect(panel).toMatch(new RegExp(`<a href="/western-civ/${first}" aria-current="page"`));
		expect(panel.match(/aria-current=/g)).toHaveLength(1);
		expect(panel).toContain('placeholder="Filter by title or position"');
	});

	it('puts each trail, collapsed, under the frame it branches from', () => {
		const { panel } = panelOf(page().body);
		const trail = subject.trails.find((t) => t.anchor === 'printing-press')!;
		const anchor = panel.indexOf('href="/western-civ/printing-press"');
		const disclosure = panel.indexOf(`Trail: ${trail.title}`);
		expect(disclosure).toBeGreaterThan(anchor);
		const button = panel.slice(panel.lastIndexOf('<button', disclosure), disclosure);
		expect(button).toContain('aria-expanded="false"');
		const list = button.match(/aria-controls="([^"]+)"/)![1];
		expect(panel).toMatch(new RegExp(`<ul id="${list}"[^>]*hidden`));
	});

	it('says the reader’s marks on a frame in words', () => {
		const settings = new UserSettings([layout], () => null);
		const body = render(Shell, {
			props: {
				subject,
				settings,
				bookmarks: {
					marked: new Set(['prometheus']),
					items: [],
					ontoggle: () => {},
					onremove: () => {}
				}
			}
		}).body;
		const at = body.indexOf('href="#prometheus"');
		expect(text(body.slice(at, body.indexOf('</a>', at)))).toContain('bookmarked');
	});
});

describe('the layout', () => {
	const shell = (shape: string) => {
		const settings = new UserSettings([layout], () => null);
		settings.set('layout', shape);
		return render(Shell, { props: { subject, settings } }).body;
	};

	it('is a setting, two panes with tabs by default', () => {
		const { body } = page();
		const id = /<label for="([^"]+)"[^>]*>Layout<\/label>/.exec(body)?.[1];
		expect(id).toBeDefined();
		expect(body).toMatch(
			new RegExp(`<select id="${id}"[^>]*>[\\s\\S]*?<option value="tabs"[^>]*selected`)
		);
	});

	it('puts Narrative and AI in a tab list, Narrative selected, each tab controlling its panel', () => {
		const body = shell('tabs');
		expect(body).toMatch(/<div role="tablist" aria-label="Right-hand pane"/);
		expect(body).toMatch(
			/role="tab" id="tab-narrative" aria-selected="true" aria-controls="narrative-panel" tabindex="0"/
		);
		expect(body).toMatch(
			/role="tab" id="tab-ai" aria-selected="false" aria-controls="ai-results" tabindex="-1"/
		);
		expect(body).toMatch(/<section id="narrative-panel"[^>]*role="tabpanel"/);
		expect(body).toMatch(
			/<div id="ai-results"[^>]*role="tabpanel"[^>]*aria-labelledby="tab-ai"[^>]*hidden/
		);
	});

	it('keeps the AI control in sight on the Narrative tab, so a question can be typed while reading', () => {
		const body = shell('tabs');
		expect(body).toMatch(/<textarea id="ai-input"/);
		expect(body.slice(body.indexOf('id="ai-results"'))).toMatch(/<form class="control/);
	});

	it('has no tabs in the other layouts, and shows the results as a region', () => {
		for (const shape of ['columns', 'strip', 'split']) {
			const body = shell(shape);
			expect(body).toContain(`class="panes ${shape}`);
			expect(body).not.toContain('role="tablist"');
			expect(body).toMatch(/<div id="ai-results"[^>]*role="region"[^>]*aria-label="AI results"/);
			expect(body).not.toMatch(/<section id="narrative-panel"[^>]*role="tabpanel"/);
		}
	});

	it('puts a divider on the spine in every layout, and one more where a layout has a third pane', () => {
		const seps = (shape: string) =>
			[...shell(shape).matchAll(/<div[^>]*role="separator"[^>]*>/g)].map((m) => m[0]);
		for (const shape of ['tabs', 'strip']) {
			expect(seps(shape)).toHaveLength(1);
			expect(seps(shape)[0]).toMatch(/aria-orientation="vertical"/);
			expect(seps(shape)[0]).toMatch(/aria-label="Resize the spine"/);
			expect(seps(shape)[0]).toMatch(/aria-controls="spine-pane"/);
			expect(seps(shape)[0]).toMatch(
				/aria-valuenow="60"[^>]*aria-valuemin="25"[^>]*aria-valuemax="75"/
			);
			expect(seps(shape)[0]).toMatch(/tabindex="0"/);
		}
		expect(seps('columns').map((s) => /aria-label="([^"]+)"/.exec(s)![1])).toEqual([
			'Resize the spine',
			'Resize the AI pane'
		]);
		expect(seps('split')[1]).toMatch(
			/aria-orientation="horizontal"[^>]*aria-label="Resize the narrative"/
		);
	});

	it('puts the keyboard help in a bar under the whole page, outside every pane', () => {
		const body = shell('columns');
		const hint = body.indexOf('<p id="ai-hint"');
		expect(hint).toBeGreaterThan(body.lastIndexOf('role="separator"'));
		expect(text(body.slice(hint))).toContain('drag a divider');
	});
});

describe('the reader’s keys', () => {
	const shell = (keys: Record<string, string>) => {
		const settings = new UserSettings([layout, ...keySettings], () => null);
		for (const [k, v] of Object.entries(keys)) settings.set(`key.${k}`, v);
		return render(Shell, { props: { subject, settings } }).body;
	};

	it('name the reader’s letters in the help, and leave out one turned off', () => {
		const hint = said(shell({ sync: 'y', trail: 'off' }).match(/<p id="ai-hint"[\s\S]*?<\/p>/)![0]);
		expect(hint).toContain('Y sync and C contents, in the spine or narrative');
		expect(hint).not.toContain('T trail');
	});

	it('say in the settings when one letter is set for two shortcuts', () => {
		expect(said(shell({ trail: 's' }))).toContain(
			'S is set for sync the narrative and enter a trail; it will sync the narrative.'
		);
		expect(shell({})).not.toContain('class="warning');
	});
});

describe('the reader’s layer on a frame', () => {
	const at = '2026-09-28T12:00:00.000Z';
	const first = 'prometheus';
	const note = (over: Partial<Note> = {}): Note => ({
		id: 'n1',
		subject: 'western-civ',
		frame: first,
		label: 'We stole FIRE.',
		text: 'Why a liver?',
		anchor: null,
		review: 'none',
		response: null,
		created: at,
		updated: at,
		...over
	});
	const layer = (over: Partial<ReaderLayer> = {}): ReaderLayer => ({
		notes: [],
		kept: {},
		saveNote: async () => null,
		deleteNote: async () => false,
		keptOn: async () => [],
		forget: async () => false,
		onkept: () => {},
		...over
	});
	const shell = (l: ReaderLayer | null, shape = 'tabs') => {
		const settings = new UserSettings([layout], () => null);
		settings.set('layout', shape);
		return render(Shell, { props: { subject, settings, layer: l } }).body;
	};

	it('adds a Notes tab beside Narrative, in every layout, when there is a reader', () => {
		for (const shape of ['tabs', 'columns', 'strip', 'split']) {
			const body = shell(layer(), shape);
			expect(body).toMatch(
				/role="tab" id="tab-notes" aria-selected="false" aria-controls="notes-panel"/
			);
			expect(body).toMatch(
				/<div id="notes-panel" class="notes[^"]*" role="tabpanel" aria-labelledby="tab-notes" hidden/
			);
		}
		expect(shell(layer())).toMatch(/id="tab-narrative"[\s\S]*id="tab-notes"[\s\S]*id="tab-ai"/);
	});

	it('has no Notes tab, panel or note key without a reader', () => {
		const body = shell(null, 'columns');
		expect(body).not.toContain('notes-panel');
		expect(body).not.toContain('role="tablist"');
		expect(said(body)).not.toContain('N note');
	});

	it('lists the frame’s notes, flagged and handled ones saying so, and counts them on the tab', () => {
		const body = shell(
			layer({
				notes: [
					note(),
					note({ id: 'n2', text: 'Reword this.', review: 'flagged' }),
					note({ id: 'n3', text: 'Odd date.', review: 'handled', response: 'Fixed the date.' }),
					note({ id: 'n4', frame: 'printing-press', text: 'Not this frame.' })
				]
			})
		);
		const panel = said(body.slice(body.indexOf('id="notes-panel"')));
		expect(panel).toContain('Why a liver?');
		expect(panel).toContain('flagged for agent review');
		expect(panel).toContain('Agent: Fixed the date.');
		expect(panel).not.toContain('Not this frame.');
		expect(panel).toContain('Edit: Why a liver?');
		expect(panel).toContain('Delete: Why a liver?');
		expect(said(body)).toContain('Notes 3, 3 on this frame');
	});

	it('marks kept answers and notes under the line, and says so in words', () => {
		const body = shell(layer({ notes: [note()], kept: { [first]: 2 } }));
		expect(body).toMatch(/role="slider"[^>]*aria-valuetext="[^"]*, 2 kept answers, 1 note"/);
		expect(body).toMatch(
			/title="[^"]*, 2 kept answers, 1 note"[^>]*>(<!--[^>]*-->)*<span class="marks[^"]*" aria-hidden="true">(<!--[^>]*-->|\s)*<span class="mark kept[^"]*"><\/span>(<!--[^>]*-->|\s)*<span class="mark note/
		);
		expect(said(body)).toContain('2 kept answers, 1 note.');
	});

	it('offers the frame’s kept answers as a closed Q&A section, only where there are some', () => {
		const body = shell(layer({ kept: { [first]: 2 } }));
		expect(body).toMatch(/<details class="qa[^"]*">\s*<summary[^>]*>Q&amp;A \(2\)<\/summary>/);
		expect(body).not.toMatch(/<details class="qa[^"]*"[^>]*\bopen/);
		expect(shell(layer())).not.toContain('class="qa');
	});

	it('says N adds a note, in the help and on the Add button', () => {
		const body = shell(layer());
		expect(said(body.match(/<p id="ai-hint"[\s\S]*?<\/p>/)![0])).toContain(
			'S sync, T trail, N note, A annotate and C contents, in the spine, narrative or notes'
		);
		expect(said(body)).toContain('Add a note N');
	});

	it('offers Annotate in the narrative with a reader, and not without', () => {
		const body = shell(layer());
		expect(body).toMatch(
			/<button type="button" class="annotate[^"]*" aria-describedby="annotate-how"/
		);
		expect(said(body)).toContain('Annotate A');
		expect(said(body)).toContain('Annotates the words selected in the reading');
		const none = shell(null, 'columns');
		expect(none).not.toContain('class="annotate');
		expect(said(none)).not.toContain('A annotate');
	});

	it('lists an annotation with the words it is on, and a way to them in the reading', () => {
		const anchor = { exact: 'kept fire', prefix: 'years of ', suffix: '.', start: 40 };
		const body = shell(layer({ notes: [note({ id: 'a1', text: 'How do we know?', anchor })] }));
		const panel = said(body.slice(body.indexOf('id="notes-panel"')));
		expect(panel).toMatch(/On the words: kept fire How do we know\?/);
		expect(panel).toContain('Show in reading: kept fire');
		expect(said(body)).toContain('Notes 1, 1 on this frame');
		// A plain note has neither.
		expect(said(shell(layer({ notes: [note()] })))).not.toContain('Show in reading');
	});
});

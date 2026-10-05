import { join } from 'node:path';
import { render } from 'svelte/server';
import { beforeAll, describe, expect, it, vi } from 'vitest';
import { loadSubject } from '$engine/load';
import type { Subject } from '$engine/model';
import { bodyOf, subjectHeadOf, type ServedBody } from '$engine/served';
import { startLook } from '$engine/start';
import { followSpine, layout, readingColours, sceneColours } from '$engine/settings';
import { parseBinding, type Shortcut } from '$engine/keys';
import type { MyNotesOffer } from '$engine/my-notes';
import type { Note, ReaderLayer } from '$engine/reader-data';
import Shell from '$engine/ui/Shell.svelte';
import { UserSettings } from '$engine/user-settings.svelte';
import Page from './+page.svelte';

// The page reads the history entry's state for the Back chip (§Connections).
const navState = vi.hoisted(() => ({ back: [] as unknown[] }));
vi.mock('$app/state', () => ({
	page: {
		get state() {
			return navState;
		}
	}
}));

let subject: Subject;
/** Every frame's body, as the page would have fetched them (§Serving). */
let bodies: Record<string, ServedBody>;
const withLinks = (links: Record<string, ServedBody['links']> = {}) =>
	Object.fromEntries(
		Object.entries(subject.frames).map(([id, f]) => [
			id,
			{ ...bodyOf(f), links: links[id] ?? { connections: [], names: {} } }
		])
	);
beforeAll(async () => {
	subject = await loadSubject(
		join(import.meta.dirname, '..', '..', '..', '..', 'subjects', 'western-civ')
	);
	bodies = withLinks();
});
/** What the load gives the page of its subject (§Serving). */
const served = () => ({
	subject: subjectHeadOf(subject),
	start: startLook(subject),
	bodies,
	build: 'test'
});

const askModels = {
	choices: [
		{ value: 'claude-sonnet-5', label: 'Sonnet 5' },
		{ value: 'claude-opus-5-5', label: 'Opus 5.5' }
	],
	default: 'claude-sonnet-5'
};
const growModels = { ...askModels, default: 'claude-opus-5-5' };
const page = (
	askWeb = 'allow',
	grow: typeof growModels | null = growModels,
	extra: Record<string, unknown> = {}
) =>
	render(Page, {
		props: {
			data: {
				...served(),
				subjects,
				ai: { askModels, askWeb, growModels: grow },
				...extra
			}
		} as never
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
/**
 * Where the icon button named `name` (its visually hidden label) opens, and
 * its opening tag: the HUD's tooltips are drawn in the browser, so the page
 * names a button only as assistive technology hears it (korg 3540).
 */
function buttonNamed(body: string, name: string): { at: number; tag: string } {
	const label = `<span class="visually-hidden">${name}</span>`;
	const end = body.indexOf(label);
	if (end < 0) return { at: -1, tag: '' };
	const at = body.lastIndexOf('<button', end);
	return { at, tag: body.slice(at, body.indexOf('>', at) + 1) };
}

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

	it('lists a frame’s edits and corrections in a closed control below Citations, and none when there are none', () => {
		expect(page().body).not.toContain('<details class="citations edits');
		const edited = {
			...bodies,
			prometheus: {
				...bodies.prometheus,
				edits: [
					{ date: '2026-10-02', kind: 'correction' as const, summary: 'Corrected: a date.' },
					{ date: '2026-09-30', kind: 'revision' as const, summary: 'Revised: rewritten.' }
				]
			}
		};
		const { body } = page('allow', growModels, { bodies: edited });
		const edits = body.slice(body.indexOf('<details class="citations edits'));
		expect(edits).not.toMatch(/^<details[^>]*\bopen\b/);
		expect(text(edits)).toMatch(
			/Edits and corrections \(2\)\s*Correction · October 2, 2026\s*Corrected: a date\.\s*Revision · September 30, 2026/
		);
		expect(body.indexOf('Citations (4)')).toBeLessThan(body.indexOf('Edits and corrections ('));
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
		expect(body.indexOf('Sources')).toBeLessThan(body.indexOf('<details class="citations'));
		expect(body.indexOf('<details class="citations')).toBeLessThan(body.indexOf('id="ai-input"'));
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

	it('names S, T, C, M, Z, D and W in the hint bar, acting anywhere but a text box (korg 3564)', () => {
		const hint = said(page().body.match(/<p id="ai-hint"[\s\S]*?<\/p>/)![0]);
		expect(hint).toContain('S sync, T trail, C contents, M map, Z zoom, D random and W anywhere ·');
		expect(hint).not.toContain('in the spine');
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

	it('lists titles without a leading "The " or the subject’s subtitle; the big title keeps both', () => {
		const { body } = render(Page, {
			props: {
				data: {
					...served(),
					subjects: [subjects[0], { ...subjects[1], subtitle: 'from myth to the modern world' }],
					ai: { askModels, askWeb: 'allow', growModels }
				}
			} as never
		});
		const at = body.indexOf('role="listbox"');
		const list = body.slice(at, body.indexOf('</div></div>', at));
		expect(text(list)).toContain('History of Western Civilization');
		expect(list).not.toContain('The History of Western Civilization');
		expect(list).not.toContain('from myth to the modern world');
		expect(body).toContain('The History of Western Civilization</h2>');
		expect(text(body)).toContain('from myth to the modern world');
	});

	it('offers the same subjects in a picker for a narrow screen, this one selected', () => {
		const { body } = page();
		const picker = body.match(
			/<select class="picker[^"]*" aria-label="Subjects"[\s\S]*?<\/select>/
		)![0];
		const options = [...picker.matchAll(/<option value="([^"]+)"([^>]*)>([^<]*)</g)];
		expect(options.map((o) => o[1])).toEqual(['ai', 'western-civ']);
		expect(options.find((o) => o[1] === 'western-civ')![2]).toContain('selected');
		expect(options.map((o) => o[3])).toEqual([
			'History and Current State of AI',
			'History of Western Civilization'
		]);
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
				data: {
					...served(),
					subjects: [subjects[1]],
					ai: { askModels, askWeb: 'allow', growModels }
				}
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
		expect(render(Shell, { props: { subject, bodies, settings } }).body).not.toContain('Home');
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
		const { body } = render(Shell, { props: { subject, bodies, settings } });
		expect(body.indexOf('class="tab-row')).toBeLessThan(body.indexOf('icon-button gear'));
		expect(body.indexOf('icon-button gear')).toBeLessThan(body.indexOf('id="sync-state"'));
	});

	it('keeps the shortcuts out of the pop-up, behind a Keyboard shortcuts button (korg 3493)', () => {
		const { body } = page();
		expect(body).not.toMatch(/<p class="group[^"]*">Keys<\/p>/);
		expect(body).not.toMatch(/<label for="[^"]+"[^>]*>Add a note<\/label>/);
		expect(body).toMatch(/<button[^>]*aria-haspopup="dialog"[^>]*>Keyboard shortcuts…<\/button>/);
		// The dialog is there, closed and empty until it opens.
		expect(body).toMatch(/<dialog class="keys-dialog[^"]*"[^>]*data-own-keys/);
	});

	it('renders each setting as a labelled select, starting at its default', () => {
		const { body } = page();
		const id = body.match(/<select[^>]*id="([^"]+)"/)![1];
		expect(body).toMatch(new RegExp(`<label for="${id}"[^>]*>Scene colors</label>`));
		expect(body).toMatch(/<option value="section"[^>]*selected/);
		expect(body).toMatch(/<option value="same"[^>]*selected/);
		expect(text(body)).toContain('Always dark');
		expect(text(body)).toContain('Always light');
		// The old single Palette row is gone (korg 3495).
		expect(body).not.toMatch(/>Palette<\/label>/);
	});

	it('keeps the brightness sliders under a collapsed Advanced, each at As designed', () => {
		const { body } = page();
		const advanced = body.slice(body.indexOf('<details class="advanced'));
		expect(advanced).toMatch(/^<details class="advanced[^"]*">/);
		expect(advanced).not.toMatch(/^<details[^>]*\bopen\b/);
		for (const label of ['Light brightness', 'Dark brightness']) {
			const id = new RegExp(`<label for="([^"]+)"[^>]*>${label}</label>`).exec(advanced)![1];
			const input = new RegExp(`<input[^>]*id="${id}"[^>]*>`).exec(advanced)![0];
			expect(input).toContain('type="range"');
			expect(input).toContain('aria-valuetext="As designed"');
		}
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
		expect(text(render(Shell, { props: { subject, bodies, settings } }).body)).toContain(
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

describe('scene and reading colours (korg 3495)', () => {
	const shell = (scene: string, reading = 'same', frame?: string) => {
		const settings = new UserSettings([sceneColours, readingColours], () => null);
		settings.set('scene', scene);
		settings.set('reading', reading);
		const body = render(Shell, { props: { subject, bodies, settings, startAt: frame } }).body;
		// The scene pane's own style, and the shell's, which the reading wears.
		const style = (re: RegExp) => body.match(re)?.[1] ?? '';
		return {
			scene: style(/id="spine-pane"[^>]*style="([^"]*)"/),
			reading: style(/class="shell[^"]*"[^>]*style="([^"]*)"/)
		};
	};
	const bg = (name: string) => `--background: ${subject.palettes[name].background}`;

	it('paints the first frame (night) as itself by section, by frame and in Dark', () => {
		for (const mode of ['section', 'frame', 'dark']) {
			const { scene, reading } = shell(mode);
			expect(scene).toContain(bg('night'));
			expect(reading).toContain(bg('night'));
		}
	});

	it('paints the first frame in its light counterpart in Light', () => {
		const { scene } = shell('light');
		expect(scene).toContain(bg('parchment'));
		expect(scene).toContain('color-scheme: light');
	});

	it('colours the reading apart from the scene when the reader fixes it', () => {
		const { scene, reading } = shell('section', 'light');
		expect(scene).toContain(bg('night'));
		expect(reading).toContain(bg('parchment'));
		expect(reading).toContain('color-scheme: light');
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
					...served(),
					subjects,
					ai: { askModels, askWeb: 'allow', growModels },
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
		expect(toggle).not.toContain('title=');
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

	it('marks what is new to the reader: the spine, the HUD’s count, the subject list and Begin', () => {
		const news = {
			readings: { 'western-civ': { first: at, caughtUp: null }, ai: { first: at, caughtUp: at } },
			lastVisit: null,
			fresh: { 'western-civ': ['prometheus'], ai: ['alexnet', 'transformer'] }
		};
		const body = withReader({ news });
		expect(body).toMatch(/role="slider"[^>]*aria-valuetext="[^"]*, new to you"/);
		expect(body).toMatch(
			/title="Myth, new to you"[^>]*>(\s*<!--[^>]*-->)*\s*<span class="marks[^"]*" aria-hidden="true">(\s*<!--[^>]*-->)*\s*<span class="mark fresh/
		);
		expect(text(body)).toContain("What's new, 1 new to you here");
		const at0 = body.indexOf('role="listbox"');
		expect(text(body.slice(at0, body.indexOf('<h2', at0)))).toMatch(
			/History and Current State of AI\s*2 new/
		);
		expect(body).toMatch(/<option value="ai"[^>]*>History and Current State of AI · 2 new</);
		// The selection is this subject: Begin says what is new in it.
		expect(text(body)).toContain('1 new since you started');
		// Nothing is new without a reader, or in a subject not started.
		expect(text(withReader({}))).not.toContain('new to you');
	});

	it('marks a bookmarked frame on the spine, in words as well as the mark', () => {
		const body = withReader({ bookmarks: [mark('prometheus'), mark('alexnet', 'ai', 'AI')] });
		expect(body).toMatch(/<button[^>]*aria-pressed="true"/);
		expect(body).toMatch(/role="slider"[^>]*aria-valuetext="[^"]*, bookmarked"/);
		expect(body).toMatch(
			/class="tick[^"]*"[^>]*title="[^"]*, bookmarked"[^>]*>(<!--[^>]*-->)*<span class="marks[^"]*" aria-hidden="true">(\s*<!--[^>]*-->)*\s*<span class="mark bookmark/
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
		// An open book, said in words to a screen reader; in words in the picker.
		expect(list).toMatch(
			/History and Current State of AI<\/span>(<!--[^>]*-->)*<span class="last[^"]*">(<!--[^>]*-->\s*)*<svg[\s\S]*?<span class="visually-hidden">Last read<\/span>/
		);
		expect(body).toMatch(/<option value="ai"[^>]*>History and Current State of AI — last read</);
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

describe('the map', () => {
	it('opens from the spine, beside the contents, and from the start screen', () => {
		const { body } = page();
		const map = buttonNamed(body, 'Map');
		expect(map.tag).toContain('aria-haspopup="dialog"');
		expect(map.at).toBeGreaterThan(buttonNamed(body, 'Contents').at);
		expect(map.at).toBeLessThan(body.indexOf('class="index'));
		// Zoom drawing (korg 3539) comes next, between the map and What's new.
		const zoom = buttonNamed(body, 'Zoom drawing');
		expect(zoom.at).toBeGreaterThan(map.at);
		expect(zoom.tag).toContain('aria-haspopup="dialog"');
		const fresh = body.indexOf('<span class="visually-hidden">What\'s new');
		expect(fresh).toBeGreaterThan(zoom.at);
		expect(body).toMatch(/<dialog[^>]*class="zoom[^"]*"[^>]*data-own-keys/);
		expect(body).toMatch(/<button[^>]*class="map-button[^>]*>\s*Map of the library/);
		// A closed modal until it is opened; the page stands its keys down inside it.
		expect(body).toMatch(/<dialog[^>]*class="map [^"]*"[^>]*data-own-keys/);
		expect(body).not.toMatch(/<dialog[^>]*class="map[^>]*open/);
	});
});

describe('the table of contents', () => {
	const panelOf = (body: string) => {
		const button = buttonNamed(body, 'Contents').tag;
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
		expect(buttonNamed(body, 'Contents').at).toBeGreaterThan(spine);
		expect(buttonNamed(body, 'Contents').at).toBeLessThan(body.indexOf('class="index'));
		const reader = render(Page, {
			props: {
				data: {
					...served(),
					subjects,
					ai: { askModels, askWeb: 'allow', growModels },
					frame: null,
					reader: { name: 'Ken' },
					readerData: { places: {}, last: null, bookmarks: [] }
				}
			} as never
		}).body;
		expect(buttonNamed(reader, 'Contents').at).toBeLessThan(reader.indexOf('Bookmark this frame'));
	});

	it('lists every frame under its segment, linked, with the current one marked', () => {
		const { panel } = panelOf(page().body);
		for (const seg of subject.spine.segments) expect(text(panel)).toContain(seg.title);
		for (const id of Object.keys(subject.frames))
			expect(panel).toContain(`href="/western-civ/${id}"`);
		const first = subject.spine.segments[0].frames[0];
		expect(panel).toMatch(new RegExp(`<a href="/western-civ/${first}" aria-current="page"`));
		expect(panel.match(/aria-current=/g)).toHaveLength(1);
		expect(panel).toContain('placeholder="Filter by title, position or topic"');
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

describe('with no AI pane (the reader edition, korg 3500)', () => {
	const bare = (extra: Record<string, unknown> = {}) =>
		render(Page, {
			props: { data: { ...served(), subjects, ai: null, ...extra } } as never
		}).body;

	it('has no AI pane, no AI tab, and no layout or model to choose', () => {
		const body = bare();
		expect(body).not.toMatch(/id="ai-pane"|id="ai-input"|id="tab-ai"/);
		expect(body).not.toMatch(/>Layout<\/label>|>Ask model<\/label>|>Grow model<\/label>/);
		expect(text(body)).not.toContain('into and out of the AI pane');
		expect(text(body)).toContain('A timeline you can read and annotate');
	});

	it('keeps the notes, with the reader’s tabs', () => {
		const body = bare({
			reader: { name: 'Joel and Kathy', signedIn: true },
			readerData: { places: {}, last: null, bookmarks: [], notes: [], kept: {}, unseen: 0 }
		});
		expect(body).toMatch(/id="tab-narrative"/);
		expect(body).toMatch(/id="tab-notes"/);
	});
});

describe('the start screen’s Welcome link and sign-out (korg 3501, 3502)', () => {
	it('links to the Welcome and How-To page always, and offers sign-out to a signed-in reader', () => {
		const signedIn = page('allow', growModels, {
			reader: { name: 'Joel and Kathy', signedIn: true }
		}).body;
		expect(signedIn).toMatch(/<a href="\/welcome"[^>]*>Welcome and how to read kloom<\/a>/);
		expect(signedIn).toMatch(/<form method="POST" action="\/signout"/);
		expect(text(signedIn)).toContain('Signed in as Joel and Kathy');
		const tailnet = page('allow', growModels, {
			reader: { name: 'Ken', signedIn: false }
		}).body;
		expect(tailnet).toMatch(/Welcome and how to read kloom/);
		expect(tailnet).not.toMatch(/action="\/signout"/);
	});

	it("links to the User's Guide beside Welcome (korg 3515)", () => {
		const body = page().body;
		const welcome = body.search(/<a href="\/welcome"/);
		const guide = body.search(/<a href="\/guide"[^>]*>User(&#39;|')s Guide<\/a>/);
		expect(guide).toBeGreaterThan(welcome);
		expect(welcome).toBeGreaterThan(-1);
	});
});

describe('the layout', () => {
	const shell = (shape: string) => {
		const settings = new UserSettings([layout], () => null);
		settings.set('layout', shape);
		return render(Shell, { props: { subject, bodies, settings } }).body;
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
		const settings = new UserSettings([layout], () => null);
		for (const [k, v] of Object.entries(keys))
			settings.keys.set(k as Shortcut, v === 'off' ? null : parseBinding(v));
		return render(Shell, { props: { subject, bodies, settings } }).body;
	};
	const hint = (body: string) => said(body.match(/<p id="ai-hint"[\s\S]*?<\/p>/)![0]);

	it('name the reader’s keys in the help, and leave out one turned off', () => {
		const h = hint(shell({ sync: 'y', trail: 'off' }));
		expect(h).toContain('Y sync, C contents and Z zoom ·');
		expect(h).not.toContain('T trail');
	});

	it('name a binding with a modifier among the rest, since every one acts anywhere (korg 3564)', () => {
		const h = hint(shell({ contents: 'alt+c', sync: 'ctrl+shift+y' }));
		expect(h).toContain('Ctrl+Shift+Y sync, T trail, Alt+C contents and Z zoom ·');
	});

	it('keep the settings pop-up to settings, with the shortcuts a button away', () => {
		const body = shell({});
		expect(body).toContain('Keyboard shortcuts…');
		expect(body).not.toMatch(/<label[^>]*>Go to a random frame/);
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
		unseen: false,
		created: at,
		updated: at,
		...over
	});
	const layer = (over: Partial<ReaderLayer> = {}): ReaderLayer => ({
		notes: [],
		kept: {},
		saveNote: async () => null,
		deleteNote: async () => false,
		seen: () => {},
		keptOn: async () => [],
		forget: async () => false,
		onkept: () => {},
		...over
	});
	const shell = (l: ReaderLayer | null, shape = 'tabs') => {
		const settings = new UserSettings([layout], () => null);
		settings.set('layout', shape);
		return render(Shell, { props: { subject, bodies, settings, layer: l } }).body;
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
			'S sync, T trail, N note, A annotate, C contents and Z zoom ·'
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

describe('My notes (§My notes)', () => {
	const offer = (unseen: number): MyNotesOffer => ({
		unseen,
		load: async () => null,
		reading: async () => null,
		seen: async () => {},
		flag: async () => null,
		clear: async () => null,
		go: () => {},
		hrefOf: (s, f) => `/${s}/${f}`
	});
	const shell = (myNotes: MyNotesOffer | null) =>
		render(Shell, {
			props: { subject, bodies, settings: new UserSettings([], () => null), myNotes }
		}).body;

	it('is a control in the HUD that says how many answers are new, and a key in the help', () => {
		const body = shell(offer(2));
		expect(body).toMatch(/<button type="button" class="icon opener[^"]*" aria-haspopup="dialog"/);
		expect(said(body)).toContain('My notes, 2 new answers');
		expect(body).toMatch(/<span class="badge[^"]*" aria-hidden="true">2<\/span>/);
		expect(said(body.match(/<p id="ai-hint"[\s\S]*?<\/p>/)![0])).toContain('O my notes');
		// Closed until opened: a dialog, with nothing loaded in it.
		expect(body).toMatch(
			/<dialog class="my-notes[^"]*" aria-labelledby="[^"]*" data-own-keys(="")?>/
		);
	});

	it('has no count when nothing is new, and is absent without a reader', () => {
		const body = shell(offer(0));
		expect(said(body)).toContain('My notes');
		expect(said(body)).not.toContain('new answer');
		expect(body).not.toContain('class="badge');
		const none = shell(null);
		expect(none).not.toContain('my-notes');
		expect(said(none)).not.toContain('O my notes');
	});
});

describe('a frame whose body is on its way (§Serving)', () => {
	const shell = (b: typeof bodies) =>
		render(Shell, { props: { subject, bodies: b, settings: new UserSettings([], () => null) } })
			.body;

	it('shows the scene from its head, and says the reading is coming', () => {
		const body = shell({});
		expect(said(body)).toContain('We stole FIRE.');
		expect(body).toMatch(/<p class="pending[^"]*" role="status">Fetching the reading…<\/p>/);
		expect(body).not.toContain('class="illustration');
		expect(said(body)).not.toContain('Sources');
	});

	it('shows the reading and the drawing once it has arrived', () => {
		const body = shell(bodies);
		expect(body).not.toContain('Fetching the reading');
		expect(body).toContain('class="illustration');
		expect(said(body)).toContain('Sources');
	});
});

describe('connections and names (§Connections)', () => {
	const connections = {
		prometheus: {
			names: {},
			connections: [
				{
					direction: 'out',
					why: 'Fire, then fire put to work.',
					subject: 'western-civ',
					subjectTitle: 'The History of Western Civilization',
					frame: 'steam',
					title: 'Then we put fire to WORK.',
					topic: "Watt's steam engine",
					label: 'AD 1776',
					trail: null,
					detached: false
				},
				{
					direction: 'in',
					why: 'Myths of made minds.',
					subject: 'ai',
					subjectTitle: 'History and Current State of AI',
					frame: 'talos',
					title: 'We imagined minds of BRONZE.',
					topic: 'Talos and ancient automata',
					label: 'Myth',
					trail: null,
					detached: false
				},
				{
					direction: 'out',
					why: 'A subject not served.',
					subject: 'physics',
					subjectTitle: 'physics',
					frame: 'fire',
					detached: true
				}
			]
		}
	};

	it("lists a frame's connections above its Sources, each with its why", () => {
		const html = page('allow', growModels, { bodies: withLinks(connections as never) }).body;
		const at = html.search(/<h3[^>]*>Connections<\/h3>/);
		const sources = html.search(/<h3[^>]*>Sources<\/h3>/);
		expect(at).toBeGreaterThan(0);
		expect(at).toBeLessThan(sources);
		const list = said(html.slice(at, sources));
		expect(list).toContain("Watt's steam engine AD 1776 Fire, then fire put to work.");
		// Another subject's frame names its subject; one stored there says so.
		expect(list).toContain('History and Current State of AI · Myth');
		expect(html).toContain('href="/ai/talos" aria-label="From Talos and ancient automata"');
		// A missing target is detached, never a failure.
		expect(list).toContain('physics/fire Not found');
	});

	it("marks a name's first mention in the reading as a button, not a link", () => {
		expect(page('allow', growModels, { bodies: withLinks(connections as never) }).body).toMatch(
			/<button type="button" class="name" data-name="prometheus" aria-haspopup="dialog" aria-expanded="false">/
		);
	});

	it('shows no Back chip without a jump, and names the last jump with one', () => {
		expect(page().body).not.toContain('class="back');
		navState.back = [
			{ subject: 'ai', frame: 'talos', title: 'We imagined minds of BRONZE.', subjectTitle: 'AI' },
			{ subject: 'ai', frame: 'eliza', title: 'We saw ourselves in a MIRROR.', subjectTitle: 'AI' }
		];
		try {
			const html = page().body;
			expect(html).toContain(
				'aria-label="Back to We saw ourselves in a MIRROR., AI, and 1 more before it"'
			);
			expect(said(html)).toContain('R back');
		} finally {
			navState.back = [];
		}
	});
});

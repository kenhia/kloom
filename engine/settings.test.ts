import { describe, expect, it } from 'vitest';
import { DEFAULT_KEYS, parseBinding, plain } from './keys';
import type { Palette } from './model';
import {
	coloursOf,
	darkBrightness,
	followSpine,
	framePalettes,
	layout,
	lightBrightness,
	migratePaletteSetting,
	paletteFor,
	readingColours,
	sceneColours,
	sectionPalette,
	keyWarnings,
	readKeymap,
	readSetting,
	writeKey,
	writeSetting,
	type Setting
} from './settings';
import { UserSettings } from './user-settings.svelte';

/** A Map-backed Storage, optionally one that throws like blocked storage. */
function memory(blocked = false) {
	const map = new Map<string, string>();
	return {
		map,
		getItem(key: string) {
			if (blocked) throw new DOMException('blocked', 'SecurityError');
			return map.get(key) ?? null;
		},
		setItem(key: string, value: string) {
			if (blocked) throw new DOMException('blocked', 'SecurityError');
			map.set(key, value);
		}
	};
}

const model: Setting = {
	id: 'model',
	label: 'Model',
	choices: [
		{ value: 'a-1', label: 'A' },
		{ value: 'b-2', label: 'B' }
	],
	default: 'a-1',
	storageKey: 'test.model'
};

describe('readSetting and writeSetting', () => {
	it('falls back to the default with nothing stored, or no storage', () => {
		expect(readSetting(model, memory())).toBe('a-1');
		expect(readSetting(model, null)).toBe('a-1');
	});

	it('remembers a choice under the storage key', () => {
		const s = memory();
		expect(writeSetting(model, 'b-2', s)).toBe(true);
		expect(s.map.get('test.model')).toBe('b-2');
		expect(readSetting(model, s)).toBe('b-2');
	});

	it('falls back to the default when the stored value is no longer a choice', () => {
		const s = memory();
		s.map.set('test.model', 'retired-model');
		expect(readSetting(model, s)).toBe('a-1');
	});

	it('refuses to store something that is not a choice', () => {
		const s = memory();
		expect(writeSetting(model, 'free text', s)).toBe(false);
		expect(s.map.size).toBe(0);
	});

	it('survives blocked storage', () => {
		const s = memory(true);
		expect(readSetting(model, s)).toBe('a-1');
		expect(writeSetting(model, 'b-2', s)).toBe(false);
	});

	it('colours scenes by section and readings as the scene, by default (korg 3495)', () => {
		expect(sceneColours.default).toBe('section');
		expect(sceneColours.choices.map((c) => c.value)).toEqual(['section', 'frame', 'dark', 'light']);
		expect(readingColours.default).toBe('same');
		expect(readingColours.choices.map((c) => c.value)).toEqual(['same', 'light', 'dark']);
	});

	it('keeps brightness under Advanced, as a slider whose default is the palettes as designed', () => {
		for (const b of [lightBrightness, darkBrightness]) {
			expect(b.control).toBe('range');
			expect(b.advanced).toBe(true);
			expect(b.default).toBe('0');
			expect(b.choices.find((c) => c.value === '0')!.label).toBe('As designed');
			const n = b.choices.map((c) => Number(c.value));
			expect(n).toEqual([...n].sort((a, z) => a - z));
		}
		expect(lightBrightness.choices[0].label).toBe('6 steps dimmer');
		expect(darkBrightness.choices.at(-1)!.label).toBe('6 steps lighter');
	});
});

describe('UserSettings', () => {
	it('starts at the defaults and loads what was remembered', () => {
		const s = memory();
		s.map.set('kloom.scene', 'light');
		const settings = new UserSettings([sceneColours, model], () => s);
		expect(settings.get('scene')).toBe('section');
		settings.load();
		expect(settings.get('scene')).toBe('light');
		expect(settings.get('model')).toBe('a-1');
	});

	it('applies and remembers a change, and ignores a bad one', () => {
		const s = memory();
		const settings = new UserSettings([model], () => s);
		settings.set('model', 'b-2');
		expect(settings.get('model')).toBe('b-2');
		expect(s.map.get('test.model')).toBe('b-2');
		settings.set('model', 'nope');
		settings.set('ghost', 'b-2');
		expect(settings.get('model')).toBe('b-2');
		expect(settings.get('ghost')).toBeUndefined();
	});

	it('still applies a change when storage is blocked', () => {
		const settings = new UserSettings([model], () => memory(true));
		settings.load();
		settings.set('model', 'b-2');
		expect(settings.get('model')).toBe('b-2');
	});

	it('takes a setting whose choices were supplied at runtime', () => {
		const fromServer = { models: [{ id: 'x-9', name: 'X' }] };
		const runtime: Setting = {
			...model,
			choices: fromServer.models.map((m) => ({ value: m.id, label: m.name })),
			default: 'x-9'
		};
		const s = memory();
		s.map.set('test.model', 'a-1'); // remembered from an older config
		const settings = new UserSettings([runtime], () => s);
		settings.load();
		expect(settings.get('model')).toBe('x-9');
	});
});

describe('paletteFor', () => {
	const colours = { background: '#0', ink: '#1', muted: '#2', accent: '#3', line: '#4' };
	const palettes: Record<string, Palette> = {
		night: { scheme: 'dark', ...colours, counterpart: 'parchment' },
		parchment: { scheme: 'light', ...colours, counterpart: 'night' },
		ember: { scheme: 'dark', ...colours, counterpart: 'parchment' },
		lone: { scheme: 'light', ...colours }
	};
	const at = (name: string, mode: string) =>
		Object.entries(palettes).find(([, p]) => p === paletteFor({ palettes }, name, mode))![0];

	it('keeps every frame’s own palette for a mode that is not a scheme', () => {
		expect(at('night', 'frame')).toBe('night');
		expect(at('parchment', 'mixed')).toBe('parchment');
	});

	it('swaps to the counterpart only when the scheme differs', () => {
		expect(at('parchment', 'dark')).toBe('night');
		expect(at('night', 'dark')).toBe('night');
		expect(at('ember', 'dark')).toBe('ember');
		expect(at('night', 'light')).toBe('parchment');
		expect(at('ember', 'light')).toBe('parchment');
	});

	it('keeps a palette with no counterpart, and treats an unknown mode as its own', () => {
		expect(at('lone', 'dark')).toBe('lone');
		expect(at('parchment', 'sepia')).toBe('parchment');
	});
});

describe('the old Palette setting, migrated (korg 3495)', () => {
	const after = (old: string | null, set: Record<string, string> = {}) => {
		const s = memory();
		if (old) s.map.set('kloom.palette', old);
		for (const [k, v] of Object.entries(set)) s.map.set(k, v);
		const settings = new UserSettings([sceneColours, readingColours], () => s);
		settings.load();
		return [settings.get('scene'), settings.get('reading')];
	};

	it('carries Mixed to By section and Same as scene', () => {
		expect(after('mixed')).toEqual(['section', 'same']);
	});

	it('carries Dark and Light to Always, scene and reading both', () => {
		expect(after('dark')).toEqual(['dark', 'dark']);
		expect(after('light')).toEqual(['light', 'light']);
	});

	it('leaves the defaults with nothing, or nonsense, remembered', () => {
		expect(after(null)).toEqual(['section', 'same']);
		expect(after('sepia')).toEqual(['section', 'same']);
	});

	it('never overrides a choice made since', () => {
		expect(after('dark', { 'kloom.reading': 'light' })).toEqual(['section', 'light']);
	});

	it('survives blocked storage', () => {
		expect(() => migratePaletteSetting(memory(true))).not.toThrow();
		expect(() => migratePaletteSetting(null)).not.toThrow();
	});
});

describe('framePalettes (korg 3495)', () => {
	const colours = {
		background: '#000000',
		ink: '#ffffff',
		muted: '#bbbbbb',
		accent: '#ffcc00',
		line: '#eeeeee'
	};
	const light = {
		background: '#ffffff',
		ink: '#000000',
		muted: '#555555',
		accent: '#aa2200',
		line: '#222222'
	};
	const subject = {
		palettes: {
			night: { scheme: 'dark', ...colours, counterpart: 'parchment' },
			parchment: { scheme: 'light', ...light, counterpart: 'night' },
			ember: { scheme: 'dark', ...colours, accent: '#ff6600', counterpart: 'scale' },
			scale: { scheme: 'light', ...light, accent: '#993300', counterpart: 'ember' }
		} satisfies Record<string, Palette>
	};
	const p = subject.palettes;
	const c = (
		scene: string,
		reading = 'same',
		bright: Partial<{ light: number; dark: number }> = {}
	) => ({
		scene,
		reading,
		light: 0,
		dark: 0,
		...bright
	});

	it('gives a frame its section’s scheme, keeping its own palette’s family', () => {
		expect(framePalettes(subject, 'ember', 'parchment', c('section')).scene).toBe(p.scale);
		expect(framePalettes(subject, 'ember', 'night', c('section')).scene).toBe(p.ember);
	});

	it('keeps the frame’s own under Each frame, and fixes the scheme under Always', () => {
		expect(framePalettes(subject, 'ember', 'parchment', c('frame')).scene).toBe(p.ember);
		expect(framePalettes(subject, 'ember', 'night', c('light')).scene).toBe(p.scale);
		expect(framePalettes(subject, 'scale', 'parchment', c('dark')).scene).toBe(p.ember);
	});

	it('reads as the scene, or in the scheme the reader fixed for reading', () => {
		const same = framePalettes(subject, 'ember', 'night', c('section'));
		expect(same.reading).toBe(same.scene);
		const apart = framePalettes(subject, 'ember', 'night', c('section', 'light'));
		expect(apart.scene).toBe(p.ember);
		expect(apart.reading).toBe(p.scale);
	});

	it('brightens each scheme by its own slider', () => {
		const { scene, reading } = framePalettes(
			subject,
			'night',
			'night',
			c('dark', 'light', { light: -4, dark: 3 })
		);
		expect(scene.background).not.toBe(p.night.background);
		expect(reading.background).not.toBe(p.parchment.background);
		expect(scene.scheme).toBe('dark');
		expect(reading.scheme).toBe('light');
	});

	it('reads the settings, a step that is not a number counting as none', () => {
		const get = (v: Record<string, string>) => ({ get: (id: string) => v[id] });
		expect(coloursOf(get({}))).toEqual({ scene: 'section', reading: 'same', light: 0, dark: 0 });
		expect(coloursOf(get({ lightBrightness: '-3', darkBrightness: 'x' }))).toMatchObject({
			light: -3,
			dark: 0
		});
	});

	it('takes a section’s palette from its segment, or else its first frame', () => {
		const frames = { a: { scene: { palette: 'ember' } } };
		expect(sectionPalette({ frames }, { frames: ['a'] })).toBe('ember');
		expect(sectionPalette({ frames }, { frames: ['a'], palette: 'night' })).toBe('night');
	});
});

describe('followSpine', () => {
	it('follows by default, under its own kloom.* key', () => {
		expect(followSpine.default).toBe('follow');
		expect(followSpine.storageKey).toBe('kloom.followSpine');
		expect(readSetting(followSpine, null)).toBe('follow');
	});

	it('remembers a reader turning it off', () => {
		const map = new Map<string, string>();
		const storage = { getItem: (k: string) => map.get(k) ?? null, setItem: map.set.bind(map) };
		expect(writeSetting(followSpine, 'manual', storage)).toBe(true);
		expect(readSetting(followSpine, storage)).toBe('manual');
	});
});

describe('layout', () => {
	it('is two panes with tabs by default, under its own kloom.* key', () => {
		expect(layout.default).toBe('tabs');
		expect(layout.storageKey).toBe('kloom.layout');
		expect(readSetting(layout, null)).toBe('tabs');
	});

	it('offers the three-column layout, and the two kept for comparison', () => {
		expect(layout.choices.map((c) => c.value)).toEqual(['tabs', 'columns', 'strip', 'split']);
	});
});

describe('the reader’s keymap (korg 3363, 3493)', () => {
	it('is the defaults with nothing stored, or no storage', () => {
		expect(readKeymap(memory())).toEqual(DEFAULT_KEYS);
		expect(readKeymap(null)).toEqual(DEFAULT_KEYS);
		expect(readKeymap(memory(true))).toEqual(DEFAULT_KEYS);
	});

	it('reads the keys stored before modifiers, a letter or off, unchanged', () => {
		const s = memory();
		s.map.set('kloom.key.sync', 'y');
		s.map.set('kloom.key.bookmark', 'off');
		const keys = readKeymap(s);
		expect(keys.sync).toEqual(plain('y'));
		expect(keys.bookmark).toBeNull();
		expect(keys.trail).toEqual(plain('t'));
		// Read, not rewritten: there is nothing to migrate.
		expect(s.map.get('kloom.key.sync')).toBe('y');
	});

	it('remembers a binding with modifiers, and off, under the same keys', () => {
		const s = memory();
		expect(writeKey('map', parseBinding('alt+m'), s)).toBe(true);
		expect(writeKey('note', null, s)).toBe(true);
		expect(s.map.get('kloom.key.map')).toBe('alt+m');
		expect(s.map.get('kloom.key.note')).toBe('off');
		const keys = readKeymap(s);
		expect(keys.map).toEqual({ ...plain('m'), alt: true });
		expect(keys.note).toBeNull();
		expect(writeKey('map', plain('m'), null)).toBe(false);
		expect(writeKey('map', plain('m'), memory(true))).toBe(false);
	});

	it('falls back to the default for what is not a binding, or one now reserved', () => {
		const s = memory();
		s.map.set('kloom.key.sync', 'ArrowLeft');
		s.map.set('kloom.key.map', 'ctrl+t');
		const keys = readKeymap(s);
		expect(keys.sync).toEqual(plain('s'));
		expect(keys.map).toEqual(plain('m'));
	});

	it('says which shortcut acts when one binding is set for two', () => {
		const keys = { ...DEFAULT_KEYS, trail: plain('s') };
		expect(keyWarnings(keys)).toEqual([
			'S is set for sync the narrative and enter a trail; it will sync the narrative.'
		]);
		expect(keyWarnings({ ...keys, trail: parseBinding('meta+s') })).toEqual([]);
		const both = { ...DEFAULT_KEYS, map: parseBinding('meta+m'), contents: parseBinding('meta+m') };
		expect(keyWarnings(both, true)).toEqual([
			'Cmd+M is set for open the contents and open the map; it will open the contents.'
		]);
		expect(keyWarnings(DEFAULT_KEYS)).toEqual([]);
	});

	it('is loaded, changed and reset through the settings’ keys', () => {
		const s = memory();
		s.map.set('kloom.key.contents', 'shift+c');
		const settings = new UserSettings([sceneColours], () => s);
		expect(settings.keys.map.contents).toEqual(plain('c'));
		settings.load();
		expect(settings.keys.map.contents).toEqual({ ...plain('c'), shift: true });
		settings.keys.set('map', parseBinding('alt+m'));
		expect(s.map.get('kloom.key.map')).toBe('alt+m');
		settings.keys.reset('map');
		expect(settings.keys.map.map).toEqual(plain('m'));
		settings.keys.set('note', null);
		settings.keys.resetAll();
		expect(settings.keys.map).toEqual(DEFAULT_KEYS);
		expect(s.map.get('kloom.key.contents')).toBe('c');
	});
});

import { describe, expect, it } from 'vitest';
import type { Palette } from './model';
import {
	followSpine,
	layout,
	paletteFor,
	paletteMode,
	readSetting,
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

	it('defaults the palette mode to Mixed, which is one of its choices', () => {
		expect(paletteMode.default).toBe('mixed');
		expect(paletteMode.choices.map((c) => c.value)).toEqual(['mixed', 'dark', 'light']);
	});
});

describe('UserSettings', () => {
	it('starts at the defaults and loads what was remembered', () => {
		const s = memory();
		s.map.set('kloom.palette', 'light');
		const settings = new UserSettings([paletteMode, model], () => s);
		expect(settings.get('palette')).toBe('mixed');
		settings.load();
		expect(settings.get('palette')).toBe('light');
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

	it('keeps every frame’s own palette in Mixed', () => {
		expect(at('night', 'mixed')).toBe('night');
		expect(at('parchment', 'mixed')).toBe('parchment');
	});

	it('swaps to the counterpart only when the scheme differs', () => {
		expect(at('parchment', 'dark')).toBe('night');
		expect(at('night', 'dark')).toBe('night');
		expect(at('ember', 'dark')).toBe('ember');
		expect(at('night', 'light')).toBe('parchment');
		expect(at('ember', 'light')).toBe('parchment');
	});

	it('keeps a palette with no counterpart, and treats an unknown mode as Mixed', () => {
		expect(at('lone', 'dark')).toBe('lone');
		expect(at('parchment', 'sepia')).toBe('parchment');
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

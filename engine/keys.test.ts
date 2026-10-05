import { describe, expect, it } from 'vitest';
import {
	bindingOf,
	bindingText,
	DEFAULT_KEYS,
	keyClashes,
	keyName,
	pageKey,
	parseBinding,
	plain,
	reserved,
	splitKey,
	tabKey,
	type Binding,
	type KeyTarget
} from './keys';

/** A stand-in element whose ancestors (itself included) match these selectors. */
const at = (...matches: string[]): KeyTarget => ({
	closest: (selectors) => (selectors.split(',').some((s) => matches.includes(s.trim())) ? {} : null)
});

const slider = at('.spine');
const reading = at('.narrative');
const notes = at('.notes');
const gear = at('.narrative', 'button');
const askBox = at('.ai', 'textarea');
const sendButton = at('.ai', 'button');
const settingsSelect = at('.narrative', '[data-own-keys]', 'select');
const body = at('body');

describe('page keys', () => {
	it('moves the spine with the arrows, Home and End from anywhere but a text field', () => {
		for (const t of [slider, reading, gear, sendButton, body, null]) {
			expect(pageKey('ArrowRight', t)).toBe('next');
			expect(pageKey('ArrowLeft', t)).toBe('previous');
			expect(pageKey('Home', t)).toBe('first');
			expect(pageKey('End', t)).toBe('last');
		}
		expect(pageKey('ArrowRight', askBox)).toBeNull();
		expect(pageKey('ArrowDown', settingsSelect)).toBeNull();
	});

	it('acts on S, T, B, N, A, O, C, R, M, Z, D and W anywhere but a text field or a control that owns its keys (korg 3564)', () => {
		for (const t of [slider, reading, gear, notes, sendButton, body, null]) {
			expect(pageKey('n', t)).toBe('note');
			expect(pageKey('N', t)).toBe('note');
			expect(pageKey('s', t)).toBe('sync');
			expect(pageKey('S', t)).toBe('sync');
			expect(pageKey('t', t)).toBe('trail');
			expect(pageKey('T', t)).toBe('trail');
			expect(pageKey('b', t)).toBe('bookmark');
			expect(pageKey('B', t)).toBe('bookmark');
			expect(pageKey('a', t)).toBe('annotate');
			expect(pageKey('o', t)).toBe('my-notes');
			expect(pageKey('c', t)).toBe('contents');
			expect(pageKey('r', t)).toBe('back');
			expect(pageKey('m', t)).toBe('map');
			expect(pageKey('z', t)).toBe('zoom');
			expect(pageKey('Z', t)).toBe('zoom');
			expect(pageKey('d', t)).toBe('random');
			expect(pageKey('W', t)).toBe('anywhere');
		}
		for (const t of [askBox, settingsSelect]) {
			expect(pageKey('s', t)).toBeNull();
			expect(pageKey('t', t)).toBeNull();
			expect(pageKey('b', t)).toBeNull();
			expect(pageKey('n', t)).toBeNull();
			expect(pageKey('a', t)).toBeNull();
			expect(pageKey('o', t)).toBeNull();
			expect(pageKey('c', t)).toBeNull();
			expect(pageKey('r', t)).toBeNull();
			expect(pageKey('z', t)).toBeNull();
			expect(pageKey('d', t)).toBeNull();
			expect(pageKey('w', t)).toBeNull();
		}
	});

	it('follows the reader’s keymap: a letter moved, and one turned off (korg 3363)', () => {
		const keys = { ...DEFAULT_KEYS, sync: plain('y'), bookmark: null };
		expect(pageKey('y', slider, keys)).toBe('sync');
		expect(pageKey('Y', slider, keys)).toBe('sync');
		expect(pageKey('s', slider, keys)).toBeNull();
		expect(pageKey('b', slider, keys)).toBeNull();
		expect(pageKey('t', slider, keys)).toBe('trail');
		// A remapped key still types in the AI pane's text box.
		expect(pageKey('y', askBox, keys)).toBeNull();
	});

	it('names a letter given to two shortcuts, and the first one acts', () => {
		const keys = { ...DEFAULT_KEYS, note: plain('b') };
		expect(keyClashes(DEFAULT_KEYS)).toEqual([]);
		expect(keyClashes(keys)).toEqual([{ binding: plain('b'), actions: ['bookmark', 'note'] }]);
		expect(pageKey('b', slider, keys)).toBe('bookmark');
	});

	it('sends Esc from anywhere in the AI pane back to the spine, text box included', () => {
		expect(pageKey('Escape', askBox)).toBe('to-spine');
		expect(pageKey('Escape', sendButton)).toBe('to-spine');
	});

	it('leaves a trail on Esc elsewhere, except inside a control that owns its keys', () => {
		expect(pageKey('Escape', slider)).toBe('leave-trail');
		expect(pageKey('Escape', body)).toBe('leave-trail');
		expect(pageKey('Escape', settingsSelect)).toBeNull();
	});

	it('ignores other keys', () => {
		expect(pageKey('x', slider)).toBeNull();
		expect(pageKey('Enter', slider)).toBeNull();
	});
});

const b = (text: string) => parseBinding(text) as Binding;

describe('bindings with modifiers (korg 3493)', () => {
	const alt = (key: string, code?: string) => ({ key, code, altKey: true });

	it('writes a binding in a fixed order and reads it back', () => {
		const binding = { key: 'm', shift: true, alt: true, ctrl: true, meta: true };
		expect(bindingText(binding)).toBe('ctrl+alt+shift+meta+m');
		expect(parseBinding('meta+shift+alt+ctrl+m')).toEqual(binding);
		expect(parseBinding('Alt+M')).toEqual({ ...plain('m'), alt: true });
		expect(parseBinding('f2')).toEqual(plain('f2'));
	});

	it('reads a stored single letter, the format before modifiers, as itself', () => {
		for (const l of 'abcdefghijklmnopqrstuvwxyz') expect(parseBinding(l)).toEqual(plain(l));
	});

	it('refuses what is not a binding', () => {
		for (const t of [
			'',
			'off',
			'alt+',
			'alt+alt+m',
			'super+m',
			'arrowleft',
			'escape',
			'tab',
			'f13',
			'/'
		])
			expect(parseBinding(t)).toBeNull();
	});

	it('names a binding as the reader sees it, Cmd and Option on a Mac', () => {
		expect(keyName(b('alt+m'))).toBe('Alt+M');
		expect(keyName(b('ctrl+shift+5'))).toBe('Ctrl+Shift+5');
		expect(keyName(b('meta+k'), true)).toBe('Cmd+K');
		expect(keyName(b('alt+k'), true)).toBe('Option+K');
	});

	it('takes the physical key when a modifier made another character', () => {
		// Option+M on a Mac is µ; Shift+1 is !.
		expect(bindingOf(alt('µ', 'KeyM'))).toEqual(b('alt+m'));
		expect(bindingOf({ key: '!', code: 'Digit1', shiftKey: true })).toEqual(b('shift+1'));
		expect(bindingOf({ key: 'F2' })).toEqual(plain('f2'));
		expect(bindingOf({ key: 'ArrowLeft', code: 'ArrowLeft' })).toBeNull();
		expect(bindingOf({ key: 'Escape' })).toBeNull();
	});

	it('matches on the key and its modifiers', () => {
		const keys = { ...DEFAULT_KEYS, map: b('alt+m'), contents: b('ctrl+shift+c') };
		expect(pageKey(alt('m', 'KeyM'), slider, keys)).toBe('map');
		expect(pageKey(alt('µ', 'KeyM'), slider, keys)).toBe('map');
		// The plain letter no longer opens the map; Alt with another letter is nothing.
		expect(pageKey('m', slider, keys)).toBeNull();
		expect(pageKey(alt('s', 'KeyS'), slider, keys)).toBeNull();
		expect(pageKey({ key: 'C', ctrlKey: true, shiftKey: true }, slider, keys)).toBe('contents');
		expect(pageKey({ key: 'c', ctrlKey: true }, slider, keys)).toBeNull();
	});

	it('lets Shift off a plain binding, as N has always meant n, but not the other way', () => {
		const keys = { ...DEFAULT_KEYS, sync: b('shift+y') };
		expect(pageKey({ key: 'N', shiftKey: true }, slider)).toBe('note');
		expect(pageKey({ key: 'Y', shiftKey: true }, slider, keys)).toBe('sync');
		expect(pageKey('y', slider, keys)).toBeNull();
	});

	it('acts on a modified binding and a Shift one alike outside the panes', () => {
		const keys = { ...DEFAULT_KEYS, map: b('alt+m'), sync: b('shift+y') };
		for (const t of [sendButton, body, null]) {
			expect(pageKey(alt('m', 'KeyM'), t, keys)).toBe('map');
			expect(pageKey({ key: 'Y', shiftKey: true }, t, keys)).toBe('sync');
		}
	});

	it('never takes a modified binding from a text field or a control that owns its keys', () => {
		const keys = { ...DEFAULT_KEYS, map: b('alt+m') };
		expect(pageKey(alt('µ', 'KeyM'), askBox, keys)).toBeNull();
		expect(pageKey(alt('m', 'KeyM'), settingsSelect, keys)).toBeNull();
	});

	it('leaves the browser its own keys: default shortcuts and fixed keys stand down under a modifier', () => {
		expect(pageKey({ key: 's', ctrlKey: true }, slider)).toBeNull();
		expect(pageKey({ key: 'ArrowLeft', altKey: true }, slider)).toBeNull();
		expect(pageKey({ key: 'Escape', altKey: true }, askBox)).toBeNull();
		// Shift alone does not: Shift+→ still steps, as it did.
		expect(pageKey({ key: 'ArrowRight', shiftKey: true }, slider)).toBe('next');
	});

	it('refuses the bindings a browser or system keeps, with a reason', () => {
		for (const t of [
			'ctrl+t',
			'meta+t',
			'ctrl+w',
			'ctrl+n',
			'ctrl+l',
			'ctrl+r',
			'ctrl+f',
			'ctrl+p',
			'meta+q',
			'ctrl+1',
			'meta+9',
			'f5',
			'shift+f5',
			'alt+f4',
			'f12',
			'ctrl+shift+i',
			'ctrl+shift+t',
			'ctrl+c',
			'alt+d'
		])
			expect(reserved(b(t)), t).toMatch(/belongs to the browser or the system \(.+\)\.$/);
		expect(reserved(b('ctrl+t'))).toBe('Ctrl+T belongs to the browser or the system (a new tab).');
		expect(reserved(b('meta+q'), true)).toBe('Cmd+Q belongs to the browser or the system (quit).');
	});

	it('allows the rest: plain letters, Alt and Shift with most, Ctrl with a few', () => {
		for (const t of [
			'm',
			'shift+m',
			'alt+m',
			'alt+shift+m',
			'ctrl+b',
			'ctrl+alt+b',
			'f2',
			'ctrl+i',
			'5',
			'alt+5'
		])
			expect(reserved(b(t)), t).toBeNull();
	});

	it('names a binding given to two shortcuts by its modifiers too', () => {
		const keys = { ...DEFAULT_KEYS, map: b('alt+m'), contents: b('alt+m') };
		expect(keyClashes(keys)).toEqual([{ binding: b('alt+m'), actions: ['contents', 'map'] }]);
		// Alt+M and M are different bindings.
		expect(keyClashes({ ...DEFAULT_KEYS, map: b('alt+m'), sync: plain('m') })).toEqual([]);
	});
});

describe('tab keys', () => {
	it('moves between tabs with the arrows, wrapping, and jumps with Home and End', () => {
		expect(tabKey('ArrowRight', 0, 2)).toBe(1);
		expect(tabKey('ArrowRight', 1, 2)).toBe(0);
		expect(tabKey('ArrowLeft', 0, 2)).toBe(1);
		expect(tabKey('ArrowLeft', 1, 3)).toBe(0);
		expect(tabKey('Home', 2, 3)).toBe(0);
		expect(tabKey('End', 0, 3)).toBe(2);
	});

	it('leaves every other key to the page', () => {
		for (const key of ['ArrowUp', 'ArrowDown', 'Escape', 's', 'Enter', ' ']) {
			expect(tabKey(key, 0, 2)).toBeNull();
		}
	});
});

describe('divider keys', () => {
	it('moves a side-by-side divider with Left and Right, a stacked one with Up and Down', () => {
		expect(splitKey('ArrowLeft', 'vertical')).toBe(-1);
		expect(splitKey('ArrowRight', 'vertical')).toBe(1);
		expect(splitKey('ArrowUp', 'horizontal')).toBe(-1);
		expect(splitKey('ArrowDown', 'horizontal')).toBe(1);
		expect(splitKey('ArrowUp', 'vertical')).toBeNull();
		expect(splitKey('ArrowLeft', 'horizontal')).toBeNull();
	});

	it('jumps with Home and End, and resets with Enter', () => {
		expect(splitKey('Home', 'vertical')).toBe('min');
		expect(splitKey('End', 'horizontal')).toBe('max');
		expect(splitKey('Enter', 'vertical')).toBe('reset');
		expect(splitKey('s', 'vertical')).toBeNull();
	});
});

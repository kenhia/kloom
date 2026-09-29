import { describe, expect, it } from 'vitest';
import { pageKey, splitKey, tabKey, type KeyTarget } from './keys';

/** A stand-in element whose ancestors (itself included) match these selectors. */
const at = (...matches: string[]): KeyTarget => ({
	closest: (selectors) => (selectors.split(',').some((s) => matches.includes(s.trim())) ? {} : null)
});

const slider = at('.spine');
const reading = at('.narrative');
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

	it('acts on S, T and B only in the spine or the narrative (WCAG 2.1.4)', () => {
		for (const t of [slider, reading, gear]) {
			expect(pageKey('s', t)).toBe('sync');
			expect(pageKey('S', t)).toBe('sync');
			expect(pageKey('t', t)).toBe('trail');
			expect(pageKey('T', t)).toBe('trail');
			expect(pageKey('b', t)).toBe('bookmark');
			expect(pageKey('B', t)).toBe('bookmark');
		}
		for (const t of [askBox, sendButton, settingsSelect, body, null]) {
			expect(pageKey('s', t)).toBeNull();
			expect(pageKey('t', t)).toBeNull();
			expect(pageKey('b', t)).toBeNull();
		}
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

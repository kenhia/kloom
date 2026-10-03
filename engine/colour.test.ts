import { readdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';
import { describe, expect, it } from 'vitest';
import { brighten, contrast, fromOklch, MIN_CONTRAST, toOklch } from './colour';
import type { Palette } from './model';
import { darkBrightness, lightBrightness } from './settings';

const night: Palette = {
	scheme: 'dark',
	background: '#0b0b0d',
	ink: '#ece4d0',
	muted: '#9a927f',
	accent: '#d9a441',
	line: '#d9a441'
};
const parchment: Palette = {
	scheme: 'light',
	background: '#efe6d2',
	ink: '#241d14',
	muted: '#6c5f4b',
	accent: '#b3261e',
	line: '#3a3024'
};

describe('OKLCH and contrast', () => {
	it('round-trips sRGB through OKLCH', () => {
		for (const c of ['#000000', '#ffffff', '#b3261e', '#0e2a47', '#7fd1a8', '#fff'])
			expect(fromOklch(toOklch(c))).toBe(c.length === 4 ? '#ffffff' : c);
	});

	it('puts black at lightness 0 and white at 1', () => {
		expect(toOklch('#000000').l).toBeCloseTo(0, 5);
		expect(toOklch('#ffffff').l).toBeCloseTo(1, 5);
	});

	it('measures WCAG contrast: 21 for black on white, 1 for a colour on itself', () => {
		expect(contrast('#000000', '#ffffff')).toBeCloseTo(21, 5);
		expect(contrast('#777777', '#777777')).toBe(1);
		expect(contrast('#ffffff', '#767676')).toBeCloseTo(4.54, 2);
	});
});

describe('brighten (korg 3495)', () => {
	it('is the palette itself at zero steps', () => {
		expect(brighten(parchment, 0)).toBe(parchment);
	});

	it('dims a light background and lifts a dark one, keeping the scheme', () => {
		const dim = brighten(parchment, -4);
		expect(toOklch(dim.background).l).toBeLessThan(toOklch(parchment.background).l);
		expect(dim.scheme).toBe('light');
		const lifted = brighten(night, 4);
		expect(toOklch(lifted.background).l).toBeGreaterThan(toOklch(night.background).l);
	});

	it('pushes a foreground that falls short back over the minimum', () => {
		// A muted colour that only just passes on its own background.
		const tight: Palette = { ...parchment, muted: '#767676', background: '#ffffff' };
		const out = brighten(tight, -6);
		expect(contrast(out.muted, out.background)).toBeGreaterThanOrEqual(MIN_CONTRAST);
	});
});

/**
 * The guarantee the sliders' ranges are chosen for: every palette of every
 * subject keeps MIN_CONTRAST for ink, muted, accent and line at every step,
 * both ends included. A range that is widened past where this holds fails here.
 */
describe('every subject’s palettes across the brightness range', () => {
	const root = join(import.meta.dirname, '..', 'subjects');
	const palettes = readdirSync(root, { withFileTypes: true })
		.filter((d) => d.isDirectory() && !d.name.startsWith('.'))
		.flatMap((d) => {
			const m = JSON.parse(readFileSync(join(root, d.name, 'subject.json'), 'utf8'));
			return Object.entries(m.palettes as Record<string, Palette>).map(
				([name, p]) => [`${d.name}/${name}`, p] as const
			);
		});
	const range = (s: typeof lightBrightness) => s.choices.map((c) => Number(c.value));

	it('finds palettes of both schemes to check', () => {
		expect(palettes.some(([, p]) => p.scheme === 'light')).toBe(true);
		expect(palettes.some(([, p]) => p.scheme === 'dark')).toBe(true);
	});

	it('keeps text and lines at 4.5:1 or better at every step', () => {
		const short: string[] = [];
		for (const [name, p] of palettes)
			for (const n of range(p.scheme === 'light' ? lightBrightness : darkBrightness)) {
				const b = brighten(p, n);
				for (const key of ['ink', 'muted', 'accent', 'line'] as const) {
					const r = contrast(b[key], b.background);
					if (r < MIN_CONTRAST) short.push(`${name} at ${n}: ${key} ${r.toFixed(2)}`);
				}
			}
		expect(short).toEqual([]);
	});

	it('moves every background at the ends of the range', () => {
		for (const [name, p] of palettes) {
			const r = range(p.scheme === 'light' ? lightBrightness : darkBrightness);
			for (const n of [r[0], r.at(-1)!])
				expect(brighten(p, n).background, `${name} at ${n}`).not.toBe(p.background);
		}
	});
});

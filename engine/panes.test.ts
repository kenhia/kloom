import { describe, expect, it } from 'vitest';
import { bounds, PANES_KEY, panesFor, readPanes, resize, writePanes } from './panes';

const store = () => {
	const map = new Map<string, string>();
	return { map, getItem: (k: string) => map.get(k) ?? null, setItem: map.set.bind(map) };
};

describe('pane sizes', () => {
	it('starts each layout at its designed proportions', () => {
		expect(panesFor({}, 'tabs')).toEqual({ spine: 0.6, ai: 0.25, upper: 0.6 });
		expect(panesFor({}, 'columns').spine).toBeCloseTo(5 / 12);
	});

	it('keeps the spine between a quarter and three quarters of the page', () => {
		expect(bounds(panesFor({}, 'tabs'), 'tabs', 'spine')).toEqual({ min: 0.25, max: 0.75 });
		expect(resize(panesFor({}, 'tabs'), 'tabs', 'spine', 0.05).spine).toBe(0.25);
		expect(resize(panesFor({}, 'tabs'), 'tabs', 'spine', 0.95).spine).toBe(0.75);
	});

	it('leaves the narrative at least a fifth of the page in three columns', () => {
		const p = { spine: 0.5, ai: 0.25, upper: 0.6 };
		expect(bounds(p, 'columns', 'spine').max).toBeCloseTo(0.55);
		expect(bounds(p, 'columns', 'ai').max).toBeCloseTo(0.3);
		expect(resize(p, 'columns', 'ai', 0.9).ai).toBeCloseTo(0.3);
	});

	it('changes only the divider it was given', () => {
		const p = resize(panesFor({}, 'split'), 'split', 'upper', 0.3);
		expect(p).toEqual({ spine: 0.6, ai: 0.25, upper: 0.3 });
	});

	it('remembers sizes per layout, and ignores anything it did not write', () => {
		const s = store();
		const saved = writePanes({}, 'tabs', { spine: 0.4, ai: 0.25, upper: 0.6 }, s);
		expect(readPanes(s)).toEqual(saved);
		expect(panesFor(readPanes(s), 'tabs').spine).toBe(0.4);
		expect(panesFor(readPanes(s), 'columns').spine).toBeCloseTo(5 / 12);
		s.map.set(PANES_KEY, '{"tabs":{"spine":"wide"},"columns":{"spine":7}}');
		expect(panesFor(readPanes(s), 'tabs').spine).toBe(0.6);
		expect(panesFor(readPanes(s), 'columns').spine).toBeCloseTo(5 / 12);
		s.map.set(PANES_KEY, 'not json');
		expect(readPanes(s)).toEqual({});
		expect(readPanes(null)).toEqual({});
	});
});

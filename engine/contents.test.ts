import { join } from 'node:path';
import { beforeAll, describe, expect, it } from 'vitest';
import { contentsCount, contentsOf, filterContents, openTrails } from './contents';
import { loadSubject } from './load';
import type { Subject } from './model';

const dir = (id: string) => join(import.meta.dirname, '..', 'subjects', id);

let civ: Subject;
beforeAll(async () => {
	civ = await loadSubject(dir('western-civ'));
});

describe('a subject’s contents', () => {
	it('lists every frame once, by segment, with trails under their anchors', () => {
		const contents = contentsOf(civ);
		expect(contents.map((s) => s.id)).toEqual(civ.spine.segments.map((s) => s.id));
		expect(contentsCount(contents)).toBe(Object.keys(civ.frames).length);
		const press = contents.flatMap((s) => s.entries).find((e) => e.id === 'printing-press')!;
		expect(press.trails.map((t) => t.id)).toContain('printing');
		expect(press.title).toBe(
			`${civ.frames['printing-press'].scene.headline} ${civ.frames['printing-press'].scene.accent}`
		);
		expect(press.position).toBe(civ.frames['printing-press'].position.label);
	});

	it('lists every frame of a long subject too', async () => {
		const ai = await loadSubject(dir('ai'));
		expect(contentsCount(contentsOf(ai))).toBe(Object.keys(ai.frames).length);
	});
});

describe('filtering the contents', () => {
	it('changes nothing with an empty query', () => {
		const contents = contentsOf(civ);
		expect(filterContents(contents, '  ')).toBe(contents);
	});

	it('keeps frames whose title or position has the words, ignoring case', () => {
		const press = civ.frames['printing-press'];
		const byTitle = filterContents(contentsOf(civ), press.scene.headline.toUpperCase());
		expect(byTitle.flatMap((s) => s.entries).map((e) => e.id)).toContain('printing-press');
		const byPosition = filterContents(contentsOf(civ), press.position.label);
		expect(byPosition.flatMap((s) => s.entries).map((e) => e.id)).toContain('printing-press');
	});

	it('keeps a trail frame’s anchor so the trail has somewhere to hang, and drops empty segments', () => {
		const printing = civ.trails.find((t) => t.id === 'printing')!;
		const inner = civ.frames[printing.spine.segments[0].frames.at(-1)!];
		const found = filterContents(contentsOf(civ), inner.scene.accent);
		const anchor = found.flatMap((s) => s.entries).find((e) => e.id === 'printing-press')!;
		expect(anchor.trails[0].frames.map((f) => f.id)).toContain(inner.id);
		expect(found.every((s) => s.entries.length)).toBe(true);
		expect(filterContents(contentsOf(civ), 'no frame says this')).toEqual([]);
	});

	it('keeps a trail whole when its title matches', () => {
		const printing = civ.trails.find((t) => t.id === 'printing')!;
		const found = filterContents(contentsOf(civ), printing.title);
		const anchor = found.flatMap((s) => s.entries).find((e) => e.id === 'printing-press')!;
		expect(anchor.trails[0].frames).toHaveLength(
			printing.spine.segments.reduce((n, s) => n + s.frames.length, 0)
		);
	});
});

describe('the trails open at first', () => {
	it('is the trail the reader is on, or those from their frame, or none', () => {
		expect(openTrails(civ, 'anything', 'measure')).toEqual(new Set(['measure']));
		expect(openTrails(civ, 'printing-press', null)).toEqual(new Set(['printing']));
		expect(openTrails(civ, civ.spine.segments[0].frames[0], null)).toEqual(new Set());
	});
});

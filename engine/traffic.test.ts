import { join } from 'node:path';
import { beforeAll, describe, expect, it } from 'vitest';
import { loadSubject } from './load';
import type { Subject } from './model';
import { levelOf, trafficRow } from './traffic';

let civ: Subject;
beforeAll(async () => {
	civ = await loadSubject(join(import.meta.dirname, '..', 'subjects', 'western-civ'));
});

describe('a traffic level (korg 3570)', () => {
	it('counts distinct readers in five steps: 0, 1, 2, 3, then 4 or more', () => {
		expect([0, 1, 2, 3, 4, 5, 40].map(levelOf)).toEqual([0, 1, 2, 3, 4, 4, 4]);
	});
});

describe('a subject’s traffic row', () => {
	it('has a cell per frame in spine order, each trail’s after its anchor', () => {
		const row = trafficRow(civ, { 'printing-press': { readers: 3, visits: 9 } });
		expect(row.cells).toHaveLength(Object.keys(civ.frames).length);
		const ids = row.cells.map((c) => c.id);
		const printing = civ.trails.find((t) => t.id === 'printing')!;
		const trailIds = printing.spine.segments.flatMap((s) => s.frames);
		const anchorAt = ids.indexOf('printing-press');
		expect(ids.slice(anchorAt + 1, anchorAt + 1 + trailIds.length)).toEqual(trailIds);
		expect(row.cells[anchorAt]).toMatchObject({ trail: null, readers: 3, visits: 9, level: 3 });
		expect(row.cells[anchorAt + 1]).toMatchObject({
			trail: printing.title,
			readers: 0,
			level: 0
		});
		// The main spine's frames, without the trails, keep their order.
		const main = civ.spine.segments.flatMap((s) => s.frames);
		expect(row.cells.filter((c) => !c.trail).map((c) => c.id)).toEqual(main);
	});
});

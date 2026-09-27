import { readFileSync } from 'node:fs';
import { join } from 'node:path';
import { describe, expect, it } from 'vitest';
import { citationProblems } from '$engine/citation';
import { illustrationProblem } from '$engine/validate';
import { loomCredit } from './credit';

describe('the start screen art', () => {
	const svg = readFileSync(join(import.meta.dirname, 'loom.svg'), 'utf8');

	it('is credited with a valid media citation', () => {
		expect(citationProblems(loomCredit)).toEqual([]);
		expect(loomCredit.licence).toBe('Public domain');
	});

	it('is a drawing and nothing more, ready to draw on', () => {
		expect(illustrationProblem(svg)).toBeNull();
		expect(svg.match(/<path pathLength="1"/g)).toHaveLength(8);
	});
});

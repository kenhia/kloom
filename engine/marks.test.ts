import { describe, expect, it } from 'vitest';
import { hasMarks, marksText, NO_MARKS } from './marks';

describe('a frame’s marks in words', () => {
	it('names each kind the frame has, counting the ones that come in numbers', () => {
		expect(marksText({ bookmarked: true, kept: 2, notes: 1, fresh: true })).toEqual([
			'new to you',
			'bookmarked',
			'2 kept answers',
			'1 note'
		]);
		expect(marksText({ bookmarked: false, kept: 1, notes: 3, fresh: false })).toEqual([
			'1 kept answer',
			'3 notes'
		]);
	});

	it('says nothing for a frame with none', () => {
		expect(marksText(NO_MARKS)).toEqual([]);
		expect(hasMarks(NO_MARKS)).toBe(false);
		expect(hasMarks({ ...NO_MARKS, notes: 1 })).toBe(true);
		expect(hasMarks({ ...NO_MARKS, fresh: true })).toBe(true);
	});
});

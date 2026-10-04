import { describe, expect, it } from 'vitest';
import { inViewShift } from './in-view';

describe('inViewShift (korg 3552)', () => {
	it('leaves a pop-up already in view where it is', () => {
		expect(inViewShift(100, 500, 1000)).toBe(0);
	});
	it('moves one past the left edge right, to the margin', () => {
		// The contents panel under a HUD button 304px from the window's left, 450px wide.
		expect(inViewShift(-146, 304, 900)).toBe(154);
	});
	it('moves one past the right edge left', () => {
		expect(inViewShift(700, 1020, 1000)).toBe(-28);
	});
	it('keeps the left edge in view when it is wider than the window', () => {
		expect(inViewShift(-50, 1100, 1000)).toBe(58);
	});
});

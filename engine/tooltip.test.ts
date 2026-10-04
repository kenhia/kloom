import { describe, expect, it } from 'vitest';
import { placeTip, TIP_DELAY, TIP_WARM, tipWait } from './tooltip';

const viewport = { width: 1000, height: 800 };
const tip = { width: 100, height: 24 };

describe('placeTip', () => {
	it('centres a tooltip under its control', () => {
		expect(placeTip({ left: 400, top: 10, width: 32, height: 32 }, tip, viewport)).toEqual({
			left: 366,
			top: 48
		});
	});

	it('goes above a control with no room below', () => {
		expect(placeTip({ left: 400, top: 770, width: 32, height: 24 }, tip, viewport).top).toBe(740);
	});

	it('stays below when there is no room above either', () => {
		const short = { width: 1000, height: 60 };
		expect(placeTip({ left: 400, top: 4, width: 32, height: 32 }, tip, short).top).toBe(42);
	});

	it('slides along to stay inside the viewport at either side', () => {
		expect(placeTip({ left: 980, top: 10, width: 16, height: 16 }, tip, viewport).left).toBe(892);
		expect(placeTip({ left: 0, top: 10, width: 16, height: 16 }, tip, viewport).left).toBe(8);
	});
});

describe('tipWait', () => {
	it('waits the delay for the first tooltip', () => {
		expect(tipWait(10_000, null, false)).toBe(TIP_DELAY);
		expect(tipWait(10_000, 10_000 - TIP_WARM - 1, false)).toBe(TIP_DELAY);
	});

	it('shows the next at once while one shows or has just hidden', () => {
		expect(tipWait(10_000, null, true)).toBe(0);
		expect(tipWait(10_000, 10_000 - TIP_WARM + 1, false)).toBe(0);
	});

	it('keeps the delay under the browser’s own two seconds', () => {
		expect(TIP_DELAY).toBeGreaterThanOrEqual(300);
		expect(TIP_DELAY).toBeLessThanOrEqual(500);
	});
});

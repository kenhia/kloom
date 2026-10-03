import { describe, expect, it } from 'vitest';
import { RateLimit } from './rate-limit';

const policy = { free: 3, base: 1000, max: 8000, forget: 60_000 };

function setup() {
	let t = 0;
	return { limit: new RateLimit(policy, () => t), pass: (ms: number) => (t += ms) };
}

describe('sign-in backoff', () => {
	it('lets the free tries through, then locks the key out', () => {
		const { limit } = setup();
		for (let i = 0; i < policy.free - 1; i++) {
			limit.fail(['user ada']);
			expect(limit.wait(['user ada'])).toBe(0);
		}
		limit.fail(['user ada']);
		expect(limit.wait(['user ada'])).toBe(1000);
		expect(limit.wait(['user bob'])).toBe(0);
	});

	it('doubles the lockout with each failure after, up to the ceiling', () => {
		const { limit, pass } = setup();
		const waits = [];
		for (let i = 0; i < 7; i++) {
			limit.fail(['k']);
			waits.push(limit.wait(['k']));
			pass(limit.wait(['k']));
		}
		expect(waits).toEqual([0, 0, 1000, 2000, 4000, 8000, 8000]);
	});

	it('answers with the longest wait among the keys asked about', () => {
		const { limit } = setup();
		for (let i = 0; i < 4; i++) limit.fail(['user ada']);
		for (let i = 0; i < 3; i++) limit.fail(['address 1.2.3.4']);
		expect(limit.wait(['user ada', 'address 1.2.3.4'])).toBe(2000);
	});

	it('forgets a key after a success, or after a quiet hour', () => {
		const { limit, pass } = setup();
		for (let i = 0; i < 3; i++) limit.fail(['a', 'b']);
		limit.succeed(['a']);
		expect(limit.wait(['a'])).toBe(0);
		pass(policy.forget + 1);
		limit.fail(['b']);
		expect(limit.wait(['b'])).toBe(0);
	});
});

import { describe, expect, it } from 'vitest';
import { clamp, cursorAt, indexLabel, stops, WheelGate } from './navigation';

describe('stops', () => {
	it('flattens segments in order and keeps each frame’s segment', () => {
		const spine = {
			segments: [
				{ id: 'a', title: 'A', labelKind: 'date' as const, frames: ['one'] },
				{ id: 'b', title: 'B', labelKind: 'technology' as const, frames: ['two', 'three'] }
			]
		};
		expect(stops(spine).map((s) => `${s.segment.id}:${s.frameId}`)).toEqual([
			'a:one',
			'b:two',
			'b:three'
		]);
	});
});

describe('HUD arithmetic', () => {
	it('clamps to the spine', () => {
		expect([clamp(-1, 3), clamp(1, 3), clamp(5, 3)]).toEqual([0, 1, 2]);
	});

	it('pads the index to at least two digits', () => {
		expect(indexLabel(0, 3)).toBe('01 / 03');
		expect(indexLabel(41, 120)).toBe('042 / 120');
	});

	it('puts the cursor at the ends and in between', () => {
		expect([cursorAt(0, 3), cursorAt(1, 3), cursorAt(2, 3), cursorAt(0, 1)]).toEqual([
			0, 0.5, 1, 0
		]);
	});
});

describe('WheelGate', () => {
	it('turns one mouse notch into one step each way', () => {
		const gate = new WheelGate();
		expect(gate.push(100, 0)).toBe(1);
		expect(gate.push(-100, 1000)).toBe(-1);
	});

	it('moves one frame for a whole trackpad gesture, inertia included', () => {
		const gate = new WheelGate();
		const steps = Array.from({ length: 40 }, (_, i) => gate.push(8, i * 10));
		expect(steps.filter((s) => s !== 0)).toEqual([1]);
	});

	it('forgets a half-made gesture after a pause', () => {
		const gate = new WheelGate();
		expect(gate.push(40, 0)).toBe(0);
		expect(gate.push(40, 1000)).toBe(0);
	});
});

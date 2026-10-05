import { describe, expect, it } from 'vitest';
import { clamp, cursorAt, indexLabel, segmentStep, stops, WheelGate } from './navigation';

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

describe('segmentStep (PageUp, PageDown; korg 3568)', () => {
	const seg = (id: string, frames: string[]) => ({
		id,
		title: id,
		labelKind: 'date' as const,
		frames
	});
	// 0 | 1 2 3 | 4 5
	const path = stops({
		segments: [seg('a', ['f0']), seg('b', ['f1', 'f2', 'f3']), seg('c', ['f4', 'f5'])]
	});

	it('goes forward to the first frame of the next segment', () => {
		expect(segmentStep(path, 0, 1)).toBe(1);
		expect(segmentStep(path, 1, 1)).toBe(4);
		expect(segmentStep(path, 2, 1)).toBe(4);
	});

	it('does nothing forward from the last segment', () => {
		expect(segmentStep(path, 4, 1)).toBeNull();
		expect(segmentStep(path, 5, 1)).toBeNull();
	});

	it('goes back to this segment’s first frame, or the previous one’s from there', () => {
		expect(segmentStep(path, 3, -1)).toBe(1);
		expect(segmentStep(path, 2, -1)).toBe(1);
		expect(segmentStep(path, 1, -1)).toBe(0);
		expect(segmentStep(path, 5, -1)).toBe(4);
		expect(segmentStep(path, 4, -1)).toBe(1);
	});

	it('does nothing back from the very first frame', () => {
		expect(segmentStep(path, 0, -1)).toBeNull();
	});

	it('steps a one-segment spine (a trail) to its start, and no further', () => {
		const trail = stops({ segments: [seg('t', ['x', 'y', 'z'])] });
		expect(segmentStep(trail, 2, -1)).toBe(0);
		expect(segmentStep(trail, 0, -1)).toBeNull();
		expect(segmentStep(trail, 0, 1)).toBeNull();
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

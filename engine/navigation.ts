import type { Segment, Spine } from './model';

/** One position on a spine, with the segment that labels it. */
export interface Stop {
	frameId: string;
	segment: Segment;
}

/** A spine flattened into the positions the cursor steps through. */
export const stops = (spine: Spine): Stop[] =>
	spine.segments.flatMap((segment) => segment.frames.map((frameId) => ({ frameId, segment })));

export const clamp = (i: number, length: number) => Math.min(Math.max(i, 0), length - 1);

/** The HUD's top-right index, zero-padded to the width of the total: "02 / 12". */
export function indexLabel(i: number, length: number): string {
	const width = String(length).length < 2 ? 2 : String(length).length;
	const pad = (n: number) => String(n).padStart(width, '0');
	return `${pad(i + 1)} / ${pad(length)}`;
}

/** Where the timeline cursor sits, 0..1. */
export const cursorAt = (i: number, length: number) => (length <= 1 ? 0 : i / (length - 1));

/** How the narrative pane follows the spine (docs/design.md §Interaction). */
export type SyncMode = 'manual' | 'follow';

/**
 * Turns a stream of wheel deltas into single steps along the spine.
 * Trackpads send dozens of small deltas per gesture and keep sending them as
 * inertia; one gesture should move one frame. Deltas accumulate until they
 * pass `threshold`, then nothing moves again until `cooldown` ms have passed,
 * and a pause of `idle` ms forgets a half-made gesture.
 */
export class WheelGate {
	private total = 0;
	private lastEvent = -Infinity;
	private lastStep = -Infinity;

	constructor(
		private readonly threshold = 60,
		private readonly cooldown = 450,
		private readonly idle = 200
	) {}

	/** Feed one wheel delta (pixels); returns the step to take: -1, 0 or 1. */
	push(delta: number, now: number): -1 | 0 | 1 {
		if (now - this.lastEvent > this.idle) this.total = 0;
		this.lastEvent = now;
		if (now - this.lastStep < this.cooldown) {
			this.total = 0;
			return 0;
		}
		this.total += delta;
		if (Math.abs(this.total) < this.threshold) return 0;
		const step = this.total > 0 ? 1 : -1;
		this.total = 0;
		this.lastStep = now;
		return step;
	}
}

import type { SubjectHead } from './model';
import { stops } from './navigation';

/**
 * Random jumps (docs/design.md §Random, korg 3437): a frame in this subject,
 * or anywhere in the library, but never the one the reader is on.
 */

/** Every frame a spine walks: the main spine's, then each trail's. */
export const walkedFrames = (subject: SubjectHead): string[] => [
	...stops(subject.spine).map((s) => s.frameId),
	...subject.trails.flatMap((t) => stops(t.spine).map((s) => s.frameId))
];

/**
 * One of `items` at random, never `current`: it is left out before the draw,
 * so every other item is equally likely. Null when there is no other.
 */
export function pickOther<T>(
	items: readonly T[],
	current: T | null,
	random: () => number = Math.random
): T | null {
	const others = items.filter((i) => i !== current);
	if (!others.length) return null;
	return others[Math.min(others.length - 1, Math.floor(random() * others.length))];
}

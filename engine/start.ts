import { stops } from './navigation';
import { sectionPalette } from './settings';
import type { Palette, Subject } from './model';

/**
 * How a subject looks on the start screen: its palettes and the name of the
 * one it opens in (its first section's, then its first frame's), and a sample of its frames'
 * illustrations to draw in a ring around the loom (docs/design.md §Start
 * screen). The illustrations are the loader's own sanitised markup.
 */
export interface StartLook {
	palettes: Record<string, Palette>;
	palette: string;
	illustrations: string[];
}

/** About as many as fit around the loom without crowding it. */
export const RING = 10;

/**
 * The subject's start look. The sample is spread evenly along the main spine,
 * so a long subject shows its whole sweep rather than its first few frames.
 */
export function startLook(subject: Subject, n = RING): StartLook {
	const drawn = stops(subject.spine)
		.map((s) => subject.frames[s.frameId]?.svg)
		.filter((svg): svg is string => !!svg);
	const count = Math.min(n, drawn.length);
	return {
		palettes: subject.palettes,
		palette: sectionPalette(subject, subject.spine.segments[0]),
		illustrations: Array.from(
			{ length: count },
			(_, i) => drawn[Math.floor((i * drawn.length) / count)]
		)
	};
}

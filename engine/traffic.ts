/**
 * The traffic page's grid (docs/design.md §Traffic, korg 3570): a row per
 * subject and a cell per frame, in the contents' order (§Contents), so each
 * trail's frames follow the frame it branches from. A cell's level counts
 * the distinct readers who opened the frame, in GitHub's five steps.
 */

import { contentsOf } from './contents';
import type { SubjectHead } from './model';

/** The brightest level: this many readers, or more. */
export const TOP_LEVEL = 4;

/** A frame's level from its readers: 0, 1, 2, 3, then 4 for more than 3. */
export const levelOf = (readers: number) => Math.min(Math.max(0, readers), TOP_LEVEL);

export interface TrafficCount {
	readers: number;
	visits: number;
}

export interface TrafficCell extends TrafficCount {
	id: string;
	title: string;
	position: string;
	/** The trail it is on, by title; null on the main spine. */
	trail: string | null;
	level: number;
}

export interface TrafficRow {
	subject: string;
	title: string;
	cells: TrafficCell[];
}

/** One subject's row, from its frames' counts (a frame nobody opened has none). */
export function trafficRow(subject: SubjectHead, counts: Record<string, TrafficCount>): TrafficRow {
	const cell = (
		f: { id: string; title: string; position: string },
		trail: string | null
	): TrafficCell => {
		const c = counts[f.id] ?? { readers: 0, visits: 0 };
		return { ...f, trail, readers: c.readers, visits: c.visits, level: levelOf(c.readers) };
	};
	return {
		subject: subject.id,
		title: subject.title,
		cells: contentsOf(subject).flatMap((s) =>
			s.entries.flatMap((e) => [
				cell(e, null),
				...e.trails.flatMap((t) => t.frames.map((f) => cell(f, t.title)))
			])
		)
	};
}

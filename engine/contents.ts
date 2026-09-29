/**
 * A subject's table of contents (docs/design.md §Contents, korg 3433): the
 * main spine's frames by segment, each trail under the frame it branches
 * from, and a filter for long subjects. The shell draws it; this decides
 * what is in it.
 */

import type { Frame, Subject, Trail } from './model';

export interface ContentsFrame {
	id: string;
	/** The scene's headline and accent, as the rest of the shell names a frame. */
	title: string;
	/** The position label: a date, a category, a technology. */
	position: string;
}

export interface ContentsTrail {
	id: string;
	title: string;
	frames: ContentsFrame[];
}

/** A main-spine frame, with the trails that branch from it. */
export interface ContentsEntry extends ContentsFrame {
	trails: ContentsTrail[];
}

export interface ContentsSegment {
	id: string;
	title: string;
	entries: ContentsEntry[];
}

const entryOf = (f: Frame): ContentsFrame => ({
	id: f.id,
	title: `${f.scene.headline} ${f.scene.accent}`,
	position: f.position.label
});

const trailOf = (t: Trail, frames: Subject['frames']): ContentsTrail => ({
	id: t.id,
	title: t.title,
	frames: t.spine.segments.flatMap((s) => s.frames.map((id) => entryOf(frames[id])))
});

export function contentsOf(subject: Subject): ContentsSegment[] {
	return subject.spine.segments.map((s) => ({
		id: s.id,
		title: s.title,
		entries: s.frames.map((id) => ({
			...entryOf(subject.frames[id]),
			trails: subject.trails.filter((t) => t.anchor === id).map((t) => trailOf(t, subject.frames))
		}))
	}));
}

/**
 * The contents narrowed to what `query` names, ignoring case: a frame whose
 * title or position has it, and a trail whose title has it, whole. A frame
 * stays when a trail under it matches, so the trail has somewhere to hang.
 * An empty query changes nothing.
 */
export function filterContents(contents: ContentsSegment[], query: string): ContentsSegment[] {
	const q = query.trim().toLowerCase();
	if (!q) return contents;
	const has = (s: string) => s.toLowerCase().includes(q);
	const hit = (f: ContentsFrame) => has(f.title) || has(f.position);
	return contents
		.map((s) => ({
			...s,
			entries: s.entries
				.map((e) => ({
					...e,
					trails: e.trails
						.map((t) => (has(t.title) ? t : { ...t, frames: t.frames.filter(hit) }))
						.filter((t) => t.frames.length)
				}))
				.filter((e) => hit(e) || e.trails.length)
		}))
		.filter((s) => s.entries.length);
}

/** How many frames the contents list, trails included. */
export const contentsCount = (contents: ContentsSegment[]) =>
	contents.reduce(
		(n, s) =>
			n + s.entries.reduce((m, e) => m + 1 + e.trails.reduce((k, t) => k + t.frames.length, 0), 0),
		0
	);

/**
 * The trails open when the contents open: the one the reader is on, or
 * those branching from the frame they are on.
 */
export function openTrails(subject: Subject, frame: string, trail: string | null): Set<string> {
	if (trail) return new Set([trail]);
	return new Set(subject.trails.filter((t) => t.anchor === frame).map((t) => t.id));
}

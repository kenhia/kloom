/**
 * How a subject is served (docs/design.md §Serving, korg 3460): the page
 * carries the subject's head, every frame's small half, and each frame's
 * body (its reading, drawing, citations and links) is fetched as the reader
 * comes to it, with its neighbours fetched ahead. Browser-safe: the compiler
 * and the store that build and read these live in `content-db.ts`.
 */

import type { FrameLinks } from './graph';
import type { Citation, Frame, FrameBody, FrameHead, Subject, SubjectHead } from './model';
import { stops } from './navigation';

/** What the frame endpoint sends: the body, and the frame's links as the library has them now. */
export interface ServedBody extends FrameBody {
	links: FrameLinks;
}

/** What ask gives the model of a frame: the reading as authored, and its citations. */
export interface FrameSource {
	reading: string;
	citations: Citation[];
}

/** How many frames either side of the reader's are fetched ahead. */
export const AHEAD = 2;

/** A frame's head: everything but its body. */
export function headOf(frame: Frame): FrameHead {
	// eslint-disable-next-line @typescript-eslint/no-unused-vars
	const { citations, sources, readingHtml, svg, edits, ...head } = frame;
	return head;
}

/** A frame's body: what its head leaves out. */
export const bodyOf = (frame: Frame): FrameBody => ({
	citations: frame.citations,
	sources: frame.sources,
	readingHtml: frame.readingHtml,
	svg: frame.svg,
	edits: frame.edits
});

/** A whole subject as its page carries it: the same, with every frame cut to its head. */
export const subjectHeadOf = (subject: Subject): SubjectHead => ({
	...subject,
	frames: Object.fromEntries(Object.entries(subject.frames).map(([id, f]) => [id, headOf(f)]))
});

/** What a frame shows until its body arrives: nothing to read yet. */
export const PENDING: ServedBody = {
	citations: [],
	sources: [],
	readingHtml: '',
	svg: null,
	edits: [],
	links: { connections: [], names: {} }
};

/**
 * The frames around `id` on the spine that walks it, the main one or a
 * trail's: itself first, then the nearest either side, out to `n`. Empty for
 * a frame no spine walks.
 */
export function around(subject: SubjectHead, id: string, n = AHEAD): string[] {
	for (const spine of [subject.spine, ...subject.trails.map((t) => t.spine)]) {
		const path = stops(spine).map((s) => s.frameId);
		const at = path.indexOf(id);
		if (at < 0) continue;
		const out = [id];
		for (let d = 1; d <= n; d++) {
			if (at + d < path.length) out.push(path[at + d]);
			if (at - d >= 0) out.push(path[at - d]);
		}
		return out;
	}
	return [];
}

import type { Citation } from './citation';

export type { Citation } from './citation';

/**
 * The content model, engine-level and subject-agnostic (docs/design.md
 * §Content model). Nothing here assumes the spine is time: each segment says
 * what kind of position label its frames carry.
 */

/** What a segment's position labels mean. Only `date` segments are ordered. */
export const LABEL_KINDS = ['date', 'category', 'technology'] as const;
export type LabelKind = (typeof LABEL_KINDS)[number];

/** A contiguous run of a spine with its own label kind. */
export interface Segment {
	id: string;
	title: string;
	labelKind: LabelKind;
	/** Frame ids, in spine order. */
	frames: string[];
}

/** An ordered list of frames, split into segments. The scroller walks it. */
export interface Spine {
	segments: Segment[];
}

/** A small spine anchored to one frame of the main spine. */
export interface Trail {
	id: string;
	title: string;
	/** The main-spine frame this trail branches from. */
	anchor: string;
	spine: Spine;
}

export interface Position {
	/** What the HUD shows bottom-left: "c. 3200 BC", "Transformers". */
	label: string;
	/** Sort key; required, and non-decreasing, within a `date` segment. */
	sort?: number;
}

export interface Source {
	title: string;
	url?: string;
	note?: string;
}

/** The scene half of a frame: what the spine scroller shows. */
export interface Scene {
	headline: string;
	/** The one word set in the accent colour after the headline. */
	accent: string;
	/** A palette name the subject defines. */
	palette: string;
	/** File name of an SVG line drawing in the frame's directory. */
	illustration?: string;
	/** Small monospace lines under the headline. */
	metadata: string[];
	counter?: { value: string; label?: string };
}

/** A frame as authored in `frame.json`; the reading lives in `reading.md`. */
export interface FrameFile {
	id: string;
	position: Position;
	scene: Scene;
	/** Required and non-empty: this is history written with an LLM. */
	sources: Source[];
	/**
	 * Where each piece of information and each image came from, structured and
	 * rendered in Chicago style under Sources. Every image or chart the reading
	 * uses needs a `media` entry here.
	 */
	citations?: Citation[];
}

/** A frame ready to render: both halves, markdown already turned to HTML. */
export interface Frame extends FrameFile {
	readingHtml: string;
	/** The illustration's markup, inlined so it can draw itself on. */
	svg: string | null;
}

export interface Palette {
	scheme: 'dark' | 'light';
	background: string;
	ink: string;
	muted: string;
	accent: string;
	line: string;
	/**
	 * The palette of the other scheme that stands in for this one when the
	 * reader picks an all-dark or all-light palette mode. Without one, this
	 * palette is kept in every mode.
	 */
	counterpart?: string;
}

/** `subject.json`: the subject's own name and theme. */
export interface Manifest {
	title: string;
	palettes: Record<string, Palette>;
}

export interface Subject {
	id: string;
	title: string;
	palettes: Record<string, Palette>;
	spine: Spine;
	trails: Trail[];
	frames: Record<string, Frame>;
}

import type { Citation, Source } from './citation';

export type { Citation, Source } from './citation';

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
	/**
	 * The section's palette (korg 3495): its frames take this palette's scheme
	 * when the reader colours scenes by section. Optional; the first frame's
	 * palette stands in.
	 */
	palette?: string;
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
	/**
	 * A dedication set as a name rather than a headline (sprint 028): a small
	 * line above it ("Dedicated to"), the name in its own case, and an optional
	 * line directly under it ("Retired"). The scene shows it in place of the
	 * headline, with the metadata below; the headline and accent still name the
	 * frame everywhere else (contents, map, screen readers).
	 */
	dedication?: { kicker: string; name: string; note?: string };
}

/**
 * A connection from one frame to another, in this subject or another
 * (docs/design.md §Connections). Stored on one side and shown on both.
 */
export interface Connection {
	/** `<subject>/<frame>`. */
	to: string;
	/** What connects them, in a sentence: required. */
	why: string;
}

/** A frame as authored in `frame.json`; the reading lives in `reading.md`. */
export interface FrameFile {
	id: string;
	/**
	 * What the frame is about, in a short plain title ("Alignment faking"):
	 * the headline is evocative and the position label may be a date, so this
	 * is what names a frame where it stands alone, as on the map (sprint 020).
	 */
	topic: string;
	position: Position;
	scene: Scene;
	/**
	 * Where each piece of information and each image came from, structured and
	 * rendered in Chicago style under Sources. Required, with at least one
	 * flagged `key`: this is history written with an LLM, and the key
	 * citations are the frame's Sources list (sprint 008). Every image or
	 * chart the reading uses needs a `media` entry here.
	 */
	citations: Citation[];
	/**
	 * `YYYY-MM` or `YYYY-MM-DD`: when a time-sensitive frame (the current state
	 * of something) was last true. Shown in the reading pane, and given to ask.
	 */
	asOf?: string;
	connections?: Connection[];
}

/**
 * A frame's head: what every frame of a subject sends with the page, for the
 * spine's ticks, the contents, the HUD and the scene's words (docs/design.md
 * §Serving). Small: no reading, no drawing, no citations.
 */
export type FrameHead = Omit<FrameFile, 'citations'>;

/** A frame's body: what is fetched as the reader comes to it (§Serving). */
export interface FrameBody {
	citations: Citation[];
	/** The Sources list, derived from the key citations. */
	sources: Source[];
	readingHtml: string;
	/** The illustration's markup, inlined so it can draw itself on. */
	svg: string | null;
}

/** A frame ready to render: both halves, markdown already turned to HTML. */
export interface Frame extends FrameFile, FrameBody {}

export interface Palette {
	scheme: 'dark' | 'light';
	background: string;
	ink: string;
	muted: string;
	accent: string;
	line: string;
	/**
	 * The palette of the other scheme that stands in for this one when the
	 * frame is to wear that scheme: by section, or always dark or light.
	 * Without one, this palette is kept in every mode.
	 */
	counterpart?: string;
}

/** `subject.json`: the subject's own name and theme. */
export interface Manifest {
	title: string;
	/** A line said with the title ("creating the objects around us"); optional. */
	subtitle?: string;
	palettes: Record<string, Palette>;
}

/** A subject as its page has it: every frame's head, no frame's body (§Serving). */
export interface SubjectHead {
	id: string;
	title: string;
	subtitle?: string;
	palettes: Record<string, Palette>;
	spine: Spine;
	trails: Trail[];
	frames: Record<string, FrameHead>;
}

/** A subject loaded whole, every frame rendered: what the compiler builds from. */
export interface Subject extends Omit<SubjectHead, 'frames'> {
	frames: Record<string, Frame>;
}

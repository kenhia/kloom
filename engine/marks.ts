/**
 * The reader's own marks on a spine frame (docs/design.md §Marks): what they
 * bookmarked, kept answers on, or wrote notes on, and what is new to them
 * (added since they started the subject, not yet opened). The content's own mark, a
 * trail branching from the frame, sits above the line; the reader's layer
 * sits below it, each kind in a fixed place and shape.
 *
 * A mark is never only a shape: the same facts are said in words wherever a
 * frame is named (the slider's value text, the tick's title, the
 * announcement), and these are the words.
 */
export interface FrameMarks {
	bookmarked: boolean;
	kept: number;
	notes: number;
	/** New to the reader (korg 3525). */
	fresh: boolean;
}

export const NO_MARKS: FrameMarks = { bookmarked: false, kept: 0, notes: 0, fresh: false };

const count = (n: number, one: string, many: string) => `${n} ${n === 1 ? one : many}`;

/** Said of a frame that is new to the reader, wherever it is named. */
export const FRESH_TEXT = 'new to you';

/** The marks as words, e.g. `["new to you", "bookmarked", "2 kept answers", "1 note"]`. */
export function marksText(m: FrameMarks): string[] {
	return [
		...(m.fresh ? [FRESH_TEXT] : []),
		...(m.bookmarked ? ['bookmarked'] : []),
		...(m.kept ? [count(m.kept, 'kept answer', 'kept answers')] : []),
		...(m.notes ? [count(m.notes, 'note', 'notes')] : [])
	];
}

/** Whether a frame carries any of the reader's marks. */
export const hasMarks = (m: FrameMarks) => m.bookmarked || m.kept > 0 || m.notes > 0 || m.fresh;

/**
 * The page's own keys (docs/design.md §Interaction): which action a key press
 * means, given where focus is. The shell listens on the window and acts on
 * the answer.
 *
 * S, T and B are single-character shortcuts, so WCAG 2.1.4 applies: they act
 * only while focus is in the spine or the narrative pane, never in the AI
 * pane, the settings panel or on the bare page (korg 3366).
 */

export type PageKey =
	| 'next'
	| 'previous'
	| 'first'
	| 'last'
	| 'scroll-down'
	| 'scroll-up'
	| 'sync'
	| 'trail'
	| 'leave-trail'
	| 'bookmark'
	| 'to-spine';

/** The part of an element this needs: tests pass a stand-in. */
export interface KeyTarget {
	closest(selectors: string): unknown;
}

/** Text fields and anything marked `data-own-keys` keep every key but Esc-to-spine. */
export const OWN_KEYS =
	'input[type="text"], input[type="search"], textarea, select, [contenteditable="true"], [data-own-keys]';

/** Where the character shortcuts (S, T, B) act. */
export const SHORTCUT_PANES = '.spine, .narrative';

export function pageKey(key: string, target: KeyTarget | null): PageKey | null {
	const within = (selectors: string) => !!target?.closest(selectors);
	if (key === 'Escape' && within('.ai')) return 'to-spine';
	if (within(OWN_KEYS)) return null;
	switch (key) {
		case 'ArrowRight':
			return 'next';
		case 'ArrowLeft':
			return 'previous';
		case 'Home':
			return 'first';
		case 'End':
			return 'last';
		case 'ArrowDown':
			return 'scroll-down';
		case 'ArrowUp':
			return 'scroll-up';
		case 's':
		case 'S':
			return within(SHORTCUT_PANES) ? 'sync' : null;
		case 't':
		case 'T':
			return within(SHORTCUT_PANES) ? 'trail' : null;
		case 'b':
		case 'B':
			return within(SHORTCUT_PANES) ? 'bookmark' : null;
		case 'Escape':
			return 'leave-trail';
		default:
			return null;
	}
}

/**
 * A key on a tab in a tab list (the ARIA tabs pattern): the tab it moves to,
 * or null when the key is not the tab list's. Left and Right wrap. The tab
 * handles the key and prevents its default, so the page's arrows stand down.
 */
export function tabKey(key: string, index: number, count: number): number | null {
	switch (key) {
		case 'ArrowRight':
			return (index + 1) % count;
		case 'ArrowLeft':
			return (index - 1 + count) % count;
		case 'Home':
			return 0;
		case 'End':
			return count - 1;
		default:
			return null;
	}
}

/**
 * A key on a pane divider (the ARIA window-splitter pattern): a step toward
 * the start (-1) or the end (1) along its own axis, a jump to a limit, or a
 * reset to the layout's own proportions. The divider prevents the key's
 * default, as a tab does.
 */
export function splitKey(
	key: string,
	orientation: 'vertical' | 'horizontal'
): -1 | 1 | 'min' | 'max' | 'reset' | null {
	const [back, forward] =
		orientation === 'vertical' ? ['ArrowLeft', 'ArrowRight'] : ['ArrowUp', 'ArrowDown'];
	switch (key) {
		case back:
			return -1;
		case forward:
			return 1;
		case 'Home':
			return 'min';
		case 'End':
			return 'max';
		case 'Enter':
			return 'reset';
		default:
			return null;
	}
}

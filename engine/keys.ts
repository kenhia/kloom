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

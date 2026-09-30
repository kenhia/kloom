/**
 * The page's own keys (docs/design.md §Interaction): which action a key press
 * means, given where focus is. The shell listens on the window and acts on
 * the answer.
 *
 * S, T, B, N, A, C, R, M, D and W are single-character shortcuts, so WCAG 2.1.4 applies. They
 * act only while focus is in the spine, the narrative or the notes (korg
 * 3366), never in the AI pane, the settings panel or on the bare page. And
 * the reader can remap each to another letter or turn it off (korg 3363):
 * the keymap is theirs, from the settings.
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
	| 'note'
	| 'annotate'
	| 'contents'
	| 'back'
	| 'map'
	| 'random'
	| 'anywhere'
	| 'to-spine';

/** The character shortcuts: the page keys a reader may remap or turn off. */
export type Shortcut =
	| 'sync'
	| 'trail'
	| 'bookmark'
	| 'note'
	| 'annotate'
	| 'contents'
	| 'back'
	| 'map'
	| 'random'
	| 'anywhere';

/** Each shortcut, what it does in a few words, and its letter out of the box. */
export const SHORTCUTS: { action: Shortcut; label: string; key: string }[] = [
	{ action: 'sync', label: 'sync the narrative', key: 's' },
	{ action: 'trail', label: 'enter a trail', key: 't' },
	{ action: 'bookmark', label: 'bookmark', key: 'b' },
	{ action: 'note', label: 'add a note', key: 'n' },
	{ action: 'annotate', label: 'annotate the reading', key: 'a' },
	{ action: 'contents', label: 'open the contents', key: 'c' },
	{ action: 'back', label: 'go back after a jump', key: 'r' },
	{ action: 'map', label: 'open the map', key: 'm' },
	{ action: 'random', label: 'go to a random frame in this subject', key: 'd' },
	{ action: 'anywhere', label: 'go to a random frame anywhere', key: 'w' }
];

/** Which lower-case letter does what; null is turned off. */
export type Keymap = Record<Shortcut, string | null>;

export const DEFAULT_KEYS = Object.fromEntries(SHORTCUTS.map((s) => [s.action, s.key])) as Keymap;

/** A key as the reader sees it written: the letter in capitals. */
export const keyName = (key: string) => key.toUpperCase();

/**
 * Letters the keymap gives to more than one shortcut. The first in
 * `SHORTCUTS` order acts; the settings say so.
 */
export function keyClashes(keys: Keymap): { key: string; actions: Shortcut[] }[] {
	const by = new Map<string, Shortcut[]>();
	for (const { action } of SHORTCUTS) {
		const k = keys[action];
		if (k) by.set(k, [...(by.get(k) ?? []), action]);
	}
	return [...by].filter(([, a]) => a.length > 1).map(([key, actions]) => ({ key, actions }));
}

/** The part of an element this needs: tests pass a stand-in. */
export interface KeyTarget {
	closest(selectors: string): unknown;
}

/** Text fields and anything marked `data-own-keys` keep every key but Esc-to-spine. */
export const OWN_KEYS =
	'input[type="text"], input[type="search"], textarea, select, [contenteditable="true"], [data-own-keys]';

/** Where the character shortcuts act. */
export const SHORTCUT_PANES = '.spine, .narrative, .notes';

export function pageKey(
	key: string,
	target: KeyTarget | null,
	keys: Keymap = DEFAULT_KEYS
): PageKey | null {
	const within = (selectors: string) => !!target?.closest(selectors);
	if (key === 'Escape' && within('.ai')) return 'to-spine';
	if (within(OWN_KEYS)) return null;
	if (key.length === 1) {
		const letter = key.toLowerCase();
		const action = SHORTCUTS.find((s) => keys[s.action] === letter)?.action;
		return action && within(SHORTCUT_PANES) ? action : null;
	}
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

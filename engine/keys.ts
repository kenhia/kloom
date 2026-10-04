/**
 * The page's own keys (docs/design.md §Interaction): which action a key press
 * means, given where focus is. The shell listens on the window and acts on
 * the answer.
 *
 * S, T, B, N, A, O, C, R, M, Z, D and W are the shortcuts out of the box, and
 * the reader can rebind each, modifiers included, or turn it off (korg 3363,
 * 3493): the keymap is theirs, from the keyboard shortcuts dialog. A binding
 * with no Alt, Ctrl or Meta is a character key, so WCAG 2.1.4 applies: it
 * acts only while focus is in the spine, the narrative or the notes (korg
 * 3366), never in the AI pane, the settings or on the bare page. A binding
 * with one of those modifiers is exempt and acts page-wide, except in a text
 * field or a dialog that keeps its own keys.
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
	| 'my-notes'
	| 'contents'
	| 'back'
	| 'map'
	| 'zoom'
	| 'random'
	| 'anywhere'
	| 'to-spine';

/** The shortcuts: the page keys a reader may rebind or turn off. */
export type Shortcut =
	| 'sync'
	| 'trail'
	| 'bookmark'
	| 'note'
	| 'annotate'
	| 'my-notes'
	| 'contents'
	| 'back'
	| 'map'
	| 'zoom'
	| 'random'
	| 'anywhere';

/** Each shortcut, what it does in a few words, and its letter out of the box. */
export const SHORTCUTS: { action: Shortcut; label: string; key: string }[] = [
	{ action: 'sync', label: 'sync the narrative', key: 's' },
	{ action: 'trail', label: 'enter a trail', key: 't' },
	{ action: 'bookmark', label: 'bookmark', key: 'b' },
	{ action: 'note', label: 'add a note', key: 'n' },
	{ action: 'annotate', label: 'annotate the reading', key: 'a' },
	{ action: 'my-notes', label: 'open my notes', key: 'o' },
	{ action: 'contents', label: 'open the contents', key: 'c' },
	{ action: 'back', label: 'go back after a jump', key: 'r' },
	{ action: 'map', label: 'open the map', key: 'm' },
	{ action: 'zoom', label: 'zoom the drawing', key: 'z' },
	{ action: 'random', label: 'go to a random frame in this subject', key: 'd' },
	{ action: 'anywhere', label: 'go to a random frame anywhere', key: 'w' }
];

/**
 * A key and the modifiers held with it. `key` is a lower-case letter, a digit
 * or a function key (`f1`…`f12`): the only keys a shortcut may take.
 */
export interface Binding {
	key: string;
	shift: boolean;
	alt: boolean;
	ctrl: boolean;
	meta: boolean;
}

/** Which binding does what; null is turned off. */
export type Keymap = Record<Shortcut, Binding | null>;

/** A plain key, no modifiers. */
export const plain = (key: string): Binding => ({
	key,
	shift: false,
	alt: false,
	ctrl: false,
	meta: false
});

export const DEFAULT_KEYS = Object.fromEntries(
	SHORTCUTS.map((s) => [s.action, plain(s.key)])
) as Keymap;

/** Alt, Ctrl or Meta held: the binding is not a character key (WCAG 2.1.4). */
export const modified = (b: Binding) => b.alt || b.ctrl || b.meta;

const BINDABLE = /^([a-z0-9]|f([1-9]|1[0-2]))$/;

/**
 * A binding as stored: its modifiers and key joined with `+`, in a fixed
 * order (`ctrl+alt+shift+meta+m`). A plain letter is just the letter, which
 * is what every stored key was before modifiers, so those still read.
 */
export function bindingText(b: Binding): string {
	const mods = (['ctrl', 'alt', 'shift', 'meta'] as const).filter((m) => b[m]);
	return [...mods, b.key].join('+');
}

/** The binding a stored string names, or null when it names none. */
export function parseBinding(text: string): Binding | null {
	const parts = text.toLowerCase().split('+');
	const key = parts.pop()!;
	if (!BINDABLE.test(key)) return null;
	const b = plain(key);
	for (const m of parts) {
		if (m !== 'ctrl' && m !== 'alt' && m !== 'shift' && m !== 'meta') return null;
		if (b[m]) return null;
		b[m] = true;
	}
	return b;
}

/** Two bindings are the same keys. */
export const sameBinding = (a: Binding | null, b: Binding | null) =>
	!!a && !!b && bindingText(a) === bindingText(b);

/**
 * A binding as the reader sees it written: `Alt+M`, `Ctrl+Shift+5`, `F2`.
 * Meta is Cmd on a Mac.
 */
export function keyName(b: Binding, mac = false): string {
	const names = [
		b.ctrl && 'Ctrl',
		b.alt && (mac ? 'Option' : 'Alt'),
		b.shift && 'Shift',
		b.meta && (mac ? 'Cmd' : 'Meta')
	].filter(Boolean);
	return [...names, b.key.toUpperCase()].join('+');
}

/** Whether this is a Mac, where Meta is Cmd and Alt is Option. False on the server. */
export function onMac(): boolean {
	return typeof navigator !== 'undefined' && /Mac|iPhone|iPad/.test(navigator.platform);
}

/** The part of a key press that matters here: tests pass a plain object. */
export interface Press {
	key: string;
	/** The physical key (`KeyM`), for when `key` is a character a modifier made. */
	code?: string;
	shiftKey?: boolean;
	altKey?: boolean;
	ctrlKey?: boolean;
	metaKey?: boolean;
}

/**
 * The bindable key a press is of, lower-cased, or null. With Option on a Mac
 * or Shift on a digit, `key` is the character made (µ, !), so the physical
 * key stands in.
 */
export function pressedKey(p: Press): string | null {
	const key = p.key.toLowerCase();
	if (BINDABLE.test(key)) return key;
	const code = /^(?:Key([A-Z])|Digit([0-9]))$/.exec(p.code ?? '');
	return code ? (code[1] ?? code[2]).toLowerCase() : null;
}

/** The binding a press would make, or null when its key is not bindable. */
export function bindingOf(p: Press): Binding | null {
	const key = pressedKey(p);
	if (!key) return null;
	return {
		key,
		shift: !!p.shiftKey,
		alt: !!p.altKey,
		ctrl: !!p.ctrlKey,
		meta: !!p.metaKey
	};
}

/**
 * Bindings the browser or the system keeps, and what for. Ctrl and Cmd are
 * both checked, since a reader's Ctrl on one machine is Cmd on another.
 * Small on purpose: these are the ones that are taken everywhere.
 */
const WITH_CTRL: Record<string, string> = {
	a: 'select all',
	c: 'copy',
	d: 'bookmark the page',
	e: 'search',
	f: 'find',
	g: 'find again',
	h: 'history, or hide the window',
	j: 'downloads',
	k: 'search',
	l: 'the address bar',
	m: 'minimize the window',
	n: 'a new window',
	o: 'open a file',
	p: 'print',
	q: 'quit',
	r: 'reload',
	s: 'save the page',
	t: 'a new tab',
	u: 'the page source',
	v: 'paste',
	w: 'close the tab',
	x: 'cut',
	y: 'redo, or history',
	z: 'undo'
};
const WITH_CTRL_SHIFT: Record<string, string> = {
	b: 'the bookmarks bar',
	c: 'the developer tools',
	i: 'the developer tools',
	j: 'the developer tools',
	n: 'a private window',
	p: 'a private window',
	t: 'reopen a closed tab'
};
const WITH_ALT: Record<string, string> = {
	d: 'the address bar',
	e: 'the browser menu',
	f: 'the browser menu',
	f4: 'close the window'
};
const FUNCTION_KEYS: Record<string, string> = {
	f1: 'help',
	f3: 'find again',
	f5: 'reload',
	f6: 'the address bar',
	f7: 'caret browsing',
	f11: 'full screen',
	f12: 'the developer tools'
};

/** Why a binding cannot be had, or null when it can. */
export function reserved(b: Binding, mac = false): string | null {
	const name = keyName(b, mac);
	const taken = (what: string) => `${name} belongs to the browser or the system (${what}).`;
	if (FUNCTION_KEYS[b.key]) return taken(FUNCTION_KEYS[b.key]);
	if (b.ctrl || b.meta) {
		if (/^[0-9]$/.test(b.key)) return taken('switch tabs');
		const why = (b.shift && WITH_CTRL_SHIFT[b.key]) || WITH_CTRL[b.key];
		if (why) return taken(why);
	}
	if (b.alt && WITH_ALT[b.key]) return taken(WITH_ALT[b.key]);
	return null;
}

/** The keys kloom keeps for itself, which no shortcut may take. */
export const FIXED_KEYS: { keys: string; does: string }[] = [
	{ keys: '← →', does: 'move along the spine' },
	{ keys: 'Home, End', does: 'go to the first or last frame' },
	{ keys: '↑ ↓', does: 'scroll the reading' },
	{ keys: 'Tab', does: 'move between the panes' },
	{ keys: 'Esc', does: 'leave a trail, close a dialog, or go back to the spine' }
];

/**
 * Bindings the keymap gives to more than one shortcut. The first in
 * `SHORTCUTS` order acts; the shortcuts dialog says so.
 */
export function keyClashes(keys: Keymap): { binding: Binding; actions: Shortcut[] }[] {
	const by = new Map<string, Shortcut[]>();
	for (const { action } of SHORTCUTS) {
		const b = keys[action];
		if (b) by.set(bindingText(b), [...(by.get(bindingText(b)) ?? []), action]);
	}
	return [...by]
		.filter(([, a]) => a.length > 1)
		.map(([text, actions]) => ({ binding: parseBinding(text)!, actions }));
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

/** The shortcut a press is bound to: exact modifiers first, then Shift let off. */
function shortcutOf(p: Press, keys: Keymap): Shortcut | null {
	const b = bindingOf(p);
	if (!b) return null;
	const find = (want: Binding) =>
		SHORTCUTS.find((s) => sameBinding(keys[s.action], want))?.action ?? null;
	// Shift with a plain letter has always meant the letter: N for n.
	return find(b) ?? (b.shift ? find({ ...b, shift: false }) : null);
}

export function pageKey(
	press: Press | string,
	target: KeyTarget | null,
	keys: Keymap = DEFAULT_KEYS
): PageKey | null {
	const p = typeof press === 'string' ? { key: press } : press;
	const within = (selectors: string) => !!target?.closest(selectors);
	const held = !!(p.altKey || p.ctrlKey || p.metaKey);
	if (p.key === 'Escape' && !held && within('.ai')) return 'to-spine';
	if (within(OWN_KEYS)) return null;
	const action = shortcutOf(p, keys);
	if (action) return held || within(SHORTCUT_PANES) ? action : null;
	// The fixed keys stand down under a modifier: Alt+← is the browser's Back.
	if (held) return null;
	switch (p.key) {
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

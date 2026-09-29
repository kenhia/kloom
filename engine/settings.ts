import { SHORTCUTS, type Keymap, type Shortcut } from './keys';
import type { Palette, Subject } from './model';

/**
 * User settings (docs/design.md §Settings): one reader's choices, made in the
 * settings pop-up and remembered per browser. App settings, which belong to
 * the deployment, live in a server config file and are not these.
 *
 * Every setting is a pick from a fixed list; there is no free-text kind. The
 * pop-up renders whatever list it is given, so a setting whose choices come
 * from the server (the ask and grow models) is built at runtime and passed in
 * like any other.
 */
export interface Choice {
	/** What is stored and acted on, e.g. a model id. */
	value: string;
	/** What the reader sees, e.g. a model's display name. */
	label: string;
}

export interface Setting {
	id: string;
	label: string;
	choices: Choice[];
	/** Must be one of `choices`' values. */
	default: string;
	/** The localStorage key it is remembered under. */
	storageKey: string;
	/** A heading the pop-up gathers it under, with the rest of its group. */
	group?: string;
}

/** The part of `Storage` a setting needs; tests pass a Map-backed one. */
export type SettingsStorage = Pick<Storage, 'getItem' | 'setItem'>;

/** localStorage, or null where it is missing or blocked. */
export function browserStorage(): SettingsStorage | null {
	try {
		return globalThis.localStorage ?? null;
	} catch {
		return null;
	}
}

export const isChoice = (setting: Setting, value: unknown): value is string =>
	setting.choices.some((c) => c.value === value);

/**
 * The remembered value, or the default when there is none, storage is
 * blocked, or what is stored is no longer a choice (a model dropped from the
 * app config, say).
 */
export function readSetting(setting: Setting, storage: SettingsStorage | null): string {
	try {
		const stored = storage?.getItem(setting.storageKey);
		if (isChoice(setting, stored)) return stored;
	} catch {
		// Blocked storage: the default is fine.
	}
	return setting.default;
}

/** Remember a value; false when it is not a choice or could not be stored. */
export function writeSetting(
	setting: Setting,
	value: string,
	storage: SettingsStorage | null
): boolean {
	if (!isChoice(setting, value) || !storage) return false;
	try {
		storage.setItem(setting.storageKey, value);
		return true;
	} catch {
		// Not remembered, still applied by the caller.
		return false;
	}
}

export type PaletteMode = 'mixed' | 'dark' | 'light';

/** The palette mode: every frame's own palette, or all dark, or all light. */
export const paletteMode: Setting = {
	id: 'palette',
	label: 'Palette',
	choices: [
		{ value: 'mixed', label: 'Mixed — each frame’s own' },
		{ value: 'dark', label: 'Dark' },
		{ value: 'light', label: 'Light' }
	],
	default: 'mixed',
	storageKey: 'kloom.palette'
};

/**
 * The palette a frame wears under a mode. Mixed, or a palette already of the
 * mode's scheme, keeps the frame's own; otherwise its `counterpart` stands in.
 * A palette with no counterpart keeps itself in every mode.
 */
export function paletteFor(
	subject: Pick<Subject, 'palettes'>,
	name: string,
	mode: string
): Palette {
	const own = subject.palettes[name];
	if (mode !== 'dark' && mode !== 'light') return own;
	if (own.scheme === mode || !own.counterpart) return own;
	return subject.palettes[own.counterpart] ?? own;
}

/**
 * Whether the narrative follows the spine (docs/design.md §Interaction). On by
 * default: moving along the spine turns the reading to that frame. Off, the
 * reading stays where it is until the sync key (S) brings it to the spine.
 */
export const followSpine: Setting = {
	id: 'followSpine',
	label: 'Narrative',
	choices: [
		{ value: 'follow', label: 'Follows the spine' },
		{ value: 'manual', label: 'Stays until synced' }
	],
	default: 'follow',
	storageKey: 'kloom.followSpine'
};

/**
 * Where the AI pane sits (docs/design.md §Layout, korg 3377). Ken's pick is
 * two panes with tabs, and three columns is the alternative. The bottom strip
 * and the right-hand split are kept so they can be compared side by side.
 * Below 760px every layout collapses to one column; tabs keep their tabs.
 */
export const layout: Setting = {
	id: 'layout',
	label: 'Layout',
	choices: [
		{ value: 'tabs', label: 'Two panes, Narrative and AI as tabs' },
		{ value: 'columns', label: 'Three columns' },
		{ value: 'strip', label: 'AI along the bottom' },
		{ value: 'split', label: 'AI below the narrative' }
	],
	default: 'tabs',
	storageKey: 'kloom.layout'
};

export type Layout = 'tabs' | 'columns' | 'strip' | 'split';

/** The ask model's setting id; the AI pane reads the reader's pick under it. */
export const ASK_MODEL = 'askModel';

/** The grow model's setting id; a grow job is queued with the pick made at the time. */
export const GROW_MODEL = 'growModel';

/**
 * A model picker, built at runtime from the choices the server offers (the
 * app config's models). The server re-checks whatever id comes back.
 */
export const modelSetting = (
	id: string,
	label: string,
	offer: { choices: Choice[]; default: string }
): Setting => ({
	id,
	label,
	choices: offer.choices,
	default: offer.default,
	storageKey: `kloom.${id}`
});

const LETTERS: Choice[] = [...'abcdefghijklmnopqrstuvwxyz'].map((l) => ({
	value: l,
	label: l.toUpperCase()
}));

/** What a key setting stores for a shortcut turned off. */
export const KEY_OFF = 'off';

/**
 * A character shortcut's key (korg 3363, WCAG 2.1.4): any letter, or off.
 * Each is a pick from a fixed list like every other setting, and the pop-up
 * gathers them under "Keys".
 */
export const keySettings: Setting[] = SHORTCUTS.map((s) => ({
	id: `key.${s.action}`,
	label: s.label[0].toUpperCase() + s.label.slice(1),
	choices: [...LETTERS, { value: KEY_OFF, label: 'Off' }],
	default: s.key,
	storageKey: `kloom.key.${s.action}`,
	group: 'Keys'
}));

/** The reader's keymap, from their key settings; a shortcut with no setting keeps its letter. */
export function keymapOf(get: (id: string) => string | undefined): Keymap {
	const keys = {} as Keymap;
	for (const s of SHORTCUTS) {
		const v = get(`key.${s.action}`) ?? s.key;
		keys[s.action as Shortcut] = v === KEY_OFF ? null : v;
	}
	return keys;
}

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

/** The ask model's setting id; the AI pane reads the reader's pick under it. */
export const ASK_MODEL = 'askModel';

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

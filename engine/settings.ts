import {
	bindingText,
	DEFAULT_KEYS,
	keyClashes,
	keyName,
	parseBinding,
	reserved,
	SHORTCUTS,
	type Binding,
	type Keymap,
	type Shortcut
} from './keys';
import { brighten } from './colour';
import type { Palette, Segment, Subject } from './model';

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
	/**
	 * How the pop-up shows it: a drop-down (the default), or a slider over
	 * the choices in order, for a setting that is a scale.
	 */
	control?: 'select' | 'range';
	/** Shown under the pop-up's collapsed Advanced disclosure. */
	advanced?: boolean;
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

/**
 * Scene colours (docs/design.md §Colours, korg 3495): the spine's scene, and
 * its HUD, coloured by section (the default), by each frame's own palette,
 * or always dark or always light.
 */
export const sceneColours: Setting = {
	id: 'scene',
	label: 'Scene colours',
	choices: [
		{ value: 'section', label: 'By section' },
		{ value: 'frame', label: 'Each frame' },
		{ value: 'dark', label: 'Always dark' },
		{ value: 'light', label: 'Always light' }
	],
	default: 'section',
	storageKey: 'kloom.scene'
};

/** Reading colours: the reading pane, and the panes beside it, as the scene or always one scheme. */
export const readingColours: Setting = {
	id: 'reading',
	label: 'Reading colours',
	choices: [
		{ value: 'same', label: 'Same as scene' },
		{ value: 'light', label: 'Always light' },
		{ value: 'dark', label: 'Always dark' }
	],
	default: 'same',
	storageKey: 'kloom.reading'
};

/**
 * A brightness setting: steps of BRIGHTNESS_STEP either side of the palettes
 * as designed (0). Still a pick from a fixed list, shown as a slider. The
 * range is where every subject's palettes keep MIN_CONTRAST, which a test
 * checks at both ends.
 */
const brightness = (
	id: string,
	label: string,
	min: number,
	max: number,
	dimmer: string,
	brighter: string
): Setting => ({
	id,
	label,
	choices: Array.from({ length: max - min + 1 }, (_, i) => {
		const n = min + i;
		const steps = Math.abs(n) === 1 ? 'step' : 'steps';
		return {
			value: String(n),
			label: n === 0 ? 'As designed' : `${Math.abs(n)} ${steps} ${n < 0 ? dimmer : brighter}`
		};
	}),
	default: '0',
	storageKey: `kloom.${id}`,
	control: 'range',
	advanced: true
});

/** The light palettes' background: mostly dimmer, for a reader who finds them bright. */
export const lightBrightness = brightness(
	'lightBrightness',
	'Light brightness',
	-6,
	1,
	'dimmer',
	'brighter'
);

/** The dark palettes' background: mostly lifted, toward a softer dark. */
export const darkBrightness = brightness(
	'darkBrightness',
	'Dark brightness',
	-2,
	6,
	'darker',
	'lighter'
);

/** Where sprint 003's single Palette setting was stored: Mixed, Dark or Light. */
export const LEGACY_PALETTE_KEY = 'kloom.palette';

/**
 * Carry a remembered Palette over to the two settings that replaced it, once:
 * Mixed is By section and Same as scene, Dark and Light are Always on both.
 * Nothing is written when either new setting is already remembered.
 */
export function migratePaletteSetting(storage: SettingsStorage | null) {
	try {
		if (!storage) return;
		const old = storage.getItem(LEGACY_PALETTE_KEY);
		if (old !== 'mixed' && old !== 'dark' && old !== 'light') return;
		if (storage.getItem(sceneColours.storageKey) || storage.getItem(readingColours.storageKey))
			return;
		storage.setItem(sceneColours.storageKey, old === 'mixed' ? 'section' : old);
		storage.setItem(readingColours.storageKey, old === 'mixed' ? 'same' : old);
	} catch {
		// Blocked storage: the defaults are fine.
	}
}

/**
 * The palette a frame wears under a scheme. A palette already of that
 * scheme, or anything but `dark` or `light`, keeps the frame's own; otherwise
 * its `counterpart` stands in. A palette with no counterpart keeps itself.
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

/** A section's palette: the one its segment names, or else its first frame's. */
export function sectionPalette(
	subject: { frames: Record<string, { scene: { palette: string } }> },
	segment: Pick<Segment, 'palette' | 'frames'>
): string {
	return segment.palette ?? subject.frames[segment.frames[0]].scene.palette;
}

/** The reader's colour settings, read once for every palette worked out under them. */
export interface Colours {
	scene: string;
	reading: string;
	/** Brightness steps for light and for dark palettes. */
	light: number;
	dark: number;
}

const steps = (v: string | undefined) => (v && Number.isInteger(Number(v)) ? Number(v) : 0);

export function coloursOf(settings: { get(id: string): string | undefined }): Colours {
	return {
		scene: settings.get(sceneColours.id) ?? sceneColours.default,
		reading: settings.get(readingColours.id) ?? readingColours.default,
		light: steps(settings.get(lightBrightness.id)),
		dark: steps(settings.get(darkBrightness.id))
	};
}

/** A palette at the reader's brightness for its scheme. */
export const atBrightness = (p: Palette, c: Pick<Colours, 'light' | 'dark'>) =>
	brighten(p, p.scheme === 'light' ? c.light : c.dark);

/**
 * What a frame wears, scene and reading (korg 3495). By section, the frame's
 * own palette takes its section's scheme through `counterpart`; Each frame
 * keeps its own; Always dark or light is that scheme. The reading is the
 * scene's palette, or its own palette in the scheme the reader fixed. Both
 * at the reader's brightness.
 */
export function framePalettes(
	subject: Pick<Subject, 'palettes'>,
	own: string,
	section: string,
	c: Colours
): { scene: Palette; reading: Palette } {
	const mode = c.scene === 'section' ? subject.palettes[section].scheme : c.scene;
	const scene = paletteFor(subject, own, mode);
	const reading =
		c.reading === 'light' || c.reading === 'dark' ? paletteFor(subject, own, c.reading) : scene;
	return { scene: atBrightness(scene, c), reading: atBrightness(reading, c) };
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

/** What a shortcut's stored value is when it is turned off. */
export const KEY_OFF = 'off';

/** Where a shortcut's binding is remembered: `kloom.key.sync`, and so on. */
export const keyStorageKey = (action: Shortcut) => `kloom.key.${action}`;

/**
 * The reader's keymap, from storage (korg 3363, 3493). Each shortcut is
 * stored as its binding's text (`alt+m`), or `off`. A single letter, which is
 * all a stored key was before modifiers, is read as itself, so those keep
 * working without being rewritten. Anything else, or a binding that has since
 * become reserved, is the default.
 */
export function readKeymap(storage: SettingsStorage | null): Keymap {
	const keys = { ...DEFAULT_KEYS };
	for (const { action } of SHORTCUTS) {
		let stored: string | null = null;
		try {
			stored = storage?.getItem(keyStorageKey(action)) ?? null;
		} catch {
			// Blocked storage: the default is fine.
		}
		if (stored === KEY_OFF) keys[action] = null;
		else if (stored) {
			const b = parseBinding(stored);
			if (b && !reserved(b)) keys[action] = b;
		}
	}
	return keys;
}

/** Remember one shortcut's binding, or that it is off; false when it could not be stored. */
export function writeKey(
	action: Shortcut,
	binding: Binding | null,
	storage: SettingsStorage | null
): boolean {
	if (!storage) return false;
	try {
		storage.setItem(keyStorageKey(action), binding ? bindingText(binding) : KEY_OFF);
		return true;
	} catch {
		return false;
	}
}

/** What the shortcuts dialog says about a keymap: each binding set for two shortcuts, and which wins. */
export function keyWarnings(keys: Keymap, mac = false): string[] {
	return keyClashes(keys).map(({ binding, actions }) => {
		const [first, ...rest] = actions.map((a) => SHORTCUTS.find((s) => s.action === a)!.label);
		return `${keyName(binding, mac)} is set for ${[first, ...rest].join(' and ')}; it will ${first}.`;
	});
}

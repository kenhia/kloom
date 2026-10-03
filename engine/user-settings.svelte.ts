import { DEFAULT_KEYS, plain, SHORTCUTS, type Binding, type Keymap, type Shortcut } from './keys';
import {
	browserStorage,
	migratePaletteSetting,
	readKeymap,
	readSetting,
	writeKey,
	writeSetting,
	type Setting,
	type SettingsStorage
} from './settings';

/**
 * The reader's settings as reactive state. The page makes one and hands it to
 * whatever reads a setting (the shell, the start screen). Values start at the
 * defaults, so the server render and the first client render agree; `load`
 * brings in the remembered ones after mount.
 */
export class UserSettings {
	#values = $state<Record<string, string>>({});
	/** The reader's keyboard shortcuts, which are not picks from a list and so not settings rows. */
	readonly keys: UserKeys;

	constructor(
		readonly list: Setting[],
		private readonly storage: () => SettingsStorage | null = browserStorage
	) {
		for (const s of list) this.#values[s.id] = s.default;
		this.keys = new UserKeys(storage);
	}

	/** The current value, or undefined for a setting not in the list. */
	get(id: string): string | undefined {
		return this.#values[id];
	}

	/** Apply a value and remember it; an unknown setting or choice is ignored. */
	set(id: string, value: string) {
		const setting = this.list.find((s) => s.id === id);
		if (!setting || !setting.choices.some((c) => c.value === value)) return;
		this.#values[id] = value;
		writeSetting(setting, value, this.storage());
	}

	/** Read every remembered value, the shortcuts too. Call from `onMount`. */
	load() {
		const storage = this.storage();
		migratePaletteSetting(storage);
		for (const s of this.list) this.#values[s.id] = readSetting(s, storage);
		this.keys.load();
	}
}

/** The reader's keymap as reactive state (docs/design.md §Keyboard shortcuts). */
export class UserKeys {
	#map = $state<Keymap>({ ...DEFAULT_KEYS });

	constructor(private readonly storage: () => SettingsStorage | null = browserStorage) {}

	get map(): Keymap {
		return this.#map;
	}

	/** Bind a shortcut, or turn it off with null, and remember it. */
	set(action: Shortcut, binding: Binding | null) {
		this.#map[action] = binding;
		writeKey(action, binding, this.storage());
	}

	/** Give a shortcut its key out of the box. */
	reset(action: Shortcut) {
		this.set(action, plain(SHORTCUTS.find((s) => s.action === action)!.key));
	}

	resetAll() {
		for (const { action } of SHORTCUTS) this.reset(action);
	}

	load() {
		this.#map = readKeymap(this.storage());
	}
}

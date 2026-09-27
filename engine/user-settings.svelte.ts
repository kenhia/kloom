import {
	browserStorage,
	readSetting,
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

	constructor(
		readonly list: Setting[],
		private readonly storage: () => SettingsStorage | null = browserStorage
	) {
		for (const s of list) this.#values[s.id] = s.default;
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

	/** Read every remembered value. Call from `onMount`. */
	load() {
		const storage = this.storage();
		for (const s of this.list) this.#values[s.id] = readSetting(s, storage);
	}
}

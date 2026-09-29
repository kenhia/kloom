import type { Layout, SettingsStorage } from './settings';

/**
 * How the reader has sized the panes (docs/design.md §Layout): fractions of
 * the page, one set per layout, dragged at the dividers. `spine` is the spine
 * pane's share of the width, `ai` the AI column's in three columns, and
 * `upper` the narrative's share of the right-hand pane's height in the split.
 * Remembered per browser, like a setting, but a size is not a pick from a
 * list, so it lives beside the settings rather than in them.
 */
export interface Panes {
	spine: number;
	ai: number;
	upper: number;
}
export type Divider = keyof Panes;
export type SavedPanes = Partial<Record<Layout, Panes>>;

export const PANES_KEY = 'kloom.panes';

const DEFAULTS: Record<Layout, Panes> = {
	tabs: { spine: 0.6, ai: 0.25, upper: 0.6 },
	columns: { spine: 5 / 12, ai: 0.25, upper: 0.6 },
	strip: { spine: 0.6, ai: 0.25, upper: 0.6 },
	split: { spine: 0.6, ai: 0.25, upper: 0.6 }
};

/** The least share the narrative keeps in three columns. */
const NARRATIVE_MIN = 0.2;

export const defaultPanes = (layout: Layout): Panes => ({ ...DEFAULTS[layout] });

/** How far a divider may go, given where the others are. */
export function bounds(panes: Panes, layout: Layout, divider: Divider) {
	const three = layout === 'columns';
	switch (divider) {
		case 'spine':
			return { min: 0.25, max: three ? Math.min(0.75, 1 - panes.ai - NARRATIVE_MIN) : 0.75 };
		case 'ai':
			return { min: 0.15, max: Math.min(0.45, 1 - panes.spine - NARRATIVE_MIN) };
		case 'upper':
			return { min: 0.2, max: 0.85 };
	}
}

/** Move one divider, held inside its bounds. */
export function resize(panes: Panes, layout: Layout, divider: Divider, value: number): Panes {
	const { min, max } = bounds(panes, layout, divider);
	return { ...panes, [divider]: Math.min(max, Math.max(min, value)) };
}

const valid = (p: unknown): p is Panes =>
	!!p &&
	typeof p === 'object' &&
	(['spine', 'ai', 'upper'] as const).every((k) => {
		const v = (p as Record<string, unknown>)[k];
		return typeof v === 'number' && v > 0 && v < 1;
	});

/** The sizes a layout opens at: the reader's, or its own. */
export const panesFor = (saved: SavedPanes, layout: Layout): Panes =>
	valid(saved[layout]) ? { ...saved[layout] } : defaultPanes(layout);

/** What was remembered; nothing when storage is blocked or holds something else. */
export function readPanes(storage: SettingsStorage | null): SavedPanes {
	try {
		const parsed = JSON.parse(storage?.getItem(PANES_KEY) ?? '{}');
		return parsed && typeof parsed === 'object' ? parsed : {};
	} catch {
		return {};
	}
}

/** Remember a layout's sizes; returns what is now saved, stored or not. */
export function writePanes(
	saved: SavedPanes,
	layout: Layout,
	panes: Panes,
	storage: SettingsStorage | null
): SavedPanes {
	const next = { ...saved, [layout]: panes };
	try {
		storage?.setItem(PANES_KEY, JSON.stringify(next));
	} catch {
		// Not remembered; still applied.
	}
	return next;
}

/**
 * The HUD's tooltips (docs/design.md §Tooltips, korg 3540): where one goes,
 * and when it shows. The browser's own `title` tooltip waits about two
 * seconds, which no page can change, and never shows on keyboard focus, so
 * the icon-only controls draw their own (engine/ui/tooltip.ts).
 */

/** How long a pointer rests on a control before its tooltip shows. */
export const TIP_DELAY = 400;
/** How long after one tooltip hides that the next shows at once, as the pointer runs along the HUD. */
export const TIP_WARM = 600;
/** How long a tooltip stays after the pointer leaves, so the pointer can move onto it (WCAG 1.4.13). */
export const TIP_GRACE = 120;

export interface Box {
	left: number;
	top: number;
	width: number;
	height: number;
}

/** The gap between a control and its tooltip, and the least room kept to the viewport's edges. */
const GAP = 6;
const MARGIN = 8;

/**
 * Where a tooltip of `tip`'s size goes for a control at `anchor`, in a
 * viewport of `width` × `height`: centred under it, above it when there is no
 * room below, and slid along so it never leaves the viewport's sides.
 */
export function placeTip(
	anchor: Box,
	tip: { width: number; height: number },
	viewport: { width: number; height: number }
): { left: number; top: number } {
	const below = anchor.top + anchor.height + GAP;
	const above = anchor.top - GAP - tip.height;
	const top = below + tip.height <= viewport.height - MARGIN || above < MARGIN ? below : above;
	const centred = anchor.left + anchor.width / 2 - tip.width / 2;
	const left = Math.max(MARGIN, Math.min(centred, viewport.width - MARGIN - tip.width));
	return { left, top };
}

/** How long to wait before showing a tooltip, given when the last one hid (`hidAt`) and now. */
export const tipWait = (now: number, hidAt: number | null, showing: boolean) =>
	showing || (hidAt !== null && now - hidAt < TIP_WARM) ? 0 : TIP_DELAY;

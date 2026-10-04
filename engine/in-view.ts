/**
 * How far to move a pop-up sideways so it stays in the window (korg 3552):
 * the HUD's contents and bookmarks panels hang from their buttons, and every
 * HUD icon added after them moves the buttons left, so a panel that fitted
 * once ran past the window's left edge on a smaller screen. Positive moves
 * it right. A pop-up wider than the window keeps its left edge in view,
 * where its text starts.
 */
export const IN_VIEW_MARGIN = 8;

export function inViewShift(
	left: number,
	right: number,
	viewport: number,
	margin = IN_VIEW_MARGIN
): number {
	if (left < margin) return margin - left;
	if (right > viewport - margin) return Math.max(viewport - margin - right, margin - left);
	return 0;
}

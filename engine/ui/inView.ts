import type { Action } from 'svelte/action';
import { inViewShift } from '../in-view';

/**
 * `use:inView` on a pop-up panel: whenever it is shown or the window
 * changes size, it is moved sideways just enough to stay in the window
 * (engine/in-view.ts, korg 3552). Its CSS places it; this only corrects
 * that, so a new HUD icon beside its button cannot push it off screen.
 */
export const inView: Action<HTMLElement> = (node) => {
	// Placed as the observers report, before the next paint, so it never shows off screen first.
	const place = () => {
		node.style.translate = '';
		if (node.hidden || !node.offsetParent) return;
		const r = node.getBoundingClientRect();
		const shift = inViewShift(r.left, r.right, document.documentElement.clientWidth);
		if (shift) node.style.translate = `${shift}px 0`;
	};
	// Shown and hidden by its `hidden` attribute; resized with its content or the window.
	const shown = new MutationObserver(place);
	shown.observe(node, { attributes: true, attributeFilter: ['hidden'] });
	const sized = new ResizeObserver(place);
	sized.observe(node);
	window.addEventListener('resize', place);
	place();
	return {
		destroy() {
			shown.disconnect();
			sized.disconnect();
			window.removeEventListener('resize', place);
		}
	};
};

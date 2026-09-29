<script lang="ts">
	import { splitKey } from '../keys';

	interface Props {
		/** `vertical` sits between side-by-side panes; `horizontal` between stacked ones. */
		orientation: 'vertical' | 'horizontal';
		/** What it resizes, e.g. "Resize the spine". */
		label: string;
		/** The id of the pane whose size it sets. */
		controls: string;
		/** The size as a fraction, and how far it may go. */
		value: number;
		min: number;
		max: number;
		/** Where the pointer is, as the fraction it asks for. */
		at: (e: PointerEvent) => number;
		onchange: (value: number) => void;
		onreset: () => void;
		/** A placement class, so the shell can put it on the right edge. */
		class?: string;
	}

	let {
		orientation,
		label,
		controls,
		value,
		min,
		max,
		at,
		onchange,
		onreset,
		class: place = ''
	}: Props = $props();

	const STEP = 0.02;
	let dragging = $state(false);

	function keydown(e: KeyboardEvent) {
		const k = splitKey(e.key, orientation);
		if (k === null) return;
		// Handled here, so the page's arrows (the spine) stand down.
		e.preventDefault();
		if (k === 'reset') onreset();
		else onchange(k === 'min' ? min : k === 'max' ? max : value + k * STEP);
	}

	function down(e: PointerEvent) {
		if (e.button !== 0) return;
		e.preventDefault();
		(e.currentTarget as HTMLElement).setPointerCapture(e.pointerId);
		dragging = true;
	}

	function move(e: PointerEvent) {
		if (dragging) onchange(at(e));
	}
</script>

<!-- A focusable separator is interactive (the ARIA window-splitter pattern). -->
<!-- svelte-ignore a11y_no_noninteractive_tabindex, a11y_no_noninteractive_element_interactions -->
<div
	class="splitter {orientation} {place}"
	class:dragging
	role="separator"
	aria-orientation={orientation}
	aria-label={label}
	aria-controls={controls}
	aria-valuenow={Math.round(value * 100)}
	aria-valuemin={Math.round(min * 100)}
	aria-valuemax={Math.round(max * 100)}
	tabindex="0"
	onkeydown={keydown}
	onpointerdown={down}
	onpointermove={move}
	onpointerup={() => (dragging = false)}
	onpointercancel={() => (dragging = false)}
	ondblclick={onreset}
></div>

<style>
	.splitter {
		position: relative;
		z-index: 2;
		touch-action: none;
	}
	.vertical {
		width: 11px;
		cursor: col-resize;
	}
	.horizontal {
		height: 11px;
		cursor: row-resize;
	}
	/* The line shows on hover, focus and drag; the hit area is wider than it. */
	.splitter::after {
		content: '';
		position: absolute;
		background: var(--accent);
		opacity: 0;
		transition: opacity 0.15s;
	}
	.vertical::after {
		inset: 0 4px;
	}
	.horizontal::after {
		inset: 4px 0;
	}
	.splitter:hover::after,
	.splitter:focus-visible::after,
	.dragging::after {
		opacity: 1;
	}
	.splitter:focus-visible {
		outline: none;
	}
	@media (prefers-reduced-motion: reduce) {
		.splitter::after {
			transition: none;
		}
	}
</style>

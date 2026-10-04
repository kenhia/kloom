<script lang="ts">
	import { bindingOf, sameBinding, type Binding } from '../keys';
	import type { Palette } from '../model';

	interface Props {
		/** The frame's drawing, as the scene inlines it. */
		svg: string;
		/** What the dialog is called: the frame's drawing, by its topic. */
		label: string;
		/** The scene's colours, so the drawing looks as it does in the scene. */
		palette: Palette;
		/** The reader's zoom key, which closes it as it opened it. */
		zoomKey: Binding | null;
	}

	let { svg, label, palette, zoomKey }: Props = $props();

	let dialog = $state<HTMLDialogElement>();
	let opener: HTMLElement | null = null;

	export const isOpen = () => !!dialog?.open;

	/** Show the drawing full-screen; focus returns where it was when it closes. */
	export function open() {
		if (!dialog || dialog.open) return;
		opener = document.activeElement instanceof HTMLElement ? document.activeElement : null;
		dialog.showModal();
	}

	export function close() {
		dialog?.close();
	}

	/** The zoom key closes it too: Esc is the dialog's own. */
	function keydown(e: KeyboardEvent) {
		const b = bindingOf(e);
		if (b && zoomKey && (sameBinding(b, zoomKey) || sameBinding({ ...b, shift: false }, zoomKey))) {
			e.preventDefault();
			close();
		}
	}

	/** A click beside the drawing, on the backdrop, closes it. */
	function click(e: MouseEvent) {
		if (e.target === dialog || (e.target as Element).classList?.contains('stage')) close();
	}
</script>

<!-- A modal, like the map: the page behind is inert, its keys stand down, and Esc closes it (§Zoom drawing). -->
<dialog
	class="zoom"
	aria-label={label}
	data-own-keys
	style:--background={palette.background}
	style:--ink={palette.ink}
	style:--muted={palette.muted}
	style:--line={palette.line}
	style:color-scheme={palette.scheme}
	bind:this={dialog}
	onkeydown={keydown}
	onclick={click}
	onclose={() => {
		opener?.focus();
		opener = null;
	}}
>
	<button type="button" class="close" onclick={close}>
		<span aria-hidden="true">×</span>
		<span class="visually-hidden">Close the drawing</span>
	</button>
	<div class="stage">
		<!-- Validated on load, as in the scene: a line drawing, no script or handlers. -->
		<!-- eslint-disable-next-line svelte/no-at-html-tags -->
		{@html svg}
	</div>
</dialog>

<style>
	.zoom {
		width: 100vw;
		height: 100dvh;
		max-width: none;
		max-height: none;
		margin: 0;
		padding: 0;
		border: 0;
		color: var(--line);
		background: var(--background);
	}
	.zoom[open] {
		display: grid;
	}
	.zoom::backdrop {
		background: rgb(0 0 0 / 0.5);
	}
	.stage {
		grid-area: 1 / 1;
		display: grid;
		place-items: center;
		min-height: 0;
		padding: clamp(1rem, 4vmin, 3rem);
	}
	/* The whole drawing, as large as the screen allows, in its own proportions: it is vector, so it stays sharp. */
	.stage :global(svg) {
		display: block;
		width: 100%;
		height: 100%;
		max-height: calc(100dvh - 2 * clamp(1rem, 4vmin, 3rem));
	}
	.close {
		grid-area: 1 / 1;
		z-index: 1;
		justify-self: end;
		align-self: start;
		margin: 0.75rem;
		width: 2.25rem;
		height: 2.25rem;
		padding: 0;
		font: 1.5rem/1 var(--serif, inherit);
		color: var(--ink);
		background: var(--background);
		border: 1px solid var(--muted);
		border-radius: 0.25rem;
		cursor: pointer;
	}
	.close:hover {
		border-color: var(--ink);
	}
</style>

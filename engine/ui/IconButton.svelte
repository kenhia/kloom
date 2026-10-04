<script lang="ts">
	import type { Snippet } from 'svelte';
	import type { HTMLButtonAttributes } from 'svelte/elements';
	import { tooltip } from './tooltip';

	interface Props extends Omit<HTMLButtonAttributes, 'children'> {
		/** Its name, for assistive technology; the icon says it to the eye. */
		label: string;
		/** Its tooltip, when it says more than the label: the shortcut, a count. */
		tip?: string;
		/** The icon: a 24×24 stroked SVG in `currentColor`. */
		children: Snippet;
	}

	let { label, tip, children, class: className = '', ...rest }: Props = $props();

	let button = $state<HTMLButtonElement>();

	export function focus() {
		button?.focus();
	}
</script>

<!-- The shell's small square icon buttons (the gear, Home): one look, not copies of it. -->
<!-- Its tooltip (§Tooltips) says the label, and the shortcut where there is one. -->
<button
	type="button"
	class="icon-button {className}"
	bind:this={button}
	use:tooltip={tip ?? label}
	{...rest}
>
	{@render children()}
	<span class="visually-hidden">{label}</span>
</button>

<style>
	.icon-button {
		display: grid;
		place-items: center;
		width: 2rem;
		height: 2rem;
		padding: 0;
		color: var(--muted);
		background: none;
		border: 1px solid transparent;
		border-radius: 0.25rem;
		cursor: pointer;
	}
	.icon-button:not([aria-disabled='true']):hover,
	.icon-button[aria-expanded='true'] {
		color: var(--ink);
		border-color: var(--muted);
	}
	/* Unavailable here, and still focusable, so its tooltip can say why. */
	.icon-button[aria-disabled='true'] {
		opacity: 0.4;
		cursor: default;
	}
	.icon-button :global(svg) {
		width: 1.25rem;
		height: 1.25rem;
	}
</style>

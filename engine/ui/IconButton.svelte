<script lang="ts">
	import type { Snippet } from 'svelte';
	import type { HTMLButtonAttributes } from 'svelte/elements';

	interface Props extends Omit<HTMLButtonAttributes, 'children'> {
		/** Its name, for assistive technology; the icon says it to the eye. */
		label: string;
		/** The icon: a 24×24 stroked SVG in `currentColor`. */
		children: Snippet;
	}

	let { label, children, class: className = '', ...rest }: Props = $props();

	let button = $state<HTMLButtonElement>();

	export function focus() {
		button?.focus();
	}
</script>

<!-- The shell's small square icon buttons (the gear, Home): one look, not copies of it. -->
<button type="button" class="icon-button {className}" bind:this={button} {...rest}>
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
	.icon-button:hover,
	.icon-button[aria-expanded='true'] {
		color: var(--ink);
		border-color: var(--muted);
	}
	.icon-button :global(svg) {
		width: 1.25rem;
		height: 1.25rem;
	}
</style>

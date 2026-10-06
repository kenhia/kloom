<script lang="ts">
	import type { Snippet } from 'svelte';

	/**
	 * A page of plain words outside the shell: signing in, a welcome link,
	 * and the Welcome and How-To page. One readable column that keeps to a
	 * phone's width and to large text, in the reader's light or dark. `wide`
	 * lets a page of figures (the traffic page) use a desktop's width.
	 */
	let {
		title,
		wide = false,
		children
	}: { title: string; wide?: boolean; children: Snippet } = $props();
</script>

<svelte:head>
	<title>{title} · kloom</title>
</svelte:head>

<main class="plain" class:wide>
	<p class="brand" aria-hidden="true">kloom</p>
	{@render children()}
</main>

<style>
	.plain {
		--ink: #ebe6da;
		--muted: #b4ad9e;
		--accent: #e2b45f;
		--line: #4a463e;
		--field: #16161a;
		box-sizing: border-box;
		max-width: 40rem;
		min-height: 100dvh;
		margin: 0 auto;
		padding: 2rem 1.25rem 4rem;
		color: var(--ink);
		font: 1.0625rem/1.6 var(--sans);
	}
	.plain.wide {
		max-width: 72rem;
	}
	@media (prefers-color-scheme: light) {
		:global(html:has(.plain)),
		:global(body:has(.plain)) {
			background: #f6f2e8;
			color-scheme: light;
		}
		.plain {
			--ink: #1f1c17;
			--muted: #5c564b;
			--accent: #8a5a00;
			--line: #c9c1b0;
			--field: #fffdf8;
		}
	}
	.brand {
		margin: 0 0 1.5rem;
		font: 0.8rem var(--mono);
		letter-spacing: 0.3em;
		text-transform: uppercase;
		color: var(--muted);
	}
	.plain :global(h1) {
		margin: 0 0 1rem;
		font: 2rem/1.2 var(--serif);
	}
	.plain :global(h2) {
		margin: 2.25rem 0 0.5rem;
		padding-top: 1rem;
		font: 1.35rem/1.3 var(--serif);
		border-top: 1px solid var(--line);
	}
	.plain :global(p),
	.plain :global(ul) {
		margin: 0 0 0.85rem;
	}
	.plain :global(li) {
		margin-bottom: 0.4rem;
	}
	.plain :global(a) {
		color: var(--accent);
		text-underline-offset: 0.2em;
	}
	.plain :global(kbd) {
		font: 0.85em var(--mono);
		padding: 0 0.3em;
		border: 1px solid var(--muted);
		border-radius: 0.2em;
	}
	.plain :global(form) {
		display: grid;
		gap: 0.9rem;
		max-width: 24rem;
	}
	.plain :global(label) {
		display: grid;
		gap: 0.3rem;
	}
	.plain :global(input) {
		font: inherit;
		padding: 0.55rem 0.7rem;
		color: var(--ink);
		background: var(--field);
		border: 1px solid var(--muted);
		border-radius: 0.3rem;
	}
	.plain :global(button) {
		justify-self: start;
		font: inherit;
		padding: 0.55rem 1.4rem;
		color: var(--field);
		background: var(--accent);
		border: 0;
		border-radius: 0.3rem;
		cursor: pointer;
	}
	.plain :global(:focus-visible) {
		outline: 2px solid var(--accent);
		outline-offset: 2px;
	}
	.plain :global(.problem) {
		padding: 0.6rem 0.8rem;
		border-left: 3px solid var(--accent);
		background: color-mix(in srgb, var(--accent) 12%, transparent);
	}
	.plain :global(.hint) {
		font-size: 0.9rem;
		color: var(--muted);
	}
</style>

<script lang="ts">
	import { onMount } from 'svelte';
	import { bibliography, chicago, type Citation } from '../citation';
	import type { Palette } from '../model';

	interface Props {
		/** The subject's title, set large. */
		title: string;
		/** A line under the title. */
		subtitle?: string;
		/** Set around the rotating dial, one letter at a time. */
		inscription: string;
		/** A line drawing to draw on in the centre, or null until it loads. */
		art: string | null;
		/** Where the art came from; shown collapsed at the foot. */
		credits: Citation[];
		/** The colours to use: the start screen wears the first frame's. */
		palette: Palette;
		onbegin: () => void;
	}

	let { title, subtitle, inscription, art, credits, palette, onbegin }: Props = $props();

	let button = $state<HTMLButtonElement>();
	let leaving = $state(false);

	onMount(() => button?.focus());

	function begin() {
		if (leaving) return;
		leaving = true;
		const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
		setTimeout(onbegin, reduced ? 0 : 500);
	}

	/** Keys stop here: the shell behind must not move while this is open. */
	function keydown(e: KeyboardEvent) {
		e.stopPropagation();
		if (e.key === 'Escape') {
			e.preventDefault();
			begin();
		}
	}

	const R = 190;
	const ticks = Array.from({ length: 120 }, (_, i) => i * 3);
	const letters = $derived([...inscription]);
</script>

<!-- A modal landing: the shell behind is inert until Begin. -->
<div
	class="start"
	class:leaving
	role="dialog"
	aria-modal="true"
	aria-labelledby="start-title"
	aria-describedby="start-subtitle"
	tabindex="-1"
	style:--start-background={palette.background}
	style:--start-ink={palette.ink}
	style:--start-muted={palette.muted}
	style:--start-accent={palette.accent}
	style:--start-line={palette.line}
	style:color-scheme={palette.scheme}
	onkeydown={keydown}
>
	<div class="stage" aria-hidden="true">
		<svg class="dial" viewBox="-220 -220 440 440" fill="none" stroke="currentColor">
			<circle r={R + 14} stroke-width="0.6" />
			<circle r={R} stroke-width="0.8" />
			<circle r={R - 34} stroke-width="0.5" />
			{#each ticks as a (a)}
				<line
					x1="0"
					y1={-R}
					x2="0"
					y2={-R - (a % 30 === 0 ? 14 : a % 15 === 0 ? 9 : 5)}
					stroke-width={a % 30 === 0 ? 1 : 0.5}
					transform="rotate({a})"
				/>
			{/each}
			<g class="inscription" fill="currentColor" stroke="none">
				{#each letters as letter, i (i)}
					<text
						y={-R + 22}
						text-anchor="middle"
						font-size="12"
						transform="rotate({(i * 360) / letters.length})">{letter}</text
					>
				{/each}
			</g>
		</svg>
		{#if art}
			<div class="art">
				<!-- The app's own drawing, from the repository (src/lib/start). -->
				<!-- eslint-disable-next-line svelte/no-at-html-tags -->
				{@html art}
			</div>
		{/if}
	</div>

	<div class="copy">
		<h2 id="start-title">{title}</h2>
		{#if subtitle}<p id="start-subtitle" class="subtitle">{subtitle}</p>{/if}
		<button type="button" class="begin" bind:this={button} onclick={begin}>
			Begin <kbd>Enter</kbd>
		</button>
	</div>

	{#if credits.length}
		<details class="credits">
			<summary>Image credit</summary>
			<ul>
				{#each bibliography(credits) as citation, i (i)}
					<li>
						{#each chicago(citation) as part, j (j)}
							{#if part.href}
								<!-- An external source, not an app route. -->
								<!-- eslint-disable-next-line svelte/no-navigation-without-resolve -->
								<a href={part.href} rel="noopener noreferrer">{part.text}</a>
							{:else if part.italic}<i>{part.text}</i>{:else}{part.text}{/if}
						{/each}
					</li>
				{/each}
			</ul>
		</details>
	{/if}
</div>

<style>
	.start {
		position: fixed;
		inset: 0;
		z-index: 10;
		display: grid;
		grid-template-rows: minmax(0, 1fr) auto auto;
		justify-items: center;
		padding: 1.5rem 1rem 1rem;
		overflow: hidden;
		color: var(--start-ink);
		background: var(--start-background);
		transition: opacity 0.5s ease-in-out;
	}
	.start:focus {
		outline: none;
	}
	.leaving {
		opacity: 0;
	}

	.stage {
		position: relative;
		display: grid;
		place-items: center;
		width: min(92vw, 44rem);
		min-height: 0;
		color: var(--start-line);
	}
	.dial {
		grid-area: 1 / 1;
		width: min(100%, 64dvh);
		height: auto;
		opacity: 0.45;
		animation: turn 120s linear infinite;
	}
	.inscription {
		font-family: var(--mono);
		letter-spacing: 0.1em;
	}
	.art {
		grid-area: 1 / 1;
		width: min(100%, 76dvh);
		filter: drop-shadow(0 0 3px color-mix(in srgb, var(--start-line) 60%, transparent));
		animation: glow 4s ease-in-out 3s infinite alternate;
	}
	.art :global(svg) {
		display: block;
		width: 100%;
		height: auto;
	}
	/* The traced loom draws on band by band, left to right. */
	.art :global(path) {
		stroke-dasharray: 1;
		stroke-dashoffset: 1;
		animation: draw 2.4s ease-in-out forwards;
	}
	.art :global(g:nth-child(2) path) {
		animation-delay: 0.3s;
	}
	.art :global(g:nth-child(3) path) {
		animation-delay: 0.6s;
	}
	.art :global(g:nth-child(4) path) {
		animation-delay: 0.9s;
	}
	.art :global(g:nth-child(5) path) {
		animation-delay: 1.2s;
	}
	.art :global(g:nth-child(6) path) {
		animation-delay: 1.5s;
	}
	.art :global(g:nth-child(7) path) {
		animation-delay: 1.8s;
	}
	.art :global(g:nth-child(n + 8) path) {
		animation-delay: 2.1s;
	}

	.copy {
		display: grid;
		justify-items: center;
		gap: 0.5rem;
		text-align: center;
	}
	h2 {
		margin: 0;
		font-family: var(--serif);
		font-size: clamp(1.75rem, min(5vw, 7dvh), 3.5rem);
		font-weight: normal;
		line-height: 1.05;
		text-transform: uppercase;
		text-wrap: balance;
	}
	.subtitle {
		margin: 0;
		font-family: var(--mono);
		font-size: 0.8rem;
		letter-spacing: 0.12em;
		text-transform: uppercase;
		color: var(--start-muted);
	}
	.begin {
		margin-top: 0.75rem;
		font: 1rem var(--sans);
		padding: 0.5rem 1.25rem;
		color: var(--start-ink);
		background: none;
		border: 1px solid var(--start-accent);
		border-radius: 0.25rem;
		cursor: pointer;
	}
	.begin:focus-visible {
		outline: 2px solid var(--start-accent);
		outline-offset: 3px;
	}
	kbd {
		font-family: var(--mono);
		font-size: 0.7rem;
		padding: 0 0.3rem;
		margin-left: 0.35rem;
		border: 1px solid var(--start-muted);
		border-radius: 0.2rem;
		color: var(--start-muted);
	}

	.credits {
		margin-top: 0.75rem;
		max-width: 44rem;
		font-size: 0.75rem;
		color: var(--start-muted);
	}
	.credits summary {
		cursor: pointer;
		width: fit-content;
		margin-inline: auto;
		font-family: var(--mono);
		letter-spacing: 0.08em;
		text-transform: uppercase;
	}
	.credits summary:focus-visible {
		outline: 2px solid var(--start-accent);
		outline-offset: 2px;
	}
	.credits ul {
		margin: 0.5rem 0 0;
		padding: 0;
		list-style: none;
		overflow-wrap: anywhere;
	}
	.credits a {
		color: inherit;
		text-decoration-color: var(--start-accent);
	}

	@keyframes turn {
		to {
			transform: rotate(360deg);
		}
	}
	@keyframes draw {
		to {
			stroke-dashoffset: 0;
		}
	}
	@keyframes glow {
		to {
			filter: drop-shadow(0 0 7px color-mix(in srgb, var(--start-line) 70%, transparent));
		}
	}

	@media (prefers-reduced-motion: reduce) {
		.start,
		.dial,
		.art {
			transition: none;
			animation: none;
		}
		.art :global(path) {
			animation: none;
			stroke-dashoffset: 0;
		}
	}
</style>

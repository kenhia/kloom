<script lang="ts">
	import { onMount } from 'svelte';
	import { bibliography, chicago, type Citation } from '../citation';
	import type { Palette } from '../model';
	import type { LibraryStats } from '../stats';
	import type { UserSettings } from '../user-settings.svelte';
	import About from './About.svelte';
	import Settings from './Settings.svelte';

	interface Props {
		/**
		 * Every subject the app serves, in the order to list them; a list is
		 * shown when there is more than one. `subtitle` is the subject's own line
		 * (korg 3465); `note` is said after the title ("last read").
		 */
		subjects: { id: string; title: string; subtitle?: string; note?: string }[];
		/** The subject selected in the list, whose title and ring are shown. */
		selected: string;
		/** The subject open behind the start screen: Begin on it, or Esc, returns there. */
		current: string;
		/** A line under the title when the selected subject has no subtitle of its own. */
		subtitle?: string;
		/** Set around the rotating dial, one letter at a time. */
		inscription: string;
		/** A line drawing to draw on in the centre, or null until it loads. */
		art: string | null;
		/** Where the art came from; shown collapsed at the foot. */
		credits: Citation[];
		/** The colours to use: the selected subject's first frame's. */
		palette: Palette;
		/** The selected subject's own illustrations, drawn small around the loom. */
		ring?: string[];
		/**
		 * Where the reader left off in the selected subject, offered under Begin
		 * and never forced. One with `onpick` resumes in this subject; one with
		 * `href` opens another.
		 */
		resume?: Resume[];
		/** Close the start screen over `current`. */
		onbegin: () => void;
		/**
		 * Begin on `current` starts it from its first frame (korg 3432): the
		 * shell moves there first. Esc only closes, leaving the reader where
		 * they were.
		 */
		onfirst?: () => void;
		/** Open another subject, from its selection in the list. */
		onopen: (id: string) => void;
		/** Open the map on the library (§The map); focus comes back to its button. */
		onmap?: (refocus: () => void) => void;
		/** The reader's settings: the gear top right, the shell's own pop-up. */
		settings?: UserSettings;
		/** The About panel top right, left of the gear: the library's counts and this build. */
		about?: { stats: () => Promise<LibraryStats>; build?: string };
	}

	interface Resume {
		key: string;
		/** What it does, e.g. "Continue where you were". */
		action: string;
		/** Where: the frame's title and position. */
		label: string;
		href?: string;
		onpick?: () => void;
	}

	let {
		subjects,
		selected = $bindable(),
		current,
		subtitle,
		inscription,
		art,
		credits,
		palette,
		ring = [],
		resume = [],
		onbegin,
		onfirst,
		onopen,
		onmap,
		settings,
		about
	}: Props = $props();

	const id = $props.id();
	let button = $state<HTMLButtonElement>();
	let mapButton = $state<HTMLButtonElement>();
	let list = $state<HTMLElement>();
	let leaving = $state(false);
	const chosen = $derived(subjects.find((s) => s.id === selected));
	const title = $derived(chosen?.title ?? '');
	const line = $derived(chosen?.subtitle ?? subtitle);
	const index = $derived(subjects.findIndex((s) => s.id === selected));

	onMount(() => button?.focus());

	/** Leave, then begin; `before` moves the shell first (a resume). */
	function begin(before?: () => void) {
		if (leaving) return;
		leaving = true;
		before?.();
		const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
		setTimeout(onbegin, reduced ? 0 : 500);
	}

	/**
	 * Begin on the selection: the subject behind from its first frame, or open another.
	 * Opening another stays put until the page moves, so a navigation the
	 * reader cancels (an unsaved note) leaves the start screen where it was.
	 */
	function go() {
		if (selected === current) begin(onfirst);
		else onopen(selected);
	}

	/** Keys stop here: the shell behind must not move while this is open. */
	function keydown(e: KeyboardEvent) {
		e.stopPropagation();
		// An Esc a pop-up in the corner took was only for closing it.
		if (e.key === 'Escape' && !e.defaultPrevented) {
			e.preventDefault();
			selected = current;
			begin();
		}
	}

	/** The subject list: arrows (either way, as it lies flat on a phone), Home, End; Enter begins. */
	function listKeys(e: KeyboardEvent) {
		const last = subjects.length - 1;
		const to = (
			{
				ArrowDown: index + 1,
				ArrowRight: index + 1,
				ArrowUp: index - 1,
				ArrowLeft: index - 1,
				Home: 0,
				End: last
			} as Record<string, number>
		)[e.key];
		if (e.key !== 'Enter' && to === undefined) return;
		// Handled once, by an option or the list around it.
		e.preventDefault();
		e.stopPropagation();
		if (e.key === 'Enter') go();
		else {
			selected = subjects[Math.min(Math.max(to, 0), last)].id;
		}
	}

	/** Where the ring's i-th drawing sits, as a percentage of the dial, clockwise from the top. */
	const place = (i: number, n: number) => {
		const a = (2 * Math.PI * i) / n - Math.PI / 2;
		return { left: `${50 + RING_R * Math.cos(a)}%`, top: `${50 + RING_R * Math.sin(a)}%` };
	};
	/** Just outside the dial's rim (204 of 220 in its viewBox, 46%). */
	const RING_R = 54;

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
	aria-labelledby="{id}-title"
	aria-describedby="{id}-subtitle"
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
		{#key ring}
			<div class="ring">
				{#each ring as svg, i (i)}
					{@const at = place(i, ring.length)}
					<div class="thumb" style:left={at.left} style:top={at.top} style:--i={i}>
						<!-- The subject's illustrations, sanitised by the loader (engine/svg.ts). -->
						<!-- eslint-disable-next-line svelte/no-at-html-tags -->
						{@html svg}
					</div>
				{/each}
			</div>
		{/key}
		{#if art}
			<div class="art">
				<!-- The app's own drawing, from the repository (src/lib/start). -->
				<!-- eslint-disable-next-line svelte/no-at-html-tags -->
				{@html art}
			</div>
		{/if}
	</div>

	<div class="copy">
		{#if subjects.length > 1}
			<!-- Selection follows the arrows; Enter, or Begin, opens the selection. -->
			<div
				class="subjects"
				role="listbox"
				tabindex="0"
				aria-label="Subjects"
				aria-activedescendant="{id}-{selected}"
				bind:this={list}
				onkeydown={listKeys}
			>
				{#each subjects as s (s.id)}
					<div
						id="{id}-{s.id}"
						role="option"
						aria-selected={s.id === selected}
						tabindex="-1"
						onclick={() => {
							selected = s.id;
							list?.focus();
						}}
						onkeydown={listKeys}
						ondblclick={go}
					>
						{s.title}{#if s.subtitle}<span class="sub">{s.subtitle}</span>{/if}{#if s.note}<span
								class="note">{s.note}</span
							>{/if}
					</div>
				{/each}
			</div>
		{/if}
		<h2 id="{id}-title">{title}</h2>
		{#if line}<p id="{id}-subtitle" class="subtitle">{line}</p>{/if}
		<button type="button" class="begin" bind:this={button} onclick={go}>
			Begin <kbd>Enter</kbd>
		</button>
		{#if resume.length}
			<ul class="resume" aria-label="Where you left off">
				{#each resume as r (r.key)}
					<li>
						{#if r.onpick}
							<button type="button" onclick={() => begin(r.onpick)}>
								<span class="action">{r.action}</span>
								<span class="where">{r.label}</span>
							</button>
						{:else}
							<!-- The page resolved these app routes. -->
							<!-- eslint-disable-next-line svelte/no-navigation-without-resolve -->
							<a href={r.href}>
								<span class="action">{r.action}</span>
								<span class="where">{r.label}</span>
							</a>
						{/if}
					</li>
				{/each}
			</ul>
		{/if}
		{#if onmap}
			<button
				type="button"
				class="map-button"
				aria-haspopup="dialog"
				bind:this={mapButton}
				onclick={() => onmap(() => mapButton?.focus())}
			>
				Map of the library
			</button>
		{/if}
	</div>

	{#if about || settings}
		<!-- Top right, as in the shell, the gear rightmost; last in the tab order. -->
		<div class="corner">
			{#if about}<About {...about} />{/if}
			{#if settings}<Settings {settings} />{/if}
		</div>
	{/if}

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
	/* The selected subject's drawings, riding just outside the dial's rim. */
	.ring {
		grid-area: 1 / 1;
		position: relative;
		width: min(100%, 64dvh);
		aspect-ratio: 1;
		animation: turn 240s linear infinite;
	}
	.thumb {
		position: absolute;
		width: 13%;
		translate: -50% -50%;
		color: var(--start-line);
		opacity: 0;
		animation:
			appear 0.6s ease-out calc(0.4s + var(--i) * 0.08s) forwards,
			turn 240s linear infinite reverse;
	}
	.thumb :global(svg) {
		display: block;
		width: 100%;
		height: auto;
	}
	/* Labels are noise this small. */
	.thumb :global(text) {
		display: none;
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
	.resume {
		display: grid;
		justify-items: center;
		gap: 0.35rem;
		margin: 0.75rem 0 0;
		padding: 0;
		list-style: none;
	}
	.resume button,
	.resume a {
		display: grid;
		justify-items: center;
		font: 0.9rem var(--sans);
		padding: 0.35rem 0.9rem;
		color: var(--start-ink);
		text-decoration: none;
		background: none;
		border: 1px solid color-mix(in srgb, var(--start-muted) 60%, transparent);
		border-radius: 0.25rem;
		cursor: pointer;
	}
	.resume button:hover,
	.resume a:hover {
		border-color: var(--start-accent);
	}
	.resume :focus-visible {
		outline: 2px solid var(--start-accent);
		outline-offset: 2px;
	}
	.map-button {
		margin-top: 0.75rem;
		font: 0.85rem var(--sans);
		padding: 0.3rem 0.8rem;
		color: var(--start-muted);
		background: none;
		border: 1px solid transparent;
		border-radius: 0.25rem;
		cursor: pointer;
	}
	.map-button:hover {
		color: var(--start-ink);
		border-color: color-mix(in srgb, var(--start-muted) 60%, transparent);
	}
	.map-button:focus-visible {
		outline: 2px solid var(--start-accent);
		outline-offset: 2px;
	}
	.resume .action {
		font-size: 0.75rem;
		letter-spacing: 0.1em;
		text-transform: uppercase;
		color: var(--start-muted);
	}
	/* A list down the left beside the loom; above the title on a narrow screen. */
	.subjects {
		display: flex;
		flex-wrap: wrap;
		justify-content: center;
		gap: 0.25rem;
		max-width: 36rem;
		margin-bottom: 0.5rem;
		font: 0.875rem var(--sans);
		border-radius: 0.25rem;
	}
	.subjects:focus-visible {
		outline: 2px solid var(--start-accent);
		outline-offset: 3px;
	}
	[role='option'] {
		padding: 0.3rem 0.75rem;
		color: var(--start-muted);
		border: 1px solid transparent;
		border-radius: 0.25rem;
		cursor: pointer;
	}
	[role='option']:hover {
		color: var(--start-ink);
	}
	[role='option'][aria-selected='true'] {
		color: var(--start-ink);
		border-color: var(--start-accent);
	}
	.sub {
		display: block;
		font-size: 0.8em;
		font-style: italic;
		color: var(--start-muted);
	}
	.note {
		display: block;
		font: 0.65rem var(--mono);
		letter-spacing: 0.1em;
		text-transform: uppercase;
		color: var(--start-muted);
	}
	@media (min-width: 60rem) {
		.subjects {
			position: absolute;
			top: 50%;
			left: clamp(1rem, 4vw, 3rem);
			flex-direction: column;
			align-items: stretch;
			width: clamp(10rem, 18vw, 15rem);
			margin: 0;
			text-align: left;
			translate: 0 -50%;
		}
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

	/* The pop-ups here take the start screen's colours. */
	.corner {
		--background: var(--start-background);
		--ink: var(--start-ink);
		--muted: var(--start-muted);
		--accent: var(--start-accent);
		position: absolute;
		top: 0.5rem;
		right: 0.5rem;
		z-index: 1;
		display: flex;
		gap: 0.25rem;
	}
	/* Both pop-ups hang from the corner's right edge, so neither leaves a phone's screen. */
	.corner :global(.about),
	.corner :global(.settings) {
		position: static;
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
	@keyframes appear {
		to {
			opacity: 0.7;
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
		.ring,
		.art {
			transition: none;
			animation: none;
		}
		.thumb {
			animation: none;
			opacity: 0.7;
		}
		.art :global(path) {
			animation: none;
			stroke-dashoffset: 0;
		}
	}
</style>

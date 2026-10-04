<script lang="ts">
	import { onMount, tick } from 'svelte';
	import { bibliography, chicago, type Citation } from '../citation';
	import type { Palette } from '../model';
	import type { LibraryStats } from '../stats';
	import type { SuggestOffer } from '../reader-data';
	import type { UserSettings } from '../user-settings.svelte';
	import About from './About.svelte';
	import Icon from './Icon.svelte';
	import IconButton from './IconButton.svelte';
	import Settings from './Settings.svelte';

	interface Props {
		/**
		 * Every subject the app serves, in the order to list them; a list is
		 * shown when there is more than one. `subtitle` is the subject's own line
		 * (korg 3465), said under the big title and not in the list; `last`
		 * marks the subject last read (an open book) and `fresh` counts its
		 * frames new to the reader (korg 3514).
		 */
		subjects: { id: string; title: string; subtitle?: string; last?: boolean; fresh?: number }[];
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
		/** Open the Changelog (§What's new), from the corner; focus comes back to its button. */
		onchangelog?: (refocus: () => void) => void;
		/**
		 * What is new to the reader in the selected subject, in words ("3 new
		 * since you started"), said under Begin; absent when nothing is.
		 */
		fresh?: string | null;
		/** The reader's settings: the gear top right, the shell's own pop-up. */
		settings?: UserSettings;
		/** The About panel top right, left of the gear: the library's counts and this build. */
		about?: {
			stats: () => Promise<LibraryStats>;
			build?: string;
			suggest?: SuggestOffer | null;
			ask?: boolean;
		};
		/** The Welcome and How-To page's address (korg 3502), offered under Begin. */
		help?: string;
		/** The User's Guide's address (korg 3515), beside Welcome. */
		guide?: string;
		/**
		 * Signing out, for a reader signed in to the reader edition (korg 3501):
		 * the form's action, and the login's display name.
		 */
		signOut?: { action: string; who: string } | null;
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
		onchangelog,
		fresh = null,
		settings,
		about,
		help,
		guide,
		signOut = null
	}: Props = $props();

	const id = $props.id();
	let button = $state<HTMLButtonElement>();
	let mapButton = $state<HTMLButtonElement>();
	let changelogButton = $state<IconButton>();
	let list = $state<HTMLElement>();
	let heading = $state<HTMLElement>();
	let leaving = $state(false);
	const chosen = $derived(subjects.find((s) => s.id === selected));
	const title = $derived(chosen?.title ?? '');
	const line = $derived(chosen?.subtitle ?? subtitle);
	const index = $derived(subjects.findIndex((s) => s.id === selected));

	/** A title in the list: a leading "The " goes (korg 3514), the subject's own title keeps it. */
	const short = (title: string) => title.replace(/^The\s+/, '');

	/** The list's scroll: whether there is more above and below, and the elevator's thumb. */
	let more = $state({ above: false, below: false, top: 0, size: 100 });
	function track() {
		if (!list) return;
		const { scrollTop, scrollHeight, clientHeight } = list;
		const room = scrollHeight - clientHeight;
		more = {
			above: scrollTop > 1,
			below: scrollTop < room - 1,
			top: room > 0 ? (scrollTop / scrollHeight) * 100 : 0,
			size: room > 0 ? (clientHeight / scrollHeight) * 100 : 100
		};
	}

	/** The faded band at a clipped edge, which a selected option is kept clear of. */
	const FADE = 28;
	const smooth = () =>
		matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth';

	/**
	 * Bring the selected option into view, inside the faded edges: to the
	 * middle (`centre`, on opening), or the nearest way. Scrolls the list
	 * only, never the page; `aria-activedescendant` scrolls nothing itself.
	 */
	function reveal(centre = false) {
		const option = list?.querySelector<HTMLElement>('[aria-selected="true"]');
		if (!list || !option) return;
		const top = option.offsetTop;
		const bottom = top + option.offsetHeight;
		let to = list.scrollTop;
		if (centre) to = top - (list.clientHeight - option.offsetHeight) / 2;
		else if (top - FADE < list.scrollTop) to = top - FADE;
		else if (bottom + FADE > list.scrollTop + list.clientHeight)
			to = bottom + FADE - list.clientHeight;
		if (to !== list.scrollTop) list.scrollTo({ top: to, behavior: centre ? 'instant' : smooth() });
	}

	/** A caret: a page of the list, up or down. */
	function page(way: 1 | -1) {
		list?.scrollBy({ top: way * (list.clientHeight - 2 * FADE), behavior: smooth() });
	}

	// The selection, however it moved, is kept in view.
	$effect(() => {
		void selected;
		tick().then(() => reveal());
	});

	/**
	 * The big title on one line, fitted to the width (korg 3514): no larger
	 * than the stylesheet's size, and no smaller than 1.5rem. A title that
	 * would need less wraps instead, in two balanced lines, at that floor or
	 * under it as far as two lines need.
	 */
	let fit = $state<{ size: number; wrap: boolean } | null>(null);
	function fitTitle() {
		const copy = heading?.parentElement;
		if (!heading || !copy || !title) return;
		const rem = parseFloat(getComputedStyle(document.documentElement).fontSize) || 16;
		// The stylesheet's clamp(1.75rem, min(5vw, 7dvh), 3.5rem), as pixels.
		const cap = Math.min(
			3.5 * rem,
			Math.max(1.75 * rem, Math.min(innerWidth * 0.05, innerHeight * 0.07))
		);
		const floor = 1.5 * rem;
		const ink = document.createElement('canvas').getContext('2d');
		if (!ink) return;
		ink.font = `${cap}px ${getComputedStyle(heading).fontFamily}`;
		const wide = ink.measureText(title.toUpperCase()).width;
		// A hair under the exact fit, so rounding never tips it onto two lines.
		const size = Math.min(cap, (cap * copy.clientWidth * 0.98) / wide);
		// Two lines at most: a title too long even for that at the floor goes smaller still,
		// with room for where its words break.
		fit =
			size < floor
				? { size: Math.min(floor, (cap * 2 * copy.clientWidth * 0.85) / wide), wrap: true }
				: { size, wrap: false };
	}
	$effect(() => {
		void title;
		fitTitle();
	});

	onMount(() => {
		button?.focus();
		reveal(true);
		track();
		const seen = new ResizeObserver(() => {
			fitTitle();
			track();
		});
		if (list) seen.observe(list);
		if (heading?.parentElement) seen.observe(heading.parentElement);
		document.fonts?.ready.then(fitTitle);
		return () => seen.disconnect();
	});

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

	/** The subject list: up and down arrows, Home, End; Enter begins. */
	function listKeys(e: KeyboardEvent) {
		const last = subjects.length - 1;
		const to = (
			{
				ArrowDown: index + 1,
				ArrowUp: index - 1,
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
	<!-- The loom's band: the list beside the dial, as tall as it at most, so it never meets the title. -->
	<div class="band">
		{#if subjects.length > 1}
			<!-- The elevator (korg 3514): the list scrolls in the dial's band, a rail beside it. -->
			<div
				class="elevator"
				style:--fade-top={more.above ? `${FADE}px` : '0px'}
				style:--fade-bottom={more.below ? `${FADE}px` : '0px'}
			>
				<div class="rail" aria-hidden="true" class:idle={!more.above && !more.below}>
					<span class="car" style:top="{more.top}%" style:height="{more.size}%"></span>
				</div>
				<!-- Selection follows the arrows; Enter, or Begin, opens the selection. -->
				<div
					class="subjects"
					role="listbox"
					tabindex="0"
					aria-label="Subjects"
					aria-activedescendant="{id}-{selected}"
					bind:this={list}
					onkeydown={listKeys}
					onscroll={track}
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
							<span class="name">{short(s.title)}</span>{#if s.last}<span class="last"
									><Icon name="last-read" /><span class="visually-hidden">Last read</span></span
								>{/if}{#if s.fresh}<span class="count">{s.fresh} new</span>{/if}
						</div>
					{/each}
				</div>
				<!-- More above or below: a page at a click. The arrows are the keyboard's way. -->
				<button
					type="button"
					class="caret up"
					tabindex="-1"
					aria-hidden="true"
					hidden={!more.above}
					onclick={() => page(-1)}
				>
					<svg viewBox="0 0 16 8"><path d="M2 7 8 1.5 14 7" /></svg>
				</button>
				<button
					type="button"
					class="caret down"
					tabindex="-1"
					aria-hidden="true"
					hidden={!more.below}
					onclick={() => page(1)}
				>
					<svg viewBox="0 0 16 8"><path d="M2 1 8 6.5 14 1" /></svg>
				</button>
			</div>
		{/if}
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
	</div>

	<div class="copy">
		<h2
			id="{id}-title"
			bind:this={heading}
			class:wrap={fit?.wrap}
			style:font-size={fit ? `${fit.size}px` : undefined}
		>
			{title}
		</h2>
		{#if line}<p id="{id}-subtitle" class="subtitle">{line}</p>{/if}
		{#if subjects.length > 1}
			<!-- On a narrow screen the list is the platform's own picker, under the title. -->
			<select class="picker" aria-label="Subjects" bind:value={selected}>
				{#each subjects as s (s.id)}
					<option value={s.id}
						>{short(s.title)}{s.last ? ' — last read' : ''}{s.fresh
							? ` · ${s.fresh} new`
							: ''}</option
					>
				{/each}
			</select>
		{/if}
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
		{#if fresh}
			<p class="fresh">{fresh}</p>
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
		{#if help || guide || signOut}
			<div class="account">
				{#if help}
					<!-- An app route, resolved by the page. -->
					<!-- eslint-disable-next-line svelte/no-navigation-without-resolve -->
					<a href={help}>Welcome and how to read kloom</a>
				{/if}
				{#if guide}
					<!-- An app route, resolved by the page. -->
					<!-- eslint-disable-next-line svelte/no-navigation-without-resolve -->
					<a href={guide}>User's Guide</a>
				{/if}
				{#if signOut}
					<!-- A plain form, so signing out works before the page's script has loaded. -->
					<form method="POST" action={signOut.action}>
						<span>Signed in as {signOut.who}</span>
						<button type="submit">Sign out</button>
					</form>
				{/if}
			</div>
		{/if}
	</div>

	{#if about || settings || onchangelog}
		<!-- Top right, as in the shell, the gear rightmost; last in the tab order. -->
		<div class="corner">
			{#if onchangelog}
				<IconButton
					label="What's new"
					tip="What's new: the Changelog"
					aria-haspopup="dialog"
					bind:this={changelogButton}
					onclick={() => onchangelog(() => changelogButton?.focus())}
				>
					<Icon name="whats-new" />
				</IconButton>
			{/if}
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
		/* The list's column, the stage between two of them, and the dial in the stage. */
		--gap: 1.5rem;
		/* What the dial leaves either side, within bounds: a short screen gives the list room. */
		--list: clamp(16rem, (100vw - 2rem - min(44rem, 64dvh)) / 2 - var(--gap), 20rem);
		--stage: min(92vw, 44rem);
		--dial: min(var(--stage), 64dvh);
		display: grid;
		grid-template-rows: minmax(0, 1fr) auto auto;
		grid-template-columns: minmax(0, 1fr);
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

	/*
	 * The loom's band. From 60rem the list stands left of the stage, a column
	 * of the same width on the right keeping the loom centred, and the stage
	 * gives way to both; below, the stage alone.
	 */
	.band {
		display: grid;
		grid-template-rows: minmax(0, 1fr);
		grid-template-columns: var(--stage);
		justify-content: center;
		column-gap: var(--gap);
		width: 100%;
		min-height: 0;
	}
	.stage {
		grid-row: 1;
		grid-column: 1;
		position: relative;
		display: grid;
		place-items: center;
		width: var(--stage);
		min-height: 0;
		color: var(--start-line);
		/* Decoration: a control it overlaps (Begin, on a short screen) still takes the click. */
		pointer-events: none;
	}
	.dial {
		grid-area: 1 / 1;
		width: var(--dial);
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
		width: var(--dial);
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
		grid-template-columns: minmax(0, 1fr);
		justify-items: center;
		gap: 0.5rem;
		width: 100%;
		min-width: 0;
		text-align: center;
	}
	/* One line, fitted to the width by the script; it wraps only below its floor. */
	h2 {
		max-width: 100%;
		margin: 0;
		font-family: var(--serif);
		font-size: clamp(1.75rem, min(5vw, 7dvh), 3.5rem);
		font-weight: normal;
		line-height: 1.05;
		text-transform: uppercase;
		white-space: nowrap;
	}
	h2.wrap {
		white-space: normal;
		text-wrap: balance;
	}
	/* A tagline wraps rather than run off the screen. */
	.subtitle {
		max-width: 100%;
		margin: 0;
		font-family: var(--mono);
		font-size: 0.8rem;
		letter-spacing: 0.12em;
		text-transform: uppercase;
		text-wrap: balance;
		color: var(--start-muted);
	}
	@media (max-width: 30rem) {
		.subtitle {
			letter-spacing: 0.06em;
		}
	}
	/* The narrow screen's picker: styled shut, the platform's own open. */
	.picker {
		width: min(100%, 22rem);
		margin-top: 0.25rem;
		font: 0.9rem var(--sans);
		padding: 0.35rem 0.6rem;
		color: var(--start-ink);
		background: var(--start-background);
		border: 1px solid var(--start-accent);
		border-radius: 0.25rem;
		cursor: pointer;
	}
	.picker:focus-visible {
		outline: 2px solid var(--start-accent);
		outline-offset: 2px;
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
	.account {
		display: flex;
		flex-wrap: wrap;
		justify-content: center;
		align-items: baseline;
		gap: 0.25rem 1.25rem;
		margin-top: 0.75rem;
		font: 0.85rem var(--sans);
		color: var(--start-muted);
	}
	.account a {
		color: var(--start-ink);
		text-underline-offset: 0.2em;
	}
	.account form {
		display: flex;
		align-items: baseline;
		gap: 0.5rem;
	}
	.account button {
		font: inherit;
		padding: 0.15rem 0.6rem;
		color: var(--start-ink);
		background: none;
		border: 1px solid color-mix(in srgb, var(--start-muted) 60%, transparent);
		border-radius: 0.25rem;
		cursor: pointer;
	}
	.account a:focus-visible,
	.account button:focus-visible {
		outline: 2px solid var(--start-accent);
		outline-offset: 2px;
	}
	.resume .action {
		font-size: 0.75rem;
		letter-spacing: 0.1em;
		text-transform: uppercase;
		color: var(--start-muted);
	}
	/*
	 * The elevator: the list in the dial's band, no taller than the dial and
	 * centred on it, scrolling natively with its bar hidden; a rail on its
	 * left shows where it is, and carets say there is more.
	 */
	.elevator {
		display: none;
	}
	.picker {
		display: block;
	}
	@media (min-width: 60rem) {
		.start {
			--stage: min(100vw - 2rem - 2 * (var(--list) + var(--gap)), 44rem);
		}
		.band {
			grid-template-columns: var(--list) var(--stage) var(--list);
		}
		.stage {
			grid-column: 2;
		}
		.elevator {
			grid-row: 1;
			grid-column: 1;
			align-self: center;
			position: relative;
			display: flex;
			max-height: min(var(--dial), 100%);
			padding-left: 0.9rem;
		}
		.picker {
			display: none;
		}
	}
	.subjects {
		position: relative;
		display: flex;
		flex-direction: column;
		gap: 0.125rem;
		width: 100%;
		min-height: 0;
		padding: 2px;
		overflow-y: auto;
		scrollbar-width: none;
		font: 0.875rem var(--sans);
		text-align: left;
		border-radius: 0.25rem;
		mask-image: linear-gradient(
			to bottom,
			transparent 0,
			#000 var(--fade-top),
			#000 calc(100% - var(--fade-bottom)),
			transparent 100%
		);
	}
	.subjects::-webkit-scrollbar {
		display: none;
	}
	.subjects:focus-visible {
		outline: 2px solid var(--start-accent);
		outline-offset: -1px;
	}
	/* One line each: a title too long for the column gives way before its marks do. */
	[role='option'] {
		display: flex;
		align-items: baseline;
		flex: none;
		white-space: nowrap;
		padding: 0.15rem 0.375rem;
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
	.name {
		min-width: 0;
		overflow: hidden;
		text-overflow: ellipsis;
	}
	/* The subject last read: an open book after its title. */
	.last {
		flex: none;
		align-self: center;
		display: inline-block;
		width: 1.1em;
		height: 1.1em;
		margin-left: 0.4em;
		color: var(--start-accent);
	}
	.last :global(svg) {
		display: block;
		width: 100%;
		height: 100%;
	}
	/* Frames new to the reader in a subject: a small count. */
	.count {
		flex: none;
		margin-left: 0.45em;
		font: 0.7rem var(--mono);
		white-space: nowrap;
		color: var(--start-accent);
	}
	/* A thin line with a stop at each end; the car is where the list is. */
	.rail {
		position: absolute;
		top: 0;
		bottom: 0;
		left: 0.2rem;
		width: 1px;
		background: color-mix(in srgb, var(--start-muted) 55%, transparent);
	}
	.rail::before,
	.rail::after {
		content: '';
		position: absolute;
		left: -0.25rem;
		width: calc(0.5rem + 1px);
		height: 1px;
		background: inherit;
	}
	.rail::before {
		top: 0;
	}
	.rail::after {
		bottom: 0;
	}
	.rail.idle {
		visibility: hidden;
	}
	.car {
		position: absolute;
		left: -1px;
		width: 3px;
		border-radius: 1.5px;
		background: var(--start-accent);
	}
	.caret {
		position: absolute;
		left: calc(0.9rem + 50% - 0.45rem - 1rem);
		width: 2rem;
		height: 1rem;
		padding: 0.15rem 0.5rem;
		color: var(--start-ink);
		background: none;
		border: none;
		cursor: pointer;
	}
	.caret[hidden] {
		display: none;
	}
	.caret.up {
		top: 0;
	}
	.caret.down {
		bottom: 0;
	}
	.caret svg {
		display: block;
		width: 100%;
		height: 100%;
		fill: none;
		stroke: currentColor;
		stroke-width: 1.5;
		stroke-linecap: round;
		stroke-linejoin: round;
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

	.fresh {
		margin: 0.5rem 0 0;
		font-size: 0.85rem;
		color: var(--start-accent);
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

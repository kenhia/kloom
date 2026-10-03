<script lang="ts">
	import type { Snippet } from 'svelte';
	import { hasMarks, marksText, NO_MARKS, type FrameMarks } from '../marks';
	import type { Frame, FrameHead, Palette, Trail } from '../model';
	import { cursorAt, indexLabel, type Stop } from '../navigation';

	interface Props {
		path: Stop[];
		index: number;
		frame: Frame;
		/**
		 * What the scene wears (korg 3495): the scene and its HUD are coloured
		 * apart from the reading, so the reader can keep one calm and the other
		 * by section.
		 */
		palette: Palette;
		/** The trail being walked, or null on the main spine. */
		trail: Trail | null;
		/** Frame ids on this spine that have a trail branching from them. */
		branches: Set<string>;
		/** The reader's marks on a frame: bookmark, kept answers, notes. */
		marksOf?: (frame: string) => FrameMarks;
		frames: Record<string, FrameHead>;
		onstep: (delta: number) => void;
		onjump: (index: number) => void;
		onwheel: (event: WheelEvent) => void;
		onleave: () => void;
		/** The timeline slider, so the shell can return focus to it. */
		slider?: HTMLElement;
		/** Controls beside the index (the bookmarks). */
		tools?: Snippet;
		/** Shown in the scene's place while the reader writes a note. */
		editor?: Snippet;
	}

	let {
		path,
		index,
		frame,
		palette,
		trail,
		branches,
		marksOf = () => NO_MARKS,
		frames,
		onstep,
		onjump,
		onwheel,
		onleave,
		slider = $bindable(),
		tools,
		editor
	}: Props = $props();

	/** The frame's marks in words, after a comma, for its value text and title. */
	const said = (id: string) =>
		marksText(marksOf(id))
			.map((m) => `, ${m}`)
			.join('');

	const stop = $derived(path[index]);
	const chapter = $derived(trail ? `${trail.title} · ${stop.segment.title}` : stop.segment.title);

	let pane: HTMLElement;
	// Registered by hand: the wheel must be non-passive to stop the page scrolling.
	$effect(() => {
		const handler = (e: WheelEvent) => onwheel(e);
		pane.addEventListener('wheel', handler, { passive: false });
		return () => pane.removeEventListener('wheel', handler);
	});

	/**
	 * How much a headline's type shrinks with its length: not at all to 26
	 * characters (most headlines), then with the square root of the excess, to
	 * no less than 0.7 (the longest, about 52).
	 */
	const fit = (headline: string, accent: string) =>
		Math.max(0.7, Math.min(1, Math.sqrt(26 / (headline.length + 1 + accent.length)))).toFixed(3);

	function jumpTo(e: MouseEvent) {
		const bar = e.currentTarget as HTMLElement;
		const { left, width } = bar.getBoundingClientRect();
		onjump(Math.round(((e.clientX - left) / width) * (path.length - 1)));
	}
</script>

<section
	id="spine-pane"
	class="spine"
	aria-label="Spine"
	style:--background={palette.background}
	style:--ink={palette.ink}
	style:--muted={palette.muted}
	style:--accent={palette.accent}
	style:--line={palette.line}
	style:color-scheme={palette.scheme}
	bind:this={pane}
>
	<span class="bracket tl" aria-hidden="true"></span>
	<span class="bracket tr" aria-hidden="true"></span>
	<span class="bracket bl" aria-hidden="true"></span>
	<span class="bracket br" aria-hidden="true"></span>

	<div class="hud top">
		<p class="chapter">
			{#if trail}
				<button type="button" class="crumb" onclick={onleave}>Main story</button>
				<span aria-hidden="true">›</span>
			{/if}
			{chapter}
		</p>
		<div class="corner">
			{@render tools?.()}
			<p class="index" aria-hidden="true">{indexLabel(index, path.length)}</p>
		</div>
	</div>

	{#if editor}
		{@render editor()}
	{:else}
		{#key frame.id}
			<div class="scene">
				{#if frame.svg}
					<div class="illustration" aria-hidden="true">
						<!-- Validated on load: a line drawing, no script or handlers. -->
						<!-- eslint-disable-next-line svelte/no-at-html-tags -->
						{@html frame.svg}
					</div>
				{/if}
				{#if frame.scene.dedication}
					<div class="dedication">
						<p class="kicker">{frame.scene.dedication.kicker}</p>
						<p class="name">{frame.scene.dedication.name}</p>
						{#if frame.scene.dedication.note}
							<p class="below">{frame.scene.dedication.note}</p>
						{/if}
					</div>
				{:else}
					<p class="headline" style:--fit={fit(frame.scene.headline, frame.scene.accent)}>
						<span class="words">{frame.scene.headline}</span>
						<em class="accent">{frame.scene.accent}</em>
					</p>
				{/if}
				{#if frame.scene.metadata.length}
					<ul class="metadata">
						{#each frame.scene.metadata as line (line)}<li>{line}</li>{/each}
					</ul>
				{/if}
			</div>
		{/key}
	{/if}

	<div class="hud bottom">
		<p class="position">{frame.position.label}</p>
		{#if frame.scene.counter}
			<p class="counter">
				<span class="value">{frame.scene.counter.value}</span>
				{#if frame.scene.counter.label}<span class="label">{frame.scene.counter.label}</span>{/if}
			</p>
		{/if}
	</div>

	<div class="timeline">
		<button
			type="button"
			class="step"
			aria-label="Previous frame"
			disabled={index === 0}
			onclick={() => onstep(-1)}>‹</button
		>
		<!-- Arrow keys are handled for the whole page by the shell, so the
		     slider takes no keydown of its own; the click is a pointer extra. -->
		<!-- svelte-ignore a11y_click_events_have_key_events -->
		<div
			class="bar"
			role="slider"
			tabindex="0"
			aria-label={trail ? `Position on the ${trail.title} trail` : 'Position on the spine'}
			aria-valuemin={1}
			aria-valuemax={path.length}
			aria-valuenow={index + 1}
			aria-valuetext={`${index + 1} of ${path.length}: ${frame.position.label}, ${frame.scene.headline} ${frame.scene.accent}${said(frame.id)}`}
			bind:this={slider}
			onclick={jumpTo}
		>
			{#each path as s, i (s.frameId)}
				{@const m = marksOf(s.frameId)}
				<span
					class="tick"
					class:boundary={i > 0 && path[i - 1].segment !== s.segment}
					class:branch={branches.has(s.frameId)}
					style:left="{cursorAt(i, path.length) * 100}%"
					title={frames[s.frameId].position.label + said(s.frameId)}
				>
					{#if hasMarks(m)}
						<!-- The reader's layer, under the line: each kind in its own place and shape. -->
						<span class="marks" aria-hidden="true">
							{#if m.bookmarked}<span class="mark bookmark"></span>{/if}
							{#if m.kept}<span class="mark kept"></span>{/if}
							{#if m.notes}<span class="mark note"></span>{/if}
						</span>
					{/if}
				</span>
			{/each}
			<span class="cursor" style:left="{cursorAt(index, path.length) * 100}%"></span>
		</div>
		<button
			type="button"
			class="step"
			aria-label="Next frame"
			disabled={index === path.length - 1}
			onclick={() => onstep(1)}>›</button
		>
	</div>
</section>

<style>
	.spine {
		position: relative;
		display: grid;
		grid-template-rows: auto minmax(0, 1fr) auto auto;
		padding: 1.25rem 1.5rem 0.75rem;
		overflow: hidden;
		user-select: none;
		color: var(--ink);
		background: var(--background);
		/* Its own palette fades as the shell's does (docs/design.md §Palette transitions). */
		transition:
			--background var(--palette-fade),
			--ink var(--palette-fade),
			--muted var(--palette-fade),
			--accent var(--palette-fade),
			--line var(--palette-fade);
	}
	@media (prefers-reduced-motion: reduce) {
		.spine {
			transition: none;
		}
	}

	.bracket {
		position: absolute;
		width: 1.25rem;
		height: 1.25rem;
		border: 0 solid var(--muted);
	}
	.tl {
		top: 0.5rem;
		left: 0.5rem;
		border-width: 1px 0 0 1px;
	}
	.tr {
		top: 0.5rem;
		right: 0.5rem;
		border-width: 1px 1px 0 0;
	}
	.bl {
		bottom: 0.5rem;
		left: 0.5rem;
		border-width: 0 0 1px 1px;
	}
	.br {
		bottom: 0.5rem;
		right: 0.5rem;
		border-width: 0 1px 1px 0;
	}

	.hud {
		display: flex;
		justify-content: space-between;
		align-items: end;
		gap: 1rem;
		font-family: var(--mono);
		font-size: 0.75rem;
		letter-spacing: 0.12em;
		text-transform: uppercase;
		color: var(--muted);
	}
	.hud p {
		margin: 0;
	}
	.corner {
		display: flex;
		flex-wrap: wrap;
		justify-content: flex-end;
		align-items: center;
		gap: 0.35rem 0.75rem;
	}
	/* The index never wraps, however much the corner holds (the Back chip). */
	.index {
		white-space: nowrap;
	}
	.crumb {
		font: inherit;
		letter-spacing: inherit;
		text-transform: inherit;
		color: var(--accent);
		background: none;
		border: 0;
		padding: 0;
		text-decoration: underline;
		cursor: pointer;
	}
	.position {
		font-size: 0.95rem;
		color: var(--ink);
	}
	.counter {
		display: grid;
		justify-items: end;
	}
	.counter .value {
		font-family: var(--serif);
		font-size: clamp(1.5rem, 4vw, 2.75rem);
		letter-spacing: 0;
		color: var(--ink);
	}

	/*
	 * The staged entrance (docs/design.md §Scene entrance). The scene is keyed
	 * by frame, so every move rebuilds it and the stages restart from zero: a
	 * burst of ← → never leaves one half-faded. The small text and the HUD are
	 * there at once and the drawing starts drawing on; then the headline, then
	 * its accent word, landing just before the drawing's last group (~2.9s).
	 */
	/*
	 * The scene fills its row of the spine and never leaves it (sprint 031,
	 * korg 3469): the words take the height they need and the drawing gives
	 * way, down to nothing, so a long headline can never push the metadata
	 * into the counter below or the drawing into the HUD above.
	 */
	.scene {
		--headline-delay: 1s;
		--headline-fade: 1s;
		--accent-delay: 1.5s;
		--accent-fade: 1s;
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		gap: min(1rem, 2dvh);
		text-align: center;
		min-height: 0;
		padding-block: 0.5rem;
	}
	.scene > * {
		flex: none;
	}
	.scene > .illustration {
		flex: 0 1 auto;
		display: flex;
		justify-content: center;
		min-height: 0;
		max-width: 100%;
		color: var(--line);
	}
	/* Sized by height as well as width, and no taller than the room left. */
	.illustration :global(svg) {
		display: block;
		width: auto;
		max-width: min(100%, 30rem);
		height: min(38dvh, 20rem);
		max-height: 100%;
	}
	/* Each path carries pathLength="1", so one dash is the whole stroke. */
	.illustration :global(svg *) {
		stroke-dasharray: 1;
		stroke-dashoffset: 1;
		animation: draw 1.4s ease-out forwards;
	}
	/*
	 * The drawing's top-level groups draw one after another, in document
	 * order: construction lines first, then the object, then its details.
	 */
	.illustration :global(svg > :nth-child(2) *) {
		animation-delay: 0.25s;
	}
	.illustration :global(svg > :nth-child(3) *) {
		animation-delay: 0.5s;
	}
	.illustration :global(svg > :nth-child(4) *) {
		animation-delay: 0.75s;
	}
	.illustration :global(svg > :nth-child(5) *) {
		animation-delay: 1s;
	}
	.illustration :global(svg > :nth-child(6) *) {
		animation-delay: 1.25s;
	}
	.illustration :global(svg > :nth-child(n + 7) *) {
		animation-delay: 1.5s;
	}
	/* Labels have no stroke to draw; they fade in once the lines are down. */
	.illustration :global(svg text) {
		opacity: 0;
		animation: appear 0.6s ease-out 1.6s forwards;
	}
	@keyframes draw {
		to {
			stroke-dashoffset: 0;
		}
	}
	@keyframes appear {
		to {
			opacity: 1;
		}
	}
	.headline {
		margin: 0;
		font-family: var(--serif);
		/* Scaled down gently by length (fit, below): long headlines wrap less. */
		font-size: clamp(1.5rem, calc(min(5.5vw, 9dvh) * var(--fit, 1)), calc(4.75rem * var(--fit, 1)));
		line-height: 1;
		text-transform: uppercase;
		text-wrap: balance;
	}
	.accent {
		font-style: normal;
		color: var(--accent);
	}
	.headline .words,
	.headline .accent {
		opacity: 0;
		animation: appear var(--headline-fade) ease-in-out var(--headline-delay) forwards;
	}
	.headline .accent {
		animation-duration: var(--accent-fade);
		animation-delay: var(--accent-delay);
	}
	/*
	 * A dedication (sprint 028): a name in its own case, not a headline in
	 * capitals, between a small line above and an optional one below. It
	 * enters with the headline's timing, all at once, with no accent word.
	 */
	.dedication {
		display: grid;
		justify-items: center;
		gap: min(0.6rem, 1.2dvh);
		opacity: 0;
		animation: appear var(--headline-fade) ease-in-out var(--headline-delay) forwards;
	}
	.dedication p {
		margin: 0;
	}
	.dedication .kicker {
		font-family: var(--mono);
		font-size: 0.8rem;
		letter-spacing: 0.3em;
		text-transform: uppercase;
		color: var(--accent);
	}
	.dedication .name {
		font-family: var(--serif);
		font-size: clamp(1.5rem, min(3.6vw, 6dvh), 2.75rem);
		line-height: 1.15;
		text-wrap: balance;
		color: var(--ink);
	}
	.dedication .below {
		font-family: var(--serif);
		font-size: clamp(1rem, min(1.8vw, 3dvh), 1.35rem);
		color: var(--muted);
	}
	.metadata {
		margin: 0;
		padding: 0;
		list-style: none;
		font-family: var(--mono);
		font-size: 0.75rem;
		letter-spacing: 0.1em;
		color: var(--muted);
	}

	.timeline {
		display: grid;
		grid-template-columns: auto 1fr auto;
		align-items: center;
		gap: 0.75rem;
		margin-top: 0.75rem;
		/* Room for the reader's marks under the line. */
		padding-bottom: 1rem;
	}
	.step {
		font: 1.25rem/1 var(--serif);
		width: 2rem;
		height: 2rem;
		color: var(--ink);
		background: none;
		border: 1px solid var(--muted);
		border-radius: 50%;
		cursor: pointer;
	}
	.step:disabled {
		opacity: 0.35;
		cursor: default;
	}
	.bar {
		position: relative;
		height: 1.5rem;
		cursor: pointer;
	}
	.bar::before {
		content: '';
		position: absolute;
		inset: 50% 0 auto;
		border-top: 1px solid var(--muted);
	}
	.tick,
	.cursor {
		position: absolute;
		top: 50%;
		transform: translate(-50%, -50%);
	}
	.tick {
		height: 0.5rem;
		border-left: 1px solid var(--muted);
	}
	.tick.boundary {
		height: 1rem;
	}
	.tick.branch::after {
		content: '';
		position: absolute;
		top: -0.45rem;
		left: -0.2rem;
		width: 0.35rem;
		height: 0.35rem;
		border: 1px solid var(--accent);
		border-radius: 50%;
	}
	/*
	 * The reader's layer (docs/design.md §Marks), under the line where the
	 * branch ring sits above it. Each kind keeps its own row whether or not the
	 * others are there: a bookmark's flag first, then a kept answer's dot, then
	 * a note's lines.
	 */
	.marks {
		position: absolute;
		top: calc(100% + 0.15rem);
		left: -0.2rem;
		display: grid;
		grid-template-rows: repeat(3, 0.45rem);
		row-gap: 0.12rem;
		width: 0.4rem;
	}
	.mark {
		display: block;
		width: 0.4rem;
	}
	.bookmark {
		grid-row: 1;
		background: var(--accent);
		clip-path: polygon(0 0, 100% 0, 100% 100%, 50% 70%, 0 100%);
	}
	.kept {
		grid-row: 2;
		height: 0.4rem;
		border-radius: 50%;
		background: var(--accent);
	}
	.note {
		grid-row: 3;
		border-top: 1px solid var(--accent);
		border-bottom: 1px solid var(--accent);
	}
	.cursor {
		width: 2px;
		height: 1.25rem;
		background: #d7261e;
		transition: left 0.35s ease;
	}

	@media (prefers-reduced-motion: reduce) {
		.illustration :global(svg *) {
			animation: none;
			stroke-dashoffset: 0;
		}
		.illustration :global(svg text),
		.headline .words,
		.headline .accent {
			animation: none;
			opacity: 1;
		}
		.cursor {
			transition: none;
		}
	}
</style>

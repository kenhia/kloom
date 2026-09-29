<script lang="ts">
	import { onMount, untrack } from 'svelte';
	import type { AiOffer } from '../ai/provider';
	import type { Frame, Subject, Trail } from '../model';
	import type { JumpItem } from '../reader-data';
	import { clamp, indexLabel, stops, WheelGate, type SyncMode } from '../navigation';
	import { pageKey, tabKey } from '../keys';
	import {
		bounds,
		defaultPanes,
		panesFor,
		readPanes,
		resize,
		writePanes,
		type Divider,
		type SavedPanes
	} from '../panes';
	import {
		browserStorage,
		followSpine,
		layout,
		paletteFor,
		paletteMode,
		type Layout
	} from '../settings';
	import type { UserSettings } from '../user-settings.svelte';
	import AiPane from './AiPane.svelte';
	import Bookmarks from './Bookmarks.svelte';
	import Narrative from './Narrative.svelte';
	import Settings from './Settings.svelte';
	import SpinePane from './SpinePane.svelte';
	import Splitter from './Splitter.svelte';

	interface Props {
		subject: Subject;
		/** The reader's settings; the page makes them and loads them on mount. */
		settings: UserSettings;
		/** What the app config offers the AI pane. */
		ai?: AiOffer;
		/** A grow job finished: the page reloads the subject from disk. */
		ongrown?: () => void;
		/** False while something (the start screen) sits in front of the shell. */
		active?: boolean;
		/** The frame to open on (a deep link); the first frame when absent. */
		startAt?: string | null;
		/** The frame on the spine changed: the page records the reader's place. */
		onplace?: (frame: Frame) => void;
		/** The reader's bookmarks; absent when there is no reader to keep them for. */
		bookmarks?: BookmarkOffer | null;
	}

	/** What the page offers for bookmarks: the frames marked, the jump list, and the writes. */
	interface BookmarkOffer {
		/** Frame ids in this subject the reader has bookmarked. */
		marked: Set<string>;
		items: JumpItem[];
		exportHref?: string;
		ontoggle: (frame: Frame) => void;
		onremove: (item: JumpItem) => void;
	}

	let {
		subject,
		settings,
		ai = { web: 'deny' },
		ongrown,
		active = true,
		startAt = null,
		onplace,
		bookmarks = null
	}: Props = $props();

	let trailId = $state<string | null>(null);
	let index = $state(0);
	/** What the narrative shows when it does not follow the spine. */
	let pinned = $state<string | null>(null);

	/** Said once when a bookmark is made or removed, so a B press is heard. */
	let markNote = $state('');

	/** The tabs layout (§Layout): which of Narrative and AI the right-hand pane shows. */
	const TABS = ['narrative', 'ai'] as const;
	let tab = $state<(typeof TABS)[number]>('narrative');
	const tabEls: HTMLButtonElement[] = [];
	/** What the AI pane reports for its tab: working, or a result not yet seen. */
	let aiActivity = $state<'idle' | 'working' | 'ready'>('idle');

	let narrativeEl = $state<HTMLElement>();
	let slider = $state<HTMLElement>();

	const trail = $derived(trailId ? (subject.trails.find((t) => t.id === trailId) ?? null) : null);
	const path = $derived(stops(trail ? trail.spine : subject.spine));
	const stop = $derived(path[clamp(index, path.length)]);
	const frame = $derived(subject.frames[stop.frameId]);
	/** A reader setting (§Interaction): the narrative follows the spine unless they said not to. */
	const sync = $derived<SyncMode>(settings.get(followSpine.id) === 'manual' ? 'manual' : 'follow');
	const shape = $derived((settings.get(layout.id) ?? layout.default) as Layout);
	const tabbed = $derived(shape === 'tabs');

	// Pane sizes (§Layout): dragged at the dividers, remembered per layout.
	let saved = $state<SavedPanes>({});
	let panesEl = $state<HTMLElement>();
	onMount(() => (saved = readPanes(browserStorage())));
	const panes = $derived(panesFor(saved, shape));
	const fr = (...parts: number[]) => parts.map((p) => `minmax(0, ${p}fr)`).join(' ');
	const cols = $derived(
		shape === 'columns'
			? fr(panes.spine, 1 - panes.spine - panes.ai, panes.ai)
			: fr(panes.spine, 1 - panes.spine)
	);
	const rows = $derived(shape === 'split' ? fr(panes.upper, 1 - panes.upper) : null);
	const setPane = (d: Divider, v: number) =>
		(saved = writePanes(saved, shape, resize(panes, shape, d, v), browserStorage()));
	const resetPane = (d: Divider) => setPane(d, defaultPanes(shape)[d]);
	/** Where the pointer is, as the share a divider asks for. */
	function pointerAt(d: Divider, e: PointerEvent) {
		const r = panesEl!.getBoundingClientRect();
		if (d === 'spine') return (e.clientX - r.left) / r.width;
		if (d === 'ai') return (r.right - e.clientX) / r.width;
		return (e.clientY - r.top) / r.height;
	}
	/** The dividers this layout has. */
	const dividers = $derived<{ id: Divider; label: string; controls: string }[]>([
		{ id: 'spine', label: 'Resize the spine', controls: 'spine-pane' },
		...(shape === 'columns'
			? [{ id: 'ai' as const, label: 'Resize the AI pane', controls: 'ai-pane' }]
			: []),
		...(shape === 'split'
			? [{ id: 'upper' as const, label: 'Resize the narrative', controls: 'narrative-panel' }]
			: [])
	]);
	const palette = $derived(
		paletteFor(subject, frame.scene.palette, settings.get(paletteMode.id) ?? paletteMode.default)
	);
	const narrativeFrame = $derived(
		sync === 'follow' || !pinned ? frame : (subject.frames[pinned] ?? frame)
	);
	const trailsFrom = (id: string) => subject.trails.filter((t) => t.anchor === id);
	const branches = $derived(new Set(trail ? [] : subject.trails.map((t) => t.anchor)));
	const marked = $derived(bookmarks?.marked ?? new Set<string>());
	const announcement = $derived(
		`${indexLabel(index, path.length)}, ${stop.segment.title}, ${frame.position.label}: ${frame.scene.headline} ${frame.scene.accent}${marked.has(frame.id) ? ' Bookmarked.' : ''}`
	);

	/**
	 * Move to a frame wherever it is: each frame sits on one spine, the main
	 * one or a trail's, so the id alone says which. An unknown id is ignored.
	 */
	export function goTo(id: string) {
		const main = stops(subject.spine).findIndex((s) => s.frameId === id);
		if (main >= 0) {
			trailId = null;
			index = main;
		} else {
			const t = subject.trails.find((t) => stops(t.spine).some((s) => s.frameId === id));
			if (!t) return;
			trailId = t.id;
			index = stops(t.spine).findIndex((s) => s.frameId === id);
		}
		pinned = id;
	}

	untrack(() => startAt && goTo(startAt));

	$effect(() => onplace?.(frame));

	function toggleMark() {
		if (!bookmarks) return;
		const on = !marked.has(frame.id);
		bookmarks.ontoggle(frame);
		markNote = on
			? `Bookmarked: ${frame.scene.headline} ${frame.scene.accent}`
			: `Bookmark removed: ${frame.scene.headline} ${frame.scene.accent}`;
	}

	// Coming forward (the start screen closed): the spine takes focus.
	let wasActive: boolean | undefined;
	$effect(() => {
		if (active && wasActive === false) slider?.focus();
		wasActive = active;
	});

	// While following, the pin tracks the spine, so turning following off
	// leaves the reading where it is rather than on some older frame.
	$effect(() => {
		if (sync === 'follow') pinned = stop.frameId;
	});

	const reducedMotion = () => matchMedia('(prefers-reduced-motion: reduce)').matches;

	function go(i: number) {
		if (pinned === null) pinned = stop.frameId;
		index = clamp(i, path.length);
	}
	const step = (delta: number) => go(index + delta);

	function syncNarrative() {
		pinned = stop.frameId;
		tab = 'narrative';
	}

	function tabKeydown(e: KeyboardEvent, i: number) {
		const to = tabKey(e.key, i, TABS.length);
		if (to === null) return;
		// Handled here, so the page's arrows (the spine) stand down.
		e.preventDefault();
		tab = TABS[to];
		tabEls[to]?.focus();
	}

	function enter(t: Trail) {
		trailId = t.id;
		index = 0;
		if (sync === 'manual')
			pinned = subject.trails.find((x) => x.id === t.id)!.spine.segments[0].frames[0];
	}

	function leave() {
		if (!trail) return;
		const anchor = trail.anchor;
		trailId = null;
		index = stops(subject.spine).findIndex((s) => s.frameId === anchor);
		if (sync === 'manual') pinned = anchor;
		slider?.focus();
	}

	const gate = new WheelGate();
	function wheel(e: WheelEvent) {
		// A pop-up over the spine (the bookmark list) scrolls as itself.
		if (e.target instanceof Element && e.target.closest('[data-own-keys]')) return;
		e.preventDefault();
		const px = e.deltaMode === 1 ? 16 : e.deltaMode === 2 ? 400 : 1;
		const delta = Math.abs(e.deltaY) >= Math.abs(e.deltaX) ? e.deltaY : e.deltaX;
		const s = gate.push(delta * px, e.timeStamp);
		if (s) step(s);
	}

	function scrollNarrative(direction: number) {
		narrativeEl?.scrollBy({ top: direction * 80, behavior: reducedMotion() ? 'auto' : 'smooth' });
	}

	/** Page-wide keys: engine/keys.ts decides what a press means where focus is. */
	function keydown(e: KeyboardEvent) {
		if (!active || e.defaultPrevented || e.altKey || e.ctrlKey || e.metaKey) return;
		const target = e.target instanceof Element ? e.target : null;
		switch (pageKey(e.key, target)) {
			case 'to-spine':
				slider?.focus();
				break;
			case 'next':
				step(1);
				break;
			case 'previous':
				step(-1);
				break;
			case 'first':
				go(0);
				break;
			case 'last':
				go(path.length - 1);
				break;
			case 'scroll-down':
				scrollNarrative(1);
				break;
			case 'scroll-up':
				scrollNarrative(-1);
				break;
			case 'sync':
				syncNarrative();
				break;
			case 'trail': {
				const [first] = trail ? [] : trailsFrom(frame.id);
				if (!first) return;
				enter(first);
				break;
			}
			case 'leave-trail':
				if (!trail) return;
				leave();
				break;
			case 'bookmark':
				if (!bookmarks) return;
				toggleMark();
				break;
			default:
				return;
		}
		e.preventDefault();
	}
</script>

<svelte:window onkeydown={keydown} />

<div
	class="shell"
	inert={!active}
	style:--background={palette.background}
	style:--ink={palette.ink}
	style:--muted={palette.muted}
	style:--accent={palette.accent}
	style:--line={palette.line}
	style:color-scheme={palette.scheme}
>
	<h1 class="visually-hidden">{subject.title}</h1>
	<p class="visually-hidden" aria-live="polite" aria-atomic="true">{announcement}</p>
	<p class="visually-hidden" role="status">{markNote}</p>

	<div
		class="panes {shape}"
		class:on-ai={tabbed && tab === 'ai'}
		style:--cols={cols}
		style:--rows={rows}
		bind:this={panesEl}
	>
		<SpinePane
			{path}
			index={clamp(index, path.length)}
			{frame}
			{trail}
			{branches}
			{marked}
			frames={subject.frames}
			onstep={step}
			onjump={go}
			onwheel={wheel}
			onleave={leave}
			bind:slider
		>
			{#snippet tools()}
				{#if bookmarks}
					<Bookmarks
						marked={marked.has(frame.id)}
						items={bookmarks.items}
						exportHref={bookmarks.exportHref}
						ontoggle={toggleMark}
						onjump={goTo}
						onremove={bookmarks.onremove}
					/>
				{/if}
			{/snippet}
		</SpinePane>

		{#if tabbed}
			<div class="tab-row">
				<div role="tablist" aria-label="Right-hand pane">
					{#each TABS as t, i (t)}
						<button
							type="button"
							role="tab"
							id="tab-{t}"
							aria-selected={tab === t}
							aria-controls={t === 'ai' ? 'ai-results' : 'narrative-panel'}
							tabindex={tab === t ? 0 : -1}
							onclick={() => (tab = t)}
							onkeydown={(e) => tabKeydown(e, i)}
							bind:this={tabEls[i]}
						>
							{t === 'ai' ? 'AI' : 'Narrative'}
							{#if t === 'ai' && aiActivity !== 'idle'}
								<span class="badge {aiActivity}" aria-hidden="true"
									>{aiActivity === 'ready' ? '●' : '…'}</span
								>
								<span class="visually-hidden"
									>{aiActivity === 'ready' ? ', a result is waiting' : ', working'}</span
								>
							{/if}
						</button>
					{/each}
				</div>
				<Settings {settings} />
			</div>
		{/if}

		<Narrative
			tab={tabbed ? 'tab-narrative' : null}
			hidden={tabbed && tab !== 'narrative'}
			frame={narrativeFrame}
			spineFrame={frame}
			{sync}
			trails={trail ? [] : trailsFrom(narrativeFrame.id)}
			onenter={enter}
			bind:element={narrativeEl}
		>
			{#snippet tools()}{#if !tabbed}<Settings {settings} />{/if}{/snippet}
		</Narrative>

		<AiPane
			subject={subject.id}
			frame={narrativeFrame}
			{trail}
			{settings}
			offer={ai}
			mainFrames={stops(subject.spine).map((s) => s.frameId)}
			titleOf={(id) =>
				subject.frames[id]
					? `${subject.frames[id].scene.headline} ${subject.frames[id].scene.accent}`
					: id}
			{ongrown}
			layout={shape}
			showResults={!tabbed || tab === 'ai'}
			onshow={() => (tab = 'ai')}
			onactivity={(a) => (aiActivity = a)}
		/>

		{#each dividers as d (d.id)}
			{@const b = bounds(panes, shape, d.id)}
			<Splitter
				class="at-{d.id}"
				orientation={d.id === 'upper' ? 'horizontal' : 'vertical'}
				label={d.label}
				controls={d.controls}
				value={panes[d.id]}
				min={b.min}
				max={b.max}
				at={(e) => pointerAt(d.id, e)}
				onchange={(v) => setPane(d.id, v)}
				onreset={() => resetPane(d.id)}
			/>
		{/each}
	</div>

	<p id="ai-hint" class="hint">
		<kbd>←</kbd><kbd>→</kbd> spine · <kbd>↑</kbd><kbd>↓</kbd> narrative · <kbd>S</kbd> sync,
		<kbd>T</kbd> trail and <kbd>B</kbd> bookmark, in the spine or narrative · <kbd>Tab</kbd> into
		and out of the AI pane · <kbd>Esc</kbd> back to the spine · drag a divider, or focus it and use the
		arrows
	</p>
</div>

<style>
	/*
	 * Registered so the palette itself interpolates. Unregistered custom
	 * properties snap, so everything painted straight from a variable (accent
	 * words, buttons, borders, SVG strokes) used to change at once while the
	 * background faded behind it: a flash bulb (korg 3370). The initial values
	 * are only fallbacks; each frame's palette sets them.
	 */
	@property --background {
		syntax: '<color>';
		inherits: true;
		initial-value: #000;
	}
	@property --ink {
		syntax: '<color>';
		inherits: true;
		initial-value: #fff;
	}
	@property --muted {
		syntax: '<color>';
		inherits: true;
		initial-value: #888;
	}
	@property --accent {
		syntax: '<color>';
		inherits: true;
		initial-value: #fff;
	}
	@property --line {
		syntax: '<color>';
		inherits: true;
		initial-value: #fff;
	}

	.shell {
		display: flex;
		flex-direction: column;
		height: 100dvh;
		color: var(--ink);
		background: var(--background);
		/* One timing for every colour, so the whole page moves together. */
		--palette-fade: 1.5s ease-in-out;
		transition:
			--background var(--palette-fade),
			--ink var(--palette-fade),
			--muted var(--palette-fade),
			--accent var(--palette-fade),
			--line var(--palette-fade);
	}

	/*
	 * §Layout: where each pane sits. Every pane is placed explicitly, so the
	 * dividers, which share its grid cell, never push a pane along. The
	 * column (and the split's row) sizes are the reader's, set inline.
	 */
	.panes {
		flex: 1;
		min-height: 0;
		display: grid;
		grid-template-columns: var(--cols);
	}
	.panes > :global(.spine) {
		grid-column: 1;
		grid-row: 1 / -1;
	}
	.panes > :global(.narrative) {
		grid-column: 2;
		grid-row: 1;
	}
	.panes > :global(.at-spine) {
		grid-column: 1;
		grid-row: 1 / -1;
		justify-self: end;
		margin-right: -5px;
	}
	.strip {
		grid-template-rows: minmax(0, 1fr) auto;
	}
	.strip > :global(.spine),
	.strip > :global(.at-spine) {
		grid-row: 1;
	}
	.strip > :global(.ai) {
		grid-column: 1 / -1;
		grid-row: 2;
	}
	.columns {
		grid-template-rows: minmax(0, 1fr);
	}
	.columns > :global(.ai) {
		grid-column: 3;
		grid-row: 1;
	}
	.columns > :global(.at-ai) {
		grid-column: 3;
		grid-row: 1;
		justify-self: start;
		margin-left: -5px;
	}
	.split {
		grid-template-rows: var(--rows);
	}
	.split > :global(.ai) {
		grid-column: 2;
		grid-row: 2;
		border-left: 1px solid color-mix(in srgb, var(--muted) 40%, transparent);
	}
	.split > :global(.at-upper) {
		grid-column: 2;
		grid-row: 1;
		align-self: end;
		margin-bottom: -5px;
	}
	.tabs {
		grid-template-rows: auto minmax(0, 1fr) auto;
	}
	.tabs > :global(.narrative) {
		grid-row: 2;
	}
	.tabs > :global(.ai) {
		grid-column: 2;
		grid-row: 3;
		border-left: 1px solid color-mix(in srgb, var(--muted) 40%, transparent);
	}
	.on-ai > :global(.ai) {
		grid-row: 2 / 4;
		border-top: 0;
	}
	.hint {
		margin: 0;
		padding: 0.35rem 1.5rem;
		font-size: 0.75rem;
		color: var(--muted);
		border-top: 1px solid color-mix(in srgb, var(--muted) 40%, transparent);
	}
	kbd {
		font-family: var(--mono);
		font-size: 0.7rem;
		padding: 0 0.25rem;
		margin-right: 0.1rem;
		border: 1px solid var(--muted);
		border-radius: 0.2rem;
	}
	.tab-row {
		grid-column: 2;
		grid-row: 1;
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: 0.5rem;
		padding: 0.5rem 1.5rem 0;
		border-left: 1px solid color-mix(in srgb, var(--muted) 40%, transparent);
	}
	[role='tablist'] {
		display: flex;
		gap: 0.25rem;
	}
	[role='tab'] {
		font-family: var(--mono);
		font-size: 0.75rem;
		letter-spacing: 0.12em;
		text-transform: uppercase;
		padding: 0.35rem 0.75rem;
		color: var(--muted);
		background: none;
		border: 0;
		border-bottom: 2px solid transparent;
		cursor: pointer;
	}
	[role='tab'][aria-selected='true'] {
		color: var(--ink);
		border-bottom-color: var(--accent);
	}
	.badge {
		margin-left: 0.25rem;
		color: var(--accent);
	}
	/* A divider shows focus as its own accent line (Splitter.svelte). */
	.shell :global(:focus-visible:not([role='separator'])) {
		outline: 2px solid var(--accent);
		outline-offset: 2px;
	}

	/* One column on a phone, in every layout: spine, (tabs), narrative, AI. No dividers. */
	@media (max-width: 760px) {
		.shell {
			height: auto;
			min-height: 100dvh;
		}
		.panes {
			grid-template-columns: minmax(0, 1fr);
			grid-template-rows: none;
		}
		.panes > :global(*) {
			grid-column: 1 !important;
			grid-row: auto !important;
		}
		.panes > :global([role='separator']) {
			display: none;
		}
		.panes > :global(.spine) {
			height: 75svh;
		}
		.panes > :global(.narrative) {
			height: 70svh;
			border-left: 0;
			border-top: 1px solid color-mix(in srgb, var(--muted) 40%, transparent);
		}
		.panes > :global(.ai) {
			border-left: 0;
		}
		.on-ai > :global(.ai) {
			min-height: 70svh;
		}
		.tab-row {
			border-left: 0;
			border-top: 1px solid color-mix(in srgb, var(--muted) 40%, transparent);
		}
	}

	@media (prefers-reduced-motion: reduce) {
		.shell {
			transition: none;
		}
	}
</style>

<script lang="ts">
	import type { AiOffer } from '../ai/provider';
	import type { Subject, Trail } from '../model';
	import { clamp, indexLabel, stops, WheelGate, type SyncMode } from '../navigation';
	import { pageKey } from '../keys';
	import { followSpine, paletteFor, paletteMode } from '../settings';
	import type { UserSettings } from '../user-settings.svelte';
	import AiPane from './AiPane.svelte';
	import Narrative from './Narrative.svelte';
	import Settings from './Settings.svelte';
	import SpinePane from './SpinePane.svelte';

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
	}

	let { subject, settings, ai = { web: 'deny' }, ongrown, active = true }: Props = $props();

	let trailId = $state<string | null>(null);
	let index = $state(0);
	/** What the narrative shows when it does not follow the spine. */
	let pinned = $state<string | null>(null);

	let narrativeEl = $state<HTMLElement>();
	let slider = $state<HTMLElement>();

	const trail = $derived(trailId ? (subject.trails.find((t) => t.id === trailId) ?? null) : null);
	const path = $derived(stops(trail ? trail.spine : subject.spine));
	const stop = $derived(path[clamp(index, path.length)]);
	const frame = $derived(subject.frames[stop.frameId]);
	/** A reader setting (§Interaction): the narrative follows the spine unless they said not to. */
	const sync = $derived<SyncMode>(settings.get(followSpine.id) === 'manual' ? 'manual' : 'follow');
	const palette = $derived(
		paletteFor(subject, frame.scene.palette, settings.get(paletteMode.id) ?? paletteMode.default)
	);
	const narrativeFrame = $derived(
		sync === 'follow' || !pinned ? frame : (subject.frames[pinned] ?? frame)
	);
	const trailsFrom = (id: string) => subject.trails.filter((t) => t.anchor === id);
	const branches = $derived(new Set(trail ? [] : subject.trails.map((t) => t.anchor)));
	const announcement = $derived(
		`${indexLabel(index, path.length)}, ${stop.segment.title}, ${frame.position.label}: ${frame.scene.headline} ${frame.scene.accent}`
	);

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

	<SpinePane
		{path}
		index={clamp(index, path.length)}
		{frame}
		{trail}
		{branches}
		frames={subject.frames}
		onstep={step}
		onjump={go}
		onwheel={wheel}
		onleave={leave}
		bind:slider
	/>

	<Narrative
		frame={narrativeFrame}
		spineFrame={frame}
		{sync}
		trails={trail ? [] : trailsFrom(narrativeFrame.id)}
		onenter={enter}
		bind:element={narrativeEl}
	>
		{#snippet tools()}<Settings {settings} />{/snippet}
	</Narrative>

	<AiPane
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
	/>
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
		display: grid;
		grid-template-columns: minmax(0, 3fr) minmax(0, 2fr);
		grid-template-rows: minmax(0, 1fr) auto;
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
	.shell > :global(.ai) {
		grid-column: 1 / -1;
	}
	.shell :global(:focus-visible) {
		outline: 2px solid var(--accent);
		outline-offset: 2px;
	}

	@media (max-width: 760px) {
		.shell {
			grid-template-columns: minmax(0, 1fr);
			grid-template-rows: 75svh minmax(0, 70svh) auto;
			height: auto;
			min-height: 100dvh;
		}
		.shell > :global(.narrative) {
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

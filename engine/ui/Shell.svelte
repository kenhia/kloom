<script lang="ts">
	import { onMount } from 'svelte';
	import type { Subject, Trail } from '../model';
	import { clamp, indexLabel, stops, WheelGate, type SyncMode } from '../navigation';
	import AiPane from './AiPane.svelte';
	import Narrative from './Narrative.svelte';
	import SpinePane from './SpinePane.svelte';

	let { subject }: { subject: Subject } = $props();

	const SYNC_KEY = 'kloom.sync';

	let trailId = $state<string | null>(null);
	let index = $state(0);
	let sync = $state<SyncMode>('manual');
	/** What the narrative shows in manual mode; follow mode ignores it. */
	let pinned = $state<string | null>(null);

	let narrativeEl = $state<HTMLElement>();
	let slider = $state<HTMLElement>();

	const trail = $derived(trailId ? (subject.trails.find((t) => t.id === trailId) ?? null) : null);
	const path = $derived(stops(trail ? trail.spine : subject.spine));
	const stop = $derived(path[clamp(index, path.length)]);
	const frame = $derived(subject.frames[stop.frameId]);
	const palette = $derived(subject.palettes[frame.scene.palette]);
	const narrativeFrame = $derived(
		sync === 'follow' || !pinned ? frame : (subject.frames[pinned] ?? frame)
	);
	const trailsFrom = (id: string) => subject.trails.filter((t) => t.anchor === id);
	const branches = $derived(new Set(trail ? [] : subject.trails.map((t) => t.anchor)));
	const announcement = $derived(
		`${indexLabel(index, path.length)}, ${stop.segment.title}, ${frame.position.label}: ${frame.scene.headline} ${frame.scene.accent}`
	);

	onMount(() => {
		try {
			if (localStorage.getItem(SYNC_KEY) === 'follow') sync = 'follow';
		} catch {
			// Storage can be blocked; the default is fine.
		}
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

	function setSync(mode: SyncMode) {
		sync = mode;
		pinned = stop.frameId;
		try {
			localStorage.setItem(SYNC_KEY, mode);
		} catch {
			// Not remembered, still applied.
		}
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

	/** Page-wide keys (docs/design.md §Interaction); text fields keep their own. */
	function keydown(e: KeyboardEvent) {
		if (e.defaultPrevented || e.altKey || e.ctrlKey || e.metaKey) return;
		const target = e.target as HTMLElement;
		if (e.key === 'Escape' && target.closest('.ai')) {
			e.preventDefault();
			slider?.focus();
			return;
		}
		if (target.closest('input[type="text"], textarea, select, [contenteditable="true"]')) return;

		switch (e.key) {
			case 'ArrowRight':
				step(1);
				break;
			case 'ArrowLeft':
				step(-1);
				break;
			case 'Home':
				go(0);
				break;
			case 'End':
				go(path.length - 1);
				break;
			case 'ArrowDown':
				scrollNarrative(1);
				break;
			case 'ArrowUp':
				scrollNarrative(-1);
				break;
			case 's':
			case 'S':
				syncNarrative();
				break;
			case 't':
			case 'T': {
				const [first] = trail ? [] : trailsFrom(frame.id);
				if (!first) return;
				enter(first);
				break;
			}
			case 'Escape':
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
		onsync={syncNarrative}
		onsyncmode={setSync}
		onenter={enter}
		bind:element={narrativeEl}
	/>

	<AiPane />
</div>

<style>
	.shell {
		display: grid;
		grid-template-columns: minmax(0, 3fr) minmax(0, 2fr);
		grid-template-rows: minmax(0, 1fr) auto;
		height: 100dvh;
		color: var(--ink);
		background: var(--background);
		transition:
			background-color 0.6s ease,
			color 0.6s ease;
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

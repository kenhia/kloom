<script lang="ts">
	import Icon from './Icon.svelte';
	import { tick } from 'svelte';
	import { SvelteSet } from 'svelte/reactivity';
	import { contentsCount, filterContents, type ContentsSegment } from '../contents';
	import { FRESH_TEXT, marksText, NO_MARKS, type FrameMarks } from '../marks';
	import IconButton from './IconButton.svelte';

	interface Props {
		/** The subject's contents (engine/contents.ts). */
		contents: ContentsSegment[];
		/** The frame on the spine: marked, and where the list opens. */
		current: string;
		/** Trails expanded when the list opens: the one the reader is on, or those from their frame. */
		startOpen: Set<string>;
		/** The reader's marks on a frame, said after its title. */
		marksOf?: (frame: string) => FrameMarks;
		/** A frame's own address, so it can open in a new tab; the page resolves it. */
		hrefOf?: (frame: string) => string;
		/** The reader's letter for opening it, or null when it has none. */
		key?: string | null;
		/**
		 * Frames new to the reader here, and "I'm caught up on this subject"
		 * (§What's new); absent with no reader.
		 */
		fresh?: { count: number; oncaughtup: () => void } | null;
		onjump: (frame: string) => void;
	}

	let {
		contents,
		current,
		startOpen,
		marksOf = () => NO_MARKS,
		hrefOf,
		key = null,
		fresh = null,
		onjump
	}: Props = $props();

	const id = $props.id();
	let open = $state(false);
	let query = $state('');
	const expanded = new SvelteSet<string>();
	let root = $state<HTMLElement>();
	let panel = $state<HTMLElement>();
	let opener = $state<IconButton>();

	const shown = $derived(filterContents(contents, query));
	const filtering = $derived(!!query.trim());
	const found = $derived(contentsCount(shown));
	const isOpen = (trail: string) => filtering || expanded.has(trail);

	/** Open the list on the frame the reader is on (the C key, or the button). */
	export async function show() {
		query = '';
		expanded.clear();
		for (const t of startOpen) expanded.add(t);
		open = true;
		await tick();
		const here = panel?.querySelector<HTMLElement>('[aria-current="page"]');
		here?.scrollIntoView({ block: 'center' });
		here?.focus();
	}

	function close(refocus: boolean) {
		open = false;
		if (refocus) opener?.focus();
	}

	function toggleTrail(trail: string, to = !expanded.has(trail)) {
		if (to) expanded.add(trail);
		else expanded.delete(trail);
	}

	function outside(e: PointerEvent) {
		if (open && !root?.contains(e.target as Node)) close(false);
	}

	function pick(e: MouseEvent, frame: string) {
		if (e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
		e.preventDefault();
		onjump(frame);
		close(true);
	}

	/**
	 * Keys in the list: ↑/↓ move between its entries (the filter box is the
	 * first), Home/End to the ends outside the box, → and ← open and close a
	 * trail, and Esc closes the list, returning focus to its button. Handled
	 * here, and their default prevented, so the page's own keys stand down.
	 */
	function keydown(e: KeyboardEvent) {
		if (e.key === 'Escape') {
			e.preventDefault();
			close(true);
			return;
		}
		const target = e.target as HTMLElement;
		const trail = target.dataset.trail;
		if (trail && (e.key === 'ArrowRight' || e.key === 'ArrowLeft')) {
			e.preventDefault();
			toggleTrail(trail, e.key === 'ArrowRight');
			return;
		}
		const inBox = target.matches('input');
		const moves: Record<string, number | 'first' | 'last'> = {
			ArrowDown: 1,
			ArrowUp: -1,
			...(inBox ? {} : { Home: 'first', End: 'last' })
		};
		const move = moves[e.key];
		if (move === undefined || !panel) return;
		e.preventDefault();
		const stops = [...panel.querySelectorAll<HTMLElement>('[data-stop]')].filter(
			(el) => el.offsetParent !== null || el === target
		);
		const at = stops.indexOf(target);
		const to = move === 'first' ? 1 : move === 'last' ? stops.length - 1 : Math.max(0, at + move);
		stops[Math.min(to, stops.length - 1)]?.focus();
	}
</script>

<svelte:window onpointerdown={outside} />

{#snippet entry(f: { id: string; title: string; position: string; topic: string })}
	{@const marks = marksText(marksOf(f.id))}
	<!-- The page resolved these app routes. -->
	<!-- eslint-disable svelte/no-navigation-without-resolve -->
	<a
		href={hrefOf?.(f.id) ?? `#${f.id}`}
		aria-current={f.id === current ? 'page' : undefined}
		data-stop
		onclick={(e) => pick(e, f.id)}
	>
		<span class="label">{f.title}</span>
		<span class="context"
			>{f.position} · {f.topic}{#if marks.length}<span class="marks">· {marks.join(', ')}</span
				>{/if}</span
		>
	</a>
	<!-- eslint-enable svelte/no-navigation-without-resolve -->
{/snippet}

<div class="contents" bind:this={root}>
	<IconButton
		label="Contents"
		tip={key ? `Contents (${key})` : 'Contents'}
		aria-expanded={open}
		aria-controls="{id}-panel"
		bind:this={opener}
		onclick={() => (open ? close(false) : show())}
		onkeydown={(e) => {
			if (e.key === 'Escape' && open) {
				e.preventDefault();
				close(true);
			}
		}}
	>
		<Icon name="contents" />
	</IconButton>

	<!-- A popover, as the gear's and the bookmarks' are: Tab leaves it, Esc closes it.
	     The page's own keys stand down in here: data-own-keys. The list's keys are
	     heard from whichever of its controls has focus. -->
	<!-- svelte-ignore a11y_no_noninteractive_element_interactions -->
	<div
		id="{id}-panel"
		class="panel"
		role="group"
		aria-labelledby="{id}-title"
		data-own-keys
		hidden={!open}
		bind:this={panel}
		onkeydown={keydown}
	>
		<!-- Stays in view as the list scrolls: the title, the close button and the filter. -->
		<div class="top">
			<div class="head">
				<p id="{id}-title" class="title">Contents</p>
				<button type="button" class="close" onclick={() => close(true)}>
					<span aria-hidden="true">×</span>
					<span class="visually-hidden">Close the contents</span>
				</button>
			</div>
			<label class="visually-hidden" for="{id}-filter">Filter the frames</label>
			<input
				id="{id}-filter"
				type="search"
				placeholder="Filter by title, position or topic"
				autocomplete="off"
				aria-describedby="{id}-found"
				data-stop
				bind:value={query}
			/>
			<p id="{id}-found" class="found" role="status">
				{#if filtering}{found === 1 ? '1 frame' : `${found} frames`}{/if}
			</p>
			{#if fresh?.count}
				<!-- The reader who reads straight through clears their marks here (korg 3525). -->
				<p class="fresh">
					<span>{fresh.count === 1 ? '1 frame' : `${fresh.count} frames`} {FRESH_TEXT}</span>
					<button type="button" class="caught-up" data-stop onclick={fresh.oncaughtup}
						>I’m caught up on this subject</button
					>
				</p>
			{/if}
		</div>

		{#each shown as segment (segment.id)}
			<p id="{id}-s-{segment.id}" class="segment">{segment.title}</p>
			<ul aria-labelledby="{id}-s-{segment.id}">
				{#each segment.entries as e (e.id)}
					<li>
						{@render entry(e)}
						{#each e.trails as t (t.id)}
							<!-- Filtering opens every trail it matches in, so there is nothing to disclose. -->
							{#if filtering}
								<p class="trail">Trail: {t.title}</p>
							{:else}
								<button
									type="button"
									class="trail"
									aria-expanded={isOpen(t.id)}
									aria-controls="{id}-t-{t.id}"
									data-stop
									data-trail={t.id}
									onclick={() => toggleTrail(t.id)}
								>
									<span class="chevron" aria-hidden="true">›</span>
									Trail: {t.title}
									<span class="count"
										>{t.frames.length === 1
											? '1 frame'
											: `${t.frames.length} frames`}{#if t.frames.some((f) => marksOf(f.id).fresh)}<span
												class="marks">· {FRESH_TEXT}</span
											>{/if}</span
									>
								</button>
							{/if}
							<ul id="{id}-t-{t.id}" class="trail-frames" hidden={!isOpen(t.id)}>
								{#each t.frames as f (f.id)}
									<li>{@render entry(f)}</li>
								{/each}
							</ul>
						{/each}
					</li>
				{/each}
			</ul>
		{:else}
			<p class="note">No frame matches.</p>
		{/each}
	</div>
</div>

<style>
	.contents {
		position: relative;
		text-transform: none;
		letter-spacing: 0;
	}
	.panel {
		position: absolute;
		top: calc(100% + 0.35rem);
		right: 0;
		z-index: 5;
		display: grid;
		gap: 0.35rem;
		width: min(26rem, calc(100vw - 2rem));
		max-height: min(70dvh, 40rem);
		overflow-y: auto;
		overscroll-behavior: contain;
		padding: 0.75rem 1rem;
		font-family: var(--sans, inherit);
		font-size: 0.9rem;
		text-align: left;
		color: var(--ink);
		background: var(--background);
		border: 1px solid var(--muted);
		border-radius: 0.25rem;
		box-shadow: 0 0.5rem 1.5rem color-mix(in srgb, #000 35%, transparent);
		user-select: text;
	}
	.panel[hidden] {
		display: none;
	}
	/* A phone: a sheet over the whole screen, under the page's own edge. */
	@media (max-width: 40rem) {
		.panel {
			position: fixed;
			inset: 0.5rem;
			width: auto;
			max-height: none;
		}
	}
	.top {
		position: sticky;
		top: -0.75rem;
		z-index: 1;
		display: grid;
		gap: 0.35rem;
		margin: -0.75rem -1rem 0;
		padding: 0.75rem 1rem 0.35rem;
		background: var(--background);
	}
	.head {
		display: flex;
		justify-content: space-between;
		align-items: center;
	}
	.title,
	.segment,
	.found,
	.note {
		margin: 0;
	}
	.title,
	.segment {
		font-family: var(--mono);
		font-size: 0.75rem;
		letter-spacing: 0.12em;
		text-transform: uppercase;
		color: var(--muted);
	}
	.segment {
		margin-top: 0.5rem;
		padding-top: 0.5rem;
		border-top: 1px solid color-mix(in srgb, var(--muted) 40%, transparent);
	}
	.found,
	.note {
		font-size: 0.8rem;
		color: var(--muted);
	}
	.fresh {
		display: flex;
		flex-wrap: wrap;
		align-items: baseline;
		gap: 0.25rem 0.6rem;
		margin: 0;
		font-size: 0.8rem;
		color: var(--accent);
	}
	.caught-up {
		font: inherit;
		padding: 0.1rem 0.5rem;
		color: var(--ink);
		background: none;
		border: 1px solid var(--muted);
		border-radius: 0.25rem;
		cursor: pointer;
	}
	.found:empty {
		display: none;
	}
	.close {
		font: 1.1rem/1 var(--serif);
		padding: 0.15rem 0.45rem;
		color: var(--muted);
		background: none;
		border: 1px solid transparent;
		border-radius: 0.25rem;
		cursor: pointer;
	}
	.close:hover {
		color: var(--ink);
		border-color: var(--muted);
	}
	input {
		font: inherit;
		min-width: 0;
		padding: 0.3rem 0.45rem;
		color: var(--ink);
		background: var(--background);
		border: 1px solid var(--muted);
		border-radius: 0.25rem;
	}
	ul {
		display: grid;
		gap: 0.2rem;
		margin: 0;
		padding: 0;
		list-style: none;
	}
	.trail-frames {
		margin: 0.15rem 0 0.35rem 1.1rem;
		padding-left: 0.6rem;
		border-left: 1px solid color-mix(in srgb, var(--muted) 50%, transparent);
	}
	.trail-frames[hidden] {
		display: none;
	}
	a {
		display: grid;
		padding: 0.2rem 0.4rem;
		color: var(--ink);
		text-decoration: none;
		border-left: 2px solid transparent;
		border-radius: 0.15rem;
	}
	a:hover .label {
		text-decoration: underline;
	}
	a[aria-current='page'] {
		border-left-color: var(--accent);
		background: color-mix(in srgb, var(--accent) 12%, transparent);
	}
	a[aria-current='page'] .label {
		color: var(--accent);
	}
	.context {
		font-size: 0.75rem;
		color: var(--muted);
	}
	.marks {
		margin-left: 0.35em;
		color: var(--accent);
	}
	.trail {
		display: flex;
		align-items: baseline;
		gap: 0.4rem;
		margin-left: 1.1rem;
		padding: 0.15rem 0.4rem;
		font: inherit;
		font-size: 0.8rem;
		text-align: left;
		color: var(--accent);
		background: none;
		border: 1px solid transparent;
		border-radius: 0.25rem;
		cursor: pointer;
	}
	button.trail:hover {
		border-color: var(--muted);
	}
	p.trail {
		margin: 0 0 0 1.1rem;
		cursor: default;
	}
	.chevron {
		display: inline-block;
		transition: transform 150ms;
	}
	.trail[aria-expanded='true'] .chevron {
		transform: rotate(90deg);
	}
	.count {
		color: var(--muted);
	}
	@media (prefers-reduced-motion: reduce) {
		.chevron {
			transition: none;
		}
	}
</style>

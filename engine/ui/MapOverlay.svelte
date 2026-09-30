<script lang="ts" module>
	import type { MapTarget } from '../map';

	/** How the map was opened: where, in which light, and where focus goes back to. */
	export interface MapOpen {
		target: MapTarget;
		/** The scheme of the palette it opens over: the map takes its own surface in that light. */
		scheme: 'dark' | 'light';
		/** Back to the control that opened it, when it closes. */
		refocus?: () => void;
		/** The frame the reader is on, so it can be named "you are here". */
		here?: string | null;
	}
</script>

<script lang="ts">
	import { tick } from 'svelte';
	import {
		extent,
		layoutView,
		MapIndex,
		placeLabels,
		stepFrom,
		subjectOf,
		subjectSlot,
		viewOf,
		type Direction,
		type LabelSide,
		type MapData,
		type MapNode,
		type MapView,
		type Point
	} from '../map';

	interface Props {
		/** The map's data: fetched when the map first opens; the page keeps it. */
		load: () => Promise<MapData>;
		/** Any frame's address; the page resolves it. */
		hrefOf: (subject: string, frame: string) => string;
		/** Go to a frame: the map closes, and the page jumps (with a way back). */
		onfollow: (subject: string, frame: string) => void;
	}

	let { load, hrefOf, onfollow }: Props = $props();

	const id = $props.id();
	let dialog = $state<HTMLDialogElement>();
	let canvas = $state<HTMLElement>();
	let opened = $state<MapOpen | null>(null);
	let index = $state<MapIndex | null>(null);
	let failed = $state(false);
	let target = $state<MapTarget>({ view: 'library' });
	/** The views before this one, for the map's own Back. */
	let trail = $state<MapTarget[]>([]);
	/** The "Show as list" switch: on by default on a phone (below 40rem). */
	let asList = $state<boolean | null>(null);
	/** The node with focus (or the pointer): the one the details describe. */
	let active = $state<string | null>(null);
	/** The node under the pointer, and the node with visible (keyboard) focus. */
	let hovered = $state<string | null>(null);
	let focused = $state<string | null>(null);
	/** The node whose links are brought forward; none at rest, when every line is dimmed. */
	const hot = $derived(hovered ?? focused);
	let width = $state(0);
	let height = $state(0);

	const view = $derived<MapView | null>(index ? viewOf(index, target) : null);
	const at = $derived<Map<string, Point>>(view ? layoutView(view) : new Map());
	const nodesById = $derived(new Map(view?.nodes.map((n) => [n.id, n]) ?? []));
	const steps = $derived(target.view === 'frame' ? target.steps : null);
	const here = $derived(opened?.here ?? null);

	/** The layout fitted to the canvas: a node's place on screen, in pixels. */
	const fit = $derived.by(() => {
		if (!view || !width || !height) return null;
		const e = extent(view, at);
		const pad = 56;
		const scale = Math.min(
			(width - 2 * pad) / Math.max(1, e.x1 - e.x0),
			(height - 2 * pad) / Math.max(1, e.y1 - e.y0),
			1.4
		);
		const cx = (e.x0 + e.x1) / 2;
		const cy = (e.y0 + e.y1) / 2;
		return (p: Point) => ({
			x: (p.x - cx) * scale + width / 2,
			y: (p.y - cy) * scale + height / 2
		});
	});
	const screen = $derived(
		new Map(fit && view ? view.nodes.map((n) => [n.id, fit(at.get(n.id)!)]) : [])
	);

	const priority = (n: MapNode) =>
		n.ring === 0 ? 1000 : n.kind === 'subject' ? 500 : n.kind === 'frame' ? 200 - 50 * n.ring : 100;
	const labels = $derived<Map<string, LabelSide | null>>(
		view && fit
			? placeLabels(
					view.nodes.map((n) => {
						const p = screen.get(n.id)!;
						return {
							id: n.id,
							x: p.x,
							y: p.y,
							r: Math.max(12, n.size),
							// About the size of the label at 0.75rem, with its plate.
							width: Math.max(...n.lines.map((l) => l.length)) * 6.6 + 10,
							height: 18 * n.lines.length,
							priority: priority(n)
						};
					}),
					{ width, height }
				)
			: new Map()
	);

	/** The hot node's neighbours on this map: marked, where the rest dim. */
	const near = $derived(
		new Set(
			view?.edges
				.filter((e) => hot && (e.a === hot || e.b === hot))
				.map((e) => (e.a === hot ? e.b : e.a)) ?? []
		)
	);
	const isLit = (e: { a: string; b: string }) => !!hot && (e.a === hot || e.b === hot);
	/** The edges, the hot node's last, so they are drawn over the rest. */
	const edges = $derived(
		view ? [...view.edges].sort((x, y) => Number(isLit(x)) - Number(isLit(y))) : []
	);
	/** How many a node is linked to on this map: said in the details. */
	const linkedTo = (node: string) =>
		view?.edges.filter((e) => e.a === node || e.b === node).length ?? 0;

	/** Focus from the keyboard brings a node forward, as the pointer does. */
	function focusNode(e: FocusEvent, node: string) {
		active = node;
		focused = (e.currentTarget as HTMLElement).matches(':focus-visible') ? node : null;
	}

	/** Open the map on a view. */
	export async function show(o: MapOpen) {
		opened = o;
		target = o.target;
		trail = [];
		failed = false;
		asList ??= matchMedia('(max-width: 40rem)').matches;
		dialog?.showModal();
		if (!index)
			try {
				index = new MapIndex(await load());
			} catch (e) {
				console.warn('map: could not load', e);
				failed = true;
			}
		await settle();
	}

	/** After the view changes: focus its centre (or its first entry), and describe it. */
	async function settle() {
		active = view?.center ?? null;
		hovered = focused = null;
		await tick();
		const first = asList
			? dialog?.querySelector<HTMLElement>('.list [data-stop]')
			: canvas?.querySelector<HTMLElement>(`[data-node="${CSS.escape(active ?? '')}"]`);
		(first ?? dialog?.querySelector<HTMLElement>('.close'))?.focus();
	}

	/** Set when the map closes to go somewhere: focus follows the jump, not the opener. */
	let leaving = false;

	function closed() {
		const back = leaving ? undefined : opened?.refocus;
		leaving = false;
		opened = null;
		back?.();
	}

	function goTo(t: MapTarget) {
		if (JSON.stringify(t) === JSON.stringify(target)) return;
		trail = [...trail, target];
		target = t;
		settle();
	}

	function goBack() {
		const t = trail.at(-1);
		if (!t) return;
		trail = trail.slice(0, -1);
		target = t;
		settle();
	}

	/** Centre the map on a node: a frame's neighbourhood, a name's frames, a subject's. */
	function centre(node: string) {
		const [kind, key] = [node[0], node.slice(2)];
		if (kind === 'f') goTo({ view: 'frame', key, steps: steps ?? 2 });
		else if (kind === 'n') goTo({ view: 'name', id: key });
		else goTo({ view: 'subject', id: key });
	}

	/** Go to a frame: close the map and jump there. */
	function follow(key: string) {
		leaving = true;
		dialog?.close();
		onfollow(subjectOf(key), key.slice(key.indexOf('/') + 1));
	}

	/** Enter goes: to a frame; a name or a subject has no place to go, so it centres. */
	function enter(node: string) {
		if (node[0] === 'f') follow(node.slice(2));
		else centre(node);
	}

	const frameHref = (key: string) => hrefOf(subjectOf(key), key.slice(key.indexOf('/') + 1));

	function pick(e: MouseEvent, key: string) {
		if (e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
		e.preventDefault();
		follow(key);
	}

	const ARROWS: Record<string, Direction> = {
		ArrowUp: 'up',
		ArrowDown: 'down',
		ArrowLeft: 'left',
		ArrowRight: 'right'
	};

	/**
	 * Keys on the map: an arrow moves to the neighbour that lies that way,
	 * Home to the centre, Enter goes, Space centres (the button's own click).
	 */
	function mapKeys(e: KeyboardEvent) {
		if (!view || !active) return;
		let to: string | null;
		if (ARROWS[e.key]) to = stepFrom(view, at, active, ARROWS[e.key]);
		else if (e.key === 'Home') to = view.center;
		else if (e.key === 'Enter') {
			e.preventDefault();
			enter(active);
			return;
		} else return;
		e.preventDefault();
		if (!to) return;
		active = to;
		canvas?.querySelector<HTMLElement>(`[data-node="${CSS.escape(to)}"]`)?.focus();
	}

	/** Keys anywhere in the map: Backspace goes back a view (outside a field). */
	function dialogKeys(e: KeyboardEvent) {
		if (e.key === 'Backspace' && trail.length && !(e.target as HTMLElement).matches('input')) {
			e.preventDefault();
			goBack();
		}
	}

	async function toggleList() {
		asList = !asList;
		await tick();
		settle();
	}

	function setSteps(n: 1 | 2) {
		if (target.view === 'frame' && target.steps !== n) {
			target = { ...target, steps: n };
			active = view?.center ?? null;
		}
	}

	const shapeOf = (n: MapNode) => (n.subject && index ? subjectSlot(index.data, n.subject) : null);
	const slotStyle = (n: MapNode) => {
		const s = shapeOf(n);
		return s?.slot
			? `var(--map-s${s.slot})`
			: n.kind === 'name'
				? 'var(--map-surface)'
				: 'var(--map-other)';
	};

	/** What the active node is, said in the details under the map. */
	const detail = $derived.by(() => {
		const n = active ? nodesById.get(active) : null;
		if (!n || !view || !index) return null;
		const why = view.edges.find(
			(e) =>
				e.kind === 'connection' &&
				((e.a === n.id && e.b === view.center) || (e.b === n.id && e.a === view.center))
		)?.why;
		const about =
			n.kind === 'name'
				? index.data.names[n.id.slice(2)]?.description
				: view.sections.flatMap((s) => s.items).find((i) => i.node === n.id)?.note;
		return { n, why, about: why ? null : about };
	});

	/** A node's name for a screen reader: all of it, and where it is. */
	const said = (n: MapNode) =>
		[
			n.full,
			n.detail,
			n.id === view?.center && view.target.view !== 'library' ? 'centre' : null,
			n.id === `f:${here}` ? 'you are here' : null
		]
			.filter(Boolean)
			.join(', ');

	/** The shapes, drawn in a 2r square around the node's centre. */
	function shapePath(shape: string, r: number) {
		const p = (pts: [number, number][]) => `M${pts.map(([x, y]) => `${x},${y}`).join('L')}Z`;
		const poly = (n: number, turn: number, k = r) =>
			Array.from({ length: n }, (_, i): [number, number] => {
				const a = turn + (2 * Math.PI * i) / n;
				return [Math.round(Math.cos(a) * k * 100) / 100, Math.round(Math.sin(a) * k * 100) / 100];
			});
		switch (shape) {
			case 'square':
				return p([
					[-r * 0.85, -r * 0.85],
					[r * 0.85, -r * 0.85],
					[r * 0.85, r * 0.85],
					[-r * 0.85, r * 0.85]
				]);
			case 'diamond':
				return p(poly(4, -Math.PI / 2, r * 1.15));
			case 'triangle':
				return p(poly(3, -Math.PI / 2, r * 1.2));
			case 'hexagon':
				return p(poly(6, 0));
			case 'star':
				return p(poly(10, -Math.PI / 2).map(([x, y], i) => (i % 2 ? [x * 0.5, y * 0.5] : [x, y])));
			default:
				return `M${-r},0A${r},${r} 0 1 0 ${r},0A${r},${r} 0 1 0 ${-r},0Z`;
		}
	}
</script>

{#snippet glyph(n: MapNode, r: number)}
	{@const s = shapeOf(n)}
	<svg
		class="glyph"
		width={r * 2 + 6}
		height={r * 2 + 6}
		viewBox="{-r - 3} {-r - 3} {r * 2 + 6} {r * 2 + 6}"
		aria-hidden="true"
	>
		<path
			d={shapePath(n.kind === 'name' ? 'circle' : (s?.shape ?? 'circle'), r)}
			fill={slotStyle(n)}
			stroke={n.kind === 'name' ? 'var(--map-ink)' : 'var(--map-surface)'}
			stroke-width={n.kind === 'name' ? 1.5 : 2}
		/>
	</svg>
{/snippet}

<!-- A modal: the page behind is inert while the map is open, and Esc closes it. -->
<dialog
	class="map {opened?.scheme ?? 'dark'}"
	aria-labelledby="{id}-title"
	data-own-keys
	bind:this={dialog}
	onclose={closed}
	onkeydown={dialogKeys}
>
	{#if opened}
		<header>
			{#if trail.length}
				<button type="button" class="back" onclick={goBack}>
					<span aria-hidden="true">←</span> Back
				</button>
			{/if}
			<h2 id="{id}-title">
				<span class="kicker">Map</span>
				{view?.title ?? 'The map'}
			</h2>
			<div class="controls">
				{#if here && !(target.view === 'frame' && target.key === here)}
					<button
						type="button"
						onclick={() => goTo({ view: 'frame', key: here, steps: steps ?? 2 })}
					>
						This frame
					</button>
				{/if}
				{#if target.view !== 'library'}
					<button type="button" onclick={() => goTo({ view: 'library' })}>Library</button>
				{/if}
				{#if steps}
					<div class="steps" role="radiogroup" aria-label="How far out">
						{#each [1, 2] as const as n (n)}
							<label>
								<input
									type="radio"
									name="{id}-steps"
									checked={steps === n}
									onchange={() => setSteps(n)}
								/>
								{n === 1 ? '1 step' : '2 steps'}
							</label>
						{/each}
					</div>
				{/if}
				<button type="button" role="switch" aria-checked={!!asList} onclick={toggleList}>
					Show as list
				</button>
				<button type="button" class="close" onclick={() => dialog?.close()}>
					<span aria-hidden="true">×</span>
					<span class="visually-hidden">Close the map</span>
				</button>
			</div>
		</header>

		{#if failed}
			<p class="empty">The map could not be loaded. Close it and try again.</p>
		{:else if !index}
			<p class="empty" role="status">Loading the map…</p>
		{:else if !view}
			<p class="empty">That is no longer on the map.</p>
		{:else if asList}
			<div class="list">
				{#each view.sections as s, i (s.title)}
					<section aria-labelledby="{id}-sec-{i}">
						<h3 id="{id}-sec-{i}">{s.title}</h3>
						<ul>
							{#each s.items as item (item.node)}
								{@const n = nodesById.get(item.node)!}
								<li>
									{#if item.node[0] === 'f'}
										{@const key = item.node.slice(2)}
										<!-- The page resolved these app routes. -->
										<!-- eslint-disable svelte/no-navigation-without-resolve -->
										<a
											href={frameHref(key)}
											data-stop
											aria-current={key === here ? 'page' : undefined}
											onclick={(e) => pick(e, key)}
										>
											{@render glyph(n, 5)}
											<span class="label">{item.label}</span>
											<span class="context"
												>{item.detail}{#if key === here}
													· you are here{/if}</span
											>
										</a>
										<!-- eslint-enable svelte/no-navigation-without-resolve -->
										<button type="button" class="centre" onclick={() => centre(item.node)}>
											Centre<span class="visually-hidden"> the map on {item.label}</span>
										</button>
									{:else}
										<button type="button" class="entry" data-stop onclick={() => centre(item.node)}>
											{@render glyph(n, 5)}
											<span class="label">{item.label}</span>
											<span class="context">{item.detail}</span>
										</button>
									{/if}
									{#if item.note}<p class="why">{item.note}</p>{/if}
								</li>
							{/each}
						</ul>
					</section>
				{:else}
					<p class="empty">Nothing is connected here yet.</p>
				{/each}
			</div>
		{:else}
			<!-- The nodes are the map's controls; the lines are drawn for the eye, and said in
			     the details and the list. The map's own keys: arrows, Home, Enter. -->
			<!-- svelte-ignore a11y_no_noninteractive_element_interactions -->
			<div
				class="canvas"
				role="group"
				aria-label="{view.title}: arrows move between neighbours, Enter goes, Space centres"
				bind:this={canvas}
				bind:clientWidth={width}
				bind:clientHeight={height}
				onkeydown={mapKeys}
			>
				{#if fit}
					<svg class="edges" class:emphasis={!!hot} {width} {height} aria-hidden="true">
						{#each edges as e (`${e.a} ${e.b}`)}
							{@const a = screen.get(e.a)!}
							{@const b = screen.get(e.b)!}
							<line
								class="edge {e.kind}"
								class:lit={isLit(e)}
								x1={a.x}
								y1={a.y}
								x2={b.x}
								y2={b.y}
								style:stroke-width={e.kind === 'between'
									? `${1 + Math.sqrt(e.weight) * 1.5}px`
									: null}
							/>
						{/each}
					</svg>
					{#each view.nodes as n (n.id)}
						{@const p = screen.get(n.id)!}
						{@const side = labels.get(n.id)}
						<button
							type="button"
							class="node {n.kind}"
							class:centre={n.id === view.center && view.target.view !== 'library'}
							class:here={n.id === `f:${here}`}
							class:active={n.id === active}
							class:hot={n.id === hot}
							class:near={near.has(n.id)}
							class:far={!!hot && n.id !== hot && !near.has(n.id)}
							style:left="{p.x}px"
							style:top="{p.y}px"
							style:--slot={slotStyle(n)}
							tabindex={n.id === active ? 0 : -1}
							data-node={n.id}
							aria-label={said(n)}
							onclick={() => (n.id === view.center ? (active = n.id) : centre(n.id))}
							ondblclick={() => enter(n.id)}
							onfocus={(e) => focusNode(e, n.id)}
							onblur={() => (focused = null)}
							onpointerenter={() => (active = hovered = n.id)}
							onpointerleave={() => (hovered = null)}
						>
							{@render glyph(n, n.size)}
							<span
								class="label {side ?? (p.x > width / 2 ? 'hidden to-left' : 'hidden')}"
								aria-hidden="true"
								>{#each n.lines as line, i (i)}<span>{line}</span>{/each}</span
							>
						</button>
					{/each}
				{/if}
			</div>
		{/if}

		<footer>
			{#if view && !asList}
				<div class="details" aria-live="polite">
					{#if detail}
						<p class="what">
							<strong>{detail.n.full}</strong>
							<span class="context">{detail.n.detail} · linked to {linkedTo(detail.n.id)} here</span
							>
						</p>
						{#if detail.why}<p class="why">{detail.why}</p>{/if}
						{#if detail.about}<p class="why">{detail.about}</p>{/if}
						<p class="actions">
							{#if detail.n.kind === 'frame'}
								{@const key = detail.n.id.slice(2)}
								<!-- eslint-disable-next-line svelte/no-navigation-without-resolve -->
								<a href={frameHref(key)} onclick={(e) => pick(e, key)}
									>Go to {detail.n.full} <kbd>Enter</kbd></a
								>
							{/if}
							{#if detail.n.id !== view.center}
								<button type="button" onclick={() => centre(detail.n.id)}>
									Centre on it <kbd>Space</kbd>
								</button>
							{/if}
						</p>
					{/if}
				</div>
			{/if}
			{#if view?.note}<p class="note">{view.note}</p>{/if}
			{#if index}
				<ul class="legend" aria-label="Subjects">
					{#each index.data.subjects as s (s.id)}
						{@const slot = subjectSlot(index.data, s.id)}
						<li>
							<svg width="14" height="14" viewBox="-7 -7 14 14" aria-hidden="true">
								<path
									d={shapePath(slot.shape === 'other' ? 'circle' : slot.shape, 5)}
									fill={slot.slot ? `var(--map-s${slot.slot})` : 'var(--map-other)'}
								/>
							</svg>
							{s.title}
						</li>
					{/each}
					<li>
						<svg width="14" height="14" viewBox="-7 -7 14 14" aria-hidden="true">
							<circle
								r="4.5"
								fill="var(--map-surface)"
								stroke="var(--map-ink)"
								stroke-width="1.5"
							/>
						</svg>
						A name
					</li>
				</ul>
			{/if}
		</footer>
	{/if}
</dialog>

<style>
	/* Its own surface, in the light of the palette it opens over, so the subject
	   colours hold (sprint 019): each is validated against these two surfaces. */
	.map {
		--map-surface: #fcfcfb;
		--map-raised: #f0efec;
		--map-ink: #1a1a19;
		--map-muted: #5f5e5a;
		--map-line: #b9b7ae;
		--map-s1: #2a78d6;
		--map-s2: #eb6834;
		--map-s3: #1baf7a;
		--map-s4: #4a3aa7;
		--map-s5: #e87ba4;
		--map-s6: #008300;
		--map-other: #8a8983;
		color-scheme: light;
	}
	.map.dark {
		--map-surface: #1a1a19;
		--map-raised: #262624;
		--map-ink: #f4f3ee;
		--map-muted: #c3c2b7;
		--map-line: #55544f;
		--map-s1: #3987e5;
		--map-s2: #d95926;
		--map-s3: #199e70;
		--map-s4: #9085e9;
		--map-s5: #d55181;
		--map-s6: #008300;
		--map-other: #8a8983;
		color-scheme: dark;
	}
	.map {
		width: 100vw;
		height: 100dvh;
		max-width: none;
		max-height: none;
		margin: 0;
		padding: 0;
		border: none;
		color: var(--map-ink);
		background: var(--map-surface);
		font-family: var(--sans, system-ui, sans-serif);
	}
	.map[open] {
		display: grid;
		grid-template-rows: auto minmax(0, 1fr) auto;
	}
	.map::backdrop {
		background: rgb(0 0 0 / 0.5);
	}
	header {
		display: flex;
		flex-wrap: wrap;
		align-items: center;
		gap: 0.5rem 1rem;
		padding: 0.75rem 1rem;
		border-bottom: 1px solid var(--map-line);
	}
	h2 {
		flex: 1 1 12rem;
		margin: 0;
		font-size: 1.05rem;
		font-weight: 600;
	}
	.kicker {
		display: block;
		font-size: 0.7rem;
		font-weight: 500;
		letter-spacing: 0.08em;
		text-transform: uppercase;
		color: var(--map-muted);
	}
	.controls {
		display: flex;
		flex-wrap: wrap;
		align-items: center;
		gap: 0.5rem;
	}
	button,
	.steps label,
	.actions a {
		font: inherit;
		font-size: 0.85rem;
		color: var(--map-ink);
		background: none;
		border: 1px solid var(--map-line);
		border-radius: 0.25rem;
		padding: 0.3rem 0.6rem;
		cursor: pointer;
		text-decoration: none;
	}
	button:hover,
	.actions a:hover {
		border-color: var(--map-ink);
	}
	button[role='switch'][aria-checked='true'] {
		background: var(--map-raised);
		border-color: var(--map-ink);
	}
	.steps {
		display: flex;
		gap: 0.25rem;
	}
	.steps label {
		display: flex;
		align-items: center;
		gap: 0.3rem;
	}
	.steps input {
		margin: 0;
		accent-color: var(--map-ink);
	}
	.close {
		font-size: 1.1rem;
		line-height: 1;
	}
	:focus-visible {
		outline: 2px solid var(--map-ink);
		outline-offset: 2px;
	}
	kbd {
		font-family: var(--mono, ui-monospace, monospace);
		font-size: 0.7rem;
		color: var(--map-muted);
	}
	.empty {
		margin: 2rem 1rem;
		color: var(--map-muted);
	}

	/* A double-click on a node goes: it must not select its label's words.
	   The details and the list stay selectable. */
	.canvas {
		position: relative;
		overflow: hidden;
		user-select: none;
		-webkit-user-select: none;
	}
	.edges {
		position: absolute;
		inset: 0;
	}
	/* At rest every line is dimmed toward the surface (sprint 020); the hot
	   node's lines come forward in full ink, and the rest recede further. */
	.edge {
		stroke: var(--map-line);
		stroke-width: 1.25;
		opacity: 0.7;
	}
	.edge.connection,
	.edge.between {
		stroke: var(--map-muted);
		stroke-width: 1.5;
		opacity: 0.35;
	}
	.edge.mention {
		stroke-dasharray: 2 3;
	}
	.emphasis .edge {
		opacity: 0.18;
	}
	.emphasis .edge.lit {
		stroke: var(--map-ink);
		opacity: 1;
	}
	.node {
		position: absolute;
		display: grid;
		place-items: center;
		/* A target of at least 24px (WCAG 2.5.8), centred on the node. */
		min-width: 1.5rem;
		min-height: 1.5rem;
		padding: 0;
		border: none;
		border-radius: 50%;
		transform: translate(-50%, -50%);
	}
	.node:hover {
		border: none;
	}
	.node .glyph {
		display: block;
	}
	.node.centre .glyph,
	.node.active .glyph {
		filter: drop-shadow(0 0 0 var(--map-ink));
	}
	.node.active::after,
	.node.near::after,
	.node.here::before {
		content: '';
		position: absolute;
		inset: -4px;
		border-radius: 50%;
		border: 1.5px solid var(--map-ink);
		pointer-events: none;
	}
	.node.here::before {
		border-style: dashed;
		inset: -7px;
	}
	/* The hot node's neighbours: outlined, their labels ruled in their subject's colour. */
	.node.near::after {
		inset: -3px;
		border-width: 1px;
	}
	.node.far {
		opacity: 0.35;
	}
	.node.hot,
	.node.near {
		z-index: 1;
	}
	/* On a plate of the surface, so no line runs through the words. */
	.label {
		position: absolute;
		display: grid;
		justify-items: start;
		padding: 0 0.2rem;
		white-space: nowrap;
		font-size: 0.75rem;
		line-height: 18px;
		color: var(--map-ink);
		background: var(--map-surface);
		border-radius: 0.2rem;
		pointer-events: none;
	}
	.label.left {
		justify-items: end;
	}
	.label.above,
	.label.below {
		justify-items: center;
	}
	.node.near .label > span {
		text-decoration: underline 2px var(--slot);
		text-underline-offset: 3px;
	}
	.node.hot .label {
		font-weight: 600;
	}
	.node.name .label {
		color: var(--map-muted);
		font-style: italic;
	}
	.node.centre .label {
		font-weight: 600;
		font-size: 0.85rem;
	}
	.label.right {
		left: calc(100% + 4px);
		top: 50%;
		transform: translateY(-50%);
	}
	.label.left {
		right: calc(100% + 4px);
		top: 50%;
		transform: translateY(-50%);
	}
	.label.above {
		bottom: calc(100% + 4px);
		left: 50%;
		transform: translateX(-50%);
	}
	.label.below {
		top: calc(100% + 4px);
		left: 50%;
		transform: translateX(-50%);
	}
	/* A label with no room waits for focus or the pointer, and sits over the rest. */
	.label.hidden {
		display: none;
		left: calc(100% + 4px);
		top: 50%;
		transform: translateY(-50%);
		padding: 0 0.3rem;
		background: var(--map-surface);
		border: 1px solid var(--map-line);
		border-radius: 0.2rem;
	}
	.label.hidden.to-left {
		left: auto;
		right: calc(100% + 4px);
	}
	.node.active,
	.node.hot {
		z-index: 2;
	}
	.node.active .label.hidden,
	.node.hot .label.hidden,
	.node.near .label.hidden {
		display: grid;
	}

	footer {
		display: grid;
		gap: 0.4rem;
		padding: 0.6rem 1rem 0.75rem;
		border-top: 1px solid var(--map-line);
		font-size: 0.85rem;
	}
	/* One height for every state, empty or full, so the graph above never
	   resizes as the pointer moves (sprint 020): the lines are clamped, and
	   the list has them whole. */
	.details {
		display: grid;
		align-content: start;
		gap: 0.25rem;
		/* One line of what, two of why, a row of buttons. */
		height: 6rem;
		overflow: hidden;
	}
	.details p {
		margin: 0;
		line-height: 1.35;
	}
	.details .what {
		overflow: hidden;
		white-space: nowrap;
		text-overflow: ellipsis;
	}
	.details .why {
		max-height: 2.7em;
		overflow: hidden;
	}
	.context {
		color: var(--map-muted);
		font-size: 0.8rem;
	}
	.what .context {
		margin-left: 0.5rem;
	}
	.why {
		margin: 0;
		color: var(--map-muted);
		font-size: 0.8rem;
		max-width: 60rem;
	}
	.actions {
		display: flex;
		flex-wrap: wrap;
		gap: 0.5rem;
		margin-top: 0.2rem !important;
	}
	.note {
		margin: 0;
		color: var(--map-muted);
		font-size: 0.8rem;
	}
	.legend {
		display: flex;
		flex-wrap: wrap;
		gap: 0.25rem 1rem;
		margin: 0;
		padding: 0;
		list-style: none;
		font-size: 0.8rem;
		color: var(--map-muted);
	}
	.legend li {
		display: flex;
		align-items: center;
		gap: 0.35rem;
	}

	.list {
		overflow-y: auto;
		padding: 0.5rem 1rem 1rem;
	}
	.list section {
		max-width: 44rem;
	}
	.list h3 {
		margin: 1rem 0 0.4rem;
		font-size: 0.75rem;
		font-weight: 600;
		letter-spacing: 0.06em;
		text-transform: uppercase;
		color: var(--map-muted);
	}
	.list ul {
		margin: 0;
		padding: 0;
		list-style: none;
	}
	.list li {
		display: grid;
		grid-template-columns: minmax(0, 1fr) auto;
		align-items: center;
		gap: 0 0.5rem;
		padding: 0.35rem 0;
		border-bottom: 1px solid var(--map-line);
	}
	/* The glyph, then the title with its context under it. */
	.list li a,
	.list .entry {
		display: grid;
		grid-template-columns: auto minmax(0, 1fr);
		align-items: center;
		gap: 0 0.5rem;
		min-height: 1.5rem;
		padding: 0.1rem 0;
		color: var(--map-ink);
		text-decoration: none;
		border: none;
		text-align: left;
		font-size: 0.9rem;
	}
	.list .entry {
		grid-column: 1 / -1;
	}
	.list li a:hover .label,
	.list .entry:hover .label {
		text-decoration: underline;
	}
	.list .context {
		grid-column: 2;
	}
	.list .label {
		position: static;
		white-space: normal;
		font-size: inherit;
		line-height: 1.3;
	}
	.list .why {
		grid-column: 1 / -1;
	}
	.list .centre {
		font-size: 0.75rem;
		padding: 0.15rem 0.45rem;
	}
	.list [aria-current='page'] .label {
		font-weight: 600;
	}
	@media (max-width: 40rem) {
		header {
			padding: 0.5rem 0.75rem;
		}
		footer {
			padding: 0.5rem 0.75rem;
		}
		.details {
			/* Two lines of what, one of why, buttons that may wrap. */
			height: 8.2rem;
		}
		.details .what {
			white-space: normal;
			max-height: 2.7em;
		}
		.details .why {
			max-height: 1.35em;
		}
		.list {
			padding: 0.25rem 0.75rem 1rem;
		}
	}
</style>

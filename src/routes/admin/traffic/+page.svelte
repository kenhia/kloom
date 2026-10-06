<script lang="ts">
	import { resolve } from '$app/paths';
	import { TOP_LEVEL, type TrafficCell, type TrafficRow } from '$engine/traffic';
	import Plain from '$lib/page/Plain.svelte';
	import type { PageProps } from './$types';

	let { data }: PageProps = $props();

	const LEVELS = Array.from({ length: TOP_LEVEL + 1 }, (_, i) => i);
	const frameHref = (subject: string, frame: string) =>
		resolve('/[subject]/[[frame]]', { subject, frame });
	const readers = (n: number) => `${n} reader${n === 1 ? '' : 's'}`;
	const say = (c: TrafficCell) =>
		`${c.title}, ${c.position}${c.trail ? `, on the trail ${c.trail}` : ''}: ${readers(c.readers)}`;

	/** The cell under the pointer or focus, said in the readout. */
	let shown = $state<{ row: TrafficRow; cell: TrafficCell } | null>(null);
	/** Each row's one tab stop (a roving tabindex): Tab passes a row, arrows move in it. */
	let stops = $state<Record<string, number>>({});
	const stopOf = (subject: string) => stops[subject] ?? 0;

	const grid = (el: HTMLElement, r: number, i: number) =>
		el.closest('.rows')?.querySelector<HTMLAnchorElement>(`[data-row="${r}"] a[data-cell="${i}"]`);

	function onkeydown(e: KeyboardEvent, r: number, i: number) {
		const row = data.rows[r];
		let to: [number, number] | null = null;
		if (e.key === 'ArrowRight') to = [r, Math.min(i + 1, row.cells.length - 1)];
		else if (e.key === 'ArrowLeft') to = [r, Math.max(i - 1, 0)];
		else if (e.key === 'Home') to = [r, 0];
		else if (e.key === 'End') to = [r, row.cells.length - 1];
		else if (e.key === 'ArrowDown' && r + 1 < data.rows.length)
			to = [r + 1, Math.min(i, data.rows[r + 1].cells.length - 1)];
		else if (e.key === 'ArrowUp' && r > 0)
			to = [r - 1, Math.min(i, data.rows[r - 1].cells.length - 1)];
		if (!to) return;
		e.preventDefault();
		stops[data.rows[to[0]].subject] = to[1];
		grid(e.currentTarget as HTMLElement, ...to)?.focus();
	}
</script>

<!--
	The traffic page (docs/design.md §Traffic, korg 3570), for admins only: a
	GitHub-style grid, a row per subject and a cell per frame, each trail's
	frames after the frame it branches from in a second hue. A cell is lit by
	the distinct readers who opened the frame, in five steps, and opens it.
-->
<Plain title="Traffic" wide>
	<h1>Traffic</h1>
	<p>
		Each square is a frame, in spine order, with a trail's frames after the frame it branches from.
		The brighter the square, the more readers have opened it. Trail frames are in the second color.
	</p>

	<div class="legend" aria-hidden="true">
		<span>Less</span>
		{#each LEVELS as level (level)}
			<span class="cell" data-level={level}></span>
		{/each}
		<span>More</span>
		<span class="cell trail" data-level={TOP_LEVEL}></span>
		<span>Trail</span>
	</div>
	<p class="hint">Levels: no readers, 1, 2, 3, and 4 or more.</p>

	<p class="readout" aria-hidden="true">
		{#if shown}
			<strong>{shown.row.title}</strong> · {shown.cell.title} · {shown.cell
				.position}{#if shown.cell.trail}
				· {shown.cell.trail}{/if} · {readers(shown.cell.readers)}
		{:else}
			Point at a square, or move to one with the arrow keys.
		{/if}
	</p>

	<div class="rows">
		{#each data.rows as row, r (row.subject)}
			<section class="row" data-row={r} aria-labelledby="row-{row.subject}">
				<h2 id="row-{row.subject}">
					{row.title}
					<span class="count"
						>{row.cells.filter((c) => c.readers).length} of {row.cells.length} frames opened</span
					>
				</h2>
				<ul class="cells">
					{#each row.cells as cell, i (cell.id)}
						<li>
							<a
								class="cell"
								class:trail={cell.trail}
								data-level={cell.level}
								data-cell={i}
								data-frame={cell.id}
								href={frameHref(row.subject, cell.id)}
								aria-label={say(cell)}
								tabindex={i === stopOf(row.subject) ? 0 : -1}
								onkeydown={(e) => onkeydown(e, r, i)}
								onfocus={() => {
									stops[row.subject] = i;
									shown = { row, cell };
								}}
								onpointerenter={() => (shown = { row, cell })}
							></a>
						</li>
					{/each}
				</ul>
			</section>
		{/each}
	</div>
</Plain>

<style>
	/* The two hues, and an empty square, in the page's dark and light. */
	.rows,
	.legend,
	.readout {
		--main: #e2b45f;
		--side: #6fb7c9;
		--empty: #2a2925;
		--page: #0b0b0d;
	}
	@media (prefers-color-scheme: light) {
		.rows,
		.legend,
		.readout {
			--main: #9a6200;
			--side: #19708a;
			--empty: #e6e0d2;
			--page: #f6f2e8;
		}
	}
	.legend {
		display: flex;
		flex-wrap: wrap;
		gap: 0.3rem;
		align-items: center;
		font-size: 0.9rem;
		color: var(--muted);
	}
	.legend span:not(.cell) {
		margin: 0 0.25rem;
	}
	.readout {
		position: sticky;
		top: 0;
		z-index: 1;
		min-height: 1.6em;
		padding: 0.4rem 0;
		background: var(--page);
	}
	.row h2 {
		display: flex;
		flex-wrap: wrap;
		gap: 0.25rem 0.75rem;
		align-items: baseline;
		margin-top: 1.25rem;
		font-size: 1.1rem;
	}
	.count {
		font: 0.85rem var(--sans);
		color: var(--muted);
	}
	.cells {
		display: flex;
		flex-wrap: wrap;
		gap: 3px;
		padding: 0;
		list-style: none;
	}
	.cells li {
		margin: 0;
	}
	.cell {
		display: block;
		box-sizing: border-box;
		width: 0.8rem;
		height: 0.8rem;
		border-radius: 2px;
		background: var(--empty);
	}
	.cell[data-level='1'] {
		background: color-mix(in srgb, var(--main) 35%, var(--empty));
	}
	.cell[data-level='2'] {
		background: color-mix(in srgb, var(--main) 58%, var(--empty));
	}
	.cell[data-level='3'] {
		background: color-mix(in srgb, var(--main) 80%, var(--empty));
	}
	.cell[data-level='4'] {
		background: var(--main);
	}
	.cell.trail {
		outline: 1px solid color-mix(in srgb, var(--side) 45%, transparent);
		outline-offset: -1px;
	}
	.cell.trail[data-level='1'] {
		background: color-mix(in srgb, var(--side) 35%, var(--empty));
	}
	.cell.trail[data-level='2'] {
		background: color-mix(in srgb, var(--side) 58%, var(--empty));
	}
	.cell.trail[data-level='3'] {
		background: color-mix(in srgb, var(--side) 80%, var(--empty));
	}
	.cell.trail[data-level='4'] {
		background: var(--side);
	}
	a.cell:hover {
		outline: 2px solid var(--ink);
		outline-offset: 1px;
	}
	@media (max-width: 30rem) {
		.cell {
			width: 0.7rem;
			height: 0.7rem;
		}
	}
</style>

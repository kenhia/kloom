<script lang="ts">
	import { onMount, untrack } from 'svelte';
	import type { CardEntry, NameCard } from '../graph';

	/**
	 * A name's card (docs/design.md §Connections): what the name is, then the
	 * frames it appears on, the frame chiefly about it first, grouped by
	 * subject with the reader's own first. Each is a link that jumps there. A
	 * popover beside the name, not a modal: Esc, or a click or focus outside,
	 * closes it and focus goes back to the name.
	 */
	interface Props {
		/** The card, or null when the registry has no such name. */
		card: NameCard | null;
		/** The words the reading marked. */
		label: string;
		/** The mark itself: pressing it again closes the card, as a toggle. */
		anchor: HTMLElement;
		/** Where it sits in the reading: below the name. */
		top: number;
		left: number;
		/** The frame the reader is on: listed, but not a link. */
		here: { subject: string; frame: string };
		hrefOf: (subject: string, frame: string) => string;
		onfollow: (subject: string, frame: string) => void;
		/** Closed; `refocus` when focus should go back to the name. */
		onclose: (refocus: boolean) => void;
	}

	let { card, label, anchor, top, left, here, hrefOf, onfollow, onclose }: Props = $props();

	// Kept as they were at opening: closing clears what they were read from.
	const mark = untrack(() => anchor);
	const id = $props.id();
	let root = $state<HTMLElement>();
	onMount(() => root?.focus());

	const KIND: Record<NameCard['kind'], string> = {
		person: 'Person',
		place: 'Place',
		org: 'Organisation',
		artifact: 'Artifact',
		idea: 'Idea',
		event: 'Event'
	};
	const isHere = (e: CardEntry) => e.subject === here.subject && e.frame === here.frame;
	const count = $derived(
		card ? (card.home ? 1 : 0) + card.groups.reduce((n, g) => n + g.entries.length, 0) : 0
	);

	function keydown(e: KeyboardEvent) {
		if (e.key !== 'Escape') return;
		e.preventDefault();
		onclose(true);
	}

	function follow(e: MouseEvent, entry: CardEntry) {
		if (e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
		e.preventDefault();
		onclose(false);
		onfollow(entry.subject, entry.frame);
	}

	function outside(e: PointerEvent) {
		const at = e.target as Node;
		if (root && !root.contains(at) && !mark.contains(at)) onclose(false);
	}

	function focusout(e: FocusEvent) {
		const to = e.relatedTarget as Node | null;
		if (to && root && !root.contains(to) && to !== mark) onclose(false);
	}
</script>

<svelte:window onpointerdown={outside} />

{#snippet entry(e: CardEntry)}
	{#if isHere(e)}
		<span class="entry" aria-current="page">
			<span class="title">{e.title}</span>
			<span class="context">{e.label}{e.trail ? ` · ${e.trail}` : ''} · you are here</span>
		</span>
	{:else}
		<!-- The page resolved this app route. -->
		<!-- eslint-disable-next-line svelte/no-navigation-without-resolve -->
		<a class="entry" href={hrefOf(e.subject, e.frame)} onclick={(ev) => follow(ev, e)}>
			<span class="title">{e.title}</span>
			<span class="context">{e.label}{e.trail ? ` · ${e.trail}` : ''}</span>
		</a>
	{/if}
{/snippet}

<!-- The page's own keys stand down in here: data-own-keys. -->
<div
	class="card"
	role="dialog"
	aria-labelledby="{id}-name"
	aria-describedby="{id}-about"
	tabindex="-1"
	data-own-keys
	style:top="{top}px"
	style:left="{left}px"
	bind:this={root}
	onkeydown={keydown}
	onfocusout={focusout}
>
	<div class="head">
		<p id="{id}-name" class="name">{card?.name ?? label}</p>
		<button type="button" class="close" onclick={() => onclose(true)}>
			<span aria-hidden="true">×</span>
			<span class="visually-hidden">Close</span>
		</button>
	</div>
	{#if card}
		<p id="{id}-about" class="about">
			<span class="kind">{KIND[card.kind]}.</span>
			{card.description}
		</p>
		{#if card.home}
			<p class="group">Chiefly</p>
			<ul>
				<li>{@render entry(card.home)}</li>
			</ul>
		{/if}
		{#if count > 1}
			<p class="group">Appears in…</p>
			{#each card.groups as g (g.subject)}
				<p class="subject">{g.subjectTitle}</p>
				<ul aria-label={g.subjectTitle}>
					{#each g.entries as e (e.frame)}
						<li>{@render entry(e)}</li>
					{/each}
				</ul>
			{/each}
		{:else}
			<p class="note">Appears only here, so far.</p>
		{/if}
		{#if card.wikidata}
			<p class="note">
				<a href="https://www.wikidata.org/wiki/{card.wikidata}" rel="noopener noreferrer"
					>{card.wikidata} on Wikidata</a
				>
			</p>
		{/if}
	{:else}
		<p id="{id}-about" class="note">This name is not in the name registry.</p>
	{/if}
</div>

<style>
	.card {
		position: absolute;
		z-index: 5;
		display: grid;
		gap: 0.4rem;
		width: min(22rem, calc(100% - 2rem));
		max-height: 60dvh;
		overflow-y: auto;
		padding: 0.75rem 1rem;
		font-family: var(--sans, inherit);
		font-size: 0.875rem;
		line-height: 1.45;
		color: var(--ink);
		background: var(--background);
		border: 1px solid var(--muted);
		border-radius: 0.25rem;
		box-shadow: 0 0.5rem 1.5rem color-mix(in srgb, #000 35%, transparent);
	}
	p {
		margin: 0;
	}
	.head {
		display: flex;
		align-items: start;
		justify-content: space-between;
		gap: 0.5rem;
	}
	.name {
		font-family: var(--serif);
		font-size: 1.15rem;
	}
	.close {
		font: 1rem/1 var(--serif);
		padding: 0.15rem 0.4rem;
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
	.kind {
		color: var(--muted);
	}
	.group,
	.subject {
		margin-top: 0.35rem;
		font-family: var(--mono);
		font-size: 0.7rem;
		letter-spacing: 0.12em;
		text-transform: uppercase;
		color: var(--muted);
	}
	.subject {
		color: var(--accent);
	}
	ul {
		display: grid;
		gap: 0.3rem;
		margin: 0;
		padding: 0;
		list-style: none;
	}
	.entry {
		display: grid;
		color: var(--ink);
		text-decoration: none;
	}
	a.entry:hover .title {
		text-decoration: underline;
		text-decoration-color: var(--accent);
	}
	.context,
	.note {
		font-size: 0.75rem;
		color: var(--muted);
	}
	.note a {
		color: inherit;
		text-decoration-color: var(--accent);
	}
</style>

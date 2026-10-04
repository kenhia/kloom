<script lang="ts">
	import Icon from './Icon.svelte';
	import type { JumpItem } from '../reader-data';
	import { tooltip } from './tooltip';

	interface Props {
		/** Whether the frame on the spine is bookmarked. */
		marked: boolean;
		items: JumpItem[];
		/** Where the reader's data can be saved from; the page resolves it. */
		exportHref?: string;
		ontoggle: () => void;
		onjump: (frame: string) => void;
		onremove: (item: JumpItem) => void;
		/** The reader's key for bookmarking, as they see it written; none when turned off. */
		key?: string | null;
	}

	let { marked, items, exportHref, ontoggle, onjump, onremove, key = null }: Props = $props();

	const id = $props.id();
	let open = $state(false);
	let root = $state<HTMLElement>();
	let opener = $state<HTMLButtonElement>();

	function close(refocus: boolean) {
		open = false;
		if (refocus) opener?.focus();
	}

	/** Esc closes the list and returns focus to its button, before the shell sees it. */
	function escape(e: KeyboardEvent) {
		if (e.key !== 'Escape' || !open) return;
		e.preventDefault();
		close(true);
	}

	function outside(e: PointerEvent) {
		if (open && !root?.contains(e.target as Node)) close(false);
	}

	function jump(e: MouseEvent, item: JumpItem) {
		if (!item.frame || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
		e.preventDefault();
		onjump(item.frame);
		close(false);
	}
</script>

<svelte:window onpointerdown={outside} />

<div class="bookmarks" bind:this={root}>
	<button
		type="button"
		class="icon"
		aria-pressed={marked}
		use:tooltip={key ? `Bookmark this frame (${key})` : 'Bookmark this frame'}
		onclick={ontoggle}
	>
		<Icon name="bookmark" filled={marked} />
		<span class="visually-hidden">Bookmark this frame</span>
	</button>
	<button
		type="button"
		class="icon"
		aria-expanded={open}
		aria-controls="{id}-panel"
		bind:this={opener}
		use:tooltip={`Bookmarks (${items.length})`}
		onclick={() => (open = !open)}
		onkeydown={escape}
	>
		<Icon name="bookmarks" />
		<span class="visually-hidden">Bookmarks ({items.length})</span>
	</button>

	<!-- The page's own keys (arrows, S, T, B) stand down in here: data-own-keys. -->
	<div
		id="{id}-panel"
		class="panel"
		role="group"
		aria-labelledby="{id}-title"
		data-own-keys
		hidden={!open}
	>
		<p id="{id}-title" class="title">Bookmarks</p>
		{#if items.length}
			<ul>
				{#each items as item (item.key)}
					<li>
						<!-- The page resolved these app routes. -->
						<!-- eslint-disable-next-line svelte/no-navigation-without-resolve -->
						<a href={item.href} onclick={(e) => jump(e, item)} onkeydown={escape}>
							<span class="label">{item.label}</span>
							<span class="context">{item.context}</span>
						</a>
						<button type="button" class="remove" onclick={() => onremove(item)} onkeydown={escape}>
							<span aria-hidden="true">×</span>
							<span class="visually-hidden">Remove bookmark: {item.label}</span>
						</button>
					</li>
				{/each}
			</ul>
		{:else}
			<p class="note">None yet. B, or the bookmark button, marks the frame you are on.</p>
		{/if}
		{#if exportHref}
			<p class="note">
				<!-- The page resolved this app route. -->
				<!-- eslint-disable-next-line svelte/no-navigation-without-resolve -->
				<a href={exportHref} download onkeydown={escape}>Export my reading data</a>
			</p>
		{/if}
	</div>
</div>

<style>
	.bookmarks {
		position: relative;
		display: flex;
		gap: 0.25rem;
		text-transform: none;
		letter-spacing: 0;
	}
	.icon {
		display: grid;
		place-items: center;
		width: 2rem;
		height: 2rem;
		padding: 0;
		color: var(--muted);
		background: none;
		border: 1px solid transparent;
		border-radius: 0.25rem;
		cursor: pointer;
	}
	.icon:hover,
	.icon[aria-expanded='true'] {
		color: var(--ink);
		border-color: var(--muted);
	}
	.icon[aria-pressed='true'] {
		color: var(--accent);
	}
	.icon :global(svg) {
		width: 1.25rem;
		height: 1.25rem;
	}
	.panel {
		position: absolute;
		top: calc(100% + 0.35rem);
		right: 0;
		z-index: 5;
		display: grid;
		gap: 0.5rem;
		width: max-content;
		min-width: 14rem;
		max-width: min(24rem, calc(100vw - 2rem));
		max-height: 60dvh;
		overflow-y: auto;
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
	.title,
	.note {
		margin: 0;
	}
	.title {
		font-family: var(--mono);
		font-size: 0.75rem;
		letter-spacing: 0.12em;
		text-transform: uppercase;
		color: var(--muted);
	}
	.note {
		font-size: 0.8rem;
		color: var(--muted);
	}
	.note a {
		color: var(--accent);
	}
	ul {
		display: grid;
		gap: 0.35rem;
		margin: 0;
		padding: 0;
		list-style: none;
	}
	li {
		display: flex;
		align-items: start;
		gap: 0.5rem;
	}
	li a {
		display: grid;
		flex: 1;
		color: var(--ink);
		text-decoration: none;
	}
	li a:hover .label {
		text-decoration: underline;
	}
	.context {
		font-size: 0.75rem;
		color: var(--muted);
	}
	.remove {
		font: 1rem/1 var(--serif);
		padding: 0.15rem 0.4rem;
		color: var(--muted);
		background: none;
		border: 1px solid transparent;
		border-radius: 0.25rem;
		cursor: pointer;
	}
	.remove:hover {
		color: var(--ink);
		border-color: var(--muted);
	}
</style>

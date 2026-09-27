<script lang="ts">
	import type { Snippet } from 'svelte';
	import { bibliography, chicago } from '../citation';
	import type { Frame, Trail } from '../model';
	import type { SyncMode } from '../navigation';

	interface Props {
		frame: Frame;
		/** The frame under the spine cursor, to say when the two differ. */
		spineFrame: Frame;
		sync: SyncMode;
		/** Trails that branch from the narrative's frame. */
		trails: Trail[];
		onsync: () => void;
		onsyncmode: (mode: SyncMode) => void;
		onenter: (trail: Trail) => void;
		/** The scrolling element, so the shell can drive it from the keyboard. */
		element?: HTMLElement;
		/** Extra controls at the end of the toolbar (the settings gear). */
		tools?: Snippet;
	}

	let {
		frame,
		spineFrame,
		sync,
		trails,
		onsync,
		onsyncmode,
		onenter,
		element = $bindable(),
		tools
	}: Props = $props();

	const behind = $derived(frame.id !== spineFrame.id);

	// A new frame starts at its top.
	$effect(() => {
		void frame.id;
		element?.scrollTo({ top: 0 });
	});
</script>

<section class="narrative" aria-label="Narrative">
	<div class="controls">
		<button type="button" class="sync" onclick={onsync} aria-describedby="sync-state">
			Sync Narrative <kbd>S</kbd>
		</button>
		<label class="follow">
			<input
				type="checkbox"
				checked={sync === 'follow'}
				onchange={(e) => onsyncmode(e.currentTarget.checked ? 'follow' : 'manual')}
			/>
			Follow the spine
		</label>
		{@render tools?.()}
		<p id="sync-state" class="state" aria-live="polite">
			{#if behind}
				Showing {frame.position.label}; the spine is at {spineFrame.position.label}.
			{:else}
				In step with the spine.
			{/if}
		</p>
	</div>

	<!-- Focusable because it scrolls: keyboard users must be able to reach it. -->
	<!-- svelte-ignore a11y_no_noninteractive_tabindex -->
	<article class="reading" tabindex="0" aria-labelledby="reading-title" bind:this={element}>
		<p class="position">{frame.position.label}</p>
		<h2 id="reading-title">{frame.scene.headline} <em>{frame.scene.accent}</em></h2>

		<div class="body">
			<!-- Rendered on load with raw HTML escaped and unsafe links dropped. -->
			<!-- eslint-disable-next-line svelte/no-at-html-tags -->
			{@html frame.readingHtml}
		</div>

		{#if trails.length}
			<h3>Trails from here</h3>
			<ul class="trails">
				{#each trails as trail (trail.id)}
					<li>
						<button type="button" onclick={() => onenter(trail)}>{trail.title} <kbd>T</kbd></button>
					</li>
				{/each}
			</ul>
		{/if}

		<h3>Sources</h3>
		<ol class="sources">
			{#each frame.sources as source, i (i)}
				<li>
					{#if source.url}
						<!-- An external source, not an app route. -->
						<!-- eslint-disable-next-line svelte/no-navigation-without-resolve -->
						<a href={source.url} rel="noopener noreferrer">{source.title}</a>
					{:else}
						{source.title}
					{/if}
					{#if source.note}<span class="note">— {source.note}</span>{/if}
				</li>
			{/each}
		</ol>

		{#if frame.citations?.length}
			<details class="citations">
				<summary>Citations ({frame.citations.length})</summary>
				<ul>
					{#each bibliography(frame.citations) as citation, i (i)}
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
	</article>
</section>

<style>
	.narrative {
		display: grid;
		grid-template-rows: auto minmax(0, 1fr);
		min-height: 0;
		border-left: 1px solid color-mix(in srgb, var(--muted) 40%, transparent);
	}

	.controls {
		display: flex;
		flex-wrap: wrap;
		align-items: center;
		gap: 0.5rem 1rem;
		padding: 0.75rem 1.5rem;
		border-bottom: 1px solid color-mix(in srgb, var(--muted) 40%, transparent);
		font-size: 0.875rem;
	}
	.sync {
		font: inherit;
		padding: 0.35rem 0.75rem;
		color: var(--ink);
		background: none;
		border: 1px solid var(--accent);
		border-radius: 0.25rem;
		cursor: pointer;
	}
	.follow {
		display: inline-flex;
		gap: 0.35rem;
		align-items: center;
	}
	.state {
		flex-basis: 100%;
		margin: 0;
		color: var(--muted);
		font-size: 0.8rem;
	}

	.reading {
		overflow-y: auto;
		overscroll-behavior: contain;
		padding: 1.25rem 1.5rem 2rem;
		line-height: 1.6;
	}
	.position {
		margin: 0;
		font-family: var(--mono);
		font-size: 0.75rem;
		letter-spacing: 0.12em;
		text-transform: uppercase;
		color: var(--muted);
	}
	h2 {
		margin: 0.25rem 0 1rem;
		font-family: var(--serif);
		font-size: 1.75rem;
		font-weight: normal;
		text-transform: uppercase;
	}
	h2 em {
		font-style: normal;
		color: var(--accent);
	}
	h3 {
		margin: 1.75rem 0 0.5rem;
		font-family: var(--mono);
		font-size: 0.75rem;
		font-weight: normal;
		letter-spacing: 0.12em;
		text-transform: uppercase;
		color: var(--muted);
	}
	.body :global(a),
	.sources a {
		color: inherit;
		text-decoration-color: var(--accent);
	}
	.body :global(h3) {
		margin: 1.75rem 0 0.5rem;
		font-family: var(--serif);
		font-size: 1.25rem;
		font-weight: normal;
	}
	.body :global(img) {
		display: block;
		max-width: 100%;
		height: auto;
		margin: 1rem auto 0.25rem;
	}
	.body :global(.figure) {
		display: block;
	}
	.body :global(.credit) {
		display: block;
		font-size: 0.75rem;
		text-align: center;
		color: var(--muted);
	}
	.body :global(table) {
		border-collapse: collapse;
		font-size: 0.875rem;
		margin: 0.5rem 0 1rem;
	}
	.body :global(th),
	.body :global(td) {
		padding: 0.2rem 0.75rem 0.2rem 0;
		border-bottom: 1px solid color-mix(in srgb, var(--muted) 40%, transparent);
		text-align: left;
	}
	.body :global(td:last-child),
	.body :global(th:last-child) {
		text-align: right;
		font-variant-numeric: tabular-nums;
	}
	.body :global(blockquote) {
		margin: 1rem 0;
		padding-left: 1rem;
		border-left: 2px solid var(--accent);
		font-family: var(--serif);
		font-style: italic;
	}
	.citations {
		margin-top: 0.75rem;
		font-size: 0.8rem;
	}
	.citations summary {
		cursor: pointer;
		width: fit-content;
		font-family: var(--mono);
		letter-spacing: 0.08em;
		text-transform: uppercase;
		color: var(--muted);
	}
	.citations ul {
		padding-left: 1.25rem;
	}
	.citations li {
		margin-bottom: 0.4rem;
		padding-left: 1.5em;
		text-indent: -1.5em;
		list-style: none;
		overflow-wrap: anywhere;
	}
	.citations a {
		color: inherit;
		text-decoration-color: var(--accent);
	}
	.trails {
		margin: 0;
		padding: 0;
		list-style: none;
	}
	.trails button {
		font: inherit;
		color: var(--ink);
		background: none;
		border: 1px dashed var(--accent);
		border-radius: 0.25rem;
		padding: 0.35rem 0.75rem;
		cursor: pointer;
	}
	.sources {
		padding-left: 1.25rem;
		font-size: 0.875rem;
	}
	.note {
		color: var(--muted);
	}
	kbd {
		font-family: var(--mono);
		font-size: 0.7rem;
		padding: 0 0.3rem;
		border: 1px solid var(--muted);
		border-radius: 0.2rem;
		color: var(--muted);
	}
</style>

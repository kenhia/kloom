<script lang="ts">
	import type { Note } from '../reader-data';

	interface Props {
		/** The frame's headline and accent. */
		title: string;
		/** The reader's notes on the frame in the reading pane, oldest first. */
		notes: Note[];
		/** The note in the editor now, if it is one of these. */
		editing?: string | null;
		/** Annotations whose words the reading no longer has. */
		detached?: string[];
		/** The add-note key, when it is on. */
		key?: string | null;
		/** The tab this is the panel of. */
		tab: string;
		hidden?: boolean;
		onadd: (from: HTMLElement) => void;
		onedit: (note: Note, from: HTMLElement) => void;
		ondelete: (note: Note) => void;
		/** Take the reader to an annotation's words in the reading. */
		onshow: (note: Note) => void;
	}

	let {
		title,
		notes,
		editing = null,
		detached = [],
		key = null,
		tab,
		hidden = false,
		onadd,
		onedit,
		ondelete,
		onshow
	}: Props = $props();

	const when = (iso: string) =>
		new Date(iso).toLocaleString(undefined, { dateStyle: 'medium', timeStyle: 'short' });
</script>

<div id="notes-panel" class="notes" role="tabpanel" aria-labelledby={tab} {hidden}>
	<div class="controls">
		<h2>Your notes <span>on {title}</span></h2>
		<button type="button" class="add" onclick={(e) => onadd(e.currentTarget)}>
			Add a note {#if key}<kbd>{key}</kbd>{/if}
		</button>
	</div>

	<!-- Focusable because it scrolls: keyboard users must be able to reach it. -->
	<!-- svelte-ignore a11y_no_noninteractive_tabindex -->
	<div class="list" tabindex="0" aria-label="Notes on this frame">
		{#if notes.length}
			<ol>
				{#each notes as note (note.id)}
					<li class:current={note.id === editing}>
						{#if note.anchor}
							<blockquote class="quote">
								<span class="visually-hidden">On the words: </span>{note.anchor.exact}
							</blockquote>
						{/if}
						<p class="text">{note.text}</p>
						<p class="meta">
							{when(note.updated)}
							{#if note.id === editing}· <strong>in the editor</strong>{/if}
							{#if note.review === 'flagged'}· <span class="flagged">flagged for agent review</span
								>{/if}
							{#if note.anchor && detached.includes(note.id)}· <span class="flagged"
									>detached: the reading no longer has these words</span
								>{/if}
						</p>
						{#if note.review === 'handled'}
							<p class="response"><span class="who">Agent:</span> {note.response}</p>
						{/if}
						<p class="actions">
							{#if note.anchor && !detached.includes(note.id)}
								<button type="button" onclick={() => onshow(note)}
									>Show in reading<span class="visually-hidden"
										>: {note.anchor.exact.slice(0, 40)}</span
									></button
								>
							{/if}
							<button type="button" onclick={(e) => onedit(note, e.currentTarget)}
								>Edit<span class="visually-hidden">: {note.text.slice(0, 40)}</span></button
							>
							<button type="button" onclick={() => ondelete(note)}
								>Delete<span class="visually-hidden">: {note.text.slice(0, 40)}</span></button
							>
						</p>
					</li>
				{/each}
			</ol>
		{:else}
			<p class="empty">
				No notes on this frame yet. Add one and the picture becomes the page you write on, or
				annotate some words of the narrative.
			</p>
		{/if}
	</div>
</div>

<style>
	.notes[hidden] {
		display: none;
	}
	.notes {
		display: grid;
		grid-template-rows: auto minmax(0, 1fr);
		min-height: 0;
		border-left: 1px solid color-mix(in srgb, var(--muted) 40%, transparent);
	}
	.controls {
		display: flex;
		flex-wrap: wrap;
		align-items: center;
		justify-content: space-between;
		gap: 0.5rem 1rem;
		padding: 0.75rem 1.5rem;
		border-bottom: 1px solid color-mix(in srgb, var(--muted) 40%, transparent);
	}
	h2 {
		margin: 0;
		font-family: var(--mono);
		font-size: 0.75rem;
		font-weight: normal;
		letter-spacing: 0.12em;
		text-transform: uppercase;
		color: var(--muted);
	}
	h2 span {
		color: var(--ink);
	}
	.list {
		overflow-y: auto;
		overscroll-behavior: contain;
		padding: 1rem 1.5rem 2rem;
	}
	ol {
		margin: 0;
		padding: 0;
		list-style: none;
	}
	li {
		padding: 0.75rem 0;
		border-bottom: 1px solid color-mix(in srgb, var(--muted) 30%, transparent);
	}
	li.current {
		border-left: 2px solid var(--accent);
		padding-left: 0.75rem;
	}
	.quote {
		margin: 0 0 0.4rem;
		padding-left: 0.6rem;
		border-left: 2px solid var(--accent);
		font: italic 0.85rem/1.45 var(--serif);
		color: var(--muted);
		display: -webkit-box;
		-webkit-box-orient: vertical;
		-webkit-line-clamp: 3;
		line-clamp: 3;
		overflow: hidden;
	}
	.text {
		margin: 0;
		font-family: var(--serif);
		line-height: 1.5;
		white-space: pre-wrap;
		overflow-wrap: anywhere;
	}
	.meta,
	.response {
		margin: 0.35rem 0 0;
		font-size: 0.75rem;
		color: var(--muted);
	}
	.flagged,
	.who {
		color: var(--accent);
	}
	.response {
		color: var(--ink);
		white-space: pre-wrap;
	}
	.actions {
		display: flex;
		gap: 0.5rem;
		margin: 0.5rem 0 0;
	}
	button {
		font: inherit;
		font-size: 0.8rem;
		padding: 0.2rem 0.7rem;
		color: var(--ink);
		background: none;
		border: 1px solid var(--muted);
		border-radius: 0.25rem;
		cursor: pointer;
	}
	.add {
		border-color: var(--accent);
	}
	.empty {
		margin: 0;
		color: var(--muted);
		font-size: 0.875rem;
	}
	kbd {
		font-family: var(--mono);
		font-size: 0.7rem;
		padding: 0 0.3rem;
		margin-left: 0.25rem;
		border: 1px solid var(--muted);
		border-radius: 0.2rem;
		color: var(--muted);
	}
</style>

<script lang="ts">
	import { onMount } from 'svelte';
	import { NOTE_MAX } from '../reader-data';

	interface Props {
		/** A new note, or an edit of one. */
		editing: boolean;
		/** The frame it is on: headline and accent. */
		title: string;
		text: string;
		/** The "Agent review" box. */
		flag: boolean;
		saving?: boolean;
		/** Why the last save failed, if it did. */
		error?: string;
		onsave: () => void;
		oncancel: () => void;
	}

	let {
		editing,
		title,
		text = $bindable(),
		flag = $bindable(),
		saving = false,
		error = '',
		onsave,
		oncancel
	}: Props = $props();

	const id = $props.id();
	let box = $state<HTMLTextAreaElement>();
	onMount(() => box?.focus());

	/**
	 * Esc cancels (the shell asks first if there are changes); Ctrl or Cmd
	 * with Enter saves. Handled here, before the shell's page-wide keys.
	 */
	function keydown(e: KeyboardEvent) {
		if (e.key === 'Escape') {
			e.preventDefault();
			oncancel();
		} else if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) {
			e.preventDefault();
			onsave();
		}
	}
</script>

<!-- The page's own keys stand down in here: data-own-keys. Esc and Ctrl+Enter
     are the form's own, heard from whichever of its controls has focus. -->
<!-- svelte-ignore a11y_no_noninteractive_element_interactions -->
<form
	class="note-editor"
	aria-labelledby="{id}-title"
	data-own-keys
	onkeydown={keydown}
	onsubmit={(e) => {
		e.preventDefault();
		onsave();
	}}
>
	<h2 id="{id}-title">{editing ? 'Editing a note' : 'New note'} <span>on {title}</span></h2>
	<label class="visually-hidden" for="{id}-text">Note</label>
	<textarea
		id="{id}-text"
		bind:value={text}
		bind:this={box}
		aria-describedby="{id}-keys"
		maxlength={NOTE_MAX}></textarea>
	<div class="row">
		<label class="flag">
			<input type="checkbox" bind:checked={flag} aria-describedby="{id}-flag" />
			Agent review
		</label>
		<span id="{id}-flag" class="hint">Flag it for an agent to look at later.</span>
	</div>
	<div class="row">
		<button type="submit" class="save" disabled={saving || !text.trim()}>
			{saving ? 'Saving…' : 'Save'}
		</button>
		<button type="button" onclick={oncancel}>Cancel</button>
		<span id="{id}-keys" class="hint"
			><kbd>Ctrl</kbd> <kbd>Enter</kbd> saves, <kbd>Esc</kbd> cancels</span
		>
	</div>
	<p class="error" role="status">{error}</p>
</form>

<style>
	.note-editor {
		align-self: stretch;
		display: grid;
		grid-template-rows: auto minmax(8rem, 1fr) auto auto auto;
		gap: 0.6rem;
		min-height: 0;
		padding: 1rem 0 0.5rem;
		user-select: text;
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
	textarea {
		font: 1rem/1.5 var(--serif);
		min-height: 0;
		padding: 0.75rem;
		resize: none;
		color: var(--ink);
		background: color-mix(in srgb, var(--background) 85%, var(--ink));
		border: 1px solid var(--muted);
		border-radius: 0.25rem;
	}
	.row {
		display: flex;
		flex-wrap: wrap;
		align-items: center;
		gap: 0.5rem 0.75rem;
		font-size: 0.875rem;
	}
	.flag {
		display: flex;
		align-items: center;
		gap: 0.35rem;
	}
	.hint {
		font-size: 0.75rem;
		color: var(--muted);
	}
	button {
		font: inherit;
		padding: 0.3rem 0.9rem;
		color: var(--ink);
		background: none;
		border: 1px solid var(--muted);
		border-radius: 0.25rem;
		cursor: pointer;
	}
	.save {
		border-color: var(--accent);
		font-weight: bold;
	}
	button:disabled {
		opacity: 0.5;
		cursor: default;
	}
	.error {
		margin: 0;
		min-height: 1em;
		font-size: 0.8rem;
		color: var(--accent);
	}
	kbd {
		font-family: var(--mono);
		font-size: 0.7rem;
		padding: 0 0.25rem;
		border: 1px solid var(--muted);
		border-radius: 0.2rem;
	}
</style>

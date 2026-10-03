<script lang="ts">
	import { tick } from 'svelte';
	import {
		SUGGESTION_STATUS_WORDS,
		SUGGESTION_TEXT_MAX,
		SUGGESTION_TITLE_MAX,
		type SuggestOffer,
		type Suggestion
	} from '../reader-data';

	interface Props {
		offer: SuggestOffer;
		/** Whether the panel it is in is open: the reader's list is loaded the first time it is. */
		active: boolean;
	}

	let { offer, active }: Props = $props();

	const id = $props.id();
	let open = $state(false);
	let title = $state('');
	let cover = $state('');
	let why = $state('');
	let sending = $state(false);
	let problem = $state('');
	let said = $state('');
	let mine = $state<Suggestion[] | null>(null);
	let loaded = false;
	let toggle = $state<HTMLButtonElement>();
	let titleField = $state<HTMLInputElement>();

	$effect(() => {
		if (!active || loaded) return;
		loaded = true;
		offer.list().then((l) => (mine = l));
	});

	async function show() {
		open = !open;
		said = '';
		if (open) {
			await tick();
			titleField?.focus();
		}
	}

	function cancel() {
		open = false;
		problem = '';
		toggle?.focus();
	}

	async function send(e: SubmitEvent) {
		e.preventDefault();
		if (sending) return;
		problem = '';
		sending = true;
		const got = await offer.send({ title, cover, why });
		sending = false;
		if ('error' in got) {
			problem = got.error;
			return;
		}
		mine = [got, ...(mine ?? [])];
		title = cover = why = '';
		open = false;
		said = `Sent: “${got.title}”. Thank you.`;
		await tick();
		toggle?.focus();
	}
</script>

<p class="group" id="{id}-heading">Suggest a subject</p>
<p>
	Is there a subject you would like kloom to have? Suggest it and Ken will read it. It is a note to
	him: nothing is written from it on its own.
</p>
<button
	type="button"
	class="toggle"
	aria-expanded={open}
	aria-controls="{id}-form"
	bind:this={toggle}
	onclick={show}>Suggest a subject…</button
>
<p class="said" role="status">{said}</p>
<form id="{id}-form" aria-labelledby="{id}-heading" hidden={!open} onsubmit={send}>
	<label for="{id}-title">Subject</label>
	<input
		id="{id}-title"
		type="text"
		required
		maxlength={SUGGESTION_TITLE_MAX}
		autocomplete="off"
		bind:value={title}
		bind:this={titleField}
	/>
	<label for="{id}-cover">What should it cover?</label>
	<textarea id="{id}-cover" rows="3" maxlength={SUGGESTION_TEXT_MAX} bind:value={cover}></textarea>
	<label for="{id}-why">Why you would like it <span class="optional">(optional)</span></label>
	<textarea id="{id}-why" rows="2" maxlength={SUGGESTION_TEXT_MAX} bind:value={why}></textarea>
	{#if problem}<p class="problem" role="alert">{problem}</p>{/if}
	<div class="actions">
		<button type="submit" disabled={sending}>{sending ? 'Sending…' : 'Send'}</button>
		<button type="button" onclick={cancel}>Cancel</button>
	</div>
</form>
{#if mine?.length}
	<p class="mine" id="{id}-mine">Your suggestions</p>
	<ul aria-labelledby="{id}-mine">
		{#each mine as s (s.id)}
			<li>
				<span class="what">{s.title}</span>
				<span class="status">{SUGGESTION_STATUS_WORDS[s.status]}</span>
			</li>
		{/each}
	</ul>
{/if}

<style>
	p {
		margin: 0 0 0.5rem;
	}
	.group {
		margin-top: 0.75rem;
		padding-top: 0.5rem;
		border-top: 1px solid color-mix(in srgb, var(--muted) 40%, transparent);
		font-family: var(--mono);
		font-size: 0.75rem;
		letter-spacing: 0.12em;
		text-transform: uppercase;
		color: var(--muted);
	}
	button {
		font: inherit;
		color: var(--ink);
		background: transparent;
		border: 1px solid var(--muted);
		border-radius: 0.2rem;
		padding: 0.2rem 0.6rem;
		cursor: pointer;
	}
	button:disabled {
		cursor: default;
		opacity: 0.6;
	}
	button:focus-visible,
	input:focus-visible,
	textarea:focus-visible {
		outline: 2px solid var(--accent);
		outline-offset: 2px;
	}
	.said:empty {
		display: none;
	}
	.said {
		margin-top: 0.4rem;
	}
	form {
		display: flex;
		flex-direction: column;
		gap: 0.2rem;
		margin: 0.5rem 0;
	}
	form[hidden] {
		display: none;
	}
	label {
		margin-top: 0.3rem;
		font-size: 0.8rem;
		color: var(--muted);
	}
	.optional {
		font-style: italic;
	}
	input,
	textarea {
		box-sizing: border-box;
		width: 100%;
		font: inherit;
		color: var(--ink);
		background: var(--background);
		border: 1px solid var(--muted);
		border-radius: 0.2rem;
		padding: 0.25rem 0.4rem;
	}
	textarea {
		resize: vertical;
	}
	.problem {
		margin: 0.3rem 0 0;
		color: var(--accent);
	}
	.actions {
		display: flex;
		gap: 0.5rem;
		margin-top: 0.5rem;
	}
	.mine {
		margin-top: 0.5rem;
		font-size: 0.8rem;
		color: var(--muted);
	}
	ul {
		margin: 0 0 0.5rem;
		padding: 0;
		list-style: none;
	}
	li {
		display: flex;
		justify-content: space-between;
		gap: 0.75rem;
		padding: 0.15rem 0;
		border-bottom: 1px solid color-mix(in srgb, var(--muted) 30%, transparent);
	}
	.what {
		overflow-wrap: anywhere;
	}
	.status {
		flex: none;
		font-size: 0.8rem;
		color: var(--muted);
	}
</style>

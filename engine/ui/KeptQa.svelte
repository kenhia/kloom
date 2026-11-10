<script lang="ts">
	import type { Kept, Share } from '../reader-data';
	import QaAnswer from './QaAnswer.svelte';

	interface Props {
		/** How many answers were kept on this frame. */
		count: number;
		/** How many citations the frame has: the answers' [n] are numbered against them. */
		citations: number;
		/** Fetch the answers; null when that failed. */
		load: () => Promise<Kept[] | null>;
		onforget: (id: string) => Promise<boolean>;
		/** Tick or untick "Share with other readers" (korg 3560): the answer after, or null. */
		onshare: (id: string, share: boolean) => Promise<Kept | null>;
		/** A frame's title if this subject has it, for "grown into". */
		titleOf: (frame: string) => string | null;
		ongoto: (frame: string) => void;
	}

	let { count, citations, load, onforget, onshare, titleOf, ongoto }: Props = $props();

	let items = $state<Kept[] | null>(null);
	let failed = $state(false);
	let said = $state('');

	/** Bodies arrive when the section is first opened; the page brings only the count. */
	async function toggle(e: Event) {
		if (!(e.currentTarget as HTMLDetailsElement).open || items) return;
		failed = false;
		const got = await load();
		if (got) items = got;
		else failed = true;
	}

	async function forget(k: Kept) {
		if (!confirm(`Remove the kept answer to “${k.answer.question}”?`)) return;
		if (await onforget(k.answer.id)) {
			items = items?.filter((x) => x.answer.id !== k.answer.id) ?? null;
			said = 'Kept answer removed.';
		} else said = 'Could not remove it.';
	}

	async function share(k: Kept, e: Event) {
		const box = e.currentTarget as HTMLInputElement;
		const after = await onshare(k.answer.id, box.checked);
		if (!after) {
			box.checked = !box.checked;
			said = 'Could not change it.';
			return;
		}
		items = items?.map((x) => (x.answer.id === k.answer.id ? after : x)) ?? null;
		said = SHARE_WORDS[after.share ?? 'none'] || 'Not shared.';
	}

	/** Where a share stands, in words; none says nothing. */
	const SHARE_WORDS: Record<Share, string> = {
		none: '',
		pending: 'Waiting for an agent to review it. Other readers see it once the review passes it.',
		shared: 'Shared: other readers see it under this frame.',
		declined: 'Not shared.'
	};

	const day = (iso: string) => new Date(iso).toLocaleDateString(undefined, { dateStyle: 'medium' });
</script>

<details class="qa" ontoggle={toggle}>
	<summary>Q&amp;A ({count})</summary>
	<p class="about">Answers you asked about this frame and kept.</p>
	{#if failed}
		<p class="about">Could not load them. Close this and open it again to retry.</p>
	{:else if !items}
		<p class="about">Loading…</p>
	{:else}
		{#each items as k (k.answer.id)}
			{@const state = k.share ?? 'none'}
			<QaAnswer answer={k.answer} {citations}>
				<p class="meta">
					Kept {day(k.answer.keptAt)} · {k.answer.model}
					{#if k.grown?.length}
						· Grown into
						{#each k.grown as f, i (f)}
							{@const t = titleOf(f)}
							{#if i > 0},{/if}
							{#if t}<button type="button" class="link" onclick={() => ongoto(f)}>{t}</button
								>{:else}{f}{/if}
						{/each}
					{/if}
					·
					<button type="button" class="link" onclick={() => forget(k)}
						>Remove<span class="visually-hidden">: {k.answer.question}</span></button
					>
				</p>
				<p class="share">
					<label>
						<input
							type="checkbox"
							checked={state === 'pending' || state === 'shared'}
							onchange={(e) => share(k, e)}
						/>
						Share with other readers<span class="visually-hidden">: {k.answer.question}</span>
					</label>
					{#if state !== 'none'}
						<span class="state">{SHARE_WORDS[state]}</span>
					{/if}
				</p>
				{#if k.shareResponse && (state === 'shared' || state === 'declined')}
					<p class="response"><span class="who">Agent review:</span> {k.shareResponse}</p>
				{/if}
			</QaAnswer>
		{/each}
	{/if}
	<p class="visually-hidden" role="status">{said}</p>
</details>

<style>
	.qa {
		margin-top: 1.75rem;
	}
	summary {
		cursor: pointer;
		width: fit-content;
		font-family: var(--mono);
		font-size: 0.75rem;
		letter-spacing: 0.12em;
		text-transform: uppercase;
		color: var(--muted);
	}
	.about {
		margin: 0.5rem 0;
		font-size: 0.8rem;
		color: var(--muted);
	}
	.meta,
	.share,
	.response {
		margin: 0.35rem 0 0;
		font-size: 0.75rem;
		color: var(--muted);
	}
	.share label {
		color: var(--ink);
		cursor: pointer;
	}
	.share input {
		accent-color: var(--accent);
	}
	.state {
		margin-left: 0.5rem;
	}
	.who {
		color: var(--ink);
	}
	.link {
		font: inherit;
		padding: 0;
		color: var(--ink);
		background: none;
		border: 0;
		text-decoration: underline;
		text-decoration-color: var(--accent);
		cursor: pointer;
	}
</style>

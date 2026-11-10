<script lang="ts">
	import type { SharedAnswer } from '../reader-data';
	import QaAnswer from './QaAnswer.svelte';

	interface Props {
		/** How many other readers' answers are shared on this frame. */
		count: number;
		/** How many citations the frame has: the answers' [n] are numbered against them. */
		citations: number;
		/** Fetch them; null when that failed. */
		load: () => Promise<SharedAnswer[] | null>;
	}

	let { count, citations, load }: Props = $props();

	let items = $state<SharedAnswer[] | null>(null);
	let failed = $state(false);

	/** Bodies arrive when the section is first opened; the page brings only the count. */
	async function toggle(e: Event) {
		if (!(e.currentTarget as HTMLDetailsElement).open || items) return;
		failed = false;
		const got = await load();
		if (got) items = got;
		else failed = true;
	}

	const day = (iso: string) => new Date(iso).toLocaleDateString(undefined, { dateStyle: 'medium' });
</script>

<!-- Other readers' kept answers, shared after an agent's review (§Shared answers, korg 3560). -->
<details class="qa" ontoggle={toggle}>
	<summary>Readers’ Q&amp;A ({count})</summary>
	<p class="about">
		Questions other readers asked about this frame, and the answers they shared. An agent reviewed
		each one before it was shown here.
	</p>
	{#if failed}
		<p class="about">Could not load them. Close this and open it again to retry.</p>
	{:else if !items}
		<p class="about">Loading…</p>
	{:else}
		{#each items as s (s.answer.id)}
			<QaAnswer answer={s.answer} {citations}>
				<p class="meta">Asked {day(s.answer.askedAt)} · {s.answer.model}</p>
			</QaAnswer>
		{/each}
	{/if}
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
	.about,
	.meta {
		margin: 0.5rem 0;
		font-size: 0.8rem;
		color: var(--muted);
	}
	.meta {
		margin: 0.35rem 0 0;
		font-size: 0.75rem;
	}
</style>

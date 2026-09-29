<script lang="ts">
	import { keptReferences } from '../ai/kept';
	import { chicago } from '../citation';
	import { renderMarkdown } from '../markdown';
	import type { Kept } from '../reader-data';

	interface Props {
		/** How many answers were kept on this frame. */
		count: number;
		/** How many citations the frame has: the answers' [n] are numbered against them. */
		citations: number;
		/** Fetch the answers; null when that failed. */
		load: () => Promise<Kept[] | null>;
		onforget: (id: string) => Promise<boolean>;
		/** A frame's title if this subject has it, for "grown into". */
		titleOf: (frame: string) => string | null;
		ongoto: (frame: string) => void;
	}

	let { count, citations, load, onforget, titleOf, ongoto }: Props = $props();

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
			{@const refs = keptReferences(k.answer, citations)}
			<article class="kept">
				<p class="question"><span class="q" aria-hidden="true">Q</span> {k.answer.question}</p>
				<div class="answer">
					<!-- A model's answer, rendered with raw HTML escaped, unsafe links dropped and no images. -->
					<!-- eslint-disable-next-line svelte/no-at-html-tags -->
					{@html renderMarkdown(k.answer.answer, { image: () => null })}
				</div>
				{#if refs.length}
					<ol class="refs" aria-label="Sources it drew on">
						{#each refs as r, i (i)}
							<li value={r.n ?? undefined} class:unnumbered={r.n === null}>
								{#each chicago(r.citation) as part, j (j)}
									{#if part.href}
										<!-- An external source, not an app route. -->
										<!-- eslint-disable-next-line svelte/no-navigation-without-resolve -->
										<a href={part.href} rel="noopener noreferrer">{part.text}</a>
									{:else if part.italic}<i>{part.text}</i>{:else}{part.text}{/if}
								{/each}
							</li>
						{/each}
					</ol>
				{/if}
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
			</article>
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
	.kept {
		margin: 1rem 0;
		padding-left: 0.75rem;
		border-left: 2px solid var(--accent);
	}
	.question {
		margin: 0;
		font-family: var(--serif);
		font-size: 1.1rem;
	}
	.q {
		font-family: var(--mono);
		font-size: 0.75rem;
		color: var(--accent);
	}
	.answer {
		font-size: 0.95rem;
	}
	.answer :global(a),
	.refs a {
		color: inherit;
		text-decoration-color: var(--accent);
	}
	.refs {
		margin: 0.25rem 0;
		padding-left: 1.75rem;
		font-size: 0.8rem;
		overflow-wrap: anywhere;
	}
	.refs li.unnumbered {
		list-style: disc;
	}
	.meta {
		margin: 0.35rem 0 0;
		font-size: 0.75rem;
		color: var(--muted);
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

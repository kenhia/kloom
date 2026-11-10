<script lang="ts">
	import type { Snippet } from 'svelte';
	import { keptReferences, type KeptAnswer } from '../ai/kept';
	import { chicago } from '../citation';
	import { renderMarkdown } from '../markdown';

	interface Props {
		answer: KeptAnswer;
		/** How many citations the frame has: the answer's [n] are numbered against them. */
		citations: number;
		/** What goes under it: when it was kept, what became of it. */
		children: Snippet;
	}

	let { answer, citations, children }: Props = $props();

	const refs = $derived(keptReferences(answer, citations));
</script>

<!-- One kept or shared answer (§Kept answers, §Shared answers): its question, the answer, its sources. -->
<article class="kept">
	<p class="question"><span class="q" aria-hidden="true">Q</span> {answer.question}</p>
	<div class="answer">
		<!-- A model's answer, rendered with raw HTML escaped, unsafe links dropped and no images. -->
		<!-- eslint-disable-next-line svelte/no-at-html-tags -->
		{@html renderMarkdown(answer.answer, { image: () => null })}
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
	{@render children()}
</article>

<style>
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
</style>

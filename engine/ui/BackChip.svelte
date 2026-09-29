<script lang="ts">
	import type { BackStop } from '../navigation';

	/**
	 * "↩ Back to <frame> · <subject>" (docs/design.md §Connections): shown in
	 * the spine's HUD after a jump, it goes back one history entry, as the
	 * browser's Back does, so the two always agree. Jumps stack; the chip
	 * names the latest and says how many more wait under it.
	 */
	interface Props {
		to: BackStop;
		/** How many jumps are stacked, this one included. */
		depth: number;
		/** The reader's back key, or null when it is off. */
		key: string | null;
		onback: () => void;
	}

	let { to, depth, key, onback }: Props = $props();

	const said = $derived(
		`Back to ${to.title}, ${to.subjectTitle}${depth > 1 ? `, and ${depth - 1} more before it` : ''}`
	);
</script>

<button
	type="button"
	class="back"
	title="{said}{key ? ` (${key})` : ''}"
	aria-label={said}
	onclick={onback}
>
	<span class="lead" aria-hidden="true">↩ Back</span>
	<span class="words" aria-hidden="true">to {to.title} · {to.subjectTitle}</span>
	{#if depth > 1}<span class="more" aria-hidden="true">+{depth - 1}</span>{/if}
	{#if key}<kbd aria-hidden="true">{key}</kbd>{/if}
</button>

<style>
	.back {
		display: flex;
		flex: none;
		align-items: center;
		gap: 0.35rem;
		max-width: min(18rem, 28vw);
		min-width: 0;
		padding: 0.2rem 0.6rem;
		font: inherit;
		letter-spacing: 0.04em;
		text-transform: none;
		color: var(--ink);
		background: color-mix(in srgb, var(--accent) 14%, transparent);
		border: 1px solid var(--accent);
		border-radius: 1rem;
		cursor: pointer;
	}
	.lead {
		white-space: nowrap;
	}
	.words {
		overflow: hidden;
		white-space: nowrap;
		text-overflow: ellipsis;
	}
	.more {
		color: var(--accent);
	}
	/* On a phone the chip says only "↩ Back"; its name still says where to. */
	@media (max-width: 760px) {
		.words {
			display: none;
		}
	}
	kbd {
		font-family: var(--mono);
		font-size: 0.7rem;
		padding: 0 0.25rem;
		border: 1px solid var(--muted);
		border-radius: 0.2rem;
		color: var(--muted);
	}
</style>

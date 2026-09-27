<script lang="ts">
	// Escape anywhere in this pane returns to the spine; the shell handles it.

	let question = $state('');
	let status = $state('');

	function submit(e: SubmitEvent) {
		e.preventDefault();
		if (!question.trim()) return;
		// No backend yet: ask and grow arrive behind the provider interface.
		status = 'The AI pane is not connected yet — asking and growing come in a later build.';
	}

	function keydown(e: KeyboardEvent) {
		if (e.key === 'Enter' && !e.shiftKey) {
			e.preventDefault();
			(e.currentTarget as HTMLTextAreaElement).form?.requestSubmit();
		}
	}
</script>

<section class="ai" aria-labelledby="ai-title">
	<h2 id="ai-title" class="title">Ask</h2>
	<form onsubmit={submit}>
		<label for="ai-input" class="visually-hidden">Ask a question about this subject</label>
		<textarea
			id="ai-input"
			rows="1"
			placeholder="Ask about what you are reading…"
			aria-describedby="ai-hint"
			bind:value={question}
			onkeydown={keydown}></textarea>
		<button type="submit">Send</button>
	</form>
	<p class="status" role="status">{status}</p>
	<p id="ai-hint" class="hint">
		<kbd>←</kbd><kbd>→</kbd> spine · <kbd>↑</kbd><kbd>↓</kbd> narrative · <kbd>S</kbd> sync ·
		<kbd>Tab</kbd> into and out of Ask · <kbd>Esc</kbd> back to the spine
	</p>
</section>

<style>
	.ai {
		display: grid;
		grid-template-columns: auto 1fr;
		align-items: center;
		gap: 0.25rem 1rem;
		padding: 0.75rem 1.5rem;
		border-top: 1px solid color-mix(in srgb, var(--muted) 40%, transparent);
	}
	.title {
		margin: 0;
		font-family: var(--mono);
		font-size: 0.75rem;
		font-weight: normal;
		letter-spacing: 0.12em;
		text-transform: uppercase;
		color: var(--muted);
	}
	form {
		display: flex;
		gap: 0.5rem;
	}
	textarea {
		flex: 1;
		font: inherit;
		resize: vertical;
		min-height: 2.25rem;
		padding: 0.4rem 0.6rem;
		color: var(--ink);
		background: color-mix(in srgb, var(--ink) 6%, transparent);
		border: 1px solid var(--muted);
		border-radius: 0.25rem;
	}
	button {
		font: inherit;
		padding: 0 1rem;
		color: var(--background);
		background: var(--accent);
		border: 0;
		border-radius: 0.25rem;
		cursor: pointer;
	}
	.status,
	.hint {
		grid-column: 2;
		margin: 0;
		font-size: 0.8rem;
		color: var(--muted);
	}
	.status:empty {
		display: none;
	}
	kbd {
		font-family: var(--mono);
		font-size: 0.7rem;
		padding: 0 0.25rem;
		margin-right: 0.1rem;
		border: 1px solid var(--muted);
		border-radius: 0.2rem;
	}
	@media (max-width: 760px) {
		.ai {
			grid-template-columns: 1fr;
		}
		.status,
		.hint {
			grid-column: 1;
		}
	}
</style>

<script lang="ts">
	// Escape anywhere in this pane returns to the spine; the shell handles it.
	import { readAskStream } from '../ai/client';
	import { renderMarkdown } from '../markdown';
	import type { Frame, Trail } from '../model';
	import { ASK_MODEL } from '../settings';
	import type { UserSettings } from '../user-settings.svelte';

	interface Props {
		/**
		 * The frame in the reading pane: what a question is asked about. In manual
		 * sync it can differ from the spine's; the reader is asking about what they read.
		 */
		frame: Frame;
		trail: Trail | null;
		settings: UserSettings;
	}

	let { frame, trail, settings }: Props = $props();

	type Phase = 'asking' | 'queued' | 'answering' | 'done' | 'stopped' | 'failed';

	/**
	 * One question and its answer. It keeps the frame it was asked about, so
	 * moving the spine while it runs neither stops it nor changes its subject.
	 */
	interface Turn {
		id: string | null;
		question: string;
		about: string;
		model: string;
		text: string;
		phase: Phase;
		kept: 'no' | 'keeping' | 'kept';
	}

	let question = $state('');
	let turn = $state<Turn | null>(null);
	let status = $state('');
	let controller: AbortController | null = null;

	const running = $derived(
		turn?.phase === 'asking' || turn?.phase === 'queued' || turn?.phase === 'answering'
	);
	// A model's answer shows no images: an image would be a request to anywhere.
	const answerHtml = $derived(turn?.text ? renderMarkdown(turn.text, { image: () => null }) : '');

	/** The trail, if the reader is on one and it holds this frame. */
	const trailOf = (id: string) =>
		trail?.spine.segments.some((s) => s.frames.includes(id)) ? trail.id : null;

	function modelLabel(id: string) {
		const setting = settings.list.find((s) => s.id === ASK_MODEL);
		return setting?.choices.find((c) => c.value === id)?.label ?? id;
	}

	async function ask(q: string) {
		controller?.abort();
		const abort = (controller = new AbortController());
		const model = settings.get(ASK_MODEL) ?? '';
		turn = {
			id: null,
			question: q,
			about: `${frame.scene.headline} ${frame.scene.accent}`,
			model: modelLabel(model),
			text: '',
			phase: 'asking',
			kept: 'no'
		};
		// The reactive proxy; a later question replaces `turn` and this one goes quiet.
		const mine = turn;
		const live = () => turn === mine && !abort.signal.aborted;
		status = `Asking ${mine.model}…`;
		const fail = (message: string) => {
			if (!live()) return;
			mine.phase = 'failed';
			status = message;
		};
		try {
			const res = await fetch('/api/ask', {
				method: 'POST',
				headers: { 'content-type': 'application/json' },
				body: JSON.stringify({ frame: frame.id, trail: trailOf(frame.id), question: q, model }),
				signal: abort.signal
			});
			if (!res.ok || !res.body) {
				const body = await res.json().catch(() => null);
				return fail(body?.message ?? `Asking failed (${res.status}).`);
			}
			await readAskStream(res.body, (e) => {
				if (!live()) return;
				if (e.type === 'start') mine.id = e.id;
				else if (e.type === 'queued') {
					mine.phase = 'queued';
					status = 'Waiting for another question to finish…';
				} else if (e.type === 'text') {
					if (mine.phase !== 'answering') status = `${mine.model} is answering…`;
					mine.phase = 'answering';
					mine.text += e.text;
				} else if (e.type === 'done') {
					mine.phase = 'done';
					status = 'Answer ready.';
				} else if (e.type === 'error') fail(e.message);
			});
			if (['asking', 'queued', 'answering'].includes(mine.phase)) fail('The answer was cut off.');
		} catch (e) {
			fail(`Asking failed: ${(e as Error).message}`);
		}
	}

	function submit(e: SubmitEvent) {
		e.preventDefault();
		if (running) return stop();
		const q = question.trim();
		if (!q) return;
		question = '';
		ask(q);
	}

	function stop() {
		controller?.abort();
		if (turn && running) turn.phase = 'stopped';
		status = 'Stopped.';
	}

	async function keepThis() {
		if (!turn?.id || turn.phase !== 'done' || turn.kept !== 'no') return;
		const t = turn;
		t.kept = 'keeping';
		try {
			const res = await fetch('/api/keep', {
				method: 'POST',
				headers: { 'content-type': 'application/json' },
				body: JSON.stringify({ id: t.id })
			});
			const body = await res.json().catch(() => null);
			if (!res.ok) throw new Error(body?.message ?? `status ${res.status}`);
			t.kept = 'kept';
			status = 'Kept. Grow can turn it into content.';
		} catch (e) {
			t.kept = 'no';
			status = `Could not keep it: ${(e as Error).message}`;
		}
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
		<label for="ai-input" class="visually-hidden">Ask a question about this frame</label>
		<textarea
			id="ai-input"
			rows="1"
			placeholder="Ask about what you are reading…"
			aria-describedby="ai-hint"
			maxlength="2000"
			bind:value={question}
			onkeydown={keydown}></textarea>
		<button type="submit">{running ? 'Stop' : 'Send'}</button>
	</form>

	{#if turn}
		<!-- Focusable because it scrolls; once focused the arrows scroll it, so the page's keys stand down. -->
		<!-- svelte-ignore a11y_no_noninteractive_tabindex -->
		<article
			class="answer"
			tabindex="0"
			aria-labelledby="ai-answer-title"
			aria-busy={running}
			data-own-keys
		>
			<h3 id="ai-answer-title" class="about">
				<span class="visually-hidden">Answer about</span>
				<span aria-hidden="true">About</span>
				{turn.about} · {turn.model}
			</h3>
			<p class="question">{turn.question}</p>
			{#if answerHtml}
				<!-- Rendered by renderMarkdown: raw HTML escaped, unsafe links dropped, no images. -->
				<!-- eslint-disable-next-line svelte/no-at-html-tags -->
				<div class="text">{@html answerHtml}</div>
			{/if}
		</article>
		{#if turn.phase === 'done'}
			<div class="actions">
				<button type="button" onclick={keepThis} disabled={turn.kept !== 'no'}>
					{turn.kept === 'kept' ? 'Kept' : turn.kept === 'keeping' ? 'Keeping…' : 'Keep this'}
				</button>
				<span class="note">Answers are not saved unless you keep them.</span>
			</div>
		{/if}
	{/if}

	<p class="status" role="status">{status}</p>
	<p id="ai-hint" class="hint">
		<kbd>←</kbd><kbd>→</kbd> spine · <kbd>↑</kbd><kbd>↓</kbd> narrative · <kbd>S</kbd> sync and
		<kbd>T</kbd> trail, in the spine or narrative · <kbd>Tab</kbd> into and out of Ask ·
		<kbd>Esc</kbd> back to the spine
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
	button:disabled {
		cursor: default;
		opacity: 0.6;
	}
	.answer,
	.actions,
	.status,
	.hint {
		grid-column: 2;
		margin: 0;
	}
	.answer {
		max-height: 35vh;
		overflow-y: auto;
		padding: 0.5rem 0.75rem;
		border-left: 2px solid var(--accent);
		background: color-mix(in srgb, var(--ink) 4%, transparent);
	}
	.about {
		margin: 0;
		font-family: var(--mono);
		font-size: 0.7rem;
		font-weight: normal;
		letter-spacing: 0.06em;
		color: var(--muted);
	}
	.question {
		margin: 0.25rem 0 0;
		font-style: italic;
	}
	.text :global(p),
	.text :global(ul),
	.text :global(ol) {
		margin: 0.5rem 0 0;
	}
	.text :global(a) {
		color: var(--accent);
	}
	.actions {
		display: flex;
		align-items: center;
		gap: 0.75rem;
	}
	.actions button {
		padding: 0.25rem 0.75rem;
	}
	.note,
	.status,
	.hint {
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
		.answer,
		.actions,
		.status,
		.hint {
			grid-column: 1;
		}
	}
</style>

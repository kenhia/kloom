<script lang="ts">
	// Escape anywhere in this pane returns to the spine; the shell handles it.
	import { onMount } from 'svelte';
	import { readAskStream } from '../ai/client';
	import type { GrowJob, GrowVerb } from '../ai/grow';
	import type { AiOffer } from '../ai/provider';
	import { renderMarkdown } from '../markdown';
	import type { Frame, Trail } from '../model';
	import { ASK_MODEL, GROW_MODEL } from '../settings';
	import type { UserSettings } from '../user-settings.svelte';

	interface Props {
		/** The subject's id: every API call names it. */
		subject: string;
		/**
		 * The frame in the reading pane: what a question is asked about. When the
		 * reader has turned following off it can differ from the spine's; they are
		 * asking about what they read.
		 */
		frame: Frame;
		trail: Trail | null;
		settings: UserSettings;
		offer: AiOffer;
		/** The main spine's frame ids: a trail may only branch from one of these. */
		mainFrames?: string[];
		/** A frame's title (headline and accent), for the grow job list. */
		titleOf?: (id: string) => string;
		/** A grow job finished and committed: the page reloads the subject. */
		ongrown?: () => void;
	}

	let {
		subject,
		frame,
		trail,
		settings,
		offer,
		mainFrames = [],
		titleOf = (id) => id,
		ongrown
	}: Props = $props();

	type Phase = 'asking' | 'queued' | 'answering' | 'done' | 'stopped' | 'failed';

	/**
	 * One question and its answer. It keeps the frame it was asked about, so
	 * moving the spine while it runs neither stops it nor changes its subject.
	 */
	interface Turn {
		id: string | null;
		/** The frame it was asked about. */
		frame: string;
		question: string;
		about: string;
		model: string;
		text: string;
		phase: Phase;
		kept: 'no' | 'keeping' | 'kept';
		web: boolean;
	}

	let question = $state('');
	// "Include web": shown unless the app denies it, checked when it allows it.
	let includeWeb = $derived(offer.web === 'allow');
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

	function modelLabel(id: string, setting = ASK_MODEL) {
		const s = settings.list.find((x) => x.id === setting);
		return s?.choices.find((c) => c.value === id)?.label ?? id;
	}

	async function ask(q: string) {
		controller?.abort();
		const abort = (controller = new AbortController());
		const model = settings.get(ASK_MODEL) ?? '';
		const web = offer.web !== 'deny' && includeWeb;
		turn = {
			id: null,
			frame: frame.id,
			question: q,
			about: `${frame.scene.headline} ${frame.scene.accent}`,
			model: modelLabel(model),
			text: '',
			phase: 'asking',
			kept: 'no',
			web
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
				body: JSON.stringify({
					subject,
					frame: frame.id,
					trail: trailOf(frame.id),
					question: q,
					model,
					web
				}),
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
				} else if (e.type === 'status') {
					// Anything before a search was the model thinking aloud.
					mine.text = '';
					status = `${mine.model} is searching the web…`;
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
				body: JSON.stringify({ subject, id: t.id })
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

	// --- Grow: queue a job, then follow it until it lands or fails. ---

	const VERBS: { value: GrowVerb; label: string; placeholder: string }[] = [
		{
			value: 'frames',
			label: 'New frames on the main spine',
			placeholder: 'What the main story should add…'
		},
		{
			value: 'trail',
			label: 'A side trail from this frame',
			placeholder: 'What the side trail should follow…'
		},
		{
			value: 'both',
			label: 'A new frame with its own trail',
			placeholder: 'A new frame, and the trail it opens…'
		}
	];
	const LIVE = ['queued', 'running', 'applying'];

	let verb = $state<GrowVerb>('frames');
	let growText = $state('');
	/** A kept answer the next job turns into content. */
	let growKept = $state<{ id: string; frame: string; about: string } | null>(null);
	let growing = $state(false);
	let jobs = $state<GrowJob[]>([]);
	let growInput = $state<HTMLInputElement>();
	let poll: ReturnType<typeof setTimeout> | undefined;

	/** The frame a job would grow from: the kept answer's, or the one being read. */
	const growAnchor = $derived(growKept?.frame ?? frame.id);
	const anchorOnMain = $derived(mainFrames.includes(growAnchor));
	const placeholder = $derived(VERBS.find((v) => v.value === verb)!.placeholder);

	$effect(() => {
		if (verb === 'trail' && !anchorOnMain) verb = 'frames';
	});

	onMount(() => {
		if (offer.grow) refreshJobs(true);
		return () => clearTimeout(poll);
	});

	function jobText(job: GrowJob) {
		switch (job.status) {
			case 'queued':
				return 'waiting';
			case 'running':
				return job.progress ?? 'starting';
			case 'applying':
				return 'committing';
			case 'done':
				return `added ${job.result?.frames.map(titleOf).join(', ')}${job.result?.pushError ? ' (committed, not yet pushed)' : ''}`;
			case 'failed':
				return `failed: ${job.error}`;
		}
	}

	/** Fetch the job list; announce what finished since last time, and keep polling while any runs. */
	async function refreshJobs(first = false) {
		clearTimeout(poll);
		let next: GrowJob[];
		try {
			const res = await fetch(`/api/grow?subject=${encodeURIComponent(subject)}`);
			if (!res.ok) throw new Error(`status ${res.status}`);
			next = (await res.json()).jobs;
		} catch {
			poll = setTimeout(refreshJobs, 10_000);
			return;
		}
		if (!first) {
			const was = new Map(jobs.map((j) => [j.id, j.status]));
			for (const j of next) {
				if (!LIVE.includes(was.get(j.id) ?? 'done')) continue;
				if (j.status === 'done') {
					status = `Grow ${jobText(j)}.`;
					ongrown?.();
				} else if (j.status === 'failed') status = `Grow ${jobText(j)}`;
			}
		}
		jobs = next;
		if (jobs.some((j) => LIVE.includes(j.status))) poll = setTimeout(refreshJobs, 3000);
	}

	async function queueGrow(e: SubmitEvent) {
		e.preventDefault();
		const request = growText.trim();
		if (growing || (!request && !growKept)) return;
		growing = true;
		try {
			const res = await fetch('/api/grow', {
				method: 'POST',
				headers: { 'content-type': 'application/json' },
				body: JSON.stringify({
					subject,
					verb,
					frame: frame.id,
					request,
					kept: growKept?.id ?? null,
					model: settings.get(GROW_MODEL)
				})
			});
			const body = await res.json().catch(() => null);
			if (!res.ok) throw new Error(body?.message ?? `status ${res.status}`);
			const job = body.job as GrowJob;
			status = `Grow queued: ${VERBS.find((v) => v.value === job.verb)!.label.toLowerCase()}, on ${modelLabel(job.model, GROW_MODEL)}.`;
			growText = '';
			growKept = null;
			jobs = [job, ...jobs.filter((j) => j.id !== job.id)];
			refreshJobs();
		} catch (err) {
			status = `Could not queue it: ${(err as Error).message}`;
		} finally {
			growing = false;
		}
	}

	/** After "Keep this": grow the kept answer into content, as a trail from its frame if it can be. */
	function growFrom() {
		if (!turn?.id || turn.kept !== 'kept') return;
		growKept = { id: turn.id, frame: turn.frame, about: turn.about };
		verb = mainFrames.includes(turn.frame) ? 'trail' : 'frames';
		growInput?.focus();
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
		{#if offer.web !== 'deny'}
			<label class="web">
				<input type="checkbox" bind:checked={includeWeb} />
				Include web
			</label>
		{/if}
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
				{turn.about} · {turn.model}{turn.web ? ' · web' : ''}
			</h3>
			{#if turn.frame !== frame.id}
				<p class="moved">You have moved on; this answer stays with the frame it was asked about.</p>
			{/if}
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
				{#if offer.grow && turn.kept === 'kept'}
					<button type="button" onclick={growFrom}>Grow from this</button>
				{/if}
				<span class="note">Answers are not saved unless you keep them.</span>
			</div>
		{/if}
	{/if}

	{#if offer.grow}
		<h3 id="grow-title" class="title grow-title">Grow</h3>
		<form class="grow" onsubmit={queueGrow} aria-labelledby="grow-title">
			<label for="grow-verb" class="visually-hidden">What to grow</label>
			<select id="grow-verb" bind:value={verb}>
				{#each VERBS as v (v.value)}
					<option value={v.value} disabled={v.value === 'trail' && !anchorOnMain}>{v.label}</option>
				{/each}
			</select>
			<label for="grow-input" class="visually-hidden">What grow should write</label>
			<input
				id="grow-input"
				type="text"
				maxlength="2000"
				{placeholder}
				bind:value={growText}
				bind:this={growInput}
			/>
			<button type="submit" disabled={growing}>Queue</button>
		</form>
		{#if growKept}
			<p class="kept-chip">
				From your kept answer about {growKept.about}
				<button type="button" class="link" onclick={() => (growKept = null)}>Don’t use it</button>
			</p>
		{/if}
		{#if jobs.length}
			<ul class="jobs" aria-label="Grow jobs">
				{#each jobs as job (job.id)}
					<li class={job.status}>
						<span class="what">
							{VERBS.find((v) => v.value === job.verb)?.label} · from {titleOf(job.anchor)} ·
							{modelLabel(job.model, GROW_MODEL)}
						</span>
						<span class="state">{jobText(job)}</span>
						{#if job.problems?.length}
							<details>
								<summary>What the validator found</summary>
								<ul>
									{#each job.problems as p, i (i)}<li>{p}</li>{/each}
								</ul>
							</details>
						{/if}
					</li>
				{/each}
			</ul>
		{/if}
	{/if}

	<p class="status" role="status">{status}</p>
	<p id="ai-hint" class="hint">
		<kbd>←</kbd><kbd>→</kbd> spine · <kbd>↑</kbd><kbd>↓</kbd> narrative · <kbd>S</kbd> sync,
		<kbd>T</kbd> trail and <kbd>B</kbd> bookmark, in the spine or narrative · <kbd>Tab</kbd> into
		and out of Ask ·
		<kbd>Esc</kbd> back to the spine
	</p>
</section>

<style>
	.ai {
		display: grid;
		grid-template-columns: auto minmax(0, 1fr);
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
	.web {
		display: flex;
		align-items: center;
		gap: 0.3rem;
		font-size: 0.8rem;
		color: var(--muted);
		white-space: nowrap;
	}
	button:disabled {
		cursor: default;
		opacity: 0.6;
	}
	.answer,
	.actions,
	.status,
	.hint,
	.kept-chip,
	.jobs {
		grid-column: 2;
		margin: 0;
	}
	.grow-title {
		grid-column: 1;
	}
	.grow input,
	.grow select {
		font: inherit;
		font-size: 0.85rem;
		padding: 0.3rem 0.5rem;
		color: var(--ink);
		background: color-mix(in srgb, var(--ink) 6%, transparent);
		border: 1px solid var(--muted);
		border-radius: 0.25rem;
	}
	.grow input {
		flex: 1;
		min-width: 8rem;
	}
	.grow select {
		max-width: 100%;
	}
	.grow {
		flex-wrap: wrap;
	}
	.kept-chip {
		font-size: 0.8rem;
		color: var(--muted);
	}
	.link {
		padding: 0;
		color: var(--accent);
		background: none;
		text-decoration: underline;
	}
	.jobs {
		list-style: none;
		padding: 0;
		font-size: 0.8rem;
	}
	.jobs > li {
		display: flex;
		flex-wrap: wrap;
		gap: 0 0.75rem;
		padding: 0.15rem 0;
	}
	.jobs .what {
		color: var(--muted);
	}
	.jobs .failed .state {
		color: var(--accent);
	}
	.jobs details {
		flex-basis: 100%;
		font-family: var(--mono);
		font-size: 0.7rem;
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
	.moved {
		margin: 0.25rem 0 0;
		font-size: 0.75rem;
		color: var(--muted);
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
			grid-template-columns: minmax(0, 1fr);
		}
		.answer,
		.actions,
		.status,
		.hint,
		.kept-chip,
		.jobs,
		.grow-title {
			grid-column: 1;
		}
	}
</style>

<script lang="ts">
	// Escape anywhere in this pane returns to the spine; the shell handles it.
	import { onMount, untrack } from 'svelte';
	import { readAskStream } from '../ai/client';
	import { aiVerbs, isGrow, type AiVerb } from '../ai/control';
	import type { GrowJob } from '../ai/grow';
	import type { AiOffer, AskBudget } from '../ai/provider';
	import { renderMarkdown } from '../markdown';
	import type { FrameHead, Trail } from '../model';
	import { ASK_MODEL, GROW_MODEL, type Layout } from '../settings';
	import type { UserSettings } from '../user-settings.svelte';

	interface Props {
		/** The subject's id: every API call names it. */
		subject: string;
		/**
		 * The frame in the reading pane: what a question is asked about. When the
		 * reader has turned following off it can differ from the spine's; they are
		 * asking about what they read.
		 */
		frame: FrameHead;
		trail: Trail | null;
		settings: UserSettings;
		offer: AiOffer;
		/** The main spine's frame ids: a trail may only branch from one of these. */
		mainFrames?: string[];
		/** A frame's title (headline and accent), for the grow job list. */
		titleOf?: (id: string) => string;
		/** A grow job finished and committed: the page reloads the subject. */
		ongrown?: () => void;
		/** Where the shell puts this pane (§Layout); it decides how the results scroll. */
		layout?: Layout;
		/** False while the results are out of sight: the tabs layout, on the Narrative tab. */
		showResults?: boolean;
		/** Bring the results into sight (the tabs layout: the AI tab). */
		onshow?: () => void;
		/**
		 * A question or a grow request was sent (korg 3568): the tabs layout
		 * brings the AI tab forward. Stop is not a send.
		 */
		onsend?: () => void;
		/** What the tab can say about the pane changed: working, or a result not yet seen. */
		onactivity?: (activity: 'idle' | 'working' | 'ready') => void;
		/** An answer was kept, on this frame: its Q&A and spine mark count it. */
		onkept?: (frame: string) => void;
	}

	let {
		subject,
		frame,
		trail,
		settings,
		offer,
		mainFrames = [],
		titleOf = (id) => id,
		ongrown,
		layout = 'strip',
		showResults = true,
		onshow,
		onsend,
		onactivity,
		onkept
	}: Props = $props();

	type Phase = 'asking' | 'queued' | 'answering' | 'done' | 'stopped' | 'failed' | 'resting';

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

	/** The one text box: a question, or what grow should write. */
	let text = $state('');
	// "Include web": shown unless the app denies it, checked when it allows it.
	let includeWeb = $derived(offer.web === 'allow');
	let turn = $state<Turn | null>(null);
	let status = $state('');
	/**
	 * A capped reader's month (the reader site, korg 3530): near the cap a
	 * gentle notice, at it ask rests until the first of next month. Never an
	 * error; the page's offer brings it, and each answer updates it.
	 */
	let budget = $state<AskBudget | undefined>(untrack(() => offer.budget));
	const resting = $derived(budget?.state === 'resting');
	const restDate = $derived(
		budget
			? new Date(`${budget.until}T12:00:00Z`).toLocaleDateString(undefined, {
					day: 'numeric',
					month: 'long',
					timeZone: 'UTC'
				})
			: ''
	);
	const budgetNote = $derived(
		budget?.state === 'resting'
			? `Ask is resting until ${restDate}: this month’s questions are used up.`
			: budget?.state === 'near'
				? `Ask is nearly at this month’s limit; it rests from then until ${restDate}.`
				: ''
	);
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
					// Anything before a search, or a fallback, was not the answer.
					mine.text = '';
					status =
						e.status === 'retrying'
							? `${mine.model} is answering again…`
							: `${mine.model} is searching the web…`;
				} else if (e.type === 'budget') {
					budget = e.budget;
					if (e.budget.state === 'resting' && mine.phase === 'asking') {
						// Nothing was asked: the question goes back in the box for next month.
						mine.phase = 'resting';
						turn = null;
						text ||= mine.question;
						status = budgetNote;
					}
				} else if (e.type === 'text') {
					if (mine.phase !== 'answering') status = `${mine.model} is answering…`;
					mine.phase = 'answering';
					mine.text += e.text;
				} else if (e.type === 'done') {
					mine.phase = 'done';
					status = showResults ? 'Answer ready.' : 'Answer ready, on the AI tab.';
					if (!showResults) unseen = true;
				} else if (e.type === 'error') fail(e.message);
			});
			if (['asking', 'queued', 'answering'].includes(mine.phase)) fail('The answer was cut off.');
			if (mine.phase === 'done' && budget?.state === 'near') status = `Answer ready. ${budgetNote}`;
		} catch (e) {
			fail(`Asking failed: ${(e as Error).message}`);
		}
	}

	function submit(e: SubmitEvent) {
		e.preventDefault();
		if (isGrow(verb)) {
			if (!growing && (text.trim() || growKept)) onsend?.();
			return queueGrow();
		}
		if (running) return stop();
		const q = text.trim();
		if (!q || resting) return;
		text = '';
		onsend?.();
		ask(q);
	}

	/** Put focus in the text box (Q, korg 3568). The tab showing stays as it is. */
	export function focusInput() {
		input?.focus();
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
			onkept?.(t.frame);
			status = offer.grow
				? 'Kept, in the frame’s Q&A. Grow can turn it into content.'
				: 'Kept, in the frame’s Q&A.';
		} catch (e) {
			t.kept = 'no';
			status = `Could not keep it: ${(e as Error).message}`;
		}
	}

	// --- Grow: queue a job, then follow it until it lands or fails. ---

	const verbs = $derived(aiVerbs(!!offer.grow));
	const verbOf = (v: AiVerb) => verbs.find((x) => x.value === v) ?? verbs[0];
	const LIVE = ['queued', 'running', 'applying'];

	/** Ask by default; back to ask after every grow, because grow spends and commits. */
	let verb = $state<AiVerb>('ask');
	const current = $derived(verbOf(verb));
	/** A kept answer the next job turns into content. */
	let growKept = $state<{ id: string; frame: string; about: string } | null>(null);
	let growing = $state(false);
	let jobs = $state<GrowJob[]>([]);
	let input = $state<HTMLTextAreaElement>();
	/** A result arrived while out of sight. */
	let unseen = $state(false);
	let poll: ReturnType<typeof setTimeout> | undefined;

	/** The frame a job would grow from: the kept answer's, or the one being read. */
	const growAnchor = $derived(growKept?.frame ?? frame.id);
	const anchorOnMain = $derived(mainFrames.includes(growAnchor));

	$effect(() => {
		if (showResults) unseen = false;
	});
	$effect(() => {
		onactivity?.(unseen ? 'ready' : running ? 'working' : 'idle');
	});

	$effect(() => {
		if (verb === 'trail' && !anchorOnMain) verb = 'frames';
	});

	onMount(() => {
		if (offer.grow) refreshJobs(true);
		return () => clearTimeout(poll);
	});

	/** A grow verb's label without its "Grow: " prefix. */
	const growLabel = (v: AiVerb) => verbOf(v).label.replace(/^Grow: /, '');

	function jobText(job: GrowJob) {
		switch (job.status) {
			case 'queued':
				return 'waiting';
			case 'running':
				return job.progress ?? 'starting';
			case 'applying':
				return 'committing';
			case 'done': {
				const added = `added ${job.result?.frames.map(titleOf).join(', ')}`;
				// A dev grow's content waits on its branch for review (korg 3442).
				const where = job.result?.branch
					? ` to ${job.result.branch}, for review; it shows here once merged`
					: '';
				return `${added}${where}${job.result?.pushError ? ' (committed, not yet pushed)' : ''}`;
			}
			case 'failed':
				return `failed: ${job.error}`;
		}
	}

	/** Fetch the job list; announce what finished since last time, and keep polling while any runs. */
	async function refreshJobs(first = false) {
		// Grow is not in the reader edition's build (korg 3500): this folds away there.
		if (__KLOOM_EDITION__ === 'reader') return;
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
				else continue;
				if (!showResults) unseen = true;
			}
		}
		jobs = next;
		if (jobs.some((j) => LIVE.includes(j.status))) poll = setTimeout(refreshJobs, 3000);
	}

	async function queueGrow() {
		if (__KLOOM_EDITION__ === 'reader') return;
		const request = text.trim();
		if (growing || !isGrow(verb) || (!request && !growKept)) return;
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
			status = `Grow queued: ${growLabel(job.verb)}, on ${modelLabel(job.model, GROW_MODEL)}.`;
			text = '';
			growKept = null;
			verb = 'ask';
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
		input?.focus();
	}

	function keydown(e: KeyboardEvent) {
		if (e.key === 'Enter' && !e.shiftKey) {
			e.preventDefault();
			(e.currentTarget as HTMLTextAreaElement).form?.requestSubmit();
		}
	}
</script>

<section id="ai-pane" class="ai {layout}" aria-labelledby="ai-title">
	<h2 id="ai-title" class="title" class:visually-hidden={layout === 'tabs'}>AI</h2>

	<!-- Focusable because it scrolls; once focused the arrows scroll it, so the page's keys stand down. -->
	<!-- svelte-ignore a11y_no_noninteractive_tabindex -->
	<div
		id="ai-results"
		class="results"
		class:empty={!turn && !jobs.length}
		role={layout === 'tabs' ? 'tabpanel' : 'region'}
		aria-labelledby={layout === 'tabs' ? 'tab-ai' : undefined}
		aria-label={layout === 'tabs' ? undefined : 'AI results'}
		tabindex="0"
		hidden={!showResults}
		data-own-keys
	>
		{#if turn}
			<article class="answer" aria-labelledby="ai-answer-title" aria-busy={running}>
				<h3 id="ai-answer-title" class="about">
					<span class="visually-hidden">Answer about</span>
					<span aria-hidden="true">About</span>
					{turn.about} · {turn.model}{turn.web ? ' · web' : ''}
				</h3>
				{#if turn.frame !== frame.id}
					<p class="moved">
						You have moved on; this answer stays with the frame it was asked about.
					</p>
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
		{:else if !jobs.length}
			<p class="note">Answers{offer.grow ? ' and grow jobs' : ''} appear here.</p>
		{/if}

		{#if jobs.length}
			<h3 class="about">Grow jobs</h3>
			<ul class="jobs" aria-label="Grow jobs">
				{#each jobs as job (job.id)}
					<li class={job.status}>
						<span class="what">
							{growLabel(job.verb)} · from {titleOf(job.anchor)} ·
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
	</div>

	<form class="control" onsubmit={submit}>
		{#if verbs.length > 1}
			<label for="ai-verb" class="visually-hidden">What to do</label>
			<select id="ai-verb" bind:value={verb}>
				{#each verbs as v (v.value)}
					<option value={v.value} disabled={v.value === 'trail' && !anchorOnMain}>{v.label}</option>
				{/each}
			</select>
		{/if}
		<label for="ai-input" class="visually-hidden">
			{isGrow(verb) ? 'What grow should write' : 'Ask a question about this frame'}
		</label>
		<textarea
			id="ai-input"
			rows="1"
			placeholder={current.placeholder}
			aria-describedby="ai-hint"
			maxlength="2000"
			bind:value={text}
			bind:this={input}
			onkeydown={keydown}></textarea>
		<div class="send">
			{#if offer.web !== 'deny' && !isGrow(verb)}
				<label class="web" title="Let the model search the web for this question">
					<input type="checkbox" bind:checked={includeWeb} />
					Web
				</label>
			{/if}
			{#if isGrow(verb)}
				<button type="submit" class="grow" disabled={growing}>{current.send}</button>
			{:else}
				<button type="submit" disabled={resting && !running}
					>{running ? 'Stop' : current.send}</button
				>
			{/if}
		</div>
	</form>
	{#if budgetNote && !isGrow(verb)}
		<p class="note budget">{budgetNote}</p>
	{/if}
	{#if isGrow(verb)}
		<p class="note grow-note">
			Grow queues a job on {modelLabel(settings.get(GROW_MODEL) ?? '', GROW_MODEL)} that writes new content
			and commits it to this subject.
		</p>
		{#if growKept}
			<p class="note">
				From your kept answer about {growKept.about}
				<button type="button" class="link" onclick={() => (growKept = null)}>Don’t use it</button>
			</p>
		{/if}
	{/if}

	<div class="status-line">
		<p class="status" role="status">{status}</p>
		{#if !showResults && unseen}
			<button type="button" class="link" onclick={onshow}>Show it</button>
		{/if}
	</div>
</section>

<style>
	.ai {
		display: flex;
		flex-direction: column;
		gap: 0.4rem;
		min-height: 0;
		padding: 0.75rem 1.5rem;
	}
	.strip {
		border-top: 1px solid color-mix(in srgb, var(--muted) 40%, transparent);
	}
	.columns {
		border-left: 1px solid color-mix(in srgb, var(--muted) 40%, transparent);
	}
	.split,
	.tabs {
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
	/* A tall pane: the results take the height and scroll; the control stays at the foot. */
	.results {
		flex: 1 1 auto;
		min-height: 0;
		overflow-y: auto;
		display: flex;
		flex-direction: column;
		gap: 0.5rem;
	}
	.results[hidden] {
		display: none;
	}
	.strip .results {
		flex: 0 1 auto;
		max-height: 35vh;
	}
	.strip .results.empty {
		display: none;
	}
	/* The verb on its own row; the text box beside a narrow column of Web over the button. */
	.control {
		display: grid;
		grid-template-columns: minmax(0, 1fr) auto;
		gap: 0.4rem 0.5rem;
	}
	.control select {
		grid-column: 1 / -1;
		justify-self: start;
	}
	.send {
		display: flex;
		flex-direction: column;
		justify-content: flex-end;
		align-items: stretch;
		gap: 0.25rem;
	}
	textarea,
	select {
		font: inherit;
		color: var(--ink);
		background: color-mix(in srgb, var(--ink) 6%, transparent);
		border: 1px solid var(--muted);
		border-radius: 0.25rem;
	}
	textarea {
		resize: vertical;
		min-height: 2.25rem;
		padding: 0.4rem 0.6rem;
	}
	select {
		font-size: 0.85rem;
		padding: 0.3rem 0.5rem;
		max-width: 100%;
	}
	button {
		font: inherit;
		font-size: 0.85rem;
		padding: 0.2rem 0.6rem;
		color: var(--background);
		background: var(--accent);
		border: 0;
		border-radius: 0.25rem;
		cursor: pointer;
	}
	/* Grow commits: its button reads as the bigger action. */
	button.grow {
		outline: 2px solid var(--accent);
		outline-offset: 2px;
		font-weight: bold;
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
	.link {
		padding: 0;
		color: var(--accent);
		background: none;
		text-decoration: underline;
	}
	.jobs {
		list-style: none;
		margin: 0;
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
		flex-wrap: wrap;
		align-items: center;
		gap: 0.75rem;
	}
	.actions button {
		padding: 0.25rem 0.75rem;
	}
	.note,
	.status {
		margin: 0;
		font-size: 0.8rem;
		color: var(--muted);
	}
	.status-line {
		display: flex;
		gap: 0.75rem;
		align-items: baseline;
	}
	.status-line .link {
		font-size: 0.8rem;
	}
	.status:empty {
		display: none;
	}
</style>

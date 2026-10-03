<script lang="ts">
	import Icon from './Icon.svelte';
	import { tick } from 'svelte';
	import {
		annotatedFrames,
		bySubject,
		clearQuestion,
		detachedIn,
		FILTERS,
		filterCounts,
		isLive,
		keeps,
		statesOf,
		type MyNotesOffer,
		type NoteEntry,
		type NotesFilter
	} from '../my-notes';
	import { readingText } from './reading-text';

	interface Props {
		offer: MyNotesOffer;
		/** The key that opens it, when it is on. */
		key?: string | null;
	}

	let { offer, key = null }: Props = $props();

	const id = $props.id();
	let dialog = $state<HTMLDialogElement>();
	let notes = $state<NoteEntry[] | null>(null);
	let failed = $state(false);
	let filter = $state<NotesFilter>('all');
	/** Annotations whose words their reading no longer has. */
	let detached = $state<ReadonlySet<string>>(new Set());
	/** Frames still being read to find annotations' words in. */
	let checking = $state(0);
	/** Said after an action: what it did. */
	let said = $state('');

	const counts = $derived(filterCounts(notes ?? [], detached));
	const shown = $derived((notes ?? []).filter((n) => keeps(filter, n, detached)));
	const groups = $derived(bySubject(shown));
	const unseenSaid = $derived(
		offer.unseen ? `, ${offer.unseen} new ${offer.unseen === 1 ? 'answer' : 'answers'}` : ''
	);

	/** Open the panel, load the list, and take the answers in it as seen. */
	export async function show() {
		if (!dialog || dialog.open) return;
		notes = null;
		failed = false;
		said = '';
		detached = new Set();
		dialog.showModal();
		const data = await offer.load();
		if (!data) {
			failed = true;
			await tick();
			dialog.querySelector<HTMLElement>('.close')?.focus();
			return;
		}
		notes = data.notes;
		await tick();
		focusEntry(0);
		// Shown as new for as long as the panel is open; the count clears now.
		const waiting = data.notes.filter((n) => n.unseen).map((n) => n.id);
		if (waiting.length) offer.seen(waiting);
		findWords(data.notes);
	}

	/**
	 * Read each annotated frame and look for its annotations' words, as the
	 * reading pane does (§Annotations). A frame the library no longer has
	 * leaves its annotations detached; one that could not be read is left
	 * unjudged.
	 */
	async function findWords(all: NoteEntry[]) {
		const frames = annotatedFrames(all);
		checking = frames.length;
		let lost: string[] = [];
		await Promise.all(
			frames.map(async (on) => {
				const [{ subject, frame }] = on;
				let found: string[] | null = on.map((n) => n.id);
				if (isLive(on[0])) {
					const html = await offer.reading(subject, frame);
					found =
						html === null
							? null
							: detachedIn(
									readingText(new DOMParser().parseFromString(html, 'text/html').body).text,
									on
								);
				}
				lost = [...lost, ...(found ?? [])];
				checking -= 1;
				detached = new Set(lost);
			})
		);
	}

	/** The entries' own controls, in the order they are shown. */
	const entries = () => [...(dialog?.querySelectorAll<HTMLElement>('[data-entry]') ?? [])];

	function focusEntry(i: number) {
		const all = entries();
		const to = all[Math.max(0, Math.min(i, all.length - 1))];
		(to ?? dialog?.querySelector<HTMLElement>('.filters input:checked'))?.focus();
	}

	/** In the list: ↑ and ↓ move between notes, Home and End to the ends, Delete clears one. */
	function entryKeys(e: KeyboardEvent, n: NoteEntry) {
		const all = entries();
		const at = all.indexOf(e.currentTarget as HTMLElement);
		const to = { ArrowDown: at + 1, ArrowUp: at - 1, Home: 0, End: all.length - 1 }[e.key];
		if (to !== undefined) {
			e.preventDefault();
			focusEntry(to);
		} else if (e.key === 'Delete') {
			e.preventDefault();
			clear(n);
		}
	}

	function go(e: MouseEvent, n: NoteEntry) {
		if (e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
		e.preventDefault();
		// Closing hands focus back to where it was when the panel opened (the
		// dialog's own behaviour); the jump then moves it on to the note.
		dialog?.close();
		offer.go(n);
	}

	const what = (n: NoteEntry) => (n.anchor ? 'annotation' : 'note');
	const opening = (n: NoteEntry) => n.text.slice(0, 40);

	/** Take notes out of the list after they were deleted, and focus what took their place. */
	async function removed(ids: string[], from: number) {
		notes = (notes ?? []).filter((n) => !ids.includes(n.id));
		await tick();
		focusEntry(from);
	}

	async function clear(n: NoteEntry) {
		if (!confirm(`Delete this ${what(n)}? This cannot be undone.`)) return;
		const at = shown.indexOf(n);
		const gone = await offer.clear([n.id]);
		if (gone === null) {
			said = `Could not delete the ${what(n)}.`;
			return;
		}
		said = `${what(n) === 'note' ? 'Note' : 'Annotation'} deleted.`;
		await removed([n.id], at);
	}

	async function clearAll(kind: 'answered' | 'detached') {
		const ids = (notes ?? []).filter((n) => keeps(kind, n, detached)).map((n) => n.id);
		if (!ids.length || !confirm(clearQuestion(kind, ids.length))) return;
		const gone = await offer.clear(ids);
		if (gone === null) {
			said = 'Could not delete them. Nothing was deleted.';
			return;
		}
		said = `${gone} deleted.`;
		await removed(ids, 0);
	}

	/** The "Agent review" box, from here: what pressing it would do. */
	const flagLabel = (n: NoteEntry) =>
		n.review === 'flagged'
			? 'Withdraw agent review'
			: n.review === 'handled'
				? 'Ask the agent again'
				: 'Flag for agent review';

	async function toggleFlag(n: NoteEntry) {
		const on = n.review !== 'flagged';
		const saved = await offer.flag(n, on);
		if (!saved) {
			said = 'Could not change the flag.';
			return;
		}
		notes = (notes ?? []).map((x) => (x.id === n.id ? { ...x, ...saved } : x));
		said =
			saved.review === 'flagged'
				? 'Flagged for agent review.'
				: saved.review === 'handled'
					? 'No longer flagged. The agent’s answer stays.'
					: 'No longer flagged.';
	}
</script>

<button
	type="button"
	class="icon opener"
	aria-haspopup="dialog"
	title={`My notes${key ? ` (${key})` : ''}${unseenSaid ? `: ${offer.unseen} new` : ''}`}
	onclick={show}
>
	<!-- A page with lines and a corner turned: the reader's own writing. -->
	<Icon name="my-notes" />
	<span class="visually-hidden">My notes{unseenSaid}</span>
	{#if offer.unseen}
		<span class="badge" aria-hidden="true">{offer.unseen}</span>
	{/if}
</button>

<!-- A modal, like the map: the page behind is inert, its keys stand down, and Esc closes it. -->
<dialog class="my-notes" aria-labelledby="{id}-title" data-own-keys bind:this={dialog}>
	<header>
		<h2 id="{id}-title">My notes</h2>
		<button type="button" class="close" onclick={() => dialog?.close()}>
			<span aria-hidden="true">×</span>
			<span class="visually-hidden">Close my notes</span>
		</button>
	</header>

	{#if failed}
		<p class="said">Could not load your notes. Close this and try again.</p>
	{:else if !notes}
		<p class="said" role="status">Loading your notes…</p>
	{:else}
		<fieldset class="filters">
			<legend class="visually-hidden">Show</legend>
			{#each FILTERS as f (f.id)}
				<label>
					<input type="radio" name="{id}-filter" value={f.id} bind:group={filter} />
					{f.label} <span class="n">({counts[f.id]})</span>
				</label>
			{/each}
		</fieldset>

		<p class="said" role="status">
			{said}
			{#if checking}
				Checking annotations’ words against their readings…
			{/if}
		</p>

		<!-- It scrolls as focus moves along its notes, each a link or a button. -->
		<div class="list">
			{#each groups as g (g.subject)}
				<section aria-labelledby="{id}-{g.subject}">
					<h3 id="{id}-{g.subject}">{g.title}</h3>
					<ul>
						{#each g.notes as n (n.id)}
							{@const states = statesOf(n, detached)}
							{@const about = `${id}-${n.id}`}
							<li class:new={n.unseen}>
								{#if isLive(n)}
									<!-- The page resolved these app routes. -->
									<!-- eslint-disable svelte/no-navigation-without-resolve -->
									<a
										class="title"
										href={offer.hrefOf(n.subject, n.frame)}
										data-entry
										aria-describedby="{about}-state {about}-text"
										onclick={(e) => go(e, n)}
										onkeydown={(e) => entryKeys(e, n)}
									>
										{n.topic}
									</a>
									<!-- eslint-enable svelte/no-navigation-without-resolve -->
									<span class="where">{n.position}</span>
								{:else}
									<button
										type="button"
										class="title gone"
										data-entry
										aria-describedby="{about}-state {about}-text"
										onclick={() =>
											(said = `“${n.label}” is no longer in the library. Its ${what(n)} can only be cleared.`)}
										onkeydown={(e) => entryKeys(e, n)}
									>
										{n.label}
									</button>
								{/if}
								<p id="{about}-state" class="state">
									{n.anchor ? 'Annotation' : 'Note'}
									{#each isLive(n) ? states : [...states, 'No longer in the library'] as s (s)}
										<span aria-hidden="true">·</span> <strong>{s}</strong>
									{/each}
								</p>
								<div id="{about}-text">
									{#if n.anchor}
										<blockquote class="quote">
											<span class="visually-hidden">On the words: </span>{n.anchor.exact}
										</blockquote>
									{/if}
									<p class="text">{n.text}</p>
									{#if n.review === 'handled'}
										<p class="response"><span class="who">Agent:</span> {n.response}</p>
									{/if}
								</div>
								<p class="actions">
									{#if isLive(n)}
										<button type="button" onclick={() => toggleFlag(n)}
											>{flagLabel(n)}<span class="visually-hidden">: {opening(n)}</span></button
										>
									{/if}
									<button type="button" onclick={() => clear(n)}
										>Clear<span class="visually-hidden">: {opening(n)}</span></button
									>
								</p>
							</li>
						{/each}
					</ul>
				</section>
			{:else}
				<p class="empty">
					{#if notes.length}
						None of your notes is {filter === 'pending'
							? 'waiting for agent review'
							: filter === 'answered'
								? 'answered'
								: 'detached'}.
					{:else}
						No notes yet. On any frame, N writes a note and A annotates words of its reading.
					{/if}
				</p>
			{/each}
		</div>

		<footer>
			<p class="keys">↑ ↓ between notes · Enter goes · Delete clears · Esc closes</p>
			<div class="bulk">
				<button type="button" disabled={!counts.answered} onclick={() => clearAll('answered')}
					>Clear answered ({counts.answered})</button
				>
				<button
					type="button"
					disabled={!counts.detached || checking > 0}
					onclick={() => clearAll('detached')}>Clear detached ({counts.detached})</button
				>
			</div>
		</footer>
	{/if}
</dialog>

<style>
	.icon {
		position: relative;
		display: grid;
		place-items: center;
		width: 2rem;
		height: 2rem;
		padding: 0;
		color: var(--muted);
		background: none;
		border: 1px solid transparent;
		border-radius: 0.25rem;
		cursor: pointer;
	}
	.icon:hover {
		color: var(--ink);
		border-color: var(--muted);
	}
	.icon :global(svg) {
		width: 1.25rem;
		height: 1.25rem;
	}
	.badge {
		position: absolute;
		top: -0.3rem;
		right: -0.3rem;
		min-width: 1rem;
		padding: 0 0.2rem;
		font: 0.65rem/1rem var(--mono);
		color: var(--background);
		background: var(--accent);
		border-radius: 0.5rem;
	}
	.my-notes {
		width: min(44rem, calc(100vw - 1rem));
		max-height: calc(100dvh - 1rem);
		padding: 0;
		font-family: var(--sans, inherit);
		font-size: 0.9rem;
		text-align: left;
		text-transform: none;
		letter-spacing: 0;
		color: var(--ink);
		background: var(--background);
		border: 1px solid var(--muted);
		border-radius: 0.25rem;
		box-shadow: 0 0.5rem 1.5rem color-mix(in srgb, #000 35%, transparent);
		user-select: text;
	}
	.my-notes[open] {
		display: grid;
		grid-template-rows: auto auto auto minmax(0, 1fr) auto;
	}
	.my-notes::backdrop {
		background: rgb(0 0 0 / 0.5);
	}
	header,
	footer {
		display: flex;
		flex-wrap: wrap;
		align-items: center;
		justify-content: space-between;
		gap: 0.5rem 1rem;
		padding: 0.75rem 1rem;
	}
	header {
		border-bottom: 1px solid color-mix(in srgb, var(--muted) 40%, transparent);
	}
	footer {
		border-top: 1px solid color-mix(in srgb, var(--muted) 40%, transparent);
	}
	h2 {
		margin: 0;
		font-family: var(--mono);
		font-size: 0.75rem;
		font-weight: normal;
		letter-spacing: 0.12em;
		text-transform: uppercase;
		color: var(--muted);
	}
	h3 {
		margin: 0 0 0.5rem;
		font-size: 0.8rem;
		color: var(--muted);
	}
	button {
		font: inherit;
		color: var(--ink);
		background: none;
		border: 1px solid var(--muted);
		border-radius: 0.25rem;
		padding: 0.2rem 0.6rem;
		cursor: pointer;
	}
	button:disabled {
		color: var(--muted);
		cursor: default;
		opacity: 0.6;
	}
	.close {
		font: 1.1rem/1 var(--serif, inherit);
		border-color: transparent;
	}
	.close:hover {
		border-color: var(--muted);
	}
	.filters {
		display: flex;
		flex-wrap: wrap;
		gap: 0.25rem 1rem;
		margin: 0;
		padding: 0.6rem 1rem 0;
		border: 0;
	}
	.filters label {
		display: flex;
		align-items: center;
		gap: 0.3rem;
		cursor: pointer;
	}
	.n,
	.where,
	.keys,
	.said,
	.empty {
		color: var(--muted);
	}
	.said {
		min-height: 1.2em;
		margin: 0;
		padding: 0.4rem 1rem 0;
		font-size: 0.8rem;
	}
	.list {
		overflow-y: auto;
		overscroll-behavior: contain;
		padding: 0.5rem 1rem 1rem;
	}
	section + section {
		margin-top: 1rem;
	}
	ul {
		display: grid;
		gap: 0.75rem;
		margin: 0;
		padding: 0;
		list-style: none;
	}
	li {
		padding: 0.6rem 0.75rem;
		border-left: 2px solid color-mix(in srgb, var(--muted) 40%, transparent);
	}
	li.new {
		border-left-color: var(--accent);
	}
	.title {
		font-weight: 600;
		color: var(--ink);
	}
	a.title {
		text-decoration: none;
	}
	a.title:hover {
		text-decoration: underline;
	}
	.title.gone {
		padding: 0;
		border: 0;
		color: var(--muted);
		text-align: left;
	}
	.where {
		margin-left: 0.4rem;
		font-size: 0.8rem;
	}
	.state,
	.text,
	.response,
	.actions {
		margin: 0.3rem 0 0;
	}
	.state {
		font-size: 0.8rem;
		color: var(--muted);
	}
	.state strong {
		font-weight: normal;
		color: var(--accent);
	}
	.quote {
		margin: 0.4rem 0 0;
		padding-left: 0.6rem;
		font-style: italic;
		border-left: 2px solid var(--accent);
	}
	.text {
		white-space: pre-wrap;
		overflow-wrap: anywhere;
	}
	.response {
		overflow-wrap: anywhere;
	}
	.who {
		color: var(--accent);
	}
	.actions {
		display: flex;
		flex-wrap: wrap;
		gap: 0.4rem;
	}
	.actions button {
		font-size: 0.8rem;
	}
	.keys {
		margin: 0;
		font-size: 0.75rem;
	}
	.bulk {
		display: flex;
		flex-wrap: wrap;
		gap: 0.5rem;
	}
	.empty {
		margin: 0.5rem 0;
	}
</style>

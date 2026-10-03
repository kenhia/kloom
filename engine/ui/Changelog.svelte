<script module lang="ts">
	import type { Palette } from '../model';
	import type { ChangelogData, ReaderNews } from '../whats-new';

	/** What the page offers the Changelog (docs/design.md §What's new, korg 3525, 3526). */
	export interface ChangelogOffer {
		/** The entries, fetched when it first opens; null when they could not be had. */
		load: () => Promise<ChangelogData | null>;
		/** The reader's side: what is new to them, their readings, their last visit. Null with no reader. */
		news: ReaderNews | null;
		hrefOf: (subject: string, frame: string) => string;
		/** Go to a frame, here or in another subject: a jump, with a way back. */
		onfollow: (subject: string, frame: string) => void;
		/** "Mark all as seen" for one subject's frames; false when it failed. */
		onseen?: (subject: string, frames: string[]) => Promise<boolean>;
		/** "I'm caught up on this subject"; false when it failed. */
		oncaughtup?: (subject: string) => Promise<boolean>;
	}
</script>

<script lang="ts">
	import { tick } from 'svelte';
	import { chicagoDate } from '../citation';
	import { FRESH_TEXT } from '../marks';
	import {
		ALL,
		byDayAndSubject,
		dayLabel,
		EDIT_WORD,
		entryFrames,
		filterChangelog,
		localDay,
		WHEN_LABEL,
		WHENS,
		type AddedEntry,
		type ChangelogFilter,
		type EditEntry
	} from '../whats-new';

	interface Props {
		offer: ChangelogOffer;
	}

	let { offer }: Props = $props();

	const id = $props.id();
	let dialog = $state<HTMLDialogElement>();
	let data = $state<ChangelogData | null>(null);
	let failed = $state(false);
	let tab = $state<'added' | 'edits'>('added');
	let filter = $state<ChangelogFilter>({ ...ALL });
	/** Said after an action: what it did. */
	let said = $state('');
	let refocus: (() => void) | null = null;
	/** The colours of what it opened over: the reading's, or the start screen's. */
	let palette = $state<Palette | null>(null);

	// The reader's presets only mean something with a reader.
	const whens = $derived(
		WHENS.filter((w) => offer.news || (w !== 'last-visit' && w !== 'caught-up'))
	);
	const titleOf = $derived(new Map((data?.subjects ?? []).map((s) => [s.id, s.title])));
	const shown = $derived(
		data
			? filterChangelog(data, filter, { now: new Date(), news: offer.news, dayOf: localDay })
			: { added: [], edits: [] }
	);
	const addedDays = $derived(byDayAndSubject(shown.added, (e) => localDay(e.at)));
	const editDays = $derived(byDayAndSubject(shown.edits, (e) => e.date));
	const fresh = (subject: string) => new Set(offer.news?.fresh[subject] ?? []);
	/** The entry's frames still new to the reader. */
	const freshIn = (e: AddedEntry) => {
		const f = fresh(e.subject);
		return entryFrames(e).filter((x) => f.has(x));
	};
	/** What "Mark all as seen" would clear: the shown entries' new frames, by subject. */
	const unseen = $derived.by(() => {
		const by: Record<string, string[]> = {};
		for (const e of shown.added)
			for (const f of freshIn(e)) if (!by[e.subject]?.includes(f)) (by[e.subject] ??= []).push(f);
		return by;
	});
	const unseenCount = $derived(Object.values(unseen).reduce((n, s) => n + s.length, 0));
	/** One subject filtered: the Changelog offers to catch up on it. */
	const only = $derived(filter.subjects.length === 1 ? filter.subjects[0] : null);

	/**
	 * Open it, on the Added tab with every subject and all time, or on one
	 * subject, in the colours of what it opens over. Focus goes back through
	 * `refocus` when it closes.
	 */
	export async function show(
		o: { refocus?: () => void; subject?: string; palette?: Palette } = {}
	) {
		if (!dialog || dialog.open) return;
		refocus = o.refocus ?? null;
		palette = o.palette ?? null;
		said = '';
		tab = 'added';
		filter = { ...ALL, subjects: o.subject ? [o.subject] : [] };
		dialog.showModal();
		// The page keeps it for the build: a grow brings a new one.
		failed = false;
		const got = await offer.load();
		data = got ?? data;
		failed = !data;
		await tick();
		dialog.querySelector<HTMLElement>(`#${CSS.escape(`${id}-tab-${tab}`)}`)?.focus();
	}

	function closed() {
		const back = refocus;
		refocus = null;
		back?.();
	}

	function toggleSubject(subject: string, on: boolean) {
		const rest = filter.subjects.filter((s) => s !== subject);
		filter = { ...filter, subjects: on ? [...rest, subject] : rest };
	}

	function tabKey(e: KeyboardEvent) {
		if (e.key !== 'ArrowLeft' && e.key !== 'ArrowRight' && e.key !== 'Home' && e.key !== 'End')
			return;
		e.preventDefault();
		tab = tab === 'added' ? 'edits' : 'added';
		dialog?.querySelector<HTMLElement>(`#${CSS.escape(`${id}-tab-${tab}`)}`)?.focus();
	}

	/** The entries' own links, in the order they are shown. */
	const entries = () => [
		...(dialog?.querySelectorAll<HTMLElement>(`#${CSS.escape(`${id}-panel`)} [data-entry]`) ?? [])
	];

	/** In the list: ↑ and ↓ move between entries, Home and End to the ends. */
	function entryKeys(e: KeyboardEvent) {
		const all = entries();
		const at = all.indexOf(e.currentTarget as HTMLElement);
		const to = { ArrowDown: at + 1, ArrowUp: at - 1, Home: 0, End: all.length - 1 }[e.key];
		if (to === undefined) return;
		e.preventDefault();
		all[Math.max(0, Math.min(to, all.length - 1))]?.focus();
	}

	function go(e: MouseEvent, subject: string, frame: string) {
		if (e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
		e.preventDefault();
		// The jump decides where focus goes: the spine, where the frame is announced.
		refocus = null;
		dialog?.close();
		offer.onfollow(subject, frame);
	}

	async function markAll() {
		if (!offer.onseen || !unseenCount) return;
		const n = unseenCount;
		const done = await Promise.all(
			Object.entries(unseen).map(([subject, frames]) => offer.onseen!(subject, frames))
		);
		said = done.every(Boolean)
			? `Marked ${n === 1 ? '1 frame' : `${n} frames`} as seen.`
			: 'Could not mark them all as seen. Try again.';
	}

	async function caughtUp(subject: string) {
		if (!offer.oncaughtup) return;
		said = (await offer.oncaughtup(subject))
			? `Caught up on ${titleOf.get(subject) ?? subject}: from now, anything added there is new.`
			: 'Could not save that you are caught up. Try again.';
	}

	const count = (n: number, one: string, many: string) => `${n} ${n === 1 ? one : many}`;
	const what = (e: AddedEntry) =>
		e.kind === 'subject'
			? `First published · ${count(e.frames?.length ?? 0, 'frame', 'frames')}`
			: e.kind === 'trail'
				? `New trail${e.frames?.length ? ` · with ${count(e.frames.length, 'frame', 'frames')}` : ''}`
				: `${e.position}${e.trail ? ` · on the ${e.trail} trail` : ''}`;
	const editKey = (e: EditEntry, i: number) => `${e.subject}/${e.frame}/${e.date}/${i}`;
</script>

<!-- A modal, like My notes and the map: the page behind is inert, its keys stand down, and Esc closes it. -->
<dialog
	class="changelog"
	aria-labelledby="{id}-title"
	data-own-keys
	style:--background={palette?.background}
	style:--ink={palette?.ink}
	style:--muted={palette?.muted}
	style:--accent={palette?.accent}
	style:color-scheme={palette?.scheme}
	bind:this={dialog}
	onclose={closed}
>
	<header>
		<h2 id="{id}-title">What’s new</h2>
		<button type="button" class="close" onclick={() => dialog?.close()}>
			<span aria-hidden="true">×</span>
			<span class="visually-hidden">Close what’s new</span>
		</button>
	</header>

	<div role="tablist" aria-label="Changelog" class="tabs">
		{#each [['added', 'Added'], ['edits', 'Edits and corrections']] as const as [t, label] (t)}
			<button
				type="button"
				role="tab"
				id="{id}-tab-{t}"
				aria-selected={tab === t}
				aria-controls="{id}-panel"
				tabindex={tab === t ? 0 : -1}
				onclick={() => (tab = t)}
				onkeydown={tabKey}>{label}</button
			>
		{/each}
	</div>

	{#if failed}
		<p class="said">Could not load the Changelog. Close this and try again.</p>
	{:else if !data}
		<p class="said" role="status">Loading the Changelog…</p>
	{:else}
		<div class="filters">
			<fieldset>
				<legend>Subjects</legend>
				{#each data.subjects as s (s.id)}
					<label>
						<input
							type="checkbox"
							checked={filter.subjects.includes(s.id)}
							onchange={(e) => toggleSubject(s.id, e.currentTarget.checked)}
						/>
						{s.title}
					</label>
				{/each}
				{#if filter.subjects.length}
					<button type="button" class="link" onclick={() => (filter = { ...filter, subjects: [] })}
						>Every subject</button
					>
				{/if}
			</fieldset>
			<div class="when">
				<label for="{id}-when">When</label>
				<select id="{id}-when" bind:value={filter.when}>
					{#each whens as w (w)}
						<option value={w}>{WHEN_LABEL[w]}</option>
					{/each}
				</select>
				{#if filter.when === 'between'}
					<label for="{id}-from">From</label>
					<input id="{id}-from" type="date" bind:value={filter.from} />
					<label for="{id}-to">To</label>
					<input id="{id}-to" type="date" bind:value={filter.to} />
				{/if}
			</div>
		</div>

		<p class="said" role="status">
			{#if said}{said}{:else}
				{tab === 'added'
					? count(shown.added.length, 'entry', 'entries')
					: count(shown.edits.length, 'edit', 'edits')}{filter.subjects.length
					? ` in ${filter.subjects.map((s) => titleOf.get(s) ?? s).join(', ')}`
					: ''}{filter.when === 'all'
					? ''
					: ` · ${WHEN_LABEL[filter.when][0].toLowerCase() + WHEN_LABEL[filter.when].slice(1)}`}
			{/if}
		</p>

		<div
			id="{id}-panel"
			class="list"
			role="tabpanel"
			aria-labelledby="{id}-tab-{tab}"
			tabindex="-1"
		>
			{#if tab === 'added'}
				{#each addedDays as d (d.day)}
					<section aria-labelledby="{id}-a-{d.day}">
						<h3 id="{id}-a-{d.day}">{dayLabel(d.day)}</h3>
						{#each d.subjects as g (g.subject)}
							<h4>{titleOf.get(g.subject) ?? g.subject}</h4>
							<ul>
								{#each g.entries as e (`${e.kind}/${e.subject}/${e.id}`)}
									{@const isNew = freshIn(e).length > 0}
									<li class:new={isNew}>
										<!-- The page resolved these app routes. -->
										<!-- eslint-disable svelte/no-navigation-without-resolve -->
										<a
											href={offer.hrefOf(e.subject, e.frame)}
											data-entry
											onclick={(ev) => go(ev, e.subject, e.frame)}
											onkeydown={entryKeys}
										>
											{e.kind === 'trail' ? `Trail: ${e.title}` : e.title}
										</a>
										<!-- eslint-enable svelte/no-navigation-without-resolve -->
										<span class="where"
											>{what(e)}{#if isNew}<strong class="fresh">· {FRESH_TEXT}</strong>{/if}</span
										>
									</li>
								{/each}
							</ul>
						{/each}
					</section>
				{:else}
					<p class="empty">Nothing was added {filter.when === 'all' ? 'yet' : 'then'}.</p>
				{/each}
			{:else}
				{#each editDays as d (d.day)}
					<section aria-labelledby="{id}-e-{d.day}">
						<h3 id="{id}-e-{d.day}">{chicagoDate(d.day)}</h3>
						{#each d.subjects as g (g.subject)}
							<h4>{titleOf.get(g.subject) ?? g.subject}</h4>
							<ul>
								{#each g.entries as e, i (editKey(e, i))}
									<li>
										<!-- eslint-disable svelte/no-navigation-without-resolve -->
										<a
											href={offer.hrefOf(e.subject, e.frame)}
											data-entry
											onclick={(ev) => go(ev, e.subject, e.frame)}
											onkeydown={entryKeys}>{e.title}</a
										>
										<!-- eslint-enable svelte/no-navigation-without-resolve -->
										<span class="where">{e.position} · {EDIT_WORD[e.kind]}</span>
										<p class="summary">{e.summary}</p>
									</li>
								{/each}
							</ul>
						{/each}
					</section>
				{:else}
					<p class="empty">No edits or corrections {filter.when === 'all' ? 'yet' : 'then'}.</p>
				{/each}
			{/if}
		</div>

		<footer>
			<p class="keys">↑ ↓ between entries · Enter goes · Esc closes</p>
			{#if offer.news && tab === 'added'}
				<div class="bulk">
					{#if offer.onseen}
						<button type="button" disabled={!unseenCount} onclick={markAll}
							>Mark all as seen ({unseenCount})</button
						>
					{/if}
					{#if only && offer.oncaughtup}
						<button type="button" onclick={() => caughtUp(only)}
							>I’m caught up on {titleOf.get(only) ?? only}</button
						>
					{/if}
				</div>
			{/if}
		</footer>
	{/if}
</dialog>

<style>
	.changelog {
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
	.changelog[open] {
		display: grid;
		grid-template-rows: auto auto auto auto minmax(0, 1fr) auto;
	}
	.changelog::backdrop {
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
		margin: 0 0 0.25rem;
		font-size: 0.85rem;
	}
	h4 {
		margin: 0.4rem 0 0.3rem;
		font-size: 0.8rem;
		font-weight: normal;
		color: var(--muted);
	}
	button,
	select,
	input[type='date'] {
		font: inherit;
		color: var(--ink);
		background: var(--background);
		border: 1px solid var(--muted);
		border-radius: 0.25rem;
		padding: 0.2rem 0.6rem;
	}
	button {
		background: none;
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
	.link {
		padding: 0;
		border: 0;
		font-size: 0.8rem;
		text-decoration: underline;
		text-decoration-color: var(--accent);
	}
	.tabs {
		display: flex;
		gap: 0.25rem;
		padding: 0.5rem 1rem 0;
	}
	[role='tab'] {
		border: 0;
		border-bottom: 2px solid transparent;
		border-radius: 0;
		color: var(--muted);
	}
	[role='tab'][aria-selected='true'] {
		color: var(--ink);
		border-bottom-color: var(--accent);
	}
	.filters {
		display: grid;
		gap: 0.4rem;
		padding: 0.5rem 1rem 0;
	}
	fieldset {
		display: flex;
		flex-wrap: wrap;
		align-items: center;
		gap: 0.2rem 0.9rem;
		margin: 0;
		padding: 0;
		border: 0;
	}
	legend {
		float: left;
		margin-right: 0.5rem;
		font-size: 0.8rem;
		color: var(--muted);
	}
	fieldset label {
		display: flex;
		align-items: center;
		gap: 0.3rem;
		cursor: pointer;
	}
	.when {
		display: flex;
		flex-wrap: wrap;
		align-items: center;
		gap: 0.3rem 0.5rem;
	}
	.when label {
		font-size: 0.8rem;
		color: var(--muted);
	}
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
		gap: 0.35rem;
		margin: 0;
		padding: 0;
		list-style: none;
	}
	li {
		padding: 0.2rem 0.6rem;
		border-left: 2px solid color-mix(in srgb, var(--muted) 40%, transparent);
	}
	li.new {
		border-left-color: var(--accent);
	}
	a {
		font-weight: 600;
		color: var(--ink);
		text-decoration: none;
	}
	a:hover {
		text-decoration: underline;
	}
	.where {
		margin-left: 0.4rem;
		font-size: 0.8rem;
	}
	.fresh {
		margin-left: 0.3rem;
		font-weight: normal;
		color: var(--accent);
	}
	.summary {
		margin: 0.2rem 0 0;
		overflow-wrap: anywhere;
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

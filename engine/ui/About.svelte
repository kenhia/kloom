<script lang="ts">
	import type { LibraryStats } from '../stats';
	import IconButton from './IconButton.svelte';

	interface Props {
		/** The library's counts, fetched when the panel first opens. */
		stats: () => Promise<LibraryStats>;
		/** Which build this is: a short commit hash and its date. */
		build?: string;
	}

	let { stats, build }: Props = $props();

	const id = $props.id();
	let open = $state(false);
	let root = $state<HTMLElement>();
	let button = $state<IconButton>();
	let loaded = $state<Promise<LibraryStats>>();

	function toggle() {
		open = !open;
		if (open && !loaded) loaded = stats();
	}

	function close(refocus: boolean) {
		open = false;
		if (refocus) button?.focus();
	}

	/** Esc closes the panel and returns focus to its button, as the settings pop-up does. */
	function escape(e: KeyboardEvent) {
		if (e.key !== 'Escape' || !open) return;
		e.preventDefault();
		close(true);
	}

	function outside(e: PointerEvent) {
		if (open && !root?.contains(e.target as Node)) close(false);
	}

	/** Moving on by Tab past the panel closes it, so it never sits over the next control. */
	function focusout(e: FocusEvent) {
		const to = e.relatedTarget as Node | null;
		if (open && to && !root?.contains(to)) close(false);
	}

	const n = (v: number) => v.toLocaleString('en-US');
	const counts = (s: LibraryStats) => [
		['Images', s.images],
		['Charts', s.charts],
		['Tables', s.tables],
		['Names', s.names],
		['Connections', s.connections],
		['Citations', s.citations]
	];
</script>

<svelte:window onpointerdown={outside} />

<!-- svelte-ignore a11y_no_static_element_interactions -->
<div class="about" bind:this={root} onkeydown={escape} onfocusout={focusout}>
	<IconButton
		label="About kloom"
		aria-expanded={open}
		aria-controls="{id}-panel"
		bind:this={button}
		onclick={toggle}
	>
		<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor">
			<circle cx="12" cy="12" r="9" stroke-width="1.5" />
			<line x1="12" y1="10.5" x2="12" y2="17" stroke-width="1.75" />
			<circle cx="12" cy="7.25" r="0.6" fill="currentColor" stroke-width="1" />
		</svg>
	</IconButton>

	<div
		id="{id}-panel"
		class="panel"
		role="group"
		aria-labelledby="{id}-title"
		data-own-keys
		hidden={!open}
	>
		<p id="{id}-title" class="title">About kloom</p>
		{#if loaded}
			{#await loaded}
				<p class="muted" role="status">Counting the library…</p>
			{:then s}
				<p class="headline">
					kloom's content is roughly equivalent to a <strong>{n(s.pages)}-page book</strong>.
				</p>
				<p class="muted">
					{n(s.words)} words in the narratives, at {s.wordsPerPage} words a page. Citations, scene text
					and your own notes and answers are not counted.
				</p>
				<table>
					<caption class="visually-hidden">Each subject's size</caption>
					<thead>
						<tr>
							<th scope="col">Subject</th>
							<th scope="col">Frames</th>
							<th scope="col">Trails</th>
							<th scope="col">Words</th>
							<th scope="col">Pages</th>
						</tr>
					</thead>
					<tbody>
						{#each s.subjects as subject (subject.id)}
							<tr>
								<th scope="row">
									{subject.title}{#if subject.subtitle}<span class="sub">{subject.subtitle}</span
										>{/if}
								</th>
								<td>{n(subject.frames)}</td>
								<td>{n(subject.trails)}</td>
								<td>{n(subject.words)}</td>
								<td>{n(subject.pages)}</td>
							</tr>
						{/each}
					</tbody>
				</table>
				<p class="group" id="{id}-library">In the whole library</p>
				<dl aria-labelledby="{id}-library">
					{#each counts(s) as [label, value] (label)}
						<div>
							<dt>{label}</dt>
							<dd>{n(value as number)}</dd>
						</div>
					{/each}
				</dl>
			{:catch}
				<p class="muted" role="status">The library could not be counted just now.</p>
			{/await}
		{/if}
		<p class="group">What it is</p>
		<p>
			An interactive, growable timeline for learning a subject: a spine of illustrated frames to
			scroll, a narrative to read, and an AI to question it and grow it. A proof of concept and a
			work in progress.
		</p>
		<ul class="links">
			<li>
				<a href="https://github.com/kenhia/kloom" rel="noopener noreferrer">The code, on GitHub</a>
			</li>
			<li>
				<a href="https://x.com/IterIntellectus/status/2103212539895017864" rel="noopener noreferrer"
					>What inspired it</a
				>
			</li>
		</ul>
		<p class="group">Credits</p>
		<p>
			Every frame cites its sources. Images are in the public domain or freely licensed, credited
			where they appear. The code is MIT licensed.
		</p>
		{#if build}<p class="muted build">Build {build}</p>{/if}
	</div>
</div>

<style>
	.about {
		position: relative;
	}
	.panel {
		position: absolute;
		top: calc(100% + 0.35rem);
		right: 0;
		z-index: 5;
		box-sizing: border-box;
		width: min(26rem, calc(100vw - 2rem));
		max-height: min(36rem, calc(100dvh - 5rem));
		overflow-y: auto;
		padding: 0.75rem 1rem;
		font: 0.875rem/1.45 var(--sans);
		text-align: left;
		color: var(--ink);
		background: var(--background);
		border: 1px solid var(--muted);
		border-radius: 0.25rem;
		box-shadow: 0 0.5rem 1.5rem color-mix(in srgb, #000 35%, transparent);
	}
	.panel[hidden] {
		display: none;
	}
	p {
		margin: 0 0 0.5rem;
	}
	.title,
	.group {
		font-family: var(--mono);
		font-size: 0.75rem;
		letter-spacing: 0.12em;
		text-transform: uppercase;
		color: var(--muted);
	}
	.group {
		margin-top: 0.75rem;
		padding-top: 0.5rem;
		border-top: 1px solid color-mix(in srgb, var(--muted) 40%, transparent);
	}
	.headline {
		font: 1.15rem/1.3 var(--serif);
	}
	.headline strong {
		color: var(--accent);
		font-weight: normal;
	}
	.muted {
		font-size: 0.8rem;
		color: var(--muted);
	}
	table {
		width: 100%;
		border-collapse: collapse;
		font-variant-numeric: tabular-nums;
		font-size: 0.8rem;
	}
	th,
	td {
		padding: 0.2rem 0.3rem;
		text-align: right;
		border-bottom: 1px solid color-mix(in srgb, var(--muted) 30%, transparent);
	}
	thead th {
		font-weight: normal;
		color: var(--muted);
	}
	th[scope='row'],
	thead th:first-child {
		text-align: left;
		font-weight: normal;
	}
	th .sub {
		display: block;
		font-style: italic;
		color: var(--muted);
	}
	dl {
		display: grid;
		grid-template-columns: repeat(3, 1fr);
		gap: 0.35rem 0.75rem;
		margin: 0;
	}
	dl div {
		display: flex;
		flex-direction: column-reverse;
	}
	dt {
		font-size: 0.75rem;
		color: var(--muted);
	}
	dd {
		margin: 0;
		font-size: 1rem;
		font-variant-numeric: tabular-nums;
	}
	.links {
		display: flex;
		flex-wrap: wrap;
		gap: 0.25rem 1rem;
		margin: 0 0 0.5rem;
		padding: 0;
		list-style: none;
	}
	a {
		color: inherit;
		text-decoration-color: var(--accent);
	}
	a:focus-visible {
		outline: 2px solid var(--accent);
		outline-offset: 2px;
	}
	.build {
		margin: 0.75rem 0 0;
		font-family: var(--mono);
	}
</style>

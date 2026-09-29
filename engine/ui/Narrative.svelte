<script module lang="ts">
	import type { Anchor } from '../anchor';
	import type { FrameLink, NameCard as Card } from '../graph';
	import type { Kept, Note } from '../reader-data';

	/** What the shell offers for connections and names (docs/design.md §Connections). */
	export interface LinksOffer {
		/** The reading's frame's connections, both ways. */
		connections: FrameLink[];
		/** The cards of the names this subject's readings mark. */
		names: Record<string, Card>;
		/** The subject the reader is in. */
		subject: string;
		hrefOf: (subject: string, frame: string) => string;
		/** A jump: to a frame here or in another subject, with a way back. */
		onfollow: (subject: string, frame: string) => void;
	}

	/** What the shell offers for the frame's kept answers (korg 3390). */
	export interface QaOffer {
		/** How many were kept on a frame. */
		count: (frame: string) => number;
		load: (frame: string) => Promise<Kept[] | null>;
		forget: (frame: string, id: string) => Promise<boolean>;
		titleOf: (frame: string) => string | null;
		ongoto: (frame: string) => void;
	}

	/** What the shell offers for annotations (korg 3415). */
	export interface AnnotationOffer {
		/** The annotate key as the reader has it; null when it is off. */
		key: string | null;
		/** Words were chosen: write an annotation on them. */
		onannotate: (anchor: Anchor, from: HTMLElement | null) => void;
		/** An annotation was opened from its highlight. */
		onopen: (note: Note, from: HTMLElement) => void;
	}
</script>

<script lang="ts">
	import { findQuote, moveEnd, moveStart, quoteOf, sentences, words, type Span } from '../anchor';
	import { bibliography, chicago, chicagoDate } from '../citation';
	import type { Frame, Trail } from '../model';
	import type { SyncMode } from '../navigation';
	import KeptQa from './KeptQa.svelte';
	import NameCard from './NameCard.svelte';
	import {
		clearHighlights,
		highlight,
		rangeOf,
		readingText,
		spanOf,
		type ReadingText
	} from './reading-text';

	interface Props {
		frame: Frame;
		/** The frame under the spine cursor, to say when the two differ. */
		spineFrame: Frame;
		/** Whether the reading follows the spine (a reader setting). */
		sync: SyncMode;
		/** Trails that branch from the narrative's frame. */
		trails: Trail[];
		onenter: (trail: Trail) => void;
		/** The scrolling element, so the shell can drive it from the keyboard. */
		element?: HTMLElement;
		/** The sync and trail keys as the reader has them; null when turned off. */
		keys?: { sync: string | null; trail: string | null };
		/** The reader's kept answers; absent when there is no reader. */
		qa?: QaOffer | null;
		/** The id of the tab this pane is the panel of, when it is one. */
		tab?: string | null;
		hidden?: boolean;
		/** The reader's annotations on this frame; absent when there is no reader. */
		annotating?: AnnotationOffer | null;
		annotations?: Note[];
		/** The ids of annotations whose words the reading no longer has. */
		detached?: string[];
		/** Connections and name cards; absent, names are plain words. */
		links?: LinksOffer | null;
	}

	let {
		frame,
		spineFrame,
		sync,
		trails,
		onenter,
		element = $bindable(),
		keys = { sync: 'S', trail: 'T' },
		qa = null,
		tab = null,
		hidden = false,
		annotating = null,
		annotations = [],
		detached = $bindable([]),
		links = null
	}: Props = $props();

	const behind = $derived(frame.id !== spineFrame.id);

	// A new frame starts at its top.
	$effect(() => {
		void frame.id;
		element?.scrollTo({ top: 0 });
	});

	let body = $state<HTMLElement>();

	const detachedSaid = $derived(
		detached.length === 1
			? 'One of your annotations here no longer finds its words in the reading. It is on the Notes tab, with the words it quoted.'
			: `${detached.length} of your annotations here no longer find their words in the reading. They are on the Notes tab, with the words they quoted.`
	);

	/**
	 * Annotations (docs/design.md §Annotations): each finds its words in the
	 * reading as it is now and highlights them, with a button after them that
	 * opens it. One that cannot find them is detached, and said to be.
	 */
	$effect(() => {
		void frame.readingHtml;
		const root = body;
		if (!root) return;
		choice = null;
		clearHighlights(root);
		const lost: string[] = [];
		for (const note of annotations) {
			const at = note.anchor && findQuote(readingText(root).text, note.anchor);
			const marks = at ? highlight(root, at, note.id) : [];
			if (!marks.length) {
				lost.push(note.id);
				continue;
			}
			const ref = document.createElement('button');
			ref.type = 'button';
			ref.className = 'annotation-ref';
			ref.dataset.note = note.id;
			ref.setAttribute('aria-label', `Your annotation: ${note.text.slice(0, 80)}`);
			marks.at(-1)!.after(ref);
		}
		if (lost.join() !== detached.join()) detached = lost;
	});

	// A highlight, or the button after it, opens its annotation. Not while
	// the reader is selecting words, which may start on a highlight.
	$effect(() => {
		const root = body;
		if (!root || !annotating) return;
		const offer = annotating;
		const click = (e: MouseEvent) => {
			const el = e.target instanceof Element ? e.target.closest<HTMLElement>('[data-note]') : null;
			if (!el || !getSelection()?.isCollapsed) return;
			const note = annotations.find((n) => n.id === el.dataset.note);
			const ref = root.querySelector<HTMLElement>(
				`.annotation-ref[data-note="${CSS.escape(el.dataset.note ?? '')}"]`
			);
			if (note) offer.onopen(note, ref ?? el);
		};
		root.addEventListener('click', click);
		return () => root.removeEventListener('click', click);
	});

	/**
	 * A name's card (§Connections), open beside its mark. A mark is a button
	 * in the reading, so Enter and Space open it as a click does.
	 */
	let naming = $state<{
		id: string;
		label: string;
		button: HTMLElement;
		top: number;
		left: number;
	} | null>(null);
	$effect(() => {
		void frame.id;
		naming = null;
	});
	$effect(() => {
		const root = body;
		if (!root || !links) return;
		const click = (e: MouseEvent) => {
			const button =
				e.target instanceof Element ? e.target.closest<HTMLElement>('button.name') : null;
			if (!button || !element) return;
			if (naming?.button === button) return closeName(false);
			const at = button.getBoundingClientRect();
			const box = element.getBoundingClientRect();
			naming?.button.setAttribute('aria-expanded', 'false');
			button.setAttribute('aria-expanded', 'true');
			naming = {
				id: button.dataset.name ?? '',
				label: button.textContent ?? '',
				button,
				top: at.bottom - box.top + element.scrollTop + 4,
				left: Math.max(0, Math.min(at.left - box.left, box.width - 22 * 16 - 32))
			};
		};
		root.addEventListener('click', click);
		return () => root.removeEventListener('click', click);
	});

	function closeName(refocus: boolean) {
		const button = naming?.button;
		button?.setAttribute('aria-expanded', 'false');
		naming = null;
		if (refocus) button?.focus();
	}

	function follow(e: MouseEvent, c: FrameLink) {
		if (!links || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
		e.preventDefault();
		links.onfollow(c.subject, c.frame);
	}

	/** Move focus to an annotation's button in the reading; false when it is detached. */
	export function show(id: string): boolean {
		const ref = body?.querySelector<HTMLElement>(`.annotation-ref[data-note="${CSS.escape(id)}"]`);
		ref?.scrollIntoView({ block: 'center' });
		ref?.focus();
		return !!ref;
	}

	/**
	 * Words being chosen with the keyboard: a sentence to start with, then
	 * moved by sentence and trimmed by word. The choice is the page's real
	 * selection, so it looks and reads like one.
	 */
	let choice = $state<{ t: ReadingText; sentences: Span[]; words: Span[]; span: Span } | null>(
		null
	);
	let chosen = $state('');

	/**
	 * Annotate (the A key, or the button): the words selected in the reading
	 * if there are some, else choose them with the keyboard.
	 */
	export function annotate(from: HTMLElement | null) {
		if (!body || !element || !annotating) return;
		const sel = getSelection();
		if (sel && !sel.isCollapsed && sel.rangeCount && sel.getRangeAt(0).intersectsNode(body)) {
			const t = readingText(body);
			const span = spanOf(t, sel.getRangeAt(0));
			const anchor = span && quoteOf(t.text, span.start, span.end);
			if (anchor) {
				sel.removeAllRanges();
				choice = null;
				annotating.onannotate(anchor, from);
				return;
			}
		}
		const t = readingText(body);
		const all = sentences(t.text, t.blocks);
		if (!all.length) return;
		// The first sentence in view, so the reader starts where they are reading.
		const top = element.getBoundingClientRect().top;
		const first = all.find((s) => (rangeOf(t, s)?.getBoundingClientRect().bottom ?? 0) > top);
		choice = { t, sentences: all, words: words(t.text), span: first ?? all[0] };
		element.focus();
		select();
	}

	/** Show the choice as the selection, in view, and say it. */
	function select() {
		if (!choice) return;
		const range = rangeOf(choice.t, choice.span);
		const sel = getSelection();
		if (!range || !sel) return;
		sel.removeAllRanges();
		sel.addRange(range);
		range.startContainer.parentElement?.scrollIntoView({ block: 'nearest' });
		chosen = `“${choice.t.text.slice(choice.span.start, choice.span.end).replace(/\s+/g, ' ')}”`;
	}

	function stopChoosing() {
		choice = null;
		chosen = '';
		getSelection()?.removeAllRanges();
	}

	/** Keys while choosing: the reading's own, so the page's stand down. */
	function chooseKey(e: KeyboardEvent) {
		if (!choice || e.altKey || e.ctrlKey || e.metaKey) return;
		const { span, sentences: all, words: ws } = choice;
		switch (e.key) {
			case 'ArrowDown':
				choice.span = all.find((s) => s.start >= span.end) ?? span;
				break;
			case 'ArrowUp':
				choice.span = all.findLast((s) => s.end <= span.start) ?? span;
				break;
			case 'ArrowLeft':
				choice.span = e.shiftKey ? moveEnd(ws, span, -1) : moveStart(ws, span, -1);
				break;
			case 'ArrowRight':
				choice.span = e.shiftKey ? moveEnd(ws, span, 1) : moveStart(ws, span, 1);
				break;
			case 'Enter':
				annotate(element ?? null);
				break;
			case 'Escape':
				stopChoosing();
				break;
			default:
				return;
		}
		e.preventDefault();
		if (choice) select();
	}
</script>

<section
	id="narrative-panel"
	class="narrative"
	aria-label="Narrative"
	role={tab ? 'tabpanel' : undefined}
	{hidden}
>
	<div class="controls">
		<p id="sync-state" class="state" aria-live="polite">
			{#if behind}
				Showing {frame.position.label}; the spine is at {spineFrame.position.label}.
				{#if keys.sync}<kbd>{keys.sync}</kbd> brings the reading here.{/if}
			{:else if sync === 'follow'}
				Following the spine.
			{:else}
				In step with the spine.
			{/if}
		</p>
		{#if annotating}
			<!-- Pressing it must not take the selection it is about to use. -->
			<button
				type="button"
				class="annotate"
				aria-describedby="annotate-how"
				onmousedown={(e) => e.preventDefault()}
				onclick={(e) => annotate(e.currentTarget)}
				>Annotate {#if annotating.key}<kbd>{annotating.key}</kbd>{/if}</button
			>
			<span id="annotate-how" class="visually-hidden"
				>Annotates the words selected in the reading, or lets you choose them with the keyboard.</span
			>
		{/if}
		{#if choice}
			<p id="choosing" class="choosing">
				Choosing words: <kbd>↑</kbd><kbd>↓</kbd> sentence · <kbd>←</kbd><kbd>→</kbd> start ·
				<kbd>Shift</kbd> <kbd>←</kbd><kbd>→</kbd> end · <kbd>Enter</kbd> annotate ·
				<kbd>Esc</kbd> cancel
			</p>
		{/if}
		<p class="visually-hidden" role="status">{chosen}</p>
	</div>

	<!-- Focusable because it scrolls: keyboard users must be able to reach it.
	     Its keys are its own only while words are being chosen in it. -->
	<!-- svelte-ignore a11y_no_noninteractive_tabindex, a11y_no_noninteractive_element_interactions -->
	<article
		class="reading"
		tabindex="0"
		aria-labelledby="reading-title"
		aria-describedby={choice ? 'choosing' : undefined}
		bind:this={element}
		onkeydown={chooseKey}
		onfocusout={(e) => {
			if (choice && !element?.contains(e.relatedTarget as Node | null)) stopChoosing();
		}}
	>
		<p class="position">
			{frame.position.label}
			{#if frame.asOf}<span class="as-of">· As of {chicagoDate(frame.asOf)}</span>{/if}
		</p>
		<h2 id="reading-title">{frame.scene.headline} <em>{frame.scene.accent}</em></h2>

		<div class="body" bind:this={body}>
			<!-- Rendered on load with raw HTML escaped and unsafe links dropped. -->
			<!-- eslint-disable-next-line svelte/no-at-html-tags -->
			{@html frame.readingHtml}
		</div>

		{#if detached.length}
			<p class="detached">{detachedSaid}</p>
		{/if}

		{#if trails.length}
			<h3>Trails from here</h3>
			<ul class="trails">
				{#each trails as trail (trail.id)}
					<li>
						<button type="button" onclick={() => onenter(trail)}
							>{trail.title}
							{#if keys.trail}<kbd>{keys.trail}</kbd>{/if}</button
						>
					</li>
				{/each}
			</ul>
		{/if}

		{#if links?.connections.length}
			<h3>Connections</h3>
			<ul class="connections">
				{#each links.connections as c (`${c.direction} ${c.subject}/${c.frame}`)}
					<li>
						{#if c.detached}
							<span class="to">{c.subject}/{c.frame}</span>
							<span class="context">Not found: the frame is not served, or has moved.</span>
						{:else}
							<!-- The page resolved this app route. A connection stored on the
							     other frame says so to a screen reader. -->
							<!-- eslint-disable svelte/no-navigation-without-resolve -->
							<a
								class="to"
								href={links.hrefOf(c.subject, c.frame)}
								aria-label={c.direction === 'in' ? `From ${c.title}` : undefined}
								onclick={(e) => follow(e, c)}>{c.title}</a
							>
							<!-- eslint-enable svelte/no-navigation-without-resolve -->
							<span class="context"
								>{c.subject === links.subject ? '' : `${c.subjectTitle} · `}{c.label}{c.trail
									? ` · ${c.trail}`
									: ''}</span
							>
						{/if}
						<span class="why">{c.why}</span>
					</li>
				{/each}
			</ul>
		{/if}

		{#if qa && qa.count(frame.id) > 0}
			<!-- Remounted when the count changes, so a new kept answer is fetched. -->
			{#key `${frame.id}:${qa.count(frame.id)}`}
				<KeptQa
					count={qa.count(frame.id)}
					citations={frame.citations?.length ?? 0}
					load={() => qa.load(frame.id)}
					onforget={(id) => qa.forget(frame.id, id)}
					titleOf={qa.titleOf}
					ongoto={qa.ongoto}
				/>
			{/key}
		{/if}

		<h3>Sources</h3>
		<ol class="sources">
			{#each frame.sources as source, i (i)}
				<li>
					{#if source.url}
						<!-- An external source, not an app route. -->
						<!-- eslint-disable-next-line svelte/no-navigation-without-resolve -->
						<a href={source.url} rel="noopener noreferrer">{source.title}</a>
					{:else}
						{source.title}
					{/if}
					{#if source.note}<span class="note">— {source.note}</span>{/if}
				</li>
			{/each}
		</ol>

		{#if naming && links}
			<!-- Each opening is its own card: it takes focus, and keeps its name. -->
			{#key naming}
				<NameCard
					card={links.names[naming.id] ?? null}
					label={naming.label}
					anchor={naming.button}
					top={naming.top}
					left={naming.left}
					here={{ subject: links.subject, frame: frame.id }}
					hrefOf={links.hrefOf}
					onfollow={links.onfollow}
					onclose={closeName}
				/>
			{/key}
		{/if}

		{#if frame.citations?.length}
			<details class="citations">
				<summary>Citations ({frame.citations.length})</summary>
				<ul>
					{#each bibliography(frame.citations) as citation, i (i)}
						<li>
							{#each chicago(citation) as part, j (j)}
								{#if part.href}
									<!-- An external source, not an app route. -->
									<!-- eslint-disable-next-line svelte/no-navigation-without-resolve -->
									<a href={part.href} rel="noopener noreferrer">{part.text}</a>
								{:else if part.italic}<i>{part.text}</i>{:else}{part.text}{/if}
							{/each}
						</li>
					{/each}
				</ul>
			</details>
		{/if}
	</article>
</section>

<style>
	.narrative[hidden] {
		display: none;
	}
	.narrative {
		display: grid;
		grid-template-rows: auto minmax(0, 1fr);
		min-height: 0;
		border-left: 1px solid color-mix(in srgb, var(--muted) 40%, transparent);
	}

	.controls {
		display: flex;
		flex-wrap: wrap;
		align-items: center;
		gap: 0.5rem 1rem;
		padding: 0.75rem 1.5rem;
		border-bottom: 1px solid color-mix(in srgb, var(--muted) 40%, transparent);
		font-size: 0.875rem;
	}
	.annotate {
		font: inherit;
		font-size: 0.8rem;
		padding: 0.2rem 0.7rem;
		color: var(--ink);
		background: none;
		border: 1px solid var(--muted);
		border-radius: 0.25rem;
		cursor: pointer;
	}
	.choosing {
		flex-basis: 100%;
		margin: 0;
		font-size: 0.75rem;
		color: var(--ink);
	}
	.detached {
		margin: 1.25rem 0 0;
		font-size: 0.8rem;
		color: var(--muted);
	}
	.body :global(mark.annotation) {
		color: inherit;
		background: color-mix(in srgb, var(--accent) 28%, transparent);
		border-bottom: 1px solid var(--accent);
		cursor: pointer;
	}
	.body :global(.annotation-ref) {
		font: inherit;
		font-size: 0.75em;
		vertical-align: super;
		line-height: 1;
		margin: 0 0 0 0.1em;
		padding: 0 0.15em;
		color: var(--accent);
		background: none;
		border: 0;
		cursor: pointer;
	}
	.body :global(.annotation-ref)::after {
		content: '✎' / '';
	}
	.state {
		flex: 1;
		margin: 0;
		color: var(--muted);
		font-size: 0.8rem;
	}

	.reading {
		position: relative;
		overflow-y: auto;
		overscroll-behavior: contain;
		padding: 1.25rem 1.5rem 2rem;
		line-height: 1.6;
	}
	.position {
		margin: 0;
		font-family: var(--mono);
		font-size: 0.75rem;
		letter-spacing: 0.12em;
		text-transform: uppercase;
		color: var(--muted);
	}
	h2 {
		margin: 0.25rem 0 1rem;
		font-family: var(--serif);
		font-size: 1.75rem;
		font-weight: normal;
		text-transform: uppercase;
	}
	h2 em {
		font-style: normal;
		color: var(--accent);
	}
	h3 {
		margin: 1.75rem 0 0.5rem;
		font-family: var(--mono);
		font-size: 0.75rem;
		font-weight: normal;
		letter-spacing: 0.12em;
		text-transform: uppercase;
		color: var(--muted);
	}
	.body :global(a),
	.sources a {
		color: inherit;
		text-decoration-color: var(--accent);
	}
	.body :global(h3) {
		margin: 1.75rem 0 0.5rem;
		font-family: var(--serif);
		font-size: 1.25rem;
		font-weight: normal;
	}
	.body :global(img) {
		display: block;
		max-width: 100%;
		height: auto;
		margin: 1rem auto 0.25rem;
	}
	.body :global(.figure) {
		display: block;
	}
	/* An inlined chart draws in currentColor and names its palette hooks, so
	   it follows the reader's palette mode and fades with the page. */
	.body :global(.chart svg) {
		display: block;
		max-width: 100%;
		height: auto;
		margin: 1rem auto 0.25rem;
		color: var(--ink);
	}
	.body :global(.chart .muted) {
		color: var(--muted);
	}
	.body :global(.chart .accent) {
		color: var(--accent);
	}
	.body :global(.credit) {
		display: block;
		font-size: 0.75rem;
		text-align: center;
		color: var(--muted);
	}
	.body :global(table) {
		border-collapse: collapse;
		font-size: 0.875rem;
		margin: 0.5rem 0 1rem;
	}
	.body :global(th),
	.body :global(td) {
		padding: 0.2rem 0.75rem 0.2rem 0;
		border-bottom: 1px solid color-mix(in srgb, var(--muted) 40%, transparent);
		text-align: left;
	}
	.body :global(td:last-child),
	.body :global(th:last-child) {
		text-align: right;
		font-variant-numeric: tabular-nums;
	}
	.body :global(blockquote) {
		margin: 1rem 0;
		padding-left: 1rem;
		border-left: 2px solid var(--accent);
		font-family: var(--serif);
		font-style: italic;
	}
	.citations {
		margin-top: 0.75rem;
		font-size: 0.8rem;
	}
	.citations summary {
		cursor: pointer;
		width: fit-content;
		font-family: var(--mono);
		letter-spacing: 0.08em;
		text-transform: uppercase;
		color: var(--muted);
	}
	.citations ul {
		padding-left: 1.25rem;
	}
	.citations li {
		margin-bottom: 0.4rem;
		padding-left: 1.5em;
		text-indent: -1.5em;
		list-style: none;
		overflow-wrap: anywhere;
	}
	.citations a {
		color: inherit;
		text-decoration-color: var(--accent);
	}
	/* A name's mark: its own words, underlined in the accent, a button. */
	.body :global(button.name) {
		font: inherit;
		line-height: inherit;
		padding: 0;
		color: inherit;
		background: none;
		border: 0;
		border-bottom: 1px dotted var(--accent);
		cursor: pointer;
	}
	.body :global(button.name:hover),
	.body :global(button.name[aria-expanded='true']) {
		border-bottom-style: solid;
		color: var(--accent);
	}
	.connections {
		display: grid;
		gap: 0.6rem;
		margin: 0;
		padding: 0;
		list-style: none;
		font-size: 0.9rem;
	}
	.connections li {
		display: grid;
	}
	.connections .to {
		color: var(--ink);
		text-decoration-color: var(--accent);
	}
	.connections .context {
		font-size: 0.75rem;
		color: var(--muted);
	}
	.connections .why {
		font-size: 0.85rem;
	}
	.trails {
		margin: 0;
		padding: 0;
		list-style: none;
	}
	.trails button {
		font: inherit;
		color: var(--ink);
		background: none;
		border: 1px dashed var(--accent);
		border-radius: 0.25rem;
		padding: 0.35rem 0.75rem;
		cursor: pointer;
	}
	.sources {
		padding-left: 1.25rem;
		font-size: 0.875rem;
	}
	.note {
		color: var(--muted);
	}
	kbd {
		font-family: var(--mono);
		font-size: 0.7rem;
		padding: 0 0.3rem;
		border: 1px solid var(--muted);
		border-radius: 0.2rem;
		color: var(--muted);
	}
</style>

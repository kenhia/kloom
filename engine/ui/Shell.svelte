<script lang="ts">
	import { onMount, tick, untrack } from 'svelte';
	import type { AiOffer } from '../ai/provider';
	import type { Anchor } from '../anchor';
	import type { Frame, FrameHead, SubjectHead, Trail } from '../model';
	import type { MyNotesOffer } from '../my-notes';
	import type { JumpItem, Note, ReaderLayer } from '../reader-data';
	import { contentsOf, openTrails } from '../contents';
	import { clamp, indexLabel, stops, WheelGate, type BackStop, type SyncMode } from '../navigation';
	import { AHEAD, PENDING, type ServedBody } from '../served';
	import { keyName, modified, onMac, pageKey, SHORTCUTS, tabKey, type Binding } from '../keys';
	import { marksText, type FrameMarks } from '../marks';
	import {
		bounds,
		defaultPanes,
		panesFor,
		readPanes,
		resize,
		writePanes,
		type Divider,
		type SavedPanes
	} from '../panes';
	import {
		browserStorage,
		coloursOf,
		followSpine,
		framePalettes,
		layout,
		sectionPalette,
		type Layout
	} from '../settings';
	import type { UserSettings } from '../user-settings.svelte';
	import AiPane from './AiPane.svelte';
	import Bookmarks from './Bookmarks.svelte';
	import MyNotes from './MyNotes.svelte';
	import Contents from './Contents.svelte';
	import type { MapOpen } from './MapOverlay.svelte';
	import BackChip from './BackChip.svelte';
	import Narrative, {
		type AnnotationOffer,
		type LinksOffer,
		type QaOffer
	} from './Narrative.svelte';
	import NoteEditor from './NoteEditor.svelte';
	import Notes from './Notes.svelte';
	import Settings from './Settings.svelte';
	import IconButton from './IconButton.svelte';
	import homeIcon from './icons/home.svg?raw';
	import SpinePane from './SpinePane.svelte';
	import Splitter from './Splitter.svelte';

	interface Props {
		/** Every frame's head (docs/design.md §Serving). */
		subject: SubjectHead;
		/**
		 * The frame bodies the page has fetched, by frame id. A frame whose
		 * body has not arrived shows its head, and its reading says it is coming.
		 */
		bodies?: Record<string, ServedBody>;
		/** The frames the shell is about to show, nearest first: the page fetches those it lacks. */
		onneed?: (ids: string[]) => void;
		/** The reader's settings; the page makes them and loads them on mount. */
		settings: UserSettings;
		/**
		 * What the app config offers the AI pane; null for no AI pane at all
		 * (the reader edition, korg 3500): no AI tab, no kept answers.
		 */
		ai?: AiOffer | null;
		/** A grow job finished: the page reloads the subject from disk. */
		ongrown?: () => void;
		/** False while something (the start screen) sits in front of the shell. */
		active?: boolean;
		/** The frame to open on (a deep link); the first frame when absent. */
		startAt?: string | null;
		/** The frame on the spine changed: the page records the reader's place. */
		onplace?: (frame: FrameHead) => void;
		/** The reader's bookmarks; absent when there is no reader to keep them for. */
		bookmarks?: BookmarkOffer | null;
		/** The reader's notes and kept answers; absent when there is no reader. */
		layer?: ReaderLayer | null;
		/** Every note across subjects (§My notes); absent when there is no reader. */
		myNotes?: MyNotesOffer | null;
		/** Back to the start screen (the Home button, left of the gear); none without it. */
		onhome?: () => void;
		/** A frame's own address, for the contents' links; the page resolves it. */
		hrefOf?: (frame: string) => string;
		/** Any frame's address, in any subject; the page resolves it. */
		hrefTo?: (subject: string, frame: string) => string;
		/** A jump to a frame, here or in another subject: the page navigates, with a way back. */
		onfollow?: (subject: string, frame: string) => void;
		/** Where the last jump left from, and how many are stacked; null when there is none. */
		back?: { to: BackStop; depth: number; onback: () => void } | null;
		/** Open the map on a frame's neighbourhood (§The map); none without it. */
		onmap?: (open: MapOpen) => void;
		/**
		 * Jump to a random frame (§Random): in this subject, or anywhere in the
		 * library, never this one. False when there was nowhere to go.
		 */
		onrandom?: (scope: RandomScope) => Promise<boolean>;
	}

	/** Where a random jump may land. */
	type RandomScope = 'subject' | 'library';

	/** What the page offers for bookmarks: the frames marked, the jump list, and the writes. */
	interface BookmarkOffer {
		/** Frame ids in this subject the reader has bookmarked. */
		marked: Set<string>;
		items: JumpItem[];
		exportHref?: string;
		ontoggle: (frame: FrameHead) => void;
		onremove: (item: JumpItem) => void;
	}

	let {
		subject,
		bodies = {},
		onneed,
		settings,
		ai = { web: 'deny' },
		ongrown,
		active = true,
		startAt = null,
		onplace,
		bookmarks = null,
		layer = null,
		myNotes = null,
		onhome,
		hrefOf,
		hrefTo,
		onfollow,
		back = null,
		onmap,
		onrandom
	}: Props = $props();

	let trailId = $state<string | null>(null);
	let index = $state(0);
	/** What the narrative shows when it does not follow the spine. */
	let pinned = $state<string | null>(null);

	/** Said once when a bookmark is made or removed, so a B press is heard. */
	let markNote = $state('');

	/**
	 * The right-hand pane's tabs (§Layout): Narrative, then Notes when there is
	 * a reader to keep them for, then AI in the tabs layout.
	 */
	type Tab = 'narrative' | 'notes' | 'ai';
	let tab = $state<Tab>('narrative');
	const tabEls = $state<HTMLButtonElement[]>([]);
	/** What the AI pane reports for its tab: working, or a result not yet seen. */
	let aiActivity = $state<'idle' | 'working' | 'ready'>('idle');

	let narrativeEl = $state<HTMLElement>();
	let narrative = $state<ReturnType<typeof Narrative>>();
	/** Annotations on the reading's frame that no longer find their words. */
	let detached = $state<string[]>([]);
	let slider = $state<HTMLElement>();

	const trail = $derived(trailId ? (subject.trails.find((t) => t.id === trailId) ?? null) : null);
	const path = $derived(stops(trail ? trail.spine : subject.spine));
	const stop = $derived(path[clamp(index, path.length)]);
	/** A frame whole: its head, and its body or, until that arrives, an empty one. */
	const whole = (
		head: FrameHead,
		body: ServedBody | undefined
	): Frame & Pick<ServedBody, 'links'> => ({
		...head,
		...(body ?? PENDING)
	});
	const spineBody = $derived(bodies[stop.frameId]);
	const frame = $derived(whole(subject.frames[stop.frameId], spineBody));
	/** A reader setting (§Interaction): the narrative follows the spine unless they said not to. */
	const sync = $derived<SyncMode>(settings.get(followSpine.id) === 'manual' ? 'manual' : 'follow');
	/**
	 * Whether there is an AI pane. The reader edition's build has none
	 * (`__KLOOM_EDITION__`), so the pane's code is not in it at all.
	 */
	const hasAi = $derived(__KLOOM_EDITION__ !== 'reader' && ai !== null);
	// With no AI pane, the layout is two panes and the setting does not apply.
	const shape = $derived((hasAi ? (settings.get(layout.id) ?? layout.default) : 'tabs') as Layout);
	const tabbed = $derived(shape === 'tabs');
	const tabs = $derived<Tab[]>([
		...(layer || tabbed ? ['narrative' as const] : []),
		...(layer ? ['notes' as const] : []),
		...(tabbed && hasAi ? ['ai' as const] : [])
	]);
	// A tab that went away (the layout changed) hands back to the narrative.
	$effect(() => {
		if (!tabs.includes(tab)) tab = 'narrative';
	});
	const TAB_LABEL: Record<Tab, string> = { narrative: 'Narrative', notes: 'Notes', ai: 'AI' };
	const TAB_PANEL: Record<Tab, string> = {
		narrative: 'narrative-panel',
		notes: 'notes-panel',
		ai: 'ai-results'
	};

	/** The reader's keys (korg 3363, 3493): their binding for each shortcut, or none. */
	const keys = $derived(settings.keys.map);
	const shown = (k: Binding | null) => (k ? keyName(k, onMac()) : null);
	// Pane sizes (§Layout): dragged at the dividers, remembered per layout.
	let saved = $state<SavedPanes>({});
	let panesEl = $state<HTMLElement>();
	let tabRowEl = $state<HTMLElement>();
	onMount(() => (saved = readPanes(browserStorage())));
	const panes = $derived(panesFor(saved, shape));
	const fr = (...parts: number[]) => parts.map((p) => `minmax(0, ${p}fr)`).join(' ');
	const cols = $derived(
		shape === 'columns'
			? fr(panes.spine, 1 - panes.spine - panes.ai, panes.ai)
			: fr(panes.spine, 1 - panes.spine)
	);
	const rows = $derived(shape === 'split' ? fr(panes.upper, 1 - panes.upper) : null);
	const setPane = (d: Divider, v: number) =>
		(saved = writePanes(saved, shape, resize(panes, shape, d, v), browserStorage()));
	const resetPane = (d: Divider) => setPane(d, defaultPanes(shape)[d]);
	/** Where the pointer is, as the share a divider asks for. */
	function pointerAt(d: Divider, e: PointerEvent) {
		const r = panesEl!.getBoundingClientRect();
		if (d === 'spine') return (e.clientX - r.left) / r.width;
		if (d === 'ai') return (r.right - e.clientX) / r.width;
		// The split's rows start under the tab row.
		const top = tabRowEl?.getBoundingClientRect().bottom ?? r.top;
		return (e.clientY - top) / (r.bottom - top);
	}
	/** The dividers this layout has. */
	const dividers = $derived<{ id: Divider; label: string; controls: string }[]>([
		{ id: 'spine', label: 'Resize the spine', controls: 'spine-pane' },
		...(shape === 'columns'
			? [{ id: 'ai' as const, label: 'Resize the AI pane', controls: 'ai-pane' }]
			: []),
		...(shape === 'split'
			? [{ id: 'upper' as const, label: 'Resize the narrative', controls: 'narrative-panel' }]
			: [])
	]);
	/**
	 * The scene's colours and the reading's (docs/design.md §Colours, korg
	 * 3495), worked out from the frame on the spine. The scene pane wears the
	 * first; the shell, and so the reading, the notes, the AI pane, the tab row
	 * and the hint line, wears the second.
	 */
	const palettes = $derived(
		framePalettes(
			subject,
			frame.scene.palette,
			sectionPalette(subject, stop.segment),
			coloursOf(settings)
		)
	);
	const palette = $derived(palettes.reading);
	const narrativeId = $derived(
		sync === 'follow' || !pinned || !subject.frames[pinned] ? stop.frameId : pinned
	);
	const narrativeBody = $derived(bodies[narrativeId]);
	const narrativeFrame = $derived(whole(subject.frames[narrativeId], narrativeBody));
	/** The narrative's frame has no body yet: its reading is on its way. */
	const pending = $derived(!narrativeBody);
	// The frames about to be shown, nearest first: the spine's, its
	// neighbours either side, and the narrative's (§Serving).
	$effect(() => {
		const ids = [stop.frameId];
		for (let d = 1; d <= AHEAD; d++)
			for (const i of [index + d, index - d])
				if (i >= 0 && i < path.length) ids.push(path[i].frameId);
		ids.push(narrativeId);
		// Read here, so bodies that go away (a new build) are asked for again.
		const missing = ids.filter((id) => !bodies[id]);
		if (missing.length) untrack(() => onneed?.(missing));
	});
	const trailsFrom = (id: string) => subject.trails.filter((t) => t.anchor === id);
	/** The table of contents (§Contents, korg 3433): rebuilt when a grow adds frames. */
	const contents = $derived(contentsOf(subject));
	let contentsEl = $state<ReturnType<typeof Contents>>();
	let mapButton = $state<IconButton>();
	/** The map (§The map): opened on the frame on the spine, focus back to its button. */
	function openMap() {
		const key = `${subject.id}/${frame.id}`;
		onmap?.({
			target: { view: 'frame', key, steps: 2 },
			scheme: palettes.scene.scheme,
			here: key,
			refocus: () => mapButton?.focus()
		});
	}
	const branches = $derived(new Set(trail ? [] : subject.trails.map((t) => t.anchor)));
	const marked = $derived(bookmarks?.marked ?? new Set<string>());
	/** Notes per frame, for the marks and the tab. */
	const noteCounts = $derived(
		(layer?.notes ?? []).reduce<Record<string, number>>((c, n) => {
			c[n.frame] = (c[n.frame] ?? 0) + 1;
			return c;
		}, {})
	);
	const marksOf = (id: string): FrameMarks => ({
		bookmarked: marked.has(id),
		kept: layer?.kept[id] ?? 0,
		notes: noteCounts[id] ?? 0
	});
	const titleOf = (f: FrameHead) => `${f.scene.headline} ${f.scene.accent}`;
	const announcement = $derived.by(() => {
		const said = marksText(marksOf(frame.id));
		const tail = said.length ? ` ${said.join(', ')}.`.replace(/ (\w)/, (m) => m.toUpperCase()) : '';
		return `${indexLabel(index, path.length)}, ${stop.segment.title}, ${frame.position.label}: ${titleOf(frame)}${tail}`;
	});

	/**
	 * A note being written (docs/design.md §Notes, korg 3409). While there is
	 * one, the scene is its editor. It stays on the frame it was started on.
	 */
	interface Draft {
		id?: string;
		frame: FrameHead;
		text: string;
		flag: boolean;
		/** The words it is on, for an annotation (§Annotations). */
		anchor: Anchor | null;
		/** What it was when the editor opened: anything else is unsaved. */
		was: { text: string; flag: boolean };
		/** Where focus goes back to when the editor closes. */
		from: HTMLElement | null;
	}
	let draft = $state<Draft | null>(null);
	let saving = $state(false);
	let saveError = $state('');
	const dirty = $derived(
		!!draft && (draft.text !== draft.was.text || draft.flag !== draft.was.flag)
	);
	const frameNotes = $derived((layer?.notes ?? []).filter((n) => n.frame === narrativeFrame.id));

	/** Whether a note has changes not saved yet; the page asks before it navigates. */
	export const hasUnsavedNote = () => dirty;
	/** Close the editor without saving: the page already asked. */
	export function discardNote() {
		draft = null;
	}

	/**
	 * Leaving the frame closes the editor. With unsaved changes, the reader is
	 * asked first; false when they chose to stay.
	 */
	function mayLeave(): boolean {
		if (!draft) return true;
		if (dirty && !confirm('This note has changes that are not saved. Discard them?')) return false;
		draft = null;
		saveError = '';
		return true;
	}

	const focused = () =>
		document.activeElement instanceof HTMLElement ? document.activeElement : null;

	function startNote(from: HTMLElement | null = focused()) {
		if (!layer) return;
		if (draft && !draft.id) return; // already writing a new one: the editor has focus
		if (!mayLeave()) return;
		draft = {
			frame: narrativeFrame,
			text: '',
			flag: false,
			anchor: null,
			was: { text: '', flag: false },
			from
		};
	}

	/** Write an annotation on words the reader chose in the reading (korg 3415). */
	function startAnnotation(anchor: Anchor, from: HTMLElement | null) {
		if (!layer || !mayLeave()) return;
		draft = {
			frame: narrativeFrame,
			text: '',
			flag: false,
			anchor,
			was: { text: '', flag: false },
			from
		};
	}

	/** Annotate: the narrative's words, so it comes forward first. */
	async function annotate(from: HTMLElement | null = focused()) {
		if (!layer) return;
		tab = 'narrative';
		await tick();
		narrative?.annotate(from);
	}

	let myNotesEl = $state<ReturnType<typeof MyNotes>>();

	/**
	 * Open the Notes tab on one of its notes (My notes' Go to): the shell has
	 * moved to its frame already. Focus lands on the note, or the spine.
	 */
	export async function showNote(id: string) {
		if (!layer) return slider?.focus();
		tab = 'notes';
		await tick();
		const el = document.getElementById(`note-${id}`);
		el?.scrollIntoView({ block: 'nearest' });
		(el ?? slider)?.focus();
	}

	// An agent's answer on the Notes tab has been seen (§My notes): the count clears.
	$effect(() => {
		if (tab !== 'notes' || !layer) return;
		const waiting = frameNotes.filter((n) => n.unseen).map((n) => n.id);
		if (waiting.length) untrack(() => layer.seen(waiting));
	});

	async function showAnnotation(note: Note) {
		tab = 'narrative';
		await tick();
		narrative?.show(note.id);
	}

	const annotating = $derived<AnnotationOffer | null>(
		layer
			? {
					key: shown(keys.annotate),
					onannotate: startAnnotation,
					onopen: (note, from) => editNote(note, from)
				}
			: null
	);

	function editNote(note: Note, from: HTMLElement) {
		if (draft?.id === note.id || !mayLeave()) return;
		const frame = subject.frames[note.frame] ?? narrativeFrame;
		draft = {
			id: note.id,
			frame,
			text: note.text,
			flag: note.review === 'flagged',
			anchor: note.anchor,
			was: { text: note.text, flag: note.review === 'flagged' },
			from
		};
	}

	function closeEditor(back = draft?.from) {
		draft = null;
		saveError = '';
		(back?.isConnected ? back : slider)?.focus();
	}

	async function saveNote() {
		if (!draft || !layer || saving || !draft.text.trim()) return;
		saving = true;
		const d = draft;
		const saved = await layer.saveNote({
			...(d.id ? { id: d.id } : {}),
			frame: d.frame.id,
			label: titleOf(d.frame),
			text: d.text,
			flag: d.flag,
			...(d.id ? {} : { anchor: d.anchor })
		});
		saving = false;
		if (draft !== d) return;
		if (!saved) {
			saveError = 'Could not save the note. Your text is still here; try again.';
			return;
		}
		markNote = `${d.anchor ? 'Annotation' : 'Note'} saved on ${titleOf(d.frame)}.`;
		closeEditor();
	}

	function cancelNote() {
		// Read first: leaving clears the draft, and with it where to go back to.
		const back = draft?.from;
		if (mayLeave()) closeEditor(back);
	}

	async function deleteNote(note: Note) {
		const what = note.anchor ? 'annotation' : 'note';
		if (!layer || !confirm(`Delete this ${what}? This cannot be undone.`)) return;
		if (draft?.id === note.id) draft = null;
		markNote = (await layer.deleteNote(note.id))
			? `${what[0].toUpperCase()}${what.slice(1)} deleted.`
			: `Could not delete the ${what}.`;
	}

	/** The shortcuts the help bar names: the reader's keys, for what this page can do. */
	const hints = $derived(
		SHORTCUTS.filter(
			(s) =>
				keys[s.action] &&
				(s.action !== 'bookmark' || bookmarks) &&
				((s.action !== 'note' && s.action !== 'annotate') || layer) &&
				(s.action !== 'my-notes' || myNotes) &&
				(s.action !== 'back' || back) &&
				(s.action !== 'map' || onmap) &&
				((s.action !== 'random' && s.action !== 'anywhere') || onrandom)
		).map((s) => ({
			action: s.action,
			/** Alt, Ctrl or Meta held: it acts anywhere, not only in the panes (WCAG 2.1.4). */
			anywhere: modified(keys[s.action]!),
			key: shown(keys[s.action])!,
			label: {
				sync: 'sync',
				trail: 'trail',
				bookmark: 'bookmark',
				note: 'note',
				annotate: 'annotate',
				'my-notes': 'my notes',
				contents: 'contents',
				back: 'back',
				map: 'map',
				random: 'random',
				anywhere: 'anywhere'
			}[s.action]
		}))
	);

	/** The hints in two runs, the scoped ones and those that act anywhere, each with its joins. */
	const hintRuns = $derived(
		[hints.filter((h) => !h.anywhere), hints.filter((h) => h.anywhere)].map((run) =>
			run.map((h, i) => ({
				...h,
				/** What comes before it: nothing, a comma, or "and" before the last. */
				lead: i === 0 ? '' : i === run.length - 1 ? ' and ' : ', '
			}))
		)
	);

	const linksOffer = $derived<LinksOffer | null>(
		hrefTo && onfollow
			? {
					connections: narrativeFrame.links.connections,
					names: narrativeFrame.links.names,
					subject: subject.id,
					hrefOf: hrefTo,
					onfollow,
					onmap: onmap
						? (name: string, refocus: () => void) =>
								onmap({
									target: { view: 'name', id: name },
									scheme: palette.scheme,
									here: `${subject.id}/${frame.id}`,
									refocus
								})
						: undefined
				}
			: null
	);

	const qa = $derived<QaOffer | null>(
		layer && hasAi
			? {
					count: (id) => layer.kept[id] ?? 0,
					load: (id) => layer.keptOn(id),
					forget: (id, answer) => layer.forget(id, answer),
					titleOf: (id) => (subject.frames[id] ? titleOf(subject.frames[id]) : null),
					ongoto: (id) => goTo(id)
				}
			: null
	);

	/** Focus the spine: where a jump lands the keyboard, as the frame is announced there. */
	export function focusSpine() {
		slider?.focus();
	}

	/**
	 * Move to a frame wherever it is: each frame sits on one spine, the main
	 * one or a trail's, so the id alone says which. An unknown id is ignored.
	 */
	export function goTo(id: string) {
		if (!mayLeave()) return;
		const main = stops(subject.spine).findIndex((s) => s.frameId === id);
		if (main >= 0) {
			trailId = null;
			index = main;
		} else {
			const t = subject.trails.find((t) => stops(t.spine).some((s) => s.frameId === id));
			if (!t) return;
			trailId = t.id;
			index = stops(t.spine).findIndex((s) => s.frameId === id);
		}
		pinned = id;
	}

	untrack(() => startAt && goTo(startAt));

	// The head, whose identity holds when the body arrives: one place per move.
	$effect(() => onplace?.(subject.frames[stop.frameId]));

	async function random(scope: RandomScope) {
		if (!onrandom || !mayLeave()) return;
		if (!(await onrandom(scope)))
			markNote =
				scope === 'subject'
					? 'There is no other frame in this subject.'
					: 'Could not reach the library. Try again.';
	}

	function toggleMark() {
		if (!bookmarks) return;
		const on = !marked.has(frame.id);
		bookmarks.ontoggle(frame);
		markNote = on ? `Bookmarked: ${titleOf(frame)}` : `Bookmark removed: ${titleOf(frame)}`;
	}

	// Coming forward (the start screen closed): the spine takes focus, or Home
	// does when that is where the reader went to the start screen from.
	let wasActive: boolean | undefined;
	let homeButton = $state<IconButton>();
	let fromHome = false;
	$effect(() => {
		if (active && wasActive === false) {
			if (fromHome) homeButton?.focus();
			else slider?.focus();
			fromHome = false;
		}
		wasActive = active;
	});

	function goHome() {
		fromHome = true;
		onhome?.();
	}

	// While following, the pin tracks the spine, so turning following off
	// leaves the reading where it is rather than on some older frame.
	$effect(() => {
		if (sync === 'follow') pinned = stop.frameId;
	});

	const reducedMotion = () => matchMedia('(prefers-reduced-motion: reduce)').matches;

	function go(i: number) {
		const to = clamp(i, path.length);
		if (to === clamp(index, path.length) || !mayLeave()) return;
		if (pinned === null) pinned = stop.frameId;
		index = to;
	}
	const step = (delta: number) => go(index + delta);

	function syncNarrative() {
		pinned = stop.frameId;
		tab = 'narrative';
	}

	function tabKeydown(e: KeyboardEvent, i: number) {
		const to = tabKey(e.key, i, tabs.length);
		if (to === null) return;
		// Handled here, so the page's arrows (the spine) stand down.
		e.preventDefault();
		tab = tabs[to];
		tabEls[to]?.focus();
	}

	function enter(t: Trail) {
		if (!mayLeave()) return;
		trailId = t.id;
		index = 0;
		if (sync === 'manual')
			pinned = subject.trails.find((x) => x.id === t.id)!.spine.segments[0].frames[0];
	}

	function leave() {
		if (!trail || !mayLeave()) return;
		const anchor = trail.anchor;
		trailId = null;
		index = stops(subject.spine).findIndex((s) => s.frameId === anchor);
		if (sync === 'manual') pinned = anchor;
		slider?.focus();
	}

	const gate = new WheelGate();
	function wheel(e: WheelEvent) {
		// A pop-up over the spine (the bookmark list) scrolls as itself.
		if (e.target instanceof Element && e.target.closest('[data-own-keys]')) return;
		e.preventDefault();
		const px = e.deltaMode === 1 ? 16 : e.deltaMode === 2 ? 400 : 1;
		const delta = Math.abs(e.deltaY) >= Math.abs(e.deltaX) ? e.deltaY : e.deltaX;
		const s = gate.push(delta * px, e.timeStamp);
		if (s) step(s);
	}

	function scrollNarrative(direction: number) {
		narrativeEl?.scrollBy({ top: direction * 80, behavior: reducedMotion() ? 'auto' : 'smooth' });
	}

	/** Page-wide keys: engine/keys.ts decides what a press means where focus is. */
	function keydown(e: KeyboardEvent) {
		if (!active || e.defaultPrevented) return;
		const target = e.target instanceof Element ? e.target : null;
		const action = pageKey(e, target, keys);
		switch (action) {
			case 'to-spine':
				slider?.focus();
				break;
			case 'next':
				step(1);
				break;
			case 'previous':
				step(-1);
				break;
			case 'first':
				go(0);
				break;
			case 'last':
				go(path.length - 1);
				break;
			case 'scroll-down':
				scrollNarrative(1);
				break;
			case 'scroll-up':
				scrollNarrative(-1);
				break;
			case 'sync':
				syncNarrative();
				break;
			case 'trail': {
				const [first] = trail ? [] : trailsFrom(frame.id);
				if (!first) return;
				enter(first);
				break;
			}
			case 'leave-trail':
				if (!trail) return;
				leave();
				break;
			case 'bookmark':
				if (!bookmarks) return;
				toggleMark();
				break;
			case 'note':
				if (!layer) return;
				startNote();
				break;
			case 'annotate':
				if (!layer) return;
				annotate();
				break;
			case 'my-notes':
				if (!myNotes) return;
				myNotesEl?.show();
				break;
			case 'contents':
				contentsEl?.show();
				break;
			case 'back':
				if (!back) return;
				back.onback();
				break;
			case 'map':
				if (!onmap) return;
				openMap();
				break;
			case 'random':
			case 'anywhere':
				if (!onrandom) return;
				random(action === 'random' ? 'subject' : 'library');
				break;
			default:
				return;
		}
		e.preventDefault();
	}
</script>

<svelte:window onkeydown={keydown} />

<!-- In the scene's place while a note is written (§Notes). -->
{#snippet noteEditor()}
	{#if draft}
		<NoteEditor
			editing={!!draft.id}
			title={titleOf(draft.frame)}
			quote={draft.anchor?.exact ?? null}
			detached={!!draft.id && detached.includes(draft.id)}
			bind:text={draft.text}
			bind:flag={draft.flag}
			{saving}
			error={saveError}
			onsave={saveNote}
			oncancel={cancelNote}
			flagHint={layer?.reviewSays}
		/>
	{/if}
{/snippet}

<div
	class="shell"
	inert={!active}
	style:--background={palette.background}
	style:--ink={palette.ink}
	style:--muted={palette.muted}
	style:--accent={palette.accent}
	style:--line={palette.line}
	style:color-scheme={palette.scheme}
>
	<h1 class="visually-hidden">{subject.title}</h1>
	<p class="visually-hidden" aria-live="polite" aria-atomic="true">{announcement}</p>
	<p class="visually-hidden" role="status">{markNote}</p>

	<div
		class="panes {shape}"
		class:on-ai={tabbed && tab === 'ai'}
		style:--cols={cols}
		style:--rows={rows}
		bind:this={panesEl}
	>
		<SpinePane
			{path}
			index={clamp(index, path.length)}
			{frame}
			palette={palettes.scene}
			{trail}
			{branches}
			{marksOf}
			editor={draft ? noteEditor : undefined}
			frames={subject.frames}
			onstep={step}
			onjump={go}
			onwheel={wheel}
			onleave={leave}
			bind:slider
		>
			{#snippet tools()}
				{#if back}
					<BackChip to={back.to} depth={back.depth} key={shown(keys.back)} onback={back.onback} />
				{/if}
				{#if onrandom}
					<IconButton
						label="Random frame in this subject"
						title={shown(keys.random)
							? `Random frame in this subject (${shown(keys.random)})`
							: 'Random frame in this subject'}
						onclick={() => random('subject')}
					>
						<!-- One die: here. -->
						<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor">
							<rect x="4.5" y="4.5" width="15" height="15" rx="2.5" stroke-width="1.5" />
							<circle cx="9" cy="9" r="1.1" fill="currentColor" stroke="none" />
							<circle cx="12" cy="12" r="1.1" fill="currentColor" stroke="none" />
							<circle cx="15" cy="15" r="1.1" fill="currentColor" stroke="none" />
						</svg>
					</IconButton>
				{/if}
				<Contents
					{contents}
					current={frame.id}
					startOpen={openTrails(subject, frame.id, trailId)}
					{marksOf}
					{hrefOf}
					key={shown(keys.contents)}
					onjump={goTo}
					bind:this={contentsEl}
				/>
				{#if onmap}
					<IconButton
						label="Map"
						title={shown(keys.map) ? `Map (${shown(keys.map)})` : 'Map'}
						aria-haspopup="dialog"
						bind:this={mapButton}
						onclick={openMap}
					>
						<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor">
							<circle cx="12" cy="12" r="2.5" stroke-width="1.5" />
							<circle cx="5" cy="6" r="1.75" stroke-width="1.5" />
							<circle cx="19" cy="7" r="1.75" stroke-width="1.5" />
							<circle cx="17" cy="19" r="1.75" stroke-width="1.5" />
							<path d="M6.5 7 10 10.5M17.4 7.9 14.2 10.8M13.6 14 16 17.5" stroke-width="1.5" />
						</svg>
					</IconButton>
				{/if}
				{#if bookmarks}
					<Bookmarks
						marked={marked.has(frame.id)}
						items={bookmarks.items}
						exportHref={bookmarks.exportHref}
						ontoggle={toggleMark}
						onjump={goTo}
						onremove={bookmarks.onremove}
					/>
				{/if}
				{#if myNotes}
					<MyNotes offer={myNotes} key={shown(keys['my-notes'])} bind:this={myNotesEl} />
				{/if}
			{/snippet}
		</SpinePane>

		<div class="tab-row" bind:this={tabRowEl}>
			{#if tabs.length > 1}
				<div role="tablist" aria-label="Right-hand pane">
					{#each tabs as t, i (t)}
						<button
							type="button"
							role="tab"
							id="tab-{t}"
							aria-selected={tab === t}
							aria-controls={TAB_PANEL[t]}
							tabindex={tab === t ? 0 : -1}
							onclick={() => (tab = t)}
							onkeydown={(e) => tabKeydown(e, i)}
							bind:this={tabEls[i]}
						>
							{TAB_LABEL[t]}
							{#if t === 'notes' && frameNotes.length}
								<span class="count" aria-hidden="true">{frameNotes.length}</span>
								<span class="visually-hidden">, {frameNotes.length} on this frame</span>
							{/if}
							{#if t === 'ai' && aiActivity !== 'idle'}
								<span class="badge {aiActivity}" aria-hidden="true"
									>{aiActivity === 'ready' ? '●' : '…'}</span
								>
								<span class="visually-hidden"
									>{aiActivity === 'ready' ? ', a result is waiting' : ', working'}</span
								>
							{/if}
						</button>
					{/each}
				</div>
			{/if}
			<div class="corner">
				{#if onrandom}
					<IconButton
						label="Random frame anywhere"
						title={shown(keys.anywhere)
							? `Random frame anywhere in the library (${shown(keys.anywhere)})`
							: 'Random frame anywhere in the library'}
						onclick={() => random('library')}
					>
						<!-- Two dice: anywhere. -->
						<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor">
							<rect x="2.5" y="8.5" width="11" height="11" rx="2" stroke-width="1.5" />
							<path
								d="M10.5 8.5V6.5a2 2 0 0 1 2-2h7a2 2 0 0 1 2 2v7a2 2 0 0 1-2 2h-6"
								stroke-width="1.5"
							/>
							<circle cx="5.75" cy="11.75" r="1" fill="currentColor" stroke="none" />
							<circle cx="10.25" cy="16.25" r="1" fill="currentColor" stroke="none" />
							<circle cx="17.5" cy="8.5" r="1" fill="currentColor" stroke="none" />
						</svg>
					</IconButton>
				{/if}
				{#if onhome}
					<IconButton
						class="home"
						label="Home"
						title="Home: the start screen"
						bind:this={homeButton}
						onclick={goHome}
					>
						<!-- kloom's own icon, from the repository (engine/ui/icons). -->
						<!-- eslint-disable-next-line svelte/no-at-html-tags -->
						{@html homeIcon}
					</IconButton>
				{/if}
				<Settings {settings} />
			</div>
		</div>

		<Narrative
			tab={tabs.length > 1 ? 'tab-narrative' : null}
			hidden={tab !== 'narrative'}
			frame={narrativeFrame}
			{pending}
			spineFrame={frame}
			{sync}
			trails={trail ? [] : trailsFrom(narrativeFrame.id)}
			onenter={enter}
			keys={{ sync: shown(keys.sync), trail: shown(keys.trail) }}
			{qa}
			{annotating}
			annotations={frameNotes.filter((n) => n.anchor)}
			links={linksOffer}
			bind:detached
			bind:element={narrativeEl}
			bind:this={narrative}
		/>

		{#if layer}
			<Notes
				tab="tab-notes"
				hidden={tab !== 'notes'}
				title={titleOf(narrativeFrame)}
				notes={frameNotes}
				editing={draft?.id ?? null}
				{detached}
				key={shown(keys.note)}
				onadd={(from) => startNote(from)}
				onedit={editNote}
				ondelete={deleteNote}
				onshow={showAnnotation}
			/>
		{/if}

		{#if __KLOOM_EDITION__ !== 'reader' && ai}
			<AiPane
				subject={subject.id}
				frame={narrativeFrame}
				{trail}
				{settings}
				offer={ai}
				mainFrames={stops(subject.spine).map((s) => s.frameId)}
				titleOf={(id) => (subject.frames[id] ? titleOf(subject.frames[id]) : id)}
				{ongrown}
				layout={shape}
				showResults={!tabbed || tab === 'ai'}
				onshow={() => (tab = 'ai')}
				onactivity={(a) => (aiActivity = a)}
				onkept={(id) => layer?.onkept(id)}
			/>
		{/if}

		{#each dividers as d (d.id)}
			{@const b = bounds(panes, shape, d.id)}
			<Splitter
				class="at-{d.id}"
				orientation={d.id === 'upper' ? 'horizontal' : 'vertical'}
				label={d.label}
				controls={d.controls}
				value={panes[d.id]}
				min={b.min}
				max={b.max}
				at={(e) => pointerAt(d.id, e)}
				onchange={(v) => setPane(d.id, v)}
				onreset={() => resetPane(d.id)}
			/>
		{/each}
	</div>

	<p id="ai-hint" class="hint">
		<kbd>←</kbd><kbd>→</kbd> spine · <kbd>↑</kbd><kbd>↓</kbd> narrative
		{#if hintRuns[0].length}
			·
			<!-- prettier-ignore -->
			<span>{#each hintRuns[0] as h (h.action)}{h.lead}<kbd>{h.key}</kbd>&nbsp;{h.label}{/each}, in the spine{layer ? ', narrative or notes' : ' or narrative'}</span>
		{/if}
		{#if hintRuns[1].length}
			·
			<!-- prettier-ignore -->
			<span>{#each hintRuns[1] as h (h.action)}{h.lead}<kbd>{h.key}</kbd>&nbsp;{h.label}{/each}, anywhere</span>
		{/if}
		{#if hasAi}· <kbd>Tab</kbd> into and out of the AI pane{/if} · <kbd>Esc</kbd> back to the spine ·
		drag a divider, or focus it and use the arrows
	</p>
</div>

<style>
	/*
	 * Registered so the palette itself interpolates. Unregistered custom
	 * properties snap, so everything painted straight from a variable (accent
	 * words, buttons, borders, SVG strokes) used to change at once while the
	 * background faded behind it: a flash bulb (korg 3370). The initial values
	 * are only fallbacks; each frame's palette sets them, the reading's here
	 * and the scene's on the spine pane.
	 */
	@property --background {
		syntax: '<color>';
		inherits: true;
		initial-value: #000;
	}
	@property --ink {
		syntax: '<color>';
		inherits: true;
		initial-value: #fff;
	}
	@property --muted {
		syntax: '<color>';
		inherits: true;
		initial-value: #888;
	}
	@property --accent {
		syntax: '<color>';
		inherits: true;
		initial-value: #fff;
	}
	@property --line {
		syntax: '<color>';
		inherits: true;
		initial-value: #fff;
	}

	.shell {
		display: flex;
		flex-direction: column;
		height: 100dvh;
		color: var(--ink);
		background: var(--background);
		/* One timing for every colour, so the whole page moves together. */
		--palette-fade: 1.5s ease-in-out;
		transition:
			--background var(--palette-fade),
			--ink var(--palette-fade),
			--muted var(--palette-fade),
			--accent var(--palette-fade),
			--line var(--palette-fade);
	}

	/*
	 * §Layout: where each pane sits. Every pane is placed explicitly, so the
	 * dividers, which share its grid cell, never push a pane along. The
	 * column (and the split's row) sizes are the reader's, set inline.
	 */
	.panes {
		flex: 1;
		min-height: 0;
		display: grid;
		grid-template-columns: var(--cols);
		grid-template-rows: auto minmax(0, 1fr);
	}
	.panes > :global(.spine) {
		grid-column: 1;
		grid-row: 1 / -1;
	}
	/* The tab row heads the right-hand pane in every layout; the gear sits in it. */
	.panes > .tab-row {
		grid-column: 2;
		grid-row: 1;
	}
	.panes > :global(.narrative),
	.panes > :global(.notes) {
		grid-column: 2;
		grid-row: 2;
	}
	.panes > :global(.at-spine) {
		grid-column: 1;
		grid-row: 1 / -1;
		justify-self: end;
		margin-right: -5px;
	}
	.strip {
		grid-template-rows: auto minmax(0, 1fr) auto;
	}
	.strip > :global(.spine),
	.strip > :global(.at-spine) {
		grid-row: 1 / 3;
	}
	.strip > :global(.ai) {
		grid-column: 1 / -1;
		grid-row: 3;
	}
	.columns > :global(.ai) {
		grid-column: 3;
		grid-row: 1 / -1;
	}
	.columns > :global(.at-ai) {
		grid-column: 3;
		grid-row: 1 / -1;
		justify-self: start;
		margin-left: -5px;
	}
	.split {
		grid-template-rows: auto var(--rows);
	}
	.split > :global(.ai) {
		grid-column: 2;
		grid-row: 3;
		border-left: 1px solid color-mix(in srgb, var(--muted) 40%, transparent);
	}
	.split > :global(.at-upper) {
		grid-column: 2;
		grid-row: 2;
		align-self: end;
		margin-bottom: -5px;
	}
	.tabs {
		grid-template-rows: auto minmax(0, 1fr) auto;
	}
	.tabs > :global(.ai) {
		grid-column: 2;
		grid-row: 3;
		border-left: 1px solid color-mix(in srgb, var(--muted) 40%, transparent);
	}
	.on-ai > :global(.ai) {
		grid-row: 2 / 4;
		border-top: 0;
	}
	.hint {
		margin: 0;
		padding: 0.35rem 1.5rem;
		font-size: 0.75rem;
		color: var(--muted);
		border-top: 1px solid color-mix(in srgb, var(--muted) 40%, transparent);
	}
	kbd {
		font-family: var(--mono);
		font-size: 0.7rem;
		padding: 0 0.25rem;
		margin-right: 0.1rem;
		border: 1px solid var(--muted);
		border-radius: 0.2rem;
	}
	.tab-row {
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: 0.5rem;
		padding: 0.5rem 1.5rem 0;
		border-left: 1px solid color-mix(in srgb, var(--muted) 40%, transparent);
	}
	.corner {
		display: flex;
		gap: 0.25rem;
		margin-left: auto;
	}
	[role='tablist'] {
		display: flex;
		gap: 0.25rem;
	}
	[role='tab'] {
		font-family: var(--mono);
		font-size: 0.75rem;
		letter-spacing: 0.12em;
		text-transform: uppercase;
		padding: 0.35rem 0.75rem;
		color: var(--muted);
		background: none;
		border: 0;
		border-bottom: 2px solid transparent;
		cursor: pointer;
	}
	[role='tab'][aria-selected='true'] {
		color: var(--ink);
		border-bottom-color: var(--accent);
	}
	.badge,
	.count {
		margin-left: 0.25rem;
		color: var(--accent);
	}
	/* A divider shows focus as its own accent line (Splitter.svelte). */
	.shell :global(:focus-visible:not([role='separator'])) {
		outline: 2px solid var(--accent);
		outline-offset: 2px;
	}

	/* One column on a phone, in every layout: spine, (tabs), narrative, AI. No dividers. */
	@media (max-width: 760px) {
		.shell {
			height: auto;
			min-height: 100dvh;
		}
		.panes {
			grid-template-columns: minmax(0, 1fr);
			grid-template-rows: none;
		}
		.panes > :global(*) {
			grid-column: 1 !important;
			grid-row: auto !important;
		}
		.panes > :global([role='separator']) {
			display: none;
		}
		.panes > :global(.spine) {
			height: 75svh;
		}
		.panes > :global(.narrative) {
			height: 70svh;
			border-left: 0;
			border-top: 1px solid color-mix(in srgb, var(--muted) 40%, transparent);
		}
		.panes > :global(.ai) {
			border-left: 0;
		}
		.on-ai > :global(.ai) {
			min-height: 70svh;
		}
		.tab-row {
			border-left: 0;
			border-top: 1px solid color-mix(in srgb, var(--muted) 40%, transparent);
		}
	}

	@media (prefers-reduced-motion: reduce) {
		.shell {
			transition: none;
		}
	}
</style>

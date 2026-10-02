<script lang="ts">
	import { onMount, tick, untrack } from 'svelte';
	import type { FrameHead } from '$engine/model';
	import {
		newerPlaces,
		type Bookmark,
		type JumpItem,
		type Kept,
		type Note,
		type Place,
		type ReaderLayer
	} from '$engine/reader-data';
	import { subjectOf, type MapData } from '$engine/map';
	import { pickOther, walkedFrames } from '$engine/random';
	import MapOverlay, { type MapOpen } from '$engine/ui/MapOverlay.svelte';
	import Shell from '$engine/ui/Shell.svelte';
	import StartScreen from '$engine/ui/StartScreen.svelte';
	import {
		afterNavigate,
		beforeNavigate,
		goto,
		invalidateAll,
		replaceState
	} from '$app/navigation';
	import { resolve } from '$app/paths';
	import { page } from '$app/state';
	import {
		ASK_MODEL,
		followSpine,
		GROW_MODEL,
		keySettings,
		layout,
		modelSetting,
		paletteFor,
		paletteMode
	} from '$engine/settings';
	import type { ServedBody } from '$engine/served';
	import type { StartLook } from '$engine/start';
	import type { LibraryStats } from '$engine/stats';
	import { UserSettings } from '$engine/user-settings.svelte';
	import { inscription, loomCredit } from '$lib/start/credit';
	import type { PageProps } from './$types';
	import type { Placed } from './+page.server';

	let { data }: PageProps = $props();

	// Begun per subject: opening another one shows its start screen first. A
	// deep link to a frame (`/<subject>/<frame>`) is begun already.
	let begun = $state<string | null>(untrack(() => (data.frame ? data.subject.id : null)));
	const started = $derived(begun === data.subject.id);
	let loom = $state<string | null>(null);

	// The reader's settings. The ask and grow models' choices come from the app
	// config, once per page load.
	const growModels = untrack(() => data.growModels);
	const settings = new UserSettings([
		paletteMode,
		followSpine,
		layout,
		modelSetting(
			ASK_MODEL,
			'Ask model',
			untrack(() => data.askModels)
		),
		...(growModels ? [modelSetting(GROW_MODEL, 'Grow model', growModels)] : []),
		...keySettings
	]);

	// The start screen's subject list (korg 3424): the selection shows its
	// title, its place and its own drawings, and wears its first frame's
	// palette, in the reader's mode. This subject's look is at hand; another's
	// is fetched when it is first selected, and kept.
	let selected = $state(untrack(() => data.subject.id));
	let looks = $state<Record<string, StartLook>>({});
	const look = $derived(selected === data.subject.id ? data.start : (looks[selected] ?? null));
	$effect(() => {
		const id = selected;
		if (id === data.subject.id || untrack(() => looks[id])) return;
		fetch(resolve('/api/start/[subject]', { subject: id }))
			.then((res) => (res.ok ? res.json() : Promise.reject(res.status)))
			.then((l: StartLook) => (looks = { ...looks, [id]: l }))
			.catch((e) => console.warn(`start look: ${id} failed`, e));
	});
	const startPalette = $derived.by(() => {
		const l = look ?? data.start;
		return paletteFor(l, l.palette, settings.get(paletteMode.id)!);
	});

	// Arriving in another subject selects it.
	$effect.pre(() => {
		const id = data.subject.id;
		untrack(() => (selected = id));
	});

	const listed = $derived(
		data.subjects.map((s) => ({
			id: s.id,
			title: s.title,
			subtitle: s.subtitle,
			note: data.readerData?.last?.subject === s.id ? 'Last read' : undefined
		}))
	);

	/** Back to the start screen over this subject, where Begin or Esc returns. */
	function home() {
		selected = data.subject.id;
		begun = null;
	}

	/** Open another subject from the list: begun already, as the reader chose it there. */
	function open(id: string) {
		begun = id;
		goto(resolve('/[subject]/[[frame]]', { subject: id }));
	}

	// The reader's own data (docs/design.md §Reader data, korg 3413, 3414).
	// Absent when there is no reader: nothing is kept, nothing is offered.
	let shell = $state<ReturnType<typeof Shell>>();

	// Frame bodies (docs/design.md §Serving, korg 3460): the load brought the
	// ones around the frame the page opened on, and the rest are fetched as
	// the shell asks for them, then kept for this subject and build. Another
	// build (a grow landed) or another subject starts afresh.
	const cacheKey = () => `${data.build} ${data.subject.id}`;
	let bodies = $state.raw<Record<string, ServedBody>>(untrack(() => ({ ...data.bodies })));
	let bodiesFor = untrack(cacheKey);
	/** Fetches made for this cache, so none is made twice. Never rendered. */
	let asked: Record<string, true> = {};
	$effect.pre(() => {
		const key = cacheKey();
		const seed = data.bodies;
		untrack(() => {
			if (key === bodiesFor) bodies = { ...bodies, ...seed };
			else {
				bodiesFor = key;
				asked = {};
				bodies = { ...seed };
			}
		});
	});
	function need(ids: string[]) {
		const subject = data.subject.id;
		const key = bodiesFor;
		for (const id of ids) {
			if (bodies[id] || asked[id]) continue;
			asked[id] = true;
			fetch(resolve('/api/frame/[subject]/[frame]', { subject, frame: id }))
				.then((res) => (res.ok ? (res.json() as Promise<ServedBody>) : Promise.reject(res.status)))
				.then((body) => {
					if (bodiesFor === key) bodies = { ...bodies, [id]: body };
				})
				.catch((e) => {
					// Asked again the next time the shell needs it.
					delete asked[id];
					console.warn(`frame ${subject}/${id}: could not fetch its body`, e);
				});
		}
	}
	let marks = $state<(Bookmark & { subjectTitle: string })[]>(
		untrack(() => data.readerData?.bookmarks ?? [])
	);
	const here = $derived(data.subjects.find((s) => s.id === data.subject.id)!);
	const titleOf = (f: FrameHead) => `${f.scene.headline} ${f.scene.accent}`;
	const frameHref = (subject: string, frame: string) =>
		resolve('/[subject]/[[frame]]', { subject, frame });

	/** Write to the reader's store; a failure is logged, and the reading goes on. */
	async function write(path: string, method: string, body: object) {
		return !!(await send(path, method, body));
	}

	/** A reader-data request: the response, or null (and a warning) when it failed. */
	async function send(path: string, method: string, body?: object) {
		const res = await fetch(path, {
			method,
			...(body
				? {
						headers: { 'content-type': 'application/json' },
						body: JSON.stringify(body),
						keepalive: true
					}
				: {})
		}).catch(() => null);
		if (!res?.ok) console.warn(`reader data: ${method} ${path} failed`, res?.status);
		return res?.ok ? res : null;
	}

	// The reader's layer on a frame (korg 3409, 3390): this subject's notes,
	// and how many answers were kept on each frame. Derived from the load, so
	// another subject brings its own, and written over as the reader acts.
	let notes = $derived<Note[]>(data.readerData?.notes ?? []);
	let keptCounts = $derived<Record<string, number>>(data.readerData?.kept ?? {});
	const layer = $derived<ReaderLayer | null>(
		data.reader
			? {
					notes,
					kept: keptCounts,
					saveNote: async (n) => {
						const res = await send(resolve('/api/reader/notes'), 'POST', {
							...n,
							subject: data.subject.id
						});
						const saved: Note | null = res ? await res.json() : null;
						if (saved)
							notes = n.id ? notes.map((x) => (x.id === saved.id ? saved : x)) : [...notes, saved];
						return saved;
					},
					deleteNote: async (id) => {
						if (!(await write(resolve('/api/reader/notes'), 'DELETE', { id }))) return false;
						notes = notes.filter((n) => n.id !== id);
						return true;
					},
					keptOn: async (frame) => {
						const q = new URLSearchParams({ subject: data.subject.id, frame });
						const res = await send(`${resolve('/api/reader/kept')}?${q}`, 'GET');
						return res ? ((await res.json()) as Kept[]) : null;
					},
					forget: async (frame, id) => {
						const ok = await write(resolve('/api/reader/kept'), 'DELETE', {
							subject: data.subject.id,
							id
						});
						if (ok)
							keptCounts = { ...keptCounts, [frame]: Math.max(0, (keptCounts[frame] ?? 1) - 1) };
						return ok;
					},
					onkept: (frame) => (keptCounts = { ...keptCounts, [frame]: (keptCounts[frame] ?? 0) + 1 })
				}
			: null
	);

	// A note with unsaved changes: leaving the subject, or the page, asks first.
	// Leaving for good (a reload, closing the tab) gets the browser's own question.
	beforeNavigate((nav) => {
		if (!shell?.hasUnsavedNote()) return;
		if (nav.willUnload) nav.cancel();
		else if (confirm('This note has changes that are not saved. Discard them?'))
			shell.discardNote();
		else nav.cancel();
	});

	// A deep link followed inside the app (the start screen's last-read offer,
	// say) opens on its frame too: the page is reused, so this runs on each.
	$effect.pre(() => {
		const frame = data.frame;
		const id = data.subject.id;
		if (!frame) return;
		untrack(() => {
			begun = id;
			shell?.goTo(frame);
		});
	});

	// Where the reader is: named in the URL, so refresh keeps it and it can be
	// shared, and kept as their place a moment after they stop moving.
	let current = $state<FrameHead | null>(null);
	let placeTimer: ReturnType<typeof setTimeout> | undefined;
	// Each subject's place as the reader's store has it (korg 3432): loaded
	// with the page, and moved here at once as the reader moves, so the start
	// screen never waits on the write. A later load keeps whichever is newer.
	let moved = $state<Record<string, Placed<Place>>>({});
	const places = $derived(newerPlaces(moved, data.readerData?.places ?? {}));
	$effect(() => {
		const f = current;
		if (!started || !f) return;
		const subject = data.subject.id;
		untrack(() => {
			const href = frameHref(subject, f.id);
			// The jumps that led here stay with the entry (§Connections).
			if (location.pathname !== href) replaceState(href, page.state);
			if (!data.reader) return;
			const label = titleOf(f);
			const at = new Date().toISOString();
			moved = {
				...moved,
				[subject]: { subject, frame: f.id, label, at, subjectTitle: here.title }
			};
			clearTimeout(placeTimer);
			placeTimer = setTimeout(() => {
				write(resolve('/api/reader/place'), 'POST', { subject, frame: f.id, label });
			}, 800);
		});
	});

	// Jumps (docs/design.md §Connections, korg 3439): following a connection
	// or a name adds a history entry, where stepping the spine replaces it.
	// Each entry carries the jumps that led to it, so the Back chip and the
	// browser's Back always agree: the chip is the browser's Back.
	function follow(subject: string, frame: string) {
		const f = current;
		const from = f
			? [{ subject: data.subject.id, frame: f.id, title: f.topic, subjectTitle: here.title }]
			: [];
		jumped = true;
		goto(frameHref(subject, frame), { state: { back: [...(page.state.back ?? []), ...from] } });
	}
	// The link followed is gone (a card closes, the list is another frame's),
	// so focus lands on the spine, where the new frame is announced. Back,
	// the chip's or the browser's, lands there too.
	let jumped = false;
	afterNavigate(async (nav) => {
		if (!jumped && nav.type !== 'popstate') return;
		jumped = false;
		await tick();
		shell?.focusSpine();
	});
	// The map (docs/design.md §The map, korg 3441): its data is fetched when it
	// first opens, and kept until a grow changes the subjects.
	let map = $state<ReturnType<typeof MapOverlay>>();
	let mapData: Promise<MapData> | null = null;
	function loadMap() {
		mapData ??= fetch(resolve('/api/map')).then((res) =>
			res.ok ? (res.json() as Promise<MapData>) : Promise.reject(res.status)
		);
		mapData.catch(() => (mapData = null));
		return mapData;
	}
	const openMap = (o: MapOpen) => map?.show(o);
	/** Go to a frame from the map: a jump, as from a connection, from the shell or the start screen. */
	function followFromMap(subject: string, frame: string) {
		if (started) follow(subject, frame);
		else {
			begun = subject;
			goto(frameHref(subject, frame));
		}
	}

	// Random jumps (docs/design.md §Random, korg 3437): a jump like any other,
	// so the Back chip and the browser's Back return from one. Anywhere in the
	// library reads the frames from the map's data, fetched once.
	async function random(scope: 'subject' | 'library') {
		const f = current;
		if (!f) return false;
		if (scope === 'subject') {
			const to = pickOther(walkedFrames(data.subject), f.id);
			if (to) follow(data.subject.id, to);
			return !!to;
		}
		const frames = await loadMap()
			.then((d) => d.frames.map((x) => x.key))
			.catch(() => null);
		const to = frames && pickOther(frames, `${data.subject.id}/${f.id}`);
		if (to) follow(subjectOf(to), to.slice(to.indexOf('/') + 1));
		return !!to;
	}

	const backOffer = $derived.by(() => {
		const stack = page.state.back ?? [];
		return stack.length
			? { to: stack[stack.length - 1], depth: stack.length, onback: () => history.back() }
			: null;
	});

	const marked = $derived(
		new Set(marks.filter((m) => m.subject === data.subject.id).map((m) => m.frame))
	);
	const bookmarkOffer = $derived(
		data.reader
			? {
					marked,
					items: marks.map((m): JumpItem => ({
						key: `${m.subject}/${m.frame}`,
						subject: m.subject,
						label:
							m.subject === data.subject.id && data.subject.frames[m.frame]
								? titleOf(data.subject.frames[m.frame])
								: m.label,
						context:
							m.subject === data.subject.id && data.subject.frames[m.frame]
								? `${data.subject.frames[m.frame].position.label} · ${data.subject.frames[m.frame].topic}`
								: m.subjectTitle,
						href: frameHref(m.subject, m.frame),
						frame: m.subject === data.subject.id ? m.frame : undefined
					})),
					exportHref: resolve('/api/reader/export'),
					ontoggle: toggleMark,
					onremove: (item: JumpItem) => unmark(item.subject, item.key.split('/')[1])
				}
			: null
	);

	async function toggleMark(f: FrameHead) {
		const subject = data.subject.id;
		if (marked.has(f.id)) return unmark(subject, f.id);
		const mark = { subject, frame: f.id, label: titleOf(f) };
		const before = marks;
		marks = [{ ...mark, at: new Date().toISOString(), subjectTitle: here.title }, ...marks];
		if (!(await write(resolve('/api/reader/bookmarks'), 'POST', mark))) marks = before;
	}

	async function unmark(subject: string, frame: string) {
		const before = marks;
		marks = marks.filter((m) => !(m.subject === subject && m.frame === frame));
		if (!(await write(resolve('/api/reader/bookmarks'), 'DELETE', { subject, frame })))
			marks = before;
	}

	// Offered on the start screen: the selected subject's place, this subject's
	// included (korg 3432). Begin starts from the first frame, so Continue is
	// the only way back to where the reader was, and never names the same place.
	const resume = $derived.by(() => {
		const p = places[selected];
		if (!p) return [];
		const action = 'Continue where you were';
		if (selected !== data.subject.id)
			return [{ key: 'here', action, label: p.label, href: frameHref(p.subject, p.frame) }];
		const f = data.subject.frames[p.frame];
		if (!f) return [];
		return [
			{
				key: 'here',
				action,
				label: `${titleOf(f)} · ${f.position.label}`,
				onpick: () => shell?.goTo(f.id)
			}
		];
	});
	const first = $derived(data.subject.spine.segments[0].frames[0]);

	/** The library's counts, for the start screen's About panel (docs/design.md §About). */
	const loadStats = (): Promise<LibraryStats> =>
		fetch(resolve('/api/stats')).then((res) => (res.ok ? res.json() : Promise.reject(res.status)));

	// Large, so it arrives after the page as its own compressed chunk.
	onMount(async () => {
		settings.load();
		loom = (await import('$lib/start/loom.svg?raw')).default;
	});
</script>

<svelte:head>
	<title>kloom · {data.subject.title}</title>
</svelte:head>

<!-- Keyed by subject: moving to another subject starts its shell afresh, at its start screen. -->
{#key data.subject.id}
	<Shell
		bind:this={shell}
		subject={data.subject}
		{bodies}
		onneed={need}
		{settings}
		ai={{ web: data.askWeb, grow: !!data.growModels }}
		ongrown={() => {
			mapData = null;
			invalidateAll();
		}}
		active={started}
		startAt={data.frame}
		onplace={(f) => (current = f)}
		bookmarks={bookmarkOffer}
		{layer}
		onhome={home}
		hrefOf={(frame) => frameHref(data.subject.id, frame)}
		hrefTo={frameHref}
		onfollow={follow}
		back={backOffer}
		onmap={openMap}
		onrandom={random}
	/>
{/key}

<MapOverlay bind:this={map} load={loadMap} hrefOf={frameHref} onfollow={followFromMap} />

{#if !started}
	<StartScreen
		subjects={listed}
		bind:selected
		current={data.subject.id}
		subtitle="A timeline you can read, question and grow"
		{inscription}
		art={loom}
		credits={[loomCredit]}
		palette={startPalette}
		ring={look?.illustrations ?? []}
		{resume}
		onbegin={() => (begun = data.subject.id)}
		onfirst={() => shell?.goTo(first)}
		onopen={open}
		onmap={(refocus) =>
			openMap({ target: { view: 'library' }, scheme: startPalette.scheme, refocus })}
		{settings}
		about={{ stats: loadStats, build: __KLOOM_BUILD__ || undefined }}
	/>
{/if}

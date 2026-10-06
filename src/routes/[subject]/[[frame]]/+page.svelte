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
		type ReaderLayer,
		type SuggestOffer,
		type Suggestion
	} from '$engine/reader-data';
	import { subjectOf, type MapData } from '$engine/map';
	import type { MyNotesData, MyNotesOffer, NoteEntry } from '$engine/my-notes';
	import { pickOther, walkedFrames } from '$engine/random';
	import MapOverlay, { type MapOpen } from '$engine/ui/MapOverlay.svelte';
	import Changelog, { type ChangelogOffer } from '$engine/ui/Changelog.svelte';
	import {
		readingFrom,
		type ChangelogData,
		type ReaderNews,
		type Reading
	} from '$engine/whats-new';
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
		coloursOf,
		darkBrightness,
		followSpine,
		framePalettes,
		GROW_MODEL,
		layout,
		lightBrightness,
		modelSetting,
		readingColours,
		sceneColours
	} from '$engine/settings';
	import type { ServedBody } from '$engine/served';
	import type { StartLook } from '$engine/start';
	import type { LibraryStats } from '$engine/stats';
	import { UserSettings } from '$engine/user-settings.svelte';
	import { PLACE_MS, VISIT_MS } from '$engine/reader-data';
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
	// config, once per page load; with no AI pane (a reader the reader site
	// has not given ask) there is no layout to choose and no model.
	const ai = untrack(() => data.ai);
	const settings = new UserSettings([
		sceneColours,
		readingColours,
		followSpine,
		...(ai
			? [
					layout,
					modelSetting(ASK_MODEL, 'Ask model', ai.askModels),
					...(ai.growModels ? [modelSetting(GROW_MODEL, 'Grow model', ai.growModels)] : [])
				]
			: []),
		lightBrightness,
		darkBrightness
	]);

	// The start screen's subject list (korg 3424): the selection shows its
	// title, its place and its own drawings, and wears its first section's
	// palette, as the reader colours scenes. This subject's look is at hand; another's
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
		return framePalettes(l, l.palette, l.palette, coloursOf(settings)).scene;
	});

	// Arriving in another subject selects it.
	$effect.pre(() => {
		const id = data.subject.id;
		untrack(() => (selected = id));
	});

	const listed = $derived(
		data.subjects.map((s) => {
			const fresh = news?.fresh[s.id]?.length ?? 0;
			const last = data.readerData?.last?.subject === s.id;
			return {
				id: s.id,
				title: s.title,
				subtitle: s.subtitle,
				...(last ? { last } : {}),
				...(fresh ? { fresh } : {})
			};
		})
	);

	// What's new (docs/design.md §What's new, korg 3525): the reader's side,
	// loaded with the page and kept current here as they open frames, mark
	// them seen or catch up. Absent with no reader.
	let news = $derived<ReaderNews | null>(data.readerData?.news ?? null);
	const freshHere = $derived(new Set(news?.fresh[data.subject.id] ?? []));
	/** These frames are not new to the reader any more. */
	function seenHere(subject: string, frames: string[]) {
		if (!news) return;
		const left = (news.fresh[subject] ?? []).filter((f) => !frames.includes(f));
		const fresh = { ...news.fresh, [subject]: left };
		if (!left.length) delete fresh[subject];
		news = { ...news, fresh };
	}
	async function markSeen(subject: string, frames: string[]) {
		const ok = await write(resolve('/api/reader/seen'), 'POST', { subject, frames });
		if (ok) seenHere(subject, frames);
		return ok;
	}
	async function caughtUp(subject: string) {
		const res = await send(resolve('/api/reader/caught-up'), 'POST', { subject });
		if (!res || !news) return false;
		const reading = (await res.json()) as Reading;
		const fresh = { ...news.fresh };
		delete fresh[subject];
		news = { ...news, readings: { ...news.readings, [subject]: reading }, fresh };
		return true;
	}
	/** Said under Begin: what is new to the reader in the selected subject. */
	const freshLine = $derived.by(() => {
		const n = news?.fresh[selected]?.length ?? 0;
		const r = news?.readings[selected];
		if (!n || !r) return null;
		const since = readingFrom(r) === r.first ? 'you started' : 'you caught up';
		return `${n} new since ${since}`;
	});

	/**
	 * Back to the start screen over this subject, where Begin or Esc returns.
	 * A history entry of its own at `/<subject>` (korg 3517), so a reload stays
	 * home, Back returns to the frame and Forward comes home again.
	 */
	let goingHome = false;
	function home() {
		selected = data.subject.id;
		begun = null;
		goingHome = true;
		// keepFocus: the start screen has taken it, and SvelteKit's reset would
		// leave it on the bare page, where neither Esc nor Enter reaches it.
		goto(resolve('/[subject]/[[frame]]', { subject: data.subject.id }), {
			state: { home: true },
			keepFocus: true
		}).finally(() => (goingHome = false));
	}
	// Coming back to a home entry (Forward, say) shows the start screen again.
	$effect.pre(() => {
		if (!page.state.home) return;
		untrack(() => {
			selected = data.subject.id;
			begun = null;
		});
	});

	/** Open another subject from the list: begun already, as the reader chose it there. */
	function open(id: string) {
		begun = id;
		// keepFocus: the new shell mounts begun and puts focus on its spine.
		goto(resolve('/[subject]/[[frame]]', { subject: id }), { keepFocus: true });
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
					// On the public site a flagged note goes to Ken (korg 3502): said where it is ticked.
					reviewSays:
						__KLOOM_EDITION__ === 'reader'
							? 'Sends this note to Ken and Ken’s agents, who read it and may answer it here.'
							: undefined,
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
					seen: (ids) => {
						notes = notes.map((n) => (ids.includes(n.id) ? { ...n, unseen: false } : n));
						see(ids);
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

	// My notes (docs/design.md §My notes, korg 3481): every note across
	// subjects, and how many agent answers wait to be seen. The list is
	// fetched each time the panel opens; a change to this subject's notes
	// there is carried into the notes the shell shows.
	let unseen = $derived<number>(data.readerData?.unseen ?? 0);
	async function see(ids: string[]) {
		const res = await send(resolve('/api/reader/my-notes'), 'POST', { ids });
		if (res) unseen = ((await res.json()) as { unseen: number }).unseen;
	}
	// Suggest a subject (korg 3459), in About: the reader's own, and a new one.
	const suggest = $derived<SuggestOffer | null>(
		data.reader
			? {
					list: async () => {
						const res = await send(resolve('/api/reader/suggestions'), 'GET');
						return res ? ((await res.json()) as Suggestion[]) : null;
					},
					send: async (s) => {
						const res = await fetch(resolve('/api/reader/suggestions'), {
							method: 'POST',
							headers: { 'content-type': 'application/json' },
							body: JSON.stringify(s)
						}).catch(() => null);
						if (res?.ok) return (await res.json()) as Suggestion;
						const said =
							res && ((await res.json().catch(() => null)) as { message?: string } | null);
						return { error: said?.message ?? 'It could not be sent just now. Please try again.' };
					}
				}
			: null
	);
	/** Opened on the Notes tab after a Go to lands. */
	let noteToShow: string | null = null;
	const myNotes = $derived<MyNotesOffer | null>(
		data.reader
			? {
					unseen,
					load: async () => {
						const res = await send(resolve('/api/reader/my-notes'), 'GET');
						const got: MyNotesData | null = res ? await res.json() : null;
						if (got) unseen = got.unseen;
						return got;
					},
					reading: async (subject, frame) => {
						if (subject === data.subject.id && bodies[frame]) return bodies[frame].readingHtml;
						const res = await fetch(resolve('/api/frame/[subject]/[frame]', { subject, frame }))
							.then((r) => (r.ok ? r : null))
							.catch(() => null);
						return res ? ((await res.json()) as ServedBody).readingHtml : null;
					},
					seen: async (ids) => {
						notes = notes.map((n) => (ids.includes(n.id) ? { ...n, unseen: false } : n));
						await see(ids);
					},
					flag: async (n, flag) => {
						const res = await send(resolve('/api/reader/notes'), 'PATCH', { id: n.id, flag });
						const saved: Note | null = res ? await res.json() : null;
						if (saved) notes = notes.map((x) => (x.id === saved.id ? saved : x));
						return saved;
					},
					clear: async (ids) => {
						const res = await send(resolve('/api/reader/notes'), 'DELETE', { ids });
						if (!res) return null;
						notes = notes.filter((n) => !ids.includes(n.id));
						return ((await res.json()) as { deleted: number }).deleted;
					},
					go: (n: NoteEntry) => {
						if (n.subject === data.subject.id && n.frame === current?.id) {
							shell?.showNote(n.id);
							return;
						}
						noteToShow = n.id;
						follow(n.subject, n.frame);
					},
					hrefOf: frameHref
				}
			: null
	);

	// A note with unsaved changes: leaving the subject, or the page, asks first.
	// Leaving for good (a reload, closing the tab) gets the browser's own question.
	beforeNavigate((nav) => {
		// Home keeps the subject, and the shell with the note in it.
		if (goingHome || !shell?.hasUnsavedNote()) return;
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
	let visitTimer: ReturnType<typeof setTimeout> | undefined;
	// Each subject's place as the reader's store has it (korg 3432): loaded
	// with the page, and moved here at once as the reader moves, so the start
	// screen never waits on the write. A later load keeps whichever is newer.
	let moved = $state<Record<string, Placed<Place>>>({});
	const places = $derived(newerPlaces(moved, data.readerData?.places ?? {}));
	$effect(() => {
		const f = current;
		// Home before five seconds is not a visit.
		if (!started || !f) return clearTimeout(visitTimer);
		const subject = data.subject.id;
		untrack(() => {
			const href = frameHref(subject, f.id);
			// The jumps that led here stay with the entry (§Connections).
			// A home entry the reader began from becomes the frame's (korg 3517).
			if (location.pathname !== href) replaceState(href, { ...page.state, home: undefined });
			if (!data.reader) return;
			const label = titleOf(f);
			const at = new Date().toISOString();
			moved = {
				...moved,
				[subject]: { subject, frame: f.id, label, at, subjectTitle: here.title }
			};
			clearTimeout(placeTimer);
			clearTimeout(visitTimer);
			placeTimer = setTimeout(async () => {
				if (!(await write(resolve('/api/reader/place'), 'POST', { subject, frame: f.id, label })))
					return;
				// A first place in a subject started it (§What's new).
				if (news && !news.readings[subject])
					news = {
						...news,
						readings: { ...news.readings, [subject]: { first: at, caughtUp: null } }
					};
			}, PLACE_MS);
			// Staying is a visit (§Traffic), and a visit opens the frame: a flick past does neither.
			visitTimer = setTimeout(async () => {
				if (await write(resolve('/api/reader/visit'), 'POST', { subject, frame: f.id }))
					seenHere(subject, [f.id]);
			}, VISIT_MS);
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
		const note = noteToShow;
		noteToShow = null;
		await tick();
		if (note && nav.type !== 'popstate') shell?.showNote(note);
		else shell?.focusSpine();
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
			goto(frameHref(subject, frame), { keepFocus: true });
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

	// The Changelog's entries: fetched when it first opens, and kept for the build.
	let changelog = $state<ReturnType<typeof Changelog>>();
	let changelogData: { build: string; got: Promise<ChangelogData | null> } | null = null;
	function loadChangelog() {
		if (changelogData?.build !== data.build)
			changelogData = {
				build: data.build,
				got: fetch(resolve('/api/changelog'))
					.then((res) => (res.ok ? (res.json() as Promise<ChangelogData>) : null))
					.catch(() => null)
			};
		const asked = changelogData;
		return asked.got.then((d) => {
			if (!d && changelogData === asked) changelogData = null;
			return d;
		});
	}
	const changelogOffer = $derived<ChangelogOffer>({
		load: loadChangelog,
		news,
		hrefOf: frameHref,
		onfollow: (subject, frame) => followFromMap(subject, frame),
		...(data.reader ? { onseen: markSeen, oncaughtup: caughtUp } : {})
	});

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
		ai={data.ai
			? {
					web: data.ai.askWeb,
					grow: !!data.ai.growModels,
					...(data.ai.budget ? { budget: data.ai.budget } : {})
				}
			: null}
		ongrown={() => {
			mapData = null;
			invalidateAll();
		}}
		active={started}
		startAt={data.frame}
		onplace={(f) => (current = f)}
		bookmarks={bookmarkOffer}
		{layer}
		{myNotes}
		onhome={home}
		hrefOf={(frame) => frameHref(data.subject.id, frame)}
		hrefTo={frameHref}
		onfollow={follow}
		back={backOffer}
		onmap={openMap}
		onrandom={random}
		fresh={data.reader ? { frames: freshHere, oncaughtup: () => caughtUp(data.subject.id) } : null}
		onchangelog={(refocus, palette) => changelog?.show({ refocus, palette })}
	/>
{/key}

<MapOverlay bind:this={map} load={loadMap} hrefOf={frameHref} onfollow={followFromMap} />
<Changelog bind:this={changelog} offer={changelogOffer} />

{#if !started}
	<StartScreen
		subjects={listed}
		bind:selected
		current={data.subject.id}
		subtitle={data.ai?.growModels
			? 'A timeline you can read, question and grow'
			: data.ai
				? 'A timeline you can read, annotate and question'
				: 'A timeline you can read and annotate'}
		{inscription}
		art={loom}
		credits={[loomCredit]}
		palette={startPalette}
		ring={look?.illustrations ?? []}
		{resume}
		onbegin={(closed) => {
			if (!closed) shell?.reading();
			begun = data.subject.id;
		}}
		onfirst={() => shell?.goTo(first)}
		onopen={open}
		onmap={(refocus) =>
			openMap({ target: { view: 'library' }, scheme: startPalette.scheme, refocus })}
		onchangelog={(refocus) => changelog?.show({ refocus, palette: startPalette })}
		fresh={freshLine}
		{settings}
		about={{ stats: loadStats, build: __KLOOM_BUILD__ || undefined, suggest, ask: !!data.ai }}
		help={resolve('/welcome')}
		guide={resolve('/guide')}
		traffic={data.admin ? resolve('/admin/traffic') : undefined}
		signOut={data.reader?.signedIn ? { action: resolve('/signout'), who: data.reader.name } : null}
	/>
{/if}

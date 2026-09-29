<script lang="ts">
	import { onMount, untrack } from 'svelte';
	import type { Frame } from '$engine/model';
	import type { Bookmark, JumpItem } from '$engine/reader-data';
	import Shell from '$engine/ui/Shell.svelte';
	import StartScreen from '$engine/ui/StartScreen.svelte';
	import { invalidateAll, replaceState } from '$app/navigation';
	import { resolve } from '$app/paths';
	import {
		ASK_MODEL,
		followSpine,
		GROW_MODEL,
		layout,
		modelSetting,
		paletteFor,
		paletteMode
	} from '$engine/settings';
	import { UserSettings } from '$engine/user-settings.svelte';
	import { inscription, loomCredit } from '$lib/start/credit';
	import type { PageProps } from './$types';

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
		...(growModels ? [modelSetting(GROW_MODEL, 'Grow model', growModels)] : [])
	]);

	// The start screen wears the first frame's palette, in the reader's mode.
	const first = $derived(data.subject.frames[data.subject.spine.segments[0].frames[0]]);
	const startPalette = $derived(
		paletteFor(data.subject, first.scene.palette, settings.get(paletteMode.id)!)
	);

	// The chooser: every other subject the app serves.
	const others = $derived(
		data.subjects
			.filter((s) => s.id !== data.subject.id)
			.map((s) => ({ title: s.title, href: resolve('/[subject]/[[frame]]', { subject: s.id }) }))
	);

	// The reader's own data (docs/design.md §Reader data, korg 3413, 3414).
	// Absent when there is no reader: nothing is kept, nothing is offered.
	let shell = $state<ReturnType<typeof Shell>>();
	let marks = $state<(Bookmark & { subjectTitle: string })[]>(
		untrack(() => data.readerData?.bookmarks ?? [])
	);
	const here = $derived(data.subjects.find((s) => s.id === data.subject.id)!);
	const titleOf = (f: Frame) => `${f.scene.headline} ${f.scene.accent}`;
	const frameHref = (subject: string, frame: string) =>
		resolve('/[subject]/[[frame]]', { subject, frame });

	/** Write to the reader's store; a failure is logged, and the reading goes on. */
	async function write(path: string, method: string, body: object) {
		const res = await fetch(path, {
			method,
			headers: { 'content-type': 'application/json' },
			body: JSON.stringify(body),
			keepalive: true
		}).catch(() => null);
		if (!res?.ok) console.warn(`reader data: ${method} ${path} failed`, res?.status);
		return !!res?.ok;
	}

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
	let current = $state<Frame | null>(null);
	let placeTimer: ReturnType<typeof setTimeout> | undefined;
	$effect(() => {
		const f = current;
		if (!started || !f) return;
		const subject = data.subject.id;
		untrack(() => {
			const href = frameHref(subject, f.id);
			if (location.pathname !== href) replaceState(href, {});
			if (!data.reader) return;
			clearTimeout(placeTimer);
			placeTimer = setTimeout(() => {
				write(resolve('/api/reader/place'), 'POST', { subject, frame: f.id, label: titleOf(f) });
			}, 800);
		});
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
								? data.subject.frames[m.frame].position.label
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

	async function toggleMark(f: Frame) {
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

	// Offered on the start screen: this subject's place, and the last place
	// anywhere when that was another subject.
	const resume = $derived.by(() => {
		const r = data.readerData;
		const offers = [];
		const f = r?.here && data.subject.frames[r.here.frame];
		if (f)
			offers.push({
				key: 'here',
				action: 'Continue where you were',
				label: `${titleOf(f)} · ${f.position.label}`,
				onpick: () => shell?.goTo(f.id)
			});
		if (r?.last)
			offers.push({
				key: 'last',
				action: `Last read · ${r.last.subjectTitle}`,
				label: r.last.label,
				href: frameHref(r.last.subject, r.last.frame)
			});
		return offers;
	});

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
		{settings}
		ai={{ web: data.askWeb, grow: !!data.growModels }}
		ongrown={() => invalidateAll()}
		active={started}
		startAt={data.frame}
		onplace={(f) => (current = f)}
		bookmarks={bookmarkOffer}
	/>
{/key}

{#if !started}
	<StartScreen
		title={data.subject.title}
		subtitle="A timeline you can read, question and grow"
		{inscription}
		art={loom}
		credits={[loomCredit]}
		palette={startPalette}
		{others}
		{resume}
		onbegin={() => (begun = data.subject.id)}
	/>
{/if}

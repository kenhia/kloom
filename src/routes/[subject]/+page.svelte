<script lang="ts">
	import { onMount, untrack } from 'svelte';
	import Shell from '$engine/ui/Shell.svelte';
	import StartScreen from '$engine/ui/StartScreen.svelte';
	import { invalidateAll } from '$app/navigation';
	import { resolve } from '$app/paths';
	import {
		ASK_MODEL,
		followSpine,
		GROW_MODEL,
		modelSetting,
		paletteFor,
		paletteMode
	} from '$engine/settings';
	import { UserSettings } from '$engine/user-settings.svelte';
	import { inscription, loomCredit } from '$lib/start/credit';
	import type { PageProps } from './$types';

	let { data }: PageProps = $props();

	// Begun per subject: opening another one shows its start screen first.
	let begun = $state<string | null>(null);
	const started = $derived(begun === data.subject.id);
	let loom = $state<string | null>(null);

	// The reader's settings. The ask and grow models' choices come from the app
	// config, once per page load.
	const growModels = untrack(() => data.growModels);
	const settings = new UserSettings([
		paletteMode,
		followSpine,
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
			.map((s) => ({ title: s.title, href: resolve('/[subject]', { subject: s.id }) }))
	);

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
		subject={data.subject}
		{settings}
		ai={{ web: data.askWeb, grow: !!data.growModels }}
		ongrown={() => invalidateAll()}
		active={started}
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
		onbegin={() => (begun = data.subject.id)}
	/>
{/if}

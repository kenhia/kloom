<script lang="ts">
	import { onMount } from 'svelte';
	import Shell from '$engine/ui/Shell.svelte';
	import StartScreen from '$engine/ui/StartScreen.svelte';
	import { paletteFor, paletteMode } from '$engine/settings';
	import { UserSettings } from '$engine/user-settings.svelte';
	import { inscription, loomCredit } from '$lib/start/credit';
	import type { PageProps } from './$types';

	let { data }: PageProps = $props();

	let started = $state(false);
	let loom = $state<string | null>(null);

	// The reader's settings: the palette mode for now; ask and grow add their models.
	const settings = new UserSettings([paletteMode]);

	// The start screen wears the first frame's palette, in the reader's mode.
	const first = $derived(data.subject.frames[data.subject.spine.segments[0].frames[0]]);
	const startPalette = $derived(
		paletteFor(data.subject, first.scene.palette, settings.get(paletteMode.id)!)
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

<Shell subject={data.subject} {settings} active={started} />

{#if !started}
	<StartScreen
		title={data.subject.title}
		subtitle="A timeline you can read, question and grow"
		{inscription}
		art={loom}
		credits={[loomCredit]}
		palette={startPalette}
		onbegin={() => (started = true)}
	/>
{/if}

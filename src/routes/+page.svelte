<script lang="ts">
	import { onMount } from 'svelte';
	import Shell from '$engine/ui/Shell.svelte';
	import StartScreen from '$engine/ui/StartScreen.svelte';
	import { inscription, loomCredit } from '$lib/start/credit';
	import type { PageProps } from './$types';

	let { data }: PageProps = $props();

	let started = $state(false);
	let loom = $state<string | null>(null);

	// The start screen wears the first frame's palette.
	const first = $derived(data.subject.frames[data.subject.spine.segments[0].frames[0]]);

	// Large, so it arrives after the page as its own compressed chunk.
	onMount(async () => {
		loom = (await import('$lib/start/loom.svg?raw')).default;
	});
</script>

<svelte:head>
	<title>kloom · {data.subject.title}</title>
</svelte:head>

<Shell subject={data.subject} active={started} />

{#if !started}
	<StartScreen
		title={data.subject.title}
		subtitle="A timeline you can read, question and grow"
		{inscription}
		art={loom}
		credits={[loomCredit]}
		palette={data.subject.palettes[first.scene.palette]}
		onbegin={() => (started = true)}
	/>
{/if}

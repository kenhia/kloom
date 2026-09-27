<script lang="ts">
	import Shell from '$engine/ui/Shell.svelte';
	import type { PageProps } from './$types';

	let { data }: PageProps = $props();
</script>

<svelte:head>
	<title>kloom · {data.subject.title}</title>
</svelte:head>

<Shell subject={data.subject} />

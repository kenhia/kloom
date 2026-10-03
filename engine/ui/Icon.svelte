<script lang="ts" module>
	/** The shell's icons: each control draws its own from here, and so does the User's Guide (korg 3515). */
	export type IconName =
		| 'contents'
		| 'map'
		| 'bookmark'
		| 'bookmarks'
		| 'my-notes'
		| 'random'
		| 'anywhere'
		| 'home'
		| 'settings'
		| 'about'
		| 'whats-new';
</script>

<script lang="ts">
	import homeIcon from './icons/home.svg?raw';

	interface Props {
		name: IconName;
		/** The bookmark filled in: this frame is marked. */
		filled?: boolean;
	}

	let { name, filled = false }: Props = $props();

	/** The gear's teeth, every 45°. */
	const ticks = [0, 45, 90, 135, 180, 225, 270, 315];
</script>

<!-- 24×24, stroked in currentColor, hidden from assistive technology: the control names itself. -->
{#if name === 'home'}
	<!-- kloom's own icon, from the repository (engine/ui/icons). -->
	<!-- eslint-disable-next-line svelte/no-at-html-tags -->
	{@html homeIcon}
{:else if name === 'bookmark'}
	<svg viewBox="0 0 24 24" aria-hidden="true" fill={filled ? 'currentColor' : 'none'}>
		<path d="M6.5 3.5h11v17l-5.5-4.25-5.5 4.25z" stroke="currentColor" stroke-width="1.5" />
	</svg>
{:else}
	<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor">
		{#if name === 'contents'}
			<path d="M4 6h2M9 6h11M4 12h2M9 12h11M11 18h9" stroke-width="1.5" />
		{:else if name === 'map'}
			<circle cx="12" cy="12" r="2.5" stroke-width="1.5" />
			<circle cx="5" cy="6" r="1.75" stroke-width="1.5" />
			<circle cx="19" cy="7" r="1.75" stroke-width="1.5" />
			<circle cx="17" cy="19" r="1.75" stroke-width="1.5" />
			<path d="M6.5 7 10 10.5M17.4 7.9 14.2 10.8M13.6 14 16 17.5" stroke-width="1.5" />
		{:else if name === 'bookmarks'}
			<path d="M4 6.5h16M4 12h16M4 17.5h10" stroke-width="1.5" />
		{:else if name === 'my-notes'}
			<path d="M6 3.5h8.5l3.5 3.5v13.5H6z" stroke-width="1.5" />
			<path d="M9 10.5h6M9 13.5h6M9 16.5h4" stroke-width="1.5" />
		{:else if name === 'random'}
			<!-- One die: here. -->
			<rect x="4.5" y="4.5" width="15" height="15" rx="2.5" stroke-width="1.5" />
			<circle cx="9" cy="9" r="1.1" fill="currentColor" stroke="none" />
			<circle cx="12" cy="12" r="1.1" fill="currentColor" stroke="none" />
			<circle cx="15" cy="15" r="1.1" fill="currentColor" stroke="none" />
		{:else if name === 'anywhere'}
			<!-- Two dice: anywhere. -->
			<rect x="2.5" y="8.5" width="11" height="11" rx="2" stroke-width="1.5" />
			<path d="M10.5 8.5V6.5a2 2 0 0 1 2-2h7a2 2 0 0 1 2 2v7a2 2 0 0 1-2 2h-6" stroke-width="1.5" />
			<circle cx="5.75" cy="11.75" r="1" fill="currentColor" stroke="none" />
			<circle cx="10.25" cy="16.25" r="1" fill="currentColor" stroke="none" />
			<circle cx="17.5" cy="8.5" r="1" fill="currentColor" stroke="none" />
		{:else if name === 'settings'}
			<circle cx="12" cy="12" r="6.25" stroke-width="1.5" />
			<circle cx="12" cy="12" r="2.25" stroke-width="1.25" />
			{#each ticks as a (a)}
				<line
					x1="12"
					y1="2.25"
					x2="12"
					y2="5.75"
					stroke-width="2.5"
					transform="rotate({a} 12 12)"
				/>
			{/each}
		{:else if name === 'whats-new'}
			<!-- What's new: a spark, as the spine marks a frame new to the reader. -->
			<path
				d="M10 3.5 11.6 8.4 16.5 10 11.6 11.6 10 16.5 8.4 11.6 3.5 10 8.4 8.4z"
				stroke-width="1.5"
				stroke-linejoin="round"
			/>
			<path d="M17.5 14.5v6M14.5 17.5h6" stroke-width="1.5" />
		{:else if name === 'about'}
			<circle cx="12" cy="12" r="9" stroke-width="1.5" />
			<line x1="12" y1="10.5" x2="12" y2="17" stroke-width="1.75" />
			<circle cx="12" cy="7.25" r="0.6" fill="currentColor" stroke-width="1" />
		{/if}
	</svg>
{/if}

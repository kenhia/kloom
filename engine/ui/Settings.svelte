<script lang="ts">
	import type { UserSettings } from '../user-settings.svelte';
	import IconButton from './IconButton.svelte';

	interface Props {
		settings: UserSettings;
		/** Things to say about the choices as they stand (two shortcuts on one key, say). */
		warnings?: string[];
	}

	let { settings, warnings = [] }: Props = $props();

	const id = $props.id();
	let open = $state(false);
	let root = $state<HTMLElement>();
	let gear = $state<IconButton>();

	function close(refocus: boolean) {
		open = false;
		if (refocus) gear?.focus();
	}

	/**
	 * Esc closes the pop-up and returns focus to the gear. Handled on the
	 * controls themselves, which run before the shell's page-wide keys, so the
	 * default being prevented stops Esc also leaving a trail.
	 */
	function escape(e: KeyboardEvent) {
		if (e.key !== 'Escape' || !open) return;
		e.preventDefault();
		close(true);
	}

	function outside(e: PointerEvent) {
		if (open && !root?.contains(e.target as Node)) close(false);
	}

	const ticks = [0, 45, 90, 135, 180, 225, 270, 315];
</script>

<svelte:window onpointerdown={outside} />

<div class="settings" bind:this={root}>
	<IconButton
		class="gear"
		label="Settings"
		aria-expanded={open}
		aria-controls="{id}-panel"
		bind:this={gear}
		onclick={() => (open = !open)}
		onkeydown={escape}
	>
		<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor">
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
		</svg>
	</IconButton>

	<!-- The page's own keys (arrows and the shortcuts) stand down in here: data-own-keys. -->
	<div
		id="{id}-panel"
		class="panel"
		role="group"
		aria-labelledby="{id}-title"
		data-own-keys
		hidden={!open}
	>
		<p id="{id}-title" class="title">Settings</p>
		{#each settings.list as setting, i (setting.id)}
			{#if setting.group && setting.group !== settings.list[i - 1]?.group}
				<p class="group">{setting.group}</p>
			{/if}
			<label for="{id}-{setting.id}">{setting.label}</label>
			<select
				id="{id}-{setting.id}"
				value={settings.get(setting.id)}
				onchange={(e) => settings.set(setting.id, e.currentTarget.value)}
				onkeydown={escape}
			>
				{#each setting.choices as choice (choice.value)}
					<option value={choice.value}>{choice.label}</option>
				{/each}
			</select>
		{/each}
		{#each warnings as w (w)}
			<p class="warning" role="status">{w}</p>
		{/each}
		<p class="note">Remembered in this browser.</p>
	</div>
</div>

<style>
	.settings {
		position: relative;
		margin-left: auto;
	}
	.panel {
		position: absolute;
		top: calc(100% + 0.35rem);
		right: 0;
		z-index: 5;
		display: grid;
		grid-template-columns: auto 1fr;
		align-items: center;
		gap: 0.5rem 0.75rem;
		width: max-content;
		max-width: min(22rem, calc(100vw - 2rem));
		max-height: min(32rem, calc(100dvh - 6rem));
		overflow-y: auto;
		padding: 0.75rem 1rem;
		color: var(--ink);
		background: var(--background);
		border: 1px solid var(--muted);
		border-radius: 0.25rem;
		box-shadow: 0 0.5rem 1.5rem color-mix(in srgb, #000 35%, transparent);
	}
	.panel[hidden] {
		display: none;
	}
	.title,
	.group,
	.note,
	.warning {
		grid-column: 1 / -1;
		margin: 0;
	}
	.group {
		margin-top: 0.35rem;
		padding-top: 0.5rem;
		border-top: 1px solid color-mix(in srgb, var(--muted) 40%, transparent);
	}
	.warning {
		font-size: 0.8rem;
		color: var(--accent);
	}
	.title,
	.group {
		font-family: var(--mono);
		font-size: 0.75rem;
		letter-spacing: 0.12em;
		text-transform: uppercase;
		color: var(--muted);
	}
	.note {
		font-size: 0.75rem;
		color: var(--muted);
	}
	select {
		font: inherit;
		min-width: 0;
		padding: 0.25rem 0.4rem;
		color: var(--ink);
		background: var(--background);
		border: 1px solid var(--muted);
		border-radius: 0.25rem;
	}
</style>

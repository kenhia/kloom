<script lang="ts">
	import Icon from './Icon.svelte';
	import type { Setting } from '../settings';
	import type { UserSettings } from '../user-settings.svelte';
	import IconButton from './IconButton.svelte';
	import KeysDialog from './KeysDialog.svelte';

	interface Props {
		settings: UserSettings;
	}

	let { settings }: Props = $props();
	let keysDialog = $state<KeysDialog>();

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

	/** The rows in the open, and those kept under Advanced (korg 3495). */
	const plain = $derived(settings.list.filter((s) => !s.advanced));
	const advanced = $derived(settings.list.filter((s) => s.advanced));

	/** A slider's position: the index of the current choice. */
	const at = (s: Setting) =>
		Math.max(
			0,
			s.choices.findIndex((c) => c.value === settings.get(s.id))
		);
</script>

<svelte:window onpointerdown={outside} />

<!-- One setting: a labelled drop-down, or a slider over its choices in order. -->
{#snippet row(setting: Setting)}
	<label for="{id}-{setting.id}">{setting.label}</label>
	{#if setting.control === 'range'}
		{@const i = at(setting)}
		<div class="range">
			<input
				id="{id}-{setting.id}"
				type="range"
				min="0"
				max={setting.choices.length - 1}
				step="1"
				value={i}
				aria-valuetext={setting.choices[i].label}
				aria-describedby="{id}-{setting.id}-said"
				oninput={(e) => settings.set(setting.id, setting.choices[+e.currentTarget.value].value)}
				onkeydown={escape}
			/>
			<output id="{id}-{setting.id}-said" for="{id}-{setting.id}">{setting.choices[i].label}</output
			>
		</div>
	{:else}
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
	{/if}
{/snippet}

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
		<Icon name="settings" />
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
		{#each plain as setting, i (setting.id)}
			{#if setting.group && setting.group !== plain[i - 1]?.group}
				<p class="group">{setting.group}</p>
			{/if}
			{@render row(setting)}
		{/each}
		{#if advanced.length}
			<details class="advanced">
				<summary onkeydown={escape}>Advanced</summary>
				<div class="rows">
					{#each advanced as setting (setting.id)}
						{@render row(setting)}
					{/each}
				</div>
			</details>
		{/if}
		<button
			type="button"
			class="keys"
			aria-haspopup="dialog"
			onclick={() => keysDialog?.show()}
			onkeydown={escape}>Keyboard shortcuts…</button
		>
		<p class="note">Remembered in this browser.</p>
	</div>
	<KeysDialog keys={settings.keys} bind:this={keysDialog} />
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
		box-sizing: border-box;
		display: grid;
		/* Labels wrap rather than set the width; a select never goes below its minimum. */
		grid-template-columns: minmax(0, auto) minmax(9rem, max-content);
		align-items: center;
		gap: 0.5rem 0.75rem;
		width: max-content;
		max-width: min(24rem, calc(100vw - 2rem));
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
	.keys,
	.advanced {
		grid-column: 1 / -1;
		margin: 0;
	}
	label {
		min-width: 0;
		overflow-wrap: break-word;
	}
	.group {
		margin-top: 0.35rem;
		padding-top: 0.5rem;
		border-top: 1px solid color-mix(in srgb, var(--muted) 40%, transparent);
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
		width: 100%;
		min-width: 9rem;
		padding: 0.25rem 0.4rem;
		color: var(--ink);
		background: var(--background);
		border: 1px solid var(--muted);
		border-radius: 0.25rem;
	}
	/* Advanced keeps the panel's two columns for its own rows. */
	.advanced .rows {
		display: grid;
		grid-template-columns: minmax(0, auto) minmax(9rem, max-content);
		align-items: center;
		gap: 0.5rem 0.75rem;
		margin-top: 0.5rem;
	}
	summary {
		width: max-content;
		cursor: pointer;
		font-family: var(--mono);
		font-size: 0.75rem;
		letter-spacing: 0.12em;
		text-transform: uppercase;
		color: var(--muted);
	}
	.range {
		display: grid;
		gap: 0.15rem;
		min-width: 9rem;
	}
	input[type='range'] {
		width: 100%;
		margin: 0;
		accent-color: var(--accent);
	}
	output {
		font-size: 0.75rem;
		color: var(--muted);
	}
	.keys {
		justify-self: start;
		margin-top: 0.35rem;
		font: inherit;
		padding: 0.25rem 0.6rem;
		color: var(--ink);
		background: none;
		border: 1px solid var(--muted);
		border-radius: 0.25rem;
		cursor: pointer;
	}
</style>

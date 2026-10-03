<script lang="ts">
	import { onMount, tick } from 'svelte';
	import {
		bindingOf,
		FIXED_KEYS,
		keyName,
		modified,
		onMac,
		plain,
		reserved,
		sameBinding,
		SHORTCUTS,
		type Binding,
		type Shortcut
	} from '../keys';
	import { keyWarnings } from '../settings';
	import type { UserKeys } from '../user-settings.svelte';

	interface Props {
		keys: UserKeys;
	}

	let { keys }: Props = $props();

	const id = $props.id();
	let dialog = $state<HTMLDialogElement>();
	/** Rendered only while open: nothing of it is in the page until it is wanted. */
	let open = $state(false);
	let mac = $state(false);
	onMount(() => (mac = onMac()));

	/** The shortcut whose new keys are being listened for. */
	let capturing = $state<Shortcut | null>(null);
	/** Keys pressed for one shortcut that another already has: swap, share or cancel. */
	let clash = $state<{ action: Shortcut; binding: Binding; other: Shortcut } | null>(null);
	/** Said after each step, and announced. */
	let said = $state('');

	const warnings = $derived(keyWarnings(keys.map, mac));
	const labelOf = (a: Shortcut) => SHORTCUTS.find((s) => s.action === a)!.label;
	const sentence = (a: Shortcut) => labelOf(a)[0].toUpperCase() + labelOf(a).slice(1);
	const name = (b: Binding) => keyName(b, mac);

	/** Open the dialog on the first shortcut's Change button. Closing returns focus to the opener. */
	export async function show() {
		if (!dialog || dialog.open) return;
		capturing = null;
		clash = null;
		said = '';
		open = true;
		dialog.showModal();
		await tick();
		focusRow(SHORTCUTS[0].action, 'change');
	}

	function focusRow(action: Shortcut, button: 'change' | 'swap') {
		dialog?.querySelector<HTMLElement>(`[data-row="${action}"] [data-${button}]`)?.focus();
	}

	function startCapture(action: Shortcut) {
		clash = null;
		capturing = action;
		said = `Press the new keys for ${labelOf(action)}, or Escape to cancel.`;
	}

	function stopCapture(message: string) {
		const action = capturing;
		capturing = null;
		said = message;
		if (action) focusRow(action, 'change');
	}

	function bind(action: Shortcut, binding: Binding | null) {
		keys.set(action, binding);
		said = binding ? `${sentence(action)} is now ${name(binding)}.` : `${sentence(action)} is off.`;
	}

	/**
	 * While a shortcut is listening, a key press is its new binding, never
	 * anything else: handled here, in the capture phase, before the dialog or
	 * the page sees it. Esc cancels and Tab moves on, so the listening can
	 * never trap focus.
	 */
	function capture(e: KeyboardEvent) {
		const action = capturing;
		if (!action) return;
		if (e.key === 'Tab') {
			capturing = null;
			said = 'Not changed.';
			return;
		}
		e.preventDefault();
		e.stopPropagation();
		if (e.key === 'Escape') return stopCapture(`${sentence(action)} not changed.`);
		if (['Shift', 'Alt', 'Control', 'Meta', 'AltGraph', 'CapsLock'].includes(e.key)) return;
		const binding = bindingOf(e);
		if (!binding) {
			said = `${e.key === ' ' ? 'Space' : e.key} cannot be a shortcut: use a letter, a digit or F1 to F12, with any modifiers. Or press Escape to cancel.`;
			return;
		}
		const refused = reserved(binding, mac);
		if (refused) {
			said = `${refused} Try other keys, or press Escape to cancel.`;
			return;
		}
		capturing = null;
		const other = SHORTCUTS.find(
			(s) => s.action !== action && sameBinding(keys.map[s.action], binding)
		)?.action;
		if (other) {
			clash = { action, binding, other };
			said = `${name(binding)} is already set to ${labelOf(other)}. Swap, use it for both, or cancel.`;
			tick().then(() => focusRow(action, 'swap'));
			return;
		}
		bind(action, binding);
		focusRow(action, 'change');
	}

	/** The other shortcut takes this one's old keys, or goes off when it had none. */
	function swap() {
		if (!clash) return;
		const { action, binding, other } = clash;
		const old = keys.map[action];
		clash = null;
		keys.set(other, old);
		keys.set(action, binding);
		said = `${sentence(action)} is now ${name(binding)}; ${labelOf(other)} is ${old ? `now ${name(old)}` : 'off'}.`;
		focusRow(action, 'change');
	}

	function share() {
		if (!clash) return;
		const { action, binding } = clash;
		clash = null;
		bind(action, binding);
		focusRow(action, 'change');
	}

	function cancelClash() {
		if (!clash) return;
		const { action } = clash;
		clash = null;
		said = `${sentence(action)} not changed.`;
		focusRow(action, 'change');
	}

	/** Esc while listening cancels the listening, not the dialog. */
	function cancel(e: Event) {
		if (capturing) e.preventDefault();
	}

	function resetAll() {
		keys.resetAll();
		clash = null;
		said = 'Every shortcut is back to its key out of the box.';
	}

	/** Keycaps for a binding: one per key. */
	const caps = (b: Binding) => name(b).split('+');
</script>

<!-- A modal, like My notes: the page behind is inert and its keys stand down. -->
<dialog
	class="keys-dialog"
	aria-labelledby="{id}-title"
	aria-describedby="{id}-about"
	data-own-keys
	bind:this={dialog}
	onkeydowncapture={capture}
	oncancel={cancel}
	onclose={() => {
		open = false;
		capturing = null;
		clash = null;
	}}
>
	{#if open}
		<header>
			<h2 id="{id}-title">Keyboard shortcuts</h2>
			<button type="button" class="close" onclick={() => dialog?.close()}>
				<span aria-hidden="true">×</span>
				<span class="visually-hidden">Close keyboard shortcuts</span>
			</button>
		</header>

		<p id="{id}-about" class="about">
			Change a shortcut, then press its new keys: a letter, a digit or F1 to F12, with Shift, {mac
				? 'Option'
				: 'Alt'}, Ctrl or {mac ? 'Cmd' : 'Meta'} if you like. Without {mac ? 'Option' : 'Alt'}, Ctrl
			or {mac ? 'Cmd' : 'Meta'} a shortcut works while you are in the spine, the reading or your notes;
			with one, it works anywhere on the page but a text box.
		</p>

		<ul class="rows">
			{#each SHORTCUTS as s (s.action)}
				{@const b = keys.map[s.action]}
				<li data-row={s.action} class:listening={capturing === s.action}>
					<span class="label" id="{id}-{s.action}">{sentence(s.action)}</span>
					<span class="binding">
						{#if capturing === s.action}
							<span class="listening-text">Press keys…</span>
						{:else if b}
							{#each caps(b) as cap, i (i)}{#if i}<span aria-hidden="true">+</span>{/if}<kbd
									>{cap}</kbd
								>{/each}
							{#if modified(b)}<span class="where">anywhere</span>{/if}
						{:else}
							<span class="off">Off</span>
						{/if}
					</span>
					<span class="actions">
						<button
							type="button"
							data-change
							aria-describedby="{id}-{s.action}"
							aria-pressed={capturing === s.action}
							onclick={() =>
								capturing === s.action ? stopCapture('Not changed.') : startCapture(s.action)}
							>Change</button
						>
						<button
							type="button"
							aria-describedby="{id}-{s.action}"
							disabled={!b}
							onclick={() => bind(s.action, null)}>Off</button
						>
						<button
							type="button"
							aria-describedby="{id}-{s.action}"
							disabled={sameBinding(b, plain(s.key))}
							onclick={() => {
								keys.reset(s.action);
								said = `${sentence(s.action)} is back to ${s.key.toUpperCase()}.`;
							}}>Reset</button
						>
					</span>
					{#if clash?.action === s.action}
						<span class="clash">
							{name(clash.binding)} is already set to {labelOf(clash.other)}.
							<button type="button" data-swap onclick={swap}>Swap</button>
							<button type="button" onclick={share}>Use for both</button>
							<button type="button" onclick={cancelClash}>Cancel</button>
						</span>
					{/if}
				</li>
			{/each}
		</ul>

		<p class="said" role="status" aria-live="polite">{said}</p>
		{#each warnings as w (w)}
			<p class="warning">{w}</p>
		{/each}

		<section class="fixed" aria-labelledby="{id}-fixed">
			<h3 id="{id}-fixed">Kept by kloom, not changeable</h3>
			<dl>
				{#each FIXED_KEYS as f (f.keys)}
					<div>
						<dt>{f.keys}</dt>
						<dd>{f.does}</dd>
					</div>
				{/each}
			</dl>
		</section>

		<footer>
			<button type="button" onclick={resetAll}>Reset all to defaults</button>
			<button type="button" onclick={() => dialog?.close()}>Done</button>
		</footer>
	{/if}
</dialog>

<style>
	.keys-dialog {
		width: min(40rem, calc(100vw - 1rem));
		max-height: calc(100dvh - 1rem);
		box-sizing: border-box;
		padding: 0;
		font-family: var(--sans, inherit);
		font-size: 0.9rem;
		text-align: left;
		text-transform: none;
		letter-spacing: 0;
		color: var(--ink);
		background: var(--background);
		border: 1px solid var(--muted);
		border-radius: 0.25rem;
		box-shadow: 0 0.5rem 1.5rem color-mix(in srgb, #000 35%, transparent);
	}
	.keys-dialog::backdrop {
		background: rgb(0 0 0 / 0.5);
	}
	header,
	footer {
		display: flex;
		flex-wrap: wrap;
		align-items: center;
		justify-content: space-between;
		gap: 0.5rem 1rem;
		padding: 0.75rem 1rem;
	}
	header {
		border-bottom: 1px solid color-mix(in srgb, var(--muted) 40%, transparent);
	}
	footer {
		border-top: 1px solid color-mix(in srgb, var(--muted) 40%, transparent);
	}
	h2,
	h3 {
		margin: 0;
		font-family: var(--mono);
		font-size: 0.75rem;
		font-weight: normal;
		letter-spacing: 0.12em;
		text-transform: uppercase;
		color: var(--muted);
	}
	.about,
	.said,
	.warning,
	.fixed {
		margin: 0.6rem 1rem;
	}
	.about,
	.fixed {
		color: var(--muted);
	}
	.said {
		min-height: 1.2em;
	}
	.warning {
		font-size: 0.8rem;
		color: var(--accent);
	}
	.rows {
		margin: 0;
		padding: 0 1rem;
		list-style: none;
	}
	.rows li {
		display: grid;
		grid-template-columns: minmax(0, 1fr) auto;
		grid-template-areas: 'label binding' 'actions actions';
		align-items: center;
		gap: 0.3rem 0.75rem;
		padding: 0.45rem 0;
		border-bottom: 1px solid color-mix(in srgb, var(--muted) 25%, transparent);
	}
	@media (min-width: 34rem) {
		.rows li {
			grid-template-columns: minmax(0, 1fr) 9rem auto;
			grid-template-areas: 'label binding actions';
		}
	}
	.label {
		grid-area: label;
	}
	.binding {
		grid-area: binding;
		display: flex;
		flex-wrap: wrap;
		align-items: center;
		gap: 0.15rem;
	}
	.actions {
		grid-area: actions;
		display: flex;
		gap: 0.35rem;
	}
	.clash {
		grid-column: 1 / -1;
		display: flex;
		flex-wrap: wrap;
		align-items: center;
		gap: 0.35rem 0.5rem;
		color: var(--accent);
	}
	.listening .listening-text {
		font-style: italic;
		color: var(--accent);
	}
	kbd {
		font: 0.8rem/1 var(--mono);
		padding: 0.2rem 0.35rem;
		border: 1px solid var(--muted);
		border-bottom-width: 2px;
		border-radius: 0.2rem;
	}
	.off,
	.where {
		font-size: 0.8rem;
		color: var(--muted);
	}
	.where {
		margin-left: 0.3rem;
	}
	button {
		font: inherit;
		color: var(--ink);
		background: none;
		border: 1px solid var(--muted);
		border-radius: 0.25rem;
		padding: 0.2rem 0.6rem;
		cursor: pointer;
	}
	button:disabled {
		color: var(--muted);
		cursor: default;
		opacity: 0.6;
	}
	button[aria-pressed='true'] {
		border-color: var(--accent);
	}
	.close {
		font: 1.1rem/1 var(--serif, inherit);
		border-color: transparent;
	}
	.close:hover {
		border-color: var(--muted);
	}
	dl {
		margin: 0.4rem 0 0;
	}
	dl div {
		display: flex;
		flex-wrap: wrap;
		gap: 0 0.6rem;
	}
	dt {
		min-width: 5rem;
		font-family: var(--mono);
		color: var(--ink);
	}
	dd {
		margin: 0;
	}
</style>

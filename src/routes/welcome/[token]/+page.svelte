<script lang="ts">
	import { resolve } from '$app/paths';
	import Plain from '$lib/page/Plain.svelte';
	import type { PageProps } from './$types';

	let { data, form }: PageProps = $props();
</script>

{#if data.invited}
	<Plain title="Welcome">
		<h1>Hi {data.invited.name}</h1>
		<p>
			Choose a password for kloom. You will use it with your username to sign in on another phone or
			computer. On this one, you stay signed in.
		</p>
		{#if form?.message}
			<p class="problem" role="alert">{form.message}</p>
		{/if}
		<form method="POST">
			<label>
				Password
				<input
					name="password"
					type="password"
					autocomplete="new-password"
					minlength={data.min}
					required
					aria-describedby="password-hint"
				/>
			</label>
			<p id="password-hint" class="hint">At least {data.min} characters.</p>
			<label>
				The same password again
				<input
					name="confirm"
					type="password"
					autocomplete="new-password"
					minlength={data.min}
					required
				/>
			</label>
			<button type="submit">Choose this password</button>
		</form>
	</Plain>
{:else}
	<Plain title="Link used">
		<h1>This link will not work now</h1>
		{#if form?.message}
			<p class="problem" role="alert">{form.message}</p>
		{/if}
		<p>
			A welcome link works once, for a week. This one has been used or has run out. Ask Ken for a
			new one.
		</p>
		<p>If you already chose a password, <a href={resolve('/signin')}>sign in</a> with it.</p>
	</Plain>
{/if}

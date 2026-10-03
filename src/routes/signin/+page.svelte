<script lang="ts">
	import Plain from '$lib/page/Plain.svelte';
	import type { PageProps } from './$types';

	let { data, form }: PageProps = $props();
</script>

<Plain title="Sign in">
	<h1>Sign in</h1>
	<p>kloom is for invited readers. Sign in with the username and password you chose.</p>
	{#if form?.message}
		<p class="problem" role="alert">{form.message}</p>
	{/if}
	<form method="POST">
		<input type="hidden" name="next" value={data.next} />
		<label>
			Username
			<input
				name="username"
				autocomplete="username"
				autocapitalize="none"
				spellcheck="false"
				required
				value={form?.username ?? ''}
			/>
		</label>
		<label>
			Password
			<input name="password" type="password" autocomplete="current-password" required />
		</label>
		<button type="submit">Sign in</button>
	</form>
	<p class="hint">
		Forgotten your password, or never had one? Ask Ken for a new welcome link. It lets you choose a
		password again.
	</p>
</Plain>

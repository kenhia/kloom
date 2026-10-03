<script lang="ts">
	import { resolve } from '$app/paths';
	import Plain from '$lib/page/Plain.svelte';
	import type { PageProps } from './$types';

	let { data }: PageProps = $props();

	/** The public site (the reader edition) has no asking or growing (korg 3500). */
	const full = __KLOOM_EDITION__ !== 'reader';
</script>

<!--
	The Welcome and How-To page (korg 3502). Written for readers who are not
	technical, and for a login two people may share: it says "you", never
	"you alone". Short sections, so it reads on a phone with large text. The
	first visit only (korg 3515): every control is in the User's Guide, and
	Agent review keeps its full statement here.
-->
<Plain title="Welcome">
	<h1>Welcome{data.reader?.signedIn ? `, ${data.reader.name}` : ''}</h1>
	<p>
		kloom is a shelf of illustrated histories. Each subject is told one frame at a time: a picture,
		and a short reading about it.
	</p>
	<p>
		<a href={resolve('/')}>Start reading</a>, or read on for the few things worth knowing first. The
		<a href={resolve('/guide')}>User's Guide</a> explains every button, the map and notes in full.
	</p>

	<h2>Reading</h2>
	<ul>
		<li>
			The <strong>spine</strong> is the picture side. Move along it with the
			<strong>‹</strong> and <strong>›</strong> buttons under the picture, or tap or drag the bar
			between them. On a keyboard, <kbd>←</kbd> and <kbd>→</kbd> do the same.
		</li>
		<li>
			The <strong>reading</strong> sits beside the picture, or below it on a phone, and follows the spine.
		</li>
		<li>
			The buttons over the picture open the contents, the map, your bookmarks and your notes. The
			<a href={resolve('/guide#buttons')}>User's Guide</a> shows each one.
		</li>
	</ul>

	<h2>Notes</h2>
	<ul>
		<li>
			Write a <strong>note</strong> on a frame from the <strong>Notes</strong> tab beside the
			reading, or an <strong>annotation</strong> on particular words by selecting them and choosing "Annotate".
		</li>
		<li>
			Your notes, bookmarks and places are <strong>private to your login</strong>. Other readers
			cannot see them. If two of you share a login, you share them with each other.
		</li>
	</ul>

	<h2>"Agent review": telling Ken about a problem</h2>
	<p>
		When you write a note (or annotation), you will see a box called <strong>Agent review</strong>.
		Please read this before you tick it.
	</p>
	<ul>
		<li>
			Ticking it <strong>sends that note to Ken and to the AI agents Ken works with</strong>. They
			read it. A note you leave unticked stays private.
		</li>
		<li>
			This is how mistakes in kloom get fixed. If something looks wrong, unclear or missing, a
			ticked note is the best way to say so.
		</li>
		<li>
			An answer may come back on the note itself. My notes shows a count when one is waiting for
			you.
		</li>
	</ul>
	<p>
		kloom is written by AI agents working from sources, and reviewed, but mistakes get through.
		<strong>About</strong>, at the top right of the start screen, says more in its note on accuracy,
		and has another way to report a problem.
	</p>

	{#if full}
		<h2>Asking and growing</h2>
		<p>
			On this copy of kloom the AI pane can also answer a question about the frame you are on (Ask),
			or write new frames and trails (Grow). Grown frames are reviewed before they become part of
			the subject.
		</p>
	{/if}

	{#if data.reader?.signedIn}
		<h2>Signing in and out</h2>
		<p>
			You stay signed in on this phone or computer for a year after you last used kloom. To sign
			out, use "Sign out" on the start screen. To sign in on another device, use your username and
			password. If you forget the password, ask Ken for a new welcome link.
		</p>
	{/if}

	<h2>Help</h2>
	<p>
		The <a href={resolve('/guide')}>User's Guide</a> has the rest. If anything is confusing or broken,
		ask Ken, who would like to know.
	</p>
	<p><a href={resolve('/')}>Start reading</a></p>
</Plain>

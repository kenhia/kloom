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
	"you alone". Short sections, so it reads on a phone with large text.
-->
<Plain title="Welcome">
	<h1>Welcome{data.reader?.signedIn ? `, ${data.reader.name}` : ''}</h1>
	<p>
		kloom is a shelf of illustrated histories. Each subject is told one frame at a time: a picture,
		and a short reading about it.
	</p>
	<p><a href={resolve('/')}>Start reading</a>, or read on for how it works.</p>

	<h2>Reading</h2>
	<ul>
		<li>
			The <strong>spine</strong> is the picture side. Move along it with the
			<strong>‹</strong> and <strong>›</strong> buttons under the picture, or tap or drag the bar
			between them. On a keyboard, <kbd>←</kbd> and <kbd>→</kbd> do the same.
		</li>
		<li>
			The <strong>reading</strong> sits beside the picture, or below it on a phone. It follows the
			spine. Scroll it, or use <kbd>↑</kbd> and <kbd>↓</kbd>.
		</li>
		<li>
			Some frames have <strong>trails</strong>: side paths that go deeper. They are listed under
			"Trails from here" at the end of a reading. Tap one to follow it. "Main story", at the top of
			the picture, brings you back.
		</li>
		<li>
			A name with a dotted underline opens a short card about that person, place or thing. Some
			readings link to a frame in another subject. After a jump, "Back to…" returns you to where you
			were.
		</li>
	</ul>

	<h2>Finding your way</h2>
	<ul>
		<li>
			The <strong>start screen</strong> lists every subject. "Continue where you were" takes you back
			to the last frame you read in that subject.
		</li>
		<li>
			<strong>Contents</strong>, over the picture, lists every frame in the subject. The
			<strong>map</strong> shows how frames connect, across subjects too.
		</li>
		<li>
			The <strong>bookmark</strong> button over the picture marks a frame. The list button beside it shows
			your bookmarks, so you can go straight back to one.
		</li>
		<li>The dice take you to a frame at random, for fun.</li>
	</ul>

	<h2>Notes and annotations</h2>
	<ul>
		<li>
			<strong>A note</strong> is about a whole frame. Open the <strong>Notes</strong> tab beside the reading
			and choose "Add a note".
		</li>
		<li>
			<strong>An annotation</strong> is a note on particular words. Select the words in the reading, then
			choose "Annotate".
		</li>
		<li>
			<strong>My notes</strong>, over the picture, lists every note you have written, in every
			subject.
		</li>
		<li>
			Your notes, bookmarks and places are <strong>private to your login</strong>. Other readers
			cannot see them. If two of you share a login, you share them with each other.
		</li>
	</ul>

	<h2>"Agent review": telling Ken about a problem</h2>
	<p>
		When you write a note, you will see a box called <strong>Agent review</strong>. Please read this
		before you tick it.
	</p>
	<ul>
		<li>
			Ticking it <strong>sends that note to Ken and the AI agents he works with</strong>. They read
			it. A note you leave unticked stays private.
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

	<h2>Settings and keys</h2>
	<p>
		The gear, at the top right, changes colours and brightness, and whether the reading follows the
		spine. "Keyboard shortcuts…" there lists every key and lets you change them.
	</p>

	{#if data.reader?.signedIn}
		<h2>Signing in and out</h2>
		<p>
			You stay signed in on this phone or computer for a year after you last used kloom. To sign
			out, use "Sign out" on the start screen. To sign in on another device, use your username and
			password. If you forget the password, ask Ken for a new welcome link.
		</p>
	{/if}

	<h2>Help</h2>
	<p>If anything is confusing or broken, ask Ken. He would like to know.</p>
	<p><a href={resolve('/')}>Start reading</a></p>
</Plain>

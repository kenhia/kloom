<script lang="ts">
	import Icon, { type IconName } from '$engine/ui/Icon.svelte';
	import { FIXED_KEYS, SHORTCUTS } from '$engine/keys';
	import { resolve } from '$app/paths';
	import Plain from '$lib/page/Plain.svelte';
	import type { PageProps } from './$types';

	let { data }: PageProps = $props();

	/** The parts of the guide, for its own contents at the top. */
	const parts = $derived([
		['start', 'The start screen'],
		['buttons', 'The buttons'],
		['reading', 'Reading a subject'],
		['contents', 'Contents'],
		['map', 'The map'],
		['bookmarks', 'Bookmarks'],
		['new', "What's new"],
		['notes', 'Notes and annotations'],
		['review', 'Agent review'],
		['about', 'About kloom'],
		['settings', 'Settings'],
		['colors', 'Colors'],
		['keys', 'Keyboard'],
		['touch', 'Phones and tablets'],
		...(data.ask ? [['ai', data.grow ? 'Asking and growing' : 'Asking']] : []),
		...(data.reader?.signedIn ? [['account', 'Signing in and out']] : []),
		['help', 'Help']
	]);
</script>

<!--
	The User's Guide (korg 3515): every control, the map and notes, for readers
	who are not technical. The icons are drawn by the app's own Icon component,
	so they always look as they do on screen. A login may be shared, so it says
	"you", never "you alone". Welcome is the short first visit; this is the
	reference it hands off to.
-->
{#snippet icon(name: IconName, filled = false)}
	<span class="icon" aria-hidden="true"><Icon {name} {filled} /></span>
{/snippet}

<Plain title="User's Guide">
	<h1>User's Guide</h1>
	<p>
		Everything kloom's buttons and screens do, in one place. New to kloom? <a
			href={resolve('/welcome')}>Welcome</a
		> is the short version.
	</p>
	<nav aria-label="In this guide">
		<ul class="parts">
			{#each parts as [id, title] (id)}
				<li><a href="#{id}">{title}</a></li>
			{/each}
		</ul>
	</nav>

	<h2 id="start">The start screen</h2>
	<p>The start screen is where kloom opens. It lists every subject on the shelf.</p>
	<ul>
		<li>
			Choose a subject from the list. Its title, its pictures and where you left off in it show
			beside the list. On a keyboard, <kbd>↑</kbd> and <kbd>↓</kbd> move through the list, and
			<kbd>Home</kbd> and <kbd>End</kbd> go to its ends.
		</li>
		<li>
			When there are more subjects than fit beside the loom, the list scrolls. A line on its left
			shows where you are in it, and an arrow above or below says there is more that way: click it
			to move a page.
		</li>
		<li>
			{@render icon('last-read')} An open book marks the subject you read last, and a number says how
			many of a subject's frames are new to you.
		</li>
		<li>On a narrow screen, such as a phone, the list is a drop-down under the title.</li>
		<li><strong>Begin</strong> starts the subject from its first frame.</li>
		<li>
			<strong>Continue where you were</strong> takes you back to the last frame you read in that subject.
		</li>
		<li><strong>Map of the library</strong> opens the map on every subject at once.</li>
		<li>
			<strong>Welcome and how to read kloom</strong> and <strong>User's Guide</strong> open these pages.
		</li>
		<li>
			{@render icon('whats-new')} <strong>What's new</strong>, {@render icon('about')}
			<strong>About</strong> and {@render icon('settings')} <strong>Settings</strong> are at the top right.
		</li>
		<li>
			Once you have started a subject, the line under Begin also says how many frames are new to you
			in it (<a href="#new">more</a>).
		</li>
		<li>
			{@render icon('home')}
			<strong>Home</strong>, at the top right of a subject, brings you back here. Your browser's
			Back button then returns you to the frame you left.
		</li>
	</ul>

	<h2 id="buttons">The buttons</h2>
	<p>
		Rest the pointer on a button, or move to it with <kbd>Tab</kbd>, and its name appears under it,
		with its key if it has one. <kbd>Esc</kbd> hides the name again.
	</p>
	<p>Over the picture, in a row along the top:</p>
	<ul class="buttons">
		<li>
			{@render icon('random')}
			<span><strong>Random frame in this subject</strong>, for fun.</span>
		</li>
		<li>
			{@render icon('contents')}
			<span
				><strong>Contents</strong>: every frame in the subject (<a href="#contents">more</a>).</span
			>
		</li>
		<li>
			{@render icon('map')}
			<span><strong>Map</strong>: how this frame connects to others (<a href="#map">more</a>).</span
			>
		</li>
		<li>
			{@render icon('zoom')}
			<span
				><strong>Zoom drawing</strong>, or <kbd>Z</kbd>: the frame's drawing, as big as the screen,
				to see its detail. <kbd>Z</kbd> again, <kbd>Esc</kbd>, the × or a click beside the drawing
				closes it.</span
			>
		</li>
		<li>
			{@render icon('whats-new')}
			<span
				><strong>What's new</strong>: what was added and what was corrected, in every subject. A
				number on it counts the frames new to you in this subject (<a href="#new">more</a>).</span
			>
		</li>
		<li>
			{@render icon('bookmark')}
			<span
				><strong>Bookmark this frame</strong>. It fills in
				{@render icon('bookmark', true)} when the frame is bookmarked. Press it again to remove the bookmark.</span
			>
		</li>
		<li>
			{@render icon('bookmarks')}
			<span><strong>Bookmarks</strong>: your list (<a href="#bookmarks">more</a>).</span>
		</li>
		<li>
			{@render icon('my-notes')}
			<span
				><strong>My notes</strong>: every note you have written, in every subject. A number on it
				counts answers you have not read yet (<a href="#notes">more</a>).</span
			>
		</li>
	</ul>
	<p>At the top right of the reading:</p>
	<ul class="buttons">
		<li>
			{@render icon('anywhere')}
			<span><strong>Random frame anywhere</strong> in the library, in any subject.</span>
		</li>
		<li>
			{@render icon('home')}
			<span><strong>Home</strong>: back to the start screen.</span>
		</li>
		<li>
			{@render icon('settings')}
			<span><strong>Settings</strong> (<a href="#settings">more</a>).</span>
		</li>
	</ul>
	<p>
		After you follow a link to another frame, a <strong>↩ Back to…</strong> button appears over the picture.
		It names the frame you came from and takes you back there, just as the browser's Back button does.
	</p>

	<h2 id="reading">Reading a subject</h2>
	<ul>
		<li>
			Each subject is a line of <strong>frames</strong>, and each frame is a picture with a reading.
			The picture side is the <strong>spine</strong>. Move along it with the <strong>‹</strong> and
			<strong>›</strong> buttons under the picture, or tap or drag the bar between them. On a
			keyboard,
			<kbd>←</kbd> and <kbd>→</kbd> do the same, and <kbd>Home</kbd> and <kbd>End</kbd> go to the first
			and last frame.
		</li>
		<li>
			The <strong>reading</strong> sits beside the picture, or below it on a phone. It follows the
			spine as you move. You can change that in Settings, so that the reading stays put until you
			press
			<kbd>S</kbd>.
		</li>
		<li>
			The tabs above the reading switch between the <strong>Narrative</strong> and your
			<strong>Notes</strong> on the frame. The line between the picture and the reading can be dragged
			to make either side wider.
		</li>
		<li>
			<strong>Trails</strong> are side paths that go deeper. They are listed under "Trails from
			here" at the end of a reading. Follow one, or press <kbd>T</kbd>. While you are on a trail,
			"Main story" at the top of the picture brings you back, as does <kbd>Esc</kbd>.
		</li>
		<li>
			A <strong>name with a dotted underline</strong> opens a card about that person, place or thing.
			The card says where else the name appears, and "Show on the map" draws them.
		</li>
		<li>
			<strong>Connections</strong>, at the end of some readings, link to frames in this subject or
			in another, each with a line on why. Following one is a jump: ↩ Back to… returns you.
		</li>
		<li>
			<strong>Sources</strong>, at the very end, lists where the reading comes from. The full
			citations are in the closed section beneath it.
		</li>
		<li>
			<strong>Edits and corrections</strong>, under the citations on some frames, says what has been
			changed in the frame since it was first published, when, and why.
		</li>
	</ul>

	<h2 id="contents">Contents</h2>
	<p>
		{@render icon('contents')} Contents, or <kbd>C</kbd>, lists every frame in the subject, grouped
		into its sections. Trails are listed under the frame they start from. Your bookmarks and notes
		are marked beside their frames. Type in the box at the top to find a frame by its title, date or
		topic. Choose a frame to go there.
	</p>

	<h2 id="map">The map</h2>
	<p>
		{@render icon('map')} The map, or <kbd>M</kbd>, is a drawing of how frames connect. It fills the
		screen;
		<kbd>Esc</kbd> or the × at the top closes it.
	</p>
	<ul>
		<li>
			Each <strong>dot</strong> is a frame, and its color and shape say which subject it belongs to.
			The key at the bottom names them. A plain round dot with an outline is a
			<strong>name</strong>: a person, place or thing.
		</li>
		<li>
			A <strong>solid line</strong> is a connection between two frames. A
			<strong>dotted line</strong> joins a name to the frames that mention it.
		</li>
		<li>
			Point at a dot, or move to it with the arrow keys, to bring it forward: its lines and its
			neighbors light up, and the details under the map say what it is.
		</li>
		<li>
			Choose a dot to put it in the middle and see what it connects to. To go to a frame, choose "Go
			to" in the details, double-click its dot, or press <kbd>Enter</kbd>. On a keyboard,
			<kbd>Space</kbd> puts the dot in the middle.
		</li>
		<li>
			<strong>Back</strong>, at the top left of the map, steps back through the views you have seen.
			"This frame" returns to the frame you are reading, and "Library" shows every subject.
		</li>
		<li>
			"How far out" shows one or two steps of connections from the frame in the middle.
			<strong>Show as list</strong> gives the same thing as a plain list.
		</li>
		<li>
			<strong>3D</strong> shows the whole library as a cloud you can turn: drag to turn it, scroll or
			pinch to zoom, and choose a frame or a name to fly to it. It is for fun; the flat map shows the
			same links.
		</li>
		<li>
			Going to a frame from the map is a jump, so ↩ Back to… brings you back to where you were.
		</li>
	</ul>

	<h2 id="bookmarks">Bookmarks</h2>
	<p>
		{@render icon('bookmark')} marks the frame you are on, or press <kbd>B</kbd>.
		{@render icon('bookmarks')} lists your bookmarks, from every subject, newest first. Choose one to
		go there, or remove it from the list. "Export my reading data" at the bottom saves a copy of your
		bookmarks, notes and places as a file.
	</p>

	<h2 id="new">What's new</h2>
	<p>
		kloom grows: frames, trails and whole subjects are added, and frames are sometimes corrected.
		{@render icon('whats-new')} <strong>What's new</strong> lists it all.
	</p>
	<ul>
		<li>
			<strong>Added</strong> lists new frames and trails, newest first, by day and subject. A new subject
			is one line, "First published". Choose an entry to go there; ↩ Back to… brings you back.
		</li>
		<li>
			<strong>Edits and corrections</strong> lists the changes made to frames already published, each
			with a sentence on what changed and why.
		</li>
		<li>
			Narrow either list with the <strong>Subjects</strong> boxes, and with <strong>When</strong>:
			all time, since my last visit, since I caught up, the last 7 or 30 days, or between two dates.
		</li>
		<li>
			Once you start a subject, anything added to it after that is <strong>new to you</strong>
			until you open it. The spine marks it with a small spark under the line, and Contents, trails and
			What's new say "new to you" beside it.
		</li>
		<li>
			If you read a subject straight through, choose <strong>I'm caught up on this subject</strong>
			in Contents when you finish. From then on, only what is added later is new to you.
			<strong>Mark all as seen</strong> in What's new clears the marks on everything the list is showing.
		</li>
	</ul>

	<h2 id="notes">Notes and annotations</h2>
	<ul>
		<li>
			<strong>A note</strong> is about a whole frame. Open the <strong>Notes</strong> tab and choose
			"Add a note", or press <kbd>N</kbd>. The note opens where the picture was. "Save" keeps it.
		</li>
		<li>
			<strong>An annotation</strong> is a note on particular words. Select the words in the reading,
			then choose "Annotate", or press <kbd>A</kbd>. Without a mouse, press <kbd>A</kbd> with nothing
			selected and choose the words with the arrow keys.
		</li>
		<li>
			The Notes tab lists the notes on the frame you are on. Each has "Edit" and "Delete", and an
			annotation has "Show in reading", which finds its words.
		</li>
		<li>
			If the reading is later rewritten and an annotation's words are gone, it is kept and marked
			<strong>detached</strong>, so nothing you wrote is lost.
		</li>
		<li>
			{@render icon('my-notes')}
			<strong>My notes</strong>, or <kbd>O</kbd>, lists every note and annotation you have written,
			in every subject. Show all of them, or only those sent for Agent review, answered, or
			detached. "Go to" opens a note on its frame, and "Clear" removes the ones shown.
		</li>
		<li>
			Your notes, bookmarks and places are <strong>private to your login</strong>. Other readers
			cannot see them. If two of you share a login, you share them with each other.
		</li>
	</ul>

	<h2 id="review">Agent review</h2>
	<p>
		When you write a note or an annotation, you will see a box called <strong>Agent review</strong>.
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
			An answer may come back on the note itself, marked "Agent:". My notes shows a count when one
			is waiting for you.
		</li>
	</ul>

	<h2 id="about">About kloom</h2>
	<p>
		{@render icon('about')} About, at the top right of the start screen, tells you what kloom is and how
		big the library is. It also has the credits, and a note on accuracy with another way to report a problem.
		<strong>Suggest a subject</strong> is there too: say what you would like to read about next, and see
		what you have suggested before.
	</p>

	<h2 id="settings">Settings</h2>
	<p>{@render icon('settings')} The gear, at the top right, opens the settings:</p>
	<ul>
		<li>
			<strong>Scene colors</strong> and <strong>Reading colors</strong>: light or dark (<a
				href="#colors">more</a
			>).
		</li>
		<li>
			<strong>Narrative</strong>: whether the reading follows the spine, or stays until you press
			<kbd>S</kbd>.
		</li>
		{#if data.ask}
			<li>
				<strong>Layout</strong>, and the model{data.grow ? 's that ask and grow use' : ' ask uses'}.
			</li>
		{/if}
		<li>
			<strong>Advanced</strong> holds <strong>Light brightness</strong> and
			<strong>Dark brightness</strong> (<a href="#colors">more</a>).
		</li>
		<li><strong>Keyboard shortcuts…</strong> lists every key and lets you change them.</li>
	</ul>
	<p>Settings are remembered in this browser, so another phone or computer keeps its own.</p>

	<h2 id="colors">Colors</h2>
	<p>
		Every section of a subject has its own colors, light or dark, chosen to suit it. Four settings
		under {@render icon('settings')} let you change how they look. The screen changes as you choose, so
		you can try each one and see.
	</p>
	<ul>
		<li>
			<strong>The two sides are colored apart.</strong> The picture side, with its buttons and the
			lists they open, follows <strong>Scene colors</strong>. The reading, the notes, the tabs and
			the settings follow <strong>Reading colors</strong>.
		</li>
		<li>
			<strong>Scene colors</strong>:
			<ul>
				<li>
					<strong>By section</strong>, the first choice: every frame in a section is light, or every
					frame is dark, so the screen does not flash between them as you move.
				</li>
				<li>
					<strong>Each frame</strong>: each frame in the colors it was made in, light or dark.
				</li>
				<li>
					<strong>Always dark</strong> or <strong>Always light</strong>: every frame that way.
				</li>
			</ul>
		</li>
		<li>
			<strong>Reading colors</strong>:
			<ul>
				<li><strong>Same as scene</strong>, the first choice: the reading matches the picture.</li>
				<li>
					<strong>Always light</strong> or <strong>Always dark</strong>: the reading stays one way
					whatever the picture does. Choose this if you find dark pages hard to read, or bright ones
					tiring.
				</li>
			</ul>
		</li>
		<li>
			<strong>Light brightness</strong> and <strong>Dark brightness</strong>, under
			<strong>Advanced</strong>, are sliders. Light brightness makes the light pages dimmer, if they
			feel too bright, or a little brighter. Dark brightness makes the dark pages softer and
			lighter, or a little darker. <strong>As designed</strong>, in the middle, is how kloom was
			made. Whichever you choose, the words keep enough contrast to read.
		</li>
	</ul>
	<p>Colors are remembered in this browser, like the other settings.</p>

	<h2 id="keys">Keyboard</h2>
	<p>kloom can be used without a mouse. These keys are always the same:</p>
	<ul class="keys">
		{#each FIXED_KEYS as k (k.keys)}
			<li><kbd>{k.keys}</kbd> {k.does}</li>
		{/each}
	</ul>
	<p>
		These letters work while you are in the picture, the reading or the notes. You can change them
		in Settings, under Keyboard shortcuts…. Out of the box they are:
	</p>
	<ul class="keys">
		{#each SHORTCUTS as s (s.action)}
			<li><kbd>{s.key.toUpperCase()}</kbd> {s.label}</li>
		{/each}
	</ul>

	<h2 id="touch">Phones and tablets</h2>
	<ul>
		<li>
			On a phone the reading is below the picture. Scroll down to read, and back up for the buttons.
		</li>
		<li>Tap the ‹ and › buttons, or drag the bar between them, to move along the spine.</li>
		<li>
			To annotate, hold your finger on a word until it is selected, drag the handles to cover the
			words you want, then tap "Annotate".
		</li>
		<li>
			On the map, tap a dot to put it in the middle, then tap "Go to" in the details to go there.
		</li>
	</ul>

	{#if data.grow}
		<h2 id="ai">Asking and growing</h2>
		<p>
			On this copy of kloom the AI pane can also answer a question about the frame you are on (Ask),
			or write new frames and trails (Grow). Choose Ask or Grow, type, and send. An answer worth
			keeping can be kept on its frame. Grown frames are reviewed before they become part of the
			subject.
		</p>
	{:else if data.ask}
		<h2 id="ai">Asking</h2>
		<p>
			Ken has turned on <strong>Ask</strong> for you. The AI pane, under the reading, answers a
			question about the frame you are on: type it and press Ask. The answers are written by Claude,
			an AI made by Anthropic, which Ken provides; they can be wrong, so check anything that matters
			against the frame's sources. If an answer is wrong or strange, tell Ken, or note it on the
			frame with <em>Agent review</em> ticked. <strong>Web</strong> lets Claude search the web for
			that question. <strong>Keep this</strong> keeps an answer on its frame, under Q&amp;A. Questions
			have a monthly allowance; if it runs out, Ask rests until the first of the next month.
		</p>
	{/if}

	{#if data.reader?.signedIn}
		<h2 id="account">Signing in and out</h2>
		<p>
			You stay signed in on this phone or computer for a year after you last used kloom. To sign
			out, use "Sign out" on the start screen. To sign in on another device, use your username and
			password. If you forget the password, ask Ken for a new welcome link.
		</p>
	{/if}

	<h2 id="help">Help</h2>
	<p>If anything is confusing or broken, ask Ken, who would like to know.</p>
	<p><a href={resolve('/')}>Start reading</a></p>
</Plain>

<style>
	/* An icon as the shell draws it: the IconButton's size and ink. */
	.icon {
		display: inline-grid;
		place-items: center;
		width: 1.75rem;
		height: 1.75rem;
		vertical-align: middle;
		color: var(--ink);
		border: 1px solid var(--line);
		border-radius: 0.25rem;
	}
	.icon :global(svg) {
		width: 1.25rem;
		height: 1.25rem;
	}
	.buttons {
		padding: 0;
		list-style: none;
	}
	.buttons li {
		display: flex;
		gap: 0.75rem;
		align-items: flex-start;
	}
	.buttons .icon {
		flex: none;
	}
	.parts {
		columns: 2 12rem;
	}
	.keys {
		padding: 0;
		list-style: none;
	}
</style>

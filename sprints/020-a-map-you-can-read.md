# Sprint 020 — A map you can read

korg proposal 3450, covering 3446, 3447 and 3448. Branch
`020-a-map-you-can-read`. From Ken's use of the map shipped in sprint 019.

## Goal

Make the map readable at a glance. A frame's headline is deliberately
evocative ("It played ALONG."), so on its own it does not say what a node
is. Every frame gains a plain `topic`, and the map labels by it. Links are
dimmed at rest and brought forward for the node under the pointer or focus.
The details panel stops resizing the graph, and a double-click no longer
selects text.

## Premise check

- **3448 holds.** The library node's `ondblclick` is in
  `engine/ui/MapOverlay.svelte`, and nothing on the canvas sets
  `user-select`.
- **3446 drifted, in the same direction.** There are 222 frames, trails
  included (ai 66, computing 70, feynman 62, western-civ 24), not about 300. No frame has a `topic`, and a `date` frame's position label is a
  date.
- **3447 holds.** `.details` has `min-height: 3.5rem` and grows when a node
  is focused.
- No cross-project plan lists kloom.

## Decisions

- **Order: 3448, then 3446's content, then the code, then 3447**, as the
  proposal set it, so the map was tuned on real topics.
- **Topics were backfilled per subject and committed per subject.**
  western-civ (24) was written by hand as the reference. ai, computing and
  feynman were each written by one agent from the readings, then reviewed
  here. The review took the safer wording where a claim is contested
  ("The Fortran compiler", not "the first compiler"; "UNIVAC I"; "The
  bombe and Enigma"), and named whose death `last-days` is about. The
  content commits come before the code that requires them, so every commit
  passes the gate it shipped with.
- **The rules a topic must meet**: required, at most 40 characters, no
  closing "." or "!", unique in its subject, and not the frame's accent
  word in capitals. The accent check is case-sensitive and whole-word, so a
  plain-case name that shares the word ("The Domain Name System" beside
  the accent NAME) passes. No accent in the four subjects is an acronym, so
  this rule cannot catch a legitimate topic. The cap is 40 because the
  backfill's longest topic is 39 characters, and nothing needed cutting.
- **Where each surface names a frame** (design.md §Topics): where a frame
  stands alone (the map, the Back chip, a name card's list, a frame's
  Connections), the topic names it. Where the reader walks their own
  subject in order (the contents, bookmarks), the headline stays the name
  and the topic goes in the context line. The contents filter matches
  topics. A bookmark's stored label is reader data and is not rewritten.
  The spine, the reading's title and the step announcement are the frame
  itself, and keep the headline. The proposal said not to let this sprawl.
  Each change here is one line, and the rule is written down.
- **Map labels are whole.** A label over 22 characters takes two lines of
  about equal length, broken at a space (`labelLines`). None is cut, and
  none breaks inside a word. The label placer sizes each box by its
  lines.
- **Emphasis follows the pointer, or keyboard focus when it is visible.**
  `hot` is the hovered node, else the node with `:focus-visible` focus.
  With no hot node the map is at rest, and every line is dimmed. A map
  opened by the pointer opens at rest. Opened by M, focus is visible on
  the centre, so the centre's links are forward. The details still follow
  the last node touched, so they never go blank as the pointer leaves.
- **The hot node's neighbours** are outlined, their labels are underlined
  in their subject's colour, and a label waiting for room shows. Every
  other node recedes to 35%. Every label sits on a plate of the map's
  surface, not only the highlighted ones. A plate costs nothing at rest,
  and it keeps lines out of every label's words.
- **The details panel is a fixed height**, clipped to whole lines (6rem
  wide, 8.2rem below 40rem). The list has the text whole. Floating it over
  the graph would have hidden nodes at the bottom of the map instead.
  `-webkit-line-clamp` collapsed to one line in Chromium here, so the
  clamp is a `max-height` in lines.
- **The details say "linked to N here"**, the node's link count on this
  map, in the live region, as 3447's keyboard-parity item asks.

## What shipped

- **3448:** the map's canvas is `user-select: none`, so a double-click
  goes to its target without selecting a word. The details and the list
  stay selectable.
- **3446:**
  - `topic` in `FrameFile`, validated in `engine/validate.ts`
    (`TOPIC_MAX`).
  - All 222 frames backfilled, in four content commits.
  - The graph carries `topic` (`GraphFrame`, `FrameLink`). A frame read
    without one, from a content clone behind the code, is named by its
    headline.
  - Topics are also used by the contents (context line and filter),
    bookmarks' context, the Back chip, name cards and Connections.
  - Grow's served-frames reference lists each frame's topic first.
  - `skills/grow/SKILL.md` requires a topic (example, rule and checklist).
    `skills/author-subject/SKILL.md` settles each frame's topic in the
    brief.
  - design.md: §Content model and a new §Topics.
- **3447:** the map labels frames by topic, whole, in one or two lines,
  and the headline moves to the details. Also:
  - Lines are dimmed at rest, and the hot node's lines come forward in
    full ink.
  - Neighbours are outlined and ruled in their subject's colour.
  - Every label sits on a plate.
  - The details panel keeps one height.
  - The link count is in the details.
  - design.md §The map: Labels, Emphasis, the details, No text selection.

## Verification

- `just check`: svelte-check clean, prettier and eslint clean, 699 tests.
- Negative tests, each seen failing:
  - a frame with its topic removed, and a topic repeating the accent in
    capitals (the real-subject load test fails on each);
  - the contents filter without topic matching (its first test could not
    fail, because a trail frame kept the anchor, so it was rewritten
    around a frame with no trail);
  - the double-click check without `user-select: none`: Chromium selected
    "Richard";
  - the canvas-height check with the old `min-height` details: three
    heights on each map, where the fix holds one.
- Chromium (Playwright, dev server), at 1280×900 and 390×844:
  - `ai/turing-machine` (dense, 31 nodes) and
    `western-civ/printing-press` (sparse, 16 nodes), each at rest, on
    hover, and by keyboard focus (an arrow from the centre).
  - Hovering every node in turn left the canvas at one height, at both
    widths.
  - The library at 1280 and 390: every hover leaves the details' lines
    whole, with nothing past the panel.
  - Screenshots in `.scratch/020/`: `wide-turing-{rest,hover,focus}`,
    `wide-printing-{rest,hover,focus}`, the same as `phone-*`,
    `library-hover` and `contents-filter`.
  - **Keyboard only** (sprint 019's walk, rerun):
    - The library opens from the start screen. The arrows and Home move,
      Space opens a subject, Backspace steps back, and Esc returns
      focus.
    - M on `ai/turing-machine`, then Space on Alan Turing, opens his view.
    - Enter on "Breaking the Lorenz cipher" jumps to `/computing/tunny`
      with the chip "↩ Back to The Turing machine".
  - A double-click on a library subject opens it with nothing selected.
  - No page errors.

## Deploy note

The service serves its own content clone, which a restart moves onto
main. The code now requires `topic`, so a grown frame without one would
fail validation. At the start of the sprint `grow/kai` had nothing
unmerged (`origin/main..origin/grow/kai` is empty), so the deploy's
restart brings the topics in with the code. A grow that lands before this
merges needs a topic added in review.

## For Ken: the look

The proposal asked to show you the emphasis states on a dense node and a
sparse one before polishing. This session ran without you, so they are
built. The screenshots listed above are the quickest way to judge them.
The open questions of look, none of them blocking:

- **How far the rest recedes.** Other nodes drop to 35% and other lines to
  18% while one is hot. In light mode, on western-civ, the faded labels
  are faint.
- **Labels on the phone.** Neighbours' plates can overlap one another at
  390 wide. The list is the default there.
- **The subject view** was busy in sprint 019. Topics make its labels
  longer, though they now wrap.

## Repaired in passing

- The contents filter's placeholder said "title or position". It now names
  topics too, which it matches.

## Follow-ups

- None filed. Physics (3428) depends on 3446 and now gets `topic` from
  the skills it is written by.

## Deployed

2026-09-29, `just deploy` (the `recipe: deploy` in `.sprint-deploy`) to the
kloom service on kai, from merged main `b629f7b` (PR #23). It built the app
and restarted `kloom.service`, and `just verify` passed all eight door
checks. The start-up sync fast-forwarded the content clone's `grow/kai` to
`origin/main`. `grow/kai` had nothing unmerged, so every served frame has a
topic.

Verified live on the ssh door (:4891), on this sprint's own behaviour:

- `GET /api/map` serves 4 subjects and 222 frames, each with a topic
  ("Alignment faking", "IBM tabulators at Los Alamos", "Breaking the Lorenz
  cipher").
- A double-click on a library subject opens it with nothing selected.
- On `ai/turing-machine` (31 nodes) and `western-civ/printing-press` (16),
  hovering every node in turn leaves the canvas at one height. An arrow
  from the centre brings the node forward with its neighbours marked, and
  the details say "linked to 4 here".
- Keyboard only (sprint 019's walk): Enter on "Breaking the Lorenz cipher"
  jumps to `/computing/tunny`, and the chip reads "↩ Back to The Turing
  machine".
- No page errors, and no errors in the service's journal since the restart.

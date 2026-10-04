# 047 — The start screen's elevator

## Goal

korg proposal 3538, fixing korg 3514. Ken saw it on the live reader site
(2026-10-02): the start screen's big title, "THE HISTORY AND CURRENT STATE OF
AI", ran under the subject list, and the tagline was clipped ("A TIMELINE
YOU CAN R…"). He set two constraints: don't wrap the title, and don't just
move the list, because it grows with every subject and would collide again.
His sketch (img-dd1) put the list in the dial's band, scrolling as an
"elevator" with a thin rail and carets. He took every recommendation in the
prep comment on 3514 on 2026-10-03, so the five decisions below were settled
before the sprint started.

## Why it overlapped

From 60rem `.subjects` was `position:absolute; top:50%` against the whole
fixed `.start`, so a longer list grew evenly up and down and reached into
the title row. The title is centred across the full width, so a long one ran
under it. On a phone the tagline was clipped because `.start`'s grid had an
`auto` column, sized to the widest thing in it, wider than the screen.

## Decisions

Settled by Ken (2026-10-03):

1. **"The "** is stripped in the list only. subject.json keeps it, so the big
   title, About and the map are unchanged.
2. **Narrow title:** one line, fitted to the width, down to a 1.5rem floor.
   Below the floor it wraps in balanced lines. In the session the guard found
   that a very long title at 390 wide needed three lines at the floor, so a
   wrapped title may go under the floor as far as two lines need. Decision 2
   allows two lines, not three.
3. **Below 60rem a native `<select>`** sits under the title (and tagline),
   styled when shut.
4. **The elevator:** a thin rail with end stops, a car that only shows
   position (not draggable in v1), and carets that appear only when there is
   more that way. A click on a caret scrolls a page.
5. **"N new"** is a small accent count after the title. The line under Begin
   stays.

Made in the sprint:

- **The band.** The list moved out of `.start` into a new `.band`, the first
  grid row, beside the stage: `list | stage | list` from 60rem. The empty
  right column keeps the loom centred over the centred title. The stage gives
  way to both columns (`--stage: min(100vw − 2rem − 2(list + gap), 44rem)`).
  The list's height is capped at the dial's `min(stage, 64dvh)` and it is
  centred on the dial, all in CSS. This fixes the sideways collision between
  60 and 75rem as well: the stage shrinks, so nothing sits on the loom.
- **The list's width is what the dial leaves,** `clamp(16rem, (100vw − 2rem −
min(44rem, 64dvh))/2 − gap, 20rem)`. A fixed `vw` width truncated "History
  of Western Civilization" with its book and count at 1280. At 1280×800 the
  dial is height-bound (512px), so the column can be 20rem without shrinking
  it. At 1024 the column floors at 16rem, and an entry carrying both marks
  can still ellipsise its title. The marks never give way.
- **Native scrolling, drawn over.** `overflow-y:auto` with the bar hidden, so
  wheel, touch and trackpad cost nothing. The rail, car and carets follow
  `scroll` and a ResizeObserver. The rail hides when the list does not
  scroll: a car filling its whole rail looked like a stray line.
- **The selection is kept in view by hand** (`reveal()`: `offsetTop` against
  the list's `scrollTop`, clear of the 28px fades) rather than by
  `scrollIntoView`. That would also scroll `.start`, which is a scroll
  container because of `overflow:hidden`. On opening, the selection is
  centred.
- **The title is fitted by measuring it on a canvas,** in the h2's computed
  font, against the copy column's width. The serif is a system stack, so
  there is no web-font race, though `document.fonts.ready` refits anyway. The
  JS repeats the stylesheet's clamp as the cap. SSR renders the clamp size
  with `nowrap`, and the fit takes over on mount.
- **Both pickers are rendered and CSS chooses one** (`display:none` on the
  other at 60rem). That works before hydration, and a `display:none` control
  is out of the accessibility tree, so a screen reader meets only one.
- **The ←/→ branch of `listKeys` is gone.** It existed only for the flat
  list.
- **A synthetic subject is a clone, not a minimal subject.** The proposal
  asked for the smallest subject.json the loader accepts. A served subject
  has to compile into `content.db` with frames, though, so start-fit gives
  each synthetic subject its own subject.json (a long title) over symlinks
  to a real subject's `frames/`, `spine.json` and `trails/`. Connections
  still resolve and there is no schema to keep in step. One trap: the
  subject listing takes `Dirent.isDirectory()`, which is false for a
  symlink, so each real subject is a directory of links, never a link.

## What shipped

- `engine/ui/StartScreen.svelte`: the band, the elevator (rail, car, carets,
  fade, `reveal`), the picker, title fitting, the tagline wrapping, the new
  entry content (stripped title, book, count) and halved option spacing
  (padding `0.15rem 0.375rem`, gap `0.125rem`). Its subject shape is now
  `{ id, title, subtitle?, last?, fresh? }` in place of a joined `note`.
- `engine/ui/icons/open-book.svg`, as `Icon` name `last-read` (the guide
  draws it too).
- `src/routes/[subject]/[[frame]]/+page.svelte`: `last` and `fresh` passed
  separately.
- `create-tools/start-fit/start_fit.mjs` and `just start-fit`. The guard
  runs every subject's title at 1024×768, 1280×800, 1400×900 and 390×844,
  with the library as served and with 24 subjects. That is 833 checks, in
  about 20 s.
- Tests: the stripped title and no subtitle in the list, the picker's
  entries and selection, the book's markup and words, and the picker's
  "— last read" and "· 2 new".
- docs/design.md §Start screen (the list bullet rewritten, a title-fitting
  bullet, the subtitle bullet), the "2 new" note in §What's new, and the
  guide's start-screen section.

## Verified

- `just start-fit`: 833/833. It was negative-tested twice. With the
  elevator's `max-height` removed, 107 failures (the list out of the dial's
  band, meeting the title). With the old balanced, unfitted title, 11
  failures (2–3 lines at 28px on a phone).
- Ken signed off on the look in the session (2026-10-03), on kai's dev
  servers with 10 and 24 subjects: "Scroll bar looks great. Drop-down for
  mobile works!" The rail stays hidden when the list does not scroll.

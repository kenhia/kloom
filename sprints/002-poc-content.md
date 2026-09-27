# 002 — POC content: curated Western Civ frames + loom start screen

## Goal

korg proposal 3367, which covers four work items, done in this order:

- korg 3371: citations. Stored as structured data, rendered in Chicago style
  in a collapsed control under Sources, with image credits.
- korg 3370: the palette "flash bulb" when the page moves between dark and
  light frames.
- korg 3361: the POC content. Hand-curated frames following the inspiration
  video's arc, with long narratives, at least one image, a chart, and one
  trail.
- korg 3359: the start screen, a gold-on-black loom from the public-domain
  Wikipedia drawing.

Ken ordered this before ask/grow (2026-09-26). The look and feel arrive
earlier, and the curated frames are the bar grow (3364) is written against.
If Claude's line art could not reach the video's look, that needed to be
known before building machinery to generate more of it.

## Decisions

- **Premises held.** At the start there were no citations anywhere and no
  `@property`, the transition at `Shell.svelte:197` was as 3370 described,
  and the three placeholder frames were still in place. kloom is not in the
  cross-project plan index.
- **Citations (3371).** `engine/citation.ts` holds the type, the
  Chicago formatter, validation and bibliography order.
  - The formatter returns text runs (plain, italic, or the URL), never
    markup, so content cannot inject HTML. The Narrative renders the runs as
    Svelte text inside `<details>`, which is closed by default and sits
    between Sources and the AI pane in tab order.
  - Entries are alphabetised, because a Chicago bibliography is. Quotation
    marks inside a quoted title become single ones.
  - I added an `article` kind (journal, volume, issue, pages) to the four
    kinds the item named. Watson & Crick, Maxwell and Buringh & van Zanden
    are journal articles, and a web-page rendering of them would not be
    Chicago.
  - **Images live in the frame directory.** A reading's image must be a
    file next to `frame.json`, and it is shown only with a `media` citation
    naming that file and a licence. The files are served at
    `/media/<frame>/<file>` by a SvelteKit route. That route reuses
    validation's file-name rule and sends `default-src 'none'; sandbox`,
    because an SVG opened on its own is a document. External image URLs are
    rejected, so a reading cannot hotlink.
  - A licence other than public domain or CC0 gets a caption credit beside
    the image. The one real user is the MIT chart ("kloom contributors /
    MIT").
- **Palette (3370).** The five palette colours are registered with
  `@property` and transitioned on `.shell`, ease-in-out. Sampling in
  Chromium showed the accent and the background now move together (for
  example, at +400ms the background was `rgb(87,84,78)` and the accent
  `rgb(204,122,53)`, both mid-flight). A → ← → burst reverses smoothly from
  wherever it is. With reduced motion the transition is `0s`. I shipped
  1s; Ken set it to 1.5s after trying it.
- **Content (3361).** There are 16 main-spine frames and the one-frame
  trail, in six segments.
  - The first segment is a `category` segment, **Myth** (Prometheus). That
    is the "don't assume the spine is time" rule showing on the real
    subject.
  - After it come Antiquity (writing, Greek inquiry, Eratosthenes,
    Pantheon), The long middle (scriptorium, Magna Carta), Rebirth (Florence
    dome, printing press, voyages, Shakespeare), Machines and fields (steam,
    Maxwell) and Code and cosmos (DNA, Apollo 11, Webb).
  - I folded SPQR/Colosseum into the Pantheon frame, to stay within ~16
    frames.
  - The three placeholders were rewritten, and the trail frame (Gutenberg
    Bible) got real text and a drawing.
  - Every reading runs roughly 450–650 words with section headings, so every
    one scrolls.
  - Every frame cites the Wikipedia revisions it drew on (fetched
    2026-09-26), plus primary or institutional sources where they exist:
    Hesiod, the _Timaeus_, the three journal articles, the National
    Archives, the First Folio, and NASA.
- **Fact-checking.** Every number and specific claim in the readings was
  checked against the text of the cited revision. The check changed these:
  - The Pantheon's oculus is about 9 m. I had no coffer-ring count to cite,
    so it came out.
  - Brunelleschi's early Rome visit is disputed, so the text now says so.
  - Flying buttresses: I dropped the "rivals' style" story for the
    article's "ugly makeshifts".
  - The last cuneiform tablet is dated AD 79/80, and about half a million
    tablets are held in museums.
  - The Saturn V is 111 m tall. The "400,000 people" and "seconds of fuel"
    claims were softened, because I couldn't find them in a cited source.
  - The Gutenberg Bible has 1,288 pages. The "Paris copy" detail came out.
  - The book-output estimates differ (about 12.6 million vs "over 20
    million" by 1500), and the reading says so.
- **Images and chart.** There are two public-domain images:
  - the 1499 Lyon _Danse macabre_ printing shop (printing press)
  - the British Library's 1215 Magna Carta (Magna Carta)

  The chart is an SVG bar chart of European printed-book output per century
  (Buringh & van Zanden 2009, table 2), with the same figures in a table
  beneath it for screen readers. I checked the per-century totals against the
  bar heights in the Commons chart of the same data: 12.6M, 217M, 532M, 984M.
  An `<img>` SVG cannot inherit the page palette, so the chart carries the
  parchment colours of its frame.

- **Start screen (3359).**
  - The Commons file page states public domain (`PD-UK-unknown`,
    `PD-1923`, attribution not required); it was checked on 2026-09-26 and
    is recorded in `src/lib/start/README.md`.
  - The drawing was traced with potrace. The contours are stroked, not
    filled, which gives the double-line wireframe look, and they are drawn
    on in eight left-to-right bands over a slowly turning inscribed dial.
  - The start screen is a modal dialog over an **inert** shell. Begin has
    focus; Enter or Esc begins, and focus moves to the spine slider.
  - It wears the first frame's palette, so the engine component names no
    subject. The loom is kloom's mark, so it lives in `src/lib/start/`.
  - The 212 KB SVG is loaded after mount as its own chunk (63 KB brotli), so
    the server-rendered page stays small.
- **Reading headings nest under the frame title.** Markdown `##` renders as
  `h3`. See Repaired in passing.

## Illustrations: what worked

This is the guidance grow will be written against, so it also lives in
docs/design.md §Illustrations.

- **Engineering plates, not pictures.**
  - The drawings that read most like the video show their geometry: the
    Pantheon section with its inscribed sphere, Brunelleschi's dome with
    the _quinto acuto_ compass centres, Eratosthenes' parallel rays and
    angle, the dodecahedron in a construction circle, the Watt engine.
  - The tell of clip-art is a lone object with nothing to measure it
    against.
- **Three stroke weights and ordered groups.** Construction lines are thin
  and faint, secondary detail is mid, and the object is at full weight.
  Top-level `<g>` groups now draw one after another (a new engine rule in
  `SpinePane.svelte`), and that sequence is most of the draftsman effect.
- **Compute the geometry.** Solids, the globe, the Globe theatre, the
  helix, gears, the EM wave and the mirror honeycomb came from a Python
  script (now `create-tools/draw-plates`), and look far better than hand-placed curves would.
  - It caught its own bugs: the dodecahedron's back edges coincided with
    the front ones at the first angle I tried, and the route drew a line
    across the globe because it crossed the antimeridian the long way.
  - Iterating on a contact sheet (Playwright screenshots of all the SVGs at
    once) was the fast loop. There were three rounds.
- **Weakest plates:** the beam engine (the parallel motion is only
  suggested) and the printing press's tympan. They read correctly, and they
  are where a second pass would go.

## What shipped

- `engine/citation.ts` holds the type, the formatter (`chicago`,
  `chicagoText`, `bibliography`, caption credit) and `citationProblems`.
- The model gains `citations?: Citation[]`.
- Validation checks citations, media files and image references, and
  `illustrationProblem` is now exported so the start screen's art is
  checked by the same tripwire.
- The loader lists media files and resolves reading images through
  `renderMarkdown(…, { image })`, and exports `readMedia` for the
  `src/routes/media/[frame]/[file]` route.
- UI:
  - The Narrative has the Citations control, image/figure/table/blockquote
    styles and h3 section headings.
  - SpinePane has larger illustrations, staggered draw-on and labels that
    fade in.
  - The Shell has the registered palette properties and an `active` prop
    (inert, with keys ignored, while the start screen is up).
  - `StartScreen.svelte` is new.
- Content: `subjects/western-civ` has 17 frames, each with `frame.json`,
  `reading.md` and `scene.svg`, plus two JPEGs and the chart, and the new
  six-segment `spine.json`.
- The app side is `src/routes/+page.svelte` (start screen, then shell) and
  `src/lib/start/` (the loom, its credit, its README and a test).
- The tests went from 43 to 76. The new ones cover:
  - the Chicago formatter for a Wikipedia article, a web page, a book, a
    journal article and a PD image, plus author order, dates, nested quotes
    and punctuation, with hostile text staying text
  - citation validation, and image and media validation
  - heading levels and image resolution with and without a caption
  - the media route refusing path tricks and sending its CSP
  - the real subject: every frame cited, every Wikipedia URL pinned, images
    served from their frame, and the chart credited
  - the page: citations closed by default and in tab order, and the start
    screen over an inert shell
  - the loom credit and the loom SVG itself
- Docs: design.md got §Citations, reading headings, §Start screen,
  §Illustrations and §Palette transitions. The roadmap is reordered to
  content, then ask, then grow. Both instruction files got the status line
  and the citation rule.

- **Authoring tools, kept (Ken's call after the first wrap-up).**
  `create-tools/` has an index README and one directory per tool, each with
  its own README:
  - `draw-plates`: `plates.py` primitives plus `western_civ.py`, the 17
    plates.
  - `wiki-cite`: Wikipedia citations pinned to a revision.
  - `bar-chart`: a JSON spec to an accessible SVG, with the book-output spec
    as its example.
  - `trace-art`: Pillow, then npm potrace installed into the git-ignored
    `.scratch/tools`, then bands.

  Each was checked by regenerating what it made: all 17 plates, the chart
  and the loom came out byte-identical, and wiki-cite's revision URLs match
  the committed citations. Agents creating a subject may add tools. Whether
  grow may add or run them is left to grow's design (3364/3365), because it
  would mean running model-written code on the host. The tools are not in
  `just check`: they are authoring aids, and their output is.

- **Palette timing.** Ken tried the shipped 1s and set it to 1.5s.

## Verification

- `just check` passes (svelte-check with 0 warnings, prettier, eslint, 76
  tests), and so does `just build`.
- **Negative tests.** Each error below was planted in the real
  `printing-press/frame.json`. Each made `just check` exit 1, and when the
  plants were re-run through vitest alone, each failed in validation with its
  own message. It passes again restored.
  - the woodcut's media citation removed → `image "printing-shop-1499.jpg"
needs a media citation with a licence`
  - a Wikipedia citation's URL changed to `/wiki/` → `a Wikipedia citation
needs a permanent revision url (oldid=)`
  - the chart's licence removed → `a media citation needs a licence`
- The new unit tests were seen failing first where written first: the
  heading level and the nested quotes.
- **In the browser** (Playwright, headless Chromium, the built server on
  127.0.0.1:5310):
  - The start screen draws on and focuses Begin. → leaves the spine alone
    while it is open. Tab reaches Image credit and then leaves the page,
    because the shell is inert. Enter begins and focus lands on the spine
    slider; → then moves it. Esc also begins.
  - All 16 frames were screenshotted in context and reviewed as a set.
  - The printing-press reading loads both images (200) from
    `/media/printing-press/…`. Citations open from the keyboard.
  - The palette fade was sampled mid-transition, as above.
  - At 390px there is no horizontal overflow on the start screen or on a
    frame. Reduced motion stops the dial, the draw-on and the palette fade.
  - There were no console errors and no failed requests.
- Screen-reader output was **not** heard. The dialog semantics, the
  `<details>` control and the heading levels were checked in the DOM and in
  tests only.

## Repaired in passing

- **The reading's headings were at the frame title's level.** The pane's
  title is an `h2`, and markdown `##` also rendered as `h2`, which flattens
  the outline a screen reader navigates by. Sprint 001's placeholders had no
  headings, so it never showed. The renderer now sets reading headings one
  level down, and there is a test.
- The tripwire check moved into an exported `illustrationProblem`, so the
  start screen's SVG is tested by the same rule rather than a copy of the
  regex.

## Follow-ups

- **Enter before hydration does nothing.** The start screen's Begin button
  needs JavaScript. A reader who presses Enter in the first fraction of a
  second waits for hydration. That is acceptable for a POC; say so if not.
- **Palette mode and the scene's entrance: korg 3372.** After trying 1.5s,
  Ken wants two things. One is a reader setting for dark, light or mixed
  palettes. The other is a staged entrance on prev/next: small text at once,
  the drawing from 0s, the headline fading in from 1s and the accent word
  from 1.5s. The timings need his eyeball check before that item is done.

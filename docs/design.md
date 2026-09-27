# kloom design

Decisions from the founding brainstorm (2026-09-26). Change them freely, but
change this file in the same PR.

## What it is

A web page with the feel of the [inspiration video](https://x.com/IterIntellectus/status/2103212539895017864)
where scrolling moves a cursor along a timeline, plus a reading pane you can
dive into and an AI pane that grows the content. The part that brings a
reader back is the reading and the ability to add more; the visuals are the
hook.

## Visual language (from the video)

- **Palette tracks the era.** Dark night + gold for the mythic and modern
  bookends; parchment + engineering line drawings for the long middle. The
  palette is a property of each frame and transitions as the cursor moves.
  That is the _Mixed_ palette mode, the default; a reader may pick all-dark
  or all-light instead (§Settings).
- **Scene grammar.** A huge serif headline, usually in a collective "we"
  voice, with one accent word in red or gold ("BACK.", "VIRAL.", "WORK.",
  "LIFE."); one line illustration that draws itself on; small monospace
  metadata; optionally a big counter.
- **Persistent HUD.** Corner brackets; chapter label top-left; index
  top-right; position label bottom-left ("AD 1429"); counter bottom-right; a
  thin timeline bar along the bottom with a red cursor. In kloom that cursor
  is real: it is where you are on the spine.

## Layout

Three panes: **spine scroller** (left), **narrative** (right), **AI** (bottom).
A collapsible left nav may come later, once trails give it something to list.

## Content model

Engine-level and subject-agnostic from the start — the Cutler rule: the only
way to build a portable OS is to build it on multiple platforms from the
start. The second subject (AI) will not be a clean timeline, so time is not
baked into the engine.

- **Spine** — an ordered list of frames. The scroller walks it.
- **Segment** — a contiguous run of a spine with its own _label kind_. Western
  Civ is all dates; an AI subject might be dates until ~2012, then
  technologies ("Transformers", "Diffusion", "RLHF"). The HUD's position label
  comes from the segment.
- **Frame** — two halves, one per pane:
  - _scene_: headline, accent word, illustration (SVG), palette, metadata,
    optional counter;
  - _reading_: markdown narrative, charts, images, and **sources** —
    required, because this is history written with an LLM.
- **Trail** — a small spine anchored to one frame of its parent.
- **Storage** — files in git, one directory per frame under
  `subjects/<subject>/`. The site builds from them; git is the history of how
  the subject grew, and its undo.
- **Files** (sprint 001) — `subjects/<subject>/` holds `subject.json` (title
  and named palettes: scheme, background, ink, muted, accent, line),
  `spine.json` (segments, each `{id, title, labelKind, frames: [ids]}`),
  `trails/<id>.json` (`{id, title, anchor, spine}`) and
  `frames/<id>/{frame.json, reading.md, *.svg}`. `frame.json` carries
  `position {label, sort?}`, `scene` and `sources`. Label kinds are `date`,
  `category` and `technology`; only `date` segments need a `sort` and must be
  non-decreasing. Every frame sits on exactly one spine, and a trail's
  anchor must be a main-spine frame. Validation collects every problem in one
  pass and the site refuses to serve an invalid subject. Reading markdown is
  rendered with raw HTML escaped. Links and images are kept only for http(s)
  or scheme-less URLs, judged after the entity and control-character
  normalisation a browser applies. An illustration is inlined (so it can
  draw itself on) behind a regex _tripwire_ for script, style, embeds, links
  and handlers. That is not a sanitiser, and grow must not write an
  illustration until a real allowlist sanitiser replaces it. Giving each
  path `pathLength="1"` lets the draw-on animation work.
- **Citations** (sprint 002) — a frame may carry `citations`, stored as
  structured data and rendered as a Chicago notes-bibliography entry,
  alphabetised, in a collapsed _Citations_ control under Sources
  (`<details>`, closed by default). The house style applies to Wikipedia and
  every other site alike. Nothing appears in the narrative itself: no
  footnote markers. The per-frame Sources list stays as it was, and stays
  required.
  - Fields: `kind` (`web`, `wikipedia`, `book`, `article`, `media`),
    `title`, `url`,
    `accessed` (`YYYY-MM-DD`), and optionally `authors` (`{family, given?}` or
    `{name}`; for Wikipedia `{name: "Wikipedia contributors"}`), `container`
    (the site or collection), `publisher`, `place`, `published` (`YYYY`,
    `YYYY-MM` or `YYYY-MM-DD`; for Wikipedia, the revision's date, rendered
    "Last modified"), for journal articles `volume`, `issue` and `pages`, and
    for media `licence` and `file`.
  - Every citation needs a title, an http(s) url and an accessed date. Any
    Wikipedia url must be a permanent revision link (`oldid=`), because
    articles change.
  - An image or chart in the reading is a file in the frame's directory
    (served at `/media/<frame>/<file>` with a no-script policy), and it is
    shown only with a `media` citation naming that `file` and a `licence`.
    Where the licence needs attribution beside the work (anything but public
    domain or CC0), the image carries a short caption credit. Scene
    illustrations drawn for kloom need no citation; one traced or copied from
    somewhere does.
  - Content never reaches the page as HTML: the formatter emits text runs
    (plain, italic, or the URL), and the renderer escapes them.
  - Grow (3364) and the framework's authoring skill must emit `citations`
    in this shape; ask's "keep this" (3360) should carry the ones its answer
    used.
- **Reading markdown** (sprint 002) — the frame's title is the reading
  pane's `h2`, so the markdown's headings are set one level down: author
  sections as `##` and they render as `h3`. A table under a chart carries its
  numbers for screen readers.
- **Authoring tools** (sprint 002) — `create-tools/` holds the scripts that
  made the content (plates, Wikipedia citations, charts, traced art), one
  directory per tool with its own README. Skills for new subjects and grow
  point there; an agent creating a subject may add tools.
- **Palette counterparts** (sprint 003) — a palette may name a
  `counterpart`: a palette of the other scheme that stands in for it when
  the reader picks Dark or Light. Validation requires it to exist and to be
  of the other scheme. Without one, a palette is kept in every mode. So the
  subject decides its own dark and light looks, and the engine names none.
  A subject with several dark palettes keeps their variety in Dark mode;
  only the light ones are swapped.
- **Engine vs subject** — `engine/` code never names a subject;
  `subjects/<subject>/` holds content and theme. Extracting the framework later
  should be moving files, not untangling them.

## AI: ask vs grow

- **Ask** — a transient answer in the AI pane. A "keep this" action turns an
  answer into content. Asking never changes the story by itself.
- **Grow** — writes content:
  - (a) add frames to the main spine;
  - (b) create a trail anchored to a frame;
  - (c) both — a new frame with a trail.
- **Runtime** — a backend on the host runs headless `claude -p` with a
  content-writing skill; grow jobs are queued, async, and commit their files.
- **Provider interface** — every model call goes through one interface, so a
  Claude API adapter (or another provider) is an additive change, not a
  rewrite.

## Interaction

- **Scroll ownership.** The wheel over the spine pane moves along the spine;
  the wheel over the narrative scrolls the narrative. Never both — a good
  narrative is often longer than a screen.
- **Narrative sync is a setting.** Default (Ken's preference): manual — scroll
  the spine, then "Sync Narrative" when something is worth diving into.
  Alternative: the narrative follows the spine.
  The choice is remembered per browser.
- **One gesture, one frame.** Wheel deltas over the spine accumulate to a
  threshold, then a cooldown swallows the trackpad's inertia.
- **Keyboard first.** Left/Right move along the spine (Home/End jump to its
  ends); Up/Down scroll the narrative; S syncs the narrative; T enters the
  trail branching from the current frame and Esc leaves it; Tab moves into
  and out of the AI pane, and Esc anywhere in it returns to the spine. Keys
  typed into a text field stay there. Visible focus, ARIA
  roles, `prefers-reduced-motion` honoured. Accessibility is a requirement
  from sprint 001, not polish.
- **Trails.** Entering a trail swaps the scroller to it with a breadcrumb
  ("Main story > Printing press"); the parent spine shows a branch marker.

## Risks

- **Illustration quality** is the biggest one: Claude-drawn SVG varies. The
  POC hand-curates its frames to set the bar; the generating skill is written
  against them.
- **Accuracy**: sources are mandatory on every frame, and the grow skill must
  produce them.

## Start screen

Built in sprint 002 (korg 3359). The page opens on a modal start screen over
an inert shell: the subject's title, a Begin button (focused; Enter or Esc
begins) and, behind them, kloom's loom drawn on in the colours of the spine's
first frame, over a slowly turning inscribed dial. The loom is the
public-domain "Modern Loose Reed Power Loom" engraving from Richard Marsden's
_Cotton Weaving_ (1895), traced to vector; its source, licence and how it was
traced are in `src/lib/start/README.md`, and it is credited under the start
screen's collapsed _Image credit_. It is kloom's mark rather than the
subject's, so it lives in `src/`; the component is `engine/ui/StartScreen.svelte`.

## Illustrations (what worked in sprint 002)

The curated frames are the bar the grow skill is written against, so the
way they were drawn is part of the design:

- **Engineering plates, not pictures.** A section, elevation or diagram of
  the thing, with its geometry showing: the Pantheon's inscribed sphere, the
  _quinto acuto_ centres of Brunelleschi's dome, Eratosthenes' parallel rays
  and angle, a Platonic solid in wireframe. Construction lines are what make
  a drawing read like the video rather than clip-art.
- **Three weights.** Construction lines thin and faint
  (`stroke-width="0.6" opacity="0.55"`), secondary detail mid
  (`0.9`/`0.8`), the object at the drawing's full weight (1.25 in a
  400×300 viewBox). One colour: `currentColor`.
- **Drawn in order.** Each top-level `<g>` draws after the one before it
  (the engine staggers them), so order the groups as a draughtsman would:
  construction, then the object, then its details and labels.
- **Few labels.** Small monospace `<text>`, `fill="currentColor"
stroke="none"`, fading in once the lines are down. Numbers that matter
  belong in the scene's counter, not the drawing.
- **Geometry is computed, not guessed.** Solids, globes, helices, gears and
  waves were generated from their maths with `create-tools/draw-plates`,
  which is far more convincing than hand-placed curves. The tool's output
  is committed content and may be edited by hand.
- Every path keeps `pathLength="1"`, and nothing the illustration tripwire
  rejects.

## Palette transitions

The palette colours are registered custom properties (`@property`, syntax
`<color>`) and transition together on the shell, 1.5s ease-in-out, so every
consumer — accent words, buttons, borders, SVG strokes — fades with the
background instead of snapping ahead of it (korg 3370). Reduced motion turns
the transition off.

## Settings

Built in sprint 003 (korg 3373, 3372).

- **Two kinds, kept apart** (Ken, 2026-09-26):
  - **User settings** are one reader's choices. They are made in the settings
    pop-up and remembered per browser in localStorage, where every read and
    write is wrapped so blocked storage costs only the memory.
  - **App settings** belong to the deployment. They live in a config file on
    the server, such as the models on offer and their ids. Readers never edit
    them. The first one arrives with ask (3368).
- **The registry.** `engine/settings.ts` defines a `Setting` as
  `{id, label, choices: [{value, label}], default, storageKey}`. Every
  setting is a pick from a fixed list, and there is no free-text kind. A
  stored value that is no longer a choice falls back to the default, which
  covers a model that is dropped from the app config. The page builds the list
  and hands it to a `UserSettings` store (`engine/user-settings.svelte.ts`),
  so a row whose choices come from the server is built at runtime like any
  other. Values start at the defaults and are loaded on mount, so the server
  render and the first client render agree.
- **One control kind: a native `<select>` with a visible `<label>`.** Model
  rows must be drop-downs, so the palette mode is one too, for consistency
  rather than a radio group. A select is compact at 390px and needs no custom
  arrow-key handling.
- **A disclosure, not a modal.** The gear is a `<button>` (named
  "Settings", with `aria-expanded`/`aria-controls`) that shows a panel below
  it. It is not a `<dialog>`, for two reasons. A setting like the palette
  mode should show its effect live on the page behind the panel, which a
  modal would dim and make inert. And a few selects do not need a focus
  trap. Esc closes the panel and returns focus to the gear, and so does a
  click outside it (without moving focus). Tab runs gear, then the panel's
  controls, in document order.
- **Page keys stand down inside it.** The panel carries `data-own-keys`,
  and the shell ignores its page-wide keys (arrows, S, T, Esc) for any
  target inside such an element. A closed gear is an ordinary button, so the
  arrows still move the spine from it.
- **Placement:** the end of the narrative's toolbar, beside the other user
  setting. It is clear of the spine's corner brackets, and it wraps with the
  toolbar at phone width.
- **"Follow the spine" stays in the toolbar.** It is a user setting, but it
  sits beside the Sync Narrative button it modifies, and a reader toggles it
  while reading. Moving it behind the gear would cost a click and separate
  it from its context. It keeps its own `kloom.sync` key.
- **Palette mode:** Mixed (each frame's own palette, the default), Dark or
  Light, stored under `kloom.palette`. The OS `prefers-color-scheme` is not
  consulted. Mixed is the designed experience, the palette tracking the era,
  and a single scheme is a reader's explicit choice rather than an inference.
  The start screen follows the mode as well. It is server-rendered in the
  default mode, so a reader with a remembered Light choice sees it switch
  once on load.

## Scene entrance

Built in sprint 003 (korg 3372). The scene is keyed by frame, so every
move along the spine rebuilds it and the stages restart from zero, and a
burst of ← → never leaves a scene half-faded:

- **0s:** the small text (metadata, and the HUD's position and counter)
  appears at once, and the drawing starts drawing on. Top-level groups each
  take 1.4s at 0.25s steps, capped at 1.5s, so the drawing is complete by
  about 2.9s.
- **1s:** the headline, without its accent word, fades in over 1s.
- **1.5s:** the accent word fades in over 1s, so it is fully on screen at
  2.5s, just before the drawing's last group lands.

The numbers are four custom properties at the top of `.scene` in
`SpinePane.svelte` (`--headline-delay`, `--headline-fade`, `--accent-delay`,
`--accent-fade`). Ken signed off on them after the
eyeball check (2026-09-27), so they ship as first set: 1s / 1s / 1.5s / 1s. The headline
enters after the 1.5s palette fade is mostly done, so the words never arrive
in the old frame's colours. The live-region announcement is unchanged, and
screen readers get the whole headline at once. Reduced motion shows
everything immediately.

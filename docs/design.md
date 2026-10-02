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

Three panes: the **spine scroller** on the left, and the **narrative** and the
**AI** pane on the right. Where the AI pane sits is a reader setting, "Layout"
(`kloom.layout`, sprint 010, korg 3377). Streamed answers in a bottom strip
competed with the reading for height, so four layouts were built and compared:

- **Two panes, Narrative and AI as tabs** (`tabs`): the default, and **Ken's
  pick** (2026-09-28). The right-hand pane has two tabs, Narrative and AI. The
  AI control (§The AI control) stays at the foot of the pane under **both**
  tabs, so a reader can keep reading while they type a question. The AI tab
  holds the results: the answer, its actions and the grow jobs. Sending does
  not switch tabs. When a result lands while the Narrative tab is showing, the
  AI tab gets a dot and the status line says "Answer ready, on the AI tab",
  with a "Show it" link. Switching to the AI tab clears it. The settings gear
  moves up into the tab row, so it stays reachable from either tab.
- **Three columns** (`columns`): spine | narrative | AI. Ken's alternative,
  kept as the switch away from tabs.
- **AI along the bottom** (`strip`): the original layout.
- **AI below the narrative** (`split`): the right-hand pane split vertically.

The last two are still built so they can be compared. Dropping them is a
settings-list edit (korg 3377's record).

**The tab row heads the right-hand pane in every layout** (sprint 011, korg
3409). Its tabs are Narrative, then **Notes** when there is a reader
(§Notes), then AI in the tabs layout. The settings gear sits at its end, in
every layout. A layout with only one tab (no reader, not the tabs layout)
shows no tab list, just the gear. The Notes tab says how many notes the frame
has ("Notes 2", and ", 2 on this frame" to a screen reader).

**Keyboard in the tabs layout** (the ARIA tabs pattern): Tab reaches the
selected tab only (a roving tabindex). Left and Right move between the tabs
and wrap, and Home and End jump to the first and last. They activate the tab
as they move. The tab handles those keys itself (`engine/keys.ts` `tabKey`),
so the spine does not move while focus is on a tab. The tab list sits in
none of `.spine`, `.narrative` and `.notes`, so the character shortcuts do
nothing there. The AI tab's panel is the AI pane's results region, inside
`.ai`: Esc from it returns to the spine, and the shortcuts stand down there,
as in every layout. S also brings the Narrative tab forward, because syncing
the reading means wanting to see it.

**Dividers** (sprint 010, Ken, 2026-09-28): the reader can drag the line
between panes, to shrink the picture while deep in the reading, say. Every
layout has one between the spine and the right-hand side. Three columns has a
second, before the AI pane, and the split has one between the narrative and
the AI pane. A divider follows the ARIA window-splitter pattern
(`Splitter.svelte`): a focusable `role="separator"` with its value as a
percentage. Left/Right (Up/Down for the split's) move it 2%, Home/End jump to
its limits, and Enter or a double-click puts it back. It handles those keys
itself (`splitKey`), so the spine stays put. The limits keep the spine
between a quarter and three quarters of the width, the AI column between 15%
and 45%, the narrative at least a fifth in three columns, and the split
between 20% and 85% (`engine/panes.ts`). A divider shares its pane's grid
cell, so every pane is placed explicitly and the divider cannot push one
along. Sizes are remembered per layout in `kloom.panes`: a size is not a pick
from a list, so it is kept beside the settings registry, not in it.

**The keyboard help** is one bar along the foot of the whole page, below every
pane in every layout (Ken, 2026-09-28). It was the last line of the AI pane,
where it took room from the text box.

**Phone width** (below 760px): every layout collapses to one column (spine,
then the tab row, then narrative or notes, then AI). The tabs layout keeps its tabs, with the AI tab's
panel taking the narrative's height. There are no dividers.

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
- **Frame** — two halves, one per pane, and a _topic_:
  - _topic_ (sprint 020): what the frame is about, in a plain title of at
    most 40 characters ("Alignment faking", "IBM tabulators at Los
    Alamos"). The headline is evocative and the position label may be a
    date, so neither says on its own what a frame is. The topic is what
    names a frame where it stands alone (§Topics);
  - _scene_: headline, accent word, illustration (SVG), palette, metadata,
    optional counter, and an optional _dedication_ (sprint 028, korg
    3475): `{kicker, name, note?}`, for a frame that dedicates a subject to
    someone. The scene then sets the name in its own case, with the kicker
    in small capitals above it and the note (such as "Retired") just below,
    in place of the headline, and the metadata beneath. The narrative's
    heading reads the same. The headline and accent stay, and still name
    the frame on every other surface (contents, map, the spine's screen
    reader label), so the accent is still unique. A dedication is a
    subject's choice, never the engine's; the first is the last frame of
    In the Blood;
  - _reading_: markdown narrative, charts, images, and **sources** —
    required, because this is history written with an LLM. Since sprint
    008 every frame flags at least one key-source citation, and the Sources
    list is built from those (§Content model, Citations).
- **Trail** — a small spine anchored to one frame of its parent.
- **Storage** — files in git, one directory per frame under
  `subjects/<subject>/`. The site builds from them; git is the history of how
  the subject grew, and its undo.
- **Files** (sprint 001) — `subjects/<subject>/` holds `subject.json` (title,
  an optional `subtitle` of at most 60 characters (sprint 026, korg 3465),
  and named palettes: scheme, background, ink, muted, accent, line),
  `spine.json` (segments, each `{id, title, labelKind, frames: [ids]}`),
  `trails/<id>.json` (`{id, title, anchor, spine}`) and
  `frames/<id>/{frame.json, reading.md, *.svg}`. `frame.json` carries
  `topic`, `position {label, sort?}`, `scene` and `citations`. Label kinds are `date`,
  `category` and `technology`; only `date` segments need a `sort` and must be
  non-decreasing. Every frame sits on exactly one spine, and a trail's
  anchor must be a main-spine frame. No two frames of a subject share an
  accent word, ignoring case and the full stop (sprint 006; grow is held to
  it too). A time-sensitive frame may carry `asOf` (`YYYY-MM` or
  `YYYY-MM-DD`): the reading pane shows "As of September 27, 2026" beside
  the position, and ask's prompt says the frame is dated. Validation collects every problem in one
  pass and the site refuses to serve an invalid subject. Reading markdown is
  rendered with raw HTML escaped. Links and images are kept only for http(s)
  or scheme-less URLs, judged after the entity and control-character
  normalisation a browser applies. An illustration is inlined (so it can
  draw itself on), so it passes an allowlist sanitiser (§Illustration
  sanitiser, sprint 005). Giving each path `pathLength="1"` lets the draw-on
  animation work. The loader skips hidden directories under `frames/`.
- **Citations** (sprint 002; reshaped in sprint 008, korg 3405) — a
  frame's `citations` are stored as structured data and rendered as Chicago
  notes-bibliography entries, alphabetised, in a collapsed _Citations_
  control under Sources (`<details>`, closed by default). The house style
  applies to Wikipedia and every other site alike. Nothing appears in the
  narrative itself: no footnote markers.
  - **Sources are derived from citations** (Ken, sprint 008). A citation
    carries `key: true` when the frame chiefly rests on it, and the frame's
    Sources list is its key citations in the order written, each as
    "Authors, Title" (Wikipedia: "Title — Wikipedia"), linked, with where
    and when it appeared and the citation's own `note`. Every frame flags
    at least one key-source citation, and validation enforces it. Authors
    keep one list, not two. A `sources` field in `frame.json` is refused,
    so content in the old form cannot go silently unshown. A key source
    links the URL that was read, so a Wikipedia source links its pinned
    revision, not the live article.
  - Fields: `kind` (`web`, `wikipedia`, `book`, `article`, `chapter`,
    `report`, `media`, `letter`, `encyclopedia`, `diary`, `case`, `statute`), `title`, `url` and/or `doi`, `accessed`
    (`YYYY-MM-DD`), and optionally `key`, `note` (a key source's remark in
    the Sources list: a page, why it matters), `authors` (`{family,
given?}` or `{name}`; for Wikipedia `{name: "Wikipedia contributors"}`),
    `container` (the site, journal or collection; for a chapter, the volume
    or proceedings), `editors` (a chapter's, or an edited book's), `publisher`, `place`,
    `number` (a report's), `published` (`YYYY`, `YYYY-MM` or `YYYY-MM-DD`;
    for Wikipedia, the revision's date, rendered "Last modified") with
    `circa: true` for an approximate date ("ca. 1951"), for journal
    articles `volume`, `issue` and `pages`, and for media `licence` and
    `file`. `etAl: true` ends a long author list with "et al." in the entry
    and in a caption credit (sprint 006): a paper with hundreds of authors
    lists the first.
  - **Older, translated and second-hand sources** (sprint 027, Ken's
    decision of 2026-10-01 on korg 3461). All optional, so no existing
    citation changed meaning:
    - **Early dates.** `published` (and a letter's `written`) also takes a
      year AD of one to three digits with no leading zero (`888`) and a
      year BC (`1550 BC`, a space before `BC`, no month or day), each with
      `circa` ("ca. 1550 BC"). Written as a string, a date reads as it is
      rendered, and the form is unambiguous: `publishedYear` turns it into
      a signed year (-1550), the convention of a frame's `position.sort`,
      to compare or sort by. A four-digit year with a leading zero
      (`0888`) is still ISO 8601's and still accepted.
    - **Roles.** `translators` ("Translated by …") and `engravers`
      ("Engraved by …"), after the title (and after an edited book's
      editors, as a title page reads); `recipients` on a letter.
    - **Fields.** `edition`, written as it reads ("2nd ed.", "Loeb
      Classical Library ed."): after the title, or, for a chapter or an
      entry, in the volume's list ("In _Volume_, edited by …, 2nd ed.,
      pages"). `volumeYear` on an article whose volume came out later
      than the year it is for: "(2016; published 2017)"; it may not be
      later than `published`. `language`, a code (`de`, `grc`), rendered
      "In German." before the access date; a Wikipedia other than
      English needs it (its url's host says which), and its key source
      reads "Title — German Wikipedia". Its `container` stays "Wikipedia,
      The Free Encyclopedia".
    - **Kinds.** `letter`: "Author. "Title." Letter to Recipients, Date
      written. In _Container_, vol. N, pages. Place: Publisher, Year." It
      needs `recipients`. `encyclopedia`: an entry, set like a chapter, "In
      _Encyclopedia_, edited by …, edition." It needs its `container`. A
      chapter of a numbered report is a `chapter` with the report's
      `number`, set after its container.
    - **Seen, not read.** `citedIn` names the work in whose references or
      quotation a source was seen ("Cited in Gleick, _Genius_, p. 247."),
      and `read` says how much of it was read when not all of it:
      `abstract`, `first-page` or `excerpt` ("Read in its abstract.",
      "Read in its first page.", "Read in an excerpt."). Both are rendered
      in the bibliography and in the key source's line, so a reader sees
      what the frame rests on. They replace the note "Read in its
      abstract", which only the Sources list showed. (Sprint 027 called the
      first `abstractOnly: true`; sprint 029 widened it to `read`, Ken's
      decision of 2026-10-01 on korg 3473, and moved every use and every
      note that meant exactly one of the three. Frame validation refuses
      `abstractOnly` now; a kept answer saved before still carries it in its
      copy of a citation, and is still read and shown as "Read in its
      abstract.")
  - **Forms from _In the Blood_** (sprint 029, Ken's decisions of
    2026-10-01 on korg 3473):
    - **A source seen only in another work** may stand without a url or a
      doi, and then without `accessed`, when its `citedIn` names, by title,
      a work the same frame cites with a url or doi. Validation checks the
      chain. Its entry has no link, and it cannot be a key source: the
      Sources list links what was read, which is the citing work.
    - **`diary`**: a dated entry in a named edition. `title` is the diary,
      `written` the entry's date (required): "Pepys, Samuel. Diary entry,
      November 14, 1666, in _The Diary of Samuel Pepys_, edited by Henry
      B. Wheatley. pepysdiary.com. London: George Bell & Sons, 1893." The
      date reads as the house style's other dates do.
    - **A mirror, when no official copy exists anywhere**: the work is
      cited with the mirror's url and `mirror: true`, rendered after the
      url, "(copy at generalstaff.org)", and in the key source's line
      ("Copy at generalstaff.org"). Not with a `doi`. Whenever an official
      copy exists, cite the work, never the mirror.
    - **JSTOR**: an article held only on JSTOR is cited by its stable url,
      `https://www.jstor.org/stable/N`, with no Crossref check (JSTOR's
      `10.2307/…` DOIs do not resolve through Crossref). Any other
      www.jstor.org url is refused.
  - **Forms from _Keeping Watch_** (sprint 033, Ken's decisions of
    2026-10-02 on korg 3478):
    - **`case`** and **`statute`**, rendered in legal form after the
      name, with where it was read (`container`, `publisher`) after that,
      and no `authors`. A case: its name in italics, then its `reporter`
      (`{volume, name, page}`, all three) and a parenthetical of its
      `court`, when the reporter does not say it, and the year of
      `published`, which it needs: "_Sparger v. Worley Hospital, Inc._,
      547 S.W.2d 582 (Tex. 1977)." A court's `neutral` citation stands in
      for the reporter and carries its own year: "_Getty Images v
      Stability AI_ [2025] EWHC 2863 (Ch)." A statute: its name, then its
      `publicLaw` ("Pub. L. No. 80-36") and its `code` (`{volume?, name,
page?}`: the session laws or the code it is in), the year left out
      where the name or the volume already says it: "Army-Navy Nurses Act
      of 1947, Pub. L. No. 80-36, 61 Stat. 41." A session law's `chapter`
      and `section` come before the volume it is printed in ("ch. 192,
      § 19, 31 Stat. 748, 753", a pinpoint after a comma); a code cited by
      section, or a state's session laws by chapter, take theirs after it
      ("42 C.F.R. § 482.23", "2023 Or. Laws ch. 507"). A statute needs a
      `publicLaw` or a `code`. The Sources list names either by its legal
      form. The 22 statutes, regulations and cases written before as
      `chapter`, `web`, `book` or `report` were moved; "Andersen v.
      Stability AI" stays `web`, a journal's piece about the case.
    - **`read: "record"`**, "Read in its catalogue record only.", for a
      work whose own bibliographic record was reached (Crossref, a
      publisher's landing page) but not its text. `citedIn` stays for a
      work known only through another work.
    - **A chart's data source by its DOI.** A `media` citation's `doi` is
      its data's, rendered with its credit: "Data: https://doi.org/…" in
      the entry and "data doi:…" in the caption credit, where the entry's
      own link is its `url`, an image's or a file's page. A chart drawn
      here may have the DOI alone. `bar_chart.py` prints the citation.
      A media citation's `number` (a NARA or Navy identifier, an image
      number) follows its container.
  - A `media` citation may credit an image by its en.wikipedia.org file
    page (`/wiki/File:…`) without a revision: it is an image's page, not
    an article (sprint 027).
  - **Kinds.** `chapter` is a chapter or a paper in an edited volume, a
    proceedings or a symposium: "In _Volume_, edited by …, pages. Place:
    Publisher, Year." It needs its `container`. `report` is a technical,
    committee or institutional report, or a lab's system card: title in
    italics, then its `number`, series, and "Place: Publisher, Date".
  - **DOI.** `doi` holds the bare DOI (`10.1109/5.58323`) and the entry
    links it at doi.org, in place of the url (a `media` citation's is its
    data's, above). A doi.org `url` is refused:
    it goes in `doi`.
  - Every citation needs a title, an http(s) url or a doi, and an accessed
    date, except one seen only in another work (above). Any Wikipedia url must be a permanent revision link (`oldid=`),
    because articles change.
  - An image or chart in the reading is a file in the frame's directory,
    shown only with a `media` citation naming that `file` and a `licence`.
    A raster image is served at `/media/<subject>/<frame>/<file>` with a
    no-script policy. An SVG is inlined through the illustration sanitiser
    (§Charts, sprint 008).
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
  directory per tool with its own README. Sprint 006 added `subject-plan`
  (the spine and trails from a plan, holding only the frames written so
  far), `commons-media` (a freely licensed image and its `media` citation)
  and a log scale for `bar-chart`. Sprint 008 added `read-source` (a PDF's
  text, or its scanned pages as PNG), the first Python tool with a
  non-stdlib dependency: Ken allowed one, declared inline for `uv run` and
  kept out of the app. Skills for new subjects and grow point there; an
  agent creating a subject may add tools.
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
  content-writing skill; grow jobs are queued, async, and commit their files
  (§Grow).
- **Provider interface** — every model call goes through one interface, so a
  Claude API adapter (or another provider) is an additive change, not a
  rewrite. Built in sprint 004; see §Ask.

## Ask

Built in sprint 004 (korg 3360).

- **The Provider interface** (`engine/ai/provider.ts`). `ask(request)`
  returns an async iterable of `{type: 'text', text}` chunks in order. A
  failure is one `{type: 'error', message}`, after which it ends; the answer
  is complete when the iterator ends. The request carries:
  - an `AskContext`: the subject's title; the frame's id, title, position,
    segment, reading markdown and citations; and the trail, if any;
  - the question;
  - a model id the server has already checked;
  - an `AbortSignal`.

  The prompt (`engine/ai/prompt.ts`) is shared by every adapter. It numbers
  the frame's citations (every source is one since sprint 008), and asks the
  model to mark what it drew on with `[n]`. A Claude API adapter is one more
  class beside `ClaudeCliProvider`, chosen by `provider.kind` in the app
  config.

- **The server builds the context.** The client sends
  `{subject, frame, trail, question, model}` to `POST /api/ask`. The server reads the
  frame's content from the library (§Serving), never from the request, and refuses an unknown
  frame, or a trail that does not hold the frame. Questions are capped at
  2000 characters. The model is honoured only if the app config lists it;
  anything else gets the default.
- **The first adapter: `claude -p`** (`engine/ai/claude-cli.ts`). It uses the
  host's logged-in subscription, as karc does. Measured with
  Claude Code 2.1.283:
  - spawned with an argv array, with no shell in between;
  - run in an empty working directory (`$TMPDIR/kloom-ask`), so no project's
    `CLAUDE.md` applies;
  - `--tools ""`, because ask needs no tools; `--strict-mcp-config`,
    `--setting-sources ""` and `--disable-slash-commands`, so no MCP server,
    hook or skill loads; `--no-session-persistence`;
  - kloom's own `--system-prompt`, with the prompt on stdin.

  `--bare` is not usable: it takes only an API key, not the subscription.
  A turn that runs past `provider.timeoutSeconds` (120) is killed and reported.

- **Streaming works cleanly.** `--output-format stream-json --verbose
--include-partial-messages` emits `content_block_delta`/`text_delta`
  lines, and the adapter yields each one. The final `result` line decides
  the outcome: `is_error: true` is an error (an unknown model reports
  itself this way), and a result with nothing streamed before it becomes
  the text. A short answer on Sonnet 5 took 4–8s.
- **Wire format.** The endpoint responds with NDJSON `AskStreamEvent`s:
  - `start` (the answer's id, the model, the frame);
  - `queued`, if another turn is running;
  - the text chunks;
  - exactly one `done` or `error`.

  When the reader closes the stream (Stop, a new question, or leaving the
  page), the turn is aborted and the process killed.

- **One turn at a time.** `TurnQueue` runs one turn on the host, lets three
  wait (each told it is queued), and refuses a fifth with 503. A request
  aborted while it waits leaves the queue.
- **Moving the spine during a turn** neither stops the turn nor changes what
  it is about. An answer belongs to the frame it was asked about, and its
  heading names that frame ("About Knowledge went VIRAL. · Sonnet 5"). A new
  question replaces the current one, cancelling it if it is still running.
- **Which frame.** The question is about the frame in the reading pane, which
  can differ from the spine's when the reader has turned following off: they
  are asking about what they are reading. The trail is sent only if it holds
  that frame. With following on (the default), moving the spine mid-answer
  moves the reading pane too, and the answer stays put: its heading names
  its frame and a line under it says the reader has moved on.
- **Transient.** The answer shows in the AI pane, rendered with the reading's
  markdown rules and with images turned off (a model's image would be a
  request to anywhere). It is not stored, and a reload forgets it; the pane
  holds the latest answer only (no history; a taller pane did not change
  that, sprint 010). The results (answer and grow jobs) scroll in one
  focusable region, `#ai-results`, marked `data-own-keys`, so the arrows
  scroll it. A `role="status"` line announces asking, queued,
  answering, ready, stopped and failed; the streaming text itself is not a
  live region.
- **Keep this.** Once an answer is done, "Keep this" sends only its id to
  `POST /api/keep`, with the subject. The server remembers finished answers (the last 50, for
  an hour) and writes what it remembers, never text the client sends back.
  Since sprint 011 it goes into the reader's store, under the reader who
  kept it (§Kept answers). Before that it was a file,
  `<dataDir>/<subject>/kept/<id>.json`. A kept answer is not subject
  content, and asking never writes subject content.
- **The kept-answer format** (`engine/ai/kept.ts`, for grow, korg 3364):

  ```json
  {
  	"kind": "kloom.kept-answer",
  	"version": 1,
  	"id": "20260927T170911Z-bdded89b",
  	"subject": "western-civ",
  	"anchor": { "frame": "printing-press", "trail": null },
  	"question": "Why did printing spread so fast?",
  	"answer": "Markdown, as the model wrote it, [n] markers and all",
  	"citations": ["the frame's citations the answer marked, first use first"],
  	"sources": [],
  	"provider": "claude-cli",
  	"model": "claude-sonnet-5",
  	"askedAt": "2026-09-27T17:09:11.000Z",
  	"keptAt": "2026-09-27T17:09:20.000Z"
  }
  ```

  The `[n]` numbers refer to the frame's references in prompt order, and
  `citations` carries exactly the ones used, in the §Citations shape. The id
  is the ask time plus 8 random hex digits, safe as a file name. Grow checks
  one with `keptAnswerProblems` before reading it. A web turn's pages
  are carried in an optional `webCitations` (§Web search for ask).
  `sources` once held the plain sources an answer marked. Since sprint 008
  every source is a citation, so it is always empty. It stays so the format,
  and the answers already kept, remain version 1.

## Web search for ask

Built in sprint 005 (korg 3376, Ken's decisions of 2026-09-27).

- **An app setting.** `ask.web` is `allow` (committed), `offer` or `deny`,
  and an absent `ask.web` means `deny`. The reader's control is a "Web"
  checkbox stacked over the Ask button (sprint 010: it was "Include web",
  beside Send), shown for the ask verb only and unless the config is `deny`. It starts
  checked under `allow` and unchecked under `offer`. It is a per-question
  choice, not a remembered setting.
- **The server enforces it.** A request's `web: true` is honoured only when
  the config is not `deny` (`resolveWeb`), the same pattern as the model.
- **Only WebSearch and WebFetch**, offered and pre-approved
  (`--tools`/`--allowedTools`), with the rest of ask's lockdown unchanged.
  Pages can carry prompt injection. With only these two tools the worst
  case is a wrong answer, never an action. A web turn's timeout is
  `provider.webTimeoutSeconds` (180).
- **"Searching the web…"** A tool starting in the stream becomes a
  `{type: 'status', status: 'searching'}` provider event, shown in the
  status line. Text streamed before it was the model thinking aloud, so the
  status also resets the answer, on the server and in the pane.
- **Web sources.** The web prompt asks for `[W1] Title — URL` lines after
  the answer, and "keep this" turns them into `webCitations`: `web`
  citations accessed on the day asked. A Wikipedia page is pinned to its
  current revision at keep time (`engine/ai/wikipedia.ts`, twin of
  `create-tools/wiki-cite`), as a `wikipedia` citation. If the lookup fails,
  the keep fails rather than store an unpinned link.

## Grow

Built in sprint 005 (korg 3364).

- **Verbs.** `frames` adds one to three frames to the main spine. `trail`
  adds a trail of two to four frames from the anchor, which must be a
  main-spine frame (or extends the trail already branching from it). `both`
  adds one main-spine frame and a trail from it. Any of them may turn a
  kept answer into content, when the anchor becomes the kept answer's
  frame. A reader grows from their own kept answers: the job reads it from
  the store of the reader who queued it (`by`), and once the job commits,
  the kept answer records the frames it grew into (§Kept answers).
- **The instructions are a skill in the repo**, `skills/grow/SKILL.md`,
  not prompt strings in code. It is the system prompt, frontmatter
  stripped, and the seed of the framework's "generate a subject" skill. It
  quotes §Illustrations and §Citations, and the job copies `docs/design.md`
  and the create-tools READMEs (plus `plates.py`) into `reference/`. The
  per-job prompt (`growPrompt`) names the verb, the anchor, the kept answer,
  whether the web is available, and the reader's words.
- **The sandbox.** The model never touches the subject. The job copies
  `subject.json`, `spine.json`, `trails/` and `frames/`, and the name
  registry as `names/`, into its own directory under `$TMPDIR`
  (`kloom-grow-<job>-…`), writes `reference/frames.md` (every served frame
  a connection may name, with its title and position), and `claude -p`
  runs there:
  - `--tools Read,Write,Edit,Glob,Grep` (plus WebSearch and WebFetch when
    `grow.web` is true), and no shell, so no model-written code runs on the
    host and create-tools are references, not tools, for grow;
  - `--permission-mode acceptEdits`, so Write and Edit act inside the
    working directory and a write anywhere else is refused (headless, a
    prompt is a no);
  - `--disallowedTools Read(~/**) Edit(~/**) Write(~/**)`, so the home
    directory, reads included, is out of reach, and a page read on the web
    cannot talk the model into reading a secret. The job refuses a work
    directory inside the home directory;
  - the rest of ask's lockdown: no MCP, settings, skills or session.

  Measured with claude 2.1.283: a write in the working directory landed; a
  write to `~` or `/tmp`, and a read of `~/.bashrc`, were refused.
  The sandbox is outside `subjects/<subject>/` on purpose. A half-written
  frame there would make the live subject fail validation mid-job, and a
  directory inside the repo would pick up its `CLAUDE.md`. What reaches
  the subject is still only files under `subjects/<subject>/`.

- **What may come back** (`growthProblems`, `engine/ai/grow.ts`). Additions
  only: `subject.json` and every existing frame unchanged; existing
  segments, trails and frames kept, in order; new frame ids lowercase and
  dashed; a new frame holding only `frame.json`, `reading.md` and `*.svg`,
  each under 200 KB, every SVG passing the sanitiser; and the verb's own
  shape. Then `validate()` over the whole copy, against the registry as
  the job left it.
- **Names and connections** (sprint 018, korg 3440; `linkGrowthProblems`).
  A grown reading marks names as any reading does (§Connections), and **a
  job may add names** (Ken, on 3440) **but change none**: an existing name
  file must come back as it went, and a new one must be valid, hold no
  Wikidata item another name holds, and be marked in a frame the job
  wrote. A new frame's connections, and a new name's home, must name a
  frame in `reference/frames.md` or one the job added, never itself. A
  connection is stored on the new frame, since existing frames are
  unchanged, and shows on both ends as every connection does.
- **One repair turn.** If the first turn leaves problems, the model gets
  one more turn over the same directory with the list (`repairPrompt`).
- **A validation failure leaves no commit.** Nothing is copied into the
  subject. The job fails with the problems (up to 20), which the AI pane
  shows under "What the validator found". The work directory is kept for
  inspection.
- **Applying.** Under a gate that makes page loads and asks wait
  (`src/lib/server/subject.ts`), the job refuses if the subject has
  uncommitted changes or differs from the copy it started from ("queue it
  again"). Otherwise it renames each new frame in from a hidden staging
  directory, replaces the changed trail files and `spine.json`, writes the
  new name files into the registry (refusing, "queue it again", if the
  registry changed while the job ran), and commits exactly those paths.
  The registry must be in the subject's repository, as it is in the
  checkout and the service's content clone. If anything fails, every file is put back and the
  index reset. The running site shows the new frames on the next load, with
  no rebuild.
- **The commit.** The committer is `kloom grow <grow@kloom.local>`. The
  author is whoever queued the job (§Who may write, sprint 007), or
  `kloom grow` for a job that predates identities. The commit is made with
  `--no-verify`. The message:

  ```
  grow(<subject>): add <frame ids>[; trail <ids>]

  <the model's two or three sentences>

  Job: <id>
  Verb: frames|trail|both
  Anchor: <frame>
  Request: <the reader's words>
  Kept answer: <id>            (when one was used)
  Names: <name ids>            (when it added names)
  Model: <model id> (<provider>)
  Web: yes|no
  Requested-by: <name> <<login>> (<via>)   (when the job has a requester)
  ```

- **The queue** (`GrowQueue`, `src/lib/server/grow.ts`) runs one job at a
  time, separately from ask's turns, and lets ten wait. There is one queue
  per subject (sprint 006), and they share one runner slot, so the host
  still runs one grow job at a time; a job waiting on another subject's
  says so. Each job is a
  `kloom.grow-job` JSON file under `<dataDir>/<subject>/grow/`, rewritten
  atomically at each step. The queue is loaded at server start
  (`hooks.server.ts` `init`), so **a restart resumes it**. A `queued` job
  waits again. A `running` job is re-run from a fresh copy, once, since
  nothing was applied. An `applying` job is failed with "check git status",
  because the subject may be half-written.
- **The model** is the reader's "Grow model" setting (default Opus 5.5,
  `grow.defaultModel`), captured when the job is queued. The server honours
  it only if the config lists it. The job and the commit record it.
- **API.** `POST /api/grow` `{subject, verb, frame, request, kept, model}`
  returns 202 and the job. `GET /api/grow?subject=` lists that subject's ten
  newest. Grow is asked for through the AI pane's one control (§The AI
  control); its job list sits in the results. The pane polls every 3s while
  a job is live, announces the outcome in the status line, and reloads the
  page's data when one lands. After "Keep this", a "Grow from this" button
  attaches the kept answer and picks a grow verb.

## The AI control

Ask and grow are one control (sprint 010, korg 3411): a verb, one text box
and a send button, in that Tab order (the "Web" box sits between the text and
the button when it shows). The verb has its own row; the text box takes the
rest of the width beside a narrow column of Web over a small button, so a
question has room before it wraps (Ken, 2026-09-28). The verbs come from `engine/ai/control.ts`.

- **The verb** is a native `<select>`. "Ask a question" is first and the
  default. Grow's verbs follow ("Grow: new frames on the main spine", "Grow:
  a side trail from this frame", "Grow: a new frame with its own trail") only
  when the app config has grow. Without grow there is no select at all, only
  the text box and Ask.
- **What follows from the verb:** the button's word (Ask or Grow), the
  placeholder, the text box's label, and the model setting that applies (Ask
  model or Grow model). "Web" is offered for ask only; grow's web
  access is the app config's `grow.web`.
- **Grow reads as the bigger action**, without a confirm dialog. Its button
  is outlined and bold, and a line under the control says the job runs on the
  grow model and commits new content to the subject. A confirm was rejected:
  the reader has already chosen a grow verb on purpose, and the verb resets
  (next point), so an accidental grow takes two deliberate steps.
- **The verb resets to Ask after each grow** is queued. Grow spends and
  commits, so it is never the sticky choice. That reset is also the quick way
  back to Ask, so there is no separate shortcut.
- **Enter sends and Shift+Enter starts a new line**, for either verb. While
  an answer streams, the Ask button reads Stop. Choosing a grow verb
  mid-answer still queues the job; the answer carries on.

## Interaction

- **Scroll ownership.** The wheel over the spine pane moves along the spine;
  the wheel over the narrative scrolls the narrative. Never both — a good
  narrative is often longer than a screen.
- **The narrative follows the spine** (Ken, 2026-09-27, sprint 006, korg
  3391). Moving along the spine turns the reading to that frame. Separate
  movement was the first default, with a "Sync Narrative" button, and it
  proved the wrong one in use. Not following is a reader setting,
  "Narrative: Stays until synced", in the settings control (`kloom.followSpine`).
  With it, the reading stays put until S brings it to the spine, and the
  toolbar's status line says where each one is. The button is gone; S
  remains.
- **One gesture, one frame.** Wheel deltas over the spine accumulate to a
  threshold, then a cooldown swallows the trackpad's inertia.
- **Keyboard first.** Left/Right move along the spine (Home/End jump to its
  ends); Up/Down scroll the narrative; S syncs the narrative; T enters the
  trail branching from the current frame and Esc leaves it (S matters only
  when the reader has turned following off); B bookmarks the frame on the
  spine, or removes its bookmark (§Reader data); N adds a note (§Notes);
  A annotates words of the reading (§Annotations); C opens the table of
  contents (§Contents); R goes back after a jump (§Connections); M opens the
  map (§The map); D jumps to a random frame in this subject and W to a
  random frame anywhere in the library (§Random); Tab moves into
  and out of the AI pane, and Esc anywhere in it returns to the spine. In the
  tabs layout, the arrows on a tab move between the tabs, and on a divider
  they move the divider (§Layout). Keys
  typed into a text field stay there. `engine/keys.ts` (`pageKey`) decides
  what a press means from where focus is, and the shell acts on it.
- **Character shortcuts are scoped** (WCAG 2.1.4, sprint 004, korg 3366). S,
  T, B, N, A, O, C, R, M, D and W act only while focus is inside the spine, the narrative or the
  notes. They do nothing in the AI pane, in the settings panel, in the note
  editor, or on the bare page.
- **And remappable** (WCAG 2.1.4's other remedy, sprint 011, korg 3363).
  Each character shortcut is a setting under "Keys": any letter, or Off
  (`kloom.key.sync`, `.trail`, `.bookmark`, `.note`, `.annotate`,
  `.my-notes`, `.contents`, `.back`, `.map`, `.random`, `.anywhere`). `keymapOf` turns the
  settings into a keymap and `pageKey` reads it. The help bar, the Add a note
  button, the trail buttons and the sync line all show the reader's letters,
  and leave a key out when it is off. A letter given to two shortcuts is
  allowed: the first in `SHORTCUTS` order acts, and the settings panel says
  which. The arrows, Home/End, Esc and Tab are not remappable. They are not
  character keys, so 2.1.4 does not reach them, and they are the slider's,
  tabs' and splitter's own ARIA keys, which assistive technology expects.
  The arrows, Home/End and Esc are not character keys, so they stay
  page-wide, except in a text field, an element marked `data-own-keys`, or
  the reading while words are being chosen in it (§Annotations).
  The hint bar says so. Visible focus, ARIA
  roles, `prefers-reduced-motion` honoured. Accessibility is a requirement
  from sprint 001, not polish.
- **Trails.** Entering a trail swaps the scroller to it with a breadcrumb
  ("Main story > Printing press"); the parent spine shows a branch marker.

## Contents

Random access for long subjects (sprint 016, korg 3433). Stepping the spine,
the timeline bar and the bookmarks were the only ways to move. That is
slow in the AI subject's 66 frames. `engine/contents.ts` decides what is
listed and `engine/ui/Contents.svelte` draws it.

- **Where.** An icon button in the spine's HUD, left of the bookmark,
  in `IconButton`'s look. It is there with or without a reader. C opens
  it too: a remappable character shortcut, scoped like the others
  (§Interaction).
- **What.** The main spine's frames under their segment titles, each with
  its title, then its position label and topic, linked to its deep link. Each trail sits
  under the frame it branches from, as a disclosure button ("Trail: The
  printing press, 1 frame"). Collapsed, and expanded its frames are
  indented under a rule. It opens with the trail the reader is on
  expanded, or the trails branching from their frame. The frame on the
  spine is marked with `aria-current="page"` and the accent. The reader's
  marks on a frame are said in words after its position, in the same
  words as the spine's marks (`marksText`).
- **A filter** at the top matches titles, position labels and topics, ignoring
  case. A frame stays when a trail under it matches, a trail whose title
  matches stays whole, and matched trails show open as plain labels.
  A status line says how many frames match.
- **A popover, not a dialog**, like the gear's settings and the bookmarks.
  Focus is not trapped: Tab leaves it, a click outside closes it, and Esc
  closes it and returns focus to its button. It opens focused on the
  current frame, scrolled to the middle of the list. Picking a frame goes
  there (into its trail if it is on one), closes the list and returns focus
  to the button, so the shortcuts still act.
- **Nested lists, not a treeview.** Each segment is a list labelled by its
  title, and each trail a list under a disclosure button. A treeview would
  make every entry an option to arrow through and announce as a tree, but
  these entries are links. The lists read correctly to a screen reader, and
  links still open in a new tab. The treeview's keys are added on top: ↑/↓
  move between the filter box, the entries and the disclosures in reading
  order, Home/End go to the ends outside the box, and →/← open and close
  a trail. The panel is `data-own-keys`, so the page's arrows stand down.
- **On a phone** (below 40rem) it is a sheet over the whole screen. Its
  title, close button and filter stay at the top while the list scrolls.

## Connections

Phase 1 of the connections design (sprint 017, korg 3439; the decisions are
Ken's, in the 2026-09-29 comment on korg 3399). The subjects touch each
other everywhere, in two ways: the same thing appears in two subjects (the
IBM 704, Project MAC, Bletchley Park), and an idea connects two frames
(softmax is the Boltzmann distribution; desktop publishing is the next
printing press). kloom has a layer for each. The map draws both (§The map).

- **Names.** A registry shared by every subject: `names/<id>.json` at the
  repository's top level, beside `subjects/` and never inside one
  (`$KLOOM_NAMES_DIR`, by default `names/` beside `$KLOOM_SUBJECTS_DIR`,
  so the service's content clone carries its own). Each file has `id` (the
  stem), `wikidata` (an item id, or `null` when there is none), `name`,
  optional `aliases`, `kind` (person, place, org, artifact, idea, event), a
  one-line `description`, and an optional `home` frame
  (`<subject>/<frame>`) chiefly about it. The Wikidata ID is the key that
  holds across repositories, so subjects kept apart (korg 3387) agree on
  who "Turing" is without sharing a file; two names may not share one.
  `engine/names.ts` checks a file.
- **Name marks.** A reading marks a name as a markdown link with the
  `kloom:` scheme: `[Alan Turing](kloom:e/alan-turing)`. Only the first
  mention in a frame is marked, the Wikipedia convention: a later mark
  renders as its words, and validation warns about it. `kloom:e/<id>` is
  the only `kloom:` link; any other fails validation and renders as its
  words. A mark renders as a button (`aria-haspopup="dialog"`), never a
  navigation link, with a dotted accent underline. `create-tools/names`
  marks first mentions from a spec, and looks up Wikidata IDs.
- **The name card.** Clicking a mark, or Enter or Space on it, opens a
  card beside it: the kind and description; the home frame, if any, as
  "Chiefly"; then "Appears in…", every frame that marks the name, grouped
  by subject with the reader's own subject first. The frame the reader is
  on is listed as "you are here", not linked; every other entry is a link
  that jumps. A popover, not a modal, like the contents: it takes focus,
  its keys are its own (`data-own-keys`), and Esc, a click outside or
  focus leaving it closes it, Esc returning focus to the mark. A mark on
  a name the registry lacks opens a card saying so.
- **Connections.** In `frame.json`: `connections: [{to:
"<subject>/<frame>", why}]`, to a frame in this subject or another. The
  `why` is required: a sentence on what connects them. A connection is
  stored on one frame and shown on both: backlinks are derived, never
  written. The narrative lists them under **Connections**, above Sources,
  each linked with the other frame's subject (when it is another), title,
  position and trail, and its _why_.
- **The graph index.** `engine/graph.ts` builds it from every served
  subject: frames, names, mentions and connections. It reads each subject
  lightly (`readGraphSubject`: titles, positions, connections and marked
  names; nothing rendered). Since sprint 032 it is built when the library
  is (§Serving), and each frame's links, the map's data and the counts are
  derived from it and stored, so no request builds it.
- **Detached, never a failure.** A connection whose target is not a frame
  shows as "Not found", and a home that is not a frame is left off the
  card. Subjects may be kept apart and change on their own, so a missing
  target must never stop a page. Serving validates marks for their form
  only, for the same reason. The gate is strict about the repository's
  own: it validates every subject against the registry, and
  `graphProblems` refuses a connection to no frame, to itself, or stored
  on both ends, a home that is no frame, and a mark on an unregistered
  name. Grow validates against the registry too, and may add names to it
  but not change them (§Grow).
- **Jumps.** Following a card's entry or a connection is a jump: it lands
  on the frame, past the start screen, on whichever spine holds it (into
  its trail if need be), in that subject's palette. A jump adds a browser
  history entry; stepping the spine still replaces the entry. Focus lands
  on the spine, where the frame is announced, after a jump and after Back.
- **The Back chip.** After a jump, "↩ Back to <frame> · <subject>" sits in
  the spine's HUD, left of the contents. Each history entry carries the
  jumps that led to it (SvelteKit's `page.state.back`, kept through the
  spine's `replaceState`), so the chip is simply the browser's Back:
  the two can never disagree, and Forward brings the chip back. Jumps
  stack; the chip names the latest and shows how many more wait (+1). R
  goes back too: the seventh character shortcut, remappable and scoped
  like the others (§Interaction).
- **Duplication across subjects stays** (Ken): each subject must read on
  its own, and a connection turns a retelling into the other angle.

## The map

Connections, phase 3 (sprint 019, korg 3441): the graph index drawn as a
picture you can move through. `engine/map.ts` decides what each view holds,
where its nodes go, which labels fit and where an arrow moves;
`engine/ui/MapOverlay.svelte` draws it. Its data comes from `GET /api/map`
(every served subject's frames, their connections and the names they mark,
about 340 KB), fetched when the map first opens and kept until a grow.

- **Where.** A full-screen modal (a native `<dialog>`): the page behind is
  inert, and Esc closes it and returns focus to what opened it. It opens
  from an icon button in the spine's HUD, right of the contents, and from
  M, the eighth character shortcut, remappable and scoped like the others
  (§Interaction), on the frame's neighbourhood. From the start screen,
  "Map of the library" opens the library, and a name card's "Show on the
  map" opens the name's view.
- **Views.** _Neighbourhood_ (a frame): the frame, its connections and the
  names it marks at one step. Two steps (the default) add the connections
  of those, and the frames that share the most telling names with it. A
  name in many frames says little about any one, so a frame is ranked by
  the sum, over the names it shares, of one over the other frames each is
  in, and only 8 are kept: sprint 018 measured a median of 22 frames one
  name away, and Richard Feynman's 63. Only the centre's names are drawn,
  so a view never holds more than about 35 nodes. _Library_: a node per
  subject, the lines thickened by the connections between each pair.
  _Subject_: its frames that have connections, and where they lead; the
  rest are counted, not drawn. _Name_: the name, with the frames that mark
  it around it (its card, as a graph). Moving the centre is a new view,
  and the map's own Back (or Backspace) steps back through them.
- **Deterministic and still.** The layout (d3-force, the one dependency
  the map adds) is seeded by the view and runs to rest before anything is
  drawn, so the same view lands the same way every time and nothing moves:
  there is no motion to reduce. The centre is pinned; the rest start on
  rings, grouped by subject, and a ring widens with its nodes.
- **Labels.** A frame is labelled by its topic, a name by its name and a
  subject by its title, always whole: a label over 22 characters takes two
  lines of about equal length, broken at a space (sprint 020; sprint 019
  cut headlines at 30 characters, mid-word). The headline is said after
  the topic in the details. Labels are placed greedily, most important
  first (the centre, then frames, then names), right of the node, else
  left, above or below, wherever a label hits no other label, no node and
  no edge of the map. A label with no room shows when its node is brought
  forward, or is a neighbour of the node brought forward. Every label sits
  on a plate of the map's surface, so no line runs through its words.
- **Emphasis** (sprint 020). At rest every line is dimmed toward the
  surface: connections (solid) and a name's mentions (dotted) alike. The
  node under the pointer, or with keyboard focus, is brought forward: its
  lines are drawn last in full ink, its neighbours are outlined and their
  labels ruled in their subject's colour, and every other node and line
  recedes. So a line that merely passes a label never reads as a link.
  Keyboard focus counts only when it is visible (`:focus-visible`), so a
  map opened by pointer opens at rest. The details keep saying the last
  node brought forward, with how many it is linked to on this map.
- **The details** have one height for every state, empty or full, so the
  graph above never resizes as the pointer moves: their lines are clipped
  to fit, and the list has them whole.
- **Subjects** wear a colour and a shape, in the order the app serves them.
  The subjects' own accents are all golds and reds, so the map takes its
  own surface (light or dark, after the palette it opens over) and a
  categorical palette validated against it. No four hues hold apart for
  every kind of colour vision on the dark surface, so colour is never the
  only cue: each subject has a shape (circle, square, diamond, triangle,
  hexagon, star), the legend names both, and the list says each frame's
  subject in words. A name is a hollow ring.
- **No text selection.** A double-click on a node goes to it, so the
  graph does not let its labels be selected (sprint 020). The details and
  the list still do: copying a title there is legitimate.
- **Keys.** Every node is a button, one of them in the tab order at a
  time. The arrows move to the neighbour that lies that way (a joined one
  first, the nearest of all when none is joined that way), Home returns to
  the centre, Space (a click) centres the map on the node, and Enter goes
  to a frame: a jump, with the Back chip (§Connections). The details under
  the map say the focused node, a connection's _why_ and a name's
  description, with Go and Centre buttons for the pointer.
- **Show as list.** A switch that shows the same view as lists: a frame's
  connections with their _why_, what is two steps away and through what,
  the frames sharing names and which, its names; or a subject's, a name's
  or the library's. On by default below 40rem, where a graph of 30 labelled
  nodes does not fit.
- **3D.** A second switch, beside Show as list, turns the whole library
  into a 3D graph (§The library in 3D). It is off whenever the map opens,
  and its own "Show on the 2D map" comes back here.

## The library in 3D

Sprint 023, korg 3449: every frame, every marked name and every connection
at once, as a force graph in WebGL that the reader turns, zooms and flies
through. It is for the pleasure of seeing the whole library. The 2D map
stays the everyday tool, and the way to read the graph.

- **Where.** The map's "3D" switch, so it opens from both places the map
  does: the spine's HUD (over a frame) and the start screen's "Map of the
  library". Show as list, or the switch again, returns to the 2D map; each
  frame's and name's details carry "Show on the 2D map", which opens the
  2D map centred there.
- **What is drawn.** `engine/library3d.ts` (`library3dOf`) reads the map's
  own data (`GET /api/map`), so there is no second fetch: 290 frames, 1,460
  names, 281 connections and 2,671 lines from frames to the names they
  mention (the library at sprint 023). A frame wears its subject's colour
  and a solid for its 2D shape (sphere, cube, octahedron, tetrahedron,
  hexagonal prism, icosahedron), sized by its links; a name is a small grey
  sphere. The pointer's label is the frame's topic, with its title, subject
  and position; or a name and its description.
- **The library.** Vasco Asturiano's `3d-force-graph` (1.80.1, MIT), on
  `three` (0.186, MIT, a direct dependency too, for the solids). **Loaded
  lazily**: the overlay imports the 3D component only when the switch is
  turned, and the component imports the graph library in turn, so nothing
  of three.js is in the page's bundle. Measured at sprint 023: the page's
  eager JavaScript grew by 4.5 KB (the random controls, the two shortcuts
  and the switch), and the 3D view's chunks are 1.55 MB (413 KB gzipped),
  fetched only when it opens.
- **Motion.** The layout runs 160 ticks before the first paint (about half
  a second), and the camera takes in the whole library, fitted to the
  frames at their middle depth (the library's own fit takes in the nearest
  points as well, which left the graph a small knot). Without reduced
  motion it then drifts on to rest for four seconds, the camera eases out
  to the whole of it, and it turns slowly until the reader takes hold of it
  or presses "Turn slowly" (WCAG 2.2.2); the links of the node under the
  pointer come forward with particles running along them. **Under reduced
  motion** it stops at first paint, never turns, has no particles and
  flies to a node without a transition: nothing moves that the reader did
  not move.
- **Accessibility, stated honestly.** A WebGL canvas is not something a
  keyboard or a screen reader can move through, so this view is decorative
  and says so. The canvas is `aria-hidden` and out of the tab order; what
  it shows is said in words under it (the counts, and a table by subject
  under "Counts by subject"), and every control is an ordinary button.
  Esc closes the map as always. It never traps focus, and the 2D map with
  Show as list is one switch away.
- **Its own surface.** It reads the map's surface and subject colours from
  the dialog, light or dark after the palette it opened over.
- **Out of scope:** VR and AR.

## Random

Sprint 023, korg 3437: two dice, for wandering. One die, left of the table
of contents in the spine's HUD, goes to a random frame in this subject; two
dice, left of Home, go to a random frame anywhere in the library. D and W
do the same, remappable and scoped like the other shortcuts (§Interaction).

- **Any frame a spine walks.** In the subject, the main spine's frames and
  every trail's (`walkedFrames`); anywhere, every frame the map's data
  holds (fetched once, as the map does). A frame on no spine is not
  reachable, and is never picked.
- **Never where you are.** The current frame is left out before the draw
  (`pickOther`), so every other frame is equally likely. Anywhere may land
  in the same subject: it is a draw over frames, not subjects, so a larger
  subject comes up more often.
- **A jump.** Both go through the page's jump (§Connections), so the Back
  chip and the browser's Back return from one, and focus lands on the
  spine, where the new frame is announced. An unsaved note asks first.

## Topics

Where a frame is named (sprint 020, korg 3446). A frame has three names:
its headline and accent (the voice), its position label (often a date) and
its topic (what it is about). The rule is one sentence: **where a frame
stands alone, the topic names it; where the reader walks their own
subject in order, the headline does, and the topic goes beside it.**

- **The map** labels frames by topic, and the details say the headline
  after it. Its view titles and list notes ("Around …", "Through …")
  use the topic.
- **The Back chip** says the topic of the frame it returns to: it is often
  in another subject, where the headline says nothing.
- **A name card's frames** and **a frame's Connections** are named by
  topic: both list frames from any subject.
- **The contents** keep the headline as each line's name, with the
  position label and topic after it, and the filter matches topics too.
- **Bookmarks** keep the headline stored with them (reader data is not
  rewritten), and a bookmark in the subject being read says its position
  and topic after it.
- **Unchanged:** the spine's scene, the reading pane's title and the
  screen reader's announcement of a step keep the headline. They are the
  frame itself, where its scene and reading say what it is about.
- **Validation.** Required, at most 40 characters (the backfill's longest
  was 39), no closing "." or "!", not the scene's accent word in capitals,
  and unique in its subject. Grow and `skills/author-subject` write one
  for every new frame. A frame read without one (a content clone behind
  the code) is named by its headline, so the graph never breaks on it.
- **The backfill** (222 frames) was written by hand for western-civ and by
  one agent per subject for the rest, reviewed and committed per subject.
  It is authored content, not grown, so it went through the sprint's own
  review rather than the grown-content path (korg 3442).

## Risks

- **Illustration quality** is the biggest one: Claude-drawn SVG varies. The
  POC hand-curates its frames to set the bar; the generating skill is written
  against them.
- **Accuracy**: every frame flags at least one key-source citation, and
  the grow skill must produce them.

## Who may write

Built in sprint 007 (korg 3384 decided it, 3388 built it). Operations are in
[deploying.md](deploying.md).

- **Reads are open; writes need a reader.** Every request that is not a
  read (ask, keep and grow are all POSTs) needs a `Reader`
  (`src/lib/server/reader.ts`): a login, a name and how it was established.
  Without one, the hook answers 401 before any route runs.
- **Two loopback doors.** The service binds 127.0.0.1 only, on two ports
  (`serve.js`). The **tailnet door** is fronted by `tailscale serve`, the one
  network ingress, and its reader is the `Tailscale-User-Login` header that
  serve injects. Serve strips a client-supplied copy, and a tagged node gets
  none, so on this door no header means no writes. The **ssh door** is for
  ssh forwards (kwork's demos). Reaching it took an ssh login on the host,
  so its reader is the host's own user, and identity headers there are
  ignored.
- **Why two ports.** Both doors arrive from 127.0.0.1, so the app cannot
  tell them apart by address, and a header sent straight to the loopback
  port is not stripped by anyone. `serve.js` marks each request with its
  door and a key made at start, overwriting any mark a client sent. The app
  trusts no mark without that key. With no mark, only `vite dev` is trusted.
  A plain `node build`, or `vite preview`, reads but never writes.
- **The reader goes on the grow job** (`by`) and becomes the commit's
  author. Keep does not record one yet. Reader data keys every row by the
  reader (§Reader data), and its routes refuse a request with none, reads
  included: a reader's places are nobody else's to read.

## The content clone

Built in sprint 007 (korg 3412). A service never grows into the checkout it
was built from or developed in.

- **Its own clone, on a grow branch.** The service reads subjects from, and
  grows into, a clone under its state directory
  (`~/.local/share/kloom/content`), checked out on `grow/<host>`
  (`$KLOOM_GROW_BRANCH`). A grow commits there and pushes the branch. Content
  comes back to main by an ordinary PR, reviewed like any other change.
  Unset, as in dev, grow commits wherever the subjects are and pushes
  nothing.
- **One long-lived branch, not one per job.** Jobs build on each other: the
  next one reads the subject the last one grew. The branch is the service's
  own, so nobody else pushes to it. Review edits go into the PR's merge, or
  onto main afterwards.
- **Picking up main at start** (`syncContent`, `src/lib/server/content.ts`).
  A deploy is a restart, so this runs on every deploy.
  - If the branch is behind main (a merge-commit merge), it fast-forwards.
  - If it is ahead (grown work waiting for its PR), it is left alone.
  - If the grown work reached main another way (a squash or rebase merge),
    main has some commit holding the grown paths exactly as the branch had
    them, even if main edited them since. The branch is reset to main then,
    or only its unmerged tail is rebased onto main.
  - Anything else is rebased onto main. A rebase that conflicts is
    abandoned, and the clone keeps serving as it was ("diverged" in the
    journal) until a person sorts it out.
  - A clone with uncommitted changes is left alone.
  - The branch is pushed after every sync, with a lease after a rewrite.
- **A grow refuses a clone that is off its branch**, and a push that fails
  leaves the commit in place: the job still succeeds, the AI pane says "not
  yet pushed", and the next push takes it.
- **Deploys replace the app, never the clone.** `just deploy` copies the
  build to `~/.local/share/kloom/app` and restarts the unit. The push uses
  the host user's existing GitHub credential, since the service already runs
  as that user; no new credential was minted.

## Serving

Built in sprint 032 (korg 3460, decided 2026-09-30). The files stay the
source of truth. Agents write them, git is review, history and undo, and
grow still commits files. What the app serves from is a compiled SQLite
file, `content.db`, derived from them and rebuildable at any time
(`engine/content-db.ts`).

- **What it holds.**
  - Each subject's head: title, palettes, segments, spine order, trails,
    and every frame's small half (id, topic, position, scene, `asOf`).
  - Every frame's body: the rendered reading (already sanitised), the
    inlined drawing, citations and Sources, and the reading as authored,
    which ask gives the model.
  - The names, their mentions and the connections, with each frame's links
    derived from them: its connections both ways, and the cards of the
    names its reading marks.
  - The map's data, the library's counts and each subject's start look.
  - An FTS5 index over every reading's text and topic, for a later search.
  - The schema version, the content's commit, the build time and what
    compiled it.

  Media stay files beside the subjects, named in the `media` table, and are
  served from disk as before. Reader data is a separate file (`reader.db`,
  §Reader data): `content.db` can be replaced, and reader data cannot.

- **The compiler** (`compileContent`, `just build-content`).
  - It validates every subject it builds, as the loader always did, so an
    invalid subject never compiles. A strict build (the gate, the recipe)
    fails with every problem named. The app's own builds keep serving such
    a subject as it was last built, and say why in the journal.
  - It is incremental. A subject whose files (path, size, modified time)
    are unchanged since the last build keeps its rows. Only what spans
    subjects is derived again: names, links, map and counts. One subject
    rebuilds in about 0.35 s, and the whole library in about 1.5 s
    (6.5 s at 5×).
  - A build by another compiler starts afresh, so new rendering code
    rebuilds everything. In a checkout the compiler is a hash of the
    engine's source. In a deployed app, which has no engine source, it is
    the build's commit.
  - It builds into a temporary file and renames it over the old one, so a
    reader never sees a half-built library. A server that finds a new file
    opens it, so a build made by hand is picked up too.
- **Keeping it current** (`src/lib/server/subject.ts`).
  - The first read builds it, or finds it current. A service builds it at
    start, after picking up main (§The content clone), and so on every
    deploy.
  - A grow job writes under the content gate, and the library is rebuilt
    before the gate opens. Readers wait at the gate, so grown frames show
    at once, as they always have.
  - In the dev server, Vite's own watcher reports a change under `subjects/`
    or `names/` (`vite.config.ts`), and the next read rebuilds what changed.
    The app keeps no watcher of its own: one over every frame directory
    cost 120 MB at 5×. A hand edit in a service's content clone shows after
    a restart.
- **The page and the frames.**
  - The page carries the subject's head, and the bodies of the frame it
    opens on and two either side.
  - The shell asks for the bodies of the frame under the cursor, two either
    side of it, and the narrative's frame (`onneed`). The page fetches the
    ones it lacks from `/api/frame/<subject>/<frame>`, tagged with the build
    (a 304 when unchanged), and keeps them for that subject and build. A new
    build, as after a grow, starts the cache afresh.
  - Until a frame's body arrives, the scene shows its head without the
    drawing, and the reading says "Fetching the reading…". Annotations wait
    for the reading rather than calling themselves detached.
  - The contents, map, marks, random jumps and the start screen use heads,
    the map's data and the start looks, never bodies.
- **Compression.** HTML, JSON, SVG, CSS and JS responses over 1 KB go as
  Brotli or gzip, as the client accepts (`src/lib/server/compress.ts`). The
  map and the counts are compressed once per build. Ask's NDJSON stream is
  never compressed, so it keeps streaming.
- **Sized for 5×** (`just bench`: the library copied five times, compiled
  and served by a production build). The targets, all met in sprint 032:
  - a first page of 300 KB or less, compressed;
  - a frame step of 100 ms or less on the LAN;
  - the map and counts in 20 ms or less;
  - a full compile well under a minute.

## Several subjects

Built in sprint 006 (korg 3396). One running app serves every subject.

- **A route per subject.** `/<subject>` serves `subjects/<subject>/`
  (`$KLOOM_SUBJECTS_DIR`). A subject is a directory whose name is a plain id
  (`[a-z0-9][a-z0-9-]*`) and that holds a readable `subject.json`. An id is
  checked against that listing, not just the pattern, so no request can
  name a path. An unknown one is a 404. `/` redirects to `$KLOOM_SUBJECT`
  (default `western-civ`), or to the first subject if that one is gone.
- **The chooser is the start screen** (sprint 013, korg 3424). A subject
  list (§Start screen) selects any served subject, and Begin opens the
  selection, already begun because the reader chose it there. The page is
  keyed by subject, so opening another one starts its shell afresh. A link
  to a bare `/<subject>` from outside still opens on its start screen.
- **Every API names its subject.** Ask, keep and grow take `subject` in the
  body (grow's job list takes `?subject=`), and media is served at
  `/media/<subject>/…`. Keep refuses an answer that was asked under
  another subject. Kept answers and grow jobs were already filed under
  `<dataDir>/<subject>/`, and a grow job commits to its own subject's
  directory.
- **Settings stay global.** Palette mode, narrative following and the
  models are one reader's choices about reading, not about a subject. None
  is clearly per-subject, so none is scoped.
- The engine still never names a subject: the shell passes `subject.id`
  through, and the page resolves the chooser's links.
- **Deep links** (sprint 009, korg 3414). `/<subject>/<frame>` opens that
  frame, past the start screen, on whichever spine holds it: every frame
  sits on exactly one, so the frame id alone says whether it is on a trail.
  As the reader moves, the URL follows (`replaceState`, so moving adds no
  history), and a refresh keeps the place. A link to a frame the subject no
  longer has, such as a stale bookmark, redirects to `/<subject>`.

## The second subject

Built in sprint 006 (korg 3395): `subjects/ai`, the History and Current
State of AI, with 41 main-spine frames and four trails. It was the Cutler
rule's test, and it is described in its sprint record.

- **The first mixed spine.** Its segments run `category` (myths and
  philosophers), then `date` (1843–2012), then `technology` (from
  embeddings to compute), then `category` (open questions). The engine
  needed nothing new for it: the HUD shows each segment's own labels, and
  the timeline marks segment boundaries with taller ticks and branch
  points with rings. It held 41 stops at phone width.
- **Its own look.** Three pairs of dark and light palettes, each the
  other's counterpart: blueprint and drafting, terminal and printout,
  neural and whitepaper. They follow the eras loosely, and they alternate
  within a segment where western-civ's stay in one.
- **Authored the way the framework will author.** A plan comes first
  (`create-tools/subject-plan/ai.json`). Frames were written by following
  `skills/grow/SKILL.md`, by several authors at once, and committed
  segment by segment. Every place the skill assumed western-civ was
  generalised in the skill (the record lists them).

## Reader data

Built in sprint 009 (korg 3413, 3414). What one reader does while reading
is not subject content. Content is files in git and gets reviewed. Reader
data belongs to one person, is written often, is never reviewed, and always
has an author. So it lives in a database, not in the repo.

- **A store behind an interface.** `ReaderStore` (`engine/reader-data.ts`)
  is written in engine terms, with methods per kind of record. Its one
  adapter is SQLite (`src/lib/server/sqlite-reader-store.ts`): a single file,
  `<dataDir>/reader.db`, in WAL mode. The methods are async although SQLite
  answers at once, so a Postgres adapter (kubsdb) can be added later
  without touching callers. It is not built.
- **Every row carries a reader and a subject.** The reader is the
  request's `Reader.login` (§Who may write): the tailnet login, or the
  host's `user@host` for the ssh door and the dev server. So there is never
  a row with no author, and sharing notes later has the authorship it
  needs. A request with no reader keeps nothing and is offered nothing:
  the bookmark controls and the resume offer are absent.
- **`node:sqlite`, not better-sqlite3.** It is built into Node 22.13 and
  later, which is already the engines floor, and it prints no experimental
  warning on the Node 24 that kai runs. So the store adds no dependency and
  no native build, and `just deploy`'s `npm ci` is unchanged.
  better-sqlite3 would bring a compiled addon, rebuilt for every Node
  upgrade, for nothing this store needs.
- **Migrations** are a list of SQL scripts in the adapter. `PRAGMA
user_version` counts how many a file has had, and opening it runs the
  rest, each in a transaction. A shipped entry is never edited; a change is
  a new entry. A file from a newer app is refused rather than guessed at.
- **Frames only, never trails.** A record names a subject and a frame, and
  the frame says which spine it is on (§Several subjects, deep links). Each
  record also keeps the frame's title when it was written, so a list that
  spans subjects can name a frame without loading another subject. The
  current subject's live titles replace it where they can.
- **Last visited.** One place per reader per subject, written 800ms after
  the reader stops moving. The last place overall is the newest of them.
  The start screen offers the selected subject's place under Begin as
  _Continue where you were_, and never forces it. The list marks the
  subject of the newest place _Last read_ (sprint 013; before it, a second
  offer named the other subject). The subject behind the start screen gets
  its offer too, after Home as much as on arrival (Ken, sprint 016, korg
  3432): Begin starts that subject from its first frame, so _Continue_ is
  the way back and the two never mean the same thing. The page keeps each
  subject's place as a live mirror of the store. The load fills it, and each
  move updates it at once, before the debounced write, so the offer never
  names where the reader was at page load. A later load keeps whichever copy
  is newer (`newerPlaces`). Begin keeps the focus.
- **Bookmarks.** A toggle in the spine's HUD (`aria-pressed`, "Bookmark
  this frame") and the B key mark the frame on the spine. A role="status"
  line says "Bookmarked: …" or "Bookmark removed: …", so a key press is
  heard. On the timeline, a bookmarked frame's tick carries a small flag
  under the line, where a branch ring sits above it. It is not shape alone:
  the tick's title, the slider's `aria-valuetext` and the spine
  announcement all say "bookmarked". The jump list beside the toggle is a
  disclosure built like the settings pop-up (`data-own-keys`, Esc returns
  to its button, and the wheel over it scrolls the list instead of stepping
  the spine). It lists every bookmark across subjects, newest first. One in
  this subject moves the shell, and one elsewhere is a deep link. Each has
  a named remove button. Writes are optimistic and roll back if the server
  refuses them.
- **Routes** (`src/routes/api/reader/`). `POST place`, `GET`/`POST`/`DELETE
bookmarks`, `GET`/`POST`/`PATCH`/`DELETE notes`, `GET`/`POST my-notes`,
  `GET`/`DELETE kept`, `GET export` and `POST import`. A place, bookmark or note must name a served subject
  (404) and a frame that subject has on disk (400).
- **Export and import.** The export is a versioned JSON file
  (`kloom: "reader-data"`, `version: 3`) of every place, bookmark, note
  (annotations included) and kept answer, and it downloads from the jump
  list's _Export my reading data_. A version 1 file (sprint 009's) still
  imports, as one with no notes or kept answers, and a version 2 file
  (sprint 011's) as one whose notes have no anchors. Import takes
  that file as the body of `POST /api/reader/import`. It files the records
  under whoever imports them, and where both hold a record, the newer one
  wins. One bad record refuses the whole file. There is no import button
  yet: it is for backup and for moving between hosts, not an everyday
  action.
- **On it since sprint 011:** notes (§Notes) and kept answers (§Kept
  answers), each with its own table, added by the second migration. The
  third (sprint 012) gave a note an `anchor` column, which makes it an
  annotation (§Annotations), and the fourth (sprint 034) an `unseen` flag,
  set when an agent answers it (§My notes).
- **The adapter loads under plain Node.** `sqlite-reader-store.ts` imports
  only `node:` modules and types, so Node's type stripping can load it
  outside the app. The review-notes skill's script does that (§Notes), and so
  reaches the store through its adapter, never around it. `reader-store.ts`
  holds the app's shared instance. A test runs the script, so an adapter
  that stops loading this way fails the gate.

## Marks

The reader's own layer on the spine (sprint 011). The content's mark, a ring
for a trail branching from a frame, sits **above** the line. The reader's
marks sit **below** it, each kind in a fixed row and shape, whether or not
the others are there:

1. a **bookmark**: a small filled flag;
2. **kept answers**: a filled dot;
3. **notes**: two short lines, like ruled paper.

A mark is never shape alone. `marksText` (`engine/marks.ts`) says the same
facts in words ("bookmarked", "2 kept answers", "1 note"), and the tick's
title, the slider's `aria-valuetext` and the spine announcement all use it.

## Notes

Built in sprint 011 (korg 3409). A note is plain text a reader writes on a
frame, kept per reader in the reader store. It is never rendered as markup.

- **The scene becomes the editor.** "Add a note" (on the Notes tab) or N
  (in the spine, narrative or notes) replaces the scene with a text box, on
  the frame in the reading pane. The HUD and the timeline stay, and so does
  the right-hand pane: the reader can still scroll the narrative, or read
  their other notes on the Notes tab. Saving or cancelling brings the
  picture back and returns focus to where the editor was opened from. Ctrl (or Cmd) with
  Enter saves; Esc cancels. The editor is marked `data-own-keys`, so every
  key typed there stays there.
- **The Notes tab** lists the frame's notes, oldest first, each with its
  date, an Edit and a Delete button (named with the note's opening words),
  and its review state. Edit opens the note in the editor. Delete asks
  first. The list says which note is in the editor.
- **Unsaved changes are guarded.** With changes not saved, moving along the
  spine (a key, a click on the timeline, the wheel, a bookmark jump),
  entering or leaving a trail, or opening another note asks "Discard
  them?". The answer No stays put. Leaving the subject asks the same, and a
  reload or closing the tab gets the browser's own question
  (`beforeNavigate`). A clean editor closes without asking.
- **"Agent review".** A box in the editor flags the note for an agent. The
  **review-notes skill** (`skills/review-notes/SKILL.md`) finds every
  flagged note with its reader, subject, frame and text
  (`review-notes.mjs list`), deals with it, and marks it handled with what
  it did (`handle`). The reader sees that response under the note. Ticking
  the box again flags it afresh and clears the old response. Unticking a
  flagged note unflags it. A handled note stays handled.
- **An edit keeps its frame.** A note belongs to the frame it was written
  on. It also keeps the frame's title as its label, like a bookmark.

## Annotations

Built in sprint 012 (korg 3415). An annotation is a note on some words of a
frame's narrative: a note (§Notes) that also records the words it is on, in
an `anchor`. Everything else is a note's: the same row in the reader store,
the same editor, the Notes tab, the "Agent review" flag and the review-notes
skill, which quotes the words.

- **The anchor survives edits.** Grow and later sprints change readings, so
  an annotation never stores character offsets alone. It stores the W3C Web
  Annotation text-quote selector: the quoted words (`exact`), up to 32
  characters on each side (`prefix`, `suffix`), and where they were
  (`start`) as a tie-breaker (`engine/anchor.ts`). It works on the
  reading's text as its text nodes give it (inlined charts left out), with
  runs of whitespace collapsed, so a re-wrapped paragraph reads the same.
- **Found again, or detached; never silently wrong.** Each time the reading
  is shown, the annotation looks for its words. They must be there exactly,
  give or take whitespace. Where they appear more than once, the place whose
  context agrees most wins, then the nearest. A place is taken only when at
  least 8 characters of context still agree, or the words are 24 characters
  or more and appear once. So a paragraph inserted above, or a reworded
  neighbouring sentence, leaves it in place, and a deleted or reworded quote
  detaches it. So does a short quote whose surroundings all changed, rather
  than landing on a "the" somewhere else. There is no fuzzy match: changed
  words are not the words the reader wrote about. A detached annotation
  keeps its words and its note. The reading says how many on this frame
  are detached, the Notes tab marks each one, and its editor says so.
- **Making one.** A (or the Annotate button in the narrative's toolbar)
  annotates the words selected in the reading. The button does not take
  focus on a mouse press, so the selection survives the click. With nothing
  selected, it starts **choosing words with the keyboard**: the first
  sentence in view is selected, ↑/↓ move by sentence (sentences are found
  per paragraph, heading or list item, with `Intl.Segmenter`), ←/→ move the
  start by a word, Shift with ←/→ the end, Enter annotates and Esc (or
  leaving the reading) cancels. The choice is the page's real selection, so
  it looks like one. A status line says the words each time they change, and
  the toolbar shows the keys while choosing. A again annotates the choice,
  as Enter does. Then the editor opens in the scene's place, as for a note,
  headed "New annotation" and quoting the words.
- **Seeing them.** Each annotation's words are wrapped in `<mark>`s, which
  assistive technology announces as highlighted, followed by a small ✎
  button named "Your annotation: <its opening words>". The buttons are in
  the tab order, which is how the keyboard moves between annotations.
  The button, or a click on the highlight (not while selecting), opens the
  annotation in the editor. Closing it returns focus to the button. The
  highlights are drawn onto the rendered reading after it is shown, and
  redrawn when it or the annotations change. Only the reading's own
  elements are touched, never the nodes Svelte placed.
- **On the Notes tab** an annotation is listed with its notes, oldest first,
  quoting its words above its text, with **Show in reading** (which brings
  the narrative forward and focuses its button) when it is not detached.
  It counts as a note on the spine's marks and the tab.
- **An edit keeps its anchor**, as it keeps its frame. The words an
  annotation is on are fixed when it is made.

## My notes

Built in sprint 034 (korg 3481). Before it, a note could only be found on
its own frame's Notes tab, so seeing which were flagged or answered meant
visiting every frame, and an annotation left detached by a fix had nowhere
to be cleared in bulk.

- **One list, every subject.** A control in the spine's HUD, beside the
  bookmarks, and O (remappable and scoped like the other shortcuts,
  §Interaction) open a modal dialog listing every note and annotation the
  reader has, grouped by subject, the last written first.
  `GET /api/reader/my-notes` sends them, each with its subject's title and
  its frame's topic and position as the library has them now; a note
  whose subject or frame is gone stays listed, to be cleared, with nowhere
  to go. The list is fetched each time the dialog opens.
- **Each entry says its state in words**: Note or Annotation, then _Agent
  review (pending)_, _Answered_ (with the agent's response under the note),
  _Detached_, _No longer in the library_, or none. An annotation quotes its
  words. The entry's link is named by the frame's topic and described by
  its state and text, so a screen reader hears both.
- **Detached is worked out as the reading pane does.** Each annotated
  frame's reading is fetched (`/api/frame`, as any jump would), parsed
  inert, and its annotations' words looked for with the same
  `readingText` and `findQuote` (`engine/my-notes.ts`, `detachedIn`).
  Until every frame is read, the status line says so and Clear detached
  waits.
- **Filters**: All, Agent review, Answered and Detached, a radio group
  with a count on each. Answered and Detached can both hold one note.
- **Per entry**: **Go to** (the link) jumps to the frame through the shared
  jump path, so the Back chip and the browser's Back return, and opens the
  Notes tab with focus on that note. **Clear** deletes it after a confirm.
  The flag button does what the editor's box does, without touching the
  text (`PATCH /api/reader/notes`): _Flag for agent review_, _Withdraw agent
  review_, or, on an answered note, _Ask the agent again_, which flags it
  afresh and clears the answer.
- **In bulk**: _Clear answered_ and _Clear detached_ delete every note the
  filter would show, after a confirm that says how many
  (`DELETE /api/reader/notes` with `ids`). They delete what was shown,
  never what the server has since.
- **Keys in the list**: ↑/↓ between notes, Home/End to the ends, Enter
  goes, Delete clears (with the confirm), Esc closes. The dialog is
  `data-own-keys`, so the page's own keys stand down in it. Closing returns
  focus where it was when the dialog opened.
- **New answers are counted.** The review-notes skill's `handle` sets the
  note's `unseen` flag. The control shows how many are waiting, a badge with
  the number and "My notes, 2 new answers" as its name. Opening the dialog
  marks the answers in it seen (`POST /api/reader/my-notes`), and so does
  the Notes tab showing one; the dialog still marks them _Answered (new)_
  while it stays open. Flagging a note afresh clears its flag. Answers given
  before sprint 034 count as unseen: nothing recorded that they were seen.
- **Works at 390 px**: the dialog takes the width less a margin, and its
  filters, entries and bulk buttons wrap.

## Kept answers

Built in sprint 011 (korg 3390). An answer the reader kept is theirs to
read again, not only grow's to consume.

- **In the reader store**, one row per reader and answer, holding the
  kept-answer format (§Ask) whole, so grow reads exactly what it read
  before. A kept answer belongs to whoever kept it. Grow reads one only for
  the reader who queued the job.
- **Moved in once.** At server start, any `<dataDir>/<subject>/kept/*.json`
  from before sprint 011 moves in under `$KLOOM_KEPT_OWNER`, or the host's
  own reader (`user@host`), because the files never said who kept them.
  Each moved file goes to `kept-migrated/` beside it. A file that is not a
  valid kept answer stays and is logged. A finished grow job that used one
  says what it grew into, and that comes too.
- **Seen again, on the spine and in the reading.** A frame with kept answers
  gets the dot under the line (§Marks). The reading gets a **Q&A** section
  after its trails: a native `<details>`, closed by default, labelled with
  the count. The page load brings only the counts per frame. The answers
  are fetched (`GET /api/reader/kept?subject=&frame=`) when the section is
  first opened. Each shows its question and its answer, rendered as ask
  renders one (no images), and the frame citations it drew on. They are
  numbered by the `[n]` the answer marks them with, recovered by pairing the
  answer's first-use order with the stored citations (`keptReferences`).
  When the frame's list no longer pairs up, they are listed unnumbered.
- **After grow.** A kept answer that grow turned into content **stays** in
  the Q&A, marked "Grown into" with a link to each frame it made. The
  answer is still what the reader asked, and the link shows where it went.
- **Remove** (with a question first) forgets a kept answer.

## The third subject

Built in sprint 014 (korg 3397): `subjects/feynman`, Richard Feynman, the
first subject built on a person, and the first written by following
`skills/author-subject/SKILL.md`, which sprint 014 wrote down from sprint
006's method. It is described in its sprint record.

- **A life on dated segments, the depth in trails.** 34 main-spine frames in
  seven `date` segments from Far Rockaway to the last years, and a closing
  `category` segment for the legend and the legacy. Five trails of five or
  six frames: two labelled by idea (`technology`: the path integral, the
  diagrams) and three by date (Los Alamos, computing, the Challenger
  commission). The engine needed nothing new.
- **The voice is "he"**, where the other subjects speak as "we". The grow
  skill now says the voice is the subject's.
- **His stories are his telling.** Frames that rest on the memoirs say so,
  and put documented accounts beside them; where the records correct him
  (the wobbling plate, the IBM throughput at Los Alamos), the reading says
  so.
- **Its own look.** Three dark/light pairs: lamplight and manila for the
  life, chalkboard and graphpaper for the physics and teaching, blueprint
  and vellum for Los Alamos, Challenger and the machines. The lowest
  contrast is 5.4:1.

## The fourth subject

Built in sprint 015 (korg 3398): `subjects/computing`, the History of
Computing, the second subject written by following
`skills/author-subject/SKILL.md`. It is described in its sprint record.

- **Dates, then technologies.** 37 main-spine frames: six `date` segments
  from counting boards to the Altair, three `technology` segments
  (networks, shared software, computing everywhere), and a closing
  `category` segment. Six trails of five frames, five by date and one, the
  internet stack, by layer. The engine needed nothing new.
- **It complements the AI subject.** Where both touch a story (Babbage and
  Lovelace, Turing, the Manchester machines, Lisp machines, GPUs), this
  subject's frame tells the machine and gives the other side a sentence.
- **Its own look.** Three dark/light pairs by era: walnut and cardstock for
  gears and cards, console and teletype for valves and mainframes, circuit
  and schematic from the microprocessor on. The lowest contrast is 5.6:1.

## The fifth subject

Built in sprint 021 (korg 3428): `subjects/physics`, the History of Physics,
the third subject written by following `skills/author-subject/SKILL.md` and
the first written with names, connections and topics from the start. It is
described in its sprint record.

- **Dates, then categories.** 45 main-spine frames: five `date` segments
  from Aristotle to Perrin's atoms (1905–08), then `category` segments for
  relativity, the quantum, the nucleus, particles and the cosmos, and a
  closing one on open questions. Four trails of five or six frames, all by
  date: the field (Ørsted to Hertz), heat and information (Maxwell's demon
  to reversible computing), the quantum revolution (1905–1927) and the
  Standard Model. The engine needed nothing new.
- **The bridge.** Physics sits between western-civ and the tech cluster
  (ai, computing, feynman): 174 connections are stored on its frames, 108
  of them into other subjects, and 63 of its 68 frames have one.
  Western-civ's Faraday and Maxwell frames tell those two stories; the
  physics field trail tells the physics around them and connects to both.
- **Its own look.** Four dark/light pairs by era: bronze and papyrus to
  Newton, gaslight and foolscap for 1700–1910, cloudchamber and photoplate
  for the quantum, the nucleus and particles, deepfield and starchart for
  relativity and the cosmos. The lowest contrast is 5.8:1.

## The sixth subject

Built in sprint 024 (korg 3429): `subjects/mathematics`, the History of
Mathematics, the second subject written with names and connections from
the start, and the first of three runs of `skills/author-subject/SKILL.md`
whose findings go to korg 3461. It is described in its sprint record.

- **Dates, then categories.** 49 main-spine frames: four `date` segments
  from the Ishango bone to Euler's bridges of Königsberg (1736), then
  `category` segments for algebra, analysis, geometry, probability, logic
  and foundations, and a closing one on mathematics now. Three date
  trails: Fermat's Last Theorem (on `diophantus`), the primes (on
  `euclid-elements`) and infinity (on `cantor`). The engine needed nothing
  new.
- **Mathematics done, not described.** Every reading carries one piece of
  real mathematics (a proof sketched, a worked example, a construction the
  plate draws), and the plates are those proofs and constructions.
- **Links.** 138 connections are stored on its frames, 68 of them into
  other subjects (26 physics, 18 ai, 11 computing, 9 western-civ, 4
  feynman). Shared stories are owned once: physics' `archimedes` keeps the
  lever and _The Method_, ai's `turing-machine` keeps Turing's paper, and
  the mathematics frames take their other angle and connect to them.
- **Its own look.** Four dark/light pairs: clay and vellum to 1500, oakgall
  and quarto for the printed treatise to 1850, blackboard and graphpaper
  for algebra, analysis and geometry, terminal and printout for
  probability, logic and machines. The lowest contrast is 5.5:1.

## The seventh subject

Built in sprint 025 (korg 3430): `subjects/chemistry`, the History of
Chemistry, the second of three runs of `skills/author-subject/SKILL.md`
whose findings go to korg 3461. It is described in its sprint record.

- **Dates, then categories.** 53 main-spine frames: four `date` segments
  from the first smelted copper (c. 5000 BC) to the Curies' radium
  (1898), then `category` segments for industry, the chemical bond,
  materials, the chemistry of life, and chemistry now. Three date trails:
  alchemy's last century (on `boyle`), finding the elements (on
  `periodic-table`) and from dyes to drugs (on `mauveine`). The engine
  needed nothing new.
- **Chemistry done, not described.** Every reading does one piece of
  chemistry: an equation with its masses worked, an isotope pattern, a
  recipe read as a ratio, a law checked against the original numbers.
- **Links.** 108 connections are stored on its frames, 58 of them into
  other subjects (22 physics, 14 western-civ, 7 computing, 6 mathematics,
  5 feynman, 4 ai); its links to the making subject (korg 3431) wait on
  that subject and are listed there.
- **Its own look.** Four dark/light pairs: furnace and alum to 1600,
  retort and filter for the laboratory to 1900, coaltar and enamel for
  industry, dyes, drugs and materials, helix and agar for the bond, life
  and the present. The lowest contrast is 5.6:1.

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

Sprint 013 (korg 3424) made it a place to come back to, and made it scale
past two subjects:

- **Home.** A house icon to the left of the settings gear opens the start
  screen over the subject, with that subject selected. The shell is not
  remounted: it goes inert behind the dialog, so the reader's place, the
  narrative and any unsaved note all survive. Esc returns to exactly where
  the reader was, and so does _Continue where you were_. Begin starts the
  subject from its first frame (sprint 016, korg 3432, §Reader data). Focus
  goes back to Home, and the URL moves only if the reader does. Opening another subject from there is a navigation, so an unsaved
  note meets the usual guard (§Notes), and a cancelled one leaves the start
  screen as it was. The gear and Home share `engine/ui/IconButton.svelte`.
  Home's icon and the four runners-up (loom, shuttle, return, title card)
  are in `engine/ui/icons/`. They are kloom's UI, not a subject's.
- **The subject list** is a listbox (`aria-activedescendant`, selection
  follows the arrows, Home/End, Enter begins, a click selects and a
  double-click begins). It is in the dialog before the title, so Shift+Tab
  from Begin reaches it. On a wide screen it stands down the left of the
  loom. Below 60rem it lies flat above the title, and ←/→ work as well as
  ↑/↓. With one subject served there is no list.
- **The selection's look.** The title, the _Continue_ offer, the palette
  (the selected subject's first frame's, in the reader's palette mode) and
  a ring of its own illustrations around the loom all follow the
  selection. The ring is a sample of about ten (`engine/start.ts`, spread
  evenly along the main spine, first frame first). The drawings sit just
  outside the dial's rim, turn with it slowly and fade in one after
  another, with their labels hidden at that size. They are the loader's
  already-sanitised markup, so there is no new sanitiser path. This
  subject's look is computed on the page. Another's comes from
  `GET /api/start/<subject>`, a read open like the page, and is kept once
  fetched. Reduced motion stops the turning and the fade.
- **The subtitle** (sprint 026, korg 3465). A subject's `subtitle` stands
  under its title on the start screen in place of kloom's tagline ("A
  timeline you can read, question and grow"), which a subject without one
  keeps. It is also said under the title in the subject list and in About's
  table of subjects. Labels that name a subject in passing (the back chip,
  a name card, the map) keep the title alone.

- **The corner** (sprint 022, korg 3456). The start screen's upper right
  holds two icon buttons in the shell's look: _About_, then the settings
  gear rightmost, as in the shell. The gear is the shell's own pop-up
  (`engine/ui/Settings.svelte` over the same settings), so palette mode,
  layout, models and keys can be set before a subject is begun. Both are
  last in the dialog's tab order, after _Map of the library_. Esc in either
  pop-up closes it and returns focus to its button without leaving the start
  screen; a second Esc begins as before. Both hang from the corner's right
  edge, so neither leaves a 390px screen.

## About

Sprint 022 (korg 3455, 3456). Ken asked: _if kloom were a book, how many
pages would it be?_ The About panel answers, from the start screen's corner.

- **What counts** (Ken, 2026-09-30): the narratives only, at **275 words a
  page**. A reading counts as the reader sees it, headings, tables and
  captions included. Excluded: markup, a picture's alt text and credit, a
  chart's labels, citations and the Sources list, the scene (headline,
  accent, metadata), and everything of the reader's own (notes, kept
  answers, annotations). A word is a whitespace-separated token with a
  letter or digit in it.
- **Counted when the library is built.** `engine/stats.ts` renders each
  reading with the same markdown renderer the reader gets and strips it to
  text. Since sprint 032 that happens per subject when the library is built
  (§Serving), and `GET /api/stats` (a read open like the page, fetched when
  the panel first opens) sends the stored sum. Grown content counts once
  its build lands, which is before the grow's gate opens. `just stats`
  still counts straight from the files.
- **What else it shows:** per subject, frames (a trail's included), trails,
  words and pages as a table; for the library, images, charts, tables,
  names in the registry, connections (each stored on one end, so counted
  once) and citations. Then what kloom is, the repo and the inspiration,
  credits, and the build: the commit's short hash and date, stamped by
  `vite.config.ts` at build time.
- **A note on accuracy** (sprint 031, korg 3477; Ken's wording, edited for
  flow) closes the panel: skills and review aim at accuracy, both views are
  given where sources disagree, people and agents both make mistakes, and it
  is a hobby, not scholarship. It says how to report an error: annotate the
  words with _Agent review_ ticked, or the repo's **Content feedback** issue
  form (`.github/ISSUE_TEMPLATE/content-feedback.yml`: subject, frame, the
  quoted text, what is wrong, a source; labelled `content-feedback`). Blank
  issues stay open for code bugs. It is worded for a reader who is not Ken,
  since the public reader site will show the same panel.
- **`just stats`** prints the same counts as a Markdown table, through the
  same engine code, for sprint records.

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
- Every path keeps `pathLength="1"`, and nothing the illustration
  sanitiser rejects (§Illustration sanitiser).

## Illustration sanitiser

Built in sprint 005 (korg 3365). `engine/svg.ts` `sanitiseSvg()` replaced
sprint 001's regex tripwire before grow could write a drawing.

- **An allowlist over a parse, re-serialised.** The source is parsed as
  XML. DOCTYPE, CDATA, processing instructions after the declaration,
  undefined entities, a bare `&` and unquoted or slash-joined attributes are
  refused. Every element and attribute must be on a list. The loader inlines
  the parse **re-serialised** with every value escaped, never the file's own
  text, so a spelling a browser reads differently from the parser (an
  entity-spelled scheme, `<g/onclick>`, odd case) cannot reach the page.
- **The list.** Elements: `svg g defs title desc path line polyline polygon
rect circle ellipse text tspan clipPath marker linearGradient
radialGradient stop`. Attributes: geometry, presentation and ARIA. Never
  `style` (element or attribute), script, `a`, `use`, `image`,
  `foreignObject`, animation, event handlers or any `href`. A `url(…)`
  value may only name `#id` inside the drawing, judged after entities are
  decoded; `xmlns` must be the SVG namespace; an `id` must be a plain name.
- **One path for everyone.** Validation reports each problem as
  `illustration: …`, and the loader inlines the output, so hand-written and
  model-written drawings are treated alike. Grow also runs every `.svg` it
  writes through it, not only the scene's. An SVG image in a reading (a
  chart) takes the same path (§Charts). A hand-written dependency was
  chosen over DOMPurify + jsdom (a DOM on the server) and sanitize-html
  (an HTML parser, where these files are case-sensitive XML).

## Charts

Built in sprint 008 (korg 3406; Ken chose inline SVG over one rendering per
scheme). A chart used to be an `<img>` of a standalone SVG drawn in its
frame's palette. An `<img>` can't inherit the page's CSS, so a chart on a
dark frame stayed dark when the reader picked Light mode.

- **Inlined, through the sanitiser.** An `.svg` image in a reading is
  inlined in place of the `<img>`. Validation runs it through the
  illustration allowlist and reports each problem as `image "x.svg": …`.
  The loader inlines the re-serialised parse, never the file's text. This
  relaxes sprint 002's "charts are media files served with a no-script
  policy". An SVG from elsewhere (a Commons diagram) that the allowlist
  refuses, usually for `style`, is converted to PNG instead.
- **Palette hooks.** A chart draws in `currentColor`, which the reading
  pane sets to `--ink`, and marks two classes that the pane colours: `muted`
  (`--muted`: axis, ticks, sublabels) and `accent` (`--accent`: a
  highlighted bar). It has no background. So it follows the palette mode and
  fades with the page's palette transition. `create-tools/bar-chart` draws
  this way.
- **Named by the alt text.** The inlined drawing is wrapped in
  `<span class="figure chart" role="img" aria-label="…">` carrying the
  markdown image's alt text, exactly as the `<img>` was named. The SVG
  inside is `aria-hidden`. Its ids, and every reference to them (`url(#…)`,
  `aria-labelledby`), are prefixed `<frame>-<file>-`, so two drawings in
  one page cannot collide. The chart's numbers are still in a table under
  it (sprint 002's rule), and the caption credit follows it as before.
- The `/media` route still serves the file, for anyone opening it alone.

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
    them. They arrived with ask (3368).
- **The app config** is `kloom.config.json` at the repo root, or
  `$KLOOM_CONFIG`. It is committed, because it holds no secret, and is read
  per request, so a renamed model is a file edit with no restart:

  ```json
  {
  	"provider": {
  		"kind": "claude-cli",
  		"command": "claude",
  		"timeoutSeconds": 120,
  		"webTimeoutSeconds": 180
  	},
  	"models": [{ "id": "claude-sonnet-5", "label": "Sonnet 5" }, "…"],
  	"ask": { "defaultModel": "claude-sonnet-5", "web": "allow" },
  	"grow": { "defaultModel": "claude-opus-5-5", "timeoutSeconds": 900, "web": true }
  }
  ```

  Validation (`src/lib/server/app-config.ts`) requires a non-empty model
  list. Ids must be letters, digits, `.`, `-` and `_`, never starting with a
  dash, so a hand edit cannot make one a CLI flag. The default must be
  listed. `ask.web` is `allow`, `offer` or `deny`. `grow` is optional:
  without it, grow is not offered. Its default model must be listed too.

- **The ask model** (sprint 004) is a user setting over that list. It is a
  drop-down labelled "Ask model", Sonnet 5 by default, stored under
  `kloom.askModel`. The page's server load serves the choices, and
  `modelSetting` (`engine/settings.ts`) turns them into a row. The pick is
  what `claude -p --model` gets. The server honours it only if the config
  lists it, so a client string never reaches the command line. The **grow
  model** (sprint 005) is a second row built the same way: "Grow model",
  Opus 5.5 by default, `kloom.growModel`.
- **The layout** (sprint 010) is a row too: "Layout", two panes with tabs by
  default, `kloom.layout` (§Layout).
- **Keys** (sprint 011): one row per character shortcut, gathered under a
  "Keys" heading (a setting's optional `group`), each any letter or Off
  (§Interaction). The panel scrolls when it outgrows the window.
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
  and the shell ignores its page-wide keys (arrows, the shortcuts, Esc) for any
  target inside such an element. A closed gear is an ordinary button, so the
  arrows still move the spine from it.
- **Placement:** the end of the tab row at the head of the right-hand pane,
  in every layout (§Layout; it sat at the end of the narrative's toolbar
  until sprint 011). It is clear of the spine's corner brackets.
- **Narrative following** (sprint 006, korg 3391) is a row in the registry,
  "Narrative": _Follows the spine_ (the default) or _Stays until synced_, stored
  under `kloom.followSpine`. It sat in the toolbar as a checkbox beside the
  Sync Narrative button until that button went. The old `kloom.sync` key is
  not read, so everyone starts on the new default.
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

## Scene fit

Sprint 031 (korg 3469). The scene keeps to its row of the spine, between
the top HUD and the bottom one that holds the position and the counter.
Before this sprint it was centred in a `1fr` row and free to overflow it. A
three-line headline pushed the drawing up into the chapter label and the
metadata down into the counter, on 292 frames at 1280×800 or 1400×900 and
361 at 390 wide. The counter already had its own row in the spine's grid,
so the fix keeps the scene in its row rather than moving the counter (Ken,
2026-10-01: "put the counter in the flow"):

- **The drawing gives way.** The scene is a column that fills its row
  (`minmax(0, 1fr)`): the headline and the metadata take the height they
  need, and the drawing shrinks into what is left, down to nothing on a
  very short pane. The scene is still centred in its row, and a scene that
  fits looks as it did before.
- **Headline type scales down with length.** Up to 26 characters
  (headline, space and accent) the type is as before. Past that it shrinks
  with the square root of the excess, to no less than 0.7 of its size at
  about 52 characters, the longest in the library. Long headlines wrap less.
- **No content rule.** There is no cap on headline length in the validator,
  and no headline was rewritten.
- **`just scene-fit [subject…]`** checks every frame at 1280×800, 1400×900
  and 390×844, with motion reduced, for anything in the scene running into
  either HUD and for the counter over the metadata. It uses the machine's
  Playwright and Chromium (`create-tools/scene-fit/scene_fit.mjs`), so it
  is not part of `just check`. It starts a dev server unless one answers on
  :5415, and takes about four minutes for the whole library.

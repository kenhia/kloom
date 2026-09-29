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
- **Frame** — two halves, one per pane:
  - _scene_: headline, accent word, illustration (SVG), palette, metadata,
    optional counter;
  - _reading_: markdown narrative, charts, images, and **sources** —
    required, because this is history written with an LLM. Since sprint
    008 every frame flags at least one key-source citation, and the Sources
    list is built from those (§Content model, Citations).
- **Trail** — a small spine anchored to one frame of its parent.
- **Storage** — files in git, one directory per frame under
  `subjects/<subject>/`. The site builds from them; git is the history of how
  the subject grew, and its undo.
- **Files** (sprint 001) — `subjects/<subject>/` holds `subject.json` (title
  and named palettes: scheme, background, ink, muted, accent, line),
  `spine.json` (segments, each `{id, title, labelKind, frames: [ids]}`),
  `trails/<id>.json` (`{id, title, anchor, spine}`) and
  `frames/<id>/{frame.json, reading.md, *.svg}`. `frame.json` carries
  `position {label, sort?}`, `scene` and `citations`. Label kinds are `date`,
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
    `report`, `media`), `title`, `url` and/or `doi`, `accessed`
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
  - **Kinds.** `chapter` is a chapter or a paper in an edited volume, a
    proceedings or a symposium: "In _Volume_, edited by …, pages. Place:
    Publisher, Year." It needs its `container`. `report` is a technical,
    committee or institutional report, or a lab's system card: title in
    italics, then its `number`, series, and "Place: Publisher, Date".
  - **DOI.** `doi` holds the bare DOI (`10.1109/5.58323`) and the entry
    links it at doi.org, in place of the url. A doi.org `url` is refused:
    it goes in `doi`.
  - Every citation needs a title, an http(s) url or a doi, and an accessed
    date. Any Wikipedia url must be a permanent revision link (`oldid=`),
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
  frame's content from disk, never from the request, and refuses an unknown
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
  `subject.json`, `spine.json`, `trails/` and `frames/` into its own
  directory under `$TMPDIR` (`kloom-grow-<job>-…`), and `claude -p` runs
  there:
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
  shape. Then `validate()` over the whole copy.
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
  directory, replaces the changed trail files and `spine.json`, and commits
  exactly those paths. If anything fails, every file is put back and the
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
  A annotates words of the reading (§Annotations); Tab moves into
  and out of the AI pane, and Esc anywhere in it returns to the spine. In the
  tabs layout, the arrows on a tab move between the tabs, and on a divider
  they move the divider (§Layout). Keys
  typed into a text field stay there. `engine/keys.ts` (`pageKey`) decides
  what a press means from where focus is, and the shell acts on it.
- **Character shortcuts are scoped** (WCAG 2.1.4, sprint 004, korg 3366). S,
  T, B, N and A act only while focus is inside the spine, the narrative or the
  notes. They do nothing in the AI pane, in the settings panel, in the note
  editor, or on the bare page.
- **And remappable** (WCAG 2.1.4's other remedy, sprint 011, korg 3363).
  Each character shortcut is a setting under "Keys": any letter, or Off
  (`kloom.key.sync`, `.trail`, `.bookmark`, `.note`, `.annotate`). `keymapOf` turns the
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
  offer named the other subject). Once the reader has begun the subject
  behind the start screen, its offer is left out, because Begin already
  returns them to where they are. Begin keeps the focus.
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
bookmarks`, `GET`/`POST`/`DELETE notes`, `GET`/`DELETE kept`, `GET export`
  and `POST import`. A place, bookmark or note must name a served subject
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
  annotation (§Annotations).
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
  narrative and any unsaved note all survive. Begin or Esc returns to
  exactly where the reader was, focus goes back to Home, and the URL never
  moves. Opening another subject from there is a navigation, so an unsaved
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

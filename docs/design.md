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
    for media `licence` and `file`. `etAl: true` ends a long author list
    with "et al." in the entry and in a caption credit (sprint 006): a
    paper with hundreds of authors lists the first.
  - Every citation needs a title, an http(s) url and an accessed date. Any
    Wikipedia url must be a permanent revision link (`oldid=`), because
    articles change.
  - An image or chart in the reading is a file in the frame's directory
    (served at `/media/<subject>/<frame>/<file>` with a no-script policy), and it is
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
  directory per tool with its own README. Sprint 006 added `subject-plan`
  (the spine and trails from a plan, holding only the frames written so
  far), `commons-media` (a freely licensed image and its `media` citation)
  and a log scale for `bar-chart`. Skills for new subjects and grow
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
    segment, reading markdown, sources and citations; and the trail, if any;
  - the question;
  - a model id the server has already checked;
  - an `AbortSignal`.

  The prompt (`engine/ai/prompt.ts`) is shared by every adapter. It numbers
  the frame's citations, then any sources no citation covers, and asks the
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
  request to anywhere). It is not stored, and a reload forgets it. The
  answer scrolls in a focusable region marked `data-own-keys`, so the
  arrows scroll it. A `role="status"` line announces asking, queued,
  answering, ready, stopped and failed; the streaming text itself is not a
  live region.
- **Keep this.** Once an answer is done, "Keep this" sends only its id to
  `POST /api/keep`, with the subject. The server remembers finished answers (the last 50, for
  an hour) and writes what it remembers, never text the client sends back.
  The file goes to `<dataDir>/<subject>/kept/<id>.json`, where `dataDir` is
  `$KLOOM_DATA_DIR` or `data/`, git-ignored. A kept answer is not subject
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
  	"sources": ["the frame's plain sources it marked"],
  	"provider": "claude-cli",
  	"model": "claude-sonnet-5",
  	"askedAt": "2026-09-27T17:09:11.000Z",
  	"keptAt": "2026-09-27T17:09:20.000Z"
  }
  ```

  The `[n]` numbers refer to the frame's references in prompt order, and
  `citations` carries exactly the ones used, in the §Citations shape. The id
  is the ask time plus 8 random hex digits, safe as a file name. Grow checks
  a file with `keptAnswerProblems` before reading it. A web turn's pages
  are carried in an optional `webCitations` (§Web search for ask).

## Web search for ask

Built in sprint 005 (korg 3376, Ken's decisions of 2026-09-27).

- **An app setting.** `ask.web` is `allow` (committed), `offer` or `deny`,
  and an absent `ask.web` means `deny`. The reader's control is an "Include
  web" checkbox beside Send, shown unless the config is `deny`. It starts
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
  frame.
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
  newest. The AI pane's Grow
  row is a verb select, a request field and Queue, with a job list. It
  polls every 3s while a job is live, announces the outcome in the status
  line, and reloads the page's data when one lands. After "Keep this", a
  "Grow from this" button attaches the kept answer.

## Interaction

- **Scroll ownership.** The wheel over the spine pane moves along the spine;
  the wheel over the narrative scrolls the narrative. Never both — a good
  narrative is often longer than a screen.
- **The narrative follows the spine** (Ken, 2026-09-27, sprint 006, korg
  3391). Moving along the spine turns the reading to that frame. Separate
  movement was the first default, with a "Sync Narrative" button, and it
  proved the wrong one in use. Not following is a reader setting,
  "Narrative: Stays until S", in the settings control (`kloom.followSpine`).
  With it, the reading stays put until S brings it to the spine, and the
  toolbar's status line says where each one is. The button is gone; S
  remains.
- **One gesture, one frame.** Wheel deltas over the spine accumulate to a
  threshold, then a cooldown swallows the trackpad's inertia.
- **Keyboard first.** Left/Right move along the spine (Home/End jump to its
  ends); Up/Down scroll the narrative; S syncs the narrative; T enters the
  trail branching from the current frame and Esc leaves it (S matters only
  when the reader has turned following off); Tab moves into
  and out of the AI pane, and Esc anywhere in it returns to the spine. Keys
  typed into a text field stay there. `engine/keys.ts` (`pageKey`) decides
  what a press means from where focus is, and the shell acts on it.
- **Character shortcuts are scoped** (WCAG 2.1.4, sprint 004, korg 3366). S
  and T act only while focus is inside the spine or the narrative pane. They
  do nothing in the AI pane, in the settings panel, or on the bare page.
  The arrows, Home/End and Esc are not character keys, so they stay
  page-wide, except in a text field or an element marked `data-own-keys`.
  The hint bar says so. Visible focus, ARIA
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
  author. Keep does not record one yet; per-reader data comes later (korg
  3413).

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
- **The chooser is the start screen.** Under Begin, "Or open" links every
  other subject, in the dialog's tab order after Begin. The page is keyed
  by subject, so opening another one starts its shell afresh at its own
  start screen.
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
  writes through it, not only the scene's. A hand-written dependency was
  chosen over DOMPurify + jsdom (a DOM on the server) and sanitize-html
  (an HTML parser, where these files are case-sensitive XML).

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
- **Narrative following** (sprint 006, korg 3391) is a row in the registry,
  "Narrative": _Follows the spine_ (the default) or _Stays until S_, stored
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

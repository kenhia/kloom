# 005 — Grow: queued frame/trail jobs behind an allowlist sanitiser, web ask, grow-model setting

## Goal

korg proposal 3369. It covers three work items, in this order:

- korg 3365: replace the illustration regex tripwire with a real allowlist
  sanitiser, applied at load, before any model writes an SVG.
- korg 3376: optional web search for ask (WebSearch/WebFetch) behind an
  app-config switch, with web sources carried into kept answers. Ken moved
  it here from 004 because grow needs the same web plumbing.
- korg 3364: grow. Queued, async jobs add main-spine frames, add a trail
  anchored to a frame, do both, or turn a kept answer into content. Each job
  writes validated frame directories and commits them. It adds a grow-model
  setting, Opus 5.5 by default.

## Decisions

- **Premises held.** The only SVG check was the regex tripwire in
  `engine/validate.ts`. Ask ran with `--tools ""` and the app config had no
  `ask.web`. No grow code existed. One part of 3365 had already shipped:
  sprint 001's `safeUrl` normalises entities and control characters in
  markdown href/src, and has tests for a tab and a leading control. That
  part was confirmed, not redone. kloom is not in the cross-project plan
  index.

### The sanitiser (3365)

- **A small hand-written allowlist parser, no dependency.** The options were
  DOMPurify + jsdom, sanitize-html, or a small parser:
  - DOMPurify needs a DOM on the server, which means jsdom and its tree.
  - sanitize-html is built on an HTML parser, and illustrations are XML:
    case matters (`viewBox`, `pathLength`) and self-closing tags are
    everywhere.
  - Illustrations are small and regular. The 16 curated plates and the
    loom use 8 elements and 26 attributes.

  `engine/svg.ts` `sanitiseSvg()` parses the source as XML and refuses
  what XML makes dangerous: DOCTYPE (entity definitions), CDATA,
  processing instructions past the declaration, undefined entities, bare
  `&` and unquoted attributes. It checks every element and attribute
  against a list, and **re-serialises the parse**. The page never receives
  the author's own text: it gets markup this module emitted, with every
  value escaped. A spelling a browser reads differently from the parser (an
  entity-spelled scheme, a slash before a handler, odd case) has nowhere to
  hide.

- **What the list allows:** the drawing elements (`svg g defs title desc
path line polyline polygon rect circle ellipse text tspan clipPath marker
linearGradient radialGradient stop`), plus geometry, presentation and ARIA
  attributes. It has no `style` (element or attribute), `script`,
  `foreignObject`, `a`, `use`, `image` or animation, no event handler, and
  no `href` of any kind. A `url(…)` value may only point at `#id` inside
  the drawing, and it is judged after entities are decoded. `xmlns` must be
  the SVG namespace. An `id` must be a plain name.
- **Applied at load.** Validation reports every problem as
  `illustration: …` and the site refuses an invalid subject, as before. The
  loader inlines the re-serialised markup, so hand-written and
  model-written drawings take the same path. Every curated plate passes,
  and its output re-sanitises to itself (a fixed point, tested per file).
- **The 001 review probes are regression tests** (`<g/onclick=…>`,
  `java&#x73;cript:`, `<style>`, `<embed>`, `<use href>`), alongside 26 more
  cases in `engine/svg.test.ts`.

### Web search for ask (3376)

- **As Ken decided (comments on 3376, 2026-09-27).** App config `ask.web`
  is `allow`, `offer` or `deny`, and the committed default is `allow`. An
  absent `ask.web` means `deny`, so a hand-written config without it is
  closed. An "Include web" checkbox sits beside Send whenever the config is
  not `deny`. It starts checked under `allow` and unchecked under `offer`
  (Ken confirmed this split at sprint start). It is not remembered: it is a
  per-question choice, not a setting.
- **The server enforces it.** `resolveWeb` honours a request's `web: true`
  only when the config is not `deny`, the same pattern as `resolveModel`.
  Only a literal `true` counts.
- **The adapter** adds `--tools WebSearch,WebFetch --allowedTools
WebSearch,WebFetch` for a web turn, and nothing else. The rest of ask's
  lockdown is unchanged. A web turn gets `provider.webTimeoutSeconds` (180)
  instead of 120.
- **"Searching the web…"** A `content_block_start` of a `tool_use` in the
  stream becomes a `{type: 'status', status: 'searching'}` provider event.
  The same event resets the answer: text streamed before a search is the
  model thinking aloud ("Let me look that up"), so the client, the
  server's remembered answer and the adapter's result fallback all drop it.
  The web system prompt also says to write nothing until searching is done.
- **Web sources: an optional `webCitations` on the kept answer**, rather
  than a version 2. The field is additive, and every version 1 file is
  still valid. The web prompt asks for `[W1] Title — URL` lines after the
  answer. At keep time, `webReferences()` reads them and they become `web`
  citations accessed on the day asked. **Wikipedia pages are pinned at keep
  time** (`engine/ai/wikipedia.ts`, the TypeScript twin of
  `create-tools/wiki-cite`). Each becomes a `wikipedia` citation at the
  article's current revision, which is the one the model just read. If
  the lookup fails, the keep fails (502, "Could not keep it: …") rather
  than storing an unpinned link that grow would have to repair.
- **Live on kai** (dev server, claude 2.1.283). A web ask on `jwst` (Haiku
  4.5) searched once, answered with three `[W1]`–`[W3]` pages, and kept
  them as three `web` citations. Sonnet 5, asked to read the Wikipedia
  article, kept it as
  `…title=James_Webb_Space_Telescope&oldid=1377003479`. Two things turned
  up along the way. A model does not always search: Haiku and Sonnet each
  answered a JWST launch-date question from their own knowledge, which the
  prompt allows. Such a keep carries an empty `webCitations`, and the file
  is still valid.

### Grow (3364)

- **The instructions are a skill file**, `skills/grow/SKILL.md`, with
  frontmatter so it can later be a Claude Code skill. The proposal asked for
  "a reusable skill/instructions file in the repo, not prompt strings
  buried in code". It is passed as the system prompt with the frontmatter
  stripped. It is written against the curated frames: the scene grammar,
  §Illustrations (plates, three weights, ordered groups, `pathLength`), the
  sanitiser's allowlist, reading length and heading rules measured from
  the 16 readings (373–615 words), and §Citations, including how to pin a
  Wikipedia revision with one WebFetch of the MediaWiki API. The per-job
  prompt (`growPrompt`) carries only the verb, anchor, kept answer, web
  availability and the reader's words.
- **Sandbox: a copy outside the repo, not a directory under
  `subjects/<subject>/`.** The proposal said "a working directory under
  subjects/<subject>/ only". What I built keeps the intent: nothing but
  files under `subjects/<subject>/` ever changes. The model itself works
  on a copy under `$TMPDIR`, for three reasons:
  - The loader serves `subjects/<subject>/` per request, and a
    half-written frame there makes the whole subject fail validation.
  - The model's file tools are confined by directory, and a working
    directory inside the repo would pick up its `CLAUDE.md`.
  - The home directory has to be denied outright (below), and the repo
    lives in it.

  The job copies back only new frame directories, trail files and
  `spine.json`.

- **Confinement was measured, not assumed** (claude 2.1.283, probe in the
  session). `--permission-mode acceptEdits` with `--tools
Read,Write,Edit,Glob,Grep` wrote `ok.txt` in the working directory, and
  refused a write to `~/kloom-probe.txt` and to `/tmp/…`. With
  `--disallowedTools Read(~/**) Edit(~/**) Write(~/**)`, reading
  `~/.bashrc` was refused. That matters because WebFetch plus a readable
  home directory is an exfiltration path: a page could ask for a key and
  the fetch URL could carry it. The job refuses a work root inside the home
  directory.
- **No shell, so grow runs no tools.** Whether grow could run or add
  create-tools had been left open in `create-tools/README.md` for this
  sprint. The answer is no: that would be model-written or model-driven
  code on the host because a reader typed a request. Grow reads the tool
  READMEs and `plates.py` as references and computes geometry itself. The
  README now says so.
- **What may come back is checked twice.** `growthProblems` checks the
  change is additive: the manifest and every existing frame unchanged, and
  segments, trails and frames kept in order. It also checks new frame ids,
  the files a new frame may hold (`frame.json`, `reading.md`, `*.svg`, each
  under 200 KB, every SVG sanitised), and the verb's shape. Then
  `validate()` runs over the whole copy.
- **One repair turn.** If the first turn leaves problems, the model gets
  the list and one more turn over the same directory. This is cheap
  insurance, because a model cannot run the validator itself.
- **A validation failure is decided as the proposal asked:** no commit,
  nothing copied, and the problems surfaced in the AI pane under "What the
  validator found". The work directory is kept for inspection.
- **Commit identity and message:** `kloom grow <grow@kloom.local>` as author
  and committer, and `--no-verify` (a repo's hooks are for people). The
  subject line is `grow(<subject>): add <ids>[; trail <ids>]`. Then come the
  model's summary and a trailer block with the job, verb, anchor, request,
  kept answer, model (with provider) and web. Only the job's own paths are
  committed (`git commit -- <paths>`), so nothing else staged goes with
  them.
- **Applying is guarded.** Grow will not apply over uncommitted changes to
  the subject. It will not apply if the subject changed since the job
  copied it, since `spine.json` is replaced whole. It writes under a gate
  that holds page loads and asks (`servedSubject`/`exclusive`), and renames
  each frame in from a hidden `.grow-<id>` directory, which the loader now
  skips. A failed commit puts every file back and resets the index. That
  path is tested with a held `index.lock`.
- **The queue survives a restart** (`GrowQueue`). Each job is a
  `kloom.grow-job` file under `<dataDir>/<subject>/grow/`, written
  atomically through one save chain. A late progress save once could have
  overwritten a job's outcome, so saves are serialised. `hooks.server.ts`
  loads the queue at start. `queued` jobs wait again. A `running` job is
  re-run once from a fresh copy, since nothing was applied, and failed on a
  second interruption. An `applying` job is failed with "check git
  status". One job runs at a time, ten may wait, and grow does not share
  ask's turn queue, so a long grow never blocks a question.
- **Found by the tests:** two jobs queued in the same second got ids that
  sort by their random tail, so the queue could run them out of order.
  `queuedAt` is now strictly increasing and is the sort key.
- **Model selection as Ken set it:** a "Grow model" drop-down built from the
  app config, Opus 5.5 by default (`grow.defaultModel`). It is captured when
  the job is queued, checked against the config (`resolveModel` with the
  grow fallback), and recorded in the job and the commit.
- **The AI pane's Grow row** is below ask, with a verb select, a labelled
  request field and Queue. "A side trail from this frame" is disabled when
  the frame is not on the main spine. The job list shows each job's verb,
  anchor, model and state. While a job is live it polls `GET /api/grow`
  every 3s. The status line announces "Grow queued…", and then "Grow added
  …" or "Grow failed: …". A landed job calls `invalidateAll()`, so the new
  frames appear. After "Keep this", "Grow from this" attaches the kept
  answer, anchoring the job to that answer's frame and choosing a trail
  when it can.
- **Provider interface.** `Provider` gained `grow(GrowRequest)`, and the
  `claude -p` adapter's process handling moved into one `#run` shared by
  ask and grow. `growArgs` holds the confinement above. Without partial
  messages, a tool shows up in the `assistant` message, and
  `parseStreamLine` now reads it there too. Grow's statuses are `reading`,
  `searching` and `writing`.

## Verification

- `just check` passes: svelte-check shows 0 warnings, prettier and eslint
  are clean, and vitest runs 223 tests (182 at the start of the sprint).
- **Negative-tested:**
  - putting `script` on the allowlist failed 2 tests;
  - letting `resolveWeb` ignore `deny` failed 1;
  - dropping the "existing frame was changed" check in `growthProblems`
    failed 1.

  Each was restored.

- **Live grow on kai** (dev server on a scratch git repo holding a copy of
  western-civ, so no model commit touched this branch). The verb was
  `frames` from `printing-press`: "Martin Luther and the Ninety-five Theses
  (1517)…". It ran on Opus 5.5 with the web.
  - It took 3m43s and passed validation on the first turn.
  - It committed `ninety-five-theses` ("We took the argument PUBLIC.", AD
    1517), between `printing-press` and `voyages`, as
    `kloom grow <grow@kloom.local>`. The commit held exactly the three
    frame files and `spine.json`.
  - The reading is 605 words. It pins three Wikipedia revisions (`oldid=`)
    and cites two real books (Edwards 1994, Pettegree 2015).
  - The plate is a folded-sheet diagram with construction lines and
    projection rays, and it reads like the curated ones.
  - The model's summary listed the three claims it had not checked against
    a source.
- **Restart, live.** A second job (Haiku 4.5, Erasmus's New Testament) was
  queued from the keyboard. The dev server was killed while it searched.
  After a restart the job came back `running` on attempt 2 from a fresh
  copy, and committed `erasmus-greek-nt`. The first attempt's orphaned
  `claude` was still running in its own temp copy; see Follow-ups.
- **Keyboard-only browser pass** (Playwright, headless Chromium, on the
  grown subject):
  - Tab from the Ask box runs: Include web (checked), Send, the verb
    select, the grow box, then Queue. Space toggles Include web.
  - ArrowDown on the verb select changes the verb and does not move the
    spine. "st" typed in the grow box stays there, and Esc returns to the
    spine.
  - On a trail frame, "A side trail from this frame" is disabled and the
    verb falls back to frames. Back on the main spine it is enabled again.
  - The gear panel lists Palette, Ask model and Grow model, and Grow model
    defaults to Opus 5.5.
  - Queue announced "Grow queued: new frames on the main spine, on Haiku
    4.5.", and the job list showed both jobs.
  - At 390px the first run **had horizontal scroll**. The AI pane's
    single `1fr` column took its minimum from the widest child. It is now
    `minmax(0, 1fr)`, the verb select may shrink, and the scroll is gone.

- **Ken's grow, on this branch.** Ken ran a grow from the app during the
  sprint: the `measure` trail from `eratosthenes` ("The measure of
  things"), with `royal-cubit`, `harrison-chronometer`, `metre-survey` and
  `si-redefinition`, committed as `e6e0997` by `kloom grow`. It ships
  with the sprint. It turned up two things:
  - A content test pinned "one trail". It now expects both trails,
    sorted.
  - `harrison-chronometer/reading.md` was valid but not Prettier-clean
    (one line wrapped early), so a grow commit could break `just check`.
    The file is reformatted. Grow now formats the JSON and Markdown it
    writes with the repo's own Prettier config before committing
    (`formatGrown`). It skips this where Prettier is not installed, since
    Prettier is a dev dependency. Tested with a minified `frame.json` and
    a `*` bullet.

- **The two live-test frames joined the subject** at Ken's request.
  `ninety-five-theses` (Opus 5.5) and `erasmus-greek-nt` (Haiku 4.5) were
  grown in the scratch repo and carried over with `format-patch`/`am`, so
  they keep their `kloom grow` commits (`f5f6856`, `397fb6e`). A style
  commit (`bd1840f`) formats them, because they predate `formatGrown`. The
  main spine is now 18 frames, and the page test's "01 / 16" is now
  "01 / 18".

## Repaired in passing

- `.github/copilot-instructions.md` had not been synced since sprint 003
  (it still said "No AI backend yet"). Its Project section is copied from
  `CLAUDE.md` again.
- `create-tools/draw-plates/__pycache__/plates.cpython-312.pyc` was
  tracked. It is now untracked, and `__pycache__/` is ignored.
- `create-tools/README.md` still named the tripwire and left grow's use of
  tools open. It now names the sanitiser and records the decision.

## Follow-ups

- **Access control before the kai service (korg 3384).** Ask and grow are
  unauthenticated, and grow commits. Loopback is fine for now. Which
  option applies is Ken's policy call. The same item notes that a grow
  job's `claude` child outlives a killed server (harmless: its own temp
  copy, no commit), which systemd's default `KillMode=control-group`
  covers.
- Models do not always keep to "two or three sentences". Haiku narrated its
  whole checklist, so the commit body is capped at 2000 characters and the
  result at 1000.
- The AI pane now holds two rows, Ask and Grow, under one "Ask" region
  label. Fold that into the layouts work (korg 3377).

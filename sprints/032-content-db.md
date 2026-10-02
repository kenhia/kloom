# 032 — content.db

## Goal

korg proposal 3480, covering korg 3460 (decided 2026-09-30): the subjects'
files stay the source of truth, and kloom serves from a compiled SQLite
`content.db`. Build it from the files, rebuild it when they change, send
frames on demand with their neighbours fetched ahead, compress responses,
and gate on a benchmark at five times today's content. It sits on the
critical path for the public reader site (3458), whichever host that picks.

## Decisions

- **The premise held, and the content had grown.** At the start every
  request still rebuilt the subject, the graph and the counts from disk,
  and the page inlined every frame (`src/lib/server/subject.ts`). Since
  3460's baseline the library had roughly doubled: 615 frames, 515,772
  words (about 1,876 pages), 3,142 names, 117 MB and 5,839 files under
  `subjects/` and `names/`. The live service (ssh door, sizes identical
  with or without `Accept-Encoding`) measured:

  | Page           |      Size |   Time |
  | -------------- | --------: | -----: |
  | `/ai/eliza`    | 1,602,092 | 0.29 s |
  | `/physics`     | 2,158,849 | 0.30 s |
  | `/western-civ` |   534,877 | 0.21 s |
  | `/blood`       | 1,942,957 | 0.28 s |
  | `/api/map`     | 1,148,262 | 0.19 s |
  | `/api/stats`   |     2,194 | 0.33 s |

  kloom is not in the cross-project plan index.

- **A frame is a head and a body** (`engine/model.ts`, `engine/served.ts`).
  The head is what every frame sends with the page: id, topic, position,
  scene and `asOf`, about 1 KB. The body is the reading, the drawing,
  citations and Sources, plus the frame's links. The contents, the map,
  the marks, random jumps and the start screen needed heads only, so
  nothing else changed shape.
- **Links went per frame.** The page used to carry `linksFor(subject)`,
  every connection and name card for the whole subject: 430 KB for
  physics. A frame's body now carries only its own connections, both ways,
  and the cards of the names its reading marks (`linksByFrame`,
  `engine/graph.ts`). They are derived once per build from the whole
  library, so a connection stored on another subject's frame shows on
  both ends as soon as either is built.
- **The compiler is incremental, and the digest is cheap.** A full build
  of today's library takes about 1.4 s, so a full rebuild after every grow
  would have held readers at the gate for about 7 s at 5×. Instead each
  subject carries a digest of its files (path, size and modified time;
  hidden entries skipped, so grow's `.grow-<id>` staging is ignored). Only
  changed subjects are compiled, then what spans subjects (names, links,
  map, counts) is derived again over the old rows. The cost is a copy of
  the file plus the derivation: 0.35 s for one subject today, 0.84–1.03 s
  at 5×. Checking a current library takes 14 ms today and 67 ms at 5×.
- **"What compiled it" is part of the key.** New rendering code must
  rebuild everything, but a digest of the content cannot know that. In a
  checkout the compiler id is a hash of the engine's non-test TypeScript
  (relative paths, sizes and modified times). In a deployed app, which has
  no engine source, it is the build's commit (`__KLOOM_BUILD__`). A
  different compiler starts afresh.
- **Strict for the gate, forgiving for the service.** `compileContent`
  validates every subject it compiles. In strict mode (the gate and
  `just build-content`) any invalid subject fails the build, every
  problem named, and the old file stands. The app's own builds keep
  serving an invalid subject as it was last built, and say why in the
  journal. A subject that was never valid is simply not served (404).
  Names changing does not recompile subjects: a grow adds names often, and
  `graphProblems` in the gate still catches a mark with no name.
- **No watcher of our own** (measured, then reversed). The first version
  had the app watch `subjects/` and `names/` recursively. At 5× Node's
  recursive watch held a watcher per directory (3,226 of them): about
  120 MB and 3 s at start. A service's content only moves at start (the
  sync) and in a grow, and both rebuild anyway. The dev server already has
  Vite's watcher, so a small plugin (`kloomContent`, `vite.config.ts`)
  forwards its events for the content directories as a process event, and
  the next read rebuilds. A hand edit in the service's clone shows after a
  restart (docs/deploying.md).
- **The page opens on what it needs.** It carries the head, the start look,
  and the bodies of the frame it opens on and two either side. The shell
  asks for the frame under the cursor, two either side, and the
  narrative's frame (`onneed`). The page fetches the missing ones from
  `/api/frame/<subject>/<frame>` and caches them per subject and build. A
  new build, after a grow, starts the cache afresh. The shell reads
  `bodies` in its effect, so a frame whose body went with the old cache is
  asked for again.
- **Pending is a state, not an error.** Until a body arrives, the scene
  shows its head without the drawing, the reading says "Fetching the
  reading…" (`role="status"`), Sources is hidden, and annotations wait
  rather than reporting themselves detached.
- **Compression in the hook, and precompressed where it repeats.**
  `compress()` (`src/lib/server/compress.ts`, called from the `handle`
  hook) sends HTML, JSON, SVG, CSS and JS over 1 KB as Brotli (quality 5)
  or gzip, and weakens a strong ETag. Ask's NDJSON is excluded, so it
  still streams. Compressing the 5.7 MB map per request took 38 ms at 5×,
  over the 20 ms target, so the map and the counts are compressed once per
  build (Brotli 9: 75 ms, once) and sent as stored, at 0.4 ms.
- **Frame bodies are tagged with the build.** The ETag is the build, so a
  revalidation is a 304. The client keeps its own cache per build, so in
  practice this matters for reloads.

## What shipped

- `engine/content-db.ts`: `compileContent` (incremental, strict or not,
  atomic rename), `ContentDb` (one indexed query per read; bodies, the map
  and the counts handed back as their stored JSON), `treeDigest`,
  `engineDigest`. The schema covers subjects (head, start look, stats,
  graph), frames (body, reading as authored), media, names, mentions,
  connections, per-frame links, the library's map and counts, FTS5 over
  reading text and topic (`ContentDb.search`, for a later search feature),
  and meta (schema, compiler, names digest, build, source commit).
- `engine/served.ts`: `FrameSource`, `ServedBody`, `headOf`, `bodyOf`,
  `subjectHeadOf`, `PENDING` and `around` (the frames either side on
  whichever spine walks one).
- `src/lib/server/subject.ts`: the library's keeper. It builds on first
  read, rebuilds after a grow inside the gate, takes the dev server's
  change events, reopens the file when a build swaps it, and memoises per
  build. `servedSubject` is now a head; `servedBody`, `servedSource`,
  `servedStart`, `servedLibrary` and `servedGraph` read the library.
  `hooks.server.ts` builds it at start, after the content sync.
- Routes: the page load (head, start look, bodies around the opening
  frame, build), the new `/api/frame/<subject>/<frame>`, and map, stats,
  start and ask from the library. Grow, media and reader data still check
  the subject on disk, since they write to it or read its files.
- The shell, spine, narrative and AI pane work on heads plus a map of
  bodies. The page holds that map, fetches what the shell needs, and
  starts afresh per build or subject.
- `just build-content [out]` (strict), `just bench [times] [args]`
  (`bench/content.mjs`), and `just verify` now checks that a frame's body
  answers and that pages go compressed, and names the library's build.
- Gate: a vitest global setup (`vitest.content.ts`) compiles every subject
  strictly before any test, so an invalid subject fails `just check` with
  its problems named, and the route tests read that library. New tests:
  the compiler (9), the served helpers, the frame endpoint, the map's
  precompression, `compress`, and the pending reading.
- Docs: design.md §Serving (new), with §Connections' graph index, §Ask's
  context and §About's counts brought up to date; docs/deploying.md (the
  library's place, what rebuilds it, the journal line).

## Measured

`just bench` copies the library N times (subject, name and Wikidata ids
suffixed per copy, connections, marks and homes renamed to match, media
hard-linked), then serves it with a production build on loopback. "Before"
is `origin/main` (eb01841) built in a worktree and served the same copy.

**Today's size (×1: 10 subjects, 2,697 files, 96 MB; 3,142 names)**

|                             |                      Before |                   After |
| --------------------------- | --------------------------: | ----------------------: |
| `/physics`, raw             |                    2,104 KB |                  401 KB |
| `/physics`, on the wire     | 2,104 KB (never compressed) |          70 KB (Brotli) |
| `/physics`, time            |                      279 ms |                  9.5 ms |
| `/western-civ`, on the wire |                      518 KB |                   39 KB |
| Frame step                  |               (in the page) |            1.0 ms, 7 KB |
| `/api/map`                  |            193 ms, 1,121 KB |          0.4 ms, 269 KB |
| `/api/stats`                |                      315 ms |                  0.3 ms |
| Library build               |                      (none) | 1.4 s; content.db 31 MB |

**Five times (×5: 50 subjects, 13,485 files, 479 MB; 15,710 names)**

|                                     |                    Before |                                       After |           Target |
| ----------------------------------- | ------------------------: | ------------------------------------------: | ---------------: |
| First page, compressed (`/physics`) | 2,114 KB (not compressed) |                                       71 KB |         ≤ 300 KB |
| First page, raw                     |                  2,114 KB |                                      411 KB |                  |
| Time to first byte (`/physics`)     |                    974 ms |                                      9.0 ms |                  |
| Frame step                          |             (in the page) |                   median 0.8 ms, p95 1.2 ms |         ≤ 100 ms |
| `/api/map`                          |          904 ms, 5,773 KB |                              0.4 ms, 396 KB |          ≤ 20 ms |
| `/api/stats`                        |                  1,569 ms |                                      0.2 ms |          ≤ 20 ms |
| Full compile                        |                    (none) |                                      6.45 s | well under 1 min |
| One subject changed                 |                           |                                 0.84–1.03 s |                  |
| content.db                          |                           |                                      157 MB |                  |
| Server memory, idle                 |                     79 MB |                                       95 MB |                  |
| after the first page                |                    315 MB |                                       99 MB |                  |
| after the whole benchmark           |                    694 MB | 248 MB (prebuilt) / 398 MB (built at start) |                  |

Every target is met at 5×. Memory after the benchmark is V8 keeping heap
it used to render and compress, not anything held: idle and first-page
figures are the steady state.

## Checked live

- **Annotations place on frames fetched on demand** (Playwright and
  Chromium against a dev server with a scratch data directory). The page
  opened on `western-civ/prometheus` and fetched nothing after load. Three
  steps right fetched `eratosthenes`, `pantheon` and `scriptorium` ahead,
  and an annotation on `eratosthenes` placed (2 marks and its button, no
  detached notice). A jump from the contents to `jwst` fetched it and its
  neighbours on the jump, and its annotation placed too. The two scratch
  notes were deleted afterwards.
- **The service's own content.** This build, run against
  `~/.local/share/kloom/content` (grow/kai at eb01841, no grow branch set,
  so nothing synced) with a scratch data directory, built all ten subjects
  in 1.45 s, every one valid, and recorded the source commit. Pages went
  as Brotli at 40–72 KB in about 10 ms.
- **A grow on the dev server shows its frames at once.** I ran a dev server
  against a disposable clone of the repo in `.scratch/` (Vite ignores
  `.scratch`, so the watcher played no part), and a real grow with Sonnet 5
  added a frame after `printing-press` on the Jikji of 1377. The first try
  timed out at the configured 900 s while the model searched the web, and
  committed nothing. The retry, with web search off and a longer timeout in
  a scratch config, committed `jikji` and six names. The journal said
  `content: built western-civ in 192 ms; 9 subject(s) unchanged`, at
  05:26:57.623, before the job reported done (.655). The first page read
  after it listed `jikji`, `/api/frame/western-civ/jikji` served its body
  under the new build, and the counts read 616 frames and 3,148 names (615
  and 3,142 before).

## Repaired in passing

- `src/lib/server/config.test.ts` restored `KLOOM_SUBJECTS_DIR` by
  assigning `undefined`, which `process.env` stores as the string
  `"undefined"`. A later test file in the same worker then served subjects
  from a directory named `undefined`. That was harmless while every read
  went to disk. Under a shared library it rebuilt the gate's
  `content.db` from no subjects in the middle of another test, which is
  how it showed up: once, as a 304 test getting a 200. It now deletes the
  variable when there was none.

## Follow-ups

- Filed as korg 3486: a dev server that reloads its server modules while a grow job
  runs restarts the job and leaves the first `claude` child running, so
  two grows write into one subject (seen here when an engine edit landed
  mid-grow). The fix is a decision about what a reloaded queue should do
  with a job already in flight: adopt it, kill it, or refuse to reload.

## Deployed

2026-10-01 22:40 PDT on kai, by `just deploy` from merged main
(`c037058`, PR #38). The start-up sync fast-forwarded the content clone
(`grow/kai`) to `origin/main`. The library then built all ten subjects in
1,422 ms (`~/.local/share/kloom/data/content.db`, 31 MB).
`just verify` passed every check, including the two new ones: a frame's
body comes from the library, and pages go compressed. It named build
`2026-10-02T05:40:51.817Z 9a7458`.

Live, on the ssh door:

- `/physics` is 73 KB as Brotli in 14 ms, and 415 KB raw in 6 ms. It was
  2,158,849 bytes in 0.30 s this morning.
- `/ai/eliza` is 55 KB in 11 ms.
- `/api/frame/physics/coulomb` is 9 KB in 2 ms.
- `/api/map` is 275 KB, and `/api/stats` takes 1 ms.

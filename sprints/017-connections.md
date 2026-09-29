# Sprint 017 — Connections 1: names, connections, and jumping between subjects

korg proposal 3443, covering 3439. Branch `017-connections`. Phase 1 of the
connections design, whose decisions are in the 2026-09-29 comment on korg 3399.

## Goal

The four subjects touch each other everywhere: Turing, the IBM 704,
Bletchley Park, softmax as the Boltzmann distribution. Sprints 006, 014 and
015 recorded 64 candidate links between them, and none could be built,
because a reading could only link http(s). This sprint builds the model and
the navigation:

- a **name registry** shared by every subject, keyed by Wikidata ID;
- **name marks** on a reading's first mention of a name, which open a card
  ("Appears in…");
- **connections** from frame to frame, each with a required _why_, shown on
  both ends;
- **jumps** that land on the frame across subjects, with the browser's Back
  and a stacking "↩ Back to…" chip.

## Premise check

- **3439 holds.** `engine/markdown.ts` still kept only http(s) and
  scheme-less links, so no reading could name another frame. The three
  §Candidate links sections were in sprints 006, 014 and 015, and western-civ
  still had 24 frames.
- No cross-project plan lists kloom.

## Decisions

Ken's, from the brainstorm on 3399 (2026-09-29): two layers, names and
connections; the first mention per frame marked; a card rather than a
direct jump; identity by Wikidata ID; history-based Back with a stacking
chip; cross-subject jumps landing on the frame; a missing target detached,
never a failure; duplication across subjects left alone for now.

The model choices the proposal left to the sprint:

- **The registry lives at the top level:** `names/<id>.json`, beside
  `subjects/`, never inside one. `$KLOOM_NAMES_DIR` overrides it, and by
  default it is `names/` beside `$KLOOM_SUBJECTS_DIR`, so the service's
  content clone carries its own and grow can extend it there later. The
  local id is the file stem and what a mark names. The Wikidata ID is a
  field, required even as `null`, so an author has to decide; two names
  may not share one.
- **The inline syntax is `[words](kloom:e/<id>)`**, as the design comment
  proposed. It is the only `kloom:` link. `kloom:<subject>/<frame>`, a link
  from a reading to a frame (3399's first comment asked), is left out:
  connections carry that with a _why_, and a second way would split them.
- **The index is built per request, lightly.** `readGraphSubject` reads
  titles, positions, connections and the marked names, and renders
  nothing: about 40 ms for the four subjects, in parallel with the
  subject's own load. That is no worse than the per-request reading the
  app already does, and content written to disk shows at once, so there is
  no cache yet.
- **Serving checks a mark's form, not its name.** A subject never becomes
  unservable because a registry kept apart from it changed. Unknown names
  are refused where content is made: by the gate, which validates every
  subject against the registry, and by grow, which is handed it.
- **A repeated mark warns in validation, and fails the gate.** It renders
  as its words, so it hurts nothing, and grow is not refused over one. But
  a warning printed only under the verbose reporter is not a gate, so the
  repository's own content must have none, as with svelte-check.
- **Connections are one list.** Outgoing and incoming together, each with
  its _why_. An incoming one says "From …" to a screen reader. The
  direction matters to whoever stored it, rarely to the reader.
- **The Back chip is the browser's Back.** Each history entry carries the
  jumps that led to it in `page.state.back`, and the spine's `replaceState`
  keeps it, so the chip can never disagree with the browser, and Forward
  brings the chip back. R is its key: the seventh shortcut, remappable and
  scoped like the others.
- **Focus lands on the spine after a jump**, and after Back. The link
  followed is gone once the card closes or the frame changes, and the
  spine announces the new frame.
- **The name card is a popover**, like the contents and the bookmarks:
  focus goes into it, Esc returns it to the mark, and a click or focus
  outside closes it.

## What shipped

- **Engine.** `engine/names.ts` (the name file and its rules),
  `engine/graph.ts` (the index, backlinks, name cards and
  `graphProblems`), and in `engine/markdown.ts` the name mark as a
  button, first mention only. Validation checks connections' form (a
  `<subject>/<frame>` target, a required _why_, no repeats) and name
  marks against a registry when given one. The loader reads the registry
  (`loadNames`) and a subject for the graph (`readGraphSubject`).
- **UI.** `NameCard.svelte`; a Connections section above Sources; the
  jump, with a history entry; `BackChip.svelte` in the spine's HUD; R.
- **Server.** The page's load carries the subject's links (`linksFor`),
  and grow validates against the registry.
- **`create-tools/names`.** `lookup` finds Wikidata items from Wikipedia
  titles and flags redirects. `mark` marks first mentions from a spec, and
  `--check` exits 1 if one is missing.
- **Content.**
  - **127 names:** 120 for western-civ, plus 7 shared things.
  - **Marks:** 169 across all 24 western-civ frames, and 29 for the
    shared things in 28 AI, Computing and Feynman frames. The specs are
    in `create-tools/names/examples/`.
  - **45 connections on 35 frames.**
  - Every Wikidata ID was checked against its item's label in one batch
    read. That caught one wrong ID: horsepower was the metric unit, and is
    now the imperial one, Watt's.
- design.md §Connections, and §Interaction's keys.

## The 64 candidates

Sprints 006, 014 and 015 listed 64 entries, about 100 links, many of them
the same link from each end. Here is where they went:

- **Connections (45).** Each is stored once, on one end, with a _why_
  checked against the readings at both ends. Three are within Computing,
  from its authors' own list: ethernet ↔ xerox-alto, tcp ↔ bsd, and
  hollerith ↔ jacquard-loom.
- **Names, not connections (7).** These were the same thing in two
  subjects, as the proposal said:
  - the IBM 701 (dartmouth, samuel-checkers, univac);
  - the IBM 704 (samuel-checkers, perceptron, fortran);
  - Project MAC (eliza, time-sharing, multics);
  - the VAX (expert-systems, bsd, minicomputer and three more);
  - Bletchley Park (governance and the Bletchley trail);
  - Hoff (adaline, microprocessor);
  - Mead (hopfield-network, moores-law, physics-of-computation,
    lectures-on-computation).
- **Moved.** `arm → connection-machine` rests on the CM-5 heading the
  first TOP500, and that fact is in `where-computing-is`, so the
  connection is there.
- **Dropped, with the reason:**
  - lenet → Bell Labs DSP chips, tokens → Gage's BPE, logic-theorist →
    JOHNNIAC, diagrams/magnetic-moment/nobel → computer algebra,
    path-integrals-today → supercomputers, thesis → Monte Carlo, and
    appendix-f → the AP-101: no frame in Computing is about them yet.
  - lisp-collapse → connection-machine is unsourced, as sprint 006 said.
  - every-path → self-attention is an analogy, not a connection;
    path-integrals-today → next-token carries the Boltzmann link.
  - the-legend → misattributed quotations was marked weak by sprint 014.
  - eliza → arpanet: nothing connects them beyond Project MAC, which is
    now a name.
  - microprocessor → physics-of-computation: the PARC connection is
    carried by xerox-alto, and "silicon gates" alone is too thin.
  - lisp-collapse → bsd: the workstation story is carried by xerox-alto
    and free-software.
  - quantum-computers → where-computing-is: Landauer is carried by
    lectures-on-computation.

## Verification

- `just check` is green: svelte-check with no warnings, Prettier, eslint,
  and 675 tests. Every subject validates against the registry with no
  warnings, and the links between them all find their frames.
- **Negative tests, each seen failing:**
  - a connection to a missing frame: the links test fails;
  - a pair stored on both ends: the links test fails;
  - a mark on an unregistered name: the subject's validity test fails;
  - a Wikidata ID without its Q: the registry's test fails;
  - grow not handed the registry: the new grow test fails;
  - a repeated mark: the subject's validity test fails on the warning;
  - a mark removed from a reading: `names.py mark --check` exits 1.
- **Browser pass** (Playwright, headless Chromium, keyboard only, on a
  scratch data directory):
  - on `/ai/eliza`, Tab reaches the Project MAC mark, and Enter opens its
    card with focus in it. The card lists "you are here" under the AI
    subject first, then Computing's two frames, with Multics under its
    trail. Esc closes it and returns focus to the mark
    (`aria-expanded` follows).
  - Tab to Multics and Enter: `/computing/multics`, no start screen, into
    the Unix and C trail ("Main story › Unix and C"). The chip reads
    "Back to We saw ourselves in a MIRROR., The History and Current State
    of AI", and focus is on the spine.
  - After the jump, → and ← step the trail, and the narrative follows. C
    opens the contents on Multics, and B bookmarks it. The chip stays.
  - R returns to `/ai/eliza` with no chip; browser Forward brings back
    Multics and the chip; browser Back removes them again.
  - Stacking: analytical-engine → jacquard-loom → back to
    analytical-engine by its incoming connection shows "+1". The chip
    goes back one, and browser Back goes back the other.
  - Stepping the spine three frames adds no history entry.
  - No page errors or console errors, and no horizontal overflow at 390px
    with a card open or after a jump.
- **The HUD with the chip.** The first pass showed the chip pushing the
  spine's index ("04 / 05") onto three lines on the desktop, and off the
  right edge on a phone. The index no longer wraps, the HUD's corner may
  wrap, and on a phone the chip says only "↩ Back", while its accessible
  name still says where to. Checked again at 1400px and 390px: the index
  ends 24px inside the pane, as it does without a chip.

## Follow-ups

- **Phase 2 (3440)** inherits the registry, the tool and the candidates
  not built (above). Grow already refuses a mark on a name the registry
  lacks, so phase 2 has one decision to make: may grow add names, or only
  mark existing ones? That is in a comment on 3440.
- The map (phase 3, 3441) and Physics (3428, phase 4) are filed.

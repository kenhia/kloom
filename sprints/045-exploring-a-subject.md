# 045 — Exploring a subject, not learning one

## Goal

A mini-sprint at Ken's request (2026-10-03), with no korg proposal. kloom
described itself as "a timeline for learning a subject". That oversells
it: reading _In the Blood_ does not teach hematology. A subject is a series
of illustrated readings to wander through, so the description now says
"exploring a subject".

## Decisions

- **"Exploring"**, over "browsing" (too passive) and "reading about" (which
  undersells ask and grow). It fits the map, the 3D graph and the dice
  (sprint 023).
- **Changed everywhere the phrase was, not only the README.** That is the
  About page (`engine/ui/About.svelte`, which readers see), `README.md`,
  `CLAUDE.md`, `.github/copilot-instructions.md`, `skills/grow/SKILL.md`
  and ask's system prompt (`engine/ai/prompt.ts`). The prompt is the one
  change with an effect: it nudges answers slightly away from a tutoring
  tone, which is intended.
- **The GitHub description** dropped its stale "POC: History of Western
  Civilization" clause (there are ten subjects). Ken's wording: "Interactive,
  growable timeline for exploring a subject: spine scroller, narrative
  pane, AI ask/grow. Several subjects (and growing), from Western
  civilization to blood banking."

## Verified

- `just check` green. Its first run failed one vitest file, which I
  didn't capture. Three more vitest runs and a second full `just check`
  all passed, so it was a one-off failure that couldn't be reproduced, not
  this change (no test touches the edited strings).
- No other instance of "learning a subject" remains outside past sprint
  records, which describe what was true then.

## Deployed

2026-10-03, `just deploy` to the service on kai from merged `main`
(`be05f0c`, PR #52). Every deploy check passed, and the live About copy
reads "growable timeline for exploring a subject". The GitHub description
was set with `gh repo edit`. The public reader site was not published;
that waits on Ken, with sprint 044.

# 042 — Ready for readers: a home button that survives a refresh, the User's Guide, and a shorter Welcome

## Goal

korg proposal 3520, covering 3517 and 3515. Ken wanted both live on
kloom.kenhiatt.us before his dad's first sign-in on 2026-10-03. Going home
had to leave the address agreeing with the screen (3517). And a User's
Guide had to cover every control, the map and notes, linked beside Welcome,
with Welcome shortened to hand off to it (3515).

The sprint ran as a karc leg, overseen. The ship is gated on the
overseer's clearance, and Ken reviews the guide copy before then.

## Premise, checked at start

- **3517 holds.** `home()` in the subject page only set `begun = null`.
  The URL kept `/<subject>/<frame>`, so a reload re-opened the frame, and
  Back and Forward never saw home.
- **3515 holds.** There was no guide. Welcome carried the whole how-to.
  The icons were inline SVGs in six components, all but Home's, which was
  already a file in `engine/ui/icons/`.
- **Nothing pending.** `just grow-pending` listed nothing, and kloom is not
  in the cross-project plan index.

## Decisions

- **Home goes to `/<subject>`, not `/`.** 3517 suggested `/`, but `/`
  redirects to the landing subject. Home from Feynman would have reopened
  on western-civ. `/<subject>` with no frame is already this subject's
  start screen.
- **The home entry carries `page.state.home`.** Forward onto it, where no
  load runs, shows the start screen again. When the reader begins or
  returns, the entry is replaced with the frame's address and `home` is
  dropped. So Back from the reading goes to the frame they left, never to
  the start screen they already passed.
- **Home skips the unsaved-note guard.** The subject and its shell stay
  mounted, as before, so the note is still there to come back to.
- **One `Icon` component, by name.** The bookmark's fill and the gear's
  teeth are markup, not static files, so the icons became a Svelte
  component (`engine/ui/Icon.svelte`) rather than more `.svg?raw` files.
  Every HUD control and the guide draw from it.
- **The guide's keys come from `engine/keys.ts`.** It lists `FIXED_KEYS`
  and `SHORTCUTS` at their letters out of the box, so the list cannot go
  stale. A reader who rebinds a key sees their own keys in Keyboard
  shortcuts….
- **Welcome keeps Agent review whole**, word for word as approved in
  sprint 039 with "(or annotation)". Reading shrank to three lines and
  notes to two. The Finding your way and Settings and keys sections moved
  to the guide.

## The overseer's ruling, mid-flight

Comment 3401 on the proposal, from Ken: the guide explains the colors in a
section of its own: both colour settings and every choice, both brightness
sliders, and the two sides colored apart (korg 3495). Its own prose is in
American English, but controls are named exactly as labeled ("Scene
colours"), because standardizing the labels is a separate item. Both are
in, and a test holds each: every choice's label appears, and the prose,
with the labels taken out, has no British spellings.

## What shipped

**3517, Home.**

- `+page.svelte`: `home()` now navigates to `/<subject>` with
  `{ home: true }`, and an effect shows the start screen on any home entry.
  The place `replaceState` drops `home`.
- `App.PageState` gains `home`.
- `just home-check` (`create-tools/home-check/home_check.mjs`) runs in the
  machine's Playwright, like keys-check. It checks Home by keyboard, then
  `/<subject>` in the address, a reload staying home, Back to the frame,
  Forward home again, and Begin back to a frame address with Back staying
  in the reading.
- Result: 11/11 with the fix. Against the previous page, 8 of 13 checks
  fail.

**3515, the User's Guide and Welcome.**

- `/guide` in both editions, behind sign-in in the reader edition like
  every page. It is linked from the start screen (a `guide` prop beside
  `help`) and from Welcome, at the top, at the buttons and under Help.
- Sections: the start screen, the buttons, reading, contents, the map,
  bookmarks, notes and annotations, Agent review, About (with Suggest a
  subject), settings, the keyboard, phones and tablets. Asking and growing
  appears in the full edition only. Signing in and out appears only for a
  signed-in reader.
- `engine/ui/Icon.svelte`; the inline SVGs in Shell, Contents, Bookmarks,
  MyNotes, Settings and About are replaced by `<Icon>`.
- Tests: `src/routes/guide/guide.test.ts` covers these:
  - every icon, rendered alone, is found in the guide
  - every control's name appears
  - every shortcut and fixed key appears
  - the Agent review statement appears
  - every in-page link has a heading
  - the shared-login wording
  - the editions

  Welcome's test now checks the hand-off. The start screen's test checks
  the guide link comes after Welcome.

- Negative-tested: dropping the About icon and renaming a heading's id
  each failed their test.

## Verified

- `just check` green: 1401 tests and a clean reader-gate.
- `just home-check` 11/11, `just keys-check` 70/70, `just colours-check`
  92/92, all against the dev server on kai.
- Screenshots of `/guide` at 1280×800 dark and 390×844 light: icons drawn
  and no console errors. The HUD was screenshotted and its icons are
  unchanged.
- The reader build serves `/guide` without the Asking and growing section.

## Repaired in passing

- The `.icon svg` size rules in Bookmarks and MyNotes would no longer have
  reached an SVG drawn by a child component. svelte-check flagged them, and
  they are now `.icon :global(svg)`. Gate: svelte-check.

## Follow-ups

None filed.

## Deployed

On 2026-10-03 (23:30 PDT on the 2nd), from merged `main` `b8a19f8`
(PR #49) on kai, under overseer clearance (comment 3403). Every probe ran
from kai.

- **The kai service** (`.sprint-deploy`, `recipe: deploy`): `just deploy`.
  `just verify` passed all ten checks and printed `deployed b8a19f8c2`,
  library `2026-10-03T06:30:25.074Z 7a1297`. On the ssh door, `/guide`,
  `/welcome` and `/western-civ` answered 200. Each carries its guide
  links (`./guide`, since SvelteKit writes relative paths), and `/guide`
  has its Colors section.
- **The public site:** `just publish-public`, release **v5**, image
  `registry.fly.io/kloom-reader:b8a19f8c2-202610030630`, library
  `2026-10-03T06:30:40.669Z b21b9f`. `verify-public` passed every check
  inside the publish and again when run alone (`note 0 notes, 0 detached`).
  For a stranger, `/guide` answers `303` to `/signin?next=%2Fguide`.
- **Signed in on the public site**, as the throwaway `kloom-verify`
  reader (enabled, invited and signed in, then disabled again with 0
  sessions; `jkh` untouched, still "invited, last seen never"):
  - `/guide` answered 200, with the Colors section, 21 icons drawn, no
    "Asking and growing", and the sign-in section.
  - `/western-civ` answered 200 and links to the guide once.
  - `/welcome` answered 200 and links to the guide three times.

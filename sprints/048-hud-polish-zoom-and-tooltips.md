# 048 — HUD polish: zoom drawing and fast tooltips

## Goal

korg proposal 3541, covering korg 3540 and 3539. Ken raised both on
2026-10-03. The first: a frame's drawing is too small in the scene to read its
detail, and he wants to see it bigger. The second, which he noticed while
asking for that: HUD tooltips take about two seconds to appear, and the
Bookmarks list icon has none at all. The proposal put the tooltips first, so
the new zoom icon would use the new pattern rather than add one more `title`.

## Premise check

Both premises held at the start. Every HUD tooltip was a native `title`
(Shell, StartScreen, Contents, MyNotes, BackChip, Bookmarks). The Bookmarks
list button (`Bookmarks.svelte:60-71`) had no `title`, only its visually
hidden "Bookmarks (N)" label.

## Tooltips (korg 3540)

- **One action, `use:tooltip={text}`** (`engine/ui/tooltip.ts`). Its timing
  and placement are pure and tested (`engine/tooltip.ts`). A single tooltip
  element serves the page.
- **Timing.** It shows after 400 ms of hover. The next control along shows
  at once while a tooltip is showing or has hidden within the last 600 ms,
  which is how native toolbars feel when the pointer runs along them. It also
  shows on keyboard focus (`:focus-visible`), never on touch.
- **WCAG 1.4.13.** Esc hides it. That Esc is consumed (`preventDefault` in a
  capture listener), so hiding a tooltip does not also leave a trail. The
  pointer can move onto the tooltip within 120 ms and keep it. It hides on
  blur, on a press, and on Enter or Space.
- **It is `aria-hidden`.** The control's name is still its visually hidden
  label, so a screen reader no longer hears the label twice.
- **`IconButton` takes a `tip`** and defaults to its `label`. The gear, Home
  and About therefore gained tooltips too: they had none before. No HUD
  control carries a `title` now. Content keeps its own titles (charts and
  images in a reading, the spine's ticks).
- **Colors are read off the control when the tooltip shows** (`--ink` on
  `--background`). The tooltip therefore inverts whichever palette it sits
  in, scene or reading, dark or light.

## Zoom drawing (korg 3539)

- **The icon was Ken's pick.** Three candidates were offered (expand corners,
  a picture with an arrow, fullscreen brackets), rendered at HUD size and
  72px in both modes. He chose **expand corners**. A magnifying glass stays
  reserved for search.
- **A modal `<dialog>`** (`engine/ui/ZoomDrawing.svelte`) fills the whole
  viewport. It uses the scene's palette (`--line` on `--background`), so
  the drawing looks as it does in the scene, only larger. The aspect ratio
  is kept, and the drawing shows whole: the scene's draw-on animation is
  scoped to `.illustration`, so it does not run here.
- **Ways to close it:** Z again (the reader's binding, Shift let off as the
  page keys do), Esc (the dialog's own), the ×, or a click beside the
  drawing. Focus goes back to wherever it was when the dialog opened: the
  spine for Z, the button for a click.
- **`zoom` joins the keymap** (`SHORTCUTS`, default `z`). A stored keymap
  falls back to the defaults for an unknown action, so nothing needed
  migrating. Z is scoped like every character key: the AI box types it.
  Inside the dialog, the page keys stand down (`data-own-keys`).
- **Decided: no stepping while zoomed.** Stepping frames with the dialog
  open was optional in the work item. It would need the arrows to act inside
  a modal, which makes it more than a dialog. Left out.
- **No drawing means unavailable, not removed.** Every frame has a drawing
  today (616 of 616), but `illustration` is optional and a frame's body can
  still be on its way. In either case the button is `aria-disabled`. It stays
  focusable, and its tooltip says "this frame has no drawing". Z does
  nothing.
- **The label.** The work item asked to reuse the illustration's alt text,
  but a scene drawing has none: it is decorative (`aria-hidden`) in the
  scene. The dialog is named "Drawing: <topic>" instead.
- **"Chart frames."** The scene drawings with labels (the AI subject's
  diagrams, e.g. `ai/alexnet`) stand in for the work item's chart frames.
  Charts inside a reading are content, not the frame's drawing, and are out
  of scope.

## Checks

- `just hud-check` (new, Playwright, not part of `just check`), 131 checks:
  - no HUD control has a `title`;
  - every HUD icon shows its tooltip on hover, the first one between 200 ms
    and 1 s, each one after it within 250 ms;
  - the Bookmarks list shows "Bookmarks (N)";
  - focus shows the tooltip, and Esc hides it while leaving focus and the
    page where they were;
  - Z/Z and Z/Esc round trips on a line-art frame and a labelled diagram, in
    dark, light and 390×844, with the drawing filling the screen and focus
    restored;
  - the button and the ×, and a backdrop click;
  - Z typed into the AI box;
  - a frame whose drawing is stripped from `/api/frame`: the button is
    marked unavailable, and its tooltip says so.
- **Negative-tested.** I planted a 2 s delay, a `title` back on Contents, and
  a zoom key that did not close the dialog. The check failed on each one
  (82/120, then the titled and too-slow controls by name). All the plants
  were reverted.
- The page's SSR tests found HUD buttons by `title`. They now find them by
  their accessible name (`buttonNamed`), and assert Zoom drawing's place
  between Map and What's new.
- `just check`, `reader-gate`, `scene-fit` (0 misfits in 616 frames at three
  sizes, with the extra icon), `keys-check`, `home-check`, `start-fit` and
  `colours-check` all pass.

## Docs

- docs/design.md: new §Tooltips and §Zoom drawing; Z added to §Interaction;
  the icon list under §User's Guide.
- The User's Guide: Zoom drawing among the buttons, and a line on how to see
  a button's name.

## Repaired in passing

- **The bookmark toggle's tooltip hard-coded "(B)"**, which was wrong for a
  reader who had rebound or turned off the key. Bookmarks now takes the
  reader's key from the shell, as Contents and My notes already did.
- **CLAUDE.md's status paragraph was missing sprint 047.** Added beside 048.

## Deployed

2026-10-04, to the service on kai, by `just deploy` (`.sprint-deploy`'s
`recipe: deploy`) from merged `main` at `59072beb` (PR #55):

- **The deploy's own verify:** all ten checks `ok` (both doors, write
  gating, reader-data and notes gating, library bodies, compression).
  `DEPLOYED` reads `59072bebc`.
- **This sprint's work, checked live:** `hud_check.mjs --url
  http://127.0.0.1:4891` (the ssh door, which carries a reader) passed
  131/131. That covers the tooltips (no HUD `title`, the delay, along the
  row, focus, Esc, Bookmarks (N)) and Zoom drawing (Z/Z and Z/Esc in dark,
  light and at phone size, the button, the ×, the backdrop, the AI box, a
  frame with no drawing).
- **Against the tailnet door (:4890) the check stops at the Bookmarks
  step.** An anonymous browser there has no reader, so there are no
  bookmarks, and the check expects a reader's page.
- **The public reader site was not published.** That is `just
  publish-public`, run separately.

# 007 — Service on kai: tailscale serve, tailnet identity, a content clone

## Goal

korg proposal 3416, first in the 2026-09-28 plan. It covers two work items:

- korg 3388: run kloom as a service on kai. It binds loopback, `tailscale
serve` is the only network ingress, and ask, keep and grow are gated on
  the tailnet identity. The ssh-loopback path stays open for kwork demos.
  This implements Ken's decision on 3384: option (b), with (a) kept.
- korg 3412: the service grows into a content clone it owns and pushes a
  branch, never into the dev checkout, and a PR brings grown content back.

Identity comes first because it is the author of every reader-data row
later (3413 onward).

## Decisions

- **Premises held.** Nothing was authenticated, the dev server bound
  127.0.0.1, and `applyGrowth` committed into whatever repository
  `subjects/` was in. kloom is not in the cross-project plan index.

### Who may write (3388)

- **Serve's header behaviour was measured, not assumed.** A throwaway
  `tailscale serve` on :18999 fronted a header-echo server on tailscale
  1.102.4, and was removed afterwards.
  - A forged `Tailscale-User-Login`, in either case, never reached the
    backend: serve strips it.
  - kai is `tag:server`, so its requests arrive with no identity at all.
  - A request made straight to the loopback port kept the forged header,
    so the trap in 3388 is real.
- **Two loopback doors, as 3388 proposed.** `serve.js` runs the adapter-node
  handler on :4890 (behind serve) and :4891 (for ssh forwards). A TCP port
  rather than a unix socket for the ssh door: `ssh -L port:127.0.0.1:port`
  is the ordinary form, and `-J` through a homelab host works unchanged.
- **The door mark carries a per-process key.** `serve.js` overwrites
  `x-kloom-door` on every request with a key made at start plus the door.
  The hook trusts no mark without the key. So a `node build` or
  `vite preview` run outside `serve.js` reads but never writes. Only
  `vite dev` is trusted without a mark, as before. A mark alone would have
  depended on every entry point remembering to strip it.
- **The gate is by method, not by route.** Any request that is not
  GET/HEAD/OPTIONS needs a reader. That covers ask, keep and grow, and fails
  closed for whatever is added next. The 401 carries a JSON `message`, which
  the AI pane already shows, so the UI needed no change for it.
- **The ssh door's reader is the host user** (`user@host`, or
  `$KLOOM_LOCAL_LOGIN`), `via: ssh`. Identity headers there are ignored, since
  reaching the port took an ssh login on kai.
- **The reader is on the grow job and is the commit's author.** The
  committer stays `kloom grow`, and a `Requested-by:` trailer names the door
  it came through. A name that serve MIME-encodes (non-ASCII) falls back to
  the login.

### The content clone (3412)

- **Branch policy: one long-lived `grow/<host>`.** Jobs build on each
  other, so per-job branches would need rebasing against each other anyway.
  The branch belongs to the service, and review edits go into the merge or
  onto main afterwards.
- **Picking up merged main happens at start, and a deploy is a restart.**
  No timer. The sync fast-forwards, leaves grown work that is ahead alone,
  resets after a squash or rebase merge, rebases an unmerged tail, and
  leaves a conflicting clone as it was ("diverged"). The squash case is
  detected by content: some commit on main holds every grown path exactly
  as a grow commit left it. That still matches after main edits those files
  further. A plain `git rebase` would conflict on `spine.json` there. Ten
  tests cover it against real repos, and the plain-rebase fallback was
  planted as a regression and caught.
- **Push credential: none new.** The service runs as ken, whose GitHub
  ssh key already pushes this repo, and grow's `claude -p` already runs as
  that user with the same reach. A deploy key would have added a secret
  without narrowing anything, so there was nothing for krot.
- **Deploys don't touch the clone.** `just deploy` builds, rsyncs the build
  and what grow reads at run time (the skill, its references, the Prettier
  config) into `~/.local/share/kloom/app`, runs `npm ci` there when the lock
  changed, and installs and restarts the unit. It includes dev dependencies,
  because grow formats with Prettier and its Svelte plugin. Measured: the
  grown files came out Prettier-clean even though the clone has no
  `node_modules`.

### Cross-repo

- k-homelab, branch `kloom-007-serve-4890` on kubs0: the `tailscale_serve`
  :4890 entry in `manifests/kai.yml`, and a `changelog-kai.md` entry. The
  serve entry was created on the host with `tailscale serve --bg`, so the
  declaration and the state match. `bin/audit kai tailscale-serve` reports
  `ok`, and k-homelab's `just check` passes. The unit belongs to this repo's
  deploy, as kfdc's did. PR: k-homelab#112, open for Ken to merge. The kubs0
  checkout was put back on `main` afterwards.

## What shipped

- `serve.js`, the production entry: two doors and the door key.
- `src/lib/server/reader.ts` (door, reader, write test) and the
  `src/hooks.server.ts` `handle` gate, with `App.Locals.reader`.
- `src/lib/server/content.ts`: `syncContent` at start, `pushGrowBranch` after
  a grow, and a grow refused off the branch. A failed push is recorded on
  the job (`result.pushError`), and the AI pane says "not yet pushed".
- `GrowJob.by`, the commit author and the `Requested-by:` trailer.
- `deploy/kloom.service`, and the `just content-init`, `just deploy` and
  `just verify` recipes.
- Docs: `docs/deploying.md` (new), and `docs/design.md` §Who may write and
  §The content clone.

## Verified live (kai, 2026-09-28)

- **From cleo over ts.net:**
  - a read of `/api/grow` and the page returned 200;
  - an ask streamed an answer;
  - a grow job (Faraday and induction, anchored on Maxwell) ran on Opus
    5.5 to commit `9c25d40` on `grow/kai`, authored
    `Ken Hiatt <ken.hiatt@gmail.com>` and committed by `kloom grow`, with
    `Requested-by: … (tailscale-serve)`, and pushed.
- **A POST over ts.net from kai** (tagged, so no identity) returned 401.
- **`ssh -L 15891:127.0.0.1:4891 -J kubs0 kai`** served the page and
  answered an ask about the new frame. kwork itself was out of reach, so
  this is the same path run from kai.
- **Redeploying the app left the clone alone.** See Deployed.

## Repaired in passing

- `just --list` showed `check` as "included: every subject under subjects/
  is loaded…", because just keeps only the last line of a two-line doc
  comment. The comment now lists as "Run type checks, formatting/lint
  checks and unit tests".

## Follow-ups

- The grown Faraday frame is waiting on `grow/kai` for Ken to review in a
  PR. It is the first real use of the way back.

## Deployed

- **2026-09-28, kai**, from this branch with `just deploy`:
  - first at `4f12268`;
  - then at `4a1ed1b` after the docs commit, a redeploy made to prove the
    clone is left alone.
- `kloom.service` is enabled and active. `tailscale serve` :4890 was added
  on the host, and the k-homelab declaration is in PR #112.
- `just verify` passes after each deploy: both doors read, the tailnet door
  answers an anonymous write with 401, and the ssh door lets a write
  through.
- Across the redeploy the content clone stayed at `9c25d40`, clean, and the
  start-up sync logged "grow/kai has 1 grow commit(s) waiting for a PR".
- The deploy after the merge should run from `main`, so that `app/DEPLOYED`
  names a commit on main.

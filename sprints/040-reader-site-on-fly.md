# 040 — The reader site on Fly.io: the image, fly.toml, and the publish, verify, invite and pull-notes recipes

## Goal

korg proposal 3506, covering 3503. This is the second slice of program
korg 3508, the public reader site. It packages sprint 039's reader edition
for the Fly app `kloom-reader` and publishes it at
<https://kloom.kenhiatt.us>. DNS, the cert, the app and its IPs were
already in place (3458 comments 3375–3377).

The sprint ran as a karc leg, overseen. The overseer's notes (comment 3387) wrote two stops for Ken into its path:

1. After the first publish and a green `verify-public`, Ken looks at the
   live site himself, signed in as a throwaway reader, `kloom-test`.
2. Ken's parents' invite runs only once Ken has said so, and Ken sends
   the link. Ken named the login `jkh`, display name "Joel and Kathy"
   (planned as J-n-K until then).

## Premise, checked at start

- **Holds.** The reader edition builds into `build-reader/`, and
  `KLOOM_EDITION=reader node serve.js` listens on 8080. `admin.mjs` opens
  `accounts.ts` and `sqlite-reader-store.ts` with plain Node 24.
- **Fly.** The app, IPs and cert were in place, with no machines, volume or
  tokens.
- **Nothing pending.** No grown content was waiting (`just grow-pending`),
  and kloom is not in the cross-project plan index.

## What shipped

**`publish.json`** lists the public subjects: all ten, by Ken's call. A
subject is held back by taking it out of the list.

**`just stage-public`** (`deploy/stage-public.mjs`) compiles the listed
subjects from this checkout into `build-public/content.db`, with `HEAD` as
its source, and copies exactly the media files that library lists into
`build-public/media/`. That is 1,407 files: 95 MB of media and a 32 MB
library. `compileContent` gained `only`: a library built from a list holds
nothing else, and a listed subject that is not on disk is refused.

**`Dockerfile`** has three stages on `node:24-slim`:

- the reader edition, built from source, with the commit passed in as
  `KLOOM_BUILD`, since the build context has no `.git`. `vite.config.ts`
  now reads that variable before asking git.
- production `node_modules`, because adapter-node leaves `dependencies`
  out of its bundle
- the runtime: `serve.js`, `admin.mjs` and its two modules, the build, and
  then the media and `content.db` as the last two layers

`.dockerignore` keeps the context to source and the staged library (98 MB).
The image is 648 MB. It runs as root, because Fly mounts the volume at
`/data` owned by root.

**`fly.toml`** sets up `kloom-reader` in `iad`:

- `shared-cpu-1x` with 512 MB, always on (`min_machines_running = 1`,
  auto-stop off)
- `force_https`, and a health check on `/robots.txt`, the one path open
  without a session
- `ORIGIN` and `KLOOM_PUBLIC_URL`
- the volume `kloom_data` (1 GB, created this sprint) at `/data`

**Recipes**, each through `deploy/fly.sh`. That script runs flyctl by full
path with `FLY_API_TOKEN` taken from kai's secrets file, in the
environment and never on a command line.

- **`publish-public`** refuses anything but a clean `main` equal to
  `origin/main`. It stages, deploys with `--local-only`, runs
  `verify-public`, and appends the release, image, commit and library to
  `~/.local/share/kloom/public/publishes.log`.
- **`verify-public`** has 18 checks (docs/deploying.md §Publishing). It signs
  in as `kloom-verify`, which each run re-invites with a random password and
  disables at the end.
- **`invite`, `readers` and `disable-reader`** run `admin.mjs` on the machine
  through `fly ssh console`.
- **`pull-notes`** takes `node:sqlite`'s backup on the machine, fetches it
  with sftp to `public/reader-YYYYMMDD-HHMM.db` (mode 600, directory 700),
  and removes the copy on the machine.

**The deploy token** is `kloom-publish-kai`, scoped to the app. It was
minted on kai straight into k-homelab's age store, then distributed to kai
as `FLY_API_TOKEN` and registered in krot. See Cross-repo changes.

**HSTS** (overseer finding, Ken approved). Every response from the reader
edition's hooks says `Strict-Transport-Security: max-age=31536000`, without
`includeSubDomains`, because kenhiatt.us has other hosts. The sign-in
redirect is now returned rather than thrown, so it carries the header too.
Static assets (`/_app/immutable/…`) are served by adapter-node's file
handler before the hooks run, so they do not; a browser takes the policy
from the first page it loads.

**Docs.** `docs/deploying.md` has a new §Public reader site.

## Decisions

- **The image is built on kai** (`--local-only`), not by Fly's remote
  builder. Only changed layers are pushed, so a content-only publish
  pushes the library and media layers alone. kai has Docker.
- **verify-public signs in for real.** Anonymously, every path but
  `robots.txt`, `/signin` and a welcome link answers 401 or a redirect. So
  "ask, grow and keep are 404" can only be checked with a session. A
  dedicated reader, disabled between runs, keeps that off anyone else's
  account.
- **The `Fly-Client-IP` check, as the overseer asked.** It sends up to 21
  wrong passwords, each under a fresh username and a made-up
  `Fly-Client-IP`. If the proxy passed a client's header through, nothing
  would wait. It does wait, because every try counts against kai's real
  address. The cost is that sign-in from the house waits 30 seconds after a
  verify.
- **A plain form POST answers 200 whatever the action returns.** The check
  therefore asks the way the page's script does (`x-sveltekit-action`) and
  reads the action's status. My first version read the HTTP code, always
  saw 200, and failed for that reason. See Verified.
- **The first publish came from the branch, not `main`.** `publish-public`
  refuses a branch, and `main` cannot hold the Dockerfile until this ships.
  So the first deploy ran the recipe's own steps by hand from commit
  `db6fd5e`: `stage-public`, `deploy/fly.sh deploy --local-only`, then
  `verify-public`. Its content is `main`'s (`5360123`); no subject changed
  on the branch. The first `just publish-public` from `main` runs at ship,
  and it writes the first line of `publishes.log`.

## Verified

- **`just check` is green.** That covers svelte-check, lint, 1372 tests
  (new: `compileContent`'s `only`, and HSTS on every hook response), tools tests, the reader gate and the
  mark check.
- **The image, locally** (Docker on kai):
  - an anonymous `/` gets a 303 to `/signin`, and `robots.txt` disallows
  - `admin.mjs invite` inside the container makes a link, and the link
    signs in
  - signed in, `/api/stats` is 200 with a build, and pages go `br`
  - a POST to ask, grow or keep is 404
- **Live, `just verify-public`: 18 of 18 ok** after the HSTS redeploy
  (image `18e8259bb-202610030525`), every probe run from kai:
  - TLS verifies; http goes to https (301)
  - HSTS on `robots.txt`, on the way to sign in, and on a reader's page.
    Negative test: before that deploy, the live site sent no HSTS on
    either of the first two, which those checks would have failed.
  - `robots.txt` disallows
  - a stranger gets a 303 to `/signin`, a deep link comes back with
    `next`, and the API returns 401
  - the welcome link signs in
  - ask, grow, keep and kept answers are 404
  - pages go `br`, and a frame's body is 200
  - the library names its build
  - Fly overwrites `Fly-Client-IP`
- **`Fly-Client-IP`, measured both ways:**
  - With kai's address already waiting, spoofed `fly-client-ip` and
    `Fly-Client-IP` headers were both answered 429, the same as no header.
  - **Negative control**, against the image on kai with no proxy in front:
    21 tries under 21 spoofed addresses never waited, while 21 under one
    address waited at try 21. So the check can fail, and it fails on
    exactly the case it exists for.
- **`just pull-notes`** fetched an 84 KB copy in 9 s.
  `review-notes.mjs --data <dir> list` read it ("No flagged notes").
- **`just readers`** lists `kloom-verify`, disabled.

## The invite

Ken looked at the live site as `kloom-test` and said it was OK. On his
word, `just invite jkh "Joel and Kathy"` ran on 2026-10-03 at 05:26 UTC.
The link is good once until 2026-10-10 05:26 UTC, and Ken sends it
himself. `kloom-test` stays in place: slice 3507 uses one for its round
trip and deletes it.

## Repaired in passing

- **`fly ssh console` hung at `Connecting to fdaa:…`** with both the token
  and Ken's login. kai's WireGuard peer for org `personal` had gone stale.
  While I was looking, I printed `~/.fly/config.yml`, which put that peer's
  private key into this session's transcript. I removed the peer
  (`fly wireguard remove`), which retires the leaked key, and flyctl made a
  new one. ssh has worked since. docs/deploying.md says how to spot the
  stale-peer case.
- **k-homelab's khomelab-secrets key table** was missing kai's
  `OPENALEX_API_KEY` row. I added it with `FLY_API_TOKEN` (PR #114).
- **docs/deploying.md** named the shared login `J-n-K`; it is `jkh`.

## Cross-repo changes made

This is the documented token procedure (overseer comment 3387, Branch A).
k-homelab's `recipes/khomelab-secrets/README.md` (§Rotating a value) and
the krot-register skill were followed.

- **k-homelab** (on kubs0), branch `kloom-fly-deploy-token`, **PR #114,
  open**:
  - the store entry `fly-deploy-token-kloom-reader`, minted with
    `fly tokens create deploy` straight into `bin/secret set`, and never
    echoed
  - its `secrets/index.yml` entry, with a probe (`bin/secret verify`: ok,
    negative control refused)
  - `FLY_API_TOKEN` in `manifests/kai.yml`
  - `bin/apply kai khomelab-secrets` has been applied, and `just check` is
    green

  The merge was refused by karc's gate (not the ship turn), so it waits
  for the ship. kubs0's clone is back on `main`. Until the PR merges, an
  apply of khomelab-secrets on kai from `main` would drop the key.

- **krot** (on kai) `registry/fly.toml` is committed and pushed to `main`:
  - `just check` is green
  - `check --manifests` was run against the PR branch's manifests: 0 errors
  - `scan` is clean, and the fingerprint was taken on kai

## Follow-ups

None filed.

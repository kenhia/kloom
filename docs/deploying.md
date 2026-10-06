# Running kloom as a service

kloom runs on kai as a systemd user unit, `kloom.service`. The design is in
[design.md](design.md) §Who may write and §The content clone. This page is
the operations side. The public site's build, the reader edition, and its
sign-in are at the end (§Editions, §Signing in), and the public site itself
after them (§Public reader site).

| What                  | Where                                                            |
| --------------------- | ---------------------------------------------------------------- |
| Tailnet URL           | `https://kai.encke-wahoo.ts.net:4890`                            |
| ssh door              | `127.0.0.1:4891` on kai, for `ssh -L`                            |
| App (the deploy copy) | `~/.local/share/kloom/app`                                       |
| Content clone         | `~/.local/share/kloom/content`, on `grow/kai`                    |
| Grow jobs             | `~/.local/share/kloom/data`                                      |
| The library (SQLite)  | `~/.local/share/kloom/data/content.db`, built from the clone     |
| Reader data (SQLite)  | `~/.local/share/kloom/data/reader.db` (with `-wal`, `-shm`)      |
| Ask's API key         | `ANTHROPIC_API_KEY` in `/etc/khomelab/secrets.env`, read per ask |
| Ask's cost log        | `ask_cost` in `reader.db`; `just ask-costs`                      |
| Unit                  | `deploy/kloom.service`, installed to `~/.config/systemd/user/`   |
| Serve entry           | k-homelab `manifests/kai.yml`, `tailscale_serve` port 4890       |

## First time on a host

```sh
just content-init    # clone origin into ~/.local/share/kloom/content, on grow/<host>
just deploy          # build, copy, install and start the unit, then `just verify`
sudo tailscale serve --bg --https=4890 http://127.0.0.1:4890
```

Declare the serve entry in k-homelab's manifest for the host too, or a
rebuilt host comes back without the URL. The unit needs lingering on for the
user, and a logged-in Claude Code at `~/.local/bin/claude`, which grow and
ask run as the host's user. The API models of ask (sprint 046) need the key in the host's
secrets file (k-homelab store entry `anthropic-api-key`, the host's
manifest, `bin/apply <host> khomelab-secrets`). The app reads that one key
per ask, so it needs the unit's user in the `khomelab` group, and no
restart after a rotation. `claude -p` never sees it.

## Deploying new app code

From a clean checkout of the commit to ship (normally `main`, after a merge):

```sh
just deploy
```

It refuses a dirty tree, because the app copy records the commit it came
from (`app/DEPLOYED`). It re-runs `npm ci` only when `package-lock.json`
changed, and it never touches the content clone. The restart makes the clone
pick up merged main (below), then build the library from it. `just verify`
checks both doors, that the tailnet door refuses an anonymous write, that
reader data answers only a reader, that a frame's body comes from the
library and that pages go compressed, and names the library's build.

`reader.db` holds every reader's places, bookmarks, notes (annotations
among them) and kept answers. It is the one piece of state that is not
rebuildable from git. Copy it with the unit stopped, or with
`sqlite3 reader.db ".backup copy.db"` while it runs. One reader can also
save their own from the bookmark list (_Export my reading data_).
Design: [design.md](design.md) §Reader data.

Kept answers were files under `data/<subject>/kept/` before sprint 011. A
start moves any it finds into `reader.db`, under `KLOOM_KEPT_OWNER` if the
unit sets it, else the host's own reader (`user@host`), and leaves each file
in `kept-migrated/` beside it. The journal says how many moved. kai had none
when that shipped.

Flagged notes are worked through with the review-notes skill, from a
checkout: `node skills/review-notes/review-notes.mjs --data
~/.local/share/kloom/data list` (`skills/review-notes/SKILL.md`).

`content.db` is the served library ([design.md](design.md) §Serving). It
is derived from the content clone and can be deleted at any time: the next
start, or the next read, builds it again. The service builds it at start
and after every grow; a hand edit in the clone shows after a restart. A
subject in the clone that fails validation keeps being served as it was
last built, and the journal names its problems.

`journalctl --user -u kloom` shows the doors, a `content:` line saying what
the start-up sync did, and another saying which subjects the library built
and how long it took.

## Bringing grown content back

Grow commits to `grow/kai` and pushes it. Grown content reaches main only
through review (korg 3442): `skills/review-grown/SKILL.md` cherry-picks the
pending grow commits onto a review branch from `main`, checks and repairs
them, and squash-merges a PR whose message ends with a
`Grow-reviewed: <tip sha> (grow/kai)` trailer. Every sprint runs
`just grow-pending` first, and reviews whatever it lists. The next restart
(`systemctl --user restart kloom`, or the next deploy) sees what main has,
the trailer included, and resets the branch onto it. That holds even when
the review repaired the grown files. Never push review edits to `grow/kai`:
that branch is the service's.

If the journal says the clone **diverged**, main and the unmerged grow
commits conflict, and the clone was left serving as it was. Resolve it by
hand in `~/.local/share/kloom/content`: rebase `grow/kai` onto `origin/main`
and push with a lease. Then restart the unit.

## Demos from kwork (off the tailnet)

kwork can ssh to homelab hosts, and the ssh door trusts whoever reached it
that way:

```sh
ssh -N -L 4891:127.0.0.1:4891 -J <homelab host> kai
# then open http://localhost:4891
```

Ask and grow work there, and a grow is authored as the host's user
(`ken@kai`).

## Editions

kloom builds as one of two editions (korg 3500). The build picks one, and
the build is the whole of the difference.

| Edition  | Build                                 | Who reads it                     | Listeners (`serve.js`)                |
| -------- | ------------------------------------- | -------------------------------- | ------------------------------------- |
| `full`   | `just build` → `build/`               | Ken and the tailnet, on kai      | the two loopback doors above          |
| `reader` | `just build-reader` → `build-reader/` | invited readers, the public site | one, `0.0.0.0:$PORT` (8080), no doors |

The **reader edition** has no grow and no `claude -p`. Since sprint 046
(korg 3530) it has **ask and keep on the Claude API, for the readers Ken
allows** (docs/design.md §Ask on the reader site); for everyone else the ask,
keep and kept-answer routes answer 404, and the page offers no AI pane. What
it lacks is **stripped, not switched off**: `KLOOM_EDITION=reader` at build
time points the `$edition` alias at `src/lib/edition/reader/`, whose
`providers` module builds the API provider only and imports none of
`claude -p`, and `__KLOOM_EDITION__` lets the shared code drop the rest (the
AI pane's grow requests, the library build). The grow route is still there
and answers 404. `just reader-gate`, part of `just check`, builds it and
fails if the build holds `claude -p`'s adapter, an import of
`node:child_process`, grow, or editor-only code, or if the browser's code
holds a grow request. It checks by category, through markers, and a marker
that is no longer in its source fails the gate too. **A new editor-only
feature goes behind `$edition` and gets a marker there.**

The reader edition never builds its library and has no content clone. It
reads:

| Variable             | What                                                                 |
| -------------------- | -------------------------------------------------------------------- |
| `KLOOM_CONTENT_DB`   | the library, built elsewhere and opened read-only                    |
| `KLOOM_MEDIA_DIR`    | media, laid out as the subjects are (`<subject>/frames/<frame>/…`)   |
| `KLOOM_DATA_DIR`     | where `reader.db` is: readers' accounts and data                     |
| `ORIGIN`             | the site's own URL; SvelteKit's origin check needs it behind a proxy |
| `PORT`, `HOST`       | the listener (8080 on 0.0.0.0)                                       |
| `KLOOM_LOGIN_DOMAIN` | readers' logins are `<username>@` this (`kloom.kenhiatt.us`)         |
| `KLOOM_CONFIG`       | the app config: `kloom.reader.json` (ask's models, prices and caps)  |
| `ANTHROPIC_API_KEY`  | the Claude API key ask uses: the Fly secret, never in the image      |

To run it on kai as the public site runs it, on loopback, against this
checkout's library and media and `data/reader.db`:

```sh
just build-content
just admin invite ada "Ada" --base http://127.0.0.1:8080   # prints a welcome link
just serve-reader                                           # then open the link
```

## Signing in

The reader edition is invite only (korg 3501). Every page needs a signed-in
reader, reads included, and a page asked for without one goes to `/signin`
and back after. `robots.txt` disallows everything, and every response says
`X-Robots-Tag: noindex`. The content is public on GitHub anyway; the site is
for the people Ken invites.

- **Accounts are logins, not people.** Two people may share one, as Ken's
  parents do (`jkh`). A reader has a username (typed, case-insensitive,
  `[A-Za-z0-9-]`), a display name (shown), and a store login,
  `<username>@kloom.kenhiatt.us`, which keys their data. A public reader
  never meets a tailnet login (`ken@github`) when notes come back to be
  reviewed. Notes, bookmarks and places are private to the login.
- **Welcome links.** `admin.mjs invite` mints a token of 32 random bytes and
  prints `/welcome/<token>`. Only the token's sha256 is stored. The link
  works once and for 7 days. Opening it only shows the form, so a message
  app's preview does not use it up. Choosing a password uses it, signs the
  reader in and lands them on the Welcome and How-To page (`/welcome`).
- **Reset is a new link.** Inviting a reader who has a password voids their
  password, their earlier links and every session, so the new link is the
  only way in. Ken texts it; there is no email.
- **Passwords** are scrypt (`node:crypto`), with a salt each, at least 8
  characters. No dependency was added.
- **Sessions** are a random id in a cookie, `kloom_session`: `HttpOnly`,
  `Secure`, `SameSite=Lax`. Only its sha256 is stored, so a copy of
  `reader.db` signs nobody in. A session lasts a year from its last use.
  "Sign out" on the start screen ends this session only.
- **Backoff.** Wrong passwords are counted per username and per address
  (`Fly-Client-IP` when present), in memory. After 5 for a username (20 for
  an address), the next try waits 30 seconds, doubling to 15 minutes.
- **CSP** comes from `kit.csp`, in the reader edition only. Scripts are
  `'self'` and SvelteKit's hashed inline script; styles allow inline, for
  the shell's palette and pane sizes. SvelteKit's origin check stays on.

### The admin CLI

The site has one admin page, the traffic grid (`/admin/traffic`,
docs/design.md §Traffic), and nothing on it administers. Everything that
changes something is `admin.mjs`, run where `reader.db` is, with plain Node
24, through the accounts module, the reader store, the ask ledger and the
admins module. On Fly it runs through `fly ssh console -C`, so Fly's own
sign-in is the admin's.

```sh
node admin.mjs add <username> <display name>      # no password until their link
node admin.mjs invite <username> [display name]   # prints the link; adds them if named
node admin.mjs disable <username>                 # their sessions end
node admin.mjs enable <username>
node admin.mjs list [--json]                      # status, last seen, sessions
node admin.mjs delete <username> --yes            # the account and everything they wrote
node admin.mjs flagged [--reader R] [--json]       # notes flagged for Agent review, readers named
node admin.mjs handle-note <reader> <id> <response> [--seen UPDATED]
node admin.mjs handle-notes '<JSON list>'          # several answers in one call
node admin.mjs detached [--library FILE] [--json]  # notes whose frame or words are gone
node admin.mjs suggestions [--status S] [--json]   # subjects readers suggested
node admin.mjs mark-suggestion <reader> <id> new|planned|written|declined
node admin.mjs reader-ask enable|disable <reader> [--cap USD]
node admin.mjs admin enable|disable <reader>       # who may see /admin/traffic
node admin.mjs admin list [--json]
```

**Admins** (sprint 054, korg 3570) are kept by login in `reader.db`'s
`admin` table, as `ask_access` keeps ask. `admin enable` is the only way one
is made; `delete` takes the flag with the account. On the public site, `just
site-admin enable ken` (`disable`, `list`). Only `ken` is an admin there.
The page is in both editions behind the same check: on kai, with one
reader, Ken makes his tailnet login an admin (`just admin admin enable
ken@github`, with `--data` the service's data directory) and the grid shows
his reading alone. Nobody else is told the page exists. The start screen's
_Traffic_ link appears only for an admin, and the page answers anyone else,
signed out included, with the same 404 as a route that was never there.

A reader is a username or a login. `handle-note` refuses a note that is gone
or no longer flagged and, given `--seen` (the `updated` it was listed with),
one the reader has edited since. `--args-b64 <base64 JSON list>` stands for
any arguments, so text with quotes or spaces passes `fly ssh console -C`,
which splits on spaces, whole. review-notes calls it that way (§Readers'
notes and the backup).

`--data DIR` (or `$KLOOM_DATA_DIR`) says where `reader.db` is, and `--base
URL` (or `$KLOOM_PUBLIC_URL`) says what the link starts with.

## Public reader site

The reader edition runs on Fly.io as the app `kloom-reader`, at
<https://kloom.kenhiatt.us> (korg 3503). Everything is done from kai, with
the recipes below.

| What             | Where                                                                           |
| ---------------- | ------------------------------------------------------------------------------- |
| App              | Fly `kloom-reader`, org `personal`, region `iad`                                |
| Machine          | one `shared-cpu-1x`, 512 MB, always on (`fly.toml`)                             |
| Readers' data    | `reader.db` on the 1 GB volume `kloom_data`, at `/data`                         |
| The image        | `Dockerfile`: the reader edition, `admin.mjs`, the library, its media           |
| What is public   | `publish.json`: the subjects the library is built from                          |
| Deploy token     | `FLY_API_TOKEN` in kai's `/etc/khomelab/secrets.env`, read by `deploy/fly.sh`   |
| Ask's API key    | the Fly secret `ANTHROPIC_API_KEY`, from store entry `anthropic-api-key-reader` |
| Publish record   | `~/.local/share/kloom/public/publishes.log` on kai                              |
| Pulled reader.db | `~/.local/share/kloom/public/reader-YYYYMMDD-HHMM.db` on kai                    |
| DNS and the cert | GoDaddy CNAMEs `kloom` and `_acme-challenge.kloom`; Fly's Let's Encrypt cert    |

**The token.** The recipes never use Ken's flyctl login. `deploy/fly.sh`
runs flyctl (`~/.fly/bin/flyctl`, by full path) with a deploy token scoped
to this one app, read from the host's secrets file on each run and passed
in the environment. Its store entry is k-homelab's
`fly-deploy-token-kloom-reader`, and its rotation is in krot
(`registry/fly.toml`).

### Publishing

```sh
just publish-public
```

It refuses anything but a clean `main` that matches `origin/main`, so what
is public is always a commit GitHub has. Then it runs these steps:

1. **`just stage-public`** compiles the subjects in `publish.json` into
   `build-public/content.db` from this checkout. It never uses the service's
   grow clone. It copies the media that library lists into
   `build-public/media/`.
2. **`fly deploy --local-only`** builds the image here and pushes it. The
   library and media are the last two layers, so a publish that changed
   only content pushes only those. The volume is not touched.
3. **`just verify-public`** runs.
4. One line goes into `publishes.log`: the release, its image, the commit,
   and the library's build and source.

A subject can be held back by taking it out of `publish.json`.

**Rollback** is the previous image, named in the log:

```sh
deploy/fly.sh deploy -a kloom-reader --image registry.fly.io/kloom-reader:<label>
```

`just verify-public` checks the live site as a stranger and as a reader:

- TLS verifies
- `robots.txt` disallows everything, and http goes to https
- a stranger is sent to sign in, and the API refuses one
- signed in as a reader without ask, ask, keep and kept answers are 404, and
  grow is 404 for everyone
- pages go compressed
- a frame's body comes from the library, and the library names its build
- Fly's proxy overwrites a `Fly-Client-IP` a client sends, so sign-in
  backoff keys on the real address
- the month's ask spend report runs (`ask:` line: spend against the site
  cap, asks, readers with ask)
- then, as `note` lines, readers' notes this library has left detached
  (`admin.mjs detached`): a frame it no longer has, or an annotation whose
  words its reading lost. They are reported, never dropped. The reader sees
  them as detached in My notes, where they can clear them. A failure to run
  the check fails the recipe; a detached note does not.

It signs in as the reader `kloom-verify`. Each run invites it afresh with a
random password, and disables it at the end. The `Fly-Client-IP` check
spends up to 21 wrong passwords from kai's address, so sign-in from that
address (the house) waits 30 seconds afterwards. A second run within the
hour doubles the wait.

### Readers

```sh
just invite <username> [display name]   # prints the welcome link; adds them if named; also the reset
just readers                            # list
just disable-reader <username>          # their sessions end
```

These run `admin.mjs` on the machine through `fly ssh console`
(§The admin CLI). If `fly ssh console` hangs at `Connecting to fdaa:…`, the
host's WireGuard peer has gone stale. `fly wireguard list personal` names
it, and `fly wireguard remove personal <name>` lets flyctl make a new one.

### Ask

Ask on the site (korg 3530; docs/design.md §Ask on the reader site) runs on
its own Claude API key, in the Console workspace `kloom-reader`, whose spend
limit is $20 a month. **The key expires on 2027-01-31**; kmon warns 14 days
ahead (korg 3533). Its age-store entry is k-homelab's
`anthropic-api-key-reader`, and its rotation is in krot
(`registry/anthropic.toml`). Ken keeps an escrow copy in LastPass, which a
rotation must update too.

```sh
just public-ask-key                        # the age store's key into the Fly secret, staged for the next deploy
just reader-ask enable jkh                 # give a reader ask, at the $5 default cap
just reader-ask enable jkh --cap 8         # or their own
just reader-ask disable jkh                # take it away; their kept answers stay
just reader-ask list
just ask-usage                             # this month's spend, site and readers, each with its cap
just ask-usage --json                      # the report kmon collects daily
just public-ask-costs                      # cost per ask, per model (`--since`, `--reader`, `--model`)
```

`public-ask-key` pipes `bin/secret get` on kubs0 into `flyctl secrets import
--stage`, so the value is never printed or written to a file on kai. A
staged secret goes live at the next `just publish-public`.
`deploy/fly.sh secrets deploy -a kloom-reader` makes it live at once, and
restarts the machine.

### Readers' notes and the backup

Notes flagged for Agent review are answered in the live store, one guarded
write each, never by pushing a database back (korg 3504). The review-notes
skill does it with `--public`:

```sh
node skills/review-notes/review-notes.mjs --public list
node skills/review-notes/review-notes.mjs --public handle <login> <id> "<response>" --seen <updated>
node skills/review-notes/review-notes.mjs --public handle --file results.json
```

Each runs `admin.mjs` on the machine through `fly ssh console`, with its
arguments base64'd (§The admin CLI): `list` is `flagged --json`, live, each
note with its reader's display name and the `--seen` value to answer it
with, and `handle` is `handle-notes`. An answer is refused when the note is
gone, no longer flagged, or edited since it was listed, so nothing a reader
wrote after the listing is answered blind or overwritten. `handle --file`
sends a JSON list of `{reader, id, response, seen}` in one call, which saves
a few seconds of ssh per note when there are several. The reader sees the
answer under their note, counted as new on My notes until they have seen
it.

```sh
just pull-notes
```

It takes a consistent copy of `reader.db` on the machine (`node:sqlite`'s
backup), fetches it to `public/reader-YYYYMMDD-HHMM.db` (mode 600), and
deletes the copy on the machine. That copy is the backup beyond Fly's daily
volume snapshots, which keep five days. Reading it offline still works (put
it in a directory as `reader.db` and pass `--data` that directory), but
answer through `--public`: an answer written into the copy never reaches the
site.

Subjects readers suggest (korg 3459) are in the same store and come back the
same way: `review-notes.mjs --public suggestions`, and `mark-suggestion`
(skills/review-notes/SKILL.md §Suggested subjects).

**Cost.** One always-on `shared-cpu-1x` 512 MB machine and a 1 GB volume
come to about $4–6 a month. Ask Ken before scaling past that.

# Running kloom as a service

kloom runs on kai as a systemd user unit, `kloom.service`. The design is in
[design.md](design.md) §Who may write and §The content clone. This page is
the operations side. The public site's build, the reader edition, and its
sign-in are at the end (§Editions, §Signing in), and the public site itself
after them (§Public reader site).

| What                  | Where                                                          |
| --------------------- | -------------------------------------------------------------- |
| Tailnet URL           | `https://kai.encke-wahoo.ts.net:4890`                          |
| ssh door              | `127.0.0.1:4891` on kai, for `ssh -L`                          |
| App (the deploy copy) | `~/.local/share/kloom/app`                                     |
| Content clone         | `~/.local/share/kloom/content`, on `grow/kai`                  |
| Grow jobs             | `~/.local/share/kloom/data`                                    |
| The library (SQLite)  | `~/.local/share/kloom/data/content.db`, built from the clone   |
| Reader data (SQLite)  | `~/.local/share/kloom/data/reader.db` (with `-wal`, `-shm`)    |
| Unit                  | `deploy/kloom.service`, installed to `~/.config/systemd/user/` |
| Serve entry           | k-homelab `manifests/kai.yml`, `tailscale_serve` port 4890     |

## First time on a host

```sh
just content-init    # clone origin into ~/.local/share/kloom/content, on grow/<host>
just deploy          # build, copy, install and start the unit, then `just verify`
sudo tailscale serve --bg --https=4890 http://127.0.0.1:4890
```

Declare the serve entry in k-homelab's manifest for the host too, or a
rebuilt host comes back without the URL. The unit needs lingering on for the
user, and a logged-in Claude Code at `~/.local/bin/claude`, which grow and
ask run as the host's user.

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

The **reader edition** has no ask, grow or keep, and no kept answers. It is
**stripped, not switched off**: `KLOOM_EDITION=reader` at build time points
the `$edition` alias at `src/lib/edition/reader/`, whose modules import none
of the agent code, and `__KLOOM_EDITION__` lets the shared code drop the
rest (the AI pane, the Q&A section, the library build). The ask, grow, keep
and kept-answer routes are still there and answer 404. `just reader-gate`,
part of `just check`, builds it and fails if the build holds the providers,
an import of `node:child_process`, or code from ask, grow, keep or
editor-only modules. It checks by category, through markers, and a marker
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
  parents do (`J-n-K`). A reader has a username (typed, case-insensitive,
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

There is no admin on the site. `admin.mjs` runs where `reader.db` is, with
plain Node 24, through the accounts module and the reader store. On Fly it
runs through `fly ssh console -C`, so Fly's own sign-in is the admin's.

```sh
node admin.mjs add <username> <display name>      # no password until their link
node admin.mjs invite <username> [display name]   # prints the link; adds them if named
node admin.mjs disable <username>                 # their sessions end
node admin.mjs enable <username>
node admin.mjs list [--json]                      # status, last seen, sessions
node admin.mjs delete <username> --yes            # the account and everything they wrote
```

`--data DIR` (or `$KLOOM_DATA_DIR`) says where `reader.db` is, and `--base
URL` (or `$KLOOM_PUBLIC_URL`) says what the link starts with.

## Public reader site

The reader edition runs on Fly.io as the app `kloom-reader`, at
<https://kloom.kenhiatt.us> (korg 3503). Everything is done from kai, with
the recipes below.

| What             | Where                                                                         |
| ---------------- | ----------------------------------------------------------------------------- |
| App              | Fly `kloom-reader`, org `personal`, region `iad`                              |
| Machine          | one `shared-cpu-1x`, 512 MB, always on (`fly.toml`)                           |
| Readers' data    | `reader.db` on the 1 GB volume `kloom_data`, at `/data`                       |
| The image        | `Dockerfile`: the reader edition, `admin.mjs`, the library, its media         |
| What is public   | `publish.json`: the subjects the library is built from                        |
| Deploy token     | `FLY_API_TOKEN` in kai's `/etc/khomelab/secrets.env`, read by `deploy/fly.sh` |
| Publish record   | `~/.local/share/kloom/public/publishes.log` on kai                            |
| Pulled reader.db | `~/.local/share/kloom/public/reader-YYYYMMDD-HHMM.db` on kai                  |
| DNS and the cert | GoDaddy CNAMEs `kloom` and `_acme-challenge.kloom`; Fly's Let's Encrypt cert  |

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
- signed in, ask, grow, keep and kept answers are 404
- pages go compressed
- a frame's body comes from the library, and the library names its build
- Fly's proxy overwrites a `Fly-Client-IP` a client sends, so sign-in
  backoff keys on the real address

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

### Readers' notes and the backup

```sh
just pull-notes
```

It takes a consistent copy of `reader.db` on the machine (`node:sqlite`'s
backup), fetches it to `public/reader-YYYYMMDD-HHMM.db` (mode 600), and
deletes the copy on the machine. That copy is the backup beyond Fly's daily
volume snapshots, which keep five days. It is also what review-notes reads:
put it in a directory as `reader.db` and pass `--data` that directory.

**Cost.** One always-on `shared-cpu-1x` 512 MB machine and a 1 GB volume
come to about $4–6 a month. Ask Ken before scaling past that.

# Running kloom as a service

kloom runs on kai as a systemd user unit, `kloom.service`. The design is in
[design.md](design.md) §Who may write and §The content clone. This page is
the operations side.

| What                  | Where                                                          |
| --------------------- | -------------------------------------------------------------- |
| Tailnet URL           | `https://kai.encke-wahoo.ts.net:4890`                          |
| ssh door              | `127.0.0.1:4891` on kai, for `ssh -L`                          |
| App (the deploy copy) | `~/.local/share/kloom/app`                                     |
| Content clone         | `~/.local/share/kloom/content`, on `grow/kai`                  |
| Grow jobs             | `~/.local/share/kloom/data`                                    |
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
pick up merged main (below). `just verify` checks both doors, that the
tailnet door refuses an anonymous write, and that reader data answers only
a reader.

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

`journalctl --user -u kloom` shows the doors, and a `content:` line saying
what the start-up sync did.

## Bringing grown content back

Grow commits to `grow/kai` and pushes it. To bring it into main, open a PR
from `grow/kai`, review it like any other change, and merge it. Any merge
style works: the next restart (`systemctl --user restart kloom`, or the
next deploy) sees what main has and moves the branch onto it. Make review
edits in the merge or on main afterwards, not by pushing to `grow/kai`,
because that branch is the service's.

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

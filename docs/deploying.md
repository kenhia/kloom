# Running kloom as a service

kloom runs on kai as a systemd user unit, `kloom.service`. The design is in
[design.md](design.md) §Who may write and §The content clone. This page is
the operations side.

| What                    | Where                                                          |
| ----------------------- | -------------------------------------------------------------- |
| Tailnet URL             | `https://kai.encke-wahoo.ts.net:4890`                          |
| ssh door                | `127.0.0.1:4891` on kai, for `ssh -L`                          |
| App (the deploy copy)   | `~/.local/share/kloom/app`                                     |
| Content clone           | `~/.local/share/kloom/content`, on `grow/kai`                  |
| Kept answers, grow jobs | `~/.local/share/kloom/data`                                    |
| Unit                    | `deploy/kloom.service`, installed to `~/.config/systemd/user/` |
| Serve entry             | k-homelab `manifests/kai.yml`, `tailscale_serve` port 4890     |

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
pick up merged main (below). `just verify` checks both doors, and that the
tailnet door refuses an anonymous write.

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

# Windows: `just` runs recipes through `sh`, which Windows does not ship — put
# Git for Windows' `usr\bin` on PATH (it holds `sh.exe`) or run from Git Bash.
# (Upstream's own requirement: "sh must be available in the PATH".)

# List available recipes
default:
    @just --list

# Every subject under subjects/ is loaded and validated by a test, too.
# Run type checks, formatting/lint checks and unit tests
check:
    npm run check
    npm run lint
    npm test

# Serve locally on loopback
dev:
    npm run dev

# Build the Node server
build:
    npm run build

# The service's home on this host: app/ (the deploy copy), content/ (its own
# clone, on its grow branch) and data/ (kept answers, grow jobs)
home := env_var_or_default("KLOOM_HOME", home_directory() / ".local/share/kloom")
grow_branch := "grow/" + `hostname -s`

# Clone the content the service serves and grows into (once per host)
content-init:
    #!/usr/bin/env bash
    set -euo pipefail
    dir="{{ home }}/content"
    if [ -d "$dir/.git" ]; then echo "content clone already at $dir"; exit 0; fi
    git clone --quiet "$(git remote get-url origin)" "$dir"
    cd "$dir"
    if git rev-parse -q --verify "origin/{{ grow_branch }}" >/dev/null; then
        git checkout -q -b "{{ grow_branch }}" "origin/{{ grow_branch }}"
    else
        git checkout -q -b "{{ grow_branch }}"
    fi
    echo "content clone at $dir, on {{ grow_branch }}"

# Build this commit and run it as the service on this host (never touches content/)
deploy: build
    #!/usr/bin/env bash
    set -euo pipefail
    [ -z "$(git status --porcelain)" ] || { echo "deploy ships a commit: commit first" >&2; exit 1; }
    [ -d "{{ home }}/content/.git" ] || { echo "no content clone: run just content-init" >&2; exit 1; }
    app="{{ home }}/app"
    mkdir -p "$app" "{{ home }}/data"
    # What grow reads at run time comes too: the skill and its references.
    rsync -a --delete --exclude node_modules build skills docs create-tools \
        serve.js package.json package-lock.json kloom.config.json prettier.config.js "$app/"
    lock="$(sha256sum package-lock.json | cut -d' ' -f1)"
    if [ "$(cat "$app/.lock-sha" 2>/dev/null)" != "$lock" ]; then
        # Dev dependencies too: grow formats with Prettier and its Svelte plugin.
        (cd "$app" && npm ci --ignore-scripts --no-audit --no-fund --loglevel=error)
        echo "$lock" > "$app/.lock-sha"
    fi
    git rev-parse HEAD > "$app/DEPLOYED"
    install -Dm644 deploy/kloom.service ~/.config/systemd/user/kloom.service
    systemctl --user daemon-reload
    systemctl --user enable --quiet kloom.service
    systemctl --user restart kloom.service
    just verify

# Check the running service: both doors read, and the tailnet door refuses an anonymous write
verify:
    #!/usr/bin/env bash
    set -euo pipefail
    for i in $(seq 20); do curl -sf -o /dev/null http://127.0.0.1:4891/ -H 'accept: text/html' -L && break; sleep 0.5; done
    code() { curl -s -o /dev/null -w '%{http_code}' "$@"; }
    fail=0
    check() { if [ "$2" = "$3" ]; then echo "ok   $1"; else echo "FAIL $1: got $2, want $3"; fail=1; fi; }
    check "tailnet door reads" "$(code -L http://127.0.0.1:4890/)" 200
    check "ssh door reads" "$(code -L http://127.0.0.1:4891/)" 200
    check "tailnet door refuses an anonymous write" \
        "$(code -X POST -H 'content-type: application/json' -d '{}' http://127.0.0.1:4890/api/keep)" 401
    check "ssh door lets a write through" \
        "$(code -X POST -H 'content-type: application/json' -d '{}' http://127.0.0.1:4891/api/keep)" 400
    echo "deployed $(cat "{{ home }}/app/DEPLOYED" | cut -c1-9); content $(git -C "{{ home }}/content" log -1 --format='%h on %D' | cut -c1-60)"
    exit $fail

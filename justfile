# Windows: `just` runs recipes through `sh`, which Windows does not ship — put
# Git for Windows' `usr\bin` on PATH (it holds `sh.exe`) or run from Git Bash.
# (Upstream's own requirement: "sh must be available in the PATH".)

# List available recipes
default:
    @just --list

# Every subject under subjects/ is loaded and validated by a test, too.
# Run type checks, formatting/lint checks, unit tests and the authoring tools' tests
check:
    npm run check
    npm run lint
    npm test
    just tools-test
    @# Every mark is placed from a spec: one typed by hand, or a spec's mark not placed, fails.
    python3 create-tools/names/names.py mark create-tools/names/examples/*.json --check --placed

# The authoring tools' own tests: each tool's test_*.py (standard library unittest)
tools-test:
    #!/usr/bin/env bash
    set -euo pipefail
    for d in create-tools/*/; do
        ls "$d"test_*.py >/dev/null 2>&1 || continue
        python3 -m unittest discover -s "$d" -p 'test_*.py' -q
    done

# The app builds its library itself on first use (docs/design.md §Serving);
# this is a build by hand: every subject validated, unchanged ones kept, the
# file swapped in whole, and an invalid subject fails it.
# Compile subjects/ and names/ into the content.db the app serves
build-content out="data/content.db":
    #!/usr/bin/env bash
    set -euo pipefail
    node --input-type=module -e "
    import { resolve } from 'node:path';
    import { runnerImport } from 'vite';
    const { module: m } = await runnerImport('./engine/content-db.ts', { configFile: false, logLevel: 'error' });
    try {
        const r = await m.compileContent({
            subjectsDir: resolve('subjects'), namesDir: resolve('names'), out: resolve('{{ out }}'),
            compiler: m.engineDigest(resolve('engine')) ?? '', strict: true,
            source: process.env.SOURCE ?? '',
        });
        for (const p of r.nameProblems) console.error('names: ' + p);
        console.log(r.changed
            ? 'built ' + (r.built.join(', ') || 'the library') + (r.reused.length ? '; ' + r.reused.length + ' unchanged' : '') + (r.dropped.length ? '; dropped ' + r.dropped.join(', ') : '') + ' in ' + Math.round(r.ms) + ' ms'
            : 'up to date (' + r.reused.length + ' subjects)');
        console.log('{{ out }}: build ' + r.build);
    } catch (e) {
        console.error(e.message);
        process.exit(1);
    }
    " 2> >(grep -v ExperimentalWarning >&2)

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
    check "tailnet door keeps reader data from an anonymous read" \
        "$(code http://127.0.0.1:4890/api/reader/export)" 401
    check "ssh door reads its reader's data" "$(code http://127.0.0.1:4891/api/reader/export)" 200
    check "tailnet door keeps notes from an anonymous read" \
        "$(code 'http://127.0.0.1:4890/api/reader/notes?subject=western-civ')" 401
    check "ssh door reads its reader's notes" \
        "$(code 'http://127.0.0.1:4891/api/reader/notes?subject=western-civ')" 200
    check "a frame's body comes from the library" \
        "$(code http://127.0.0.1:4891/api/frame/western-civ/prometheus)" 200
    check "pages go compressed" \
        "$(curl -s -o /dev/null -H 'accept-encoding: br' -w '%header{content-encoding}' http://127.0.0.1:4891/western-civ)" br
    echo "library: $(curl -s -o /dev/null -w '%header{x-kloom-build}' http://127.0.0.1:4891/api/stats)"
    echo "deployed $(cat "{{ home }}/app/DEPLOYED" | cut -c1-9); content $(git -C "{{ home }}/content" log -1 --format='%h on %D' | cut -c1-60)"
    exit $fail

# The library copied `times` over, compiled and served by this checkout's
# build, measured against the targets in docs/design.md §Serving (korg 3460).
# `--app <dir>` serves another commit's build; `--skip-copy` reuses the copy.
# Benchmark serving at several times today's content
bench times="5" *args: build
    node bench/content.mjs --times {{ times }} {{ args }}

# The library's size: words, the book they would make, and what else it holds
stats:
    #!/usr/bin/env bash
    set -euo pipefail
    # The engine's own code, run through Vite's module runner (no dependency added).
    node --input-type=module -e "
    import { existsSync, readdirSync } from 'node:fs';
    import { runnerImport } from 'vite';
    const { module: m } = await runnerImport('./engine/stats.ts', { configFile: false, logLevel: 'error' });
    const subjects = readdirSync('subjects', { withFileTypes: true })
        .filter((d) => d.isDirectory() && existsSync('subjects/' + d.name + '/subject.json'))
        .map((d) => ({ id: d.name, dir: 'subjects/' + d.name }))
        .sort((a, b) => a.id.localeCompare(b.id));
    console.log(m.statsReport(await m.readLibraryStats(subjects, 'names')));
    "

# Every frame's scene fits the spine at 1280x800, 1400x900 and 390 wide: nothing
# runs into the HUD and the counter never meets the metadata (needs a local
# Playwright and Chromium; starts a dev server unless one answers on :5415)
scene-fit *subjects:
    #!/usr/bin/env bash
    set -euo pipefail
    url="${KLOOM_URL:-http://localhost:5415}"
    if ! curl -sf -o /dev/null "$url/"; then
        node_modules/.bin/vite dev --host 127.0.0.1 --port 5415 --strictPort >/dev/null 2>&1 &
        server=$!
        trap 'kill $server' EXIT
        for _ in $(seq 60); do curl -sf -o /dev/null "$url/" && break; sleep 0.5; done
    fi
    node create-tools/scene-fit/scene_fit.mjs --url "$url" {{ subjects }}

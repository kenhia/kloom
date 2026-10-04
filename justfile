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
    just reader-gate
    @# Every mark is placed from a spec: one typed by hand, or a spec's mark not placed, fails.
    python3 create-tools/names/names.py mark create-tools/names/examples/*.json --check --placed
    @# kloom's own words are American English; quotations, titles and names keep theirs (korg 3521).
    python3 create-tools/spelling/american.py check subjects names src engine

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
            source: process.env.SOURCE ?? '', added: await m.gitAddedDates(resolve('subjects')),
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

# The public site's edition (docs/deploying.md §Editions, korg 3500): ask,
# grow, keep and the agent code stripped out, into build-reader/. Then the
# generated types are put back to the full edition's.
# Build the reader edition
build-reader:
    KLOOM_EDITION=reader npm run build
    npx svelte-kit sync

# Builds the reader edition and fails if it holds the providers, a spawn,
# or ask, grow, keep or editor-only code (create-tools/reader-gate).
# Check the reader edition is stripped, not switched off
reader-gate:
    node create-tools/reader-gate/reader_gate.mjs

# Loopback only, serving this checkout's library (`just build-content`) and
# subjects' media, with readers in data/reader.db. Add one with
# `just admin invite <username> <display name> --base http://127.0.0.1:8080`,
# then open the link it prints.
# Run the reader edition locally, as the public site runs it
serve-reader port="8080": build-reader
    KLOOM_EDITION=reader PORT={{ port }} HOST=127.0.0.1 ORIGIN=http://127.0.0.1:{{ port }} \
        KLOOM_PUBLIC_URL=http://127.0.0.1:{{ port }} KLOOM_CONTENT_DB="$PWD/data/content.db" \
        KLOOM_CONFIG="$PWD/kloom.reader.json" \
        KLOOM_MEDIA_DIR="$PWD/subjects" node serve.js

# The reader edition's admin (admin.mjs): add, invite, disable, enable, list,
# delete. Against data/reader.db here; on Fly through `fly ssh console -C`.
# Manage the reader edition's readers
admin *args:
    node admin.mjs {{ args }}

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

# Grow branches with content main lacks (korg 3442): the sprint-start check in
# CLAUDE.md. Fetches first; exits 1 when one is pending, so it reads as a gate.
# A squash-merged or since-edited branch counts as merged. Review with
# skills/review-grown.
# List grow branches waiting for review
grow-pending:
    #!/usr/bin/env bash
    set -euo pipefail
    git fetch --quiet origin
    node --input-type=module -e "
    import { runnerImport } from 'vite';
    const { module: m } = await runnerImport('./src/lib/server/grow-branches.ts', { configFile: false, logLevel: 'error' });
    const states = await m.growBranches('.', 'origin/main');
    const waiting = states.filter((b) => !b.merged);
    for (const b of states) console.log((b.merged ? 'merged   ' : 'PENDING  ') + b.ref + (b.merged ? '' : '  (' + b.ahead + ' commit(s) ahead of origin/main)'));
    if (!states.length) console.log('no grow branches');
    if (waiting.length) { console.log('\n' + waiting.length + ' grow branch(es) to review first: skills/review-grown/SKILL.md'); process.exit(1); }
    console.log('nothing pending');
    "

# Evaluate ask providers (korg 3483): every question in
# bench/ask-eval/questions.json asked as ask asks it, under Sonnet 5 and the RA
# (kvllm's resident model) at three reasoning efforts, graded blind by Opus 5.5.
# Resumable; results under .scratch/ask-eval. `--only ra-low` or `--ids q01` narrow it;
# `--only sonnet-web,ra-low-web` adds web (the RA's is a Wikipedia-only shim).
# Ask the question set, grade the answers and print the tables
ask-eval *args:
    just build-content
    node bench/ask-eval/run.mjs {{ args }}
    node bench/ask-eval/judge.mjs
    node bench/ask-eval/report.mjs

# What API asks cost (korg 3529), from the cost log in the service's
# reader.db on this host: count, total, mean, p50 and p90 per ask, cost per
# 1k output tokens and the web's share, per model. `--since DATE`, `--until
# DATE`, `--reader R`, `--model M`, `--json`. The public site's: public-ask-costs.
# Report the cost per API ask
ask-costs *args:
    node --disable-warning=ExperimentalWarning admin.mjs --data "{{ home }}/data" ask-costs {{ args }}

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

# The settings pop-up and the keyboard shortcuts dialog, keyboard-only, at
# 1280x800 and 390 wide (korg 3493): selects never under their minimum, capture,
# clashes, reserved keys, Esc and focus (same Playwright and dev server as scene-fit)
keys-check:
    #!/usr/bin/env bash
    set -euo pipefail
    url="${KLOOM_URL:-http://localhost:5415}"
    if ! curl -sf -o /dev/null "$url/"; then
        node_modules/.bin/vite dev --host 127.0.0.1 --port 5415 --strictPort >/dev/null 2>&1 &
        server=$!
        trap 'kill $server' EXIT
        for _ in $(seq 60); do curl -sf -o /dev/null "$url/" && break; sleep 0.5; done
    fi
    node create-tools/keys-check/keys_check.mjs --url "$url"

# The Home button (korg 3517): home is a history entry at /<subject>, so a
# reload stays home, Back returns to the frame and Forward comes home (same
# Playwright and dev server as scene-fit)
home-check:
    #!/usr/bin/env bash
    set -euo pipefail
    url="${KLOOM_URL:-http://localhost:5415}"
    if ! curl -sf -o /dev/null "$url/"; then
        node_modules/.bin/vite dev --host 127.0.0.1 --port 5415 --strictPort >/dev/null 2>&1 &
        server=$!
        trap 'kill $server' EXIT
        for _ in $(seq 60); do curl -sf -o /dev/null "$url/" && break; sleep 0.5; done
    fi
    node create-tools/home-check/home_check.mjs --url "$url"

# The start screen (korg 3514) at 1024x768, 1280x800, 1400x900 and 390x844,
# with the library as served and with 24 subjects: every title on one line
# and on screen, the list in the dial's band and never meeting the title, the
# selection in view after End and Home, the carets true, and the picker below
# 60rem (same Playwright and dev server as scene-fit; the 24-subject library
# gets its own server on :5417)
start-fit:
    #!/usr/bin/env bash
    set -euo pipefail
    url="${KLOOM_URL:-http://localhost:5415}"
    if ! curl -sf -o /dev/null "$url/"; then
        node_modules/.bin/vite dev --host 127.0.0.1 --port 5415 --strictPort >/dev/null 2>&1 &
        server=$!
        trap 'kill $server' EXIT
        for _ in $(seq 60); do curl -sf -o /dev/null "$url/" && break; sleep 0.5; done
    fi
    node create-tools/start-fit/start_fit.mjs --url "$url"

# Scene and reading colours (korg 3495), keyboard-only at 1280x800 and 390
# wide: the panes coloured apart, the old Palette setting carried over, both
# brightness sliders at both ends with contrast read off the page, and the
# pop-up on screen (same Playwright and dev server as scene-fit)
colours-check:
    #!/usr/bin/env bash
    set -euo pipefail
    url="${KLOOM_URL:-http://localhost:5415}"
    if ! curl -sf -o /dev/null "$url/"; then
        node_modules/.bin/vite dev --host 127.0.0.1 --port 5415 --strictPort >/dev/null 2>&1 &
        server=$!
        trap 'kill $server' EXIT
        for _ in $(seq 60); do curl -sf -o /dev/null "$url/" && break; sleep 0.5; done
    fi
    node create-tools/colours-check/colours_check.mjs --url "$url"

# ---- The public reader site: kloom.kenhiatt.us on Fly app kloom-reader ----
# docs/deploying.md §Public reader site (korg 3503). Run on kai: flyctl is
# Ken's install there, and the deploy token is kai's FLY_API_TOKEN, which
# deploy/fly.sh reads per run.

fly := "deploy/fly.sh"
fly_app := "kloom-reader"
public_url := "https://kloom.kenhiatt.us"
public_home := home / "public"

# Compile publish.json's subjects from this checkout into build-public/ (content.db and the media it lists)
stage-public:
    node --disable-warning=ExperimentalWarning deploy/stage-public.mjs

# Refuses anything but a clean main that GitHub has. Builds the image here,
# library and media last, deploys it, runs verify-public, and records the
# release with the library's source commit in public/publishes.log. Rollback:
# `deploy/fly.sh deploy -a kloom-reader --image <an earlier image>` (the log
# names each one).
# Publish this commit of main to the public site
publish-public:
    #!/usr/bin/env bash
    set -euo pipefail
    [ "$(git branch --show-current)" = main ] || { echo "publish-public ships main: check out main" >&2; exit 1; }
    [ -z "$(git status --porcelain)" ] || { echo "publish-public ships a commit: the tree is not clean" >&2; exit 1; }
    git fetch --quiet origin main
    [ "$(git rev-parse HEAD)" = "$(git rev-parse origin/main)" ] || { echo "main is not origin/main: pull or push first" >&2; exit 1; }
    just stage-public
    commit="$(git rev-parse HEAD)"
    {{ fly }} deploy -a {{ fly_app }} --local-only --ha=false --yes \
        --build-arg KLOOM_BUILD="$(git log -1 --format='%h · %cs')" \
        --image-label "$(git rev-parse --short=9 HEAD)-$(date -u +%Y%m%d%H%M)"
    just verify-public
    mkdir -p "{{ public_home }}"
    release="$({{ fly }} releases -a {{ fly_app }} --image --json | node -e "const r = JSON.parse(require('fs').readFileSync(0, 'utf8'))[0]; console.log('v' + r.Version + ' image ' + (r.ImageRef ?? r.Image ?? '?'))")"
    echo "$(date -u +%Y-%m-%dT%H:%MZ) $release commit $commit $(cat build-public/LIBRARY)" | tee -a "{{ public_home }}/publishes.log"

# The public site as a stranger and as a reader sees it: TLS and HSTS, the
# sign-in wall, robots, grow gone and ask/keep gone for a reader without ask,
# compression, the library build, the ask spend report (korg 3530), and that
# Fly's proxy overwrites a Fly-Client-IP a client sends; then reports readers'
# notes the library has left detached. Signs in as the
# `kloom-verify` reader (a fresh welcome link each run, disabled after). The
# last check leaves this address waiting 30 s at sign-in, longer if run again
# within the hour.
# Check the public site
verify-public:
    #!/usr/bin/env bash
    set -euo pipefail
    url="{{ public_url }}"
    tmp="$(mktemp -d)"; trap 'rm -rf "$tmp"' EXIT
    jar="$tmp/jar"
    fail=0
    check() { if [ "$2" = "$3" ]; then echo "ok   $1"; else echo "FAIL $1: got $2, want $3"; fail=1; fi; }
    code() { curl -s -o /dev/null -w '%{http_code}' "$@"; }
    admin() { {{ fly }} ssh console -a {{ fly_app }} -q -C "node --disable-warning=ExperimentalWarning /app/admin.mjs --data /data $*" 2>&1; }

    for i in $(seq 30); do [ "$(code "$url/robots.txt")" = 200 ] && break; sleep 2; done
    check "TLS verifies" "$(curl -s -o /dev/null -w '%{ssl_verify_result}' "$url/robots.txt" || echo error)" 0
    check "robots.txt disallows everything" "$(curl -s "$url/robots.txt" | grep -cx 'Disallow: /')" 1
    hsts() { curl -s -o /dev/null -w '%header{strict-transport-security}' "$@"; }
    check "HSTS, a year, this host only: robots.txt" "$(hsts "$url/robots.txt")" "max-age=31536000"
    check "HSTS, a year, this host only: the way to sign in" "$(hsts "$url/western-civ")" "max-age=31536000"
    check "a stranger is sent to sign in" "$(curl -s -o /dev/null -w '%{http_code} %{redirect_url}' "$url/")" "303 $url/signin"
    check "a stranger's deep link comes back after" "$(curl -s -o /dev/null -w '%{redirect_url}' "$url/western-civ")" "$url/signin?next=%2Fwestern-civ"
    check "the API refuses a stranger" "$(code "$url/api/stats")" 401
    check "http goes to https" "$(code "http://${url#https://}/robots.txt")" 301

    admin enable kloom-verify >/dev/null || admin add kloom-verify "Publish check" >/dev/null
    link="$(admin invite kloom-verify --base "$url" | grep -o "$url/welcome/[A-Za-z0-9_-]*" || true)"
    [ -n "$link" ] || { echo "FAIL no welcome link from the admin CLI"; exit 1; }
    pw="$(head -c 18 /dev/urandom | base64 | tr -d '/+=')"
    curl -s -o /dev/null -c "$jar" -H "origin: $url" --data-urlencode "password=$pw" --data-urlencode "confirm=$pw" "$link"
    check "a welcome link signs the reader in" "$(code -b "$jar" "$url/api/stats")" 200
    # kloom-verify is never given ask, so ask and keep are 404 for it as for
    # anyone Ken has not allowed; grow is 404 for everyone.
    for p in ask grow keep; do
        check "grow, and ask and keep without ask, are 404: $p" \
            "$(code -b "$jar" -X POST -H "origin: $url" -H 'content-type: application/json' -d '{}' "$url/api/$p")" 404
    done
    check "kept answers are 404 without ask" "$(code -b "$jar" "$url/api/reader/kept?subject=western-civ")" 404
    check "pages go compressed" \
        "$(curl -s -o /dev/null -b "$jar" -H 'accept-encoding: br' -w '%header{content-encoding}' "$url/western-civ")" br
    check "HSTS, a year, this host only: a reader's page" "$(hsts -b "$jar" "$url/western-civ")" "max-age=31536000"
    check "a frame's body comes from the library" "$(code -b "$jar" "$url/api/frame/western-civ/prometheus")" 200
    build="$(curl -s -o /dev/null -b "$jar" -w '%header{x-kloom-build}' "$url/api/stats")"
    check "the library names its build" "$([ -n "$build" ] && echo yes || echo no)" yes
    curl -s -o /dev/null -b "$jar" -X POST -H "origin: $url" "$url/signout"
    admin disable kloom-verify >/dev/null

    # Backoff keys on Fly-Client-IP (src/lib/server/session.ts). If Fly's proxy
    # passed a client's own through, each try below would count against a
    # made-up address and none would wait; overwritten, they are all this
    # address's, and the twenty-first waits (or the first, if an earlier run
    # left this address waiting). Fresh usernames, so only the address can
    # be what waits. Asked as the page's script asks, so the action's own
    # status comes back: a plain form post answers 200 either way.
    waited=no
    for i in $(seq 21); do
        c="$(curl -s -X POST -H "origin: $url" -H 'accept: application/json' -H 'x-sveltekit-action: true' \
            -H "fly-client-ip: 203.0.113.$i" --data-urlencode "username=nobody-$RANDOM$RANDOM" \
            --data-urlencode "password=not-a-password" "$url/signin" | grep -o '"status":[0-9]*' || true)"
        [ "$c" = '"status":429' ] && { waited=yes; break; }
        [ "$c" = '"status":400' ] || { echo "FAIL sign-in answered ${c:-nothing}, not a refusal"; fail=1; break; }
    done
    check "Fly overwrites a client's Fly-Client-IP (backoff keys on the real address)" "$waited" yes

    echo "library: $build"

    # The month's ask spend against the caps (korg 3530): the report kmon reads.
    if usage="$(admin ask-usage --json)" && echo "$usage" | node -e "const u=JSON.parse(require('fs').readFileSync(0,'utf8')); if (typeof u.site?.spentUsd!=='number') process.exit(1); console.log('ask: ' + u.month + ' \$' + u.site.spentUsd.toFixed(2) + ' of \$' + u.site.capUsd + ', ' + u.site.asks + ' asks, ' + u.readers.filter((r) => r.allowed).length + ' reader(s) with ask')"; then :
    else echo "FAIL the ask spend report: $usage"; fail=1; fi

    # Readers' notes against this library (korg 3504): a note whose frame, or
    # annotation whose words, it no longer has is reported, never dropped.
    # Its reader sees it as detached in My notes; this is so Ken does too.
    if notes="$(admin detached)"; then echo "$notes" | sed 's/^/note /'
    else echo "FAIL the detached-note check: $notes"; fail=1; fi
    exit $fail

# Invite a public reader, adding them when given a display name; prints their welcome link (also the reset)
invite username *name:
    {{ fly }} ssh console -a {{ fly_app }} -q -C "node --disable-warning=ExperimentalWarning /app/admin.mjs --data /data invite {{ username }} {{ name }}"

# List the public site's readers
readers:
    {{ fly }} ssh console -a {{ fly_app }} -q -C "node --disable-warning=ExperimentalWarning /app/admin.mjs --data /data list"

# Disable a public reader: their sessions end
disable-reader username:
    {{ fly }} ssh console -a {{ fly_app }} -q -C "node --disable-warning=ExperimentalWarning /app/admin.mjs --data /data disable {{ username }}"

# Ask on the public site (korg 3530): `enable <reader> [--cap USD]` gives a
# reader ask at the configured cap ($5) or their own; `disable <reader>`
# takes it away; `list`. Everyone else sees no ask at all.
# Give a public reader ask, or take it away
reader-ask action *args:
    {{ fly }} ssh console -a {{ fly_app }} -q -C "node --disable-warning=ExperimentalWarning /app/admin.mjs --data /data reader-ask {{ action }} {{ args }}"

# This month's spend on the public site, per reader and site-wide, each with
# its cap (kloom.reader.json): `--json` is the report kmon collects (korg
# 3533), `--month YYYY-MM` another month.
# The public site's ask spend against its caps
ask-usage *args:
    {{ fly }} ssh console -a {{ fly_app }} -q -C "node --disable-warning=ExperimentalWarning /app/admin.mjs --data /data ask-usage {{ args }}"

# Cost per API ask from the public site's cost log (`ask-costs`' options)
public-ask-costs *args:
    {{ fly }} ssh console -a {{ fly_app }} -q -C "node --disable-warning=ExperimentalWarning /app/admin.mjs --data /data ask-costs {{ args }}"

# The public site's Claude API key (korg 3530), from k-homelab's age store
# entry anthropic-api-key-reader on kubs0 straight into the app's Fly secret
# ANTHROPIC_API_KEY, staged for the next deploy. Never printed, never in a
# file here.
# Set the public site's API key from the age store
public-ask-key:
    #!/usr/bin/env bash
    set -euo pipefail
    { printf 'ANTHROPIC_API_KEY='; ssh kubs0 'cd ~/k-homelab && bin/secret get anthropic-api-key-reader' | tr -d '\n'; echo; } \
        | {{ fly }} secrets import -a {{ fly_app }} --stage
    {{ fly }} secrets list -a {{ fly_app }}

# A consistent copy of the site's reader.db (node:sqlite's backup, on the
# machine), fetched to public/reader-YYYYMMDD-HHMM.db here: the backup beyond
# Fly's snapshots. Readable offline (`--data` a directory holding it as
# reader.db); notes are answered live, with review-notes' `--public`.
# Copy the public site's reader data to kai
pull-notes:
    #!/usr/bin/env bash
    set -euo pipefail
    # Readers' accounts are in it (hashes only, but still theirs): owner only.
    mkdir -p -m 700 "{{ public_home }}"
    out="{{ public_home }}/reader-$(date -u +%Y%m%d-%H%M).db"
    {{ fly }} ssh console -a {{ fly_app }} -q -C "node --disable-warning=ExperimentalWarning -e \"require('node:sqlite').backup(new (require('node:sqlite').DatabaseSync)('/data/reader.db'), '/data/pull.db').then(() => console.log('backed up'))\""
    {{ fly }} ssh sftp get -a {{ fly_app }} /data/pull.db "$out" >/dev/null
    chmod 600 "$out"
    {{ fly }} ssh console -a {{ fly_app }} -q -C "rm -f /data/pull.db"
    echo "$out ($(du -h "$out" | cut -f1))"

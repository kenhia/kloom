# 046 — Ask via the Claude API

## Goal

korg proposal 3532, covering 3529 and 3530. Run ask on the Claude API with
an API key, and log what every ask costs, first on Ken's instance; then
offer ask on the public reader site to the readers Ken chooses, `jkh` (his
parents) first, within monthly caps. Ken wants ask live for his parents
before their "intro to kloom" call, so the publish is the goal; it follows
the ship, after asking Ken.

## Decisions

Ken's, recorded on the items (2026-10-03):

- **Models.** On Ken's instance the `claude -p` default becomes Sonnet 5.5,
  and the API's Sonnet 5.5 and Haiku 4.5 sit beside it as "· API". On the
  reader site, Haiku 4.5 is the default, with Sonnet 5.5 offered.
- **Web is capped**: 3 searches, and 2 fetches of 8,000 tokens each. It is
  on by default on the reader site. Haiku takes the basic tool versions.
- **Caps** are $5 a month for `jkh` and $15 a month site-wide, beneath
  the Console workspace's $20.
- **Spend goes to kmon** as JSON through the admin path.
- **Sonnet 5.5 sends the refusal fallback** (`fallbacks: "default"`).

Mine:

- **Providers are a list, and each model entry names its provider.** An
  entry's `id` is what the reader's setting stores; its `model` is what
  the provider is given. One model on two routes is two entries
  (`claude-sonnet-5-5` and `api:claude-sonnet-5-5`), so the setting can
  hold either.
- **The cost log and the allow-list live in `reader.db`**: migration 8 adds
  the `ask_cost` and `ask_access` tables. A separate module,
  `ask-ledger.ts`, holds them; like `accounts.ts` it imports only `node:`
  modules, so `admin.mjs` loads it with plain Node. It is not reader data in
  `ReaderStore`'s sense (places, notes, kept answers). It is the
  deployment's ledger, keyed by reader. A row never holds the question.
- **The key is read per ask, and only that key.** It comes from the
  environment (Fly) or else from one line of kai's
  `/etc/khomelab/secrets.env` (`keyFile`). Loading the whole file with
  `EnvironmentFile=` would have handed the Fly, HF and OpenAlex tokens to the
  app, and to every `claude -p` it spawns. `claude -p` is now spawned
  without `ANTHROPIC_API_KEY`: with the key set, it would bill the key
  rather than Ken's subscription.
- **The reader edition chooses its providers through `$edition/providers`**.
  The reader's module builds the API provider and refuses `claude-cli`, so
  `claude -p`'s adapter is not in that build. The reader gate's
  categories changed. Ask, keep and kept answers left the forbidden list.
  `claude -p` (two markers), grow and editor-only stayed, and editor-only
  now includes moving kept-answer files. The client may no longer hold
  `/api/grow`. Both new rules were negative-tested: the full edition's
  providers dropped into the reader's failed on `--strict-mcp-config` and
  `child_process`, and an un-guarded `refreshJobs` failed on `/api/grow`.
- **A cap rests ask rather than failing it.** A request at either cap gets
  one `budget` event and no turn. The pane disables Ask and puts the
  question back in the box. Past 80% of either cap it says ask is nearly at
  this month's limit. The one ask that crosses a cap can overshoot it, by
  about $0.15 at most with web.
- **Prices are per serving model, at the alias's rate.** The API names the
  serving model by its dated id; the first live ask was priced 5× too high
  until `undated()` mapped it (found in the end-to-end test, now tested).
  A model missing from the table is priced at the dearest rate, so a cap
  never undercounts.

## What shipped

- `engine/ai/anthropic-api.ts`: streaming through the SDK's beta stream;
  `server_tool_use` becomes `searching` and `fallback` becomes `retrying`,
  both resetting the answer; `pause_turn` resumed; `usage` reported per
  serving model; a refusal shown plainly; errors that never name the key.
- `kloom.config.json` (providers, prices checked 2026-10-03 against the
  pricing page) and `kloom.reader.json` (API only, caps).
- `src/lib/server/ask-route.ts`, one ask handler for both editions;
  `offer.ts`, the AI pane's offer with the reader's standing; the reader
  edition's ask, keep and kept answers gated by the allow-list.
- `admin.mjs reader-ask | ask-usage | ask-costs`. The `just` recipes
  `ask-costs`, `reader-ask`, `ask-usage`, `public-ask-costs` and
  `public-ask-key`. The Dockerfile ships `kloom.reader.json` and the ledger.
  `verify-public` checks the spend report.
- The AI pane's budget notice and resting state, and grow folded out of the
  reader build. The Q&A section and the AI pane appear wherever the page
  offers them. About, Welcome and the User's Guide tell a reader with ask
  who answers (Claude, an AI made by Anthropic, provided by Ken), that it
  can be wrong, and how to say so.
- Docs: design.md §Settings, §Ask on the Claude API, §Ask costs, §Ask on the
  reader site; deploying.md §Editions and §Ask; README.

## Keys

- **`anthropic-api-key`** (Ken's): piped from `kai:~/jupyter/.env` into
  the age store, never printed, then index entry, kai manifest and apply
  (k-homelab #115, `79a511a`) and krot (`registry/anthropic.toml`,
  `a029547`). The `~/jupyter/.env` copy is a stray under the one-copy-per-host
  convention. Jupyter reads it, so moving that is Ken's call; reported, not
  deleted.
- **`anthropic-api-key-reader`** (the site's, workspace `kloom-reader`,
  expires 2027-01-31): index entry and probe, krot entry with a Fly
  `[consumer]` row, and staged as the Fly secret by `just public-ask-key`.
  krot has no expiry field, so the date is in the entry's prose (noted on
  kmon 3533).
- Both probes are one-token Haiku Messages calls. `bin/secret verify`
  passes both, each with its wrong-key control refused, and a wrong key run
  by hand failed (curl 22). Both krot notes carry the LastPass escrow line.

## The leak, and five rotations

While fingerprinting Ken's key for krot, I ran a command that printed all of
kai's `/etc/khomelab/secrets.env` into this session's transcript: five live
values (`ANTHROPIC_API_KEY`, `FLY_API_TOKEN`, `HF_TOKEN`,
`OPENALEX_API_KEY`, `REDISCLI_AUTH`). The site's key was not in that file.
I stopped and asked, and Ken ruled: rotate all five.

- **Redis rpi53**: minted by kaed, applied at rpi53, distributed to all
  eleven hosts (`bin/apply`, and the helpers for cleo and for kimac, which
  only kai could reach), consumers restarted, verified (authority with
  control, all eleven fingerprints, live health keys with a WRONGPASS
  control, the kubsdb dashboard), and swept. New `1f9229e1c5f5`. kimac,
  asleep to kubs0 at first, was caught through kai, then converged by
  `bin/apply` once awake (its stale flag cleared) and proven with
  `kdash-pub check` authenticating from the file.
- **Fly deploy token**: `kloom-publish-kai-2` minted into the store, applied
  to kai and proven, and the old token revoked. New `372e2c3c4239`.
- **Anthropic (Ken's), HuggingFace, OpenAlex**: mint in the browser.
  Waiting on Ken (see Follow-ups).

The rule it taught is now in CLAUDE.md: never print a secrets file.

## Verified

- `just check` green: svelte-check, prettier and eslint, 1,457 tests,
  tools-test, reader-gate, marks and spelling.
- **On Ken's instance** (the full edition's dev server, Ken's key):
  - Haiku · API asked without web, and Haiku and Sonnet 5.5 · API asked with
    web, all streamed end to end, each with a matching `ask_cost` row (web
    turns $0.029 and $0.162; `just ask-costs` reads them).
  - Sonnet 5.5 took `fallbacks: "default"`.
  - Keep stored the API answer with its two web citations and `anthropic-api`.
- **The reader edition**, served locally with the site's own key:
  - `jkh` asks and keeps; `other` gets a 404 and no AI pane; grow is a 404
    for `jkh` too.
  - `capped` ($0.01) went near on ask 3, crossed on ask 4, and on ask 5 got
    a resting budget with no turn.
  - `ask-usage --json` matched the rows exactly, per reader and site-wide.
  - In the browser: `capped` sees "Ask is resting until November 1" with
    Ask disabled. `jkh` asks and keeps by keyboard alone, with no grow
    control.
- Neither server log, nor any output, holds a key (grep `sk-ant`: 0).

## Repaired in passing

- `/api/reader/kept` checked its subject against the subject directories
  (`requireSubjectDir`), which the reader edition does not have. It checks
  the library now (`servedSubject`), in both editions.
- krot's Redis entry named apt-temps at `~/src/homelab/apt-temps`; it is at
  `/datastore/apt-temps` (found in the restart, corrected).

## Follow-ups

- Ken mints new keys for his default Anthropic workspace, HuggingFace and
  OpenAlex; then they are applied, verified and stamped in krot, and the old
  ones revoked. After the Anthropic one, one more API ask on kai.
- After the ship: back up the reader store, ask Ken, `just publish-public`,
  then `just reader-ask enable jkh` and `just reader-ask enable ken` (Ken,
  2026-10-03: his own account too, at the same $5 default cap; two readers
  at $5 fit inside the $15 site cap), and one real question there. The
  site's `admin.mjs` gains `reader-ask` only with this publish, so neither
  can be enabled before it. `jkh` is still `invited` (never signed in), so
  Ken's parents need their welcome link used, or a new one
  (`just invite jkh`), before the call.

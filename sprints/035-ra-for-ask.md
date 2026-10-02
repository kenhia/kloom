# 035 — The RA for ask

## Goal

korg proposal 3484, covering korg 3483: find out whether the RA, the
resident model kvllm serves on kai, answers ask's questions well enough to
offer beside Claude. Phase 1 evaluates it against Sonnet 5, the default,
and ends at a go/no-go for Ken. Phase 2, adding the RA as a second provider
(an `openai-compatible` kind in the config, "RA · <model>" in the ask-model
setting, ask only, streamed, without web), is built only on his go.

## Decisions

- **Premise, checked at start.** It held. `kloom.config.json` has one
  `provider` of kind `claude-cli`, and `appConfigProblems` refuses any other
  kind. kvllm answers on `localhost:8000/v1`, and `/v1/models` names the
  resident: **`qwen3.8-27b-nvfp4`** (Qwen3.8 27B, NVFP4, 122,880 context,
  reasoning parser `qwen3`, served at `reasoning_effort: medium`). kloom is
  not in the cross-project plan index.
- **The eval runs what the app runs.** The harness (`bench/ask-eval/`,
  `just ask-eval`) builds each question's context the way the ask route
  does, from `content.db` through `askContext`, and sends the shared
  `askSystem()` and `askPrompt()` with no web. Sonnet 5 goes through the real
  `ClaudeCliProvider`, so its latency includes the CLI's own start. The RA
  gets one streamed `/v1/chat/completions` call per question, the way a
  phase-2 adapter would make it. No dependency was added: the scripts load
  the engine through Vite's module runner, as `just stats` does.
- **The RA at three efforts, not one.** Ask is a reader waiting on a pane,
  so how long the RA thinks matters as much as what it says. Each question
  goes to the RA as served (`medium`), at `reasoning_effort: low`, and with
  thinking off (`enable_thinking: false`), all per request through
  `chat_template_kwargs`. The served model was never switched, and none of
  its settings were changed.
- **kvllm's judge shape, not its harness.** kvllm's judged suite is an
  Inspect AI task with its own prompts and a Haiku 4.5 judge calibrated
  against Ken's hand scores on those tasks. Its tasks do not fit ask's
  prompt, and Haiku grading Sonnet is the weaker grading the stronger. So
  the judge here borrows the suite's shape (0–10 per axis with a rationale,
  a list of violations, and mechanical checks for the rules that are
  objective) and uses **Opus 5.5** through `claude -p`, with no tools. It
  grades all four answers to a question in one call, **blind**: the
  answers carry letters, shuffled by a fixed per-question seed, and nothing
  names a model. Its axes are the ones 3483 names: accuracy, grounding (the
  `[n]` markers), honesty (inventing, or not saying when it does not know)
  and clarity, plus an overall score and a list of false claims. The
  mechanical checks cover length over 250 words, a heading, reasoning
  leaked into the answer, and a marker with no source.
- **One draw per question.** The RA samples at its served T=1.0, so a
  second run gives different answers. (q01's medium answer in the smoke
  test was clean; in the full run it invented a figure.) Thirty questions
  under four conditions is the sample. A gap smaller than about a point on
  the overall mean is noise.
- **The question set** (`bench/ask-eval/questions.json`, 29 questions over
  all ten subjects): eight factual lookups the frame answers, four "explain
  it more simply", four "why did it matter", three that need the frame's
  citations, four the frame cannot answer (three unknowable names and one
  half-answerable count-and-name), and six of Ken's own questions, taken
  word for word from his kept answers. Each unanswerable question carries a
  note for the judge saying what an invention would look like.
- **Sequential, one request at a time.** The RA is shared with kmon and
  kyac. The runner reads vLLM's own `num_requests_running` and
  `num_requests_waiting` before each RA request, so contention shows in the
  results rather than hiding in the latency.
- **Trail frames are asked from the trail.** Five of the questions sit on
  frames that only a side trail reaches (`surgical-count`, `uncertainty`,
  `self-attention`, `rsa`, `adaline`). They carry a `trail`, so the prompt
  says "on the side trail …" as it would for a reader there. The first run
  stopped at the first of them; the runner resumed where it stopped.

## Phase 1: results

Run on 2026-10-02 against `qwen3.8-27b-nvfp4` as served (vLLM on kai, MTP
draft head on) and `claude-sonnet-5` through `claude -p`. The judge was
Opus 5.5. vLLM's gauges showed **no other consumer** using the RA during
any request, so these latencies are an idle RA's. Raw answers and grades
are under `.scratch/ask-eval/` (draw 1) and `.scratch/ask-eval-2/`
(draw 2), and `node bench/ask-eval/report.mjs --out <dir>` reprints the
tables.

**Draw 1: all four conditions, 29 questions, graded together:**

| condition | overall | accuracy | grounding | honesty | clarity | with a false claim | over 250 words | judged best | words (median) |
| --------- | ------: | -------: | --------: | ------: | ------: | -----------------: | -------------: | ----------: | -------------: |
| Sonnet 5  |     8.2 |      8.6 |       8.8 |     8.8 |     8.1 |            7 of 29 |             10 |          17 |            232 |
| RA medium |     7.1 |      7.4 |       7.6 |     7.1 |     8.0 |           18 of 29 |              7 |           8 |            218 |
| RA low    |     7.7 |      8.2 |       7.9 |     7.9 |     8.3 |           12 of 29 |              4 |           4 |            182 |
| RA off    |     6.1 |      7.3 |       5.8 |     6.9 |     7.2 |           14 of 29 |              4 |           0 |            187 |

| condition | first word, median | first word, p90 | whole answer, median | whole answer, p90 |
| --------- | -----------------: | --------------: | -------------------: | ----------------: |
| Sonnet 5  |              1.9 s |           4.4 s |                7.2 s |             9.8 s |
| RA medium |              4.2 s |          10.1 s |                9.3 s |            16.8 s |
| RA low    |              3.3 s |           7.2 s |                7.0 s |            11.2 s |
| RA off    |              0.3 s |           0.4 s |                4.7 s |             6.3 s |

Overall score by kind of question:

| kind                | Sonnet 5 | RA medium | RA low | RA off |
| ------------------- | -------: | --------: | -----: | -----: |
| factual (8)         |      8.4 |       7.1 |    8.0 |    6.1 |
| simpler (4)         |      8.3 |       7.8 |    7.0 |    6.3 |
| why it mattered (4) |      8.0 |       6.5 |    7.0 |    5.5 |
| citations (3)       |      9.0 |       6.7 |    8.7 |    7.3 |
| unanswerable (4)    |      8.0 |       8.5 |    8.8 |    7.5 |
| Ken's own (6)       |      7.8 |       6.5 |    6.8 |    4.7 |

**Draw 2: the two contenders again, fresh answers, graded as a pair:**

| condition | overall | accuracy | grounding | honesty | with a false claim | Ken's own (6) | unanswerable (4) | first word, median | whole answer, median |
| --------- | ------: | -------: | --------: | ------: | -----------------: | ------------: | ---------------: | -----------------: | -------------------: |
| Sonnet 5  |     8.3 |      8.7 |       9.0 |     8.3 |            9 of 29 |           8.0 |              9.5 |              1.7 s |                7.6 s |
| RA low    |     7.2 |      7.5 |       7.4 |     7.5 |           19 of 29 |           5.8 |              7.3 |              3.1 s |                7.2 s |

What the numbers say:

- **Sonnet is ahead in both draws, by 0.5 and then 1.1 overall,** and the
  RA makes a false claim in 12 to 19 answers of 29 against Sonnet's 7
  to 9. The second draw widened the gap rather than closing it, so it is
  not the RA's sampling noise.
- **The RA does not invent the unknowable.** Asked the name of the
  Ishango bone's carver, the Antikythera ship's captain or the first
  soldier saved by Blood for Britain, it said no one knows, every time.
  Its false claims are details: a quotation made of a paraphrase, a figure
  worked out and stated as fact ("six to seven weeks"), a `[n]` marker on
  a source that does not say it, or a wrong date or relation (Matthias as
  Rudolf II's son).
- **It is weakest on Ken's own questions,** which are the ones that reach
  past the frame (modem training tones, who Kepler was, square roots on a
  soroban, revisits of the Turing test). That is world knowledge, and a 27B
  model has less of it. Asked whether the modem screech was the echo
  canceller adapting, it said no in both draws ("Not exactly", then "No"),
  with confidence. The handshakes of V.32 and V.34 modems have an
  echo-canceller training phase, so the answer is "partly, yes".
- **Grounding is the RA's other weak axis.** It marks more than it should,
  sometimes `[1][2]` on every sentence with thinking off, and it puts
  markers on sources that do not support the sentence.
- **It is not faster,** except with thinking off, which is also the worst
  answer by every measure. At low effort its whole answer takes about as
  long as Sonnet's, but the first word comes later (3.3 s against 1.9 s),
  because it thinks before it writes and the reader sees nothing while it
  does.
- **Low effort beat medium in draw 1.** More thinking gave longer answers,
  more invented detail and slower ones. Low effort used a median of 194
  reasoning tokens (at most 1,062); no answer ran out of budget.

Examples, the same question to each (draw 1):

> **q24, Ken's: was the modem's screech the echo canceller adapting?**
>
> _Sonnet 5 (8):_ "Yes, largely so. … The screeching handshake tones heard
> when a modem connects were part of this startup negotiation — the modems
> exchanging known reference signals so each side's adaptive filters (both
> the echo canceller and the line equalizer) could converge … the frame
> itself doesn't explicitly mention the handshake screech … that detail
> goes a bit beyond what's given."
>
> _RA low (6):_ "Not exactly. … the training tones you hear are the
> equalizer and overall link setup 'locking on,' not an echo canceller
> specifically converging." The judge: it plays down echo-canceller
> training too far, puts `[5]` on an equalisation claim that an
> echo-cancellation source does not support, and does not say it has gone
> beyond the frame.

> **q20: who carved the Ishango bone?**
>
> _Sonnet 5 (8):_ "The frame doesn't name the person who carved the bone —
> and no one knows. … The carver himself remains anonymous". The judge
> marked down "himself" as an assumption.
>
> _RA low (9):_ "We don't know. The bone dates to roughly 20,000 years ago,
> far before any written records of individual names existed [1]. The
> frame notes only that 'someone cut these marks deliberately, in groups,
> and kept the tool' — but no individual is identified."

> **q19: which source reports the CMB's discovery, and what did they
> measure?** Both scored 9. Both named `[1]`, Penzias and Wilson's paper,
> gave the 3.5 K excess at 4,080 Mc/s with the frame's budget (6.7 K at the
> zenith, less 2.3 K of atmosphere and 0.9 K of antenna), and said that
> `[2]`, Dicke's group, supplied the interpretation. The RA took 136 words
> to do it and Sonnet took 224.

> **q27, Ken's: why can "deaths a year per 100 sick" exceed 100?** Both
> scored 8. Both explained annualising a short window and quoted the
> frame's "about a third". Sonnet used a speedometer analogy and slipped on
> one figure (34 per 100 where the frame's arithmetic gives about 32). The
> RA set out the arithmetic step by step, then muddled its last paragraph
> ("the hospital would be empty of sick … long before 100 per 100 were
> reached").

Caveats: one judge, and that judge is Claude grading a Claude answer
against a Qwen one, blind but not free of family resemblance. Ken's spot
check of a sample is the counterweight 3483 asks for. The answers sit side
by side in `answers.jsonl`, keyed by question.

### Also found

- **Sonnet runs past ask's 250-word limit** in 10 and 13 answers of 29,
  mostly by 10 to 60 words. Ken's call (korg 3490): **250 is a soft
  limit.** An answer over it is shown whole, never truncated or failed, and
  the limit is revisited only if answers grow much longer. Recorded in
  `docs/design.md` §Ask.

## Phase 1b: Ken's questions with the web

Ken asked, before deciding, what the RA does when it can look things up,
since his own questions are the ones that reach past the frame. Sonnet's
side needed only a flag: the real adapter with `web: true`, so WebSearch
and WebFetch, as a reader's web turn gets them. The RA has no search of its
own, and nothing in the homelab offers one (kmon's "search" is klams), so
the harness gives it a **Wikipedia-only shim**
(`bench/ask-eval/wikipedia-tools.mjs`). `search` runs English Wikipedia's
search API and returns five titles, URLs and snippets. `fetch` reads one
article as plain text, the first 15,000 characters, and refuses any other
site. They are offered in the OpenAI tool format through vLLM's `qwen3_xml`
parser, with ask's real web prompt (`askSystem(true)`). Text the RA wrote
before a tool call is dropped, as ask drops it. The comparison is therefore
the RA plus Wikipedia against Sonnet plus Anthropic's search: narrower for
the RA, but it is the search a phase 2 with web would have to supply.

Ken's six questions, four conditions each, two draws, each draw graded
blind as a set of four (`.scratch/ask-eval-web-1/`, `-2/`):

| condition     | overall, draw 1 | overall, draw 2 | with a false claim | first word, median | whole answer, median |
| ------------- | --------------: | --------------: | -----------------: | -----------------: | -------------------: |
| Sonnet 5      |             7.5 |             6.8 |     2 of 6, 3 of 6 |          1.6–1.7 s |            7.9–8.1 s |
| Sonnet 5, web |             7.2 |             8.0 |     4 of 6, 2 of 6 |        10.5–10.7 s |          18.7–19.9 s |
| RA low        |             5.0 |             6.2 |     5 of 6, 4 of 6 |          6.1–7.7 s |          12.3–13.7 s |
| RA low, web   |    5.6 (5 of 6) |             6.3 |     4 of 5, 4 of 6 |        14.3–16.4 s |          19.1–23.1 s |

What the web did:

- **It lifted the RA a little, not to Sonnet's level, and not even to
  Sonnet's level without the web.** RA with web averaged about 6.0 on
  Ken's questions; Sonnet without it about 7.2, and Sonnet with it 7.6.
- **The RA does not search well.** It wrote its queries for a general web
  engine (`OR`, quoted phrases, years: `dialup modem "whine" OR "screech"
"training" phase sound reason`), which Wikipedia's search does not parse,
  so many came back empty or off target. Its median was 2 and then 5 tool
  calls an answer. It read an article in only 2 of 5 and 3 of 6 answers, and
  listed its pages in 2 of 5 and 4 of 6.
- **Once it looped and never answered.** On the Turing-test question (q29,
  draw 1) it made 18 tool calls over the harness's ten rounds: 16 searches
  and two page reads, and no answer. The real adapter would have hit its
  timeout and shown the reader an error.
- **What it read, it still garbled.** It dated _Astronomia nova_ 1619
  (1609) and credited it with all three laws, said Zhu Zaiyu worked a root
  on "nine abacuses", and called four weeks "a fortnight-and-a-half".
- **The web helped Sonnet on the questions that need it** (the modem
  handshake, the Turing-test revisits, the abacus), and in draw 2 it was
  judged best on three of the six. It was slower: a median of about 10 s
  to the first word, and up to 46 s.
- **Six questions over two draws is a small sample.** Sonnet's own score
  without the web moved 0.7 between draws, so the RA's +0.3 to +0.6 from
  the web is inside the noise. Only the direction is clear: the web does
  not close the gap.
- A general search engine would serve the RA's queries better than
  Wikipedia does. But it would not fix its attribution, it would cost an
  account and a key, and the slow first word and the loop would remain.

## Phase 1c: Sonnet against Haiku

Ken asked, once the RA was settled, whether Haiku 4.5 is worth its speed:
would a slightly worse answer that arrives much sooner be a fair trade?
Haiku is already in `kloom.config.json`'s models list, so the question is
whether it should be offered, or made the default.

**Haiku is slower than Sonnet as kloom runs it.** Under `claude -p`, Haiku
4.5 opens every turn with an extended-thinking block, and the reader sees
nothing until it ends. Sonnet 5 decides for itself and, on ask's questions,
does not think. The raw stream shows it: Haiku `thinking` then `text`,
Sonnet `text` at once. `MAX_THINKING_TOKENS=0` in the environment, or
`--settings '{"alwaysThinkingEnabled": false}'`, turns it off. So the
harness ran Haiku both ways (`haiku`, and `haiku-nothink` through a second
`ClaudeCliProvider` whose `spawn` hook sets the variable; the app's adapter
is unchanged). Each draw graded the three together, blind, all 29
questions (`.scratch/ask-eval-nothink-1/`, `-2/`):

| condition             |  overall | with a false claim | Ken's own (6) | first word, median | whole answer, median |
| --------------------- | -------: | -----------------: | ------------: | -----------------: | -------------------: |
| Sonnet 5              | 8.5, 8.5 |         5, 5 of 29 |      8.0, 8.2 |              1.7 s |            7.4–7.5 s |
| Haiku 4.5, as run now | 6.9, 7.3 |       15, 14 of 29 |      6.3, 7.0 |          5.3–5.7 s |            9.1–9.4 s |
| Haiku, thinking off   | 6.9, 7.0 |       14, 12 of 29 |      6.0, 5.8 |              0.9 s |            4.8–5.1 s |

And Ken's six with the web, two draws, all six conditions graded together
(`.scratch/ask-eval-nothink-web-1/`, `-2/`):

| condition                |  overall | first word, median |    whole answer, median |
| ------------------------ | -------: | -----------------: | ----------------------: |
| Sonnet 5                 | 7.8, 7.5 |          1.4–2.0 s |               7.6–8.9 s |
| Sonnet 5, web            | 7.8, 7.7 |        10.1–12.3 s |             17.6–18.9 s |
| Haiku 4.5, web           | 5.5, 6.5 |        18.5–22.1 s |             22.5–26.6 s |
| Haiku, thinking off      | 5.7, 5.5 |              0.9 s |               4.9–5.5 s |
| Haiku, thinking off, web | 5.5, 5.8 |        16.4–16.6 s | 19.9–20.4 s (one 161 s) |

What it says:

- **Thinking costs Haiku its speed and buys nothing.** With it off, Haiku
  scored the same (6.9 against 6.9, 7.0 against 7.3: inside the noise)
  and reached the first word five times sooner.
- **Haiku with thinking off is faster than Sonnet, but not by much.** Its
  first word arrives at 0.9 s against Sonnet's 1.7 s, and its whole answer
  at about 5 s against 7.5 s. The answer streams, so the reader starts
  reading about 0.8 s sooner, and Sonnet's first word is already under two
  seconds.
- **The quality drop is not small.** About 1.5 points overall (8.5 against
  7.0), a false claim in 12–14 answers of 29 against Sonnet's 5, and
  Sonnet judged the best answer in 25–26 of 29. On Ken's own questions the
  gap is wider: about 5.9 against 8.1. That is roughly the RA's level, at
  Claude's speed.
- **The web does not help Haiku either,** and is slower for it than for
  Sonnet (a median of 16–22 s to the first word, and one answer that took
  2.7 minutes).

## Recommendation

**No-go, for now; the web runs (Phase 1b) did not change it.** The RA
answers kloom's questions decently, and as honestly as Sonnet about what
nobody knows. But it gets details wrong in roughly half its answers, twice
as often as Sonnet, and most often on the questions Ken actually asks, the
ones that go past the frame. For a reader learning a subject, a confident
wrong detail is the expensive failure. It is also no faster to the first
word unless its thinking is turned off, which makes it worse again. The case
for it would be cost or privacy; Sonnet runs on the existing subscription,
and the questions are about public history.

**Would a different resident do better?** Probably not enough. The gap is
world knowledge and careful attribution, which track model size more than
tuning. kvllm's board has the second opinion, `gemma-4-31b-it-awq`, below
Qwen3.8 on its judged writing suite (0.68–0.85 against 0.97). The served
model was not switched to find out, and should not be for this. If a
larger resident ever lands, `just ask-eval --only ra-low` re-asks the
same questions against it, and `--out` keeps the runs apart.

## Decision

Ken, 2026-10-02, after phase 1 and 1b: **no-go.** Phase 2 was not built:
no provider list, no `openai-compatible` kind, no RA in the ask-model
setting. What ships is the eval harness (`bench/ask-eval/`, `just
ask-eval`), so the question can be asked again of a later resident, and
the findings (here, on korg 3483, and in klams for kmon and kyac, which
share the RA).

Ken, the same day, after phase 1c: **Haiku comes out of the models list.**
As `claude -p` runs it, it was slower to its first word than Sonnet and
worse. With thinking off it is only about 0.8 s faster to the first word,
at a cost of 1.5 points and twice the false claims. `kloom.config.json` now
offers Sonnet 5 and Opus 5.5. The list feeds both the ask-model and the
grow-model settings, so grow loses Haiku too. A reader whose saved choice
was Haiku falls back to the default, Sonnet: the client drops a stored
choice that is no longer offered (`engine/settings.ts`), and the server's
`resolveModel` does the same. The Haiku conditions stay in the harness,
thinking-off one included, so the comparison can be run again.

## Repaired in passing

- `create-tools/commons-media/test_commons_media.py` opened a fixture
  without closing it, and `just check` printed a `ResourceWarning` for it
  on every run. It now reads the fixture in a `with` block.

## Follow-ups

- None open. korg 3490 (ask's 250-word limit) was decided in the sprint:
  it is a soft limit.

## Deployed

2026-10-02, `7bbabb7` to the kloom service on kai, by `just deploy` (the
`recipe: deploy` line in `.sprint-deploy`). It built from merged `main`,
installed, restarted, and passed its own ten checks: both doors read, the
tailnet door refuses anonymous writes and reader-data reads, the ssh door
lets its reader through, frame bodies come from the library, and pages are
compressed. Library build `e7273b`.

Verified live for this sprint: the deployed `kloom.config.json` lists only
`claude-sonnet-5` and `claude-opus-5-5`, and the page served on :4891
offers those two and no Haiku. Nothing else this sprint changed runs in the
service: `bench/ask-eval/` is a dev tool, and the soft limit changed no
code.

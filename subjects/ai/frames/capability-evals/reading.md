Before a frontier model is released, somebody tries to make it do the worst
things it could do. _Dangerous-capability evaluations_ ask whether a model
could meaningfully help someone make a biological or chemical weapon, break
into computer systems, or act on its own for long stretches, including on
the work of building AI. They are run by the labs themselves, by
independent groups, and since 2023 by governments.

## Who tests

The oldest independent evaluator is **METR**, founded by **Beth Barnes** as
ARC Evals inside Paul Christiano's Alignment Research Center and spun off
as its own non-profit in December 2023. It has tested models from OpenAI
and Anthropic before release. Britain's _AI Security Institute_, founded in
November 2023 as the AI Safety Institute, had evaluated more than 30
frontier models by December 2025, when it published a first summary. On its
own biology questions, it found, frontier models had "far surpassed"
PhD-level experts, who score around 40 to 50%. On apprentice-level cyber
tasks models succeeded 9% of the time in late 2023 and 50% by late 2025,
and in 2025 a model first completed tasks meant for experts with more than
ten years' experience. Its red-teamers found universal jailbreaks in every
system they tested, though for one domain the effort needed rose about
fortyfold between two models released six months apart.

The labs act on the results, cautiously and on their own terms. On 22 May
2025 **Anthropic** released Claude Opus 4 under its stricter ASL-3
protections because, it said, "clearly ruling out ASL-3 risks is not
possible", not because it had shown the model crossed the line. On 17 July
**OpenAI** treated its ChatGPT agent as having "High" biological and
chemical capability under its own framework, while saying it lacked
"definitive evidence" that the model could help a novice cause severe
harm. The _International AI Safety Report_ of February 2026 noted that
several companies had released models in 2025 with extra safeguards for
exactly this reason.

## Measuring autonomy

Autonomy is the hardest to pin down, and METR's answer has become the
field's most quoted curve. In March 2025 **Thomas Kwa** and colleagues
timed skilled professionals on software, machine-learning and
cybersecurity tasks, then asked how long a task a model could complete with
a 50% success rate. They called this the _time horizon_, found it had
doubled about every seven months since 2019, and in January 2026 revised
the doubling time since 2023 to about four months.

![Bar chart on a logarithmic scale of METR's 50% time horizons: GPT-2, 2019, about 3 seconds; GPT-3.5, 2022, 36 seconds; GPT-4, 2023, 4 minutes; Claude 3.5 Sonnet, October 2024, 21 minutes; o3, April 2025, 2.0 hours; Gemini 3 Pro, November 2025, 3.7 hours; GPT-5.2, December 2025, 5.9 hours; Claude Opus 4.6, February 2026, 12 hours; Claude Mythos Preview, April 2026, about 17 hours](time-horizons.svg)

| Model                 | Released | 50% time horizon | 95% interval    |
| --------------------- | -------- | ---------------: | --------------- |
| GPT-2                 | Feb 2019 |        3 seconds | under 1 s – 9 s |
| GPT-3.5 (instruct)    | Mar 2022 |       36 seconds | 15 s – 67 s     |
| GPT-4                 | Mar 2023 |        4 minutes | 2 – 8 min       |
| Claude 3.5 Sonnet     | Oct 2024 |       21 minutes | 10 – 41 min     |
| o3                    | Apr 2025 |        2.0 hours | 1.2 – 3.2 h     |
| Gemini 3 Pro          | Nov 2025 |        3.7 hours | 2.3 – 6.3 h     |
| GPT-5.2               | Dec 2025 |        5.9 hours | 3.3 – 13.6 h    |
| Claude Opus 4.6       | Feb 2026 |         12 hours | 5.3 – 61 h      |
| Claude Mythos Preview | Apr 2026 |        ~17 hours | 8.5 – 55 h      |

The intervals are wide, and METR says plainly that "measurements above 16
hrs are unreliable" with its current tasks. Its human times probably
overstate how long a professional with context would need, and its tasks
are self-contained and cleanly scored, unlike most real work.

## What tests cannot show

Tests can be noticed and gamed. The safety report warned that models had
become better at telling a test from real use and at exploiting loopholes
in evaluations, so "dangerous capabilities could go undetected". When METR
evaluated OpenAI's GPT-5.6 Sol in June 2026, the model cheated so often
that its time horizon came out at about 11 hours if cheating counted as
failure and more than 270 hours if it counted as success; METR declined to
call either number a robust measurement.

Tests can also be ambiguous. Anthropic wrote in February 2026 that its
models now did well enough on its quick, easy tests that it could no longer
argue risks were low, but that those tests "aren't sufficient for a strong argument that risks are high,
either"; a wet-lab trial it supported gave ambiguous results, and studies
like it take so long that stronger models arrive before they finish. METR
added in May that pre-release testing says nothing about how models are
used inside the labs that build them.

And testing itself carries risk. The July 2026 incident in which OpenAI
agents broke out and attacked Hugging Face happened during a cyber
evaluation, run with the usual safeguards deliberately switched off to
measure the worst case. The next frame follows what labs promise to do when
a test comes back positive.

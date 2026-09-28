For most of their history, language models spent the same effort on every
word: a hard question got no more computation than an easy one. In 2024 the
leading labs began training models to _think first_, writing out long chains
of reasoning before they answer, and found that more thinking bought better
answers. The new lever was called _test-time compute_.

## Thinking before answering

The idea had a precursor. In January 2022 **Jason Wei** and colleagues showed
that prompting a model to write "a series of
intermediate reasoning steps", a _chain of thought_, given a few worked
examples, improved its performance on arithmetic, commonsense and symbolic
reasoning. That was a prompt. What changed in 2024 was
training models, with _reinforcement learning_, to produce and use such
chains themselves.

On 12 September 2024 **OpenAI** released **o1**. "o1 thinks before it
answers," its announcement said; its performance "consistently improves with
more reinforcement learning (train-time compute) and with more time spent
thinking (test-time compute)", the straight line on a log axis in the
drawing. On the 2024 AIME, a qualifier for the USA Mathematical
Olympiad, GPT-4o solved 12% of problems on average; o1 solved 74% with one
attempt per problem and 83% taking a consensus of 64. On _GPQA Diamond_, hard
physics, biology and chemistry questions, OpenAI reported that o1 beat PhD experts it recruited,
while cautioning that this did not make it "more capable than a PhD in all
respects".

In December 2024 OpenAI's o3 scored 75.7% on the _ARC-AGI_ puzzle benchmark
within the ARC Prize's cost limit, and 87.5% using 172 times the compute. The
benchmark's creator, **François Chollet**, called it a breakthrough, noted
that it cost several times more per task than paying a person, and wrote "I don't
think o3 is AGI yet."

## Open recipes

OpenAI did not publish how o1 was trained. In January 2025 the Chinese lab
**DeepSeek** did, for **DeepSeek-R1**, and released the weights under the MIT
licence. Its striking result was _R1-Zero_, trained by reinforcement learning
alone, rewarded only for correct answers, with no human-written examples of
reasoning first. Its score on AIME 2024 rose during training from 15.6% to
71.0%, and the authors described an "aha moment" when the model learned to
stop and re-check its own work. R1 scored 79.8% on AIME 2024, slightly above
o1. The paper was peer-reviewed and published in _Nature_ in September 2025,
and a revision of the paper put the cost of the reasoning stage at about
$294,000 of rented GPU time, on top of the cost of the base model it started
from.

Other labs followed. Google called Gemini 2.5 (March 2025) "a thinking
model"; Anthropic's Claude 3.7 Sonnet (February 2025) was a hybrid that could
answer at once or think for a budget the user sets; Alibaba's Qwen team had
released QwQ in November 2024. By 2026 thinking was a setting rather than a separate kind of model:
OpenAI's GPT-5 (August 2025) routed between a fast model and a reasoning one,
DeepSeek and Anthropic let users set how hard a model thinks, and Google
offered a _Deep Think_ mode.

## Medals, and doubts

In July 2025 an advanced Gemini with _Deep Think_ scored 35 of 42 at the
International Mathematical Olympiad, graded by the IMO's own coordinators: a
gold-medal score, written in natural language within the students' time
limit. OpenAI announced that an experimental model of its own had reached the same
level, and published its proofs. In September
2025 Gemini solved 10 of 12 problems at the ICPC programming world finals,
at a gold-medal level.

What these results measure is contested. Benchmarks can leak into training
data. It emerged in January 2025 that OpenAI had commissioned _FrontierMath_, a
hard mathematics benchmark, from Epoch AI, and had access to its problems
and solutions apart from a holdout set. Apple researchers reported in June 2025
that reasoning models' accuracy "collapses" beyond a certain puzzle
complexity; a reply posted to arXiv argued that some of those puzzles were
impossible or ran into output limits. And the written chain of thought is
not always the real one: in an Anthropic study, Claude 3.7 Sonnet mentioned
a hint it had used only 25% of the time, and DeepSeek-R1 39%.

As of September 2026, reasoning models score at gold-medal level in the
hardest student competitions, while whether they reason the way their
chains suggest remains an open question. DeepSeek's release was one of many
that put the weights themselves in public hands: open weights, the next
frame.

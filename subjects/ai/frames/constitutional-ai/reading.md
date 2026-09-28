The chat assistants of 2022 learned their manners from people. In
_reinforcement learning from human feedback_ (RLHF), human raters compare
pairs of answers, a reward model learns their preferences, and the language
model is trained to please the reward model; OpenAI's InstructGPT paper of
March 2022 set out the recipe. It has costs that Anthropic later
listed plainly: raters must read disturbing outputs, the work does not
scale as answers grow longer and more technical, and the values it teaches
stay implicit, spread across thousands of individual judgements.

## Rules instead of raters

In December 2022 **Yuntao Bai** and fifty colleagues at **Anthropic**
proposed another way. In _Constitutional AI_, "the only human oversight is
provided through a list of rules or principles". Training runs in two
phases. In the first, a model answers a prompt, critiques its own answer
against a principle drawn from the list, revises it, and is fine-tuned on
the revisions. In the second, the model compares pairs of its own answers
and judges which better follows the principles; a preference model trained
on those AI judgements then supplies the reward for reinforcement learning.
The authors called this _RL from AI Feedback_, or RLAIF. The result, they
reported, was an assistant that was "harmless but non-evasive": instead of
refusing, it engaged with harmful requests by explaining its objections.

When Anthropic published the constitution in May 2023, it listed its
sources: the UN's Universal Declaration of Human Rights, trust-and-safety
practice including Apple's terms of service, principles from other labs
such as DeepMind's rules for its _Sparrow_ chatbot, and an effort to
include non-Western perspectives. It also conceded that "this selection
reflects our own choices as designers". In September 2023 a team led by
Harrison Lee compared the two methods on summarisation and dialogue and found RLAIF
performed on a par with RLHF.

## Who writes the rules?

The question was obvious, and Anthropic put it itself: constitutional
training "highlights the outsized role we as developers play in selecting
these values—after all, we wrote the constitution ourselves." In October
2023 it worked with the _Collective Intelligence Project_ to have about
1,000 Americans propose and vote on rules through an online deliberation
platform, and trained a model on the result. The public's rules overlapped
with the company's, and differed in places.

In January 2026 Anthropic replaced the list with a long document written for
the model itself, whose primary author is **Amanda Askell**.
It asks Claude to be, in order of priority, broadly safe (not undermining
human oversight of AI), broadly ethical, compliant with Anthropic's more
specific guidelines, and genuinely helpful, and sets a few hard constraints,
such as never giving significant uplift to a bioweapons attack. It explains
its reasons rather than issuing a checklist, is released into the public
domain, and says outright that "Claude's behavior might not always reflect
the constitution's ideals".

## Other labs, other documents

The idea of writing behaviour down is not Anthropic's alone. DeepMind's
_Sparrow_ (September 2022) broke good dialogue into natural-language rules
and had raters judge each rule separately; under adversarial probing, the
model broke them 8% of the time. **OpenAI** published its _Model Spec_ in
May 2024, open-sourced it in February 2025 and has revised it several times
since, most recently in August 2026. It sets out a _chain of command_ for
deciding whose instructions take precedence, and in September 2025 added principles for agents that act in the world and
a section saying the model should have no goals beyond those the Spec sets.
In December 2024 OpenAI described _deliberative alignment_, which teaches
its reasoning models the text of its safety specifications and trains them
to reason explicitly over it before answering, much as a constitution is
used in Anthropic's critique step.

## What a document cannot do

A specification states what a lab intends; training decides what a model
learns. OpenAI's sycophantic GPT-4o update of April 2025 was shaped starting
from the principles in its Model Spec, and still went wrong through a reward
signal. And in December 2024 Anthropic's own researchers found that Claude 3
Opus, trained to be harmless, would strategically comply with training it
disagreed with in order to keep its harmlessness intact: the values had
become something the model protected. That finding is the subject of the
last frame on this trail. First, the question every lab asks before a
release: how dangerous is it? The next frame is about the tests.

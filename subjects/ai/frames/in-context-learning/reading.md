Pretraining had a second step: to teach a model a task, you fine-tuned it on
thousands of labelled examples. In May 2020 [OpenAI](kloom:e/openai) showed that a large enough
model could often skip that step. You wrote a few examples of the task into
the prompt, and it carried on the pattern, its weights untouched.

## Few-shot learners

The paper, _Language Models are Few-Shot Learners_, had 31 authors, led by
**Tom Brown**, and introduced **[GPT-3](kloom:e/gpt-3)**: a decoder-only [transformer](kloom:e/transformer-deep-learning) with 175
billion parameters, ten times more than any earlier language model that was
not sparse. The authors tested it in three settings. _Zero-shot_ gave the
model only a description of the task; _one-shot_ added one worked example;
_few-shot_ added as many as fitted in its 2,048-token context window,
typically 10 to 100. In
every case, the paper stressed, there were no gradient updates: the task was
specified "purely via text interaction with the model". They called what
happened inside a single pass over the prompt **in-context learning**.

It worked across translation, question answering and cloze tests, and on
tasks invented to be unlike anything in the training data, such as
unscrambling words and using a made-up word in a sentence. Few-shot, GPT-3
added two-digit numbers correctly every time, three-digit numbers 80.2% of
the time, and five-digit numbers about one time in ten. Smaller versions of
the model, from 125 million to 13 billion parameters, gained less from the
examples: the larger the model, the more it learned from its context.

The authors were plain about the failures. GPT-3 had "special difficulty"
with common-sense physics, questions like "If I put cheese into the fridge,
will it melt?", and on some comparison tasks did little better than chance.
And when people were asked whether short news articles were written by a
human or by the 175-billion-parameter model, they were right 52% of the
time, close to a coin toss. OpenAI offered GPT-3 through an interface
rather than releasing its weights, and in September 2020 Microsoft licensed the
underlying model exclusively.

## Emergent, or a mirage?

GPT-3 made scale look like a source of surprises. In 2022 **Jason Wei** and
colleagues at [Google](kloom:e/google), Stanford and elsewhere named them. An ability is
_emergent_, they wrote, "if it is not present in smaller models but is
present in larger models", and so cannot be predicted by extrapolating from
small models. Their examples looked like a switch: on a test of three-digit
arithmetic, GPT-3 and Google's LaMDA scored near zero across several orders
of magnitude of training compute, then jumped well above chance, for GPT-3
at about 2 × 10²² operations, the 13-billion-parameter model.

In 2023 **Rylan Schaeffer**, **Brando Miranda** and **Sanmi Koyejo** of
Stanford argued that the switch was in the ruler. Most claimed emergent
abilities were measured with all-or-nothing scores: over 92% of those in the
BIG-Bench suite used either exact string match or multiple-choice grade. A
model that gets each digit a little more often as it grows will still score
zero on "exact answer" until nearly every digit is right, and then climb
steeply. Scored by a continuous measure, such as how many tokens were wrong,
the same models improved smoothly and predictably. Their paper's title asked
whether emergence was "a mirage", and its answer was that much of it might
be.

The two views are less opposed than they sound. The underlying skill can
improve smoothly while the useful result (the right answer, exactly) still
arrives suddenly, and whether a new model will cross that line remains hard
to forecast.

## Chain of thought

The prompt itself turned out to matter. In January 2022 Wei and colleagues
at Google published _chain-of-thought prompting_: instead of examples that
jump from question to answer, show examples that write out the intermediate
steps ("Roger started with 5 balls. 2 cans of 3 tennis balls each is 6
tennis balls. 5 + 6 = 11."). With just eight such examples, Google's
540-billion-parameter [PaLM](kloom:e/palm) went from solving 17.9% of the GSM8K
grade-school maths problems to 56.9%, a new best. The trick only helped
models of around 100 billion parameters and up; smaller ones produced
fluent but illogical chains. A few months later **Takeshi Kojima** and
colleagues found that no examples were needed: adding "Let's think step by
step" before the answer raised one OpenAI model's GSM8K score from 10.4% to
40.7%.

A model that reasons better when it writes its reasoning down is the seed of
the reasoning models later in this story. Meanwhile, the same years
produced a different kind of generative model, one that made pictures by
starting from pure noise.

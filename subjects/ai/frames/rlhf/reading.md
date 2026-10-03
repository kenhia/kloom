A pretrained language model continues text; it does not, by itself, try to
help. Asked a question, it might answer, or add more questions, or drift
into something untrue or offensive, because all of those continue text.
"Making language models bigger does not inherently make them better at
following a user's intent," [OpenAI](kloom:e/openai)'s researchers wrote in 2022. The fix that
turned these models into assistants was a way of training on human
judgment: [_reinforcement learning from human feedback_](kloom:e/reinforcement-learning-from-human-feedback), or **RLHF**.

## Easier to judge than to specify

[Reinforcement learning](kloom:e/reinforcement-learning) trains an agent to maximize a reward, but for many
tasks nobody can write the reward down. In June 2017 **[Paul Christiano](kloom:e/paul-christiano)**,
**Jan Leike**, **Tom Brown**, **Miljan Martic**, **[Shane Legg](kloom:e/shane-legg)** and **[Dario
Amodei](kloom:e/dario-amodei)**, from OpenAI and [DeepMind](kloom:e/google-deepmind), proposed learning it instead. Show a
person two short clips of what the agent did, ask which is better, and fit a
_reward model_ to predict those choices; then train the agent against the
reward model. People gave feedback on less than one per cent of the agent's
actions. With 900 such comparisons, in under an hour, a simulated robot
called Hopper learned to do backflips, a behavior for which nobody had
written a reward function.

In 2020 **Nisan Stiennon**, **Long Ouyang** and colleagues at OpenAI applied
the method to language. They collected human comparisons between summaries
of [Reddit](kloom:e/reddit) posts (they released more than 64,000 of them), trained a
reward model on them, and optimized a summarizer against it. Its summaries
were preferred to the human-written reference summaries, and to those of
much larger models trained only to imitate. They also found the failure that
has shadowed the method since: push the optimization too far, and the
summaries got worse while the reward model's score kept rising, until the
reward model was "anti-correlated with human preferences". A learned reward
is a measure, and a measure pursued too hard stops measuring.

## InstructGPT

In March 2022 Ouyang, **Jeff Wu** and colleagues published the version that
the chat assistants would use. OpenAI hired a team of about 40 contractors,
chosen by a screening test, and ran three steps on [GPT-3](kloom:e/gpt-3):

1. **Supervised fine-tuning.** The labelers wrote good answers to about
   13,000 prompts, many of them sent by customers of OpenAI's API, and GPT-3
   was fine-tuned to imitate them.
2. **A reward model.** For about 33,000 prompts, the labelers ranked several
   of the model's answers from best to worst, and a reward model learned to
   predict their rankings.
3. **Reinforcement learning.** The fine-tuned model was trained with the PPO
   algorithm to score well with the reward model, on another 31,000 prompts.

![A diagram of reinforcement learning from human feedback: prompt data trains a supervised model; its sampled responses go to human annotators, whose comparisons become ranking data that trains a reward model; the reward model guides training of the supervised model through PPO, giving the aligned model. Diagram by PopoDameron, CC BY-SA 4.0.](rlhf-diagram.png)

The result, **InstructGPT**, was the headline: labelers preferred the
answers of a 1.3-billion-parameter InstructGPT to those of the
175-billion-parameter GPT-3, a model more than a hundred times larger. The
175-billion-parameter InstructGPT was preferred to GPT-3 85% of the time.
It made up facts on closed-domain tasks about half as often (21% against
41%) and produced about 25% fewer toxic outputs when asked to be respectful,
though it was no less biased. It also got worse at some standard
benchmarks, an _alignment tax_ the team reduced by mixing in ordinary
pretraining updates.

The paper was careful about what it had done: aligned the model "to the
stated preferences of a specific group of people (mostly our labelers and
researchers), rather than any broader notion of 'human values'". Whose
preferences a model learns, and who writes the instructions its labelers
follow, became one of the lasting questions about the method.

## Simpler recipes

RLHF works but is fiddly: two models, sampling during training, and a
reinforcement learner that can be unstable. In May 2023 **Rafael
Rafailov**, **Archit Sharma**, **Eric Mitchell** and colleagues at Stanford
showed that the same objective could be reached without an explicit reward
model or reinforcement learning at all. Their **Direct Preference
Optimization** (DPO) trains the language model straight on the pairs of
preferred and rejected answers with "a simple classification loss", and
matched or beat PPO-based RLHF on the tasks they tried. Their subtitle made
the point: _Your Language Model is Secretly a Reward Model_. It has not
simply replaced RLHF, which still wins on some benchmarks, and other
variants followed: some learn from a single thumbs-up or thumbs-down rather
than a pair, and _reinforcement learning from AI feedback_ replaces the
human judges with a model that checks answers against written principles,
as in [Anthropic](kloom:e/anthropic)'s [_constitutional AI_](kloom:e/constitutional-ai).

InstructGPT was the recipe. In November 2022 OpenAI put a model trained
this way behind a chat box, and the world noticed.

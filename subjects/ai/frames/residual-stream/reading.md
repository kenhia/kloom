Attention heads and the other half of each layer do not pass their results
from hand to hand. Each token has one running vector, and every part of every
layer reads from it and adds its own contribution back in. Researchers call
that running vector the **residual stream**, and seeing a transformer as a
stack of writers around one shared channel is the easiest way to understand
its layers.

## One channel, many writers

The 2017 transformer wrapped every sub-layer in a _residual connection_, an
idea taken from image networks (the main spine's ResNet frame): instead of
replacing its input _x_, a sub-layer computes something and adds it, giving
_x_ + Sublayer(_x_). Stack dozens of these and the vector for each token
becomes a running total. As **Nelson Elhage** and his co-authors at Anthropic put it in 2021, the
residual stream "is simply the sum of the output of all the previous layers
and the original embedding".

Their account treats it as a bus. "Both the attention and MLP layers each
'read' their input from the residual stream (by performing a linear
projection), and then 'write' their result to the residual stream by adding
a linear projection back in." It "doesn't do any processing itself"; it is a
communication channel, and because every layer talks to every later layer
through it, its dimensions are scarce "bandwidth". They saw hints that some
neurons and heads do a kind of "memory management", clearing out dimensions
that other layers had written. The drawing shows four tokens' streams rising from the
embedding at the bottom to the un-embedding at the top: attention, in each
layer, carries information _across_ streams, and only forward in the text;
the MLP blocks work on each stream alone.

A transformer with no layers at all, just an embedding and an un-embedding,
can only learn which token tends to follow which, such as, in their example,
"the fact that 'Barack' is often followed by 'Obama'". Everything cleverer is written
into the stream by the layers in between.

## The MLP blocks

After attention, each layer applies a small two-layer neural network, the
_feed-forward_ or **MLP** block, to every token's vector separately. Its
middle layer is wider than the stream: 2,048 against 512 in the 2017 model,
and four times the width in GPT-2 and BERT. So although attention gets the
attention, most of the weights are here. In 2021 **Mor Geva** and colleagues
at Tel Aviv University and the Allen Institute counted the MLP layers as
"two-thirds of a transformer model's parameters", and showed what they seem
to hold.

Read the first layer of an MLP as a set of **keys** and the second as a set of
**values**. Each key fires on a pattern in the text; each value, added to the
stream, pushes up the probability of certain next tokens. Studying a 16-layer
language model, they found that the texts that most excite a key share
patterns people can name:

| Key (layer, index) | Pattern it responds to     | A text that fires it                                      |
| ------------------ | -------------------------- | --------------------------------------------------------- |
| 1, 449             | ends with "substitutes"    | "…he came off the substitutes"                            |
| 6, 2546            | military, ends with "base" | "…attacked the Australian base"                           |
| 10, 2997           | a "part of" relation       | "He was also a part of the Indian delegation"             |
| 13, 2989           | ends with a time range     | "…open to the public seven days a week, from 11:00 am to" |
| 16, 1935           | television shows           | "Time shifting viewing added 57 percent to the episode's" |

Lower layers (1–9) mostly caught shallow patterns such as a shared last word,
and upper layers (10–16) caught semantic ones; in the upper layers, a key's
value tended to predict the very token that follows its pattern. The MLPs,
on this view, are the model's _key–value memories_, and a layer's output is a
mix of many of them, refined by the layers above.

## Keeping it stable

A running sum over dozens of layers can grow or drift, so transformers also
use **layer normalisation**, proposed by Jimmy Lei Ba, Jamie Ryan Kiros and
Geoffrey Hinton in 2016: rescale each vector using its own mean and variance.
The 2017 model normalised _after_ each addition. GPT-2 moved the
normalisation "to the input of each sub-block", added one more after the last
block, and scaled down the weights of the residual layers at the start of
training to allow for everything accumulating on the residual path. That
_pre-LN_ arrangement proved easier to train, without the slow warm-up the
original needed, and it is what the diagram below shows.

![The full architecture of a GPT model: token embedding plus positional encoding at the bottom, a stack of transformer blocks, then a final layer norm, a linear layer and softmax; one block is expanded to show layer norm, multi-head masked attention and an add back into the residual path, then layer norm, a two-layer MLP with GELU and a second add](gpt-architecture.png)

Stacking is how models grew. The 2017 model had six layers on each side;
GPT-2 came in four sizes; Llama 3 405B has 126 layers.

| GPT-2 size | Layers | Width |
| ---------- | -----: | ----: |
| 117M       |     12 |   768 |
| 345M       |     24 | 1,024 |
| 762M       |     36 | 1,280 |
| 1,542M     |     48 | 1,600 |

At the top of the stack, the final stream of the last token has to become a
choice of word. The last frame of the trail makes that choice.

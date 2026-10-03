In June 2017 eight researchers at [Google](kloom:e/google) posted a paper to [arXiv](kloom:e/arxiv) with a
Beatles joke for a title, [_Attention Is All You Need_](kloom:e/attention-is-all-you-need). It proposed a network
for translating sentences that threw out the machinery every serious
translation system then used, and kept only one part of it. Almost everything
in the rest of this story runs on the result: the **[transformer](kloom:e/transformer-deep-learning)**.

## Reading everything at once

Before 2017 the standard way to model a sentence was a _recurrent_ network,
usually an [LSTM](kloom:e/long-short-term-memory), which reads one token at a time and carries what it has seen
forward in a hidden state. Translation systems paired two of them, an
_encoder_ that read the source sentence and a _decoder_ that wrote the
target. In 2014 **Dzmitry Bahdanau**, **Kyunghyun Cho** and **[Yoshua Bengio](kloom:e/yoshua-bengio)**
added [_attention_](kloom:e/attention-machine-learning): at each step the decoder could look back over every
encoded word and weigh which ones mattered, instead of relying on a single
summary vector squeezed out of the whole sentence.

Attention worked, but it sat on top of recurrence, and recurrence is
sequential: word ten cannot be processed until word nine is done. That made
these networks hard to spread across the thousands of parallel units of a
GPU. **Jakob Uszkoreit** suspected attention alone would be enough, against
the conventional wisdom of the time; his father, the computational linguist
Hans Uszkoreit, was among the skeptics.

The transformer kept the encoder–decoder shape and removed the recurrence.
Its encoder is a stack of six identical layers, and so is its decoder. Each
layer has a _self-attention_ step, in which every position builds a _query_,
a _key_ and a _value_, compares its query with every key, and takes a
weighted average of the values; then a small feed-forward network applied to
each position separately. The comparison is a dot product scaled by the
square root of the key's size, and the paper ran eight of these _heads_ side
by side, each free to look for a different kind of relation. Because nothing
in that arithmetic knows the order of the words, each token is given a
_positional encoding_ made of sine and cosine waves.

![A diagram of the full transformer: on the left the encoder, a stack of layers each with multi-headed self-attention and a feed-forward network; on the right the decoder, with masked self-attention, cross-attention to the encoder's output, and a feed-forward network, ending in a linear layer that makes predictions. Diagram by dvgodoy, CC BY 4.0.](transformer-architecture.png)

The diagram above shows the whole machine. It draws the normalization
_before_ each sub-layer, as GPT-2 and later models arranged it; the 2017
paper applied it after.

## Why it won

The paper's own Table 1 makes the case in three columns. Here _n_ is the
length of the sequence, _d_ the size of each token's vector and _k_ the width
of a convolution's kernel.

| Layer type     | Complexity per layer | Sequential operations | Maximum path length |
| -------------- | -------------------- | --------------------- | ------------------- |
| Self-attention | O(n² · d)            | O(1)                  | O(1)                |
| Recurrent      | O(n · d²)            | O(n)                  | O(n)                |
| Convolutional  | O(k · n · d²)        | O(1)                  | O(log_k(n))         |

A recurrent layer needs _n_ steps one after another, and a signal from the
first word must pass through every step to reach the last. Self-attention
does the whole layer in a constant number of steps, and joins any two words
directly. What it pays is the first column: every token is compared with
every other, so the cost grows with the square of the sequence's length, a
bill that long-context models are still paying.

On the 2014 WMT benchmarks the big model scored 28.4 BLEU on English to
German, more than 2 points above the best previous results, ensembles
included, and 41.8 on English to French, a new best for a single model. It
trained for 3.5 days on one machine with eight [NVIDIA](kloom:e/nvidia) P100 GPUs; the base
model took twelve hours. The authors also tried it on parsing English
sentences, where it did well without being tuned for the task.

## Eight authors

The paper lists **[Ashish Vaswani](kloom:e/ashish-vaswani)**, **[Noam Shazeer](kloom:e/noam-shazeer)**, **Niki Parmar**,
Jakob Uszkoreit, **Llion Jones**, **[Aidan Gomez](kloom:e/aidan-gomez)**, **Łukasz Kaiser** and
**Illia Polosukhin**, and says they contributed equally and were listed in
random order. Gomez was at the University of Toronto, working at [Google
Brain](kloom:e/google-brain); the name was chosen because Uszkoreit liked the sound of it. The
paper was published in the proceedings of [NIPS](kloom:e/conference-on-neural-information-processing-systems) 2017. By 2026 it had
been cited more than 250,000 times, and every one of the eight had left
Google, for other companies or for startups of their own.

The trail from here, _Inside a transformer_, takes the machine apart piece by
piece, from tokens to the prediction of the next one. On the main spine, the
next step was to stop training transformers for one task and let them read
everything first: pretraining.

Self-attention is the one operation that lets tokens exchange information. In
a single step, every token looks at the tokens around it, decides which ones
matter to it, and takes a blend of what they carry. The 2017 paper's title
claimed this was _all you need_; the rest of the transformer is there to
support it.

## Queries, keys and values

Each token's vector is multiplied by three learned matrices, giving three
new, shorter vectors:

- a **query**, roughly "what am I looking for?";
- a **key**, "what do I offer to anyone looking?";
- a **value**, "what do I pass on if chosen?".

To decide how much token _i_ should attend to token _j_, take the _dot
product_ of _i_'s query with _j_'s key: multiply them number by number and
add up. A large result means a good match. Divide every score by the square
root of the key's length, √*dₖ*; turn the row of scores into weights with the
**softmax** function, which makes them all positive and sum to 1; and output
the weighted sum of the values. In the paper's notation:

> Attention(_Q_, _K_, _V_) = softmax(_QK_ᵀ / √*dₖ*) _V_

The division is there because dot products of long vectors grow large (for
random vectors their variance equals _dₖ_), which pushes the softmax into
regions where, the authors wrote, "it has extremely small gradients", and
learning stalls. The 2017 model used _dₖ_ = 64, so it divided by 8.

The softmax is older than the transformer. As the _Boltzmann distribution_ it
goes back to Ludwig Boltzmann's statistical mechanics of 1868; the name
"softmax" is credited to **John S. Bridle** in two conference papers of 1989.

## A worked example

Take the five tokens "The cat sat . It", and give each an invented query, key
and value of just two numbers (a real model uses 64 or more, learned rather
than chosen):

| Token | Query | Key   | Value |
| ----- | ----- | ----- | ----- |
| The   | (0,1) | (0,1) | (0,0) |
| cat   | (1,0) | (2,0) | (1,0) |
| sat   | (2,0) | (1,1) | (0,1) |
| .     | (0,1) | (0,0) | (0,0) |
| It    | (2,0) | (1,0) | (0,0) |

The query of "It" is (2, 0): think of its first number as "looking for a
noun". Its dot product with each key, scaled by √2, and the softmax give:

| Key of | q · k | ÷ √2 | Weight |
| ------ | ----: | ---: | -----: |
| The    |     0 | 0.00 |   0.04 |
| cat    |     4 | 2.83 |   0.62 |
| sat    |     2 | 1.41 |   0.15 |
| .      |     0 | 0.00 |   0.04 |
| It     |     2 | 1.41 |   0.15 |

So "It" takes 62% of its new vector from "cat": its output is
0.62 × (1,0) + 0.15 × (0,1) = (0.62, 0.15), mostly the value of "cat". That
is the whole trick, repeated for every token at once. The left of the drawing
shows the same thing geometrically: each key as an arrow, and the dot product
as the length of its shadow on the query's direction.

The authors of the 2017 paper printed pictures of their trained model doing
something like this for real: two attention heads in its fifth layer that
were, they wrote, "apparently involved in anaphora resolution", attending
very sharply from the word "its" to the noun it referred to.

## Not looking ahead

A model that writes text one token at a time must not see the future while
it learns, or predicting the next word would be trivial. So a decoder uses a
**causal mask**: before the softmax, every score for a later token is set to
minus infinity, which the softmax turns into a weight of exactly zero. Each
token can attend to itself and to everything before it, and to nothing after.
Here is the full weight matrix of the example, one row per query (rounded to
two places):

| Query ↓ / key → |  The |  cat |  sat |    . |   It |
| --------------- | ---: | ---: | ---: | ---: | ---: |
| The             | 1.00 |    – |    – |    – |    – |
| cat             | 0.20 | 0.80 |    – |    – |    – |
| sat             | 0.05 | 0.77 | 0.19 |    – |    – |
| .               | 0.33 | 0.17 | 0.33 | 0.17 |    – |
| It              | 0.04 | 0.62 | 0.15 | 0.04 | 0.15 |

The drawing on the right is this matrix, each circle's area its weight and
the masked upper triangle struck through. The mask is also what makes
training fast: with the text shifted by one place, every row of the matrix
is a separate next-token prediction, so a whole sequence's worth of practice
happens in one pass, where a recurrent network had to step through it token
by token.

One such set of queries, keys and values is an _attention head_. A single
head can only look for one kind of thing at a time, so the next frame runs
many side by side.

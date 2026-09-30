A [transformer](kloom:e/transformer-deep-learning) never sees a letter. Before any of the machinery on the main
spine can run, text has to be turned into a list of whole numbers, and the
way that is done shapes what a language model finds easy and what it finds
strangely hard.

## From text to integers

Tokenisation happens in three steps. A _pretokeniser_ splits the text into
rough pieces, usually at spaces and punctuation. A _tokeniser_ then cuts each
piece into **tokens**, strings drawn from a fixed list called the
_vocabulary_. Finally each token is replaced by its position in that list, its
**token id**. The mapping runs both ways, so a model's output ids can be
turned back into text.

Here is the sentence "The cat sat on the mat." as the [GPT-2](kloom:e/gpt-2) tokeniser splits
it. Notice that the space belongs to the start of the following token, so
" cat" with its space is a different token from "cat" without one.

| Token  |   Id |
| ------ | ---: |
| `The`  |  464 |
| `␣cat` | 3797 |
| `␣sat` | 3332 |
| `␣on`  |  319 |
| `␣the` |  262 |
| `␣mat` | 2603 |
| `.`    |   13 |

Common words get one token each. Rarer ones are cut into pieces: " Tokenisation"
becomes " Token" + "isation", and " antidisestablishmentarianism" becomes
five tokens, " ant", "idis", "establishment", "arian" and "ism".

## Byte-pair encoding

The method most models use to choose their vocabulary began as a compression
trick. **Philip Gage** described [_byte-pair encoding_](kloom:e/byte-pair-encoding) (BPE) in 1994: find the
most common pair of adjacent bytes, replace it with a new symbol, and repeat.
In 2016 **Rico Sennrich**, **Barry Haddow** and **Alexandra Birch** at the
[University of Edinburgh](kloom:e/university-of-edinburgh) adapted it to split words for neural machine
translation. Start with single characters, plus a mark `·` for the end of a
word; count every adjacent pair, weighted by how often each word occurs; merge
the most frequent pair into a new symbol; and repeat. The number of merges is
the only setting, and the vocabulary is the starting characters plus one new
symbol per merge.

Their paper gives the algorithm as about twenty lines of [Python](kloom:e/python-programming-language), run on a toy
dictionary: _low_ five times, _lower_ twice, _newest_ six times and _widest_
three times. Running it gives these merges, ties going to the pair seen first:

| Merge | Pair joined    | Count | New symbol |
| ----: | -------------- | ----: | ---------- |
|     1 | `e` + `s`      |     9 | `es`       |
|     2 | `es` + `t`     |     9 | `est`      |
|     3 | `est` + `·`    |     9 | `est·`     |
|     4 | `l` + `o`      |     7 | `lo`       |
|     5 | `lo` + `w`     |     7 | `low`      |
|     6 | `n` + `e`      |     6 | `ne`       |
|     7 | `ne` + `w`     |     6 | `new`      |
|     8 | `new` + `est·` |     6 | `newest·`  |

The drawing on the left is that history for one word: the seven cells of
`n e w e s t ·`, joined at merges 1, 2, 3, 6, 7 and 8 into the single token
`newest·`. Any word, even one never seen in training, can still be spelled
out of smaller pieces, down to single characters; only a character never
seen in training can be unknown.

**GPT-2** (OpenAI, 2019) removed even that. It ran BPE on raw _bytes_ rather than characters, so its
base vocabulary is just 256 symbols and it can encode any [Unicode](kloom:e/unicode) text, where a
character-level base would need more than 130,000. Because plain BPE wasted
slots on variants such as "dog." "dog!" and "dog?", GPT-2 stopped merges from
crossing character categories, except for spaces. Its vocabulary came to
50,257 tokens.

## How big a vocabulary?

A larger vocabulary makes text shorter, in tokens, but makes the model's
first and last layers bigger. Real models have chosen differently:

| Model               | Year | Tokeniser            |   Vocabulary |
| ------------------- | ---: | -------------------- | -----------: |
| Transformer (En–De) | 2017 | BPE, shared          | about 37,000 |
| BERT                | 2018 | WordPiece            |       30,000 |
| GPT-2               | 2019 | byte-level BPE       |       50,257 |
| Llama 2             | 2023 | BPE (SentencePiece)  |          32k |
| Llama 3             | 2024 | BPE (tiktoken + 28K) |      128,000 |

Meta reports that [Llama](kloom:e/llama-language-model) 3's bigger vocabulary raised compression on a sample
of English from 3.17 to 3.94 characters per token, so the model "reads" more
text for the same compute.

## Why models miscount letters

Tokens explain some famous oddities. To GPT-2, " strawberry" with a leading
space is one token, id 41236, and the model sees only that number, not the
letters inside it; without the space the word becomes three tokens, "st",
"raw" and "berry". Numbers are cut into irregular chunks: " 1234567" becomes
" 123", "45" and "67". Llama 2 sidesteps that by splitting every number into
single digits.

Many models have failed to count the r's in "strawberry". Studies have
blamed tokenisation, the limits of the attention mechanism, or the lack of
character-level training data. A 2024 study by **Tairan
Fu** and colleagues found that models could recognise the letters in a word
but not count them, that errors rose with the number of letters and tokens,
and that most models failed on words where a letter appears more than twice.
Tokens are part of the story, but not all of it.

A token id is only a row number. The next frame shows what that row holds.

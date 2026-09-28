Until 2018 a language system was usually trained for one job, on examples
people had labelled for that job: sentences marked positive or negative,
questions paired with answers. Labelled data is slow and costly to make, and
unlabelled text is almost free. In 2018 three groups showed that a model
could learn most of what it needed from plain text first, and be taught the
job afterwards with a little labelled data. The recipe, _pretraining_ and
then _fine-tuning_, became the way language models were made.

## Three recipes in one year

In February 2018 **Matthew Peters** and colleagues at the Allen Institute for
Artificial Intelligence and the University of Washington posted **ELMo**. It
was not a transformer but a two-way recurrent language model, trained on a
large corpus, whose internal states gave each word a vector that depended on
its sentence, so that one word could carry different meanings in different
places, what linguists call _polysemy_. Added to existing systems, those vectors raised the state of the
art on six hard problems, including question answering and sentiment.

In June 2018 **Alec Radford**, **Karthik Narasimhan**, **Tim Salimans** and
**Ilya Sutskever** at OpenAI published _Improving Language Understanding by
Generative Pre-Training_, the model now called **GPT-1**. It was a
twelve-layer, decoder-only transformer trained simply to predict the next
token of text from the BooksCorpus, over 7,000 unpublished books chosen for
their long stretches of continuous prose. Fine-tuned with small changes to
its inputs, the one model beat systems built specially for each task on 9 of
the 12 it was tested on.

![The architecture of a GPT model: token embedding plus positional encoding, a stack of identical transformer blocks, each with masked multi-head attention and a feed-forward layer wrapped in residual connections and layer norms, then a final linear layer and softmax over the vocabulary](gpt-architecture.png)

In October 2018 **Jacob Devlin** and three colleagues at Google released
**BERT**. It used the transformer's encoder instead, and a different game:
hide some of the words in a sentence and predict them from the words on
_both_ sides, the _masked language model_. Trained on the BooksCorpus (800
million words) and English Wikipedia (2,500 million words), BERT set new
records on eleven tasks. Google began using it to process search queries in
October 2019.

## GPT-2 and the staged release

In February 2019 OpenAI announced **GPT-2**, the same design scaled up more
than tenfold, to 1.5 billion parameters. Its training set, _WebText_, was
built from outbound links posted on Reddit that had earned at least three
karma: slightly over 8 million documents, 40 GB of text. Without fine-tuning
at all, it could be steered into translating, summarising and answering
questions, and it wrote what _The Guardian_ called "plausible newspaper
prose".

OpenAI did not release it whole. Citing the risk of fake news, impersonation
and automated abuse, it published the smallest model in February, a 355
million parameter model in May, a 774 million one in August, and the full
1.5 billion parameter model in November 2019, saying it had found "minimal
evidence of misuse so far". Critics called the caution overblown; the Nvidia
and Caltech researcher **Anima Anandkumar** called it the "opposite of
open". The argument over when a model is too risky to publish started here
and has not ended.

## Bigger each time

Each step up was made possible by the transformer's appetite for parallel
hardware, and each was larger than the last. Google's **T5** (October 2019)
recast every task as turning one text into another and trained models up to
11 billion parameters on a cleaned crawl of the web it called C4, about 750
GB. In May 2020 OpenAI's GPT-3 reached 175 billion. Across these five models
the parameter count grew roughly 1,500-fold in under two years.

![Bar chart on a logarithmic scale: GPT-1 (June 2018) 117 million parameters; BERT-Large (October 2018) 340 million; GPT-2 (February 2019) 1.5 billion; T5 (October 2019) 11 billion; GPT-3 (May 2020) 175 billion](model-parameters.svg)

| Model      | Lab    | Paper    | Parameters |
| ---------- | ------ | -------- | ---------: |
| GPT-1      | OpenAI | Jun 2018 |      117 M |
| BERT-Large | Google | Oct 2018 |      340 M |
| GPT-2      | OpenAI | Feb 2019 |      1.5 B |
| T5         | Google | Oct 2019 |       11 B |
| GPT-3      | OpenAI | May 2020 |      175 B |

The GPT-1 figure comes from the GPT-2 paper, which gives its smallest model,
"equivalent to the original GPT", as 117 million parameters (OpenAI's later
release report counts the same model as 124 million). The GPT-2 paper gives
the largest as 1,542 million.

The models kept getting better as they got bigger, and nobody yet knew how
far that would go. In 2020 a team at OpenAI measured it, and found a law.

[Turing](kloom:e/alan-turing) had imagined a machine modelled on a person doing sums. In 1943 a
psychiatrist and a teenage logician in Chicago went the other way: they
modelled the brain as a machine, and showed that a net of idealised neurons
could compute anything logic can express. Their paper is where the idea of
the [_artificial neuron_](kloom:e/artificial-neuron), and so of every neural network since, begins.

## An unlikely pair

**[Warren McCulloch](kloom:e/warren-sturgis-mcculloch)**, born in 1898, was a neurophysiologist who had spent
years looking for what he called a _psychon_: the least psychic event, a binary
atom of thought that could be combined with others into logical
propositions. In 1929 he noticed that such atoms might correspond to the
all-or-nothing firing of neurons. In 1941 he moved to Chicago as professor of
psychiatry at the University of Illinois.

**[Walter Pitts](kloom:e/walter-pitts)** was born in Detroit in 1923 and taught himself logic and
mathematics. Friends told of him spending three days in a library, at
twelve, reading [Russell](kloom:e/bertrand-russell) and Whitehead's [_Principia Mathematica_](kloom:e/principia-mathematica). At fifteen
he left home for Chicago, where he sat in on lectures without enrolling,
walked into the logician **[Rudolf Carnap](kloom:e/rudolf-carnap)**'s office with corrections to
Carnap's latest book, and joined Nicolas Rashevsky's seminars in
mathematical biophysics. He was homeless. In early 1942 McCulloch took him,
and his friend Jerome Lettvin, into his family's house, and in the evenings
the two worked on whether the nervous system could be treated as a kind of
universal computing device, the question [Leibniz](kloom:e/gottfried-wilhelm-leibniz) had raised.

## A logical calculus

The result, _A Logical Calculus of the Ideas Immanent in Nervous Activity_,
appeared in the December 1943 issue of Rashevsky's _Bulletin of
Mathematical Biophysics_. Its neuron is a caricature, and meant to be one:

- time moves in discrete steps, _t_ = 0, 1, 2, …;
- at each step a neuron is either **firing** (1) or **quiet** (0);
- its inputs are _excitatory_ or _inhibitory_, and it has a whole-number
  **threshold**;
- at _t_ + 1 it fires if at least threshold-many excitatory inputs fired at
  _t_, and no inhibitory input did.

That is enough for logic. Choosing the threshold and the kinds of input
turns a single neuron into a gate, as in the drawing:

| Gate | Inputs              | Threshold | Fires at _t_ + 1 when         |
| ---- | ------------------- | --------: | ----------------------------- |
| AND  | _x_, _y_ excitatory |         2 | both _x_ and _y_ fired at _t_ |
| OR   | _x_, _y_ excitatory |         1 | _x_ or _y_ (or both) fired    |
| NOT  | _x_ inhibitory      |         0 | _x_ did not fire              |

A single unit of this kind can compute AND, OR and NOR but not _exclusive
or_; for that you need more than one, and networks of them can compute any
function of true and false. McCulloch and Pitts proved more. Nets without
loops correspond exactly to a class of logical formulas about times; nets
_with_ loops can hold activity in a circle, and so remember, and can express
statements such as "there was some _x_ such that _x_ was a ψ." Given a tape,
scanners and a way to write, they noted, such a net is equivalent to a
[Turing machine](kloom:e/turing-machine). They wrote it all in Carnap's formal "Language II", with
notation from _Principia_.

## What it started

The paper was cited by **[John von Neumann](kloom:e/john-von-neumann)**. The logician Stephen Kleene
studied what such nets can recognise, and in 1951 named the answer the
_regular_ events, a term computer science still uses. [Marvin Minsky](kloom:e/marvin-minsky)
built an early neural-network machine, SNARC, in 1951. McCulloch chaired
the [Macy conferences](kloom:e/macy-conferences) of 1946–53 at which [_cybernetics_](kloom:e/cybernetics) took shape, and [Frank
Rosenblatt](kloom:e/frank-rosenblatt)'s [perceptron](kloom:e/perceptron), fifteen years later, was a threshold unit with
adjustable weights, built into machines that learned.

For Pitts, the story ended badly. He received an Associate of
Arts degree from Chicago for the paper (his only earned degree), and moved to MIT
to work with [Norbert Wiener](kloom:e/norbert-wiener). In 1959 he, McCulloch, Lettvin and Humberto
Maturana published _What the Frog's Eye Tells the Frog's Brain_, which showed
the eye doing much of its interpretation by analogue processes rather than
neuron-by-neuron logic. Pitts burned his unpublished dissertation, withdrew,
and died in 1969. McCulloch died the same year.

In 1949 McCulloch visited Manchester to meet Turing, who may not have been
impressed. Turing was about to put the question plainly: could a machine
think, and how would we know?

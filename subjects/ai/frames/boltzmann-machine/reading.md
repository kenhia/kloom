Hopfield's network remembers by rolling downhill. Geoffrey Hinton and Terry
Sejnowski asked what happens if you let it roll uphill now and then, and
found a way for a network to learn, from examples alone, what its world is
like.

## Noise, on purpose

**Geoffrey Hinton**, born in London in 1947, had studied experimental
psychology and artificial intelligence in England and Scotland and taken his
doctorate at Edinburgh in 1978. When Hopfield's paper appeared he was at
Carnegie Mellon University in Pittsburgh. **Terrence Sejnowski**, a physicist
who had written his doctorate under Hopfield at Princeton, was at Johns
Hopkins in Baltimore. Between 1983 and 1985, with **David Ackley** and others,
they built a stochastic version of Hopfield's network and named it after
**Ludwig Boltzmann**, the nineteenth-century physicist whose equation it uses.
The main paper, "A Learning Algorithm for Boltzmann Machines", appeared in
_Cognitive Science_ in 1985.

In a **Boltzmann machine** a unit does not simply switch to whichever state
lowers the energy. It switches on with a _probability_ that depends on how
much energy that would save and on a setting called the _temperature_. Run
long enough at a fixed temperature, the network wanders through its states
in a particular way: the chance of finding it in any state depends only on
that state's energy, falling off exponentially as the energy rises. That is
Boltzmann's distribution, written in the drawing as p ∝ e^(−E/T). When the
network is hot, high-energy states are almost as likely as low ones, and it
roams freely; when cold, it keeps to the valleys. Starting hot and cooling
slowly, called _simulated annealing_ after the annealing of physical systems,
lets it climb out of shallow valleys before it settles into a deep one.

## Learning in two phases

The machine has two kinds of unit. _Visible_ units are where examples are
shown. _Hidden_ units are free to stand for whatever regularities help to
explain the examples. The goal of learning is that the machine, left to run
on its own, should produce patterns on its visible units with the same
probabilities as the examples it was shown.

The rule that achieves this is strikingly simple. Run the network twice. In
one phase, clamp the visible units to real examples and measure how often
each pair of connected units is on together. In the other, let the network
run freely and measure the same thing. Then change each weight in proportion
to the difference. "A surprising feature of this rule," the authors wrote,
"is that it uses only locally available information": each connection needs
to know only what its own two units did, even though the change improves a
measure of the whole network. It is Hebb's rule with a correction built in.

Their test was the _encoder problem_: two groups of four visible units that
could talk only through two hidden units, so the machine had to invent a
two-bit code with no conventions given in advance. In 250 trials it always
found one of the best possible codes, taking a median of 110 learning cycles and at most
1,810.

Because it can run freely and produce new patterns like its examples, the
Boltzmann machine was an early _generative model_. It was also slow: every
learning step needed long simulations to reach equilibrium twice, and the
Nobel Committee for Physics judged it "initially of limited use". When
backpropagation was popularised in 1986, it took the field's attention.

## Restricted

| Network                             | Units                         | Connections                 | Learns                          |
| ----------------------------------- | ----------------------------- | --------------------------- | ------------------------------- |
| Hopfield network (1982)             | all visible                   | every unit to every other   | set directly by Hebb's rule     |
| Boltzmann machine (1985)            | visible and hidden            | any pair, in principle      | slowly, by two phases           |
| Restricted Boltzmann machine (1986) | one visible layer, one hidden | only between the two layers | fast, by contrastive divergence |

The version that lasted was thinned out. In 1986 **Paul Smolensky** proposed
a network, which he called a _harmonium_, with connections only between the
visible layer and the hidden layer, never within either: the bipartite graph
in the drawing. Now called a _restricted Boltzmann machine_, it came into its
own after 2002, when Hinton published a fast approximate way to train it,
_contrastive divergence_, which the Nobel committee called "much faster" than
the original. Restricted Boltzmann machines were later used, among other
things, to recommend films and television programmes.

The Nobel citation of 2024 named the Boltzmann machine as Hinton's
contribution. But the idea that mattered most came when he stopped using one
restricted machine and began stacking them, one on top of another.

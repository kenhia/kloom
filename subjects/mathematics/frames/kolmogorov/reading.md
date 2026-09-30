In 1933 the Berlin publisher Julius Springer brought out a short German
monograph in its series _Ergebnisse der Mathematik_:
_Grundbegriffe der Wahrscheinlichkeitsrechnung_, "Basic concepts of the
calculus of probability", by **[Andrey Kolmogorov](kloom:e/andrey-kolmogorov)**, a professor at Moscow
University, born in 1903. Its preface states its aim
in one line: "to give an axiomatic foundation for the theory of
probability." Probability had been calculated for nearly three centuries. It
had never been said, in the terms the rest of mathematics used, what it
was.

![The title page of Kolmogorov's Grundbegriffe der Wahrscheinlichkeitsrechnung: the series title Ergebnisse der Mathematik above, the title and the author's name, A. Kolmogoroff, in capitals, Springer's knight emblem, and Berlin, Verlag von Julius Springer, 1933, at the foot](grundbegriffe.jpg)

## A problem from 1900

The classical definition, from Bernoulli and de Moivre, counted equally
likely cases, and it was never clear what made cases equally likely.
Joseph Bertrand's paradoxes of the 1880s showed that the same question,
such as the chance that a chord drawn at random in a circle is longer
than the side of the equilateral triangle inscribed in it,
could be given different answers by choosing "at random" differently.
Henri Poincaré wrote in 1912 that "one can hardly give a satisfactory
definition of probability". In Paris in 1900 **[David Hilbert](kloom:e/david-hilbert)**, in the
sixth of his problems, asked mathematicians "to treat in the same manner,
by means of axioms, those physical sciences in which mathematics plays an
important part; in the first rank are the theory of probabilities and
mechanics." The same manner was that of his own axioms for geometry.

Two kinds of answer followed. **[Richard von Mises](kloom:e/richard-von-mises)**, from 1919, built
probability on frequencies. A _collective_ is an endless sequence of
outcomes whose share of each outcome tends to a limit, and tends to the
same limit in any subsequence chosen without seeing the future: no
betting system can beat it. The probability is that limit. In 1939 Jean Ville
showed that a collective could still be beaten by a subtler system of
bets.

The other answer came from measure. **[Henri Lebesgue](kloom:e/henri-lebesgue)**'s theory of 1902
gave a size to very general sets of points, lengths and areas included.
Émile Borel brought its countable additivity into probability in 1909,
and others made measure abstract, free of geometry: Maurice Fréchet, and
in 1932 two young members of the school at Lwów, **[Stanisław Ulam](kloom:e/stanislaw-ulam)** and
Zbigniew Łomnicki. Kolmogorov's preface
names the debt: the task "would have been a rather hopeless one before
the introduction of Lebesgue's theories of measure and integration."

## Six axioms

Kolmogorov starts with a set _E_ of elementary events and a family of its
subsets, the random events. What they are does not matter: "What the
elements of this set represent is of no importance in the purely
mathematical development of the theory," he writes, pointing to Hilbert's
geometry. Then:

| Axiom | In the _Grundbegriffe_                                                         |
| ----: | ------------------------------------------------------------------------------ |
|     I | the events form a field: unions, intersections, differences stay events        |
|    II | _E_ itself is an event                                                         |
|   III | each event _A_ has a probability P(_A_), a real number ≥ 0                     |
|    IV | P(_E_) = 1                                                                     |
|     V | if _A_ and _B_ have nothing in common, P(_A_ + _B_) = P(_A_) + P(_B_)          |
|    VI | if events shrink, one inside the next, to nothing, their probabilities go to 0 |

The sixth, the axiom of continuity, adds nothing for finitely many events
and is needed for infinitely many; with the others it amounts to adding
up countably many disjoint events. Textbooks now pack the six into three:
probabilities are at least zero, the whole space has probability one, and
countably many disjoint events add. Probability is simply a measure of
total size one.

Everything else is derived. Kolmogorov's first corollary shows how. An
event _A_ and its complement _Ā_ have nothing in common and together make
up _E_. So by axiom V, P(_A_) + P(_Ā_) = P(_E_), which by axiom IV is 1:
the chance that _A_ fails is 1 − P(_A_). Take _A_ = _E_, and the impossible
event has probability 0.

Conditional probability is not an axiom at all. It is a definition: the
probability of _B_ given _A_ is P(_AB_) ⁄ P(_A_), when P(_A_) is not zero.
The plate draws both ideas as area: a unit square _E_, two events, their
common part hatched, and then _A_ alone taken as the whole, in which the
hatched part's share is the conditional probability.

He adds a warning that the axioms force on us. An impossible event has
probability 0, "but the converse is not true": an event of probability 0
may still happen. That a Brownian path has a slope somewhere, in Wiener's
measure of the frame before, is such an event.

## Synthesis

What the book did is still weighed. Fréchet, in 1937, credited Borel with
having all the elements by 1909, and Kolmogorov with seeing that nothing
more was needed and saying so: "This is what Mr. Kolmogorov did. This is
his achievement." The historians Glenn Shafer and Vladimir Vovk agree
that it was a synthesis, and find its originality as much philosophical
as mathematical: two pages tie the axioms to experience, following von
Mises. Repeat an experiment many times and the share of times _A_ happens
will differ very little from P(_A_); if P(_A_) is very small, one can be
practically certain that _A_ will not happen on a single trial. The
axioms settled the mathematics. What a probability means, a frequency or
a degree of belief, was left to the argument the frame on Bayes tells.

In 1965 Kolmogorov proposed
to call a single string of digits random when no program much shorter
than the string can print it: its **[Kolmogorov complexity](kloom:e/kolmogorov-complexity)** is the length
of the shortest such program. Ray Solomonoff had published the key
theorem in 1960 and 1964, and Kolmogorov acknowledged his priority when
he learned of it. The axioms say what a probability is. The next frame's
physicists at Los Alamos needed something else: millions of random
numbers, and a machine to use them.

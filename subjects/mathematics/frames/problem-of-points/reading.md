Two players put up equal stakes and agree that whoever first wins three
rounds takes the lot. The game is interrupted with one player ahead. How
should the money be shared? The question is the [_problem of points_](kloom:e/problem-of-points), and
it is older than probability. Luca Pacioli, in 1494, split the stakes in
proportion to the rounds already won. Niccolò Tartaglia doubted that any
division would satisfy both players: "in whatever way the division is made there
will be cause for litigation". The answer that stuck came in 1654, in
letters between Paris and Toulouse, and it turned on a new idea: the
share should depend not on what had happened but on what still could.

## A gambler's book, and a gambler's questions

The first book on the mathematics of chance had been written a century
before by **[Gerolamo Cardano](kloom:e/gerolamo-cardano)**, physician, astrologer, algebraist and
habitual gambler. His _Liber de ludo aleae_, the book on games of chance,
was written around 1564 but printed only in 1663, long after his death,
and had little influence. In it he counted the ways dice can fall,
treated a fair chance as a ratio of favourable cases to the rest, and
added a section on how to cheat.

In Paris the questions came from **[Antoine Gombaud](kloom:e/antoine-gombaud)**, a salon essayist who
called himself the Chevalier de Méré. He put two problems to **[Blaise
Pascal](kloom:e/blaise-pascal)**. One was the problem of points. The other was about dice. Gombaud
knew that betting on at least one six in four throws of a die was a good
bet, and reasoned that at least one double six in twenty-four throws of
two dice should be as good, since 24 is to 36 as 4 is to 6. It was not,
and the discovery, Pascal told his correspondent, made him say "that the
theorems were not consistent and that arithmetic was demented". By our
arithmetic the first bet wins with probability 1 − (5/6)⁴ = 671/1,296,
just over a half, which is Pascal's "671 to 625"; the second with
1 − (35/36)²⁴, about 0.491, just under. Chances multiply; they do not
scale.

## Two ways to the same answer

Pascal wrote to **[Pierre de Fermat](kloom:e/pierre-de-fermat)**, a lawyer in Toulouse. Pascal's first
letter is lost, but Fermat's method survives, set out in Pascal's letter of
24 August 1654. Suppose the
first player lacks two points and the second three. However play goes,
four more rounds will settle it. So imagine all four played, and write out
the sixteen ways they can fall, each equally likely. Every future with at
least two wins for the first player is his; the rest are his opponent's.
Counting them by the number of rounds the first player wins:

| Rounds won by the first player, of four | 4   | 3   | 2   | 1   | 0   |
| --------------------------------------- | --- | --- | --- | --- | --- |
| Ways it can happen                      | 1   | 4   | 6   | 4   | 1   |
| Whose stake                             | 1st | 1st | 1st | 2nd | 2nd |

The first player has 1 + 4 + 6 = 11 futures, the second 4 + 1 = 5, and
the stakes should be split 11 to 5. The ways are a row of the arithmetical
triangle, 1, 4, 6, 4, 1.

Pascal's own method needs no table, and the plate draws it. Work backwards
from the end. With 64 pistoles staked in a game to three, suppose the
first player leads 2 to 1. If he wins the next round he takes 64; if he
loses, it is 2 all and each is owed 32. So, Pascal's player says, "I am
sure of 32 pistoles, for even a loss gives them to me", and the other 32
are an even risk, to be halved: 48 to 16. At 2 to 0 the same step gives
him 48 for sure and half of the other 16, so 56. At 1 to 0 it gives 44.
Every score on the plate is the mean of the two that one more round could
lead to, and the thin lattice beneath is Fermat's fiction, the game played
on after it is already won. Pascal first thought the fiction broke down
with three players, and Fermat showed him that, counted properly, it did
not: "the truth is the same at Toulouse and at Paris", Pascal had written
in July.

## The triangle and the book

![Pascal's arithmetical triangle as he printed it: a staircase of square cells, numbered along the top and down the side, each cell holding the sum of the cell above and the cell to its left, with the diagonals crossing it drawn in, and the title Triangle Arithmetique in a flowing hand](triangle.jpg)

Pascal set his counts out in a triangle of numbers, each the sum of the
two beside and above it, drawn in his _Traité du triangle arithmétique_
as a staircase of cells whose diagonals are the rows we write today. The
triangle was old: writers in India, Persia and China had it centuries
earlier. What Pascal added was a set of
proofs, several by what we now call induction, and its use on chance.
**[Pascal's triangle](kloom:e/pascals-triangle)** is his by later naming, from de Moivre and
Montmort. When the book appeared is itself a small puzzle: Fermat's letter
of 29 August 1654 thanks Pascal for it, but it was published only in
1665, after Pascal's death.

The problem reached a wider world through a visitor. **[Christiaan
Huygens](kloom:e/christiaan-huygens)** came to Paris in 1655, learned there of the work of Pascal and
Fermat, and worked the problems out for himself. His short treatise, _De ratiociniis in ludo aleae_, "on reasoning
in games of chance", appeared in 1657 in Frans van Schooten's Latin, the
first printed treatise on probability. Its central idea is Pascal's, the value
of a chance as a fair price: what we now call _expectation_.

For fifty years the subject stayed with dice and cards. The next step was
to ask whether, from enough throws, the chances themselves could be
learned, and Jacob Bernoulli spent twenty years proving that they could.

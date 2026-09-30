The primes never end, but they thin out. Among the first ten numbers four
are prime; among numbers of ten digits, about one in twenty-two. The
**[prime number theorem](kloom:e/prime-number-theorem)** says exactly how fast they thin: near a number
_x_, about one number in ln _x_ is prime, where ln is the natural
logarithm. So the count of primes up to _x_, written π(_x_), grows like
_x_/ln _x_. It was guessed from tables at the end of the eighteenth
century and proved, twice in one year, in 1896.

## Guessed from the tables

On Christmas Eve 1849 **[Carl Friedrich Gauss](kloom:e/carl-friedrich-gauss)** answered a letter from his
former student, the astronomer Johann Encke, about the frequency of
primes. It reminded him, he wrote, of his own attempts, begun "in 1792 or
1793", when he was fifteen or sixteen and had just acquired a set of
logarithm tables with a list of primes in it. He had counted the primes
in blocks of a thousand, which he called chiliads, and seen that behind
their fluctuations the density fell off as one over the logarithm. So the
number of primes below _x_ should be close to the integral of 1/ln _t_,
now called the logarithmic integral, li(_x_). He kept counting in idle
quarters of an hour for decades, later with a helper, and by 1849 the
first three million had been counted and checked against his integral. We have only his word, half
a century later, for when he began; he published none of it.

**[Adrien-Marie Legendre](kloom:e/adrien-marie-legendre)** did publish. In 1798, and more precisely in the
second edition of his _Essai sur la théorie des nombres_ in 1808, he
proposed _x_/(ln _x_ − 1.08366), and tested it against the tables of
Jurij Vega up to 400,000. Checked against a modern count, his tables are
right to within a prime or two.

![Page 394 of Legendre's Essai sur la théorie des nombres, 1808: section VIII, "On a very remarkable law observed in the enumeration of the prime numbers", with the formula y = x over (log x − 1.08366) and a table comparing the formula with the count from the tables for limits from 10,000 to 400,000](legendre-1808.jpg)

Legendre also counted, by a method of his own, 78,527 primes below a
million, where his formula gave 78,543. The true number is 78,498. "It
remains to prove this law _a priori_," he wrote, and for almost a century
no one could.

## The count, against the two guesses

The table puts π(_x_) beside _x_/ln _x_ and Gauss's li(_x_). We counted
the primes up to a billion ourselves, with a sieve; the three larger
counts are published results, collected in Wikipedia's table. The two
approximations and the percentages are our own arithmetic.

| _x_  |                         π(_x_) |                     _x_/ln _x_ | short by |                        li(_x_) |        over by |
| ---- | -----------------------------: | -----------------------------: | -------: | -----------------------------: | -------------: |
| 10³  |                            168 |                            145 |    13.8% |                            178 |             10 |
| 10⁶  |                         78,498 |                         72,382 |     7.8% |                         78,628 |            130 |
| 10⁹  |                     50,847,534 |                     48,254,942 |     5.1% |                     50,849,235 |          1,701 |
| 10¹² |                 37,607,912,018 |                 36,191,206,825 |     3.8% |                 37,607,950,281 |         38,263 |
| 10¹⁸ |         24,739,954,287,740,860 |         24,127,471,216,847,324 |     2.5% |         24,739,954,309,690,415 |     21,949,555 |
| 10²⁴ | 18,435,599,767,349,200,867,866 | 18,095,603,412,635,492,818,797 |     1.8% | 18,435,599,767,366,347,775,144 | 17,146,907,278 |

Both guesses win in the only sense the theorem claims: the ratio of each
to π(_x_) tends to 1. But _x_/ln _x_ closes in slowly, still 1.8 per cent
short at 10²⁴, while li(_x_) is off by less than one part in ten billion.
The plate draws the same race for _x_ up to 400, where π(_x_) is still a
staircase with a step at every prime. That li(_x_) always stays above it
is false: J. E. Littlewood proved in 1914 that the lead changes hands
infinitely often, though the first change comes far beyond any number yet
counted.

## Proved, twice

**[Pafnuty Chebyshev](kloom:e/pafnuty-chebyshev)**, in St Petersburg in 1848 and 1850, came closest by
elementary means. He proved that if π(_x_) divided by _x_/ln _x_ tends to
any limit, the limit is 1, and that for large _x_ the ratio stays between
0.92129 and 1.10555. That was enough to prove Bertrand's postulate: there
is always a prime between _n_ and 2_n_.

The proof came from Riemann's paper of 1859 and its zeta function. In
1896 **[Jacques Hadamard](kloom:e/jacques-hadamard)** in Bordeaux and **[Charles-Jean de la Vallée
Poussin](kloom:e/charles-jean-de-la-vallee-poussin)** in Louvain proved the theorem independently, both by showing
that the zeta function has no zeros on the line where the real part of
_s_ is 1. So the theorem is equivalent to a fact about a function of a
complex variable, and G. H. Hardy told the Copenhagen mathematicians in
1921 that an elementary proof seemed to him "extraordinarily unlikely".

It came in 1948, with a bitter quarrel. **[Atle Selberg](kloom:e/atle-selberg)**, at the
Institute for Advanced Study, had found an elementary inequality he kept
to himself. **[Paul Erdős](kloom:e/paul-erdos)** heard of it secondhand and used it to prove a
result about primes in short intervals; within days Selberg used Erdős's
result to finish a proof of the theorem, then found a second proof that
did without it. They could not agree on a joint paper. Selberg published
alone in the _Annals of Mathematics_, Erdős in the _Proceedings of the
National Academy of Sciences_, and the historian Dorian Goldfeld, who
knew both, collected their letters in 2004 because the story had been
distorted in the telling. Selberg won a Fields Medal in 1950.

The theorem counts primes on average. It says nothing about how close two
of them can sit, and the last frame of this trail is about that. First,
the frame on RSA puts large primes to work.

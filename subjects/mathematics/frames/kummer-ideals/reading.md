On Monday 1 March 1847, at the **[Academy of Sciences](kloom:e/french-academy-of-sciences)** in Paris, **[Gabriel
Lamé](kloom:e/gabriel-lame)** read a paper whose title promised a general proof of **[Fermat's
Last Theorem](kloom:e/fermats-last-theorem)**: that _x_ⁿ + _y_ⁿ = _z_ⁿ has no solution in whole numbers
when _n_ is greater than 2. Proofs existed for the exponents 3, 5 and 7,
he said, each resting on splitting the left side into two factors, and
from 11 on the method stalled. His idea, which he credited to **[Joseph
Liouville](kloom:e/joseph-liouville)**, was to split it into _n_ factors at once, using a number _r_
with _r_ⁿ = 1. For an odd prime _n_,

_x_ⁿ + _y_ⁿ = (_x_ + _y_)(_x_ + _ry_)(_x_ + _r_²_y_) ⋯ (_x_ + _r_ⁿ⁻¹_y_).

![The head of Lamé's note in the Academy's printed proceedings: its title, "Démonstration générale du théorème de Fermat, sur l'impossibilité, en nombres entiers, de l'équation xⁿ + yⁿ = zⁿ; par M. Lamé", and its first paragraph, which credits Liouville with the idea](lame-1847.jpg)

The factors are _cyclotomic integers_, sums of powers of _r_ with
whole-number coefficients. If their product is an _n_th power and they
share no factor, each of them should be an _n_th power too. That is how
the argument runs for ordinary whole numbers, where every number breaks
into primes in only one way.

## A gap to fill

Liouville answered at the same sitting. The idea was not new, he said,
and it needed a theorem Lamé had not proved: that these numbers, like the
ordinary ones, factor into primes in only one way. "Is there not a gap to
fill there?" **[Augustin-Louis Cauchy](kloom:e/augustin-louis-cauchy)** then reminded the Academy of a
memoir he had presented the previous October, which he thought might lead
to a proof. For the next three months the proceedings read like a race.
On 22 March Cauchy and Lamé each lodged a sealed envelope with the
Academy, the way a claim was then staked without being published, and
Lamé brought a second memoir in April and a third in May.

The answer came from Breslau. The proceedings of 24 May printed a letter
to Liouville from **[Ernst Kummer](kloom:e/ernst-kummer)**, dated 28 April. Unique factorisation,
Kummer wrote, "does not hold in general" for these numbers, and he had
shown as much in a memoir of 1844; "but one can save it by introducing a
new kind of complex number, which I have called an ideal complex number."
Among the exponents it fails for is 23.

## Six, two ways

The trouble is easiest to see in a smaller system. Take the numbers _a_ + *b*√−5, with _a_ and _b_ whole.
Then

6 = 2 × 3 = (1 + √−5)(1 − √−5).

Give each number its _norm_, _N_(_a_ + *b*√−5) = _a_² + 5_b_², which
multiplies as the numbers do. _N_(2) = 4, _N_(3) = 9 and _N_(1 ± √−5) = 6.
A factor of 2 would need norm 2, and a factor of 3 norm 3, but _a_² + 5_b_²
is never 2 or 3. So none of the four numbers breaks any further, and 6
has two different factorisations into numbers that cannot be split. The
plate draws the numbers as a lattice, with a circle for each norm: the
circles of norm 2 and 3 pass through no point at all.

Kummer's cure was to invent the missing factors. Here they are three
ideal primes, _P_, _Q_ and _Q_′, with 2 = _P_², 3 = *QQ*′, 1 + √−5 = *PQ*
and 1 − √−5 = *PQ*′. Both factorisations of 6 become *P_²_QQ*′, and
uniqueness is restored. **[Richard Dedekind](kloom:e/richard-dedekind)** made such factors concrete.
*P* is the set of all the numbers 2_x_ + (1 + √−5)_y_, and a set of that
kind, closed under addition and under multiplication by any number of the
ring, he named an _ideal_, "because of its relation to Kummer's ideal
numbers". His own example, in the same numbers, was 21 = 3 × 7 =
(1 + 2√−5)(1 − 2√−5). He set the theory out in supplements to his
editions of Dirichlet's lectures on number theory; accounts date the first
of them to 1871, 1876 or 1879.

## Regular primes

Kummer did prove Fermat's theorem for many exponents. In 1850 he showed
that it holds for every _regular_ prime _p_: one that does not divide the
numerator of any of the Bernoulli numbers _B_₂, _B_₄, …, _B_ₚ₋₃. Below 100
only 37, 59 and 67 fail the test. For 37 the culprit is _B_₃₂ =
−7,709,321,041,217/510, whose numerator is 37 × 208,360,028,141, by our
arithmetic. The irregular primes were then worked through one by one,
and by 1993 computers had carried the check past four million.

The Academy had offered a prize for a proof. In 1857 Cauchy reported that
eleven memoirs had come in and none had succeeded, and the Academy gave
its medal instead to Kummer, who had not entered, for his "beautiful
research on complex numbers composed of roots of unity and whole numbers".

Whether Fermat was what drove him is argued. In 1910 Kurt Hensel told how
Kummer, like Lamé, had once believed he had a proof until Dirichlet
pointed out that it assumed unique factorisation; the MacTutor archive
still says Kummer invented ideal numbers because of Fermat. The historian
Harold Edwards found Hensel's story probably garbled and judged that
Kummer's real interest was the higher reciprocity laws; Kummer called his
Fermat result a curiosity. His letter of 1847 says only that its
applications to Fermat's theorem "have occupied me for a long time".

Ideals outlived the problem that set them going: they are how algebraic
number theory still counts. Fermat's equation would wait another century,
and its next great step came from a different direction altogether, from
curves.

Euclid proved that the primes never end. Whether they keep coming in
close pairs is still unknown. **[Twin primes](kloom:e/twin-prime)** are two primes that differ
by 2: 3 and 5, 11 and 13, 101 and 103. The twin prime conjecture says
there are infinitely many. In 1849 Alphonse de Polignac went further and
stated, as a "theorem" he could not prove, that every even number is the
gap between consecutive primes infinitely often. It is still unproved for
any gap at all. What was proved, starting in 2013, is that some gap below
a fixed bound recurs forever.

## Counting the pairs

Every pair after 3 and 5 sits on either side of a multiple of 6, and 3, 5
and 7 are the only three primes in a row two apart, because of any three
numbers _n_, _n_ + 2, _n_ + 4 one is divisible by 3. We counted the pairs
ourselves with a sieve:

| Up to |     Pairs | Hardy–Littlewood estimate |
| ----- | --------: | ------------------------: |
| 10²   |         8 |                        14 |
| 10³   |        35 |                        46 |
| 10⁴   |       205 |                       214 |
| 10⁵   |     1,224 |                     1,249 |
| 10⁶   |     8,169 |                     8,248 |
| 10⁷   |    58,980 |                    58,754 |
| 10⁸   |   440,312 |                   440,368 |
| 10⁹   | 3,424,506 |                 3,425,308 |

The pairs thin out faster than the primes, roughly as 1/(ln _x_)² rather
than 1/ln _x_. G. H. Hardy and J. E. Littlewood conjectured how many
there should be: 2_C_₂ times the integral of 1/(ln _t_)², where _C_₂
≈ 0.6601618 is a product over the odd primes. The estimate column is
that formula, computed by us; below a billion it is off by less than one
part in four thousand. A conjecture that fits so well is still not a
proof.

In 1919 the Norwegian **[Viggo Brun](kloom:e/viggo-brun)** proved that the sum 1/3 + 1/5 + 1/5

- 1/7 + 1/11 + 1/13 + … over all twin primes converges, to a number near
  1.902, although the sum over all primes grows without end. So the twins
  are rare, but his result cannot say whether they run out. Computing that
  sum, Thomas Nicely found an error in the division unit of Intel's
  Pentium chip, the flaw that became known as the Pentium FDIV bug. The largest known pair,
  found in 2016, is 2,996,863,034,895 × 2¹²⁹⁰⁰⁰⁰ ± 1, with 388,342 digits.

## Seventy million

On 17 April 2013 a paper reached the _Annals of Mathematics_ from **[Yitang
Zhang](kloom:e/yitang-zhang)**, a lecturer at the University of New Hampshire in his late
fifties whom few number theorists had heard of. It proved that some gap
smaller than 70 million occurs between primes infinitely often. One
referee called it "a landmark theorem in the distribution of prime
numbers", and the journal accepted it within weeks.

![Yitang Zhang, a man with short dark hair and metal-framed glasses, speaking in an interview in front of a bright window](yitang-zhang.jpg)

Zhang had taken his doctorate at Purdue in 1991 and found no academic
job. For years he worked as an accountant, in a motel and in a Subway
sandwich shop before a lecturer's post at New Hampshire in 1999. He has
said that his adviser, Tzuong-Tsieng Moh, wrote him no letters of
recommendation; Moh says Zhang never asked for any. Zhang built on a
2005 method of Daniel Goldston, János Pintz and Cem Yıldırım, which had
come within a hair of the result, and pushed through the step that
experts had tried and failed to make.

## From 70 million to 246

Within weeks the bound was falling. **[Terence Tao](kloom:e/terence-tao)** opened a **[Polymath
Project](kloom:e/polymath-project)**, an open online collaboration, which brought it to 4,680. In
November 2013 **[James Maynard](kloom:e/james-maynard-mathematician)**, born in 1987, found a simpler and stronger sieve that gave 600 with no need
for Zhang's hardest step, and Tao found much the same method on his own.
Combining the two, the Polymath project reached 246 in 2014.

![Bar chart on a logarithmic scale: the proven bound on a gap between primes that recurs forever was 70 million in Zhang's 2013 paper, 4,680 from Polymath8a, 600 from Maynard, 246 from Polymath8b in 2014, 240 and 212 in preprints of 2026, against the 2 of the twin prime conjecture](gap-bounds.svg)

| Result                     | Bound      | Status on 30 September 2026 |
| -------------------------- | ---------- | --------------------------- |
| Zhang, 2013                | 70,000,000 | published                   |
| Polymath8a, 2013           | 4,680      | published                   |
| Maynard, November 2013     | 600        | published                   |
| Polymath8b, 2014           | 246        | published                   |
| Stadlmann, August 2026     | 240        | preprint                    |
| Axiom Math, September 2026 | 212        | preliminary draft           |

The number 246 is the width of a list of fifty offsets, 0, 4, 6, 16, …,
244, 246, that the plate draws. The list is _admissible_: for every prime
_p_ it leaves at least one remainder on division by _p_ unused, so no
single prime is bound to divide one of the numbers _n_, _n_ + 4, …,
_n_ + 246 whatever _n_ is. The
theorem says that for infinitely many _n_ at least two of those fifty
numbers are prime, and two of them are never more than 246 apart. Even if
the deepest conjectures about primes in progressions were granted, the
Polymath paper showed, sieve methods of this kind could get no lower than
6, never to 2.

As of 30 September 2026 the bound had just begun to move again. On 31
August **[Julia Stadlmann](kloom:e/julia-stadlmann)** posted a preprint lowering it to 240, and on 3
September a group at the company Axiom Math dated a preliminary draft
claiming 212 by optimising her method, with part of the argument checked
by machine in the Lean language, in a certificate written by their AI
prover. Neither had yet been refereed;
Wikipedia's article on Zhang already gives 212. Euclid's proof, where
this trail began, still guarantees only that the primes go on, not that
any two of them stay close.

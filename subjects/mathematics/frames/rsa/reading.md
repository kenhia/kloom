For all of history, two people who wanted to write in secret had first to
share a secret: the key. In November 1976 **[Whitfield Diffie](kloom:e/whitfield-diffie)** and Martin
Hellman of Stanford published a way round it, which they called
**[public-key cryptography](kloom:e/public-key-cryptography)**. Each person could publish a key for locking
messages to them and keep a different key for unlocking. They showed how
two strangers could agree a key in public, a scheme the computing
subject's frame on network security works through, but they had no
practical way to make a published lock that only its owner could open.

At MIT, **[Ron Rivest](kloom:e/ron-rivest)**, **[Adi Shamir](kloom:e/adi-shamir)** and **[Leonard Adleman](kloom:e/leonard-adleman)** spent a
year looking for one, Rivest and Shamir proposing functions and Adleman,
the mathematician, breaking them. As the story is usually told, the idea
came to Rivest on a night in April 1977, after a Passover dinner, and he
had most of the paper written by morning. Their paper reached its
journal on 4 April 1977. The method, **[RSA](kloom:e/rsa-cryptosystem)** after their initials, rests on the primes.

## A lock made of two primes

Choose two primes _p_ and _q_ and multiply them: _n_ = _pq_. Publish _n_
and an exponent _e_. To send a number _M_ smaller than _n_, compute _C_ =
_M_ᵉ mod _n_, the remainder when _M_ᵉ is divided by _n_. The owner, who
alone knows _p_ and _q_, knows (_p_ − 1)(_q_ − 1), and so can find the
number _d_ with _ed_ one more than a multiple of it. Then _C_ᵈ mod _n_ is
_M_ again. That is the theorem of Fermat and Euler: _M_ raised to the
power (_p_ − 1)(_q_ − 1) leaves remainder 1, so _M_ᵉᵈ leaves _M_.

The paper, published in _Communications of the ACM_ in February 1978,
works its own small example. Take _p_ = 47 and _q_ = 59, so _n_ = 2773
and (_p_ − 1)(_q_ − 1) = 46 × 58 = 2668. Take _d_ = 157; then _e_ = 17,
since 17 × 157 = 2669 = 2668 + 1. The message ITS ALL GREEK TO ME is
written two letters to a block, A as 01 and a space as 00, so the first
block, IT, is 0920. To raise 920 to the 17th power, square four times
and multiply once:

| Power of 920 | mod 2773 | How                          |
| -----------: | -------: | ---------------------------- |
|            1 |      920 |                              |
|            2 |      635 | 920²                         |
|            4 |    1,140 | 635²                         |
|            8 |    1,836 | 1,140²                       |
|           16 |    1,701 | 1,836²                       |
|       **17** |  **948** | 1,701 × 920, and 948 is sent |

The owner computes 948¹⁵⁷ mod 2773 and gets back 920. Anyone who could
factor 2773 into 47 × 59 could find _d_ as easily; the whole security is
that for an _n_ of hundreds of digits no one knows how. The primes
themselves are easy to find. By the prime number theorem about one number
in 710 near 2¹⁰²⁴ is prime, one odd number in 355 by our arithmetic, and
testing a number for primality is fast. The plate does the same with _n_
= 33: cubing shuffles the numbers 0 to 32, and raising to the seventh
power puts every one back.

## A hundred dollars and forty quadrillion years

**Martin Gardner** announced the method in his "Mathematical Games"
column in _Scientific American_ in August 1977, under the headline "A new
kind of cipher that would take millions of years to break". Rivest
estimated that factoring a 125-digit product of two primes would take
about 40 quadrillion years. The inventors set readers a message locked
with a 129-digit _n_, now called RSA-129, and offered $100.

It fell in April 1994. Derek Atkins, Michael Graff, Arjen Lenstra and
Paul Leyland split the work among some 600 volunteers and more than 1,600
machines over the internet, two of them fax machines, and found the
factors on 2 April. The message read "THE MAGIC WORDS ARE SQUEAMISH
OSSIFRAGE". The algorithm that did it, the quadratic sieve, had been invented only in 1981.

The idea was older than the paper. At Britain's signals intelligence
agency, **[Clifford Cocks](kloom:e/clifford-cocks)**, a young number theorist, had written a secret
note on 20 November 1973 describing essentially the same system, with _n_
itself as the exponent. It stayed classified until December 1997.

## Where it stands

![Bar chart: the largest RSA challenge number factored had 129 digits in 1994, 155 in 1999, 200 in 2005, 232 in 2009, 250 in 2020, 260 in September 2026 and 270 in September 2026](factoring-records.svg)

| Number  | Digits | Factored          |
| ------- | -----: | ----------------- |
| RSA-129 |    129 | April 1994        |
| RSA-155 |    155 | August 1999       |
| RSA-200 |    200 | May 2005          |
| RSA-768 |    232 | December 2009     |
| RSA-250 |    250 | February 2020     |
| RSA-260 |    260 | 3 September 2026  |
| RSA-896 |    270 | 19 September 2026 |

As of 30 September 2026 the record had moved twice in a month. Eric Lu of
Cognition factored RSA-260 on 3 September on spare GPUs, with software
built by the company's AI agents, and Stephen Weis factored RSA-896 on 19
September on idle GPUs at Anthropic, with Claude porting the software.
Both say the algorithm itself was not improved, and both announced their
results on their own sites, not in journals; we multiplied the published
factors of RSA-896 and got RSA Laboratories' number back. The keys the
web uses have 2048 bits, 617 digits, and Lu judged them about a billion
times harder than 1024-bit ones.

The larger threat is a different machine. In 1994 **[Peter Shor](kloom:e/peter-shor)** showed
that a quantum computer could factor in a number of steps growing only
like a power of the number of digits. None large enough exists yet, but
in August 2024 the US National Institute of Standards and Technology
published its first standards for encryption built on other problems,
and a NIST draft that November proposed deprecating RSA after 2030 and
disallowing it after 2035. The primes
RSA stands on are plentiful; the last frame of the trail asks how closely
they can crowd together.

The square root of minus one came into mathematics by the back door. The
formula for the cubic in Cardano's _Ars Magna_ reached real answers only by
passing through it, and Bombelli learned to calculate with it before anyone
could say what it was. For two centuries it was used and not believed.
**[René Descartes](kloom:e/rene-descartes)**, in his _Géométrie_ of 1637, gave such roots their
name: sometimes, he wrote, they are "only imaginary", and "there exists no
quantity that matches that which we imagine." The word was meant to keep
them in their place.

## Euler's jewel

**[Leonhard Euler](kloom:e/leonhard-euler)** used them without apology. In his _Introductio in
analysin infinitorum_ of 1748 he compared the series for the exponential
with those for the sine and cosine, and found

e^(i*x*) = cos _x_ + _i_ sin _x_.

Put _x_ = π, and cos π = −1 while sin π = 0, so e^(iπ) = −1, or
e^(iπ) + 1 = 0: five of the most important numbers in mathematics in one
line. It is usually credited to the _Introductio_, but the identity itself
seems not to be there. The mathematician Robin Wilson, who wrote a book
about it, found that Euler "does not seem to have written it down
explicitly", though it follows at once from his formula, and that no one
knows who first stated it. **Richard
Feynman**, in _The Feynman Lectures on Physics_, called the formula "our
jewel".

## A quarter turn

What made imaginary numbers respectable was a picture. **[Caspar Wessel](kloom:e/caspar-wessel)**, a
surveyor mapping Denmark, presented one to the Danish academy in 1797, and
it was printed in Danish in 1799 and went unread for nearly a century. In
Paris in 1806 **[Jean-Robert Argand](kloom:e/jean-robert-argand)**, a Genevan amateur who kept a
bookshop or, in another account, kept books, published the same idea
privately, in a small pamphlet with no author's name on it.

![The title page of Argand's Essai sur une manière de représenter les quantités imaginaires dans les constructions géométriques, Paris, 1806, with no author named. Facing it is a handwritten address to Monsieur Gergonne at Nîmes, and on the title page the bookseller's address is crossed out and "Mr Argand, rue de Gentilly No 12" written above it](argand-essai.jpg)

Argand's question was simple: what _x_ makes +1 : _x_ :: _x_ : −1? No
number on the line will do. But give numbers a direction, and minus one is
a turn half way round; what he wanted was a third direction, "such that the
positive direction shall stand in the same relation to it that the latter
does to the negative": a line at right angles. Multiplying by _i_
turns a number a quarter of the way round zero, and doing it twice turns
it half way, which is multiplying by −1. That is all *i*² = −1 says.

Take 3 + 2*i*, the point three across and two up, and multiply by _i_
four times, remembering that _i_ × _i_ = −1:

| Step        | The number | How it is reached                  |
| ----------- | ---------- | ---------------------------------- |
| start       | 3 + 2*i*   |                                    |
| × _i_       | −2 + 3*i*  | 3*i* + 2*i*² = 3*i* − 2            |
| × _i_ again | −3 − 2*i*  | the start turned half way, or × −1 |
| × _i_ again | 2 − 3*i*   | three quarters round               |
| × _i_ again | 3 + 2*i*   | home                               |

Each point is as far from zero as the last, √13, and a quarter turn on. The
plate draws the four of them as the corners of a square. Euler's formula
says the same for any angle: e^(i*x*) is the turn through _x_, and
e^(iπ) + 1 = 0 says that a half turn is minus one.

**[Carl Friedrich Gauss](kloom:e/carl-friedrich-gauss)** gave the idea his authority in 1831, and the name
"complex number" with it. The darkness around the subject, he wrote, came
from clumsy words: had +1, −1 and √−1 been called "direct, inverse, or
lateral units", there could scarcely have been talk of darkness.

## Every equation has its roots

The prize for admitting these numbers is the **[fundamental theorem of
algebra](kloom:e/fundamental-theorem-of-algebra)**: every polynomial equation of degree _n_ has _n_ roots among the
complex numbers, so nothing further is ever needed. Gauss made it the
subject of his doctoral thesis at Helmstedt in 1799, and began by showing
that every earlier proof was unsatisfactory. For a century and a half
textbooks called his the first rigorous one. In 1981 **Stephen Smale**
pointed out "what an immense gap" it contained: it takes for granted that
a curve which enters a region must leave it again, a fact Gauss said in a
footnote no one had ever doubted and he would prove "if anybody desires
it". He never did; the gap was closed by Alexander Ostrowski in 1920. The
proof Argand set out in 1806 and more fully in 1813 is now often counted
the first complete one, and Cauchy's _Cours d'analyse_ of 1821 reprinted
it without his name.

## Beyond the plane

If a pair of numbers could describe a turn in the plane, could a triple
describe a turn in space? **[William Rowan Hamilton](kloom:e/william-rowan-hamilton)** tried for years. In a
letter to his son in 1865 he recalled that each morning in October 1843
the boys asked, "Well, Papa, can you multiply triplets?", and he had to
answer, "No, I can only add and subtract them." On 16 October, walking
along the Royal Canal in Dublin, he saw that it took four numbers, not
three, and cut the rule into a stone of Brougham Bridge:
*i*² = *j*² = *k*² = _ijk_ = −1. The carving, he wrote, "has long since
mouldered away"; a plaque now marks the place. The price of **[quaternions](kloom:e/quaternion)**
is that order matters: _ij_ = _k_, but _ji_ = −*k*.

The imaginary unit now sits at the heart of quantum mechanics, in the rule
_pq_ − _qp_ = _h_/2π*i*. It is also inside machines that read. Rotary position embedding,
proposed in 2021 and used by many language models, treats each pair of
numbers in a word's vector as one complex number and multiplies it by
e^(i*mθ*) at position _m_: Argand's turn, applied to words.

Euler's formula binds the turn to the sine and the cosine, and those are
what Fourier would build every curve from.

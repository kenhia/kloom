Two old problems ran through the geometry Descartes had just made
algebraic. One asked for the tangent to a curve at a point, and so for how
fast a quantity changes at an instant. The other asked for the area under a
curve, and so for the whole that many small changes add up to. Fermat,
Cavalieri, Wallis and others had methods for special cases, and in
fourteenth-century Kerala the school of Madhava had found infinite series of
the kind now named for Taylor. Between 1665
and 1687, two men working apart turned the two problems into one method, and
then spent their last years fighting over whose it was.

## Newton's fluxions

**[Isaac Newton](kloom:e/isaac-newton)** was a student at Cambridge, and had read Descartes in van
Schooten's Latin, when plague closed the university in 1665. In the
plague years, 1665 and 1666, he worked out what he called the
method of fluxions: a curve is traced by a moving point, each quantity that
flows is a _fluent_, and its rate of flowing is its _fluxion_, in time
written with a dot over the letter. A manuscript dated 20 May 1665 already
finds the tangent and the curvature of any curve, and a tract of October
1666 sets the method out. Later he called these years "the
prime of my age for invention".

He published none of it. His _De analysi_ went in manuscript in 1669 to his
teacher **[Isaac Barrow](kloom:e/isaac-barrow)**, who sent it to the mathematician John Collins in
London; the fuller _Method of Fluxions_ of 1671 was printed only in 1736,
after his death. The _Principia_ of 1687 used a geometric form of the method,
its "first and last ratios", and not the fluxions themselves.

## Undoing the tangent

The heart of the method was a discovery Newton made while finding areas,
and which **[James Gregory](kloom:e/james-gregory-mathematician)** and Barrow had glimpsed geometrically by 1670:
the area problem is the tangent problem run backwards. This is now called
the **[fundamental theorem of calculus](kloom:e/fundamental-theorem-of-calculus)**. In _De analysi_ Newton showed it
with a letter _o_ for a moment of increase.

Suppose, to take the simplest case, the area under a curve from 0 up to _x_
is _x_³/3, and let _x_ grow by the moment _o_. The area grows by
(_x_ + _o_)³/3 − _x_³/3 = _x_²_o_ + _x o_² + _o_³/3. That new sliver of area
is a thin strip, as tall as the curve, _y_, and as wide as _o_, so divide by
_o_: _y_ = _x_² + _x o_ + _o_²/3. Now let the moment vanish, "blotting out"
the terms that still hold _o_, since terms "multiplied by it will be
nothing in respect to the rest": the curve is _y_ = _x_².

| At _x_ | Area under _x_², _x_³/3 | Height of the curve, _x_² | Slope of the area curve |
| -----: | ----------------------: | ------------------------: | ----------------------: |
|      1 |                     1/3 |                         1 |                       1 |
|    1.5 |                   1.125 |                      2.25 |                    2.25 |
|      2 |                     8/3 |                         4 |                       4 |

The plate draws both halves: below, the parabola with the area under it
built from thin rectangles; above, the area as a curve of its own, whose
tangent at every _x_ is as steep as the parabola is high. Area
grows as fast as the curve is tall. **[Nicole Oresme](kloom:e/nicole-oresme)** had drawn the
distance a steadily speeding body covers as the area under its line of
speed, three centuries before; the calculus made that true for any curve.
Newton himself admitted that dropping the _o_ was "shortly explained rather
than accurately demonstrated". Making it rigorous took until the nineteenth
century.

## Leibniz's _d_ and ∫

**[Gottfried Wilhelm Leibniz](kloom:e/gottfried-wilhelm-leibniz)** came to the problem in Paris in the 1670s,
as a newcomer to mathematics. In notes of 25 October to 11
November 1675 he wrote _dx_ and _dy_ for the smallest differences of _x_
and _y_, and a long _s_, ∫, for _summa_, the sum of infinitely many thin
rectangles. He chose his signs with the care of a man who hoped one day to
write all reasoning in symbols. The next year he wrote the chain rule for
the first time, in a memoir with a sign error in it.

![The first page of Leibniz's Nova methodus in the Acta Eruditorum for October 1684, page 467: the title in large italic capitals, then Latin text defining dx and dv, with the rules for addition, subtraction, multiplication and division set out in the new signs](nova-methodus.jpg)

He published first. In October 1684 the Leipzig journal **[_Acta
Eruditorum_](kloom:e/acta-eruditorum)** printed his "New method for maxima and minima, and for
tangents", seven pages signed only G. G. L., whose title ends "and a singular kind
of calculus for them"; the subject takes its name from that title. The
rules are on its first page: the difference of a product, _d_(_xv_) =
_x dv_ + _v dx_. With the Bernoulli brothers and l'Hôpital's textbook of 1696,
Leibniz's notation carried the calculus across the Continent.

## The quarrel

Peace lasted until 1699, when Nicolas Fatio de Duillier publicly accused
Leibniz of taking the method from Newton. The charge grew, and Leibniz
appealed to the **[Royal Society](kloom:e/royal-society)**, whose president was Newton.
Its committee heard no evidence from Leibniz, and its report, received on
24 April 1712 and printed with the old letters as the _Commercium
epistolicum_, concluded: "we reckon Mr. Newton the first Inventor". Newton
had drafted it himself. The book is dated 1712; Wikipedia's editors, and
the physics subject's frame on the _Principia_, date the verdict to 1713,
when the report was published.

The case was not all spite. In 1849 extracts from Newton's _De analysi_ in
Leibniz's hand were found among his papers, though when he copied them is
unknown. The historians' verdict now is that each invented the calculus
independently, Newton first, Leibniz first in print. The cost fell on
England: its mathematicians kept Newton's dots until the 1820s while the
Continent ran ahead with _d_ and ∫. A generation later one of the calculus's
masters, Leonhard Euler, wrote a paper that needed no calculus at all.

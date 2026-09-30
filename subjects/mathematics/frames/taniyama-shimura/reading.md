In 1955 an international symposium on algebraic number theory met in Tokyo
and Nikkō, and a young mathematician from the University of Tokyo,
**[Yutaka Taniyama](kloom:e/yutaka-taniyama)**, handed out a list of problems in English. Among the guests were **[André Weil](kloom:e/andre-weil)** and **[Jean-Pierre Serre](kloom:e/jean-pierre-serre)**. Problems 12 and 13
suggested, not quite correctly as stated, that two kinds of object which
had nothing to do with each other were secretly the same. Refined with
his friend **[Goro Shimura](kloom:e/goro-shimura)**, the suggestion became the road by which
Fermat's equation was finally settled.

## A curve that adds

The first kind of object is an **[elliptic curve](kloom:e/elliptic-curve)**: the points (_x_, _y_)
with _y_² equal to a cubic in _x_ whose three roots differ. Its points can
be added. Draw the line through two points _P_ and _Q_; in general it meets the curve at exactly one more point, _R_; reflect _R_ in the _x_-axis, and
that is _P_ + _Q_. The tangent at _P_ gives _P_ + _P_ the same way. If
_P_ and _Q_ have rational coordinates, so does _P_ + _Q_, so the rational
points of a curve form a group of their own.

The plate draws the construction on _y_² = _x_(_x_ − 9)(_x_ + 16), a curve built as **[Gerhard Frey](kloom:e/gerhard-frey-mathematician)** would build his, from the equation 3² + 4² =
5²; its _P_ and _Q_ are invented. The same arithmetic, done with remainders
modulo a large prime, now protects much of the web. The X25519 key
exchange in TLS takes a point on _Curve25519_, _v_² = _u_³ + 486662_u_² +
_u_ modulo 2²⁵⁵ − 19, and multiplies it by a secret number, which is to
say adds it to itself by this rule.

## Counting modulo p

The second kind of object is a _modular form_, a function on the complex
numbers with an enormous family of symmetries, written as a power series
in _q_. What the conjecture claims can be checked by hand. Take the curve
_y_² + _y_ = _x_³ − _x_², and for each prime _p_ count its solutions in
whole numbers modulo _p_. Then multiply out the modular form

_q_(1 − _q_)²(1 − _q_¹¹)²(1 − _q_²)²(1 − _q_²²)² ⋯ = _q_ − 2_q_² − _q_³ + 2_q_⁴ + _q_⁵ + 2_q_⁶ − 2_q_⁷ − ⋯

| Prime _p_               |   2 |   3 |   5 |   7 |  13 |  17 |  19 |  23 |
| ----------------------- | --: | --: | --: | --: | --: | --: | --: | --: |
| Solutions modulo _p_    |   4 |   4 |   4 |   9 |   9 |  19 |  19 |  24 |
| _p_ minus the solutions |  −2 |  −1 |   1 |  −2 |   4 |  −2 |   0 |  −1 |
| Coefficient of _q_ᵖ     |  −2 |  −1 |   1 |  −2 |   4 |  −2 |   0 |  −1 |

The last two rows agree, prime after prime; we counted both by our own
arithmetic, and the LMFDB database lists the same curve and form. The
**[modularity theorem](kloom:e/modularity-theorem)**, as the conjecture is now called, says this happens
for every elliptic curve over the rational numbers. The form's _level_,
here 11, matches a number measured from the curve, its _conductor_, and
there is no form of the right kind at any level below 11.

## Whose conjecture

Taniyama did not see it proved. He took his own life in Tokyo on 17
November 1958, at 31, a few weeks after his engagement; his note said he
had lost confidence in his future, and his fiancée, Misako Suzuki, died
the same way a month later. Shimura wrote that Taniyama had been "the
moral support of many" who worked with him.

The name is still argued over. By Shimura's account, he put the
conjecture to Weil at the Institute for Advanced Study in
Princeton, most likely in 1964. Weil's paper of 1967 all but stated it,
left whether it always held "as an exercise" for the interested reader,
and added the precise claim that the level equals the conductor. Serre recalled Weil explaining that to him in a Latin Quarter
café in the summer of 1966: it made the conjecture checkable, and within
a few hours of checking curves Serre was convinced. For years it was the
Weil conjecture, then the Taniyama–Weil; in 1995 Serge Lang argued at
length for Shimura's share. Wiles's paper of 1995 gives the history in a
sentence: the conjecture grew out of the work of Shimura and Taniyama,
and became widely known through Weil.

## Fermat's equation returns

In the mid-1980s Frey turned the conjecture on Fermat. (Most
accounts date his idea to 1984; Wiles's paper says 1985; his paper
appeared in 1986.) Suppose _a_ᵖ + _b_ᵖ = _c_ᵖ for a prime _p_ of 5 or
more. Then the curve _y_² = _x_(_x_ − _a_ᵖ)(_x_ + _b_ᵖ) has a discriminant
of 2⁻⁸(_abc_)²ᵖ, almost a perfect _p_th power, and a curve that strange
seemed unlikely to be modular. Frey gave a plausibility argument, not a
proof. Serre pinned down what was missing, a statement that came to be
called the epsilon conjecture, and **[Ken Ribet](kloom:e/ken-ribet)** proved it in the summer
of 1986. In his telling the last step came over a cappuccino with Barry
Mazur, who pointed out that Ribet had already done it. Ribet's theorem
pushes the Frey curve's form down to level 2, where there is no form at
all. So if every such curve is modular, Fermat's Last Theorem is true.

Few thought the conjecture could be proved. Ribet counted himself among
"the vast majority" who believed it completely inaccessible. One mathematician, by his own account hearing the news over iced tea at a friend's house, went home to try.

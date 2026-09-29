On 19 April 1965 the trade magazine _Electronics_ ran a series headed
"The experts look ahead", and one of the experts was the director of
research at Fairchild Semiconductor, **Gordon Moore**. His article,
_Cramming More Components onto Integrated Circuits_, became the most
quoted forecast in the history of technology, and what it forecast is
often simplified.

## What Moore said

Moore's argument was about cost. A simple circuit on a chip costs roughly
the same whatever it holds, so the cost per component falls as more are
added; but past a point, yields fall and the cost per component rises
again. So at any time there is a cheapest complexity. In 1965, he wrote,
the minimum came at about 50 components per circuit; in five years he
expected it at about 1,000, at a tenth of the cost. The plate redraws his
two graphs: the cost curves, whose shapes here are a simple model but
whose minima are his, and the complexity itself.

That complexity, "the complexity for minimum component costs", had
"increased at a rate of roughly a factor of two per year", and Moore saw
no reason it should not stay nearly constant "for at least 10 years". By
1975, then, 65,000 components on a chip. He thought one would fit in about
a quarter of a square inch. The article also foresaw home computers,
"automatic controls for automobiles" and personal portable communications
equipment. He asked whether the heat of tens of thousands of components
could be removed from one chip, and answered that it could: a chip is flat,
so every source of heat is close to a surface, and shrinking the
dimensions, he wrote, makes it possible to run the structure faster "for
the same power per unit area". Nine years later that sentence got its
proof.

In 1975, now at Intel, which he had founded with **Robert Noyce** in 1968,
Moore looked again. Complexity had in fact doubled about every year. But
he split the gain into bigger chips, smaller features and what he called
"circuit and device cleverness", and the last, he judged, was nearly used
up. The slope might approximate "a doubling every two years, rather than
every year, by the end of the decade". The name _Moore's law_ came later: the
Caltech professor Carver Mead popularised it.

![Gordon Moore, seated with a pen over papers, and Robert Noyce, standing and looking down at them, at Intel in 1970](moore-noyce.png)

## Dennard's rules

Moore described a trend; in 1974 **Robert Dennard** and his colleagues at
IBM explained why shrinking paid. Their paper on very small MOS
transistors showed that if every dimension of a transistor, and its
voltage, is cut by a factor κ, and its doping raised by κ, it behaves the
same, only smaller and faster:

| Quantity (Dennard et al., 1974, table I) | Scales by |
| ---------------------------------------- | --------- |
| Dimensions, and voltage                  | 1/κ       |
| Doping concentration                     | κ         |
| Current, and capacitance                 | 1/κ       |
| Delay time per circuit                   | 1/κ       |
| Power per circuit                        | 1/κ²      |
| Power per unit area                      | 1         |

The last line is the one that mattered. Shrink the features by 30 per
cent, κ about 1.4, and a chip holds twice as many transistors, each faster,
for the same power per square millimetre. For thirty years each new
generation of chips was denser, faster and no hotter than the last, and
cheaper per transistor too.

## Fifty-five years of it

The chart follows transistors on one processor, from Intel's 4004 of 1971,
the first single-chip microprocessor, to Nvidia's _Rubin_ of 2026.

![Bar chart on a logarithmic scale: Intel 4004 (1971) 2,300 transistors; 8086 (1978) 29,000; 386 (1985) 275,000; Pentium (1993) 3.1 million; Pentium 4 (2000) 42 million; Core 2 Duo (2006) 291 million; Apple M1 (2020) 16 billion; Apple M3 Max (2023) 92 billion; Nvidia Rubin (2026) 336 billion](transistor-counts.svg)

| Processor        | Introduced | Transistors | Source                         |
| ---------------- | ---------- | ----------: | ------------------------------ |
| Intel 4004       | Nov 1971   |       2,300 | Intel                          |
| Intel 8086       | Jun 1978   |      29,000 | Intel                          |
| Intel386 DX      | Oct 1985   |     275,000 | Intel                          |
| Pentium          | Mar 1993   |   3,100,000 | Intel                          |
| Pentium 4        | Nov 2000   |  42,000,000 | Intel                          |
| Core 2 Duo E6700 | Jul 2006   | 291,000,000 | Intel                          |
| Apple M1         | Nov 2020   |  16 billion | Apple                          |
| Apple M3 Max     | Oct 2023   |  92 billion | Apple                          |
| Nvidia Rubin GPU | 2026       | 336 billion | Nvidia (two dies, one package) |

From the 4004 to Rubin is a factor of about 146 million, some 27
doublings in 55 years: one every two years, as Moore revised it. (That is
our arithmetic on these nine chips, which mix processors, a laptop system
on a chip and a two-die graphics processor for AI data centres; a
different choice would move it a little.) Richard Feynman had told physicists in
1959 that there was plenty of room at the bottom; the industry spent half
a century using it.

The count kept rising. What the bottom rows hide is that, from the middle
of the 2000s, Dennard's last line stopped holding, and each doubling began
to cost more than the one before.

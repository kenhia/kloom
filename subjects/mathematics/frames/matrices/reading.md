A **[matrix](kloom:e/matrix-mathematics)** is a rectangle of numbers. For most of its history it was only
a way of laying out the coefficients of equations so that they could be
worked on, as the _Nine Chapters on the Mathematical Art_ did on a counting
board, which its own frame tells. In the nineteenth century the rectangle
became an object that could be added and multiplied as if it were a
number. Then it turned out to describe the atom, and in our century to be
the arithmetic that neural networks run on.

## Determinants first

Before the matrix came the _determinant_, a single number computed from the
coefficients of a set of equations, which says whether they have one
solution. In Japan in 1683 **[Seki Takakazu](kloom:e/seki-takakazu)**, a samurai and an official of
the Kōfu domain, used it in _Kaifukudai no Hō_, his method for eliminating
unknowns; his five-by-five formula is wrong, and a correct general rule
appears only in a later work written with his pupils. In 1693
**[Gottfried Wilhelm Leibniz](kloom:e/gottfried-wilhelm-leibniz)** wrote to the Marquis de l'Hôpital about three
equations in two unknowns, their coefficients written as two-digit numbers,
the first digit naming the equation and the second the place:

| Leibniz's equations |
| ------------------- |
| 10 + 11x + 12y = 0  |
| 20 + 21x + 22y = 0  |
| 30 + 31x + 32y = 0  |

All three can hold, he said, when 10·21·32 + 11·22·30 + 12·20·31 =
10·22·31 + 11·20·32 + 12·21·30: when the determinant is zero. A number as
an address, row then column, is still how an entry of a matrix, _a_ᵢⱼ, is
named. Gabriel Cramer printed the general rule in 1750, without proof.

**[Carl Friedrich Gauss](kloom:e/carl-friedrich-gauss)** named the determinant in 1801, for a different
quantity from ours, and in 1810, fitting the orbit of the asteroid Pallas,
set out a systematic elimination of unknowns. Historians part over whether that makes it his. The MacTutor history calls the Pallas
calculation "precisely Gaussian elimination"; Joseph Grcar answers that
Newton had written the lesson in 1669–70, that Gauss's contribution was a
notation for least squares, and that the name dates from 1953, when George
Forsythe misattributed the schoolroom method to Gauss.

## A map of the plane

A 2 × 2 matrix
sends each point (_x_, _y_) of the plane to another. The shear _S_, with
rows (1, 1) and (0, 1), sends (_x_, _y_) to (_x_ + _y_, _y_): it slides
every line sideways by its height. The quarter turn _R_, with rows (0, −1)
and (1, 0), sends (_x_, _y_) to (−*y*, _x_). A matrix's columns are where
the unit arrows (1, 0) and (0, 1) land.

Doing one map after another is multiplying their matrices, each row of the
left against each column of the right. Shear first and then turn is _RS_:
its first entry is 0·1 + (−1)·0 = 0, and its rows are (0, −1) and (1, 1).
Turn first and then shear is _SR_, with rows (1, −1) and (1, 0). They are
not the same, and the plate draws the difference: one hatched square, sent
to two different places.

| Corner of the square | Shear, then turn (_RS_) | Turn, then shear (_SR_) |
| -------------------- | ----------------------- | ----------------------- |
| (1, 0)               | (0, 1)                  | (1, 1)                  |
| (1, 1)               | (−1, 2)                 | (0, 1)                  |
| (0, 1)               | (−1, 1)                 | (−1, 0)                 |

Both parallelograms have area 1, because every matrix here has determinant
1, and a determinant is the factor by which its map stretches area. The
shear also leaves one direction alone: an arrow along the _x_-axis comes
out unchanged, an _eigenvector_ of the map. The quarter turn moves every
direction, and has none among the real numbers.

## The word and the algebra

**[James Joseph Sylvester](kloom:e/james-joseph-sylvester)** coined the word in 1850 for an "oblong
arrangement of terms" that was not a determinant but the source of many:
_matrix_, Latin for womb, the array "out of which different systems of
determinants may be engendered, as from the womb of a common parent," as he
put it in 1851. His friend **[Arthur Cayley](kloom:e/arthur-cayley)**, a barrister, made the rectangle a
quantity. In _A Memoir on the Theory of Matrices_, read to the Royal
Society in January 1858, matrices "comport themselves as single
quantities", with "the peculiarity that matrices are not in general
convertible": the order of multiplication matters. Cayley proved that every
2 × 2 matrix satisfies an equation of its own degree, checked the 3 × 3
case, and declined "the labour of a formal proof" in general.

![The title page of Grassmann's Die lineale Ausdehnungslehre, ein neuer Zweig der Mathematik, Leipzig, 1844: the theory of linear extension, a new branch of mathematics, with applications to statics, mechanics, magnetism and crystallography, by Hermann Grassmann, teacher at the Friedrich-Wilhelms-Schule in Stettin](ausdehnungslehre.png)

Fourteen years earlier **[Hermann Grassmann](kloom:e/hermann-grassmann)**, a schoolteacher in Stettin,
had published a bolder book: vectors, subspaces, independence and
dimension, in any number of dimensions, most of what is now called a
vector space. Almost no one read it, and Ernst Kummer, asked about him for
a professorship, found good material "expressed in a deficient form".

## The arithmetic of the machines

In 1925 **[Werner Heisenberg](kloom:e/werner-heisenberg)** built a mechanics of the atom from tables of
numbers with a strange product. Max Born recognized them after a week of thought: such square arrays, he recalled in his Nobel lecture, "in conjunction with a specific
rule for multiplication, are called matrices." Matrix mechanics, as its own
frame in physics tells, put Cayley's unconvertible product at the heart of
quantum theory.

A neural network's layer computes weighted sums of the layer before it,
which is a matrix multiplying a vector, and a transformer's attention
multiplies each word's vector by learned matrices. So the heart of Google's
first Tensor Processing Unit, described in 2017, was "a 65,536 8-bit MAC
matrix multiply unit": multipliers and adders laid out in a square.

Cayley showed that a thing could be multiplied without its products
commuting, and algebra opened to objects that were not numbers at all.
Emmy Noether would make such algebras a subject of their own.

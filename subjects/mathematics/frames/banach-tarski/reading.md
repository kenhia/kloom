In 1924 two Polish mathematicians, **[Stefan Banach](kloom:e/stefan-banach)** of Lwów and **[Alfred Tarski](kloom:e/alfred-tarski)** of Warsaw, published a paper in the Polish journal _Fundamenta Mathematicae_ with a mild title, "On the decomposition of sets of points into respectively congruent parts". Its first theorem said that in space of three dimensions or more, any two bounded solids, "for example two spheres of different radii", can each be cut into the same finite number of pieces, the pieces of one congruent to the pieces of the other. Cut one ball, move the pieces without stretching them, and put them together again as two balls, each the size of the first. The result is known as the **[Banach–Tarski paradox](kloom:e/banach-tarski-paradox)**. It is not a contradiction but a theorem, and what it proves is that some collections of points have no volume at all.

## The axiom of choice

The proof rests on a principle argued over for twenty years. In 1904 **[Ernst Zermelo](kloom:e/ernst-zermelo)** proved that every set can be put in a _well-ordering_, a line in which every part has a first member. To do it he assumed that from any collection of non-empty sets one member can be chosen from each, all at once, even when there are infinitely many sets and no rule for choosing. In Bertrand Russell's comparison, from infinitely many pairs of shoes one can take each left shoe; from pairs of socks there is no rule, and the **[axiom of choice](kloom:e/axiom-of-choice)** says a choice exists anyway.

Many mathematicians objected, among them the French analysts René Baire, Émile Borel and Henri Lebesgue, for whom a mathematical object existed only if it could be described exactly. Zermelo answered in 1908 with the first list of axioms for set theory, the axiom among them.

## A set with no length

In 1905 **[Giuseppe Vitali](kloom:e/giuseppe-vitali)**, in a pamphlet printed at Bologna, used the axiom to build a set of numbers that can have no length.

Take the numbers from 0 up to 1, and bend the segment into a circle, so that sliding past 1 comes round again to 0. Call two numbers _related_ when they differ by a fraction, such as ⅓ or ¹⁷⁄₁₀₀. The related numbers fall into uncountably many families. Now choose one number from each family, with no rule to do it by: that is where the axiom is needed. Call the chosen set _V_.

Slide _V_ round the circle by each fraction between 0 and 1. That gives countably many copies of _V_, and every number on the circle lies in exactly one of them: in the copy slid by the fraction that separates it from its own family's chosen member. Sliding changes no length, so if _V_ had a length ℓ, the circle's length would be ℓ + ℓ + ℓ + …, once for each copy. That sum is 0 if ℓ is 0, and infinite if ℓ is anything larger. It is never 1. So _V_ has no length, and no rule for length that is unchanged by sliding and adds up over countably many pieces can measure every set.

Vitali's pieces are infinitely many. In 1914 **[Felix Hausdorff](kloom:e/felix-hausdorff)** did it with finitely many, on the surface of a sphere: leaving out a countable set of points, he split the rest into three pieces _A_, _B_ and _C_, each congruent to the others, and _B_ congruent to _B_ and _C_ together. A half of the sphere was congruent to a third. Banach and Tarski built on both, as their first page says.

## Why three dimensions

The plate is a schematic: the real pieces cannot be drawn, since each is a cloud of points spread through the ball. The mechanism is in the rotations of space. Two rotations about different axes, by suitable angles, never undo one another, so every sequence of them is a different rotation. Sorted by their first turn, the sequences fall into four classes, and turning one class back makes it three classes' worth: four pieces make two wholes. The axiom of choice carries this bookkeeping over to the points of the sphere, and the sphere to the ball. In the plane, motions cannot be combined so freely, and there the doubling fails. In 1929 **[John von Neumann](kloom:e/john-von-neumann)** found the property of a group of motions that allows it.

| Year | Who               | Result                                                                 |
| ---: | ----------------- | ---------------------------------------------------------------------- |
| 1904 | Zermelo           | the axiom of choice, and the well-ordering of every set                |
| 1905 | Vitali            | a set of numbers with no length                                        |
| 1914 | Hausdorff         | a sphere, less a countable set, in three pieces, half equal to a third |
| 1924 | Banach and Tarski | one ball cut into finitely many pieces makes two                       |
| 1947 | Raphael Robinson  | five pieces are enough, and four are not                               |

Banach and Tarski noted that their second theorem, that of two polygons one inside the other, neither can be cut up into the other, used the axiom even more heavily than the paradox did, though it agrees with every intuition. "The role that this axiom plays in our reasoning seems to us to deserve attention," they wrote. To reject the axiom for the paradox's sake would cost the intuitive theorem too, though in 1949 A. P. Morse proved that one without it.

## What it means

Most mathematicians accepted the axiom, because too much else needs it. Gödel proved in the late 1930s that it cannot contradict the other axioms of set theory, and Paul Cohen in 1963–64 that it cannot be proved from them. Without it, or something close to it, the doubling cannot be proved. Nobody can cut a real ball this way. What the theorem shows is that volume, like length, cannot be given to every set of points that the axiom of choice says exists.

Gödel's proof reached further than the axiom of choice. It answered half of the question Cantor had asked in 1878, and spent his life on.

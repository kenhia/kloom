On Sunday 7 September 1930, at the end of a conference on the philosophy of the exact sciences in Königsberg, the speakers of the first day sat at a round table to discuss their talks. **[Kurt Gödel](kloom:e/kurt-godel)**, a twenty-four-year-old from Vienna, had spoken the day before about his proof that the rules of first-order logic are complete. Now, almost in passing, he added that one could give examples of propositions, even of the kind of Goldbach's or Fermat's, that are "contentually true" but unprovable in the formal system of classical mathematics. Almost no one took it in, except **[John von Neumann](kloom:e/john-von-neumann)**, who took Gödel aside.

## Two theorems

The paper, "On formally undecidable propositions of _Principia Mathematica_ and related systems I", reached the _Monatshefte für Mathematik und Physik_ on 17 November 1930 and was printed in 1931. The first of **[Gödel's incompleteness theorems](kloom:e/godels-incompleteness-theorems)** says that any consistent formal system strong enough for the arithmetic of whole numbers, whose axioms can be listed by rule, contains statements it can neither prove nor refute. (Gödel assumed slightly more than consistency; J. Barkley Rosser showed in 1936 that consistency is enough.) The second says that such a system cannot prove its own consistency.

Von Neumann found the second theorem for himself and wrote to Gödel about it on 20 November, as one account dates the letter; another puts it less than a month after the conference. Gödel had already put it in the manuscript he submitted three days earlier. Von Neumann did no more research on the foundations of mathematics. He said later, a colleague recalled, that he would be forgotten while Gödel was remembered with Pythagoras.

![A granite plaque on a Vienna house front: "In this house lived from 1930 to 1937 the great mathematician and logician Kurt Gödel, 1906–1978. Here he discovered his famous incompleteness theorem, the most important mathematical discovery of the twentieth century. 2006"](goedel-plaque.jpg)

## Numbers for signs

The paper's engine is a code. Gödel gave each basic sign of his system a number, and in his translator's notation they are these:

| Sign   | 0   | succ | ¬   | ∨   | ∀   | (   | )   |
| ------ | --- | ---- | --- | --- | --- | --- | --- |
| Number | 1   | 3    | 5   | 7   | 9   | 11  | 13  |

Variables got powers of primes above 13. A string of signs with numbers _n_₁, _n_₂, …, _n_ₖ gets the single number 2^_n_₁ · 3^_n_₂ · 5^_n_₃ ⋯, the primes in order carrying the codes as exponents. Take a string of our own choosing, _ff_0, the successor of the successor of zero, which is the number two: its codes are 3, 3, 1, so its number is 2³ · 3³ · 5¹ = 8 · 27 · 5 = 1080. Going back is only factoring, as the plate draws it: 1080 = 2 · 2 · 2 · 3 · 3 · 3 · 5, three 2s, three 3s and one 5, so the signs were _f_, _f_, 0. Real formulas give enormous numbers. A formula of four signs saying that zero belongs to a class, its variable coded 17², the least code its kind of variable allows, comes to 2²⁸⁹ · 3¹¹ · 5 · 7¹³, a number of 104 digits, by our arithmetic.

A proof is a string of formulas, so it has a number too. Statements about formulas and proofs become statements about numbers, which arithmetic itself can make. Gödel built up forty-six definitions, from "_x_ is divisible by _y_" to the forty-sixth, "_x_ is a provable formula". Then, by a diagonal construction like Cantor's, he found a formula with number _g_ that says: the formula with number _g_ is not provable. Call it G. If G were provable, the system would prove something false, so a consistent system cannot prove it. So G is unprovable, which is what it says: it is true. Its negation is not provable either. The second theorem follows from formalising this argument inside the system. If the system could prove "I am consistent", then by the argument just given it could prove G, and it cannot.

## What it ended

**[Hilbert's programme](kloom:e/hilberts-program)** had hoped to prove, by finite means inside mathematics, that mathematics is consistent. The second theorem is usually read as ending that hope as Hilbert meant it; Gerhard Gentzen's consistency proof for arithmetic in 1936 used an infinite induction that not everyone accepts as finite, and whether Gödel settled Hilbert's second problem is still disputed. Hilbert, his biographer says, was at first "somewhat angry". In 1950 **[Alan Turing](kloom:e/alan-turing)**, arguing that machines might think, answered "the mathematical objection", that Gödel's theorem limits machines and not minds: it had "only been stated, without any sort of proof", he replied, that no such limits apply to us.

## Princeton

Gödel first visited the **[Institute for Advanced Study](kloom:e/institute-for-advanced-study)** in 1933, and lectured there on his theorems in 1934. After the murder of his teacher Moritz Schlick in 1936 he suffered a breakdown and a lasting fear of being poisoned. In March 1940 he and his wife Adele reached San Francisco from Nazi Vienna, by the Trans-Siberian Railway and the Pacific, and he stayed at the Institute for the rest of his life. There a close friend was **[Albert Einstein](kloom:e/albert-einstein)**: they walked home together, and in Oskar Morgenstern's telling Einstein said late in life that he came to the Institute "merely to have the privilege of walking home with Gödel". For Einstein's seventieth birthday, it is said, Gödel gave him a solution of his equations of gravitation, a rotating universe in which one could travel into one's own past. He ate only what Adele prepared, and when she went into hospital in late 1977 he stopped eating. He died on 14 January 1978, weighing 29 kilograms.

Gödel had shown that no system can prove every truth. Whether some procedure could at least decide, mechanically, what a system can prove was a separate question, and in 1934 his audience at Princeton had included the logician who would answer it first.

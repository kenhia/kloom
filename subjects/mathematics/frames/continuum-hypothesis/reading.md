At the end of a paper he dated at Halle on 11 July 1877 and published in Crelle's _Journal_ the next year, **[Georg Cantor](kloom:e/georg-cantor)** asked a question and guessed its answer. He had shown that the whole numbers and the real numbers are infinities of different sizes. Were there any sizes in between? He guessed that every infinite collection of real numbers can be paired either with the whole numbers or with all the real numbers. The guess is the **[continuum hypothesis](kloom:e/continuum-hypothesis)**, the _continuum_ being the line of real numbers. It took eighty-five years to learn that the usual axioms cannot settle it, and what that means is still argued.

![A printed page in German headed "Cantor, ein Beitrag zur Mannigfaltigkeitslehre" and numbered 257: a formula for numbering pairs of whole numbers, then a long paragraph ending with the classes of linear manifolds, whose number is "gleich zwei", equal to two](cantor-1878.jpg)

## Two classes

The page asks how the infinite sets of points on a line "fall into classes" when sets of the same _Mächtigkeit_, power, go into one class. In our translation: "By a process of induction, which we shall not describe here, we are led to the theorem that the number of classes of linear manifolds arising from this principle is finite, and indeed that it is equal to two." He put off "the exact investigation of this question to a later occasion." It never came: Cantor believed at times that he could prove it, and never did. In 1900 **[David Hilbert](kloom:e/david-hilbert)** made it the first of his problems for the new century.

## How big is the continuum?

Every real number between 0 and 1 has a binary expansion, a string of 0s and 1s, and a string of 0s and 1s is the same as a set of whole numbers: the places where the 1s stand. Take, for an example of our own, the set {1, 3, 4}:

| Place        | 1   | 2   | 3   | 4    | 5 … |
| ------------ | --- | --- | --- | ---- | --- |
| In the set?  | yes | no  | yes | yes  | no  |
| Binary digit | 1   | 0   | 1   | 1    | 0   |
| Worth        | 1/2 | 0   | 1/8 | 1/16 | 0   |

So {1, 3, 4} is the number 0.1011 in binary, which is 1/2 + 1/8 + 1/16 = 11/16. The plate draws the same choice as a path down a tree, left for 0 and right for 1, closing in on 11/16 on the line below. Endless paths give every point of the line, and (after a small repair for numbers like ½, which have two expansions) the real numbers are exactly as many as the sets of whole numbers. The whole numbers are ℵ₀; their sets, and so the real numbers, are 2 to the power ℵ₀, written 𝔠, and Cantor proved 𝔠 larger than ℵ₀. The next infinity after ℵ₀ is called ℵ₁. The continuum hypothesis is the equation 𝔠 = ℵ₁.

## Neither proof nor disproof

The first half of the answer came from **[Kurt Gödel](kloom:e/kurt-godel)**. In a note to the _Proceedings of the National Academy of Sciences_ in November 1938 he announced that the hypothesis and the axiom of choice can be added to the axioms of set theory without contradiction, if those axioms were free of it already. He built a model of mathematics out of the _constructible_ sets alone, the sets that can be defined step by step, and in it the hypothesis holds. He thought that the statement that every set is constructible "seems to give a natural completion of the axioms". By 1947 he thought the opposite of the hypothesis: that the continuum problem would lead to "new axioms which will make it possible to disprove Cantor's conjecture."

The second half came from **[Paul Cohen](kloom:e/paul-cohen)**, a young mathematician at Stanford who had made his name in analysis. His note "The Independence of the Continuum Hypothesis" was communicated to the same _Proceedings_ by Gödel on 30 September 1963. Cohen invented **[forcing](kloom:e/forcing-mathematics)**, a method for adjoining new sets to a model of the axioms, here new real numbers, until the continuum is bigger than ℵ₁ and every axiom still holds. Together, Gödel's model and Cohen's show that **[Zermelo–Fraenkel set theory](kloom:e/zermelo-fraenkel-set-theory)** with the axiom of choice, ZFC, the axioms most mathematics rests on, can neither prove the hypothesis nor refute it. Cohen was awarded a Fields Medal in 1966, and as of 2026 it is still the only one given for work in logic.

The axioms allow the continuum many sizes, but not every size:

| The size of the continuum | Allowed by ZFC? | Where it holds                                       |
| ------------------------- | --------------- | ---------------------------------------------------- |
| ℵ₁                        | yes             | Gödel's constructible sets; Woodin's hoped-for model |
| ℵ₂                        | yes             | the forcing axiom Martin's maximum, and Woodin's (*) |
| ℵ₃₅, or ℵ₁₀₀₀             | yes             | models built by forcing                              |
| ℵ\_ω, the first limit     | no              | ruled out by Kőnig's theorem of 1906                 |

## Is there an answer?

Cohen thought the independence was the end of the matter: the hypothesis could be taken or left. Gödel thought it showed only that the axioms were too weak, and that new ones, justified on their own merits, would decide it. Most set theorists side with Gödel on that, _Quanta Magazine_ reported in 2021, and disagree about which way it goes.

**[W. Hugh Woodin](kloom:e/w-hugh-woodin)** has argued both ways. In the 1990s he proposed an axiom he called (\*), which makes the continuum ℵ₂. In 2021 David Asperó and Ralf Schindler proved, in the _Annals of Mathematics_, that (\*) follows from a strong form of Martin's maximum, joining two of the most studied new axioms in a picture where the hypothesis is false. But Woodin had by then changed his mind. He conjectures that there is an _ultimate L_, a model like Gödel's constructible universe that can hold almost every large infinity set theorists study, and in it the hypothesis is true. "I'm considered a traitor," he told _Quanta_. Others, among them Joel David Hamkins and Saharon Shelah, think there are many equally good universes of sets, and no one answer.

As of September 2026 the ultimate L conjecture was unproved, no new axiom had been generally accepted, and Cantor's question of 1877 was still open in the only sense left to it: which axioms to believe. That is where the Infinity trail ends, back where it began, with Cantor's infinities.

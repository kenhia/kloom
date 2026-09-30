On 16 June 1902 the thirty-year-old **[Bertrand Russell](kloom:e/bertrand-russell)** wrote from England to **[Gottlob Frege](kloom:e/gottlob-frege)**, a professor of mathematics at Jena. The letter began with admiration for Frege's work and then, in a few lines, showed that it contained a contradiction. The second volume of Frege's life's work was already at the printer. He answered within a week, and added an afterword to the book, which opens: "Hardly anything more unwelcome can befall a scientific writer than to have one of the foundations of his building shaken after the work is finished."

## A script for thought

Frege's aim was to show that arithmetic is logic: that numbers and their laws could be derived from principles of pure reasoning, with no appeal to intuition anywhere. For that, ordinary language and Boole's algebra were too loose, so in 1879 he invented a notation of his own, the **[_Begriffsschrift_](kloom:e/begriffsschrift)**, or "concept-script". It could _quantify_, saying "for all" and "there is" of things and of relations between them, and so could write down, and check, arguments that Aristotle's syllogisms could not express, such as Euclid's proof that the primes never end. Frege wrote it in two dimensions, as branching lines, and nobody has written it since; its ideas, in other notation, are the logic every mathematician now uses.

![Two formulas from Frege's Begriffsschrift of 1879, numbered 87 and 88: each is a long horizontal stroke with vertical strokes branching down from it to conditions set at the right, written as F(z), f(y, z) and so on, and one with a small cup on its stroke marking "for all"](begriffsschrift-88.png)

The derivation itself came in the _Grundgesetze der Arithmetik_, the _Basic Laws of Arithmetic_, whose first volume appeared in 1893; the second, which he paid for himself, in 1903. One of its basic laws, Law V, says in effect that every concept has an extension: whatever can be said of things picks out the class of things it is true of. Frege himself had admitted in 1893 that this law was less evident than the others.

## The class that cannot exist

Frege's afterword sets out the contradiction in his own words, and it can be followed step by step. No one, he says, will claim that the class of men is a man. So here is a class that does not belong to itself. Take the concept "class that does not belong to itself", and by Law V its extension, the class of all such classes; call it _K_, as Frege did. Then ask whether _K_ belongs to itself.

- Suppose it does. Then it is one of the classes that do not belong to themselves, so it does not.
- Suppose it does not. Then it is exactly the kind of class _K_ collects, so it does.

Either way, a contradiction. In symbols, with _K_ = {_x_ : _x_ ∉ _x_}, it is _K_ ∈ _K_ if and only if _K_ ∉ _K_. The plate draws _K_ with the class of men inside it, and its own copy on the edge, which can go neither in nor out. Nothing in the argument uses numbers or infinity, only the idea that every property defines a class, and that was the ground under Cantor's sets as well as Frege's. Frege saw it: the blow fell, he wrote, on everyone who had used classes in their proofs, and in a footnote he named Richard Dedekind's among them.

The popular form is a village barber who shaves all those, and only those, who do not shave themselves. Russell disowned it. The barber, he said, is just a man who cannot exist; the class problem is not so easily dismissed.

Russell had found the contradiction in 1901, while probing Cantor's proof that there is no largest infinity, but his own tellings of when drift from June to "the spring" to May. He was not quite first. **[Ernst Zermelo](kloom:e/ernst-zermelo)** had found the same argument at Göttingen, perhaps years earlier, and told **[David Hilbert](kloom:e/david-hilbert)**, who reminded Frege of it in 1903; Zermelo never published it.

## Two ways out

Both repairs came in 1908. Zermelo gave set theory axioms. His axiom of separation lets a property carve a subset only out of a set already given, never out of everything. Run the argument on a given set _A_, and it no longer contradicts anything: it proves that the class of _A_'s members that are not members of themselves is not in _A_. So no set contains everything, and no universal set exists. With later additions, Zermelo's axioms became the standard foundation of mathematics.

Russell's way was a theory of _types_, in which a class and its members live at different levels, so that "_x_ ∈ _x_" cannot even be written. On it he and **[Alfred North Whitehead](kloom:e/alfred-north-whitehead)** built **[_Principia Mathematica_](kloom:e/principia-mathematica)**, three volumes, 1910 to 1913, deriving mathematics from logic as Frege had meant to. On page 379 of the first volume stands proposition ✳54.43, with the note: "From this proposition it will follow, when arithmetical addition has been defined, that 1 + 1 = 2." That proof is finished only in the second volume, as ✳110.643, with the remark "The above proposition is occasionally useful." In 1956 the Logic Theorist, one of the first programs to prove theorems, proved 38 of the first 52 theorems of the book's second chapter.

Frege never found a repair that satisfied him. He died in 1925, little read; a diary from his last year, published in 1994, shows him bitterly antisemitic. The machinery of _Principia_, and of Gödel's theorems to come, was his. The paradoxes left mathematicians wanting a proof that their axioms could never contradict themselves, and David Hilbert set out to find one.

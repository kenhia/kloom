When the physics of computation split into three courses, [Feynman](kloom:e/richard-feynman) kept
his strand and gave it a title of his own: **Potentialities and
Limitations of Computing Machines**. It was the last course he taught at
Caltech, and it was about computer science, not physics. Eight years
after his death it became a book, the [_Feynman Lectures on Computation_](kloom:e/feynman-lectures-on-computation).

## The course

The dates vary a little with the source. The Caltech record, as the book's
editor **[Tony Hey](kloom:e/tony-hey)** reports it, has the course starting in the autumn of
1983, and the publisher gives 1983 to 1986; Hey's own abstract of the
book, from 1996, says 1984 to 1986. Hey writes that Feynman lectured on
computation first with [Hopfield](kloom:e/john-hopfield) and [Mead](kloom:e/carver-mead), and then with **Gerald Jay
Sussman**, a computer scientist from MIT. Guest speakers included
**[Marvin Minsky](kloom:e/marvin-minsky)**, **Charles Bennett** and Hopfield again.

Feynman did not survey the field. He rebuilt it from the bottom, in his
own order. A computer, he told the class, is a file clerk who spends most
of the time shuffling information from one place to another and only now
and then does any processing. From that picture he built up logic gates, memory,
instructions and the hierarchy of languages, then finite-state machines
and, in the phrase the book keeps, "Mr. [Turing](kloom:e/alan-turing)'s machines". Throughout, he urged
students to play with a problem and work it out for themselves before
looking up the answer.

| Chapter | Subject                                                     |
| ------- | ----------------------------------------------------------- |
| 1       | Introduction to computers: the file clerk                   |
| 2       | Computer organization: gates, memory, instructions          |
| 3       | The theory of computation: finite-state and Turing machines |
| 4       | Coding and information theory: Shannon's theorem            |
| 5       | Reversible computation and the thermodynamics of computing  |
| 6       | Quantum mechanical computers                                |
| 7       | Physical aspects of computation: the physics of chips       |

## What a bit costs

The chapter at the book's center asks the question the physics of
computation began with: is there a least amount of energy a computation
must spend? The answer that [Landauer](kloom:e/rolf-landauer) and Bennett had given, and Feynman
worked through for students, is that computing need cost nothing, but
forgetting does. The plate draws the textbook argument. Keep one bit as a
single molecule of gas in a cylinder: the left half is 0, the right half
is 1. To erase the bit, to set it to 0 whatever it was, push a piston in
from the right to the middle. The molecule is now certainly on the left,
and compressing its one-molecule gas to half its volume at a steady
temperature _T_ takes work _kT_ ln 2, the hatched area under the curve.
That work leaves as heat. At room temperature it is about 3 × 10⁻²¹
joules, a figure a team in France and Germany measured directly for the
first time in 2012.

A computer that never erases, that keeps the information it would have
thrown away and later runs itself backwards to clear it, need not pay
even that. It is the argument behind the reversible gates of Feynman's
1985 paper, which the book reprints as its sixth chapter.

## The book

In November 1987, Hey has written, Feynman's long-time secretary **Helen
Tuck** called to say that Feynman wanted him to write up the lecture
notes. Feynman died in February 1988. Hey and **Robin Allen** edited the
lectures, and _Feynman Lectures on Computation_ appeared from
Addison-Wesley in 1996. A companion volume of essays by colleagues, _Feynman and Computation_,
followed in 1999.

In 2023 an anniversary edition added three chapters by others: on
computing beyond [Moore's law](kloom:e/moores-law), on Feynman and [artificial intelligence](kloom:e/artificial-intelligence), and,
by **John Preskill**, "Quantum Computing 40 Years Later", an account of
how far his proposal had come. The trail's last frame takes that story
on to 2026.

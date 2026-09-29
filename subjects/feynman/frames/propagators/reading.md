[Feynman](kloom:e/richard-feynman)'s papers of 1949 turned [quantum electrodynamics](kloom:e/quantum-electrodynamics) into something that could be drawn. A calculation became a set of pictures, and each picture stood for one term of the answer, to be written down from the picture by rule. The rules are few. This frame sets them out; the anchor frame, Diagrams, has the paper in which the first of the pictures was printed.

## Three pieces

Everything in QED, Feynman said, is made of three things happening. An electron goes from one point in space and time to another. A photon goes from one point to another. And an electron emits or absorbs a photon. The first two are the lines of a diagram, the third its corners, or _vertices_.

Each piece carries a factor. The function that gives the amplitude for an electron to get from one point to another, which Feynman wrote K₊ and later textbooks called the electron [_propagator_](kloom:e/propagator), is the factor for a straight line; the photon's propagator is the factor for a wavy one; and each vertex contributes the electron's charge, _e_, with a matrix that keeps track of its spin. Multiply the factors for every line and vertex in a drawing, add up over every place and time at which the vertices could happen, and the result is that diagram's contribution to the amplitude. The plate draws the three pieces, each with its factor as the momentum-space rules write it, and two ways for two electrons to scatter.

By the mid-1950s textbooks printed the rules as a table: this line gives this factor, this corner gives that one. The historian **[David Kaiser](kloom:e/david-kaiser-physicist)** reproduces one from **Josef Jauch** and **[Fritz Rohrlich](kloom:e/fritz-rohrlich)**'s _The Theory of Photons and Electrons_ (1955), where each piece of a diagram has exactly one mathematical meaning. Feynman had arrived at some of them less formally. In his Nobel lecture he said he first settled the signs of certain terms empirically, by inventing rules and trying them.

## Scattering, one photon at a time

Two electrons approach, repel and fly apart. The simplest diagram for it has each electron's line bend once, at a vertex, with one photon passing between them. There are two vertices, so the amplitude carries _e_ twice, _e²_.

Next come diagrams with two photons exchanged, and diagrams in which an electron emits a photon and reabsorbs it itself, and diagrams in which the photon in flight briefly becomes an electron and a positron. Each has four vertices, so _e⁴_. With three photons, six vertices, _e⁶_. The ordering of the terms is simply the count of vertices, and a physicist can list every term of a given order by drawing every way of connecting the lines.

## Why the series works

In the units physicists use, _e²_ is proportional to the [_fine-structure constant_](kloom:e/fine-structure-constant), α, a pure number close to 1/137. In his book [_QED_](kloom:e/qed-the-strange-theory-of-light-and-matter) (1985) Feynman gave the amplitude for an electron to emit or absorb a photon as about −0.085, whose square is 1/137. So each extra pair of vertices makes a term roughly a hundred times smaller than the one before, and a few orders are enough for most purposes.

The table works it out as a rough scale. It leaves out everything but the powers of α: the factors of π, the numbers that come out of each diagram's integral, and the number of diagrams at each order, which grows fast. It is arithmetic, not a measurement.

| Photons exchanged | Vertices | Factor | Size, as a fraction |
| ----------------- | -------: | ------ | ------------------: |
| one               |        2 | α      |              0.0073 |
| two               |        4 | α²     |           0.000 053 |
| three             |        6 | α³     |        0.000 000 39 |

This is what made the diagrams practical in QED and troublesome elsewhere. Where the coupling is small, the first few diagrams give the answer. Where it is not, as in the forces that hold the nucleus together, every order is as big as the last, and the drawings stop being a sum that converges; the last frame of this trail, Dispersion, follows physicists who kept drawing them anyway.

## Loops

A diagram with a closed loop, an electron emitting and reabsorbing its own photon, sends momentum round the loop with nothing to fix it, and summing over every possible momentum gives the infinities of the frame before. Feynman's 1949 paper, following [Bethe](kloom:e/hans-bethe), showed that the infinite parts only change the electron's mass and charge. Expressed in the measured mass and charge, every other effect came out finite. The self-energy loop is the one behind the [Lamb shift](kloom:e/lamb-shift).

One of Feynman's rules did something the older methods could not do simply. Where they counted electrons and positrons as separate particles, and the positron as a hole in a sea of electrons, his electron line could run backwards in time, and the next frame, Backwards in time, is about that line.

In July 1961 the _IBM Journal of Research and Development_ printed a paper
by **[Rolf Landauer](kloom:e/rolf-landauer)**, a physicist at **[IBM](kloom:e/ibm)**'s research division, that
asked where the shrinking of computers must stop. His answer
was not about size or speed. A computer, he argued, must now and then
throw information away, and throwing away one bit must give off at least
_kT_ ln 2 of heat, where _T_ is the temperature and _k_ is **[Boltzmann's
constant](kloom:e/boltzmann-constant)**. That floor, now called **[Landauer's principle](kloom:e/landauers-principle)**, was the first
place where information, as Shannon measured it, had a price in joules.

## Restore to one

Landauer's bit is the plate's upper drawing, his own first figure: a
particle in a well with two hollows, a barrier between them, the left
hollow called ZERO and the right ONE. Now reset it: make it ONE, whatever
it was. If you know where the particle is, that costs nothing: leave it,
or push it over the barrier and catch the energy back as it rolls down.
But a computer does not look first. It applies one operation to whatever
data arrive.

No single push can do that without loss, he showed. The laws of motion
run backwards as well as forwards; a frictionless push that took both
ZERO and ONE to ONE would, reversed, take one starting state to two
different ends, which mechanics forbids. So the reset needs friction,
and friction makes heat. Counting states gives the least of it. A bit
that could be either has two states; after the reset it has one. Its
entropy has fallen by _k_ ln 2, "0.6931 _k_ per bit", and since the
entropy of a closed system cannot fall, that much must appear in the
surroundings as heat: 0.6931 _kT_ per bit, "a minimum heating effect",
he wrote, with "no guarantee that this minimum is in fact achievable."

He called an operation _logically irreversible_ when its output does not
fix its input. Erasure is one, and so is AND: an output of 0 could have
come from three different inputs. His argument, he noted, did not rest on
the analogies "frequently made in other writings" between entropy and
information. He started instead from **[Léon Brillouin](kloom:e/leon-brillouin)**'s claim that a
measurement must cost about _kT_: computing, he wrote, is closely akin to
measuring, though the link is hard to argue exactly. He also asked whether a computer could avoid erasing by keeping
everything, and concluded that it could not be useful if it did. That
conclusion did not last.

At room temperature, 300 kelvin, _kT_ ln 2 is 2.9 × 10⁻²¹ joules, about
0.018 electronvolts, by our arithmetic. One joule would pay for erasing
some 3.5 × 10²⁰ bits.

## A bead in a double well

For fifty years the bound was a calculation. In March 2012 a team from
the École normale supérieure de Lyon and the universities of Augsburg and
Kaiserslautern, Antoine Bérut, Sergio Ciliberto, Eric Lutz and three
colleagues, reported in
_Nature_ that they had measured it. Their bit was a silica bead two
microns across, in water, held by a laser beam switched ten thousand times
a second between two spots a micron apart: a double well made of light. To erase it they
did what the plate's lower row draws: lower the barrier, tilt the well
by moving the cell so the water drags the bead, and raise the barrier
again, leaving the bead in ZERO whichever side it began.

From the bead's tracked path they worked out the heat each erasure gave
off. The slower the erasure, the less heat, and the average approached
_kT_ ln 2. In their fuller account of 2015 a fit to the slow runs gave
0.72 _kT_, against the bound's 0.693 _kT_. Some single erasures gave off
less than the bound, a few even took heat in: the principle holds for
the average, as the second law does. A feedback trap at Simon Fraser
University in 2014 and nanomagnets at Berkeley in 2016 gave results that
agreed with the bound; the nanomagnet flip took about 44 per cent more.

Not everyone accepts the argument. The philosopher of science John
Norton has called it circular, a consequence assumed rather than
derived; Charles Bennett and others have answered that it is the second
law applied to machines, and later work derived it from the second law
with measurement and feedback included.

## How far above it we compute

![Bar chart on a logarithmic scale of energy in joules: Landauer's bound at 300 K, 2.9 × 10⁻²¹; a nanomagnetic bit flipped in 2016, 4.2 × 10⁻²¹; switching a CMOS logic gate, 10⁻¹⁶ at the least; one 16-bit floating-point operation, about 1.5 × 10⁻¹³; moving a bit across a chip, about 6 × 10⁻¹³; reading a bit from DRAM, about 5 × 10⁻¹²](energy-per-bit.svg)

| What                                | Joules      | Times kT ln 2 (ours) |
| ----------------------------------- | ----------- | -------------------: |
| Landauer's bound, 300 K             | 2.9 × 10⁻²¹ |                    1 |
| A nanomagnetic bit, 2016            | 4.2 × 10⁻²¹ |                  1.5 |
| Switching a CMOS gate, at the least | 10⁻¹⁶       |               35,000 |
| One 16-bit floating-point operation | 1.5 × 10⁻¹³ |           52 million |
| Moving one bit across a chip        | 6 × 10⁻¹³   |          210 million |
| Reading one bit from DRAM           | 5 × 10⁻¹²   |          1.7 billion |

As of 2026 the machines are nowhere near the floor. The figures for
today's chips, gathered in 2023 by Anson Ho, Ege Erdil and Tamay
Besiroglu, put switching a gate at tens of thousands of times the bound
at best, and moving data far above that. Much of a chip's heat is not the
price of forgetting at all, but of charging and discharging its wires.
Their own estimate is that ordinary chips, pushed to their limits, might
become only about two hundred times more efficient.

Landauer's floor is low, but it is a floor only for machines that forget.
Whether a computer must forget is the question of the trail's next
frame, reversible computing.

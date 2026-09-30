In 1929 the _Zeitschrift für Physik_ printed a paper by a young Hungarian
lecturer at the University of Berlin, **[Leo Szilard](kloom:e/leo-szilard)**, with a title that
said exactly what it was about: "On the decrease of entropy in a
thermodynamic system by the intervention of intelligent beings". It shrank
Maxwell's demon to its smallest case, one molecule in a box and one
yes-or-no question about it, and put a number on what the demon's knowing
must cost. That number, _k_ ln 2, turned up again, in other forms, in
every later chapter of the story.

## Why one molecule

Szilard had come to Berlin from Budapest at the end of 1919 and heard
lectures by Einstein, Planck and Max von Laue, whose assistant he became
in 1924. His doctoral
dissertation of 1922 was on thermodynamic fluctuations, the small, random
departures from equilibrium that Einstein's work on Brownian motion had
made visible; Wikipedia's article on him says it already bore on
Maxwell's demon. The paper on intelligent beings was written soon after,
served as his habilitation lecture when he qualified to teach in 1927, and
was published two years later.

Fluctuations were the demon's new opening. In 1914 **[Marian
Smoluchowski](kloom:e/marian-smoluchowski)** had shown why an automatic demon fails: a trapdoor on a
spring, light enough to be pushed open by one molecule, is itself jostled
by the molecules until it flaps at random, and sorts nothing. But he left
one door open: a machine that beat the second law "might, perhaps,
function regularly if it were appropriately operated by intelligent
beings." Szilard took up exactly that case, and made it as simple as it
can be made.

## The engine

A cylinder holds a single molecule and sits in a bath of heat at
temperature _T_. The molecule bounces about, taking energy from the walls
and giving it back. The plate draws the cycle.

| Step | What happens                                                                      |
| ---- | --------------------------------------------------------------------------------- |
| 1    | A partition is slid into the middle of the cylinder                               |
| 2    | The operator looks, and learns which half holds the molecule                      |
| 3    | The partition, now a piston, is let move towards the empty half, lifting a weight |
| 4    | The piston reaches the end, is removed, and the cylinder is as it began           |

In step 3 the one-molecule gas pushes the piston as any gas would, and the
bath keeps its temperature up, so heat flows in from the bath and leaves
as work. By the ideal-gas law with one molecule, _pV_ = _kT_, doubling the
volume at steady temperature yields work _kT_ ln 2. At room temperature,
300 kelvin, that is about 2.9 × 10⁻²¹ joules, my arithmetic from the
exact value of _k_. Small, but the cycle can be repeated forever, and it
draws work from a single bath with no colder body to spill heat into,
which is what Thomson's statement of the second law forbids. Everything turns on step 2. Without knowing which side the
molecule is on, the operator cannot tell which way to connect the weight,
and on average gets nothing.

## The price of knowing

Szilard did not try to show that no being could do step 2 for free.
Instead he assumed the second law holds, and asked what it demands. His
answer was that the measurement must produce, on average, at least as
much entropy as the engine removes: _k_ ln 2, where _k_ is Boltzmann's constant. For the
first time a quantity of entropy was tied to a single binary choice, what
would later be called a bit.

Where exactly the cost falls is still argued. Most readers took Szilard
to mean that measuring costs entropy, and **[Léon Brillouin](kloom:e/leon-brillouin)** and **[Dennis
Gabor](kloom:e/dennis-gabor)** built arguments on that from the 1950s. **[Charles Bennett](kloom:e/charles-h-bennett-physicist)** pointed
out in 2003 that the paper is "tantalizingly ambiguous": its prose puts
the cost in the measurement, but its detailed analysis at the end puts it
where the memory is reset for the next cycle. Owen Maroney's article in
the _Stanford Encyclopedia of Philosophy_ agrees that it is the erasure,
not the measurement, that pays in Szilard's own example. When the idea
arrived from communications engineering after the Second World War, John
von Neumann pointed out, in a review of Norbert Wiener's _Cybernetics_,
that Szilard had been the first to equate information with entropy.

That is where the trail goes next: to Claude Shannon's entropy of a
message in 1948, to Rolf Landauer's price for erasing a bit in 1961, and
to Bennett's reversible computer, which found that erasing, not knowing,
is what the demon cannot do for free.

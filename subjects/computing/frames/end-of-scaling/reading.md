The count of transistors never stopped climbing. What stopped, around
2005, was the free ride that came with it: the rule that a smaller
transistor was also faster and no hotter. Since then each doubling has
been bought with new shapes of transistor, new ways of printing them, and
eventually by giving up on putting everything on one piece of silicon.

## The power wall

[Dennard's scaling](kloom:e/dennard-scaling) assumed that voltage fell with size. By the mid-2000s it
could not fall much further: the threshold voltage at which a transistor
turns on did not shrink with it, and the current leaking through a
transistor that was meant to be off grew. Power per square millimeter began to rise with each
shrink. Clock speeds, which had climbed from megahertz to gigahertz, went
flat. [Intel](kloom:e/intel) reached 2 GHz in August 2001 and 3.4 GHz by early 2005, but in
2004 it canceled its next Pentium 4 designs and dropped its plans for a 4 GHz
chip. Since then clock rates have stayed at about 4 to 6 GHz.

**Herb Sutter**'s essay _The Free Lunch Is Over_, in the March 2005 _Dr.
Dobb's Journal_, told programmers what this meant: the curve of clock
speeds had turned sharply around the start of 2003, and from now on the
extra transistors would arrive as more processor _cores_, which only
software written to run in parallel could use. Intel's dual-core Pentium
D came out in May 2005. The gains for a single core
slowed: by the figures Wikipedia gives, about
52 percent a year from 1986 to 2003, 23 percent to 2011, and 7 percent
from 2011 to 2018.

## New shapes, new light

A flat transistor has its gate on one side of the channel, and as the
channel shortens the gate loses control of it and current leaks through.
The answer was to wrap the gate round the channel, as the plate shows. In
2011 Intel made its 22-nanometer transistors as **[FinFETs](kloom:e/fin-field-effect-transistor)**, standing the
channel up as a thin fin, 8 nm wide, with the gate over three sides. The
next step surrounds the channel completely, in stacked horizontal sheets:
**[Samsung](kloom:e/samsung-electronics)** began production of such _gate-all-around_ transistors at
3 nm on 30 June 2022, **[TSMC](kloom:e/tsmc)** started volume production of its 2 nm
nanosheet process in the fourth quarter of 2025, and **Intel**'s 18A,
with its _RibbonFET_ nanosheets and power wiring moved to the back of the
wafer, is in high-volume production in the United States.

Printing the patterns needed new light. **ASML**'s [extreme-ultraviolet
lithography](kloom:e/euv-lithography) uses light of 13.5 nm wavelength, more than fourteen times
shorter than the 193 nm deep ultraviolet before it, made by hitting
molten tin droplets about 25 microns across with a laser, 50,000 times a
second. Intel assembled the first commercial high-NA machine, for finer
features still, in April 2024.

## Names that are not sizes

A node's name once measured its transistors. It stopped in the mid-1990s,
when gates were shrunk faster than everything else, and by the FinFET
the name matched nothing on the chip. **Paolo Gargini**, chairman of the IEEE's International
Roadmap for Devices and Systems (IRDS), proposed in 2020 quoting the two pitches that actually limit density, the
contacted gate pitch and the metal pitch.

| Node name      | What was measured or projected                            | Source                    |
| -------------- | --------------------------------------------------------- | ------------------------- |
| "130 nm"       | gate length 70 nm                                         | _IEEE Spectrum_, 2020     |
| Intel "22 nm"  | gate length 26 nm, metal half-pitch 40 nm, fins 8 nm wide | _IEEE Spectrum_, 2020     |
| "5 nm"         | contacted gate pitch 48 nm, metal pitch 36 nm             | IRDS, via _IEEE Spectrum_ |
| "2.1 nm" label | contacted gate pitch 45 nm, metal pitch 20 nm (projected) | IRDS 2021, via Wikipedia  |

## Chiplets, and where the doubling stands

When a chip cannot grow, the package can. A _chiplet_ design joins several
dies side by side in one package, each made on the process that suits
it: Apple's M3 Ultra is two dies joined by a bridge, and [Nvidia](kloom:e/nvidia)'s Rubin,
the last bar of the transistor-count
chart in the frame on [Moore's law](kloom:e/moores-law), is two dies at the maximum size a
lithography machine can print, working as one GPU. The appetite for
arithmetic that drives the largest of these packages is a story of its
own, in the data centers of AI.

As of 28 September 2026, the counts still double, but by the industry's
own account more slowly and at rising cost. Intel's chief executive said at
the end of 2023 that doubling was coming "closer to every three years";
Nvidia's had called Moore's law dead in 2022. In 2020 Gargini expected
lithography to reach its limit around 2029, and density to continue after
that only by stacking layers of transistors on each other.

From a gold-foil wedge on germanium to sheets of silicon a few atoms
thick, the switch that the telephone company wanted in 1947 is still the
one being shrunk.

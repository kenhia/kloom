A fission bomb blows itself apart. The moment enough uranium or plutonium
is brought together, neutrons multiply through it faster and faster; the
energy they release heats the metal and drives it outward; and as it
expands the neutrons escape more easily, until the chain reaction stops.
Everything the bomb will ever release happens in that short race. The
first question [Los Alamos](kloom:e/los-alamos-national-laboratory) had to answer was how much of the material would
fission before the race was lost: the bomb's _efficiency_.

## From Serber's lectures to a formula

In April 1943 **[Robert Serber](kloom:e/robert-serber)** gave the new laboratory five lectures on
the bomb, typed up as its first report, the [_Los Alamos Primer_](kloom:e/los-alamos-primer). They
included an estimate of the efficiency for an assembly only a little over
critical, made at Berkeley the summer before. It was rough, and Serber
later recalled [Oppenheimer](kloom:e/j-robert-oppenheimer)'s displeasure with how casually it treated the
expansion.

Through 1943 **[Hans Bethe](kloom:e/hans-bethe)** and [Feynman](kloom:e/richard-feynman) worked out something better. The
laboratory's official history, written in 1946 and 1947, describes the
steps. Feynman's group, **T-4**, calculated efficiencies for masses far
above critical, using results from Serber's group on how quickly the
neutrons' multiplication slows as the metal expands. Bethe and Feynman
then made a semi-empirical formula that fitted those calculations at the
top end and reduced, at the bottom, to the Berkeley one. They argued that
it would hold in between too, since it held at both extremes. By the end of
1943, the history says, the laboratory could give a reasonably good
account of the efficiency of any proposed design.

The derivation is still classified, but its form is published. In the
version that physicists from Los Alamos and Livermore printed in 2021, the yield of a bare sphere
of fissile metal is

**Y = f · M · R₀² · α₀² · δ**

where _M_ is the mass, _R₀_ its radius when it goes off, _α₀_ the rate at
which the neutron population grows (it multiplies by _e_ every 1/_α₀_
seconds), and _δ_ how far the sphere must swell, as a fraction of its
radius, before it falls below critical again. Bethe and Feynman's guess
was that the growth rate falls in proportion to the expansion; the plate
draws it falling in a straight line to nothing, and the area under that
line is the energy. The number _f_ in front is what their calculations
supplied.

| Illustrative 80 kg sphere of uranium-235 | Value                  |
| ---------------------------------------- | ---------------------- |
| Critical mass at normal density          | 46.6 kg, radius 8.4 cm |
| Radius when it goes off, _R₀_            | 10.0 cm                |
| Radius when it falls subcritical, _R₂_   | 11.0 cm                |
| Expansion needed, _δ_ = _R₂_/_R₀_ − 1    | 0.10                   |

The numbers are the 2021 paper's worked example, not a real weapon. It
shows how little room there is: a swelling of a tenth of the radius ends
the reaction. The same paper points out that **[Otto Frisch](kloom:e/otto-robert-frisch)** and **[Rudolf
Peierls](kloom:e/rudolf-peierls)** had written down a formula of the same shape in Birmingham in
1940, and Serber's differed only in the number in front: about 0.2 for
Frisch and Peierls, a third for Serber. There is no sign that Bethe and
Feynman knew of the British memorandum, although Peierls later worked in
the same building as they did at Los Alamos.

## The Water Boiler

T Division also had to calculate the **Water Boiler**, a small reactor of
uranium salt dissolved in water inside a steel sphere a foot across,
proposed by Robert Bacher in April 1943 to measure critical conditions
with real material. The theorists thought it a distraction, but its
calculations took an inordinate share of their time that year. In his own
account Feynman had taken the design on before he arrived, working out
what it would take and what could be measured with it, and doing sums in a
truck cab while he waited at the gate. The critical mass itself was
**[Robert Christy](kloom:e/robert-f-christy)**'s calculation, and it was remarkably good.

| Water Boiler, grams of uranium-235 to go critical | Grams |
| ------------------------------------------------- | ----- |
| Christy's first estimate, 1943                    | 600   |
| Refined with better cross-sections                | 575   |
| Measured when it went critical, 9 May 1944        | 565   |

His group's hardest problem, Feynman told Charles Weiner in 1966, was a
bomb of **uranium hydride**, where the hydrogen slows the neutrons and no
single-speed approximation will do. T-4 found ways to break the problem
into a series of one-speed problems, and, as he remembered it, to bracket
the answer tightly from above and below. The idea itself died by August
1944; the efficiency was, in Bethe's recollection, "negligible or less, as
Feynman would say."

The official history also records a "Feynman experiment", never done
itself: mix enough of the neutron absorber boron-10 through a
supercritical assembly to hold it below critical, and measure how fast its
neutrons die away. Its principle went into several experiments. The
calculations that came after the formula needed machines, and people to
run them: the next frame, on the computers and the punched cards.

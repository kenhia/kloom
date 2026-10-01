The most precise machines made in any number are built in **[Veldhoven](kloom:e/veldhoven)**, in the south of the Netherlands, by **[ASML](kloom:e/asml)**, and as of 30 September 2026 no one else makes them. They print the finest layers of the most advanced chips by **[extreme-ultraviolet lithography](kloom:e/euv-lithography)**, with light of 13.5 nanometres that nothing on Earth gives off by itself and almost every material swallows. ASML's NXE:3600D weighs about 180 tonnes and travels in three Boeing 747s. This frame is how such a machine makes its light, why it steers it with mirrors, and how it lays one layer of a chip on another to within a nanometre.

## Thirty years of doubt

The idea is Japanese. **Hiroo Kinoshita**, at the telephone company NTT, began to think about imaging with soft X-rays in 1984, and showed the first images at the Japan Society of Applied Physics in 1986. In his own account, written with Obert Wood, the audience "seemed unwilling to believe" that an image had been made by bending X-rays. A proposal from Bell Labs to the US government that year was turned down by reviewers who wrote that printing features of 0.1 micron "would never be needed" for silicon chips. **[Lawrence Livermore](kloom:e/lawrence-livermore-national-laboratory)** and Sandia took the idea up, and in 1997 American chipmakers led by Intel formed the EUV LLC to pay for the national laboratories' work. ASML began its own programme the same year, joined that consortium in 1999, and shipped its first prototypes, to imec in Belgium and to Albany in New York, in 2006.

The first EUV chips reached the shops in 2019, in Samsung's Galaxy Note10. "I once said naively that EUV would be in volume production in 2006," ASML's technology chief Jos Benschop said that year, admitting it was thirteen years late. ASML dates its hundredth shipment to December 2020 in one account and to the beginning of 2020 in another.

## Light from tin

Inside the source, a generator fires drops of molten **[tin](kloom:e/tin)** about 25 micrometres across at 70 metres a second, 50,000 of them a second; by our arithmetic they fly 1.4 millimetres apart. Each drop is struck twice by a carbon-dioxide laser built by **[Trumpf](kloom:e/trumpf)**, which **[Carl Zeiss SMT](kloom:e/carl-zeiss-smt)** calls the most powerful pulsed industrial laser in the world, at 30 kilowatts. A weak pre-pulse flattens the drop into a pancake. The main pulse turns the pancake into a plasma at nearly 220,000 °C, by Zeiss's figure, and ions of tin stripped of eight to thirteen electrons give off a narrow band of light around 13.5 nm. ASML's source reached 250 watts of usable light only after years of what Benschop called a "public beating" from customers; the NXE:3800E's source is rated at 500 watts and runs its droplets faster.

## Why mirrors

Glass absorbs this light, and so does air, so there can be no lenses and the whole light path is a vacuum. Every surface that steers the light is a mirror, and a single polished surface reflects only about one per cent of it. So each mirror is coated with about a hundred alternating layers of molybdenum and silicon, each a few nanometres thick, and the faint reflections from all the boundaries add up in step. **[Bragg's law](kloom:e/braggs-law)** sets the spacing: a pair of layers must be half a wavelength deep, so that light from each boundary travels exactly one wavelength further than light from the one above. At 13.5 nm that is about 6.8 nm a pair, by our arithmetic. Zeiss gets about 70 per cent back from each mirror, and the losses multiply:

| Light has met                      | Reflections | Left (0.70ⁿ) |
| ---------------------------------- | ----------: | -----------: |
| the collector, round the plasma    |           1 |          70% |
| two illuminator mirrors, at least  |           3 |          34% |
| the mask, itself a mirror          |           4 |          24% |
| six mirrors of the projection lens |          10 |         2.8% |

The numbers in the last column are ours. So the source must be bright, and most of its light ends as heat in mirrors that must not move.

The mirrors must also be smooth beyond anything polished before. Zeiss says that an EUV mirror blown up to the size of Germany would have no bump higher than a tenth of a millimetre; ASML, describing the same mirrors, says a millimetre. They may mean mirrors of different sizes; ASML also calls its largest a metre across and "smooth down to tens of picometers".

![Bar chart on a logarithmic scale: the smallest feature ASML's machines print, from about 1,000 nm with blue mercury light of 436 nm to 8 nm with extreme ultraviolet at a numerical aperture of 0.55](euv-features.svg)

| Light                  | Wavelength | Smallest feature |
| ---------------------- | ---------: | ---------------: |
| mercury g-line         |     436 nm |         1,000 nm |
| mercury i-line         |     365 nm |           220 nm |
| krypton fluoride       |     248 nm |            80 nm |
| argon fluoride         |     193 nm |            38 nm |
| EUV, NA 0.33           |    13.5 nm |            13 nm |
| EUV, NA 0.55 (High NA) |    13.5 nm |             8 nm |

## A nanometre between layers

Printing a fine line is half the work. A chip is built up through as many as a hundred layers, and each must land on the one beneath. That alignment is _overlay_. ASML specifies the NXE:3800E to lay a layer within 0.9 nm of one printed by another machine, and within 0.8 nm of its own earlier work; it reported 0.6 nm. To do it, ASML's stages measure the wafer's position 20,000 times a second to about 60 picometres, less than the width of a silicon atom, while the mask races the other way at up to 15 times the pull of gravity.

ASML recognised 48 EUV machines in sales in 2025. By our arithmetic from its annual report, the 44 of the 0.33 NA kind brought in about €237 million each, and the four High NA machines about €289 million each; Wikipedia's article gives about $370 million for the latter. In July 2026 ASML said it could build about 65 of the older kind a year.

The resists that catch this light are chemistry's story, and the transistors it prints are computing's. The last frame steps back to ask how far making has come, from the first knapped edge to a nanometre.

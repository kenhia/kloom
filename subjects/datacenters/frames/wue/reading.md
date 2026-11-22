**[Water usage effectiveness](kloom:e/water-usage-effectiveness)** (WUE) was proposed in March 2011 by **[The Green Grid](kloom:e/the-green-grid)**, a consortium of data center companies and equipment makers, in its white paper 35, whose contributors came from Symantec, [Microsoft](kloom:e/microsoft) and Emerson, with an editor from Intel. It is a data center's annual water use in liters divided by the energy its computing equipment uses in kilowatt-hours. As Eric Masanet of the University of California, Santa Barbara quotes it in his 2026 review of the field, the paper counted "cooling tower evaporation, blowdown, and drift," so its "usage" was closer to water taken in than to water consumed. It also defined a _source_ WUE, adding the water used to generate the site's electricity. The **[International Organization for Standardization](kloom:e/international-organization-for-standardization)**'s standard ISO/IEC 30134-9, published in March 2022, sorts site WUE into two categories: water taken in, and water taken in minus what leaves for reuse elsewhere, which is close to consumption.

## What companies report

Four of the largest operators each publish a WUE, each its own measurement of its own buildings, and no two define it alike.

| Operator                              | Year    | WUE, L/kWh | What the numerator counts, in its own words                                           |
| ------------------------------------- | ------- | ---------: | ------------------------------------------------------------------------------------- |
| Amazon Web Services                   | 2025    |       0.12 | "liters of water withdrawn per kilowatt-hour (kWh) of IT load"                        |
| Meta                                  | 2025    |       0.14 | "total water consumption of the data center," for cooling and humidifying             |
| Microsoft                             | FY 2025 |       0.27 | "datacenter water use (for cooling and humidification)," withdrawn or consumed unsaid |
| Google                                | 2024    |       1.15 | freshwater consumed, ISO category 2, at the sites serving its language models         |
| LBNL model, US hyperscale             | 2023    |       0.32 | water consumed on site, simulated                                                     |
| LBNL model, US midsize and colocation | 2023    |       0.67 | water consumed on site, simulated                                                     |

**[Amazon](kloom:e/amazon-company)** says its figure is about a seventh of an average data center's. **[Meta](kloom:e/meta-platforms)** reported a fall of 26% in a year. Microsoft reported 25% below its 2022 baseline. **[Google](kloom:e/google)** gives its figure not in its environmental report but in an August 2025 paper on the energy of its AI prompts. By our arithmetic from that report, its data centers consumed about 0.94 liters per kilowatt-hour of all their electricity in 2025. **[Lawrence Berkeley National Laboratory](kloom:e/lawrence-berkeley-national-laboratory)** models the national average at just over 0.36 in 2023, rising to between 0.45 and 0.48 by 2028 as more servers move into large buildings and liquid cooling.

The table cannot rank the companies. Google consumes about four-fifths of what it withdraws, so a withdrawal and a consumption WUE differ at the same site; climates differ; and none of the four reports says how its sites divide among cooling designs. The industry's case is that the low numbers are real engineering: Amazon says it uses evaporative cooling for "less than 10% of the year" where weather permits, and no water for cooling in some of its most water-stressed regions. Critics' case is that a ratio says nothing of the total: Google reported the same ratio for 2023 and 2024 while its water consumption rose 28% in 2024, and 34% more in 2025.

## What the ratio leaves out

WUE is per kilowatt-hour, so it says nothing about how much water a site uses, or from where. A liter of reclaimed wastewater and a liter of groundwater from a depleted aquifer count the same. Amazon and Meta screen their sites with the **[World Resources Institute](kloom:e/world-resources-institute)**'s Aqueduct atlas of water stress, and Amazon reports 22% of its 2025 withdrawals in regions of high or extremely high stress; Google, by its own framework, puts 13% of its freshwater withdrawals at high risk. Nor does the ratio show timing: a tower evaporates most in the hottest weather, and the stress a liter causes varies by season as well as by place.

And a site can lower its WUE by spending electricity, which uses water at a power plant. The Berkeley laboratory warns that its own discussion "does not imply low site WUEs are necessarily good." Its simulations put each cooling design's median [power usage effectiveness](kloom:e/power-usage-effectiveness) beside its WUE; the plate draws them, as read from its figure 4.4.

| Cooling system, by Berkeley's size class  | Median PUE | Median WUE, L/kWh |
| ----------------------------------------- | ---------: | ----------------: |
| Midsize, air-cooled chillers              |       1.83 |              ≈0.0 |
| Midsize, water-cooled chillers and towers |       1.52 |               2.9 |
| Midsize, airside economizer, towers       |       1.45 |               1.3 |
| Large, waterside economizer, towers       |       1.12 |               2.2 |
| Large, outdoor air with adiabatic assist  |       1.14 |               0.4 |
| Large, liquid-cooled servers, dry coolers |       1.09 |              ≈0.0 |

Among midsize designs, evaporation buys efficiency. Among large ones the medians differ by a tenth at most, and the newest designs, liquid-cooled chips with warm-water loops and dry coolers, are modeled to escape the trade in favorable climates; the laboratory notes that its simulations assume equipment runs as designed, which "is rarely the case." _Zero-water cooling_ follows Microsoft's attempt.

## Better measures

Masanet's review proposes fourteen best practices for anyone reporting data center water, beginning with stating whether a number is a withdrawal, an input or a consumption, and which category of WUE it is. A 2026 paper by Zahidur Talukder and colleagues weights each liter by its county's water stress, month by month. Neither is yet a standard. What is not known is how the companies' figures compare on one definition, since each company measures its own and none breaks its figure down by cooling system. _The water behind the electricity_ adds what a site's WUE leaves out at the power plant.

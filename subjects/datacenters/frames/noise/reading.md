A data center's sound comes from the machines that keep it running: fans that push air through the racks and out through the roof, chillers and cooling towers that throw off the heat, transformers at its substation, and, for a few minutes a month, diesel generators under test. What neighbors describe is that it never stops: a hum or drone, day and night, that carries through walls. In 2024 the legislative auditors of **[Virginia](kloom:e/virginia)**, the Joint Legislative Audit and Review Commission (JLARC), counted at least 15 operating data center sites in the state, about one in ten, whose noise nearby residents regarded as a problem, and found that most draw no complaints. Noise is a small share of what opponents name (9% of them in Gallup's open answers, about one in ten in Heatmap's poll), though Heatmap Pro says its own project data shows noise among the biggest reasons projects are canceled, a claim made from data it has not published.

## Why a meter misses the hum

Sound is measured in **[decibels](kloom:e/decibel)**, a logarithmic scale: ten more decibels is ten times the sound energy. From a small source in open air, the level falls by about 6 decibels for each doubling of distance (by our arithmetic from the inverse-square law), which is what a setback buys. Most noise rules use **[A-weighting](kloom:e/a-weighting)**, a filter dating from 1930s measurements of how the ear hears quiet pure tones. It discounts low pitches, where the ear is less sensitive. Low pitches also pass through walls. Both effects favor the hum:

![Grouped bar chart by octave band from 31.5 to 1,000 hertz: how many decibels A-weighting subtracts, falling from 39 to 0, beside how many a wood-frame house removes, rising from 11 to 25](weighting.svg)

| Octave band | A-weighting subtracts | A wood-frame house removes (windows open 2 inches) |
| ----------- | --------------------: | -------------------------------------------------: |
| 31.5 Hz     |                 39 dB |                                              11 dB |
| 63 Hz       |                 26 dB |                                              15 dB |
| 125 Hz      |                 16 dB |                                              19 dB |
| 250 Hz      |                  9 dB |                                              21 dB |
| 1,000 Hz    |                  0 dB |                                              25 dB |

The house's figures are from Nelson Acoustics, the consultant that **[Prince William County](kloom:e/prince-william-county-virginia)** hired; the weights are the standard's, rounded. So a sound can read modestly outdoors in dBA and still be what a family hears indoors at night. C-weighting, which discounts low pitches far less, catches more of it. JLARC found that the complaints it reviewed concerned sound of an estimated 40 to 59 dBA, mostly below the 55- or 60-decibel limits that Loudoun, Prince William and **[Fairfax](kloom:e/fairfax-county-virginia)** counties set for homes.

## Great Oak

The best-recorded case is Great Oak, 291 homes near Manassas, about 600 feet from a four-building **[Amazon](kloom:e/amazon-company)** campus. On May 16, 2022, John and Gloria Biess called the county police about a roar and a screech; their own meter later read up to 65 decibels at night, and the county's 55-decibel night limit then exempted cooling equipment. Residents described lost sleep, migraines and decks they no longer used; one family moved a baby's crib to the basement. That is testimony of experience, not a measurement of cause.

Residents say Amazon at first called its cooling design proprietary, and that the shrouds it wrapped around its rooftop exhaust fans gained about 1 decibel. By August 18, 2023 it had replaced the fans and blades, raised all 424 exhaust stacks by three feet and slowed the fan controls; residents' and Amazon's measurements both put the drop at about 10 decibels, to around 50. "Residents confirm that the steps we're taking at the facility are already having a positive impact," a spokesman said. Acoustic baffles behind the air-intake louvers followed in October 2024. Residents, whose 1,600 readings were taken with a consumer meter and a phone app, reported tones as low as 70 hertz still coming through their walls. The county's consultant found the data center hard to separate from traffic; in July 2025 county staff said that after almost a year of testing they had isolated the noise, attributed it to Amazon's campus, and found it above the levels then proposed.

## The rules

Fairfax County's zoning amendment of September 2024 keeps a new data center building 200 feet from homes and its outdoor equipment, generators included, 300 feet away unless the building stands between, requires that equipment to be enclosed, and asks for noise studies before approval and after construction. In Prince William, a residents' advisory group worked with Nelson Acoustics on octave-band limits equal to about 43 dBA at night, 12 decibels stricter than the old rule. In October 2025 the board disbanded the group and adopted a version written by Supervisor Kenny Boddye, with C-weighted limits for "steady tonal sound," in force from May 1, 2026. _E&E News_ reported it raised the limits and dropped the octave-band method. Boddye said the earlier draft "would have chilled economic growth and been nearly impossible to enforce."

## Health, and the industry's answer

The **[World Health Organization](kloom:e/world-health-organization)**'s 2018 guidelines set night limits for roads, railways and aircraft, but none for industrial noise, saying the sources vary too much, and they call for research on ventilation and similar equipment. A 2016 review of low-frequency noise found seven studies, with associations with annoyance, poor sleep and headache, and "very limited" evidence on chronic illness.

Operators answer that quiet can be designed in. Amazon said it is helping suppliers redesign products "to significantly reduce sound levels," and companies told JLARC they model sound before building because fixing it afterward is costly. Whether liquid cooling, which needs fewer fans, makes campuses quieter is not yet measured in any study we found. Whether the campus meets the ordinance now in force has not been reported. Nor is the combined hum of many campuses measured: Great Oak's residents count about two dozen data center buildings operating, building or planned within a mile of their homes. The loudest thing a campus does, it does rarely, when its _Backup diesel generators_ start.

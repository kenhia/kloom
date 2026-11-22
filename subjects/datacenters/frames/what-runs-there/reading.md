A **[data center](kloom:e/data-center)** does not do one thing. The same hall may answer a web search, deliver mail, draw a map, stream a film, clear a card payment, hold a hospital's records, run a tax agency's site and train or run an AI model. No public statistic says how much electricity goes to each service, because operators do not report it that way. What can be estimated is the machinery, and who owns the building it sits in. As of November 2026 the newest estimates are these.

## The work, by machine

**[Lawrence Berkeley National Laboratory](kloom:e/lawrence-berkeley-national-laboratory)**'s 2024 report to Congress, written for the Department of Energy, models American data centers from the bottom up: how many servers, drives and switches were shipped, and how hard each is likely run. Its figures are estimates, not meter readings.

| United States, 2023 (modeled)             | Electricity, TWh                        |
| ----------------------------------------- | --------------------------------------- |
| Conventional servers                      | nearly 60                               |
| GPU-accelerated servers for AI            | more than 40 (under 2 in 2017)          |
| Storage                                   | 16                                      |
| Cooling, power conversion and other plant | about 30% of the total                  |
| All data centers                          | 176 (4.4% of the country's electricity) |

Of the AI servers' electricity, nearly 60% went to running models for users (inference) rather than training them. Worldwide, the **[International Energy Agency](kloom:e/international-energy-agency)** estimated data centers' use at about 415 terawatt-hours in 2024, about 1.5% of the world's electricity. Its April 2026 update put 2025 at 485, up 17%, and projects about 950 by 2030 in its central case, with the consumption of AI-focused data centers tripling. Both are model estimates; the 2030 figure is a projection.

The Berkeley total leaves out **[Bitcoin](kloom:e/bitcoin)** mining, which runs on its own special chips in single-purpose buildings, and treats it separately. The Energy Information Administration's preliminary estimate of February 2024 put cryptocurrency mining at 0.6% to 2.3% of American electricity, a range as wide as it is because miners are hard to find among millions of customers.

## Who owns the buildings

The report sorts buildings by who runs them: _internal_ data centers, run by an organization for itself; _colocation_ buildings, whose owners lease space, power and cooling to tenants' machines; and _hyperscale_ campuses, built by companies running internet services at very large scale. Amazon, Microsoft and Google own more than half of the hyperscale buildings, by a Synergy Research count the report cites.

| Year | Servers in hyperscale and colocation buildings (modeled) |
| ---- | -------------------------------------------------------: |
| 2014 |                                                      20% |
| 2020 |                                                      57% |
| 2023 |                                                      74% |
| 2028 |                                          85% (projected) |

Internal data centers held over 60% of server electricity in 2014 and about 10% in 2023. Much of the work moved into rented capacity, **[cloud computing](kloom:e/cloud-computing)**, whose rise _The cloud_ tells.

## The case, and the reply

Supporters argue that this work is worth far more than it costs, much of it to people who pay nothing. In a study published in 2019, **[Erik Brynjolfsson](kloom:e/erik-brynjolfsson)**, Avinash Collis and Felix Eggers collected about 65,000 answers from a representative online sample of Americans, each asked once how much they would have to be paid to give up a whole category of service for a year. The answers are what people said, not what they were paid, and the authors call them coarse; where they did pay people to go without Facebook, the median asked about $48 a month. The study was funded by MIT's Initiative on the Digital Economy, through a grant from the Markle Foundation.

| Category, 2017 survey | Median payment asked to give it up for a year |
| --------------------- | --------------------------------------------: |
| Search engines        |                                       $17,530 |
| Email                 |                                        $8,414 |
| Digital maps          |                                        $3,648 |
| Video streaming       |                                        $1,173 |

The AI side of the case is demand: the IEA reported in 2026 that the major model providers claimed three times as many active users, and five times the revenue, as a year before.

Critics answer that the services valued in 2017 are not what is driving the new building. The growth in the Berkeley figures is in AI servers, and whether that work is worth its power, water and land is the contested part: 14% of the opponents Gallup asked in 2026 named a dislike or distrust of AI itself. _The race for compute_ and _Is it a bubble?_ take that up.

## Streaming, and what is not measured

Video is the clearest case of a number that traveled. In July 2019 **[The Shift Project](kloom:e/the-shift-project)**, a French think tank that campaigns for "digital sobriety", estimated that online video produced more than 300 million tonnes of carbon dioxide in 2018. Media outlets then repeated a figure drawn from its numbers: half an hour of **[Netflix](kloom:e/netflix)** emitted 1.6 kilograms, "the same as driving almost 4 miles." In June 2020 the Shift Project corrected a conversion of bits to bytes, cutting its figure eightfold, to a level close to a peer-reviewed study of 2014. George Kamiya, an analyst at the IEA, rebuilt the estimate from published energy-intensity data, drawing partly on Netflix's own reported electricity use, 0.45 terawatt-hours in 2019.

![Bar chart on a logarithmic scale of grams of carbon dioxide per half hour of Netflix: 1,600 as reported from The Shift Project in 2019, 200 as it corrected the figure in 2020, and 18 in the IEA's estimate](streaming.svg)

| Estimate                              | Grams of CO2 per half hour |
| ------------------------------------- | -------------------------: |
| The Shift Project, as reported (2019) |                      1,600 |
| The Shift Project, corrected (2020)   |                        200 |
| IEA, Kamiya (updated December 2020)   |                         18 |

Kamiya's figure is also a model, but one built from measured energy intensities, and it found the data center only about 5% of streaming's electricity: the television or phone took 72% and the networks 23%. Kamiya still warned that slowing efficiency gains, rebound effects and new demands such as AI "raise increasing concerns" for the coming decades.

No company publishes its electricity by service, so how much goes to search, to video or to AI is inferred, not counted. The EIA's survey of crypto miners was stopped, and the AI share depends on how many chips are installed and how hard they run. The next frame asks whether efficiency can carry the growth.

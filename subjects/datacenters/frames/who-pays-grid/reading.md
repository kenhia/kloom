A large data center campus needs a substation, often new transmission lines, and enough power plants promised for the hottest afternoon of the year. Someone pays for each. In Gallup's 2026 poll, 15% of the people who opposed a data center nearby named their utility bill. What they will pay is settled in three places: a state commission's rate case, a regional formula for transmission and, across much of the East, a capacity auction. Each is public, technical and contested, and this frame follows all three as of November 2026.

## How the costs are shared

| Cost                         | Who sets it                                             | How it is shared                                                      |
| ---------------------------- | ------------------------------------------------------- | --------------------------------------------------------------------- |
| Local wires and substations  | the state utility commission, in a rate case            | by customer class, from the utility's cost-of-service study           |
| High-voltage transmission    | the Federal Energy Regulatory Commission and the region | across a utility's zone or the whole region, by each zone's peak load |
| Capacity (plants on call)    | PJM's auction, in thirteen states and Washington, D.C.  | to every utility's customers, by their share of the peak              |
| A new large customer's lines | the commission, in a contract or tariff                 | to that customer, through a contribution or a minimum bill            |

In a rate case the utility adds up its costs and a return on what it has invested, its _revenue requirement_, and proposes how to divide it among classes: residential, commercial, industrial. Regulators call the principle _cost causation_: whoever causes a cost should pay it. The plate draws that split. The argument is over the dividing, because many costs are shared and the studies that apportion them rest on choices of method.

## The capacity auction

**[PJM Interconnection](kloom:e/pjm-interconnection)** runs the grid and wholesale market for 67 million people. Each year it buys, about three years ahead, promises from power plants to be available at the peak. Its auction results are measured: they are what the market cleared.

![Bar chart of the price at which PJM's capacity auction cleared, in dollars per megawatt-day: 28.92 for 2024/25, 269.92 for 2025/26, then at the price cap, 329.17 for 2026/27, 333.44 for 2027/28 and 325.00 for 2028/29](capacity-price.svg)

| Delivery year | Price, $ per MW-day | Total, $ billion |
| ------------- | ------------------: | ---------------: |
| 2024/25       |               28.92 |              2.2 |
| 2025/26       |              269.92 |             14.7 |
| 2026/27       |        329.17 (cap) |             16.1 |
| 2027/28       |        333.44 (cap) |             16.4 |
| 2028/29       |        325.00 (cap) |             16.4 |

The last three cleared at a cap PJM set with the region's governors and [FERC](kloom:e/federal-energy-regulatory-commission); without it, PJM's simulation puts 2028/29 at $554.72. The last two bought less than PJM's reliability requirement, 6.8 gigawatts short in 2028/29. PJM's independent market monitor, Monitoring Analytics, attributes much of the rise to data centers: in October 2025 it said that "data center load growth is the primary reason" for the market's conditions, and in July 2026 that data centers accounted for $6.3 billion of the latest auction's $16.4 billion. Those figures are its model of what prices would have been without that load. PJM's own account is that "demand for electricity continues to grow faster than electricity supply." A study the Data Center Coalition paid for, by the consultancy E3, calls data center load one of several causes, "alongside market design changes and power plant retirements."

## The case that households are paying

Ari Peskoe and Eliza Martin of **[Harvard Law School](kloom:e/harvard-law-school)**'s Electricity Law Initiative reviewed nearly 50 regulatory proceedings in 2025 and wrote that they were "skeptical of utility claims that data center energy costs are isolated from other consumers' bills," pointing to confidential contracts and to transmission costs that fall between federal and state rules. In **[Virginia](kloom:e/virginia)**, where many commenters told the [State Corporation Commission](kloom:e/state-corporation-commission-virginia) that a rate increase was meant "primarily to subsidize data centers," the commission's November 2025 order answered that inflation had raised the utility's costs too. But it also found, from **[Dominion Energy](kloom:e/dominion-energy)**'s own cost-of-service study, that the customers who will form its new class for loads of 25 megawatts or more had earned the utility a 6.28% return, the lowest of any class but outdoor lighting, against 20.75% for the large customers left in their old class. A low return is not a loss, and the figure turns on how the study divides shared plant; the commission ordered Dominion to develop other methods. In **[Ohio](kloom:e/ohio)**, the state's manufacturers' association, a trade group of large customers, argues that "paper demand is driving real costs."

## The case that they are not, or need not be

Virginia's legislative audit commission, with E3 as its consultant, found in 2024 that "data centers are currently paying their full cost of service." It also projected that growth could add $14 to $37 a month to a typical Dominion household's bill by 2040, in today's dollars. **[Lawrence Berkeley National Laboratory](kloom:e/lawrence-berkeley-national-laboratory)** and the Brattle Group, for the Department of Energy, found that from 2019 to 2025 the states whose demand grew most generally saw real prices fall, as fixed costs were spread over more sales, though their own PJM case study shows the reverse where supply is tight. E3's study for the industry, which the coalition reviewed before publication, found "no evidence that data centers have been historically subsidized by other customers." In March 2026 Google, Meta, Microsoft and other companies pledged at the White House to protect consumers from price increases their data centers cause. The market monitor's president, Joseph Bowring, said that under PJM's current rules the pledge cannot be met.

## Large-load tariffs

| Utility, regulator            | Decided                      | Who                               | Terms                                                                                              |
| ----------------------------- | ---------------------------- | --------------------------------- | -------------------------------------------------------------------------------------------------- |
| AEP Ohio, PUCO                | July 9, 2025                 | new data centers of 25 MW or more | a minimum bill on up to 85% of contracted capacity, by a schedule; a ramp of up to 4 years, then 8 |
| Dominion, Virginia SCC (GS-5) | November 25, 2025; from 2027 | 25 MW or more, 75% load factor    | 14-year contracts; minimum 85% for wires, 60% for generation; an exit fee                          |

The **[Public Utilities Commission of Ohio](kloom:e/public-utilities-commission-of-ohio)** adopted a settlement among **[American Electric Power](kloom:e/american-electric-power)**, its staff and the state's consumer counsel; Microsoft, Amazon, Google and the Data Center Coalition had backed a rival one. E3 counts 30 such tariffs adopted in 2025 and 2026 alone.

## What is not known

No tariff has run its course, and no study yet separates cause from correlation. PJM's backstop auction for the missing capacity, which FERC only partly approved in September 2026, is now planned for March 2027, and the next capacity auction, in December 2026, is capped again. Next, where the new power comes from: _Gas plants for data centers_.

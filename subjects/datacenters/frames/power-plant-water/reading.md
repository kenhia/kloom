The water a data center evaporates on its own roof is the part people can photograph. Most of the water tied to its electricity is consumed somewhere else: at the power plants that make it, in their cooling, and, by one way of counting, from the reservoirs behind hydroelectric dams. **[Lawrence Berkeley National Laboratory](kloom:e/lawrence-berkeley-national-laboratory)** estimated that indirect water at nearly 800 billion liters for American data centers in 2023, against about 66 billion on their own sites. It is the largest water number in the argument, and the one that depends most on how it is counted.

## Why power plants use water

A **[thermal power station](kloom:e/thermal-power-station)**, burning coal or gas or splitting uranium, boils water into steam to turn a turbine, and the spent steam must be condensed before it can be boiled again. As **[Carnot](kloom:e/nicolas-leonard-sadi-carnot)** showed in 1824, every heat engine must give heat to something colder, and at most plants that is water. A _once-through_ plant pumps river or lake water through its condenser and returns nearly all of it, warmer. A plant with a **[cooling tower](kloom:e/cooling-tower)** recirculates its water and evaporates part of it, so it withdraws far less and consumes far more of what it withdraws.

The **[United States Geological Survey](kloom:e/united-states-geological-survey)** now models this water use plant by plant. Its latest national assessment, published in 2025, puts freshwater withdrawals for thermoelectric power at an average of 82,656 million gallons a day over the water years 2010 to 2020, about 37% of the fresh water withdrawn for irrigation, public supply and power together, by our arithmetic. Consumption was 2,904 million gallons a day, about 4% of the withdrawal. Both have fallen since 2008, as coal plants closed and others moved to towers. The often-quoted "about 40%" is the survey's 2015 inventory: thermoelectric power then took 41% of all withdrawals, salt water included, and 34% of fresh water.

## Water per megawatt-hour

In 2012 Jordan Macknick and colleagues at the **[National Renewable Energy Laboratory](kloom:e/national-laboratory-of-the-rockies)**, renamed the **National Laboratory of the Rockies** in December 2025, gathered published estimates of how much water each kind of plant consumes. The chart gives their medians: engineering estimates from the literature, which the authors did not audit, not meter readings.

![Bar chart of median water consumed per megawatt-hour: wind 0 gallons, photovoltaics 1, gas combined cycle with dry cooling 2, gas combined cycle once-through 100, gas combined cycle with a tower 205, coal once-through 250, nuclear once-through 269, nuclear with a tower 672, coal with a tower 687](consumption.svg)

| Technology and cooling          | Consumed, gal/MWh (median) | Withdrawn, gal/MWh (median) |
| ------------------------------- | -------------------------: | --------------------------: |
| Wind                            |                          0 |                           0 |
| Utility-scale photovoltaics     |                          1 |                           1 |
| Gas combined cycle, dry cooling |                          2 |                           2 |
| Gas combined cycle, tower       |                        205 |                         255 |
| Nuclear, once-through           |                        269 |                      44,350 |
| Nuclear, tower                  |                        672 |                       1,101 |
| Coal, tower                     |                        687 |                       1,005 |
| Hydropower, reservoir           |                      4,491 |                  not listed |

**[Hydroelectricity](kloom:e/hydroelectricity)** is the hard case. Its median counts all of a reservoir's evaporation against the power, though reservoirs also supply water and control floods. The paper calls that allocation complicated and leaves hydropower off its figures. Whether to count it is a choice, and it moves every total that follows.

## A data center's share

The laboratory's 2024 report traced electricity from power plants to data centers' counties, through the grid's balancing authorities, using plant data from the **[Energy Information Administration](kloom:e/energy-information-administration)**. It found 4.52 liters consumed per kilowatt-hour that data centers used in 2023, against 4.35 for American electricity overall. Its method follows work by Md Abu Bakar Siddik and colleagues, whose 2021 paper assigned all of a reservoir's evaporation to hydropower and found the water behind each kilowatt-hour a data center used in 2018, on site and at the plant, ranging from 1.8 to 105.9 liters by location. Shaolei Ren's group at UC Riverside reads the laboratory's figure as including reservoir evaporation too, and a national average above even a coal plant with a tower, 2.6 liters by our arithmetic, implies that much of it is.

Read one way, as Ren's group argues, the on-site figures that companies report leave out about nine-tenths of the water, by our arithmetic, and should count it as their own. Read the other way, as most companies' reports do by counting only on-site water, this water is the grid's: any user of the same electricity carries it, and per kilowatt-hour data centers carry about the national average. The Riverside group replies that operators choose where and when to run their computing, and so choose that water too. The report itself calls site and source water together "the true water cost of data centers," and adds that the calculation is "highly dependent on the source of electricity." It also ignores companies' power purchase agreements, for lack of data. Meta reports its electricity's water too: 3.7 liters per kilowatt-hour for 2023, by the Riverside group's arithmetic from Meta's own figures.

## The trade at the wall

Cooling without evaporation saves water on site and uses more electricity, so it moves water to the power plant. The table works the trade by our arithmetic for two pairs of cooling systems the laboratory simulated (medians read off its figure 4.4): on-site water plus PUE times the grid's water, for stated grids.

| Liters per kWh of computing             | Midsize, towers (PUE 1.52, 2.9 L on site) | Midsize, air-cooled (1.83, 0.06 L) | Large, towers (1.12, 2.2 L) | Large, dry cooler (1.20, 0.25 L) |
| --------------------------------------- | ----------------------------------------: | ---------------------------------: | --------------------------: | -------------------------------: |
| Wind and solar, about 0 L/kWh           |                                       2.9 |                                0.1 |                         2.2 |                              0.2 |
| Gas combined cycle with towers, 0.78    |                                       4.1 |                                1.5 |                         3.1 |                              1.2 |
| Coal with towers, 2.6                   |                                       6.9 |                                4.8 |                         5.1 |                              3.4 |
| Data centers' U.S. average, 4.52        |                                       9.8 |                                8.3 |                         7.3 |                              5.7 |
| Washington State, hydropower-heavy, 9.5 |                                      17.3 |                               17.4 |                        12.8 |                             11.7 |

The dry design comes out ahead until the grid's water passes about 9 liters per kilowatt-hour for the midsize pair and about 24 for the large one: on most American grids, not on a reservoir-heavy one. On a wind-and-solar grid, nearly all of a data center's water is its own; on a coal grid, most is at the plant. The table leaves out two things: on a fossil grid the dry design's extra electricity also means more emissions, which _Counting a data center's carbon_ weighs, and the water saved on site comes from a local utility, while the power plant's may be in another basin.

No one has measured any data center's source water: the figures rest on grid averages, simulated cooling and a contested treatment of reservoirs. _The water in a chatbot answer_ shows how the same choices shape the smallest number in the argument.

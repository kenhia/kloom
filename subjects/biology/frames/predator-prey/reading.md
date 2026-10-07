During the First World War, fishing in the northern **[Adriatic](kloom:e/adriatic-sea)** almost ceased. A young Italian zoologist, **[Umberto D'Ancona](kloom:e/umberto-dancona)**, who had fought as an artillery officer, afterwards gathered the catch records of the region's fish markets, among them the market at Fiume, the city now called **[Rijeka](kloom:e/rijeka)**. He noticed that in the war years the voracious fish, the sharks and rays that feed on other fish, made up a larger share of the catch than before or after. Why should a pause in fishing favor the hunters over the hunted?

D'Ancona married Luisa Volterra in 1926, and put the question to her father, **[Vito Volterra](kloom:e/vito-volterra)**, a mathematician of 66 who had turned after the war to biology. Volterra's answer appeared in Italian that year, and in English in _Nature_ in October 1926.

![A bar chart of sharks and rays as a percentage of fish landed at Fiume: 7.4 in 1914, then 5.8, 10.5, 13.8 and 18.7 in 1915 to 1918, highlighted, then 8.2, 6.9, 5.8, 7.5 and 6.3 from 1919 to 1923](fiume-sharks.svg)

The chart is our arithmetic from the Fiume market's records, as D'Ancona published them and as Italian oceanographers digitized them in 2017: sharks and rays as a share, by weight, of all the fish landed.

| Year | Sharks and rays, % of fish landed |
| ---- | --------------------------------- |
| 1914 | 7.4                               |
| 1915 | 5.8                               |
| 1916 | 10.5                              |
| 1917 | 13.8                              |
| 1918 | 18.7                              |
| 1919 | 8.2                               |
| 1920 | 6.9                               |
| 1921 | 5.8                               |
| 1922 | 7.5                               |
| 1923 | 6.3                               |

## Two equations

Volterra wrote down the simplest case: one species with plenty of food, which would multiply without limit if left alone, and a second that eats it and would starve without it. Call the prey _x_ and the predators _y_:

| Equation                 | Term  | What it says                                                      |
| ------------------------ | ----- | ----------------------------------------------------------------- |
| d*x*/d*t* = α*x* − β*xy* | α*x*  | Prey left alone grow in proportion to their number                |
|                          | β*xy* | Prey are eaten in proportion to how often prey and predators meet |
| d*y*/d*t* = δ*xy* − γ*y* | δ*xy* | Predators grow in proportion to the prey they catch               |
|                          | γ*y*  | Predators die at a steady rate                                    |

The first term is the geometrical increase of **[Thomas Robert Malthus](kloom:e/thomas-robert-malthus)**; the rest is what stops it. The integrals, Volterra wrote, "reveal the fact that the numbers of individuals of the two species are periodic functions of the time, with equal periods but with different phases." Plotted against each other they trace closed curves, which the plate draws. His third law answered D'Ancona: fishing both species evenly raises the average number of prey and lowers the average of predators, so stopping it does the reverse. "A complete closure of the fishery," he wrote, "was a form of 'protection' under which the voracious fishes were much the better."

A worked run shows the cycle. The numbers are invented: α = 1 a year, β = 0.1, γ = 1 and δ = 0.025, starting from 40 prey and 5 predators. Stepping the equations forward by computer gives, by our arithmetic:

| Year      | 0   | 1   | 2   | 3   | 4   | 5   | 6   | 7   |
| --------- | --- | --- | --- | --- | --- | --- | --- | --- |
| Prey      | 40  | 63  | 66  | 35  | 21  | 22  | 32  | 51  |
| Predators | 5.0 | 6.6 | 13  | 17  | 12  | 7.5 | 5.3 | 5.4 |

The prey peak first; the predators, fed, peak about a year later; the prey crash, then the predators, and after about six and a half years the system is back where it began. The averages over a cycle are fixed by the other species' constants: 40 prey (γ/δ) and 10 predators (α/β).

## Lotka got there first

In a letter to _Nature_ on 1 January 1927, **[Alfred J. Lotka](kloom:e/alfred-j-lotka)**, a statistician at the Metropolitan Life Insurance Company in New York, pointed out that the theory was already in his _Elements of Physical Biology_ of 1925, with the same closed curves on page 90 and the same formula for the period. Lotka had reached them from chemistry, and from insects: a host and a parasite that lays one egg in each host it kills. Volterra replied in the same issue: "In this I recognize his priority, and am sorry not to have known his work." He added that Sir **[Ronald Ross](kloom:e/ronald-ross)**'s equations for malaria came earlier still. They are now the **[Lotka–Volterra equations](kloom:e/lotka-volterra-equations)**. Volterra was one of only twelve of Italy's 1,250 professors who refused the Fascist oath of loyalty in 1931, and lost his chair.

## Hares, lynx and the jars

The best-known test came from fur. The **[Hudson's Bay Company](kloom:e/hudsons-bay-company)** kept counts of the pelts its posts bought, and in 1942 the Oxford ecologist **[Charles Elton](kloom:e/charles-sutherland-elton)** and Mary Nicholson drew from them a cycle of **[Canada lynx](kloom:e/canada-lynx)** returns averaging 9.6 years, rising and falling a little after the **[snowshoe hare](kloom:e/snowshoe-hare)** it eats. In 1831 a company manager in northern Ontario had reported the Ojibwe starving for want of "rabbits." It became the textbook predator–prey cycle. It is more tangled. On Anticosti Island, which has no lynx, the hares still cycle, other predators taking its place. At Kluane in the Yukon, Charles Krebs and colleagues fenced out predators and fed hares on square-kilometer plots for eight years: keeping predators out doubled hare numbers at the peak and decline, food tripled them, and both together raised them elevenfold. "Lotka and Volterra were partly correct," Krebs and his colleagues concluded in 2001, but the cycle "can be understood only by analyzing three trophic levels rather than two."

In Moscow, the young **[Georgy Gause](kloom:e/georgy-gause)** tested the equations in glassware: two yeasts grown together in 1932, then two species of **[_Paramecium_](kloom:e/paramecium)**, _P. aurelia_ and _P. caudatum_. Each grew well alone; on one food together, _P. aurelia_ drove out _P. caudatum_. The result is remembered as the **[competitive exclusion principle](kloom:e/competitive-exclusion-principle)**, "one niche, one species," though Gause never stated it as a law, and the naturalist Joseph Grinnell had said as much from the field in 1904. With the predatory ciliate _Didinium_ hunting _Paramecium_, Gause got cycles like Volterra's only by imitating migration, adding animals from outside. In 1976 the ecologist Robert May showed that even one species' numbers, stepped from one generation to the next, can turn chaotic. Next comes Elton's own picture of who eats whom.

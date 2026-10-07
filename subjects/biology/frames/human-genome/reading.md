On the morning of 26 June 2000, in the East Room of the White House, President **[Bill Clinton](kloom:e/bill-clinton)** stood between two rivals. **[Francis Collins](kloom:e/francis-collins)** led the public **[Human Genome Project](kloom:e/human-genome-project)**; **[J. Craig Venter](kloom:e/j-craig-venter)** led **[Celera Genomics](kloom:e/celera-corporation)**, a company that had set out to beat it. Each announced a draft of the same thing, the order of the three billion letters of human **[DNA](kloom:e/dna)**, and Clinton, with Prime Minister Tony Blair joining by satellite from London, gave the day its line: "Today, we are learning the language in which God created life." The two drafts were published in February 2001, the public one in _Nature_ and Celera's in _Science_.

## Three billion letters

The project began as an argument over whether it was worth doing. In May 1985 **[Robert Sinsheimer](kloom:e/robert-l-sinsheimer)**, then chancellor of the University of California, Santa Cruz, gathered scientists there to discuss sequencing the whole human genome; in 1986 Charles DeLisi of the **[US Department of Energy](kloom:e/united-states-department-of-energy)** held a workshop at Santa Fe, and **[Renato Dulbecco](kloom:e/renato-dulbecco)** argued in _Science_ that cancer research needed the sequence. It began formally in 1990, run by the Department of Energy and the **[National Institutes of Health](kloom:e/national-institutes-of-health)**, with **[James Watson](kloom:e/james-watson)** heading the NIH's part until Collins succeeded him in 1993. The projected cost was $3 billion over fifteen years. The Wellcome Trust, a British charity, joined in, paying for the Sanger Centre near Cambridge, one of the largest sequencing centers, and in the end 20 groups in six countries took part. Meeting in Bermuda in 1996, the centers agreed to put every stretch they sequenced into a public database within 24 hours.

## Reading in pieces

The sequencing machines of the 1990s, which used Sanger's method, read only a few hundred to a thousand letters at a time. So DNA was broken into fragments, each fragment read, and the reads put back together by their overlaps, as in this toy example of our own invention:

```
read 1   GATTACAGTC
read 2       ACAGTCCTGA
read 3           TCCTGAAGGC
joined   GATTACAGTCCTGAAGGC
```

Each read ends with letters that begin the next, so they can be laid end to end. The trouble is that more than half of the human genome is repeated sequence; a repeat longer than a read can sit in many places, and the reads cannot say which. The plate shows the two answers the rivals chose:

| Strategy                                             | How it worked                                                                                                                                                                             |
| ---------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Hierarchical, or clone-by-clone (the public project) | DNA cut into pieces of 100,000 to 200,000 letters, each grown in bacteria as a bacterial artificial chromosome; the pieces mapped; then each piece shotgunned and assembled on its own    |
| Whole-genome shotgun (Celera)                        | The whole genome broken at random into small fragments, each fragment read from both ends, and everything assembled at once by computer, the pairs of ends holding distant reads in place |

The public consortium gave four reasons for the slower way: a misassembly would stay local, each **[bacterial artificial chromosome](kloom:e/bacterial-artificial-chromosome)** came from a single copy of a chromosome, gaps could be targeted, and the work divided neatly among centers. Celera began sequencing on 8 September 1999 and used 27,271,853 reads from five people, covering the genome a little over five times. It also took the public data, cut into pieces 550 letters long, into its assembly. In 2002 three leaders of the public project, Robert Waterston, **[Eric Lander](kloom:e/eric-lander)** and **[John Sulston](kloom:e/john-sulston)**, argued that Celera's paper was "neither a meaningful test of the WGS approach nor an independent sequence of the human genome"; Celera's scientists answered that the charge rested on "incorrect assumptions and flawed reasoning", since their own 27 million paired reads had fixed the genome's order. After leaving the company in 2002, Venter said that much of the DNA it had sequenced was his own.

## What was in it

Before the project, estimates of the number of human genes ran from 80,000 to 140,000. The public paper of 2001 found "about 30,000–40,000 protein-coding genes", "only about twice as many as in worm or fly"; Celera counted 26,588 well supported and about 12,000 more. The "essentially complete" sequence of April 2003 covered 92 percent of the genome with fewer than 400 gaps, and in 2004 the consortium put the count at 20,000 to 25,000. Only about 1.1 percent of the genome lies in exons, the parts of genes that are kept, and about half of it descends from transposable elements. The last 8 percent, the centromeres and other long repeats, waited almost two decades: in 2022 the Telomere-to-Telomere consortium published a gapless sequence of every chromosome but the Y, 3.055 billion letters, and the Y followed in 2023.

The National Human Genome Research Institute puts the cost of that first human sequence at between $500 million and $1 billion, and the American share of the whole project at about $2.7 billion. It has also tracked what a human genome cost to sequence at its centers since then, against a curve that halves every two years:

![Bar chart on a logarithmic scale of the cost of sequencing a human genome: September 2001, 95 million dollars; October 2003, 40 million; October 2005, 14 million; October 2007, 7.1 million; October 2009, 70,000; October 2011, 7,700; October 2013, 5,100; October 2015, 1,200; November 2017, 1,800; November 2019, 700; November 2021, 550; May 2022, 525](cost-per-genome.svg)

| Date     | Cost per genome (NHGRI) | Halving every two years, from 2001 (our arithmetic) |
| -------- | ----------------------: | --------------------------------------------------: |
| Sep 2001 |             $95,263,072 |                                         $95,263,072 |
| Oct 2005 |             $13,801,124 |                                         $23,100,000 |
| Oct 2009 |                 $70,333 |                                          $5,780,000 |
| Oct 2015 |                  $1,245 |                                            $723,000 |
| May 2022 |                    $525 |                                             $73,900 |

For six years the cost fell a little faster than **[Moore's law](kloom:e/moores-law)**, a halving every two years, would have it. Then, in January 2008, the centers changed to new machines that read millions of short fragments at once, and by 2022 the cost was about 140 times below the curve, by our arithmetic. By 2023 the record for reading a human genome was about five hours.

The same machines turned to the genomes of the dead, among them the Neanderthals, in the next frame.

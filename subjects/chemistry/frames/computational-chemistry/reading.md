In 1929 the physicist **[Paul Dirac](kloom:e/paul-dirac)** wrote that the laws needed for "the whole of chemistry" were now completely known, and that the difficulty lay only in the fact that applying them "leads to equations that are too complex to be solved". **[John Pople](kloom:e/john-pople)**, quoting him in his Nobel lecture of 1998, called it "a cry both of triumph and of despair"; **[Walter Kohn](kloom:e/walter-kohn)**, in his, told it as an oral tradition. The equation was Schrödinger's, and for anything larger than a hydrogen atom it could not be solved exactly, by hand or by any machine. **[Computational chemistry](kloom:e/computational-chemistry)** is the half century of finding ways round that, once there were machines to do the arithmetic.

## First machines

The first came from Cambridge. In 1950 **[Frank Boys](kloom:e/samuel-francis-boys)** showed that if the orbitals of a molecule were built from _Gaussian_ functions, bell curves in three dimensions, every one of the hard integrals of the theory could be done exactly. Single Gaussians were poor copies of real orbitals, but a computer could use many of them. In the 1950s Boys and his colleagues ran the first _configuration interaction_ calculations, which let electrons dodge one another, on **[EDSAC](kloom:e/edsac)**, the university's own computer.

At Los Alamos, meanwhile, **[Nicholas Metropolis](kloom:e/nicholas-metropolis)**, Arianna and Marshall Rosenbluth, and Augusta and Edward Teller asked the MANIAC computer a question about matter in bulk. Their paper of 1953, "Equation of State Calculations by Fast Computing Machines", put 224 hard disks in a square and moved them one at a time at random. A move that lowered the energy was always kept; one that raised it by Δ*E* was kept only with chance e^(−Δ*E*/_kT_). Sampling that way, the machine visited arrangements as often as nature would at temperature _T_, and averages over them gave the pressure of the model liquid. Each cycle of 224 moves took the MANIAC about three minutes, and each point on their curve four to five hours. The mathematics subject's Monte Carlo frame tells who did what; in chemistry the rule became the basis of simulating atoms and molecules by chance.

A second way of simulating was to solve Newton's equations for every atom and let them move: **molecular dynamics**. Aneesur Rahman simulated liquid argon in 1964. In 1976, at a workshop in Orsay, J. Andrew McCammon and Bruce Gelin, working with **Martin Karplus**, ran the first simulation of a protein, bovine pancreatic trypsin inhibitor, 58 residues and 458 atoms (some groups counted as one), for 9.2 picoseconds. It showed a protein's inside moving like a fluid, which surprised crystallographers used to still pictures. That year Arieh Warshel and Michael Levitt treated the few atoms where the enzyme lysozyme does its chemistry by quantum mechanics and the rest by classical physics. Karplus, Levitt and Warshel shared the Nobel Prize in Chemistry in 2013 for such "multiscale models".

Pople's group began its program, **Gaussian**, in 1968 and released it as Gaussian 70. It made Boys's functions a standard method that any chemist could run, and of the programs of its time it alone, much expanded, is still in use.

## The exponential wall

Why could the exact answer not simply wait for faster computers? Kohn did the arithmetic in his Nobel lecture. A wavefunction for _N_ electrons is a function of 3*N* coordinates. If each coordinate needs _p_ numbers to describe it, between 3 and 10, the wavefunction needs _p_ to the power 3*N*. For a hundred electrons and _p_ = 3 he found 3³⁰⁰, which he gave as about 10¹⁵⁰ (by our arithmetic it is nearer 10¹⁴³, and he warned that only the logarithm of such estimates should be taken seriously), and wrote that he could not foresee a computer that could search a space that size. Taking a machine that could handle a billion numbers, he found the largest molecule it could treat exactly held six electrons. He called this the "exponential wall".

By our arithmetic, on a coarse grid of 10 points along each coordinate:

| Molecule | Electrons, _N_ | Numbers in the wavefunction, 10³ᴺ | Numbers in the electron density |
| -------- | -------------: | --------------------------------: | ------------------------------: |
| H        |              1 |                               10³ |                             10³ |
| H₂       |              2 |                               10⁶ |                             10³ |
| H₂O      |             10 |                              10³⁰ |                             10³ |
| Benzene  |             42 |                             10¹²⁶ |                             10³ |

Each electron added multiplies the wavefunction a thousandfold. The density, how much electron there is at each point, is a function of three coordinates however many electrons there are.

## Trading exactness for the density

That was Kohn's way through. In Paris in the autumn of 1963 he and Pierre Hohenberg proved that the density of a molecule's lowest state fixes everything else about it, so in principle the energy can be written from the density alone. In 1965 Kohn and Lu Jeu Sham turned the idea into equations for one electron at a time, which a computer could solve. That is **[density functional theory](kloom:e/density-functional-theory)**. Its cost rose, Kohn said, only as the square or cube of the number of atoms, and it handled hundreds of them. Physicists used it from the 1970s; chemists trusted it only in the 1990s, once the approximations below were refined.

The trade is exactness. One term, the energy of exchange and correlation, carries all the ways electrons avoid one another, and its exact form is unknown. Every calculation uses an approximation to it, and the answer is only as good as that approximation. Kohn and Pople shared the Nobel Prize in Chemistry of 1998, Kohn for density functional theory and Pople for computational methods in quantum chemistry. Richard Feynman had made the wall's point in 1981 about all quantum systems, and proposed a quantum computer to climb it. The next segment turns from bonds to materials.

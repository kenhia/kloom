The programs of the 1950s and 1960s lived inside computers, working on
theorems, puzzles and typed sentences. **[Shakey](kloom:e/shakey-the-robot)**, built at the **[Stanford
Research Institute](kloom:e/sri-international)** (now SRI International) in Menlo Park, California,
between 1966 and 1972, was the first mobile robot that could reason about
its own actions. It perceived its world, planned how to reach a goal, and
carried the plan out, in a building rather than on paper.

## A robot, and its world

The project was funded by the [Defense Advanced Research Projects Agency](kloom:e/darpa),
from an SRI proposal of April 1964 for research in "intelligent automata",
and its managers were **Charles Rosen**, **[Nils Nilsson](kloom:e/nils-john-nilsson)** and **[Peter
Hart](kloom:e/peter-e-hart)**. The team kept the machine simple: no arm, and no miniaturization,
just an electronics rack on wheels with a television camera and a homemade
laser rangefinder on top, "bump detectors" to feel for collisions, and an
antenna for the radio link to its computer. That was an [SDS 940](kloom:e/sds-940) at first,
and from 1970 a [DEC](kloom:e/digital-equipment-corporation) [PDP-10](kloom:e/pdp-10), one of the handful of machines on the [ARPANET](kloom:e/arpanet)
at its birth. The name was chosen after a month of looking for a better
one: "it shakes like hell and moves around, let's just call it Shakey."

![Shakey in 1972, with its parts labeled: the antenna for the radio link, the television camera and range finder on its head, the on-board logic and camera control unit, bump detectors, and the drive motor, drive wheel and caster wheel. Photograph by SRI International, CC BY-SA 3.0.](shakey-callouts.jpg)

Its world was built to match. It was half a dozen rooms joined by doorways,
with large geometric blocks painted so their edges showed up on the
low-resolution camera. Dark baseboards made the walls visible too, and gave
the robot a way to correct the errors that built up as it tracked its
position by counting its motors' steps. A task, typed at a console, might be
"push the block off the platform": Shakey had to find the platform, locate a
ramp, push the ramp over to the platform, roll up it, and push the block
off.

## Planning as search

In its second version Shakey's software was built in layers, the first time
a robot had been controlled that way. The layers ran from motor commands at
the bottom to a planner and a supervisor at the top:

| Layer                      | What it did                                                                                             |
| -------------------------- | ------------------------------------------------------------------------------------------------------- |
| Low-level actions          | Talked to the hardware: ROLL, PAN, and PANTO to turn the head to a given direction                      |
| Intermediate-level actions | _Markov tables_ such as GOTHRUDOOR: scan for the first true condition, act, loop, and so keep on trying |
| **STRIPS**, the planner    | Chained actions into a plan to reach a goal                                                             |
| **PLANEX**, the executive  | Watched the plan being carried out, and replanned from the point where it went wrong                    |

**[STRIPS](kloom:e/stanford-research-institute-problem-solver)** (1971), by **Richard Fikes** and Nilsson, combined the
_means–ends analysis_ of [Newell](kloom:e/allen-newell) and [Simon](kloom:e/herbert-a-simon)'s [General Problem Solver](kloom:e/general-problem-solver) with
theorem proving in the predicate calculus. Each action was written as a
rule with _preconditions_ that must hold before it, a _delete list_ of facts
it makes false and an _add list_ of facts it makes true. STRIPS rules, or
their descendants, are used in most planners since. PLANEX generalized
plans into _triangle tables_ that recorded how the steps depended on one
another, so that when something went wrong in the real world it could reuse what still held,
or skip ahead if luck had brought it closer to the goal.

To move between rooms, Shakey needed shortest paths, and Nilsson first
proposed an existing method, the Graph Traverser, which chose the next point
to explore by an estimate _h(n)_ of the distance still to go. **Bertram
Raphael** suggested adding the distance already traveled, _g(n)_, and Hart
worked out the conditions on the estimate that made the result provably
best. The algorithm, **[A\*](kloom:e/a-search-algorithm)**, was published in 1968; the leading journals had
rejected it first. It is still widely used for finding paths. The drawing on the
left is A\* at work on a grid: every dot is a cell it
had to look at on its way from start to goal.

Shakey also needed to see walls and block edges, and there was little
computer vision to borrow. **Richard Duda** and Hart took a 1962 patent by
Paul Hough, which turned the points of an image into lines in a transform
space, and replaced its slopes, which run off to infinity, with an angle and
a distance borrowed from nineteenth-century integral geometry. The result,
published in 1972, is the [_Hough transform_](kloom:e/hough-transform) still used to find lines and
curves in images.

## What it proved

A 1969 SRI film brought Shakey attention. _Life_ called it the "first
electronic person" in 1970. It is now in a glass case at the [Computer
History Museum](kloom:e/computer-history-museum) in Mountain View. But its world had been six rooms and some
painted blocks. By the early 1970s even the most impressive AI programs
could handle only trivial versions of the problems they were meant for; in
some sense they were all "toys". In Britain, a report was about to say so,
and the money would follow it.

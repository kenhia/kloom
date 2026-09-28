At IBM's Watson Research Center in the early 1990s, **Gerald Tesauro** set a
neural network to play backgammon against itself, starting from random
weights and no knowledge of the game. It came close to the best players in the world, and the experts changed how they played.

## Learning from the next guess

Tesauro had already built **Neurogammon**, a network trained on positions
that human experts had scored; it won the Computer Olympiad in 1989. Its
successor, **TD-Gammon**, learned from no expert at all. It used _TD(λ)_, a _temporal-difference_ method invented by **Richard Sutton** on the foundation of Samuel's work: adjust each prediction to match the later, better-informed prediction that follows it.

The network watches one game from the opening to the end. For each
position x_t it outputs Y_t, four numbers estimating the chances of each
result: White or Black winning, by a single game or a _gammon_. After each
move the weights change in proportion to the difference Y_t+1 − Y_t, with a
parameter λ controlling how far back each correction reaches. At the end of
the game the last estimate is compared with the actual result, z. The
drawing shows it: the network above, and below it one game's run of
estimates, each pulled toward the next and the last toward the result.

The network chose the moves for both sides. At first its play was random,
and games could last "several hundred or even several thousand time steps",
against fifty or sixty in human play. It learned anyway. In a few thousand
games it picked up elementary tactics; after tens of thousands, more
sophisticated ideas. A network given only the raw board, with 40 hidden
units and 200,000 games of training, played about as well as Neurogammon.
Its weights had found features of its own, which Tesauro called "one of the
longstanding goals of game learning research since the time of Samuel".
Adding Neurogammon's hand-made features on top produced TD-Gammon 1.0.

## Against the grandmasters

Tesauro's 1995 account gives the program's record against world-class
players, as net points lost:

| Version | Training games | Search | Opponents                                        | Result          |
| ------- | -------------: | ------ | ------------------------------------------------ | --------------- |
| 1.0     |        300,000 | 1-ply  | Robertie, Davis, Magriel                         | −13 in 51 games |
| 2.0     |        800,000 | 2-ply  | Goulding, Woolsey, Snellings, Russell, Sylvester | −7 in 38 games  |
| 2.1     |      1,500,000 | 2-ply  | Robertie                                         | −1 in 40 games  |

Version 2.0 made its public debut at the 1992 World Cup of Backgammon. The
former world champion **Bill Robertie** judged version 2.1 to play "at a
strong master level" within a few hundredths of a point a game of the best
humans, and thought its steadiness would make it the favourite in a long
session.

## The student taught the experts

The surprise was not the strength but the style. For about thirty years
the near-universal opening play with a roll of 2-1, 4-1 or 5-1 had been to
_slot_: move a checker from the six point to the five point, risking a hit
for a strong position. When Robertie wrote about TD-Gammon in _Inside
Backgammon_ in 1992, he included its rollouts showing that splitting the
back checkers, 24-23, was better. Top players tried the split, won with it,
and by Tesauro's 1995 account slotting had "virtually disappeared from
tournament competition". (It later came back for the 2-1 roll.) The expert **Kit Woolsey** found its weighing of risk against safety better than his own or any human's.

It had weaknesses. Its short look-ahead left it weak in endgames that need
calculation, and it had been trained without the doubling cube. In a
100-game exhibition against **Malcolm Davis** at the 1998 AAAI Hall of
Champions, it lost by eight points, mostly on one doubling blunder.
TD-Gammon itself was never sold, but commercial neural-network programs
such as JellyFish and Snowie followed, and the papers on deep Q-learning
and AlphaGo cited it.

TD-Gammon found its knowledge for itself. The next machine in this trail was the opposite: everything it knew was put there by hand, and it was built to beat one man.

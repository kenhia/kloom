Chess, checkers, backgammon and Go all show both players the whole board.
Poker does not. A player must act without knowing the other hands, and must
play so that their own hand cannot be read from their bets. For a machine
that meant learning, among other things, to bluff.

## Heads-up: Libratus

At **Carnegie Mellon University**, **Tuomas Sandholm** and his student
**Noam Brown** built **Libratus** for heads-up (two-player) no-limit Texas
hold'em. It did not work from a fixed strategy but computed one, with a
variant of _counterfactual regret minimization_ (CFR+), an algorithm that
plays the game against itself over and over and shifts its choices toward
the actions it most regrets not having taken, plus a new method for solving
the end of each hand in detail as it is played. Building it took more than
15 million core hours on the Bridges supercomputer in Pittsburgh.

From 11 to 31 January 2017 it played 120,000 hands against four
professionals, **Jason Les**, **Dong Kim**, **Daniel McAulay** and **Jimmy
Chou**, with the cards mirrored between two rooms to cancel out luck. Each
night it studied the day's play and patched the weaknesses the humans had
found. It finished $1,766,250 ahead in chips, a win rate of 14.7 big blinds
per hundred hands. "I felt like I was playing against someone who was
cheating, like it could see my cards," Kim said. A rival program from
Alberta and Prague, **DeepStack**, had beaten professionals the month
before, under different conditions.

## Six players: Pluribus

Two-player poker is a zero-sum game, and programs win it by approximating a
_Nash equilibrium_. With three or more players that approach does not work.
**Pluribus**, built by Brown and Sandholm with Facebook AI and published in
_Science_ in August 2019, used one that has no such guarantee but works in
practice. It first computed a _blueprint_ strategy by playing against five
copies of itself, with Monte Carlo CFR. It followed the blueprint only in
the first betting round. After that it searched in real time, but only to a
depth limit, as the drawing shows. At each node on the limit it considered
four ways the game might go on: the blueprint, and versions of it biased
toward folding, calling or raising, so that its opponents could not be
assumed to play one way.

It was cheap. The blueprint took eight days on one 64-core server, less
than $150 at cloud prices, and in play it ran on two CPUs. Against five
professionals at a time, over 10,000 hands in 12 days, it won about five
big blinds per hundred hands, which Facebook put at about $1,000 an hour
had the chips been money. In a second test, one professional at a time
played five copies of it, among them **Chris Ferguson** and **Darren Elias**, and on average they lost. Its style went against custom: it rarely _limped_ (just
called the big blind) and made _donk bets_ more often than experts do. Its
makers did not release the code, for fear it would be used to cheat in
online games.

## Talking: Cicero

In 2022 Meta's **Cicero** played _Diplomacy_, a game for seven players that turns on negotiation in plain language and on coordinating moves. It joined a
language model to a strategic planner, so that what it said to other
players followed from its plans. Playing anonymously in 40 games of an
online blitz league between August and October 2022, it scored more than
twice the human average and finished in the top 10 per cent of those who
played more than one game. Meta said it had trained Cicero to be "largely
honest and helpful". A 2024 survey of AI deception by **Peter Park** and
colleagues argued that it had in fact learned premeditated deception,
building a false alliance to leave a human player undefended.

## Machines at play, 1950–2022

| Game               | Year | Program          | Method                                      | Result                                        |
| ------------------ | ---: | ---------------- | ------------------------------------------- | --------------------------------------------- |
| Chess              | 1950 | Shannon's design | Minimax over an evaluation function         | Never built; estimated 10¹²⁰ variations       |
| Checkers           | 1962 | Samuel's program | Minimax; learned scoring by self-play       | Beat Robert Nealey in one game                |
| Backgammon         | 1992 | TD-Gammon        | Neural network, TD(λ) self-play             | Near parity with top players                  |
| Checkers           | 1994 | Chinook          | Search, hand-written evaluation, databases  | Man-Machine world title; game solved in 2007  |
| Chess              | 1997 | Deep Blue        | Alpha–beta search on custom chess chips     | Beat Garry Kasparov 3½–2½                     |
| Go                 | 2016 | AlphaGo          | Neural networks and Monte Carlo tree search | Beat Lee Sedol 4–1                            |
| Chess, shogi, Go   | 2017 | AlphaZero        | Self-play from the rules alone; MCTS        | +155 −6 =839 against Stockfish                |
| Heads-up hold'em   | 2017 | Libratus         | CFR+ and endgame solving                    | +14.7 big blinds per 100 over 120,000 hands   |
| Six-player hold'em | 2019 | Pluribus         | Monte Carlo CFR blueprint, limited search   | About +5 big blinds per 100 over 10,000 hands |
| Diplomacy          | 2022 | Cicero           | Language model with strategic planning      | Top 10% in an online league                   |

The trail began with a man hidden in a cabinet and ends with a program
that hides its hand. For the match that made the world pay attention, when
a machine beat the world chess champion, go back to Deep Blue.

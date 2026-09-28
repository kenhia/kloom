The symbolic programs of the 1950s did what their authors told them.
**Frank Rosenblatt**, a psychologist, wanted a machine that would be shown
examples and find its own rules, as he believed a brain does. He called it
the **perceptron**, and it is the ancestor of every neural network in this
subject.

## A model of a brain

Rosenblatt (1928–1971) took his doctorate at Cornell in 1956 and moved to
the **Cornell Aeronautical Laboratory** in Buffalo, New York. In 1957 he
simulated a perceptron on an IBM 704 there, and in 1958 he set the idea out
in _Psychological Review_: a network of three kinds of units, _sensory_ (S),
_association_ (A) and _response_ (R). Its neuron was, in his words, "a direct
descendant" of the one McCulloch and Pitts had proposed in 1943, but the
perceptron's connections into its response units carried _weights_ that
changed with experience. When it answered wrongly, the
weights were adjusted, and if the problem could be solved at all by a single
dividing line through the space of inputs, the adjustments were guaranteed
to arrive at one: Rosenblatt's convergence theorem.

The money came from the US Office of Naval Research (ONR), under a
contract called **Project PARA** ("Perceiving and Recognition Automata"),
and from the Rome Air Development Center. The sums were modest. ONR's
research manager, Marvin Denicoff, later said ONR rather than ARPA funded
the project because it was unlikely to produce technological results in the
near or medium term: ONR grants were of the order of $10,000, where ARPA's
ran to millions.

## "The embryo of an electronic computer"

In 1958 the Navy organised a press conference for Rosenblatt in
Washington. Early demonstrations were simple: telling sheets of paper marked
on the right from sheets marked on the left. On 8 July _The New York Times_
ran the story on page 25 as "New Navy Device Learns by Doing", and it began:

> The Navy revealed the embryo of an electronic computer today that it
> expects will be able to walk, talk, see, write, reproduce itself and be
> conscious of its existence.

What Rosenblatt said caused a heated controversy in the young AI
community. He had been a schoolmate of **Marvin Minsky** at the Bronx High
School of Science, and Minsky became a staunch objector to pure
_connectionist_ AI, built from networks like this one. The competition for
government funding ended with symbolic AI the winner.

## The Mark I

Rosenblatt wanted a machine, not a program. The **Mark I Perceptron** was a
custom analogue computer. Its retina was a 20 × 20 grid of 400 photocells.
Each could connect to up to 40 of 512 association units, wired at random
through a plugboard according to a table of random numbers, because
Rosenblatt believed the retina was randomly connected to the visual cortex.
Eight response units took the association units' outputs through
adjustable weights, which were potentiometers turned by electric motors
while the machine learned.

![The Mark I Perceptron, figure 2 of its operators' manual (February 1960): a camera on a tripod, the S-unit monitor and manual stimulus switches, the plugboard of random S-unit to A-unit connections, the racks of association units, and the response and meter panels](mark-i.png)

Sources disagree on the date. The team assembled and tested the machine
between June and December 1959, and its first public demonstration was on
23 June 1960; some accounts date the Mark I to 1958, the year of the paper
and the press conference. Reported experiments show both what it could do
and how narrow the tasks were:

| Task              | Units | Training images | Accuracy      | Variation allowed         |
| ----------------- | ----- | --------------: | ------------- | ------------------------- |
| Square or circle  | 500   |          10,000 | 99.8%         | position and orientation  |
| Square or diamond | 1,000 |              60 | 100%          | position only             |
| Letter X or E     | 1,000 |              20 | 100%          | position, rotation to 30° |
| Letter X or E     | 1,000 |              60 | 90%           | position, any rotation    |
| Letter E or F     | 1,000 |              60 | more than 80% | position only             |

The CIA's photographic division studied it from 1960 to 1964 for picking out
planes and ships in aerial photographs. In 1967 the machine went to the
Smithsonian, where it is now in the National Museum of American History.

In 1969 Minsky and Seymour Papert's book _Perceptrons_ showed that a
single-layer perceptron cannot learn some simple functions, such as
exclusive-or. The book was widely, and often wrongly, cited as proof that
perceptrons in general were limited, and interest and funding for neural
networks fell away for a decade. Rosenblatt died in a boating accident on his 43rd birthday, in July 1971. Follow the trail from here for the long road from his machine to deep
learning, or go on along the main spine to a program that needed no learning
at all to convince people it understood them.

The convolutional network that reads your photographs has a grandparent
that was built to understand a cat's eye. It came from a Japanese broadcast
engineer, a decade before anyone could train such a thing well.

## Simple cells and complex cells

In 1959 **David Hubel** and **Torsten Wiesel** published "Receptive fields of
single neurones in the cat's striate cortex". Recording from single cells in
the visual cortex, they found that each responds only to a small patch of
the visual field, its _receptive field_. In that paper and the work that
followed through the 1960s, they sorted the cells into kinds. _Simple cells_ fire most for a straight edge at a particular angle in
a particular place. _Complex cells_ have larger receptive fields and respond
to the edge wherever it falls within them. Hubel and Wiesel proposed a
hierarchy in which the one kind feeds the other, small simple fields combining into
larger and more complex ones. They shared the Nobel Prize in Physiology or
Medicine in 1981.

## Fukushima's layers

**Kunihiko Fukushima** (born 1936) studied electronics at Kyoto University
and worked at the research laboratories of NHK, Japan's public broadcaster.
In 1969 he published a layered network for picking out visual features,
modelled on Hubel and Wiesel. "All the elements in one layer have the same
set of interconnecting coefficients," he wrote. Its connections were designed
by hand; the same paper introduced the _rectified linear unit_, now the most
common activation function in deep learning. In 1975 came the _cognitron_,
which organised itself by learning but took a pattern in a new position for
a different pattern. Its successor, first reported in 1979, was published in
_Biological Cybernetics_ in 1980 under the title "Neocognitron: A
self-organizing neural network model for a mechanism of pattern recognition
unaffected by shift in position".

The **neocognitron** alternates two kinds of layer, named for Hubel and
Wiesel's cells. _S-cells_ extract features: their input connections are
learned, and each comes to respond to one pattern, such as a line at one
angle, in its small receptive field. _C-cells_ tolerate shifts: each has
fixed connections from a group of S-cells that detect the same feature in
slightly different places, and fires if any of them does, so a feature that
moves a little still excites the same C-cell. Repeated stage after stage,
local features combine into larger ones while small distortions are absorbed
a little at a time. The last layer's cells each stand for one whole pattern,
wherever it appears.

The key design decision was that the cells in each _cell-plane_ share the
same input connections, each looking at a different place. One set of
weights is swept across the whole image. That is what we now call a
_convolution_, and the C-layers are what we now call _pooling_.

The 1980 computer simulation, the network in the drawing, had seven layers:

| Layer | Cells        | What it does                            |
| ----- | ------------ | --------------------------------------- |
| U0    | 16 × 16      | the input, an array of photoreceptors   |
| US1   | 16 × 16 × 24 | first features, each from a 5 × 5 patch |
| UC1   | 10 × 10 × 24 | tolerates small shifts                  |
| US2   | 8 × 8 × 24   | combinations of features                |
| UC2   | 6 × 6 × 24   | tolerates shifts again                  |
| US3   | 2 × 2 × 24   | near-whole patterns                     |
| UC3   | 24           | one cell per cell-plane: the answer     |

It learned "without a teacher": in each small area, the S-cell that
responded most strongly to a pattern had its active connections
strengthened: winner takes all. Fukushima showed it the digits 0 to
4, each twenty times at randomly shifted positions. Afterwards each digit
excited exactly one cell in the last layer, and shifting the digit did not
change which. Ten digits could be learned, but only with finely tuned
settings. More cell-planes would help, he wrote, but that had not been tried
"because of the lack of memory capacity of our computer".

## The ancestry of convolution

What the neocognitron lacked was a way to train every layer towards a goal.
Its learning was local and unsupervised. In 1989 **Yann LeCun** and his
colleagues trained the weights of a convolutional network directly from
images of handwritten digits by backpropagation, and the Nobel Committee for
Physics, writing in 2024, traced that architecture's roots to the
neocognitron, and through it to Hubel and Wiesel. LeCun's networks were
reading handwritten digits on cheques for several American banks from the
mid-1990s. Fukushima, who later taught at Osaka University and elsewhere,
received the Bower Award for Achievement in Science in 2020.

The neocognitron passed signals one way, from the eye upward. In 1982 a
physicist at Caltech published a network in which every unit talks to every
other, and a memory is a place the network settles into.

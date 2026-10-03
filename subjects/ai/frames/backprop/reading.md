In 1969 the case against neural networks had been that a single layer of
artificial neurons could learn only simple things. Everyone knew that networks
with more layers could represent far more; what nobody could say was how to
train them. On 9 October 1986 a four-page letter in _Nature_ gave the answer
that stuck.

## Four pages in Nature

"Learning representations by back-propagating errors" was written by
**[David Rumelhart](kloom:e/david-rumelhart)** and **[Ronald Williams](kloom:e/ronald-j-williams)** of the Institute for Cognitive
Science at the University of California, San Diego, and **[Geoffrey Hinton](kloom:e/geoffrey-hinton)**,
then at [Carnegie Mellon](kloom:e/carnegie-mellon-university) in Pittsburgh. Its abstract describes the whole
method in one sentence: a procedure that "repeatedly adjusts the weights of the
connections in the network so as to minimize a measure of the difference
between the actual output vector of the net and the desired output vector."

The paper's network is built in layers, like the one on the left of the
drawing. In the _forward pass_, each unit adds up its inputs, each multiplied
by the weight of its connection, and passes the sum through a smooth S-shaped
function, the _sigmoid_ drawn on the right. The error is half the sum of the
squared differences between what the output units produced and what they
should have produced.

The _backward pass_ is the new part. For each output unit the error's
sensitivity to its output is simply the difference, actual minus desired.
Multiply that by the slope of the sigmoid at that point, which is y(1−y) and
costs nothing to compute, and you have the error's sensitivity to the unit's
input. From there the _chain rule_ of calculus runs backwards: every weight
feeding the unit gets its share, in proportion to the activity that came
through it, and every unit in the layer below receives a sum of these signals
from above and repeats the calculation. One sweep backwards gives the
derivative of the error with respect to every weight in the network at once.
Nudge each weight a little against its derivative, and the error falls.

## Hidden units

The point of the paper was in its title: _representations_. Units in the
middle of the network, belonging to neither input nor output, "come to
represent important features of the task domain". One small network learned
to tell whether a row of inputs was a mirror image of itself; after 1,425
sweeps through all 64 possible inputs, its two hidden units had found weights
in a symmetric pattern of ratio 1:2:4 that no one had put there. A larger one
learned two family trees of twelve people each, one English and one Italian.
Trained on 100 of the 104 relationships in them, it got the other four right,
and when the authors looked inside, one hidden unit had come to stand for
English versus Italian and another for generation, though nothing in the
input said so.

## Who invented it

The Nature paper popularized [backpropagation](kloom:e/backpropagation); it did not originate it, and
the history is tangled. The chain rule itself goes back to **[Leibniz](kloom:e/gottfried-wilhelm-leibniz)** in 1676. **[Frank Rosenblatt](kloom:e/frank-rosenblatt)** used the phrase "back-propagating error correction"
in 1962 without having a way to do it. In 1970 the Finnish student **[Seppo
Linnainmaa](kloom:e/seppo-linnainmaa)** described the _reverse mode of automatic differentiation_ in his
master's thesis, which is the same calculation for any network of
differentiable functions, though he did not apply it to neural networks. The
American **[Paul Werbos](kloom:e/paul-werbos)** described training neural networks by
backpropagation in his 1974 dissertation, and in 1982 applied it to layered
networks in the way that became standard. Rumelhart worked the method out
independently in the spring of 1982, and the 1986 authors did not cite the
earlier work because they did not know of it.

The Nature letter itself credited independent variants by **David
Parker** and **[Yann LeCun](kloom:e/yann-lecun)**. Acceptance took time. Gradient descent offered no
guarantee of finding the best weights rather than merely a local minimum, a
drawback the authors admitted, and physiologists
"knew" that real neurons fired all or nothing, which leaves no gradient to
follow. What won the argument was results: in 1987 **NETtalk** learned to
pronounce English text and appeared on the _Today_ show, and in 1989 a
network trained this way began reading handwritten postcodes.

The paper arrived with a movement. The same year Rumelhart, **[James
McClelland](kloom:e/james-mcclelland-psychologist)** and the **PDP Research Group** published _Parallel Distributed
Processing_, two volumes from MIT Press that set out [_connectionism_](kloom:e/connectionism), the view
that cognition emerges from many simple units working at once, against the
symbol-processing AI of the expert systems. Hinton shared the 2024 [Nobel Prize
in Physics](kloom:e/nobel-prize-in-physics) for his work on neural networks. The rule-based systems, meanwhile,
were about to lose the machines built to run them: the next frame is the
collapse of the Lisp machine market.

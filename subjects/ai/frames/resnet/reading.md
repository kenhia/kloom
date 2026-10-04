After [AlexNet](kloom:e/alexnet) the lesson seemed simple: deeper networks see better. AlexNet
had eight layers; the VGG networks of 2014 had nineteen. But past a point,
adding layers made networks worse, and not in the way anyone expected. In
December 2015 four researchers at [Microsoft Research](kloom:e/microsoft-research) published a fix so
simple it fits in one line, and it has been part of deep networks ever
since.

## The degradation problem

A deeper network ought to be able to do at least as well as a shallower one.
Take a good shallow network, add layers that simply pass their input through
unchanged, and the deeper network computes exactly the same thing. Yet when
**[Kaiming He](kloom:e/kaiming-he)**, Xiangyu Zhang, Shaoqing Ren and Jian Sun trained plain
networks of increasing depth, the deeper ones had _higher_ error, and not
only on new images: they were worse on the very images they were trained on.
So this was not overfitting. The optimizer simply could not find the
solution that was known to exist.

Their own comparison on [ImageNet](kloom:e/imagenet) shows it. In the table below, adding sixteen
layers to a plain network made its error worse; adding the same layers to a
[residual network](kloom:e/residual-neural-network) made it better.

| Layers | Plain network | Residual network |
| -----: | ------------: | ---------------: |
|     18 |        27.94% |           27.88% |
|     34 |        28.54% |           25.03% |

_Top-1 error on the ImageNet validation set, 10-crop testing (He et al.,
table 2)._

It was not the old problem of [_vanishing gradients_](kloom:e/vanishing-gradient-problem), they argued. Their plain
networks used **batch normalization**, a technique published that February
by Sergey Ioffe and Christian Szegedy at Google, which rescales the inputs to
each layer over every mini-batch of training examples. Ioffe and Szegedy had
shown that it let networks train with much higher learning rates, reaching
the same accuracy in fourteen times fewer steps, and with it they had pushed
ImageNet top-5 error to 4.9 percent. With batch normalization the signals in
He's plain networks did not vanish, going forward or back. The networks were
just hard to optimize. (Why batch normalization itself works is still debated: its
authors said it reduced shifts in each layer's inputs during training, and
later experiments suggest that is not the reason.)

## Learn the difference

The fix was to change what each block of layers is asked to learn. Instead
of learning a whole mapping _H_(_x_), a block learns only the _residual_,
_F_(_x_) = _H_(_x_) − _x_, and a _shortcut connection_ adds the input back at
the end: the output is _F_(_x_) + _x_. That is the plate on the left: two
weight layers, and the input carried round them to be added back. If the
best thing a block can do is nothing, its layers only have to learn zero,
which is easy, rather than the identity, which stacks of plain layers
seemed to find hard. The shortcut adds no parameters, and no computation
beyond the addition.

With it, depth paid off again. The team trained residual networks of 50, 101
and **152 layers**, eight times deeper than VGG. Even at 152 layers the
network needed 11.3 billion multiply–add operations for an image, fewer than
the 19.6 billion of the 19-layer VGG. On a smaller dataset, CIFAR-10, they
trained networks of more than 100 layers and explored one of more than
1,000. An ensemble of residual networks reached 3.57 percent top-5 error on
the ImageNet test set and won the 2015 challenge's classification task; the
same networks won its detection and localization tasks, and detection and
segmentation in the COCO competition.

## Everywhere since

Shortcuts were not new. Skip-layer connections appear in networks of the
1980s, and _highway networks_, also from 2015, used gated shortcuts; a residual network behaves like a highway network with its gates
held open. What the paper showed, at scale, was that the plain identity shortcut was
enough, and it made the pattern widely popular.

It has stayed so. Residual connections run through [AlphaGo Zero](kloom:e/alphago-zero) and
[AlphaFold](kloom:e/alphafold), and through the [transformer](kloom:e/transformer-deep-learning) models, [BERT](kloom:e/bert-language-model) and GPT among them, that
come later on this spine. The next frame returns
to games, where deep networks met another way of learning: from reward.

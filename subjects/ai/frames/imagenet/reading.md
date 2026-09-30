In the 2000s most artificial intelligence research was about models and
algorithms. An assistant professor at [Princeton](kloom:e/princeton-university) bet on something else: that
machines learning to see needed, above all, far more to look at.

## A picture for every noun

**[Fei-Fei Li](kloom:e/fei-fei-li)** began working on the idea in 2006. In 2007 she met **Christiane
Fellbaum**, one of the creators of [_WordNet_](kloom:e/wordnet), a database that sorts English
words into sets of synonyms, _synsets_, arranged in a hierarchy from general
to particular (in [ImageNet](kloom:e/imagenet) it runs nine levels deep, from _mammal_ down to
_German shepherd_). Li decided to build an image database on that skeleton, starting from WordNet's
roughly 22,000 nouns, and to fill each synset with hundreds of photographs.
The plate on the left is that design: a tree of concepts, and a stack of
labelled images hanging from every leaf.

The first paper, by **Jia Deng**, Li and their colleagues at the 2009
Conference on Computer Vision and Pattern Recognition (CVPR), described
twelve subtrees, from mammals and birds to tools and fruit: 5,247 synsets and
3.2 million images. The aim was far larger, an average of 500 to 1,000 clean
images for each of WordNet's 80,000 noun synsets, "tens of millions of
annotated images".

![Fei-Fei Li speaking at a lectern at the ITU's AI for Good summit in 2017](fei-fei-li.jpg)

## Forty-nine thousand labellers

The candidates came from image search engines, queried with each synset's
synonyms and their translations into Chinese, Spanish, Dutch and Italian.
Deciding which of them really showed the thing named was the expensive part,
far beyond what a small group of annotators could do. The team turned to
**[Amazon Mechanical Turk](kloom:e/amazon-mechanical-turk)**, an online marketplace for small paid tasks.
Several workers judged each image independently, and it was kept only with a
convincing majority. The majority needed depended on the synset: a few votes
settle "cat", but the paper found that "Burmese cat" could take five. The
result, checked by sampling, was 99.7 per cent precise.
Labelling ran from July 2008 to April 2010. By one account 49,000 workers in
167 countries filtered more than 160 million candidate images, and in 2012
ImageNet was the largest academic user of Mechanical Turk in the world.

By April 2010 the database held **14,197,122 images** in 21,841 synsets, a
million of them with boxes drawn around the objects. ImageNet did not own the
pictures: what it published was the list of their web addresses and the
labels.

| ImageNet, by stage                | Categories |                Images |
| --------------------------------- | ---------: | --------------------: |
| CVPR paper, 2009                  |      5,247 |           3.2 million |
| Full release, April 2010          |     21,841 |            14,197,122 |
| ILSVRC challenge set, 2010 onward |      1,000 | ~1.2 million training |

## The challenge

A dataset only changes a field if people use it. In 2010 Li's group started
the **ImageNet Large Scale Visual Recognition Challenge** (ILSVRC), modelled
on the smaller PASCAL VOC contest, which in 2010 had 20 object classes and
19,737 images. ILSVRC used 1,000 classes (from 2012, 120 of them breeds of dog), with
about 1.2 million training images, 50,000 for validation and 100,000 for a
test set whose labels, after the first year, were kept secret. Each image
carried one label, but a photograph labelled _strawberry_ might show an apple
too, so a program was allowed five guesses. It was scored by its _top-5
error_: how often the right answer was not among them.

Eleven teams entered the first year. The winner, a team from NEC Labs
America, the University of Illinois and Rutgers, combined hand-designed image
features (SIFT and LBP) with a
[support vector machine](kloom:e/support-vector-machine), and it missed on 28.2 per cent of the test images.
In 2011 the best entry, from Xerox Research Centre Europe, got that down to
25.8 per cent.

## What was in the pictures

A dataset built from the web and WordNet carries both with it. In 2019 and
2020 the ImageNet team examined the 2,832 categories in its _person_ subtree
and judged 1,593 of them potentially offensive, and most of the rest not
visual at all: only 158 described something a photograph could show. By 2021
most of the person categories had been removed from the full dataset, and the
faces in the challenge images were blurred. Studies have also estimated that more than 6 per cent of
the labels in the challenge's validation set are wrong.

None of this was visible yet in 2011. What was visible was a leaderboard,
improving by a few points a year. In 2012 a team from [Toronto](kloom:e/university-of-toronto) entered a
neural network, and cut the winning error by nearly ten points at once.

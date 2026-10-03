# Start screen art

`loom.svg` is kloom's opening drawing: a power loom, traced to vector and
re-inked by the page (gold on black for the western-civ subject).

## Source and license

- **Work:** "Modern Loose Reed Power Loom", an engraving from Richard
  Marsden, _Cotton Weaving: Its Development, Principles, and Practice_
  (London: George Bell & Sons, 1895). The Commons file page gives the date
  as "Published 1892" and the book citation as 1895.
- **File:** [File:Modern_Loose_Reed_Power_Loom-marsden.png](https://commons.wikimedia.org/wiki/File:Modern_Loose_Reed_Power_Loom-marsden.png)
  on Wikimedia Commons, scanned and uploaded by Clem Rutter (2009), used in
  the Wikipedia article _Lancashire Loom_.
- **License:** public domain. Checked on 2026-09-26: the file page carries
  `{{PD-UK-unknown}}` and `{{PD-1923}}` (public domain in the United
  States), and its metadata states "Public domain", attribution not
  required. We credit it anyway, in the start screen's _Image credit_ and in
  `credit.ts`.

## How it was made (sprint 002)

With [`create-tools/trace-art`](../../../create-tools/trace-art/), with its
defaults: flattened onto white, traced with potrace (threshold 150,
turdsize 6, opttolerance 0.6), and the 901 contours sorted into eight
left-to-right bands. Running it on the Commons PNG reproduces this file byte
for byte. The page strokes the contours instead of filling them, which gives
the double-line "wireframe" look.

The drawing is loaded after the page, as its own compressed chunk, so the
server-rendered page stays small.

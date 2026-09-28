# bar-chart

A bar chart for the reading pane, written as an SVG and placed with a
markdown image. The reading pane inlines it through the illustration
sanitiser, so the chart takes the reader's palette and follows the palette
mode (sprint 008, korg 3406). It draws in `currentColor`, the page's ink, and
marks its palette hooks with two classes that the page colours: `muted` (the
axis and sublabels) and `accent` (a highlighted bar). The markdown image's alt
text is its accessible name in the page. The file's own `<title>` and
`<desc>` serve anyone who opens it alone. Also put the numbers in a table
under the image.

```sh
python3 create-tools/bar-chart/bar_chart.py create-tools/bar-chart/examples/book-output.json \
  subjects/western-civ/frames/printing-press/book-output.svg
```

## Spec

See `examples/book-output.json`, the printing-press chart.

| Field                         | Meaning                                                                                       |
| ----------------------------- | --------------------------------------------------------------------------------------------- |
| `title`, `description`        | The SVG's accessible name and description.                                                    |
| `heading`                     | The small caption across the top.                                                             |
| `unit`                        | Suffix for the value labels (`"M"`).                                                          |
| `scale`                       | Optional: `"log"` for a log10 axis (sprint 006, for quantities spanning orders of magnitude). |
| `axis`                        | `max` (and `min`, required for `log`), and `ticks` as `[value, label]` pairs.                 |
| `bars`                        | `label`, optional `sublabel`, `value`, optional `display` (the value's label), `highlight`.   |
| `width`, `height`, `barWidth` | Optional; default 480, 300 and 56.                                                            |

The chart is media, so the frame needs a `media` citation for the file. Give
it a licence (the repo's MIT for a chart drawn here), and put the data's
source in the citation's `url` and `container`.

## The charts made with it

Each spec in `examples/` is the source of one committed chart. Re-running
all of them reproduces the charts byte for byte:

| Spec                        | Chart                                                        |
| --------------------------- | ------------------------------------------------------------ |
| `book-output.json`          | `subjects/western-civ/frames/printing-press/book-output.svg` |
| `alphazero-search.json`     | `subjects/ai/frames/alphazero/search-speed.svg`              |
| `dartmouth-budget.json`     | `subjects/ai/frames/dartmouth/budget.svg`                    |
| `ilsvrc-top5.json`          | `subjects/ai/frames/alexnet/ilsvrc-top5.svg`                 |
| `metr-time-horizons.json`   | `subjects/ai/frames/capability-evals/time-horizons.svg`      |
| `mnist-2006.json`           | `subjects/ai/frames/deep-belief-nets/mnist-error.svg`        |
| `model-parameters.json`     | `subjects/ai/frames/pretraining/model-parameters.svg`        |
| `sae-dictionary-size.json`  | `subjects/ai/frames/interpretability/dictionary-size.svg`    |
| `temperature.json`          | `subjects/ai/frames/next-token/temperature.svg`              |
| `tokens-per-parameter.json` | `subjects/ai/frames/scaling-laws/tokens-per-parameter.svg`   |
| `training-compute.json`     | `subjects/ai/frames/compute/training-compute.svg`            |
| `turing-storage.json`       | `subjects/ai/frames/turing-test/turing-storage.svg`          |

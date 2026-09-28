# bar-chart

A bar chart for the reading pane, as a standalone SVG shown with a markdown
image. It carries `<title>` and `<desc>` for screen readers. Also put the
numbers in a table under the image.

```sh
python3 create-tools/bar-chart/bar_chart.py create-tools/bar-chart/examples/book-output.json \
  subjects/western-civ/frames/printing-press/book-output.svg
```

## Spec

See `examples/book-output.json`, the printing-press chart.

| Field                         | Meaning                                                                                            |
| ----------------------------- | -------------------------------------------------------------------------------------------------- |
| `title`, `description`        | The SVG's accessible name and description.                                                         |
| `heading`                     | The small caption across the top.                                                                  |
| `unit`                        | Suffix for the value labels (`"M"`).                                                               |
| `colours`                     | `background`, `ink`, `muted`, `accent`: the frame's palette. An `<img>` cannot inherit the page's. |
| `scale`                       | Optional: `"log"` for a log10 axis (sprint 006, for quantities spanning orders of magnitude).      |
| `axis`                        | `max` (and `min`, required for `log`), and `ticks` as `[value, label]` pairs.                      |
| `bars`                        | `label`, optional `sublabel`, `value`, optional `display` (the value's label), `highlight`.        |
| `width`, `height`, `barWidth` | Optional; default 480, 300 and 56.                                                                 |

The chart is media, so the frame needs a `media` citation for the file. Give
it a licence (the repo's MIT for a chart drawn here), and put the data's
source in the citation's `url` and `container`.

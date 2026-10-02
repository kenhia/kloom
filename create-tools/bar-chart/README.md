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

| Field                         | Meaning                                                                                         |
| ----------------------------- | ----------------------------------------------------------------------------------------------- |
| `title`, `description`        | The SVG's accessible name and description.                                                      |
| `heading`                     | The small caption across the top.                                                               |
| `unit`                        | Suffix for the value labels (`"M"`).                                                            |
| `scale`                       | Optional: `"log"` for a log10 axis (sprint 006, for quantities spanning orders of magnitude).   |
| `axis`                        | `max` (and `min`, required for `log`), and `ticks` as `[value, label]` pairs.                   |
| `bars`                        | `label`, optional `sublabel`, `value`, optional `display` (the value's label), `highlight`.     |
| `width`, `height`, `barWidth` | Optional; default 480, 300 and 56.                                                              |
| `source`                      | Optional: `container`, `doi` and/or `url`, `accessed`. The chart's `media` citation is printed. |

A value's label has one decimal under 100 unless the value is whole: 28, not 28.0 (sprint 015).

It refuses, writing nothing, a spec whose text will not fit (sprint 021,
when authors could not see their charts and three headings ran off the
right edge): a heading wider than the chart, two neighbouring labels that
overlap, a bar so tall that its value's label meets the heading, and (since
sprint 027, after a "1,000,000" tick was cut off) a tick label wider than
the space left of the axis, about eight characters. Widen
the chart (`width`) or raise the axis `max`; shorten text only when nothing
is lost. The estimate takes a monospace glyph as 0.6 em. Look at a chart
before it goes live with `contact_sheet.py <subject> <frame> --charts`.

The chart is media, so the frame needs a `media` citation for the file. Give
it a licence (the repo's MIT for a chart drawn here), and put the data's
source in the citation's `container`, with its DOI in `doi` (bare,
`10.1289/EHP7932`) or, without one, its `url`. A media citation's DOI is
its data's: the bibliography gives it as "Data: https://doi.org/…" and the
caption credit as "data doi:…", and `url` stays for an image's or a file's
own page (sprint 033). Give the spec a `source` (`container`, `doi` and/or
`url`, and `accessed` if not today) and the tool prints that citation, ready
to paste.

## The charts made with it

Each spec in `examples/` is the source of one committed chart. Re-running
all of them reproduces the charts byte for byte:

| Spec                                              | Chart                                                                 |
| ------------------------------------------------- | --------------------------------------------------------------------- |
| `alphazero-search.json`                           | `subjects/ai/frames/alphazero/search-speed.svg`                       |
| `book-output.json`                                | `subjects/western-civ/frames/printing-press/book-output.svg`          |
| `computing-arpanet-nodes.json`                    | `subjects/computing/frames/arpanet/nodes.svg`                         |
| `computing-bombes-available.json`                 | `subjects/computing/frames/bombe/bombes-available.svg`                |
| `computing-bsd-copies.json`                       | `subjects/computing/frames/bsd/copies-shipped.svg`                    |
| `computing-calculators-made.json`                 | `subjects/computing/frames/pascaline/calculators-made.svg`            |
| `computing-census-trial.json`                     | `subjects/computing/frames/hollerith/census-trial.svg`                |
| `computing-cloud-q2.json`                         | `subjects/computing/frames/cloud/cloud-q2.svg`                        |
| `computing-disk-cost.json`                        | `subjects/computing/frames/ibm-360/disk-cost.svg`                     |
| `computing-early-valves.json`                     | `subjects/computing/frames/eniac/valves.svg`                          |
| `computing-engine-costs.json`                     | `subjects/computing/frames/clement-fragment/engine-costs.svg`         |
| `computing-ethernet-speeds.json`                  | `subjects/computing/frames/ethernet/ethernet-speeds.svg`              |
| `computing-first-stores.json`                     | `subjects/computing/frames/univac/first-stores.svg`                   |
| `computing-flops-per-watt.json`                   | `subjects/computing/frames/where-computing-is/flops-per-watt.svg`     |
| `computing-gui-prices.json`                       | `subjects/computing/frames/macintosh/gui-prices.svg`                  |
| `computing-https-share.json`                      | `subjects/computing/frames/tls/https-share.svg`                       |
| `computing-internet-hosts.json`                   | `subjects/computing/frames/internet/hosts.svg`                        |
| `computing-ipv6-share.json`                       | `subjects/computing/frames/ip-routing/ipv6-share.svg`                 |
| `computing-life-table-pages.json`                 | `subjects/computing/frames/scheutz-engine/life-table-pages.svg`       |
| `computing-multiplication-time.json`              | `subjects/computing/frames/edvac-report/multiplication-time.svg`      |
| `computing-newmanry-staff.json`                   | `subjects/computing/frames/heath-robinson/newmanry-staff.svg`         |
| `computing-root-sites.json`                       | `subjects/computing/frames/dns/root-sites.svg`                        |
| `computing-table-errors.json`                     | `subjects/computing/frames/difference-engine/table-errors.svg`        |
| `computing-top500-linux.json`                     | `subjects/computing/frames/linux/top500-linux.svg`                    |
| `computing-trajectory-time.json`                  | `subjects/computing/frames/differential-analyzer/trajectory-time.svg` |
| `computing-transistor-counts.json`                | `subjects/computing/frames/moores-law/transistor-counts.svg`          |
| `computing-tunny-reading-speed.json`              | `subjects/computing/frames/colossus-d-day/reading-speed.svg`          |
| `computing-web-sites.json`                        | `subjects/computing/frames/world-wide-web/sites.svg`                  |
| `dartmouth-budget.json`                           | `subjects/ai/frames/dartmouth/budget.svg`                             |
| `feynman-diagrams-per-order.json`                 | `subjects/feynman/frames/magnetic-moment/diagrams-per-order.svg`      |
| `feynman-glass-reflection.json`                   | `subjects/feynman/frames/qed-book/glass-reflection.svg`               |
| `feynman-ibm-problems.json`                       | `subjects/feynman/frames/punched-cards/problems-per-month.svg`        |
| `feynman-muon-gap.json`                           | `subjects/feynman/frames/path-integrals-today/muon-gap.svg`           |
| `feynman-o-ring-distress.json`                    | `subjects/feynman/frames/teleconference/o-ring-distress.svg`          |
| `feynman-plenty-citations.json`                   | `subjects/feynman/frames/plenty-of-room/citations.svg`                |
| `feynman-roton-gap.json`                          | `subjects/feynman/frames/superfluid-helium/roton-gap.svg`             |
| `feynman-rsa-qubits.json`                         | `subjects/feynman/frames/quantum-computing-now/rsa-qubits.svg`        |
| `feynman-shuttle-odds.json`                       | `subjects/feynman/frames/reliability/shuttle-odds.svg`                |
| `feynman-state-memory.json`                       | `subjects/feynman/frames/simulating-physics/state-memory.svg`         |
| `feynman-trinity-yield.json`                      | `subjects/feynman/frames/trinity/yield-estimates.svg`                 |
| `feynman-wobble-ratio.json`                       | `subjects/feynman/frames/wobbling-plate/wobble-ratio.svg`             |
| `ilsvrc-top5.json`                                | `subjects/ai/frames/alexnet/ilsvrc-top5.svg`                          |
| `metr-time-horizons.json`                         | `subjects/ai/frames/capability-evals/time-horizons.svg`               |
| `mnist-2006.json`                                 | `subjects/ai/frames/deep-belief-nets/mnist-error.svg`                 |
| `model-parameters.json`                           | `subjects/ai/frames/pretraining/model-parameters.svg`                 |
| `physics-carnot-efficiency.json`                  | `subjects/physics/frames/carnot/efficiency.svg`                       |
| `physics-cmb-resolution.json`                     | `subjects/physics/frames/cmb/resolution.svg`                          |
| `physics-coulomb-g-uncertainty.json`              | `subjects/physics/frames/coulomb/g-uncertainty.svg`                   |
| `physics-dark-energy-significance.json`           | `subjects/physics/frames/dark-energy/significance.svg`                |
| `physics-de-broglie-wavelengths.json`             | `subjects/physics/frames/de-broglie/wavelengths.svg`                  |
| `physics-expanding-universe-hubble-constant.json` | `subjects/physics/frames/expanding-universe/hubble-constant.svg`      |
| `physics-falling-bodies-odd-numbers.json`         | `subjects/physics/frames/falling-bodies/odd-numbers.svg`              |
| `physics-fission-countdown.json`                  | `subjects/physics/frames/fission/countdown.svg`                       |
| `physics-fusion-nif-yields.json`                  | `subjects/physics/frames/fusion/nif-yields.svg`                       |
| `physics-general-relativity-deflection.json`      | `subjects/physics/frames/general-relativity/deflection.svg`           |
| `physics-gravitational-waves-catalogue.json`      | `subjects/physics/frames/gravitational-waves/catalogue.svg`           |
| `physics-landauer.json`                           | `subjects/physics/frames/landauer/energy-per-bit.svg`                 |
| `physics-manhattan-costs.json`                    | `subjects/physics/frames/manhattan-project/costs.svg`                 |
| `physics-quantum-mechanics-interpretations.json`  | `subjects/physics/frames/quantum-mechanics/interpretations.svg`       |
| `physics-solids-resistivity.json`                 | `subjects/physics/frames/solids/resistivity.svg`                      |
| `physics-standard-model-energies.json`            | `subjects/physics/frames/standard-model/beam-energy.svg`              |
| `physics-superconductivity-tc.json`               | `subjects/physics/frames/superconductivity/critical-temperatures.svg` |
| `sae-dictionary-size.json`                        | `subjects/ai/frames/interpretability/dictionary-size.svg`             |
| `temperature.json`                                | `subjects/ai/frames/next-token/temperature.svg`                       |
| `tokens-per-parameter.json`                       | `subjects/ai/frames/scaling-laws/tokens-per-parameter.svg`            |
| `training-compute.json`                           | `subjects/ai/frames/compute/training-compute.svg`                     |
| `turing-storage.json`                             | `subjects/ai/frames/turing-test/turing-storage.svg`                   |

`test_bar_chart.py` checks the fit rules and that every spec in
`examples/` passes them (`just check` runs it).

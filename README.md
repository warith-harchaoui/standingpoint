# Standpoint

Know where each option stands.

Standpoint reads a comparison table (options as rows, criteria as columns, numbers
in the cells) and produces a 2D positioning map, a short written analysis, and a
YAML file with all the coordinates and coefficients. One command does it.

The method is ordinary PCA, which people have used for perceptual maps for a long
time. What Standpoint adds is the work you would otherwise do by hand: it orients
the map around a reference option, names the axes in plain words (in the language
of your columns), colours and labels the points, and writes everything out.

## What you get

Input: a table of options and their ratings.

| Language | Performance | Ease of Learning | Ecosystem | Concurrency | Type Safety | Job Market | Tooling |
|---|---|---|---|---|---|---|---|
| Python | 2 | 5 | 5 | 2 | 2 | 5 | 4 |
| Rust | 5 | 2 | 3 | 5 | 5 | 3 | 4 |
| Go | 4 | 4 | 4 | 5 | 4 | 4 | 4 |
| JavaScript | 3 | 4 | 5 | 3 | 2 | 5 | 3 |
| … | | | | | | | |

Output: a positioning map,

![Programming languages positioning map](https://raw.githubusercontent.com/warith-harchaoui/standpoint/main/examples/programming_languages.png)

plus a Markdown analysis (what the axes mean, where the reference wins, which groups
stand out, with the loadings and a ranking) and a YAML file with every option's
coordinates, role, colour, and original values.

## Install and run

```bash
pip install -e .          # or: pip install -r requirements.txt
standpoint examples/sidekick_landscape.csv --outdir out
# without installing: python3 -m standpoint examples/sidekick_landscape.csv --outdir out
```

Two equivalent CLIs are installed: `standpoint` (argparse) and `standpoint-click`.

As a library:

```python
import standpoint as sp
sp.positioning("examples/sidekick_landscape.csv").export("out")
```

More in [EXAMPLES.md](https://github.com/warith-harchaoui/standpoint/blob/main/EXAMPLES.md).

Axis names and the written analysis need a local [Ollama](https://ollama.com)
model (default `qwen2.5vl:7b`, which also checks the figure when you pass
`--check`). Without it, use `--no-llm`: you still get the map, with axis names
taken from the strongest column at each end and no written analysis.

```bash
standpoint my_table.csv --no-llm
standpoint my_table.csv --model qwen3:8b
```

## Input format

A CSV or Markdown table. The first column holds the option names; the rest are
numeric criteria on any scale. Higher means better. Empty cells are filled with
the column's minimum, so a missing rating never helps an option.

| Language | Performance | Ease of Learning | Ecosystem | Type Safety | Job Market |
|---|---|---|---|---|---|
| Python | 2 | 5 | 5 | 2 | 5 |
| Rust | 5 | 2 | 3 | 5 | 3 |
| Go | 4 | 4 | 4 | 4 | 4 |

The first row is the reference and goes to the top right. Change it with
`--reference "<name>"`. Mark a lower-is-better column with `(↓)`, e.g.
`Price (↓)`, or list it in `--lower`.

## How it works

1. Standardize each criterion to mean 0 and standard deviation 1. PCA is sensitive
   to scale, so this puts every criterion on equal footing.
2. Run PCA and keep two components. The axes stay as weighted sums of the original
   columns, so you can read them.
3. Rotate the map so the reference sits top right. If the reference scores top
   marks on everything, it is placed just past the best competitor on each axis
   rather than far off on its own.
4. Label it. Roles (best, worst, most innovative, most trustworthy) come from
   projections in the standardized space. Each option takes its own colour from its
   position. A local model reads the loadings and names the four axis ends, as
   positive qualities, in your columns' language (English, French, or Spanish).

The figure keeps to a dotted cross for the axes, the pole words at the ends, labels
only where they fit, and a legend for the rest.

![Electric cars, French input gives French axis names](https://raw.githubusercontent.com/warith-harchaoui/standpoint/main/examples/voitures_electriques.png)

## Notes

- Axis names come from a local model. A guard keeps them positive, distinct, and
  free of acronyms; a larger `--model` helps, and `--check` asks the vision model
  whether the figure reads correctly.
- Higher is better by default. For a column where lower is better, mark its header
  with `(↓)` (`Price (↓)`, `Latency (↓)`) or pass `--lower Price,Latency`. Standpoint
  negates it and names the pole for the benefit ("Affordable", "Portable"), never
  the drawback.
- It is a 2D projection. The axes carry a stated fraction of the variance, so read
  it as a summary rather than the whole picture.

## Examples

Tracked in `examples/`, input CSV and generated figures:

| Table | Language | Leader |
|---|---|---|
| `sidekick_landscape.csv` | en | Sidekick (contact-centre voice AI) |
| `programming_languages.csv` | en | Python |
| `cloud_providers.csv` | en | AWS |
| `laptops.csv` | en | MacBook Air (uses `Price (↓)` / `Weight (↓)`) |
| `voitures_electriques.csv` | fr | Tesla Model 3 |

## Development

```bash
pip install -r requirements-dev.txt
python3 -m pytest tests/ -q       # deterministic tests; model-backed ones auto-skip
python3 -m ruff check .
```

## Credits

PCA perceptual maps are standard (`factoextra` and `FactoMineR` in R, `prince` and
`pca` in Python); using a model to read the components is a newer idea. Colours
come from the ["Good Colors"](https://harchaoui.org/warith/colors/) palette.
Figures are rendered by [`vl-convert`](https://github.com/vega/vl-convert) over
[Vega-Lite](https://vega.github.io/vega-lite/).

## Author

[Warith Harchaoui](https://www.linkedin.com/in/warith-harchaoui)

## License

BSD 3-Clause, the same license as scikit-learn. See
[`LICENSE`](https://github.com/warith-harchaoui/standpoint/blob/main/LICENSE).

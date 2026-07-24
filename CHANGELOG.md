# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.0] - 2026-07-24

### Added

- **Joined the [AI Helpers](https://harchaoui.org/warith/ai-helpers) suite** (Misc
  group): suite framing + logo in the README/LISEZMOI, a canonical Documentation
  section, and a self-referential positioning map wired into `LANDSCAPE.md` /
  `PAYSAGE.md` from the committed `assets/landscape.csv` / `paysage.csv` source.
- **First PyPI release** (`pip install standpoint`); README/LISEZMOI use absolute
  URLs so they render on the PyPI project page.

### Changed

- **Highlighted roles are now domain-agnostic.** The two extra highlights used to be
  chosen with a fixed keyword list carried over from an early voice-AI example, so on
  a generic table they degraded to an arbitrary pick. They are now read straight off
  the map geometry: the leader, the weakest overall, and the two challengers reaching
  furthest toward the **top** and **right** poles ("strongest toward `<pole>`"). The
  corresponding CLI overrides were renamed `--innovative`/`--trustworthy` →
  `--top`/`--right`, and `positioning(innovative=, trustworthy=)` → `top=`/`right=`.
- **The figure title is fully localized.** A French table now reads
  *Voitures dans le quadrant* (and Spanish *… en el cuadrante*) instead of keeping the
  English connector. Driven by a per-language `title_template` in `i18n.yaml`.

### Added

- **Two figure backgrounds per run.** Every render now writes a **transparent**
  `<name>.png` / `.svg` (default, drops onto any page) *and* a white-background
  `<name>.white.png` / `.white.svg` (for dark surfaces where the near-black labels
  would vanish on transparency). The `--check` vision self-assessment runs against a
  white-composited render (`png_on_white`) so transparency can't fool it.
- Bilingual documentation: reworked `README.md` and a French `LISEZMOI.md`, plus this
  `CHANGELOG.md`, a `CONTRIBUTING.md`, and the repository `CODING.md`.
- A competitive positioning map of the tool itself in `LANDSCAPE.md` / `PAYSAGE.md`,
  rendered by Standpoint (dogfooding).
- Continuous integration (`.github/workflows/ci.yml`): ruff lint + format check and a
  pytest matrix on Python 3.10–3.13.
- An optional DeepEval evaluation of pole-naming quality (`tests/test_eval.py`),
  auto-skipped when Ollama or the model is unavailable.
- Explicit ruff configuration in `pyproject.toml` (line length 100, target py310,
  a conservative lint set); the package is now `ruff check` and `ruff format` clean.

### Fixed

- Library diagnostics go through the `logging` module instead of a bare `print`.
- Numpydoc docstrings and full type annotations on every private and nested function.

## [0.1.0] - 2026-07-23

### Added

- Initial public release. From one comparison table (`options × criteria`, CSV or
  Markdown, numeric ratings on any scale), Standpoint produces a three-fold
  deliverable in one command:
  - a **figure** — a labelled 2D positioning map (PNG + SVG + Vega-Lite JSON), the
    reference option rotated to the top-right, de-cluttered labels, full legend;
  - a **Markdown** interpretation (axes, where the leader wins, standout options,
    loadings, ranking);
  - a **YAML** dump of every option's coordinates, role, colour, and original values,
    plus axis loadings and variance.
- Correlation PCA (z-score standardization) with the axes kept as readable weighted
  sums of the criteria.
- Local-LLM axis-pole naming (default `qwen2.5vl:7b`) in the table's own language
  (English, French, Spanish), with a guard enforcing positive, distinct, acronym-free
  labels; deterministic `--no-llm` fallback.
- Per-column polarity: lower-is-better criteria via a `(↓)` header marker or `--lower`.
- Optional `--check` vision self-assessment of the rendered figure.
- Two console commands (`standpoint`, `standpoint-click`) and a `positioning()`
  library API returning a `Positioning` object.

[Unreleased]: https://github.com/warith-harchaoui/standingpoint/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/warith-harchaoui/standingpoint/releases/tag/v0.1.0

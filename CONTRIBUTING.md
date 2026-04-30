# Contributing

Thanks for your interest in contributing. This project is a public Quarto site documenting cloud-native resampling and reprojection in Python, with memory and time benchmarks for a growing set of libraries and an ecosystem overview at `pages/ecosystem.qmd`.

Contributions are welcome — new benchmarks, new tools to profile, corrections, clearer framing, or additions to the roadmap.

## Before you start

- Read the **[Ecosystem & Roadmap](./pages/ecosystem.qmd)** page to understand the scope of the site and where your contribution fits. It organizes the landscape by mathematical family (F1 kernel convolution, F2 scattered-data, F3 conservative, F4 statistical aggregation, F5 mesh) and by architectural layer.
- Check existing [issues](https://github.com/developmentseed/warp-resample-profiling/issues) and [pull requests](https://github.com/developmentseed/warp-resample-profiling/pulls) to avoid duplication.
- For anything larger than a typo fix, open an issue first to discuss scope.

## Ways to contribute

### Report an issue
Found a bug in a notebook, an outdated link, a claim that doesn't match evidence, or something unclear? Open an issue with a reproducible description.

### Propose a new benchmark
The Ecosystem page's **§5 Roadmap** lists the highest-leverage additions (Tier 1: F3 conservation with a conservation-error metric; categorical downsample with class-frequency divergence; correctness as a first-class metric). Contributions in those tiers are especially welcome.

To add a benchmark:
1. Open an issue describing the scenario, the tool(s), the dataset, and the metric(s) you plan to measure.
2. Discuss scope and framing before writing code — the site aims to stay cited correctly, so scoping matters.
3. Follow the [Adding a new benchmark](#adding-a-new-benchmark) checklist.

### Propose an ecosystem entry or roadmap update
Noticed a library missing from `ecosystem.qmd`? A family variant unrepresented? A citation you think would strengthen the site? Open a PR editing `pages/ecosystem.qmd` directly, or file an issue if you'd rather discuss first.

### Fix documentation
Typo, dead link, confusing sentence — open a PR. No issue required.

### Extend or refine the coverage matrix
The `§6 Coverage matrix` in `ecosystem.qmd` lists tools × families with current status (benchmarked / exists / out of scope). If you know the current state better than the matrix reflects, PRs to update it are welcome.

## Development setup

### Reproducible environment (recommended)

The notebooks can be run using the Docker image `quay.io/developmentseed/warp-resample-profiling:latest`, built via `repo2docker` from the Dockerfile in `binder/`.

```bash
# Using repo2docker directly
pip install jupyter-repo2docker
jupyter-repo2docker https://github.com/developmentseed/warp-resample-profiling
```

Or launch on [mybinder.org](https://mybinder.org/v2/gh/developmentseed/warp-resample-profiling/main) for a hosted session.

### Local setup

```bash
git clone https://github.com/developmentseed/warp-resample-profiling.git
cd warp-resample-profiling
uv sync  # or: pip install -e .
```

Dependencies are declared in `pyproject.toml`.

### Building the Quarto site locally

[Install Quarto](https://quarto.org/docs/get-started/), then:

```bash
quarto preview    # live reload on local changes
quarto render     # one-off render to _site/
```

The rendered site appears in `_site/`. Navigate to any page via the sidebar or direct URL.

## Adding a new benchmark

### 1. Pick a notebook name that follows the existing convention

Benchmark notebooks in `examples/` follow `resample-<input-format>-<library>-<reader>-<storage>.ipynb`. Examples:
- `resample-netcdf-rioxarray-h5netcdf-local.ipynb`
- `resample-netcdf-odc-zarr-icechunk.ipynb`
- `resample-cog-rasterio-cog-.ipynb` (empty storage segment means "not specified")

Keep the convention so the sidebar stays scannable and the results pages can group notebooks correctly.

### 2. Include profiling hooks

Every benchmark notebook captures both time and memory. The standard pattern:

- Wall time via `time.perf_counter()` before/after the resampling call.
- Peak heap memory via `memray` or `pyinstrument` (see existing notebooks for the pattern).
- Results written to a Parquet file that `examples/process-results.ipynb` or `examples/process-gpm-results.ipynb` can aggregate.

Look at an existing notebook in `examples/` as a template. Match the output schema so the summary notebooks can consume it.

### 3. Report correctness, not just performance

If you're adding a scenario in Tier 1 (F3 conservation, categorical, etc.), report a correctness metric alongside time and memory:

- **Conservation scenarios**: `|Σ input·area − Σ output·area| / Σ input·area` as a conservation-error fraction.
- **Categorical scenarios**: class-frequency histogram divergence (KL or simple L1) vs. a scale-aware reference.
- **Continuous scenarios**: MAE / RMSE vs. a high-quality reference (e.g., GDAL warp with Lanczos).
- **Smooth reprojection**: gradient-magnitude artifacts vs. input.

Time without correctness is misleading for anything outside F1 kernel convolution on continuous data.

### 4. Add the notebook to the sidebar

Edit `_quarto.yml` to register the notebook in the appropriate `section:`. Keep it grouped with peers (same library or same scenario class).

### 5. Document scope honestly

In the notebook's markdown cells, state:
- What family the resampling falls under (F1, F3, F4 within-cell, F4 point-to-cell, …).
- What correctness metric you're reporting, if any.
- What this benchmark cannot claim (be narrow about the conclusion).

This keeps the site easy to cite correctly — see `ecosystem.qmd` §8.

## Adding an ecosystem entry or tool

### New tool in the coverage matrix

1. Add a row to `pages/ecosystem.qmd` §6 with the tool name and cell status per family (✅ benchmarked / 🟡 exists / — out of scope).
2. Add a reference entry to §9, grouped by layer (native-grid I/O, loader + read-time warp, grid math, etc.).
3. If a benchmark for the tool is planned, add a line to §5 Tier 2 (or the appropriate tier).

### New reference or discussion

§9 has categories for ecosystem discussions, layer-based project lists, and standards. Pick the nearest fit; open an issue if no category fits.

### Update an SVG

Diagrams live in `pages/assets/`:
- `resampling_families.svg` — the 5-family taxonomy.
- `resampling_ecosystem.svg` — layered architecture with tool placement.

Edit the SVG source directly (they're hand-authored, not generated). Keep a consistent style; if a significant restructure is needed, open an issue first.

## Style and conventions

### Quarto / Markdown
- Match the tone of existing pages — precise, factual, tradeoff-aware.
- Prefer tables over long bulleted lists where structure helps.
- Link inline rather than via footnotes.
- Use sentence case for headings.

### Python
- Lint via `ruff` / format via `ruff format` if you're adding Python files outside notebooks.
- Keep notebook cells focused; one operation per cell where reasonable.
- Use explicit imports (`from rasterio.warp import reproject`) over `import *`.

### Citations and scope
When describing a tool's performance, stay within the scope actually measured. A tool being fast in the benchmark's narrow scope is not a claim about general fitness. `ecosystem.qmd` §8 has guidance that applies equally to PR prose.

## Reporting security issues

If you find a security issue in the profiling infrastructure or Docker image, please do not open a public issue. Contact the maintainers privately via the email in the repo owner's GitHub profile.

## Code of conduct

Be professional, be specific, and assume good intent. Technical disagreements are welcome; personal attacks are not. If someone's behavior in issues or PRs makes the project worse, flag it to the maintainers.

## License

By contributing, you agree that your contributions will be licensed under the project's existing license (see `LICENSE` at the repo root).

## Acknowledgements

Thanks to all contributors listed in the [README acknowledgements](./README.md#acknowledgements), and to everyone who opens issues, files PRs, or shares framing that sharpens the site.

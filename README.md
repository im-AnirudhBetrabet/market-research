# market-research

A small research codebase for exploring market signals (NIFTY / SENSEX) and related features, correlations and simple strategy validation. The project collects raw market data, builds aligned and feature datasets, runs correlation and lag analyses, and generates plots and markdown reports.

This README documents repository layout, setup, common workflows, key scripts and modules, and tips for contributing.

---

## Quick start

Prerequisites:

- Python 3.10+ (this repo was developed with CPython 3.10+ / 3.11+)
- Git (optional, for cloning)

Install dependencies:

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Run an end-to-end minimal workflow (assumes raw CSVs are present in `data/raw`):

```powershell
# ingest or place raw data into data/raw, then:
python .\scripts\build_aligned_dataset.py
python .\scripts\build_feature_dataset.py
python .\scripts\run_correlation_analysis.py
```

See the `scripts/` section below for more options.

---

## Repository layout

Top-level:

- `data/`
  - `raw/` - original ingested CSVs (gitignored in normal workflows)
  - `processed/` - cleaned, aligned, and feature CSV outputs
- `notebooks/` - exploratory notebooks (data validation, correlation, feature engineering, baseline models, strategy validation)
- `src/` - main python source package
- `scripts/` - convenience scripts to run common tasks (ingest, build datasets, run analyses)
- `charts/` - generated output charts
- `reports/` - generated markdown research reports
- `tests/` - unit/integration tests (add tests here)

A concise tree (important files):

```
README.md
requirements.txt
scripts/
    ingest_data.py
    build_aligned_dataset.py
    build_feature_dataset.py
    build_features.py
    run_correlation_analysis.py
    run_correlation.py
src/
    ingestion/
    features/
    analytics/
    visualization/
    reporting/
    research/
    domain/
    common/
notebooks/
data/
charts/
reports/
```

---

## Data layout and expected CSVs

- `data/raw/` expected inputs (examples present in this repo):
  - `gift_nifty.csv` - (GIFT / NIFTY mapping data used for special features)
  - `nifty.csv` - NIFTY market prices / OHLC
  - `sensex.csv` - SENSEX market prices / OHLC
  - `india_vix.csv` - VIX / volatility series

- `data/processed/` outputs produced by scripts:
  - `aligned_dataset.csv` - market series aligned by date, used for analysis
  - `feature_dataset.csv` - dataset with engineered features ready for modeling

If you obtain fresh raw data, place the CSVs into `data/raw/` and run the ingest / build scripts.

---

## Key scripts

All scripts are runnable directly with Python from the repo root. Examples below use PowerShell-style paths on Windows.

- `scripts/ingest_data.py` - helper to ingest and normalize raw CSVs (if present)
- `scripts/build_aligned_dataset.py` - creates `data/processed/aligned_dataset.csv` by aligning time series and filling/validating
- `scripts/build_feature_dataset.py` - generates `data/processed/feature_dataset.csv` by applying feature builders
- `scripts/build_features.py` - lower-level feature creation utilities (invokes `src/features` modules)
- `scripts/run_correlation_analysis.py` - runs the correlation & lag analysis and writes charts to `charts/`
- `scripts/run_correlation.py` - lighter-weight correlation runner used by notebooks and experiments

Run any script:

```powershell
python .\scripts\build_aligned_dataset.py
```

If you prefer to run via the package (recommended for development to get import behavior consistent):

```powershell
python -m src.scripts.build_aligned_dataset
```

(Adjust module path if you use a different import layout.)

---

## Main modules (src)

High-level overview of packages under `src/`:

- `src.ingestion` - loaders and base classes to read CSVs and external sources. Key modules:
  - `csv_market_loader.py` - CSV loader utilities
  - `gift_nifty_loader.py` - loader for GIFT vs NIFTY data
  - `yfinance_loader.py` - helper to fetch data from yfinance (if configured)

- `src.features` - feature engineering code
  - `feature_builder.py` - orchestrates feature construction
  - `gift_features.py` / `nifty_features.py` - domain-specific feature functions

- `src.analytics` - analysis engines
  - `correlation_engine.py` - computes correlation matrices and summaries
  - `lag_analysis_engine.py` / `lag_analysis.py` - analyze lagged relationships between series
  - `bucket_analysis_engine.py`, `directional_analysis_engine.py` - additional analysis utilities
  - `statistics.py` - helpers for statistical summaries

- `src.reporting` - report builder to write markdown summaries (`markdown_report_builder.py`)

- `src.visualization` - plotting utilities (write charts into `charts/`)

- `src.research` - dataset builders and experiment orchestration (`aligned_dataset.py`, `dataset_builder.py`)

- `src.domain` - domain models and enums (`models.py`, `enums.py`)

- `src.common` - constants and shared exceptions

- `src.pipelines` - high-level pipeline definitions (a minimal pipeline exists in `market_data_pipeline.py`)

Review individual modules for more details; the code is organized with small, testable components.

---

## Notebooks

The `notebooks/` directory contains exploratory analysis and example flows:

- `01_data_validation.ipynb` - checks and data quality validation
- `02_correlation_analysis.ipynb` - interactive correlation / lag exploration
- `03_feature_engineering.ipynb` - feature building and visualization
- `04_baseline_models.ipynb` - simple baseline model experiments
- `05_strategy_validation.ipynb` - simulated strategy backtests and validation

Open notebooks with Jupyter/Lab:

```powershell
pip install jupyterlab
jupyter lab
```

---

## Running tests

This repo includes a `tests/` directory. If you add tests, run them with pytest:

```powershell
pip install pytest
pytest -q
```

Add unit tests for modules under `src/` to keep behavior stable.

---

## Development tips

- Use the package import style (add the project root to PYTHONPATH or install in editable mode) while developing to avoid import errors:

```powershell
# from project root
pip install -e .
# or
$env:PYTHONPATH = (Resolve-Path .).Path; python -m pytest
```

- Use virtual environments to keep dependencies isolated.
- Keep raw data out of version control; store only derived/summary outputs or sample CSVs.

---

## Adding datasets or features

- Place new raw CSVs in `data/raw/` and update or extend the loaders in `src/ingestion` if file format differs.
- Update `src/features/feature_builder.py` to register new feature groups and add tests for new feature logic.

---

## Troubleshooting

- If imports fail when running scripts, ensure your current working directory is the repository root and your venv is active.
- If a script fails due to missing columns, inspect the raw CSV and the corresponding loader in `src/ingestion`.

---

## Contributing

Contributions are welcome. Suggested workflow:

1. Fork and create a feature branch
2. Add tests for behavioral changes
3. Run tests and format code (optionally using black / flake8 if added)
4. Open a PR describing the change

---
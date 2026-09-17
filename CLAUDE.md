# CLAUDE.md

## Project
INF601 Mini Project 3 — a small data-science exercise built with TDD, using Pandas
for all data work and Matplotlib for the final visualization.

## Dataset
Source file: `data/spotify_ds.csv` (gitignored — not committed, too large).
Columns: `track_id, spotify_id, title, track_artist, release_year, loudness, mode_name`

`mode_name` is a string column — either "major" or "minor"
## Question
Has music shifted toward louder, more major-key-dominant sound over time?

## Pipeline (two stages — keep them separate)

### Stage 1: Preprocessing (produces the committed sample file)
1. Load `data/spotify_ds.csv`.
2. Derive `decade = (release_year // 10) * 10`.
3. Group by decade. Sample `min(len(group), 5000)` rows per decade — do not assume
   every decade has ≥5000 rows; that assumption will silently break on sparse decades.
4. Use a fixed `random_state` for reproducibility (tests will assert on this).
5. Drop any decade bucket with fewer than ~100 rows post-sample and log a warning —
   too few rows to trust a decade mean.
6. Write result to `data/spotify_sample.csv` (this file IS committed — it's the
   truncated version for repo transport / automated grading, per the assignment's
   "no manual download step" constraint).

### Stage 2: Analysis + chart (runs against the committed sample, every time)
1. Load `data/spotify_sample.csv`.
2. Group by decade: mean `loudness`, and `% major` (share of `mode_name == 'major'`
   per decade — confirm exact string value first).
3. Plot: one figure, twin y-axis line chart. Left axis = % major mode, right axis =
   mean loudness, x-axis = decade.
4. Save to `charts/loudness_mode_trend.png` (charts/ is gitignored — generated on
   run, per rubric, never committed).

## TDD strategy
Test the transformation functions, not the plot. Specifically, write tests for:
- decade bucketing (`year -> decade`) on boundary years (e.g. 1970, 1979, 1980)
- per-decade sampling respects the `min(len(group), 5000)` cap and is reproducible
  given the same `random_state`
- the "is major" flag / percent-major calculation, including a decade with 0% and
  100% major as edge cases
- the final aggregation (mean loudness, % major per decade) against a small
  hand-built fixture DataFrame with known expected output

- logfile.txt is a constantly appended file for test runs and modifications. Append to it when told to.

Do NOT write a test that asserts on the PNG's pixel content or tries to snapshot
the chart. Instead, optionally assert the figure was created with two axes and
non-empty data — that's the ceiling of what's meaningfully testable here.

## Environment
This project uses a Python venv at `./.venv`. Before running any Python command
(scripts, tests, pip installs), activate it:
    source .venv/bin/activate
Do not install packages globally or use system Python.

## File structure
miniproject3/
├── data/
│   ├── spotify_ds.csv          # gitignored, full source, not committed
│   └── spotify_sample.csv      # committed, truncated, used by the analysis script
├── charts/                      # gitignored, generated on run
├── tests/
│   └── test_pipeline.py
├── preprocess.py                # Stage 1
├── main.py        # Stage 2, entry point, has required header comment
├── requirements.txt
├── .gitignore
└── README.md
logfile.txt

README.md starts as a copy of a previous projects README to maintain structure. 

## Non-negotiables from the assignment rubric
- Header comment block in the main .py file: name, class ("INF601 - Advanced
  Programming in Python"), "Mini Project 3"
- `requirements.txt` present and accurate
- `charts/` in `.gitignore`, PNG generated fresh on every run
- README includes install/run steps and an `## AI Usage` section. Update the version changes per-commit. 
- At least 5 commits — commit incrementally per stage/feature, not as one dump. This is done by writing test, verifying test, completing test being each of its own commits

## Data Atttribution

Make sure that README has a data section that includes the following:

data/spotify_sample.csv is a derivative of [Spotify Music Features Dataset](https://www.kaggle.com/datasets/amith1707/spotify-music-features-dataset) itself source from [TidyTuesday 2020-01-21 Spotify Data](https://github.com/rfordatascience/tidytuesday/tree/main/data/2020/2020-01-21). Licensed under the ODC Open Database License (ODbL) v1.0 -- see LICENSE-DATA.txt 

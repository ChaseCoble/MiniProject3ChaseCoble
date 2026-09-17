### INF601 - Advanced Programming in Python
### Chase Coble
### Mini Project 3


# Loudness & Major-Key Trend Analysis

## Description

A small Pandas + Matplotlib data-science exercise, built test-first (TDD), that
asks: **has music shifted toward louder, more major-key-dominant sound over
time?** The pipeline is split into two stages — a preprocessing step that
buckets tracks into decades and samples them down to a committed CSV, and an
analysis step that aggregates that sample and plots a twin-axis line chart of
mean loudness and percent-major-mode by decade.

**Answer:** No — at least not in this sample. Mean loudness and percent-major
zig-zag from decade to decade (loud/quiet/loud/quiet) rather than trending in
either direction, and re-running the sampling step with a different
`random_state` reproduces the same up-and-down pattern for most decades. There's
no evident relationship between decade and either loudness or major-key
dominance here — the data doesn't support the "louder and more major over time"
hypothesis.

## Getting Started

### Dependencies

* Python 3
* pandas
* matplotlib
* pytest

See `requirements.txt` for exact pinned versions.

## Installing

1. Clone the repository:
   ```bash
   git clone https://github.com/<your-username>/miniproject3ChaseCoble.git
   cd miniproject3ChaseCoble
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate    # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Executing program

`data/spotify_sample.csv` is already committed, so the analysis stage runs
out of the box with no manual download step:

```bash
python main.py
```

This loads the committed sample, aggregates mean loudness and percent-major
mode by decade, and saves a twin-axis line chart to
`charts/loudness_mode_trend.png` (regenerated fresh on every run).

Regenerating `data/spotify_sample.csv` itself (Stage 1) requires the full,
gitignored source dataset at `data/spotify_ds.csv`, which is not included in
this repo:

```bash
python preprocess.py
```

Run the test suite with:

```bash
pytest
```

## Data

`data/spotify_sample.csv` is a derivative of the
[Spotify Music Features Dataset](https://www.kaggle.com/datasets/amith1707/spotify-music-features-dataset),
itself sourced from the
[TidyTuesday 2020-01-21 Spotify Data](https://github.com/rfordatascience/tidytuesday/tree/main/data/2020/2020-01-21).
Licensed under the ODC Open Database License (ODbL) v1.0 — see
`LICENSE-DATA.txt`.

## Authors

Chase Coble

## Version History

* 1.0
    * README completed with findings; full test suite green (16 tests)
* 0.9
    * Stage 2 plotting function implemented; chart generation verified end-to-end
* 0.8
    * load_and_aggregate implemented in main.py; Stage 2 ingestion tested
* 0.7
    * Sample parameters tuned: 1950/1960/1970 excluded, per-decade cap set to 1000
* 0.6
    * Stage 1 orchestration wired up in preprocess.py (runnable end-to-end)
* 0.5
    * Test written and implementation completed for final aggregation
      (mean loudness + percent-major by decade)
* 0.4
    * Test written and implementation completed for is_major / percent_major_by_decade
* 0.3
    * Test written and implementation completed for sample_by_decade
      (pivoted off groupby().apply() after a pandas 3.0 behavior change)
* 0.2
    * Test written and implementation completed for year_to_decade boundary cases
* 0.1
    * Initial project scaffold: CLAUDE.md, file structure, requirements.txt

## License

* This project is unlicensed. The bundled data sample is licensed separately
  under ODbL v1.0 — see the Data section above.

## Acknowledgements

* [Pandas documentation](https://pandas.pydata.org/docs/)
* [Matplotlib documentation](https://matplotlib.org/stable/index.html)

## AI Usage

* Claude Code used throughout in a strict test-first loop: tests were written
  and confirmed red before any implementation, then implementations were
  written to turn them green. Claude also wired up the Stage 1/Stage 2
  orchestration scripts, diagnosed a pandas 3.0 `groupby().apply()` behavior
  change during the `sample_by_decade` implementation, and ran ad-hoc
  comparisons across different `random_state` values to sanity-check whether
  the loudness/major-mode trend was a real signal or sampling noise.

### Human Contributions

* Wrote and iterated on `CLAUDE.md` itself — the pipeline spec, the TDD
  strategy, the `logfile.txt` requirement and its exact append syntax, and
  the correction that expected/red-step test failures should not be logged.
* Directed the TDD workflow turn-by-turn: decided which function got tests
  written next (decade bucketing, per-decade sampling, is-major/percent-major,
  final aggregation, then the `main.py` ingestion and plotting functions), and
  gated each implementation on reviewing the red step first.
* Diagnosed the manual-run test failures firsthand and reported the exact
  symptoms (cache permission issue, then a `ModuleNotFoundError`) that led to
  the `pytest.ini` fix.
* Made the analysis judgment calls: chose to exclude the 1950s/1960s/1970s
  decades and set the per-decade sample cap to 1000 for compute savings,
  flagged the resulting chart as "dodgy," and requested the second
  `random_state` run used to tell real signal from sampling noise.
* Reviewed and directed every README revision, including requiring this
  section.

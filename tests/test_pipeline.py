# Chase Coble
# INF601 - Advanced Programming in Python
# Mini Project 3

import pandas as pd
import pytest

from main import load_and_aggregate
from preprocess import (
    aggregate_by_decade,
    is_major,
    percent_major_by_decade,
    sample_by_decade,
    year_to_decade,
)


@pytest.mark.parametrize(
    "year, expected_decade",
    [
        (1970, 1970),  # start of a decade
        (1979, 1970),  # end of a decade
        (1980, 1980),  # start of the next decade
        (1969, 1960),  # end of the prior decade
        (1999, 1990),  # end-of-decade boundary elsewhere in the range
        (2000, 2000),  # start-of-decade boundary elsewhere in the range
    ],
)
def test_year_to_decade_boundaries(year, expected_decade):
    assert year_to_decade(year) == expected_decade


def _make_decade_df(decade, n_rows):
    return pd.DataFrame(
        {
            "track_id": [f"{decade}-{i}" for i in range(n_rows)],
            "decade": decade,
        }
    )


def test_sample_by_decade_caps_large_group_at_5000():
    df = pd.concat(
        [_make_decade_df(1990, 5010), _make_decade_df(1950, 42)],
        ignore_index=True,
    )

    result = sample_by_decade(df, random_state=42)

    assert (result["decade"] == 1990).sum() == 5000


def test_sample_by_decade_keeps_all_rows_when_under_cap():
    small_decade = _make_decade_df(1950, 42)

    result = sample_by_decade(small_decade, random_state=42)

    assert len(result) == 42
    assert set(result["track_id"]) == set(small_decade["track_id"])


def test_sample_by_decade_is_reproducible_given_same_random_state():
    df = pd.concat(
        [_make_decade_df(1990, 5010), _make_decade_df(1950, 42)],
        ignore_index=True,
    )

    first = sample_by_decade(df, random_state=42)
    second = sample_by_decade(df, random_state=42)

    pd.testing.assert_frame_equal(
        first.sort_values("track_id").reset_index(drop=True),
        second.sort_values("track_id").reset_index(drop=True),
    )


@pytest.mark.parametrize(
    "mode_name, expected",
    [
        ("major", True),
        ("minor", False),
    ],
)
def test_is_major_flags_major_and_minor(mode_name, expected):
    assert is_major(mode_name) is expected


def _make_mode_df(decade, modes):
    return pd.DataFrame(
        {
            "decade": decade,
            "mode_name": modes,
        }
    )


def test_percent_major_by_decade_all_major_is_100_percent():
    df = _make_mode_df(1990, ["major", "major", "major"])

    result = percent_major_by_decade(df)

    assert result.loc[1990] == 1.0


def test_percent_major_by_decade_all_minor_is_0_percent():
    df = _make_mode_df(1950, ["minor", "minor"])

    result = percent_major_by_decade(df)

    assert result.loc[1950] == 0.0


def test_percent_major_by_decade_handles_multiple_decades_independently():
    df = pd.concat(
        [
            _make_mode_df(1990, ["major", "major", "major"]),
            _make_mode_df(1950, ["minor", "minor"]),
            _make_mode_df(1980, ["major", "minor"]),
        ],
        ignore_index=True,
    )

    result = percent_major_by_decade(df)

    assert result.loc[1990] == 1.0
    assert result.loc[1950] == 0.0
    assert result.loc[1980] == 0.5


def test_aggregate_by_decade_computes_mean_loudness_and_percent_major():
    df = pd.DataFrame(
        {
            "decade": [1980, 1980, 1990, 1990, 1990],
            "loudness": [-10.0, -8.0, -5.0, -7.0, -6.0],
            "mode_name": ["minor", "minor", "major", "major", "minor"],
        }
    )

    result = aggregate_by_decade(df)

    expected = pd.DataFrame(
        {
            "decade": [1980, 1990],
            "mean_loudness": [-9.0, -6.0],
            "percent_major": [0.0, 2 / 3],
        }
    )

    pd.testing.assert_frame_equal(
        result.sort_values("decade").reset_index(drop=True),
        expected,
    )


def test_load_and_aggregate_reads_csv_and_aggregates_by_decade(tmp_path):
    sample_path = tmp_path / "spotify_sample.csv"
    pd.DataFrame(
        {
            "decade": [1980, 1980, 1990, 1990, 1990],
            "loudness": [-10.0, -8.0, -5.0, -7.0, -6.0],
            "mode_name": ["minor", "minor", "major", "major", "minor"],
        }
    ).to_csv(sample_path, index=False)

    result = load_and_aggregate(sample_path)

    expected = pd.DataFrame(
        {
            "decade": [1980, 1990],
            "mean_loudness": [-9.0, -6.0],
            "percent_major": [0.0, 2 / 3],
        }
    )

    pd.testing.assert_frame_equal(
        result.sort_values("decade").reset_index(drop=True),
        expected,
    )

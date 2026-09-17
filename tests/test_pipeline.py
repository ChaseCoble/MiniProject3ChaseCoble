# Chase Coble
# INF601 - Advanced Programming in Python
# Mini Project 3

import pandas as pd
import pytest

from preprocess import sample_by_decade, year_to_decade


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

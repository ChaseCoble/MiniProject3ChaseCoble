# Chase Coble
# INF601 - Advanced Programming in Python
# Mini Project 3

import pytest

from preprocess import year_to_decade


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

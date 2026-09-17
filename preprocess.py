# Chase Coble
# INF601 - Advanced Programming in Python
# Mini Project 3

import logging

import pandas as pd

logger = logging.getLogger(__name__)

MIN_ROWS_PER_DECADE = 100
SAMPLE_SIZE = 1000
EXCLUDED_DECADES = {1950, 1960, 1970}
INPUT_PATH = "data/spotify_ds.csv"
OUTPUT_PATH = "data/spotify_sample.csv"


def year_to_decade(year):
    return (year // 10) * 10


def sample_by_decade(df, decade_col="decade", sample_size=5000, random_state=42):
    sampled_groups = [
        group.sample(n=min(len(group), sample_size), random_state=random_state)
        for _, group in df.groupby(decade_col, group_keys=False)
    ]
    return pd.concat(sampled_groups, ignore_index=True)


def is_major(mode_name):
    return mode_name == "major"


def percent_major_by_decade(df, decade_col="decade", mode_col="mode_name"):
    is_major_flags = df[mode_col].map(is_major)
    return is_major_flags.groupby(df[decade_col]).mean()


def aggregate_by_decade(df, decade_col="decade", loudness_col="loudness", mode_col="mode_name"):
    working = df.assign(_is_major=df[mode_col].map(is_major))
    return working.groupby(decade_col).agg(
        mean_loudness=(loudness_col, "mean"),
        percent_major=("_is_major", "mean"),
    ).reset_index()


def add_decade_column(df, year_col="release_year", decade_col="decade"):
    return df.assign(**{decade_col: df[year_col].map(year_to_decade)})


def drop_small_decades(df, decade_col="decade", min_rows=MIN_ROWS_PER_DECADE):
    counts = df[decade_col].value_counts()
    small_decades = counts[counts < min_rows].index
    for decade in sorted(small_decades):
        logger.warning(
            "Dropping decade %s: only %d rows after sampling (< %d minimum)",
            decade, counts[decade], min_rows,
        )
    return df[~df[decade_col].isin(small_decades)].reset_index(drop=True)


def drop_excluded_decades(df, decade_col="decade", excluded=EXCLUDED_DECADES):
    return df[~df[decade_col].isin(excluded)].reset_index(drop=True)


def preprocess(input_path=INPUT_PATH, output_path=OUTPUT_PATH, random_state=42, sample_size=SAMPLE_SIZE):
    df = pd.read_csv(input_path)
    df = add_decade_column(df)
    df = drop_excluded_decades(df)
    df = sample_by_decade(df, sample_size=sample_size, random_state=random_state)
    df = drop_small_decades(df)
    df.to_csv(output_path, index=False)
    return df


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    preprocess()

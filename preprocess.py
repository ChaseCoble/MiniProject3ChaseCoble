# Chase Coble
# INF601 - Advanced Programming in Python
# Mini Project 3

import pandas as pd


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

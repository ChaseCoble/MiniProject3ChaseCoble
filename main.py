# Chase Coble
# INF601 - Advanced Programming in Python
# Mini Project 3

import pandas as pd

from preprocess import aggregate_by_decade

SAMPLE_PATH = "data/spotify_sample.csv"


def load_and_aggregate(sample_path=SAMPLE_PATH):
    df = pd.read_csv(sample_path)
    return aggregate_by_decade(df)

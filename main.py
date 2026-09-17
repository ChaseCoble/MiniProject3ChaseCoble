# Chase Coble
# INF601 - Advanced Programming in Python
# Mini Project 3

import os

import matplotlib.pyplot as plt
import pandas as pd

from preprocess import aggregate_by_decade

SAMPLE_PATH = "data/spotify_sample.csv"
CHART_PATH = "charts/loudness_mode_trend.png"


def load_and_aggregate(sample_path=SAMPLE_PATH):
    df = pd.read_csv(sample_path)
    return aggregate_by_decade(df)


def plot_loudness_mode_trend(agg_df, output_path=CHART_PATH):
    agg_df = agg_df.sort_values("decade")

    fig, ax1 = plt.subplots()

    ax1.plot(agg_df["decade"], agg_df["percent_major"], color="tab:blue", marker="o")
    ax1.set_xlabel("Decade")
    ax1.set_ylabel("% Major Mode", color="tab:blue")
    ax1.tick_params(axis="y", labelcolor="tab:blue")

    ax2 = ax1.twinx()
    ax2.plot(agg_df["decade"], agg_df["mean_loudness"], color="tab:red", marker="s")
    ax2.set_ylabel("Mean Loudness (dB)", color="tab:red")
    ax2.tick_params(axis="y", labelcolor="tab:red")

    fig.suptitle("Loudness and Major-Key Trend by Decade")
    fig.tight_layout()

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fig.savefig(output_path)
    plt.close(fig)

    return fig


def main():
    agg_df = load_and_aggregate()
    plot_loudness_mode_trend(agg_df)


if __name__ == "__main__":
    main()

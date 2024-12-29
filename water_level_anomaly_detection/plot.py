import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import pandas as pd


plt.style.use("fivethirtyeight")


def plot_detection(df: pd.DataFrame) -> plt.Figure:

    fig, ax = plt.subplots(figsize=(11, 7))

    # Extract the date from the first timestamp to include in the legend or title
    date_str = df["timestamp"].dt.date.iloc[0].strftime("%Y-%m-%d")

    # Plot normal points
    ax.scatter(
        df["timestamp"][df["novelty"] == 1],
        df["value"][df["novelty"] == 1],
        label=f"Normal",
        c="blue",
        marker="o",
    )

    # Plot outliers
    ax.scatter(
        df["timestamp"][df["novelty"] == -1],
        df["value"][df["novelty"] == -1],
        label="Novelty",
        facecolors="none",
        s=100,
        edgecolors="red",
    )

    # Set x-axis to display hours, minutes, and seconds
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M:%S"))

    ax.set_xlabel("Timestamp (hh:mm:ss)")
    ax.set_ylabel("Value")
    ax.set_title(f"Novelty Detection Results on  {date_str}")
    ax.legend()
    ax.grid(True, which="both", linestyle="--", linewidth=0.5, alpha=0.7)

    plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
    plt.tight_layout(pad=2)

    return fig


def plot_reference_data(df: pd.DataFrame) -> plt.Figure:

    fig, ax = plt.subplots(figsize=(12, 7))

    date_str = df["timestamp"].dt.date.iloc[0].strftime("%Y-%m-%d")

    ax.plot(
        df["timestamp"],
        df["value"],
        "o-",
        label=f"Reference",
        color="#adad3b",
        linewidth=3,
    )

    ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M:%S"))

    ax.set_xlabel("Timestamp (hh:mm:ss)")
    ax.set_ylabel("Value")
    ax.set_title(f"Reference measurements on {date_str}")
    ax.legend()
    ax.grid(True, which="both", linestyle="--", linewidth=0.5, alpha=0.7)

    plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
    plt.tight_layout(pad=2)

    return fig

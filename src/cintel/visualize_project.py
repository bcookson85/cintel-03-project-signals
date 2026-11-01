"""Visualize project performance monitoring signals.

Author: Brian Cookson
Date: 2026-11

Generate a chart comparing project request response times
against the selected seven-day threshold.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import polars as pl

ROOT_DIR = Path.cwd()
DATA_FILE = ROOT_DIR / "artifacts" / "project_signals.csv"
OUTPUT_FILE = ROOT_DIR / "docs" / "images" / "project_response_chart.png"

THRESHOLD_DAYS = 7


def main() -> None:
    """Generate the project response-time visualization."""
    df = pl.read_csv(DATA_FILE)

    request_ids = df["request_id"].to_list()
    response_days = df["response_days"].to_list()
    overdue_flags = df["overdue_flag"].to_list()

    colors = ["firebrick" if flag == 1 else "steelblue" for flag in overdue_flags]

    fig, ax = plt.subplots(figsize=(12, 5))

    ax.bar(request_ids, response_days, color=colors)

    ax.axhline(
        y=THRESHOLD_DAYS,
        color="black",
        linestyle="--",
        linewidth=1.5,
        label="7-day response threshold",
    )

    ax.set_title("Project Request Response Times")
    ax.set_xlabel("Request ID")
    ax.set_ylabel("Response Time (Days)")
    ax.tick_params(axis="x", rotation=55)
    ax.legend()

    fig.tight_layout()

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT_FILE, dpi=150)
    plt.close(fig)

    print(f"Chart saved successfully: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()

"""Utilities for project performance signal design.

Author: Brian Cookson
Date: 2026-11

Load synthetic project request data and calculate
derived performance monitoring signals.
"""

from pathlib import Path

import polars as pl


def load_project_data(data_file: Path) -> pl.DataFrame:
    """Read project request records from a CSV file."""
    return pl.read_csv(data_file)


def design_project_signals(
    df: pl.DataFrame,
    threshold_days: int = 7,
) -> pl.DataFrame:
    """Calculate project response-time monitoring signals."""
    return df.with_columns(
        [
            (pl.col("response_days") > threshold_days)
            .cast(pl.Int8)
            .alias("overdue_flag"),
            (pl.col("response_days") - threshold_days)
            .clip(lower_bound=0)
            .alias("days_over_threshold"),
            pl.col("response_days")
            .mean()
            .over("project_phase")
            .round(2)
            .alias("phase_avg_response_days"),
        ]
    )


def summarize_project_signals(df: pl.DataFrame) -> pl.DataFrame:
    """Summarize project response performance by phase."""
    return (
        df.group_by("project_phase")
        .agg(
            [
                pl.len().alias("total_requests"),
                pl.col("response_days").mean().round(2).alias("avg_response_days"),
                pl.col("overdue_flag").sum().alias("overdue_requests"),
                (pl.col("overdue_flag").mean() * 100)
                .round(2)
                .alias("overdue_rate_pct"),
            ]
        )
        .sort("project_phase")
    )

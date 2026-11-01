"""Project performance signal-design pipeline.

Author: Brian Cookson
Date: 2026-11

Analyze synthetic project request data and generate
operational monitoring signals and phase summaries.
"""

import logging
from pathlib import Path
from typing import Final

from datafun_toolkit.logger import get_logger, log_header, log_path

from cintel.utils_project import (
    design_project_signals,
    load_project_data,
    summarize_project_signals,
)

LOG: logging.Logger = get_logger("P3", level="DEBUG")

ROOT_DIR: Final[Path] = Path.cwd()
DATA_FILE: Final[Path] = ROOT_DIR / "data" / "project_responses.csv"
ARTIFACTS_DIR: Final[Path] = ROOT_DIR / "artifacts"
SIGNALS_FILE: Final[Path] = ARTIFACTS_DIR / "project_signals.csv"
SUMMARY_FILE: Final[Path] = ARTIFACTS_DIR / "project_phase_summary.csv"

THRESHOLD_DAYS: Final[int] = 7


def main() -> None:
    """Run the project performance signal-design pipeline."""
    log_header(LOG, "PROJECT PERFORMANCE SIGNAL DESIGN")

    log_path(LOG, "DATA_FILE", DATA_FILE)
    log_path(LOG, "SIGNALS_FILE", SIGNALS_FILE)
    log_path(LOG, "SUMMARY_FILE", SUMMARY_FILE)

    df = load_project_data(DATA_FILE)
    LOG.info(f"Loaded {df.height} project requests")

    signals_df = design_project_signals(
        df,
        threshold_days=THRESHOLD_DAYS,
    )

    summary_df = summarize_project_signals(signals_df)

    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)

    signals_df.write_csv(SIGNALS_FILE)
    summary_df.write_csv(SUMMARY_FILE)

    overdue_count = signals_df["overdue_flag"].sum()
    overdue_rate = signals_df["overdue_flag"].mean() * 100

    LOG.info(f"Response-time threshold: {THRESHOLD_DAYS} days")
    LOG.info(f"Overdue requests: {overdue_count}")
    LOG.info(f"Overall overdue rate: {overdue_rate:.2f}%")
    LOG.info(f"Project phases summarized: {summary_df.height}")

    LOG.info("Project performance signals saved successfully.")
    LOG.info("Pipeline executed successfully!")


if __name__ == "__main__":
    main()

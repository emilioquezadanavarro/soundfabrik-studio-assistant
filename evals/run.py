"""Run one or more eval suites, print a summary, and write evals/results/latest.md.

Usage:
    python3 evals/run.py                       # all suites
    python3 evals/run.py --suite guard         # just one
    python3 evals/run.py --suite retrieval quality
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # repo root on path

# Evals make real LLM calls and would otherwise trace into whatever
# LANGSMITH_PROJECT the local .env sets for interactive use. Force a
# separate project so eval runs never mix into the dev/prod trace buckets.
# Must happen before backend.config's load_dotenv() runs (it never
# overrides an already-set env var).
os.environ["LANGSMITH_PROJECT"] = "studio-assistant-tracing-evals"

from evals import guard_set, quality_set, retrieval_set  # noqa: E402
from evals.runner import print_summary, render_report, write_report  # noqa: E402

SUITES = {
    "retrieval": retrieval_set.run,
    "guard": guard_set.run,
    "quality": quality_set.run,
}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--suite",
        nargs="+",
        choices=list(SUITES) + ["all"],
        default=["all"],
        help="Which suite(s) to run (default: all)",
    )
    args = parser.parse_args()

    names = list(SUITES) if "all" in args.suite else args.suite
    results = [SUITES[name]() for name in names]

    print_summary(results)
    report = render_report(results)
    write_report(report)
    print(f"\nWrote evals/results/latest.md")


if __name__ == "__main__":
    main()

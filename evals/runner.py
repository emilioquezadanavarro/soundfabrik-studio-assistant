"""Shared harness: run a suite of eval cases, print and render a results table."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

RESULTS_FILE = Path(__file__).resolve().parent / "results" / "latest.md"


@dataclass
class CaseResult:
    name: str
    passed: bool
    detail: str = ""


@dataclass
class SuiteResult:
    name: str
    metrics: dict[str, float]
    cases: list[CaseResult] = field(default_factory=list)


def render_report(suites: list[SuiteResult]) -> str:
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = ["# Eval results", "", f"_Generated {generated_at}_", ""]

    for suite in suites:
        passed = sum(1 for c in suite.cases if c.passed)
        lines.append(f"## {suite.name} ({passed}/{len(suite.cases)} cases passed)")
        lines.append("")
        metrics_line = " · ".join(f"**{k}**: {v:.2f}" for k, v in suite.metrics.items())
        if metrics_line:
            lines.append(metrics_line)
            lines.append("")
        lines.append("| Case | Result | Detail |")
        lines.append("|---|---|---|")
        for case in suite.cases:
            mark = "PASS" if case.passed else "FAIL"
            detail = case.detail.replace("|", "\\|").replace("\n", " ")
            lines.append(f"| {case.name} | {mark} | {detail} |")
        lines.append("")

    return "\n".join(lines)


def write_report(text: str, path: Path = RESULTS_FILE) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def print_summary(suites: list[SuiteResult]) -> None:
    for suite in suites:
        passed = sum(1 for c in suite.cases if c.passed)
        metrics = " ".join(f"{k}={v:.2f}" for k, v in suite.metrics.items())
        print(f"[{suite.name}] {passed}/{len(suite.cases)} passed  {metrics}")
        for case in suite.cases:
            if not case.passed:
                print(f"  FAIL: {case.name} — {case.detail}")

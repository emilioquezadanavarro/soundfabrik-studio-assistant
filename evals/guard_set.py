"""Guard eval: labeled on-topic / off-topic messages. Metrics: precision, recall.

Categories mirror the ALLOW/REFUSE taxonomy already written into
TOPIC_GUARD_PROMPT (backend/prompts.py), so this doesn't invent a second,
possibly-inconsistent definition of "in scope".
"""

from __future__ import annotations

from dataclasses import dataclass

from backend.guard import is_on_topic

from evals.runner import CaseResult, SuiteResult


@dataclass
class GuardCase:
    message: str
    expect_allow: bool


CASES: list[GuardCase] = [
    # ALLOW: studios, gear, services
    GuardCase("What's the difference between Studio A and Studio B?", True),
    GuardCase("Do you have a Neumann U87 I could use?", True),
    GuardCase("Do you offer mastering as a standalone service?", True),
    GuardCase("Can I get Dolby Atmos mixing done there?", True),
    # ALLOW: booking / rates
    GuardCase("How much would a two-day session cost?", True),
    GuardCase("Are you available next Friday?", True),
    GuardCase("I'd like a quote for mixing my EP.", True),
    # ALLOW: team / location
    GuardCase("Who should I talk to about booking?", True),
    GuardCase("Where exactly is the studio located?", True),
    GuardCase("Is there parking nearby for loading in gear?", True),
    # ALLOW: greetings / small talk / self-identification
    GuardCase("Hi there!", True),
    GuardCase("Thanks, that's really helpful.", True),
    GuardCase("My name is Jana and I'm working on a jazz album.", True),
    # ALLOW: production questions in context of recording here
    GuardCase("What's the best mic placement for a grand piano session?", True),
    # REFUSE: tourism / lifestyle
    GuardCase("What's the best pizza place near Neukölln?", False),
    GuardCase("Any good bars to check out in Berlin tonight?", False),
    GuardCase("What hotels do you recommend nearby?", False),
    # REFUSE: news / politics / weather / trivia
    GuardCase("What's the weather forecast for tomorrow?", False),
    GuardCase("What do you think about the upcoming election?", False),
    GuardCase("Who won the World Cup in 2018?", False),
    # REFUSE: unrelated help requests
    GuardCase("Can you help me debug my Python script?", False),
    GuardCase("What's a good recipe for banana bread?", False),
]


def run() -> SuiteResult:
    cases: list[CaseResult] = []
    tp = fp = fn = tn = 0

    for case in CASES:
        predicted_allow = is_on_topic(case.message, history=[])
        if case.expect_allow and predicted_allow:
            tp += 1
        elif not case.expect_allow and predicted_allow:
            fp += 1
        elif case.expect_allow and not predicted_allow:
            fn += 1
        else:
            tn += 1

        passed = predicted_allow == case.expect_allow
        detail = f"expected {'ALLOW' if case.expect_allow else 'REFUSE'}, got {'ALLOW' if predicted_allow else 'REFUSE'}"
        cases.append(CaseResult(name=case.message, passed=passed, detail=detail))

    precision = tp / (tp + fp) if (tp + fp) else 1.0
    recall = tp / (tp + fn) if (tp + fn) else 1.0
    metrics = {"precision": precision, "recall": recall}
    return SuiteResult(name="Guard", metrics=metrics, cases=cases)

"""Answer-quality eval: golden questions + LLM-as-judge.

Judges two things per reply: grounded-in-context (no invented facts, and no
invented *absence* of a fact either) and stayed-in-scope. Case 9 is a
retrieval-coverage regression test for the "who owns it" gap:
sample-docs/team.md lists two owners, so a grounded answer must name both.
"""

from __future__ import annotations

from dataclasses import dataclass

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage
from langsmith import traceable

from backend.config import GUARD_MODEL, anthropic_api_key
from backend.generate import generate_reply, message_text
from backend.ingestion import get_vectorstore
from backend.retrieve import format_context, retrieve_chunks

from evals.runner import CaseResult, SuiteResult

JUDGE_PROMPT = """You are grading a studio assistant's reply against the context it was given.

Judge two things:
1. GROUNDED: every factual claim in the reply is supported by the context, OR
   the reply appropriately says it isn't sure rather than inventing a fact.
   A reply that invents a NEGATIVE ("we don't have that") for something simply
   absent from the excerpts is NOT grounded. A reply that declines to help
   (off-topic message) is trivially grounded.
2. SCOPE: the reply only discusses the studio (rooms, gear, services, team,
   booking, location) and does not answer unrelated topics.

Reply with exactly two lines:
GROUNDED: yes|no
SCOPE: yes|no"""


@dataclass
class QualityCase:
    question: str


CASES: list[QualityCase] = [
    QualityCase("What's the difference between Studio North and Studio South?"),
    QualityCase("Can I record a full band in Studio South?"),
    QualityCase("Can I bring my own DAW?"),
    QualityCase("How much does a session cost?"),
    QualityCase("Who do I contact to book a session?"),
    QualityCase("Do you offer mixing without recording?"),
    QualityCase("Do you do immersive audio?"),
    QualityCase("Can I use the studio for tour rehearsals?"),
    QualityCase("Who is the owner of the studio?"),
    QualityCase("Do you have a drum kit I can use?"),
    QualityCase("What's the best pizza place near the studio?"),
    QualityCase("What's your address?"),
]


def _judge() -> ChatAnthropic:
    return ChatAnthropic(
        model=GUARD_MODEL,
        temperature=0,
        max_tokens=20,
        api_key=anthropic_api_key(),
    )


@traceable(name="judge_reply", run_type="chain")
def _judge_reply(question: str, context: str, reply: str) -> tuple[bool, bool]:
    messages = [
        SystemMessage(content=JUDGE_PROMPT),
        HumanMessage(
            content=f"CONTEXT:\n{context}\n\nQUESTION:\n{question}\n\nREPLY:\n{reply}"
        ),
    ]
    verdict = message_text(_judge().invoke(messages).content).strip().lower()
    grounded = "grounded: yes" in verdict
    scope = "scope: yes" in verdict
    return grounded, scope


def run() -> SuiteResult:
    store = get_vectorstore()
    cases: list[CaseResult] = []
    grounded_count = 0
    scope_count = 0

    for case in CASES:
        chunks = retrieve_chunks(store, case.question)
        context = format_context(chunks)
        reply = generate_reply(case.question, history=[], context=context)
        grounded, in_scope = _judge_reply(case.question, context, reply)

        grounded_count += int(grounded)
        scope_count += int(in_scope)
        passed = grounded and in_scope
        detail = f"grounded={grounded} scope={in_scope} reply={reply[:120]!r}"
        cases.append(CaseResult(name=case.question, passed=passed, detail=detail))

    total = len(cases)
    metrics = {
        "pass_rate": sum(1 for c in cases if c.passed) / total,
        "grounded_rate": grounded_count / total,
        "scope_rate": scope_count / total,
    }
    return SuiteResult(name="Answer quality", metrics=metrics, cases=cases)

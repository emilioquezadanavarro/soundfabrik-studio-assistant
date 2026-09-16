"""Retrieval eval: question -> expected source doc(s). Metrics: recall@k, MRR.

Runs against the tracked sample-docs/ set (not the private real docs) so this
is reproducible in CI with no secrets beyond the OpenAI key.
"""

from __future__ import annotations

from dataclasses import dataclass

from backend.ingestion import get_vectorstore
from backend.retrieve import retrieve_chunks

from evals.runner import CaseResult, SuiteResult


@dataclass
class RetrievalCase:
    question: str
    expected_sources: tuple[str, ...]  # any one of these counts as a hit


CASES: list[RetrievalCase] = [
    RetrievalCase("What rooms does Master Sound Berlin have?", ("home.md",)),
    RetrievalCase("Who has recorded at the studio?", ("home.md",)),
    RetrievalCase("Which room should I choose for a full band?", ("faq.md", "studio-a.md")),
    RetrievalCase("Can I record drums in Studio B?", ("faq.md", "studio-b.md")),
    RetrievalCase("Can I bring my own laptop and DAW?", ("faq.md", "studio-b.md")),
    RetrievalCase("Do I need to book an engineer or can I work alone?", ("faq.md",)),
    RetrievalCase("How much does a session cost?", ("faq.md",)),
    RetrievalCase("How do I book a session?", ("faq.md",)),
    RetrievalCase("Do you offer mixing without recording?", ("faq.md",)),
    RetrievalCase("Do you do immersive audio?", ("faq.md", "studio-b.md", "services.md")),
    RetrievalCase("What services do you offer besides recording?", ("services.md",)),
    RetrievalCase("Can I rehearse for a tour at the studio?", ("services.md", "faq.md")),
    RetrievalCase("Can I shoot a music video there?", ("services.md",)),
    RetrievalCase("What's in Studio A's live room?", ("studio-a.md",)),
    RetrievalCase("What piano do you have?", ("studio-a.md",)),
    RetrievalCase("What monitoring does Studio B have?", ("studio-b.md",)),
    RetrievalCase("What plugins are available in Studio B?", ("studio-b.md",)),
    RetrievalCase("Who is on the team?", ("team.md",)),
    RetrievalCase("Who is the owner of the studio?", ("team.md",)),
    RetrievalCase("What's your address?", ("contact.md",)),
    RetrievalCase("How do I contact the studio?", ("contact.md", "faq.md")),
]


def run(k: int = 5) -> SuiteResult:
    store = get_vectorstore()
    cases: list[CaseResult] = []
    reciprocal_ranks: list[float] = []
    hits: list[int] = []

    for case in CASES:
        docs = retrieve_chunks(store, case.question, k=k)
        sources = [d.metadata.get("source", "") for d in docs]

        rank = next(
            (i + 1 for i, s in enumerate(sources) if s in case.expected_sources),
            None,
        )
        hit = rank is not None
        hits.append(1 if hit else 0)
        reciprocal_ranks.append(1 / rank if hit else 0.0)

        detail = f"expected one of {case.expected_sources}, got {sources}"
        cases.append(CaseResult(name=case.question, passed=hit, detail=detail))

    metrics = {
        f"recall@{k}": sum(hits) / len(hits),
        "MRR": sum(reciprocal_ranks) / len(reciprocal_ranks),
    }
    return SuiteResult(name="Retrieval", metrics=metrics, cases=cases)

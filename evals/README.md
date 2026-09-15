# Evals

Three labeled suites that measure quality with real API calls, separate from
`tests/` (which is offline and free). Each run prints a summary and writes
`evals/results/latest.md`.

## Suites

- **Retrieval** (`retrieval_set.py`) — ~20 `question → expected source doc(s)`
  cases against the tracked `sample-docs/`. Reports `recall@k` and MRR:
  does the right document come back at all, and how high does it rank.
- **Guard** (`guard_set.py`) — ~20 labeled on-topic/off-topic messages, using
  the same ALLOW/REFUSE taxonomy already written into `TOPIC_GUARD_PROMPT`
  (`backend/prompts.py`). Reports precision and recall.
- **Answer quality** (`quality_set.py`) — 12 golden questions run through the
  real generation pipeline, judged by a second Claude call for whether the
  reply is grounded in the retrieved context and stayed in scope. Includes a
  permanent regression case for the "who owns it" retrieval-coverage gap
  (see Improvement Plan.md, item C7).

All three run against `sample-docs/`/`sample-assets/` (the tracked fictional
studio), not the private real content, so results are reproducible in CI and
by anyone who clones the repo with just an OpenAI + Anthropic key.

## Running

```bash
python3 evals/run.py                    # all three suites
python3 evals/run.py --suite guard      # just one
python3 evals/run.py --suite retrieval quality
```

This makes real, billed API calls (OpenAI embeddings, Anthropic Haiku for the
guard classifier and the quality judge) — small, but not free. That's why
these are separate from `pytest`/`tests/`, and why CI only runs them on
manual dispatch or a `run-evals`-labeled PR (see
`.github/workflows/evals.yml`), not on every push.

## Reading `results/latest.md`

Each suite gets its own section: a metrics line, then a table of every case
with PASS/FAIL and a one-line detail (what was expected vs. what happened).
A failing case is the actual regression signal — the aggregate metric alone
can look fine while a specific, meaningful question quietly breaks (this is
exactly how the C7 owner-coverage gap and a cross-room hallucination were
found and fixed).

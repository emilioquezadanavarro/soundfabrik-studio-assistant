# CLAUDE.md

Guidance for working in this repo — human or AI.

## What this is

A RAG studio-assistant chatbot ("Franz") for Soundfabrik Berlin: guard →
retrieve → generate, plus lead capture. Streamlit frontend, LangChain +
Chroma + Claude/OpenAI backend.

## Architecture boundaries

- **`backend/` has no Streamlit imports.** It must run headless (see
  `scripts/chat.py`, a terminal REPL that exercises the full pipeline with
  no UI). `frontend/` is the only place Streamlit is imported.
- **One turn = `handle_turn()` in `backend/pipeline.py`**: lead capture check
  → guard (`backend/guard.py`) → retrieve (`backend/retrieve.py`) → generate
  (`backend/generate.py`). Each stage is its own module and does not import
  the others' internals beyond what's re-exported.
- **`backend/retrieve.py` has no LLM calls** — plain vector similarity plus
  regex-based query expansion (`GEAR_QUERY`). Keep it that way so it stays
  testable without an API key.
- **`backend/guard.py` is regex-first, LLM-fallback**: `STUDIO_TERMS` is a
  fast in-topic match; only ambiguous messages hit the Claude classifier
  (`is_on_topic`). Don't remove the regex fast path — it's there to save
  API calls, not as a redundant check.
- **Docs source is env-driven, not hardcoded.** `backend/config.py` reads
  `DOCS_DIR`/`ASSETS_DIR` (default: `sample-docs/`/`sample-assets/`, the
  tracked fictional set). The real `studio-docs/`/`studio-assets/` are
  gitignored and only used via a local `.env` override — never assume they
  exist in a fresh clone or in CI.
- **Franz's persona name/address are env-driven too** (`STUDIO_NAME`,
  `STUDIO_ADDRESS` in `backend/config.py`, used throughout
  `backend/prompts.py` and `backend/pipeline.py`). Never hardcode the real
  studio's name or address in a prompt string — it has to stay truthful
  when `FILES_DIR` points at `sample-docs/`.
- **Prompts live in `backend/prompts.py`**, not inline in `generate.py` or
  `guard.py`. `system_prompt(lead_captured)` swaps in a different lead-capture
  section depending on session state rather than branching in the caller.
- **Tracing is LangSmith, env-var driven.** `ChatAnthropic.invoke()` calls
  trace themselves automatically once `LANGSMITH_TRACING`/`LANGSMITH_API_KEY`
  are set, and nest under whatever `@traceable` span is currently active via
  context propagation — not by explicit parent wiring. Two different reasons
  functions carry `@traceable`:
  - **Visibility**: `retrieve_chunks()` calls a plain `similarity_search()`,
    not a `Runnable`, so it has zero auto-tracing and needs the decorator
    just to appear at all.
  - **Naming/legibility**: `handle_turn()` (root span per turn),
    `is_on_topic()` (as `guard_is_on_topic`) and `generate_reply()` already
    auto-trace their inner `ChatAnthropic` calls either way (context
    propagation), but without a name on the wrapping function, two
    `ChatAnthropic` nodes in one turn (guard's classifier + the real reply)
    are indistinguishable in the tree. Naming the step, not the raw LLM
    call, also captures the surrounding logic (guard's regex fast path,
    generate's prompt assembly + `strip_dashes` post-processing) as part of
    that span.
  Same pattern in `evals/quality_set.py`: `_judge_reply` is named so the
  judge's LLM call doesn't look identical to the answer's `generate_reply`
  call in the same eval case.
  Three `LANGSMITH_PROJECT` buckets: `studio-assistant-tracing-dev` (local),
  `studio-assistant-tracing-evals` (`evals/run.py` forces this, overriding
  `.env`), `studio-assistant-tracing-prod` (Block F deploy).

## Conventions

- `from __future__ import annotations` at the top of backend modules.
- One-line module docstrings stating the module's single responsibility
  (e.g. `"""Query → similar chunks. No LLM in this module"""`).
- Session/result state is a `@dataclass`, not a dict (`SessionState`,
  `TurnResult` in `pipeline.py`).
- No comments beyond a one-line *why* for non-obvious behavior (see
  `strip_dashes`'s docstring explaining why hyphens are spared). Don't add
  docstring essays.
- No commit trailers (no `Co-Authored-By`, no session links) — plain
  commit messages only.
- **Git write commands (commit/push/rm/branch) are run by the user, never
  by an assistant.** Hand over ready-to-run commands instead.

## Commands

- Run the app: `streamlit run run.py`
- Terminal smoke test (no UI, real API calls): `python3 scripts/chat.py`
- Run tests: `pytest`
- Run evals (real, billed API calls — see `evals/README.md`): `python3 evals/run.py`
- Force a full re-ingest of the docs into Chroma:
  `python3 -c "from backend.ingestion import ingest; ingest(force=True)"`

## Testing

- `tests/` covers pure-logic functions only (no network, no API keys):
  `extract_lead`, the guard regexes, `retrieve_chunks` dedup/expansion
  (against a stub vectorstore), `format_context`/`source_names`,
  `strip_dashes`. `tests/conftest.py` force-disables LangSmith tracing
  before any test imports `backend.*` — without it, `@traceable` on
  `retrieve_chunks` would make even offline tests attempt a real network
  call. Keep that guard if you add more `@traceable` functions.
- `evals/` covers everything that calls Claude, OpenAI, or web search:
  retrieval recall@k/MRR, guard precision/recall, and answer-quality
  (LLM-as-judge for grounded-in-context + stayed-in-scope). Runs against
  `sample-docs/`, not the private real content. CI runs `tests/` on every
  push and `evals/` only on manual dispatch, to control API spend.

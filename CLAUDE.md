# CLAUDE.md

Guidance for working in this repo — human or AI.

## What this is

A RAG studio-assistant chatbot ("Franz") for Soundfabrik Berlin: guard →
retrieve → generate, plus lead capture. Streamlit frontend, LangChain +
Chroma + Claude/OpenAI backend. See `Improvement Plan.md` for the roadmap
and current status; it is gitignored, so ask if you need its contents.

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
- **Prompts live in `backend/prompts.py`**, not inline in `generate.py` or
  `guard.py`. `system_prompt(lead_captured)` swaps in a different lead-capture
  section depending on session state rather than branching in the caller.

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
- Force a full re-ingest of the docs into Chroma:
  `python3 -c "from backend.ingestion import ingest; ingest(force=True)"`

## Testing

- `tests/` covers pure-logic functions only (no network, no API keys):
  `extract_lead`, the guard regexes, `retrieve_chunks` dedup/expansion
  (against a stub vectorstore), `format_context`/`source_names`,
  `strip_dashes`.
- Anything that calls Claude, OpenAI, or web search belongs in `evals/`
  (LLM-as-judge, guard precision/recall), not `tests/` — keep the unit
  suite fast and free to run on every push.

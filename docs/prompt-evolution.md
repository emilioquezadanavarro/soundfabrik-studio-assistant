# Prompt evolution

Franz's system prompt (`backend/prompts.py`) and reply post-processing (`backend/generate.py`) didn't arrive in their current shape. Each change below was a response to something specific that broke, either found by hand or surfaced by `evals/`. Commit hashes are real and checkable against this repo's history.

## 1. Baseline (`03636ef`)

`backend/config.py` and `backend/prompts.py` start as one module apiece: a single `SYSTEM_PROMPT` string, no lead-capture awareness, no reply-length constraints. Enough to answer a question grounded in retrieved context, nothing more.

## 2. Splitting the prompt by lead state (`965e15e`)

Franz needed to behave differently depending on whether a lead was already on file: ask for contact info when a visitor asks about booking, but never ask again once it's captured, and never pitch it onto the end of an unrelated answer. A single static prompt couldn't express that.

`SYSTEM_PROMPT` split into head / lead-capture / tail parts, with a new `system_prompt(lead_captured)` swapping in one of two sections:

- `_LEAD_CAPTURE_SECTION`: ask for contact only when the visitor directly asks about booking, rates, or availability.
- `_LEAD_ON_FILE_SECTION`: once a lead exists, stop asking, tell the visitor the team will follow up.

The same change tightened reply format (1 to 3 sentences by default, bullet lists only on request, no bold headers) and added a rule that's still in the prompt today:

> Never use an em dash or en dash. Use commas, periods, or parentheses.

The reasoning written into the prompt at the time: dashes "read as machine-written." That's the same instinct behind this project's own README being hand-edited to remove them, before this doc was written, the person editing the README wasn't thinking about the prompt rule; the prompt rule was thinking about exactly that tell.

## 3. Backing the prompt rule with code (`a722621`)

A prompt instruction is a request, not a guarantee. Haiku didn't reliably follow the no-dash rule on its own, so `strip_dashes()` was added to `backend/generate.py` as an enforcement layer: every reply gets `em`/`en` dashes replaced with commas after generation, regardless of what the model actually produced. Plain hyphens (`plug-and-play`, `Walters-Storyk`) are left alone, the regex specifically targets `—`/`–`, not `-`.

The same commit threaded `lead_captured` and a per-turn `instruction` string into `generate_reply()`, so the pipeline's booking/capture turns could steer one reply's tone ("thank them for the details, don't ask again") without a separate prompt variant for every branch in `handle_turn()`. History window also got trimmed from 8 turns to 6, a small, deliberate cost cut.

## 4. Eval-driven fixes (`659a5e1`)

The first real eval run against `evals/quality_set.py` didn't pass cleanly, it surfaced four concrete failures, each fixed at the layer that actually caused it:

- **Owner-coverage gap.** Asked "who is the owner," the model sometimes named only one of two co-owners listed in the retrieved context. Fixed at both layers: a `TEAM_QUERY` regex in `backend/retrieve.py` broadens retrieval for owner/team questions, and an explicit rule in `backend/prompts.py` says to name every person the context lists for an asked-about role, not just one.
- **Hardcoded studio identity.** `backend/prompts.py` had the real studio's name and address as static text, which the model trusted over retrieved context, producing wrong answers when tested against `sample-docs/`. Fixed by making `STUDIO_NAME`/`STUDIO_ADDRESS` env-driven (`backend/config.py`), same pattern later extended to `STUDIO_WEBSITE`.
- **Cross-room hallucination.** Asked about one room, the model sometimes claimed a fact "also" applied to the other room, unprompted. Fixed with an explicit room-scoping rule: a fact about one room applies only to that room unless the excerpts say otherwise for both.
- **Scope leak on decline.** An off-topic question got a correct refusal, then Franz volunteered unrelated commentary anyway (e.g. neighborhood suggestions after declining a "best pizza place" question). Fixed with an explicit instruction: decline in one sentence and stop.

None of these were hypothetical edge cases, they were real replies the eval suite generated and then judged, which is the point of having `evals/quality_set.py` grounded/in-scope checks instead of only eyeballing a few manual conversations.

## What this shows

The prompt didn't get better by writing a longer prompt. It got better by finding a specific wrong reply, tracing it to the layer actually responsible (prompt wording, retrieval, or post-processing), and fixing that layer, sometimes more than one at once. `strip_dashes()` exists because a prompt instruction alone wasn't reliable enough to trust; the eval suite exists for the same reason, applied to correctness instead of formatting.

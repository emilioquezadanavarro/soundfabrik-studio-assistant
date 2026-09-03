"""Terminal REPL for exercising the pipeline without Streamlit.

A manual smoke test harness, not part of the automated test suite: it makes
real API calls (needs the keys in .env) and appends captured leads to
data/leads.json. Handy for eyeballing prompt or branching changes end to end.

Run from the repo root:  python3 scripts/chat.py

Type messages as the visitor; an empty line or Ctrl-C quits. SessionState and
history persist across turns, the same way the real frontend will feed them in.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # repo root on path

from backend.pipeline import handle_turn, SessionState  # noqa: E402

state = SessionState()
history: list[dict] = []
print("\n**** MANUAL SMOKE TEST **** (Empty line or Ctrl+C to exit)")
print("Frank chat 🤖")
try:
    while True:
        msg = input("you  > ").strip()
        if not msg:
            break
        result = handle_turn(msg, history, state)
        print(f"franz> {result.reply}")
        if result.sources:
            print(f"       (sources: {result.sources})")
        if result.lead_saved:
            print(f"       (LEAD SAVED: {result.lead_saved})")
        print(f"       (state: awaiting_lead={result.state.awaiting_lead} "
              f"lead_captured={result.state.lead_captured})\n")
        history += [
            {"role": "user", "content": msg},
            {"role": "assistant", "content": result.reply},
        ]
        state = result.state
except (KeyboardInterrupt, EOFError):
    print()

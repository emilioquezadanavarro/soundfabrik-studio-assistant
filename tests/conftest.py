"""Keep the unit suite offline: never send LangSmith traces from a test run.

Must run before any test module imports backend.* — backend/config.py's
load_dotenv() never overrides an already-set env var, so setting this here
first wins over whatever .env has locally. Sets both the current
(LANGSMITH_TRACING) and legacy (LANGCHAIN_TRACING_V2) names since this is
a safety guard, not a feature — belt and suspenders.
"""

import os

os.environ["LANGSMITH_TRACING"] = "false"
os.environ["LANGCHAIN_TRACING_V2"] = "false"

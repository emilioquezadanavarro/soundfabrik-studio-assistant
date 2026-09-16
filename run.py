"""Single entrypoint for the app: `streamlit run run.py`."""

from __future__ import annotations

from frontend.secrets_bridge import bridge_secrets_to_env

bridge_secrets_to_env()

from frontend.app import main  # noqa: E402 — must run after the bridge above

if __name__ == "__main__":
    main()

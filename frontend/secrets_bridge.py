"""Copy Streamlit secrets into os.environ before backend.config is ever imported.

backend/config.py reads several vars (DOCS_DIR, ASSETS_DIR, STUDIO_NAME,
STUDIO_ADDRESS) at module import time, not lazily. run.py must call
bridge_secrets_to_env() before importing frontend.app (which transitively
imports backend.config), or those values get locked in to their defaults
before Streamlit secrets ever reach os.environ.
"""

from __future__ import annotations

import os

import streamlit as st

SECRET_ENV_KEYS = (
    "OPENAI_API_KEY",
    "ANTHROPIC_API_KEY",
    "SUPABASE_URL",
    "SUPABASE_SERVICE_ROLE_KEY",
    "DOCS_DIR",
    "ASSETS_DIR",
    "STUDIO_NAME",
    "STUDIO_ADDRESS",
    "LANGSMITH_TRACING",
    "LANGSMITH_API_KEY",
    "LANGSMITH_PROJECT",
    "LANGSMITH_ENDPOINT",
)


def bridge_secrets_to_env() -> None:
    for key in SECRET_ENV_KEYS:
        try:
            value = st.secrets[key]
        except Exception:
            continue
        if value:
            os.environ.setdefault(key, str(value))

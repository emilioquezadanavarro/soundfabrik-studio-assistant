"""Paths, model names, and API keys. No Streamlit imports."""

from __future__ import annotations
import os
from pathlib import Path

from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parents[1]
load_dotenv(ROOT_DIR / ".env")

# Default to the tracked sample-docs/ set so `clone && run` works with zero
# secrets beyond API keys. Point DOCS_DIR/ASSETS_DIR at the real (gitignored)
# studio-docs/studio-assets for the live deploy.
FILES_DIR = ROOT_DIR / os.getenv("DOCS_DIR", "sample-docs")
ASSETS_DIR = ROOT_DIR / os.getenv("ASSETS_DIR", "sample-assets")
DATA_DIR = ROOT_DIR / "data"
CHROMA_DIR = DATA_DIR / "chroma"
LEADS_FILE = DATA_DIR / "leads.json"
INGEST_HASH_FILE = CHROMA_DIR / ".ingest_hash"


def _first_logo() -> Path:
    return next(iter(sorted(ASSETS_DIR.glob("*.png"))), ASSETS_DIR / "logo.png")


LOGO_MARK = _first_logo()

# Franz's persona text (backend/prompts.py) is built from these rather than
# hardcoding the real studio's name/address, so it stays truthful when
# FILES_DIR points at sample-docs/ instead of the real studio-docs/.
STUDIO_NAME = os.getenv("STUDIO_NAME", "Klangraum Berlin")
STUDIO_ADDRESS = os.getenv("STUDIO_ADDRESS", "Weserstraße 12, 12047 Berlin")

COLLECTION_NAME = "soundfabrik_knowledge"
CHUNK_SIZE = 800
CHUNK_OVERLAP = 150
RETRIEVE_K = 5

EMBEDDING_MODEL = "text-embedding-3-small"
CHAT_MODEL = os.getenv("ANTHROPIC_CHAT_MODEL", "claude-haiku-4-5")
GUARD_MODEL = os.getenv("ANTHROPIC_GUARD_MODEL", "claude-haiku-4-5")

# Abuse guards for the public live demo (Block F).
MAX_MESSAGE_CHARS = 1000
MAX_TURNS_PER_SESSION = 20
HISTORY_TURN_LIMIT = 10


def openai_api_key() -> str:
    key = (os.getenv("OPENAI_API_KEY") or "").strip()
    if not key or key.startswith("sk-your-"):
        raise RuntimeError(
            "Missing OPENAI_API_KEY (used for embeddings). "
            "Set it in .env or .streamlit/secrets.toml."
        )
    return key


def anthropic_api_key() -> str:
    key = (os.getenv("ANTHROPIC_API_KEY") or "").strip()
    if not key:
        raise RuntimeError(
            "Missing ANTHROPIC_API_KEY (used for Claude). "
            "Set it in .env or .streamlit/secrets.toml."
        )
    return key


def supabase_url() -> str:
    url = (os.getenv("SUPABASE_URL") or "").strip()
    if not url:
        raise RuntimeError(
            "Missing SUPABASE_URL (used for lead storage). "
            "Set it in .env or .streamlit/secrets.toml."
        )
    return url


def supabase_service_role_key() -> str:
    key = (os.getenv("SUPABASE_SERVICE_ROLE_KEY") or "").strip()
    if not key:
        raise RuntimeError(
            "Missing SUPABASE_SERVICE_ROLE_KEY (used for lead storage). "
            "Set it in .env or .streamlit/secrets.toml."
        )
    return key
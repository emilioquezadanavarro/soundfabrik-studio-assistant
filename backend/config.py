"""Paths, model names, and API keys. No Streamlit imports."""

from __future__ import annotations
import os
from pathlib import Path

from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parents[1]
load_dotenv(ROOT_DIR / ".env")

FILES_DIR = ROOT_DIR / "studio-docs"
ASSETS_DIR = ROOT_DIR / "studio-assets"
DATA_DIR = ROOT_DIR / "data"
CHROMA_DIR = DATA_DIR / "chroma"
LEADS_FILE = DATA_DIR / "leads.json"
INGEST_HASH_FILE = CHROMA_DIR / ".ingest_hash"
LOGO_MARK = ASSETS_DIR / "soundfabrik-mark-dark.png"

COLLECTION_NAME = "soundfabrik_knowledge"
CHUNK_SIZE = 800
CHUNK_OVERLAP = 150
RETRIEVE_K = 5

EMBEDDING_MODEL = "text-embedding-3-small"
CHAT_MODEL = os.getenv("ANTHROPIC_CHAT_MODEL", "claude-haiku-4-5")
GUARD_MODEL = os.getenv("ANTHROPIC_GUARD_MODEL", "claude-haiku-4-5")


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
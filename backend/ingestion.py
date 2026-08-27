""" Load Markdown → chunk → embed → Chroma. Rebuilds when FILES/ change """

from __future__ import annotations

import hashlib
import shutil
from pathlib import Path

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from backend.config import (
CHROMA_DIR,
CHUNK_OVERLAP,
CHUNK_SIZE,
COLLECTION_NAME,
EMBEDDING_MODEL,
FILES_DIR,
INGEST_HASH_FILE,
openai_api_key,
)


def __files_fingerprint(files: list[Path]) -> str:
    """Combine every file's name and bytes into a single sha256 hash.

    We use this as a cheap way to know if anything in studio-docs/ changed
    since the last ingest. If the hash we get now matches the one we saved
    last time, nothing changed (added, removed or edited) and we can just
    reuse the existing Chroma store instead of paying to re embed everything.
    """
    hasher = hashlib.sha256()
    for path in files:
        hasher.update(path.name.encode())
        hasher.update(path.read_bytes())
    return hasher.hexdigest()


def _embeddings() -> OpenAIEmbeddings:
    """Build the OpenAI embeddings client used to turn text chunks into vectors."""
    return OpenAIEmbeddings(model=EMBEDDING_MODEL, api_key=openai_api_key())


def ingest(*, force: bool = False) -> tuple[Chroma, int]:
    """Build or reuse the Chroma vector store from the markdown docs.

    Reads every .md file in FILES_DIR, and if the content has not changed
    since the last run (checked through the fingerprint below), it just
    opens the existing store on disk instead of re embedding anything.
    When something did change, or force is True, it rebuilds the store
    from scratch: chunks the docs, embeds them and persists them to Chroma.

    Returns a tuple of the store and how many chunks it holds.
    """
    md_files = sorted(FILES_DIR.glob("*.md"))
    if not md_files:
        raise FileNotFoundError(f"No .md files found in {FILES_DIR}")

    fingerprint = __files_fingerprint(md_files)
    embeddings = _embeddings()

    if (
        not force
        and CHROMA_DIR.exists()
        and any(CHROMA_DIR.iterdir())
        and INGEST_HASH_FILE.exists()
        and INGEST_HASH_FILE.read_text().strip() == fingerprint
    ):
        # Docs have not changed since the last ingest, so just open what we
        # already have on disk. No embedding calls needed here.
        store = Chroma(
            persist_directory=str(CHROMA_DIR),
            embedding_function=embeddings,
            collection_name=COLLECTION_NAME,
        )

        return store, store._collection.count()

    # Either the docs changed, the store is missing, or a rebuild was asked
    # for explicitly. Wipe whatever is there and start clean.
    if CHROMA_DIR.exists():
        shutil.rmtree(CHROMA_DIR)
    CHROMA_DIR.mkdir(parents=True, exist_ok=True)

    # Turn each markdown file into a Document, keeping the file name and
    # path as metadata so we can trace an answer back to its source later.
    documents: list[Document] = []
    for path in md_files:
        documents.append(
            Document(
                page_content=path.read_text(encoding="utf-8"),
                metadata={"source": path.name, "path": str(path)},
            )
        )

    # Split on markdown headers first, then fall back to paragraphs, lines
    # and words so a chunk almost never gets cut off mid sentence.
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n## ", "\n# ", "\n\n", "\n", " ", ""],
    )

    chunks = splitter.split_documents(documents)

    # Embed every chunk and persist the result to disk under CHROMA_DIR.
    store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(CHROMA_DIR),
        collection_name=COLLECTION_NAME,
    )

    # Save the fingerprint so the next call can skip re embedding if the
    # docs have not changed.
    INGEST_HASH_FILE.write_text(fingerprint, encoding="utf-8")
    return store, len(chunks)


def get_vectorstore() -> Chroma:
    """Convenience wrapper for callers who only care about the store itself."""
    store, _ = ingest(force=False)
    return store

""" Query → similar chunks. No LLM in this module """

from __future__ import annotations
import re

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langsmith import traceable

from backend.config import RETRIEVE_K

# Words that suggest the visitor is asking about gear or equipment rather
# than the studio in general. When a query matches one of these, we run a
# second, broadened search alongside the original one, since a short query
# like "drums?" on its own does not always pull in the full equipment list.
GEAR_QUERY = re.compile(
    r"\b(drum|kit|snare|cymbal|mic|microphone|amp|guitar|bass|piano|"
    r"steinway|gear|equipment|instrument|console|neve)\b",
      re.IGNORECASE,
)

# Team/ownership questions have the same problem as gear questions: the team
# page splits into one chunk per person, so a plain top-k search over the
# whole corpus can surface only one team member's chunk and silently drop
# the rest (e.g. "who is the owner" naming only one of two owners).
TEAM_QUERY = re.compile(
    r"\b(owner|owners|founder|founders|team|staff|who\s+runs|who\s+owns)\b",
    re.IGNORECASE,
)


@traceable(name="retrieve_chunks", run_type="retriever")
def retrieve_chunks(vectorestore: Chroma, query: str, k:int = RETRIEVE_K) -> list[Document]:
    """Find the chunks in the vector store most relevant to a user query.

    Runs a plain similarity search against the query. If the query looks
    like it is about gear/equipment (GEAR_QUERY) or the team/ownership
    (TEAM_QUERY), a second search is run with the query broadened, so we
    do not miss gear or team members that live on a page the original
    wording did not point to directly.

    Results from every search are merged and deduplicated (by comparing
    the first 200 characters of each chunk), so the same chunk showing up
    in both searches only gets returned once.
    """
    queries = [query]
    if GEAR_QUERY.search(query):
        queries.append(
            f"{query} equipment list gear inventory Studio A and Studio B"
        )
    if TEAM_QUERY.search(query):
        queries.append(f"{query} team members owners staff roster")

    seen: set[str] = set()
    docs: list[Document] = []

    for query in queries:
        for doc in vectorestore.similarity_search(query, k=k):
            # Using a slice of the content as the dedup key is enough here,
            # since two different chunks starting the same way would be
            # very unlikely given how the docs are split.
            key = doc.page_content[:200]

            if key in seen:
                continue

            seen.add(key)
            docs.append(doc)

    return docs


def format_context(docs: list[Document]) -> str:
    """Turn retrieved chunks into one text block the LLM can read as context.

    Each chunk gets numbered and labeled with the file it came from, so the
    model (and anyone debugging an answer) can see where each piece of
    information is sourced from.
    """
    if not docs:
        return "(No matching studio documents founds)"

    parts = []
    for i, doc in enumerate(docs, start=1):
        source = doc.metadata.get("source", "unknown")
        parts.append(f"[Excerpt {i} - {source}]\n{doc.page_content}")
    return "\n\n".join(parts)


def source_names(docs: list[Document]) -> list[str]:
    """Return the distinct source file names behind a list of chunks.

    Used to show the visitor (or a log) which documents an answer was
    actually pulled from, without listing the same file more than once.
    """
    names: list[str] = []
    for doc in docs:
        source = doc.metadata.get("source", "unknown")
        if source not in names:
            names.append(source)
    return names

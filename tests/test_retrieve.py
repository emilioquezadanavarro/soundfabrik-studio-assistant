from langchain_core.documents import Document

from backend.retrieve import format_context, retrieve_chunks, source_names


class StubVectorstore:
    """Returns one canned response per call, in call order, ignoring the
    actual query text: lets tests control exactly what each search
    returns without needing a real embedding model."""

    def __init__(self, responses: list[list[Document]]):
        self._responses = responses
        self.calls: list[str] = []

    def similarity_search(self, query: str, k: int = 5) -> list[Document]:
        self.calls.append(query)
        index = len(self.calls) - 1
        return self._responses[index] if index < len(self._responses) else []


def _doc(text: str, source: str) -> Document:
    return Document(page_content=text, metadata={"source": source})


def test_retrieve_chunks_dedupes_within_a_single_search():
    duplicate = _doc("Studio A is our live room.", "studio-a.md")
    store = StubVectorstore([[duplicate, duplicate]])

    docs = retrieve_chunks(store, "Tell me about Studio A")

    assert len(docs) == 1


def test_retrieve_chunks_expands_gear_queries_and_dedupes_across_calls():
    shared = _doc("Our mic collection includes several Neumann U87s.", "studio-a.md")
    only_in_second = _doc("Studio B mic list: 1x Neumann U87.", "studio-b.md")
    store = StubVectorstore([[shared], [shared, only_in_second]])

    docs = retrieve_chunks(store, "Do you have a drum kit?")

    # Second, broadened search actually ran.
    assert len(store.calls) == 2
    assert "equipment list gear inventory" in store.calls[1]
    # The shared chunk is merged, not duplicated; the new one is kept.
    assert docs == [shared, only_in_second]


def test_retrieve_chunks_skips_expansion_for_non_gear_queries():
    store = StubVectorstore([[_doc("Rates depend on the project.", "faq.md")]])

    retrieve_chunks(store, "How much does a session cost?")

    assert len(store.calls) == 1


def test_format_context_empty_list():
    assert format_context([]) == "(No matching studio documents found)"


def test_format_context_labels_each_chunk_with_its_source():
    docs = [_doc("Studio A details.", "studio-a.md")]
    context = format_context(docs)
    assert "[Excerpt 1 - studio-a.md]" in context
    assert "Studio A details." in context


def test_source_names_dedupes_and_preserves_order():
    docs = [
        _doc("a", "studio-a.md"),
        _doc("b", "faq.md"),
        _doc("c", "studio-a.md"),
    ]
    assert source_names(docs) == ["studio-a.md", "faq.md"]

import numpy as np

from src.models import DocumentChunk
from src.retriever import CohereRetriever


def test_search_orders_results_by_similarity() -> None:
    retriever = CohereRetriever.__new__(CohereRetriever)
    retriever.chunks = [
        DocumentChunk("1", "restablecer contraseña", 2, "manual.pdf"),
        DocumentChunk("2", "solicitar una notebook", 5, "manual.pdf"),
    ]
    retriever._document_embeddings = np.array(
        [[1.0, 0.0], [0.0, 1.0]], dtype=np.float32
    )
    retriever._embed = lambda texts, input_type: np.array(
        [[0.9, 0.1]], dtype=np.float32
    )

    results = retriever.search("olvide mi clave", top_k=2)

    assert results[0].chunk.id == "1"
    assert results[0].score > results[1].score


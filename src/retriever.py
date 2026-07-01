from collections.abc import Sequence
import numpy as np

from src.models import DocumentChunk, SearchResult


class CohereRetriever:
    def __init__(
        self,
        api_key: str,
        chunks: Sequence[DocumentChunk],
        model: str = "embed-v4.0",
    ) -> None:
        if not chunks:
            raise ValueError("Se necesita al menos un fragmento")
        import cohere

        self.client = cohere.ClientV2(api_key=api_key)
        self.chunks = list(chunks)
        self.model = model
        self._document_embeddings = self._embed(
            [chunk.text for chunk in self.chunks], "search_document"
        )

    def _embed(self, texts: list[str], input_type: str) -> np.ndarray:
        response = self.client.embed(
            texts=texts,
            model=self.model,
            input_type=input_type,
            embedding_types=["float"],
            output_dimension=1024,
        )
        return np.asarray(response.embeddings.float, dtype=np.float32)

    def search(self, query: str, top_k: int = 4) -> list[SearchResult]:
        if not query.strip():
            return []

        query_embedding = self._embed([query], "search_query")[0]
        doc_norms = np.linalg.norm(self._document_embeddings, axis=1)
        query_norm = np.linalg.norm(query_embedding)
        scores = (self._document_embeddings @ query_embedding) / (
            doc_norms * query_norm + 1e-12
        )
        best_indices = np.argsort(scores)[::-1][:top_k]

        return [
            SearchResult(chunk=self.chunks[index], score=float(scores[index]))
            for index in best_indices
        ]

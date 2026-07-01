from dataclasses import dataclass


@dataclass(frozen=True)
class DocumentChunk:
    id: str
    text: str
    page: int
    source: str


@dataclass(frozen=True)
class SearchResult:
    chunk: DocumentChunk
    score: float


@dataclass(frozen=True)
class AgentResponse:
    answer: str
    sources: list[SearchResult]


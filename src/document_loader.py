from pathlib import Path

from pypdf import PdfReader

from src.models import DocumentChunk


def _split_text(text: str, chunk_size: int, overlap: int) -> list[str]:
    if chunk_size <= overlap:
        raise ValueError("chunk_size debe ser mayor que overlap")

    paragraphs = [line.strip() for line in text.splitlines() if line.strip()]
    chunks: list[str] = []
    current = ""

    for paragraph in paragraphs:
        candidate = f"{current}\n{paragraph}".strip()
        if current and len(candidate) > chunk_size:
            chunks.append(current)
            tail = current[-overlap:] if overlap else ""
            current = f"{tail}\n{paragraph}".strip()
        else:
            current = candidate

    if current:
        chunks.append(current)
    return chunks


def load_pdf(
    path: str | Path, chunk_size: int = 1100, overlap: int = 180
) -> list[DocumentChunk]:
    pdf_path = Path(path)
    if not pdf_path.exists():
        raise FileNotFoundError(f"No se encontro el documento: {pdf_path}")

    reader = PdfReader(pdf_path)
    chunks: list[DocumentChunk] = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        for index, fragment in enumerate(
            _split_text(text, chunk_size, overlap), start=1
        ):
            chunks.append(
                DocumentChunk(
                    id=f"p{page_number}-c{index}",
                    text=fragment,
                    page=page_number,
                    source=pdf_path.name,
                )
            )

    if not chunks:
        raise ValueError("El PDF no contiene texto extraible")
    return chunks


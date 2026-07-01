from src.document_loader import _split_text


def test_split_text_keeps_content() -> None:
    text = "Primer procedimiento.\nSegundo procedimiento con mas informacion."
    chunks = _split_text(text, chunk_size=35, overlap=5)

    assert len(chunks) == 2
    assert "Primer procedimiento" in chunks[0]
    assert "Segundo procedimiento" in chunks[1]


def test_split_text_rejects_invalid_sizes() -> None:
    try:
        _split_text("contenido", chunk_size=100, overlap=100)
    except ValueError as error:
        assert "mayor" in str(error)
    else:
        raise AssertionError("Se esperaba ValueError")


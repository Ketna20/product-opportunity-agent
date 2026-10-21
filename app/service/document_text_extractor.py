from pathlib import Path

SUPPORTED_TEXT_EXTENSIONS = {".txt", ".md"}


def extract_text(filename: str, file_bytes: bytes) -> str:
    extension = Path(filename).suffix.lower()

    if extension not in SUPPORTED_TEXT_EXTENSIONS:
        raise ValueError(f"Unsupported file extension: {extension}")

    try:
        text = file_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Document must contain valid UTF-8 text") from exc

    text = text.strip()
    if not text:
        raise ValueError("Document contains no text")

    return text
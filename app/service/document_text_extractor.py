from pathlib import Path
from io import BytesIO
from pypdf import PdfReader
from pypdf.errors import PdfReadError

SUPPORTED_TEXT_EXTENSIONS = {".txt", ".md"}


def extract_text(filename: str, file_bytes: bytes) -> str:
    extension = Path(filename).suffix.lower()

    if extension == ".pdf":
        text = extract_text_from_pdf(file_bytes)
    elif extension in SUPPORTED_TEXT_EXTENSIONS:
        try:
            text = file_bytes.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Document must contain valid UTF-8 text") from exc
    else:
        raise ValueError(f"Unsupported file extension: {extension}")

    text = text.strip()
    if not text:
        raise ValueError("Document contains no text")

    return text


def extract_text_from_pdf(file_bytes: bytes) -> str:
    try:
        pdf_reader = PdfReader(BytesIO(file_bytes))
        page_texts = []
        for page in pdf_reader.pages:
            page_texts.append(page.extract_text() or "")

        return "\n".join(page_texts).strip()
    except PdfReadError as exc:
        raise ValueError("Invalid PDF file. Document is not a readable PDF.") from exc

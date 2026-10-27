import pytest
from io import BytesIO
from pypdf import PdfWriter
from pathlib import Path
from app.service.document_text_extractor import extract_text


def test_extract_text_from_txt_document() -> None:

    result = extract_text("feedback.txt", b"  Customers want clearer labels.  ")

    assert result == "Customers want clearer labels."

def test_extract_text_from_markdown_document_with_uppercase_extension() -> None:
    result = extract_text("feedback.MD", b"Recurring customer feedback")

    assert result == "Recurring customer feedback"

def test_extract_text_rejects_unsupported_extension() -> None:
    with pytest.raises(ValueError, match="Unsupported file extension"):
        extract_text("feedback.csv", b"Some text")

def test_extract_text_rejects_invalid_utf8() -> None:
    with pytest.raises(ValueError, match="valid UTF-8"):
        extract_text("feedback.txt", b"\xff\xfe")

def test_extract_text_rejects_blank_content() -> None:
    with pytest.raises(ValueError, match="contains no text"):
        extract_text("feedback.txt", b" \n\t ")

def test_extract_text_reject_invalid_pdf() -> None:
    with pytest.raises(ValueError, match="Invalid PDF file"):
        extract_text("feedback.pdf", b"Invalid PDF content")

def test_extractor_text_rejects_pdf_without_text() -> None:
    pdf_writer = PdfWriter()
    pdf_writer.add_blank_page(width=612, height=792)

    buffer = BytesIO()
    pdf_writer.write(buffer)
    buffer.seek(0)

    with pytest.raises(ValueError, match="contains no text"):
        extract_text("blank.pdf", buffer.getvalue())

def test_extract_text_from_pdf_document() -> None:
    pdf_path = (
        Path(__file__).parent / "fixtures" / "customer_feedback.pdf"
    )

    result = extract_text("customer_feedback.pdf", pdf_path.read_bytes())

    normalized_text = " ".join(result.split())

    assert normalized_text == "Customers want clearer product labels."
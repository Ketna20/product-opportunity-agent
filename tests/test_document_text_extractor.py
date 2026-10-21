import pytest
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
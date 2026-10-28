import pytest

from app.service.text_chunker import chunk_text

@pytest.mark.parametrize("chunk_size", [0, -1])
def test_chunk_text_rejects_nonpositive_chunk_size(chunk_size: int) -> None:
    with pytest.raises(ValueError, match="chunk_size must be greater than 0"):
        chunk_text("Customer feedback", chunk_size=chunk_size)

def test_chunk_text_rejects_negative_overlap() -> None:
    with pytest.raises(ValueError, match="overlap must not be negative"):
        chunk_text("Customer feedback", chunk_size=1000, overlap=-1)


@pytest.mark.parametrize("overlap", [10, 11])
def test_chunk_text_rejects_overlap_at_least_chunk_size(overlap: int) -> None:
    with pytest.raises(ValueError, match="overlap must be less than chunk_size"):
        chunk_text("Customer feedback", chunk_size=10, overlap=overlap)


@pytest.mark.parametrize("text", ["", "   ", "\n\t"])
def test_chunk_text_returns_empty_list_for_empty_text(text: str) -> None:
    assert chunk_text(text) == []


def test_chunk_text_returns_single_chunk_for_short_text() -> None:
    result = chunk_text("Clearer lables", chunk_size=20, overlap=5)

    assert result == ["Clearer lables"]


def test_chunk_text_returns_one_chunk_at_exact_size() -> None:
    result = chunk_text("abcdefghi", chunk_size=10, overlap=2)

    assert result == ["abcdefghi"]


def test_chunk_text_splits_long_text_with_overlap() -> None:
    text = "abcdefghijkl"
    chunk_size = 5
    overlap = 2

    result = chunk_text(text, chunk_size=chunk_size, overlap=overlap)
    expected_chunks = ["abcde", "defgh", "ghijk", "jkl"]


    assert result == expected_chunks


def test_chunk_text_splits_without_overlap() -> None:
    text = "abcdefghijkl"
    chunk_size = 5
    overlap = 0

    result = chunk_text(text, chunk_size=chunk_size, overlap=overlap)

    assert result == ["abcde", "fghij", "kl"]


def test_chunk_text_stops_when_final_chunk_ends_at_text_boundary() -> None:
    result = chunk_text("abcdefgh", chunk_size=5, overlap=2)

    assert result == ["abcde", "defgh"]


def test_chunk_text_supports_chunk_size_of_one() -> None:
    result = chunk_text("abc", chunk_size=1, overlap=0)

    assert result == ["a", "b", "c"]


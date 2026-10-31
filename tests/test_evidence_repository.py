from datetime import UTC, datetime
from uuid import uuid4

from app.repository.evidence_repo import (
    InMemoryEvidenceRepository,
)

from app.schema.evidence import (
    EvidenceResponse,
)

from app.schema.evidence_chunk import (
    EvidenceChunkResponse,
)

def test_find_evidence_by_opportunity_search_id() -> None:
    repository = InMemoryEvidenceRepository()
    search_id1 = uuid4()
    search_id2 = uuid4()
    evidence_id1 = uuid4()
    evidence_id2 = uuid4()
    evidence_id3 = uuid4()
    evidence1 = EvidenceResponse(
        id=evidence_id1,
        opportunity_search_id=search_id1,
        source_type="Test evidence Type1",
        source_name="Test source name1",
        content="Test content1",
        source_url="https://example.com/test1",
        created_at=datetime.now(UTC),
    )

    evidence2 = EvidenceResponse(
            id=evidence_id2,
            opportunity_search_id=search_id1,
            source_type="Test evidence Type2",
            source_name="Test source name2",
            content="Test2 content2",
            source_url="https://example.com/test2",
            created_at=datetime.now(UTC),
    )
    evidence3 = EvidenceResponse(
                id=evidence_id3,
                opportunity_search_id=search_id2,
                source_type="Test evidence Type3",
                source_name="Test source name3",
                content="Test2 content3",
                source_url="https://example.com/test3",
                created_at=datetime.now(UTC),
    )

    saved_evidence1 = repository.save(evidence1)
    saved_evidence2 = repository.save(evidence2)
    saved_evidence3 = repository.save(evidence3)
    retrieved_evidence_list1 = repository.find_by_opportunity_search_id(search_id1)
    retrieved_evidence_list2 = repository.find_by_opportunity_search_id(search_id2)


    assert retrieved_evidence_list1 == [
        saved_evidence1,
        saved_evidence2,
    ]
    assert retrieved_evidence_list2 == [saved_evidence3]

def test_find_evidence_returns_empty_list_when_none_exist() -> None:
    repository = InMemoryEvidenceRepository()

    retrieved_evidence = repository.find_by_opportunity_search_id(uuid4())

    assert retrieved_evidence == []

def test_save_evidence_with_chunks_and_retrieve_in_order() -> None:
    repository = InMemoryEvidenceRepository()
    now = datetime.now(UTC)

    evidence = EvidenceResponse(
        id=uuid4(),
        opportunity_search_id=uuid4(),
        source_type="document",
        source_name="customer_feedback.txt",
        content="Customers want less packaging and lower prices.",
        source_url=None,
        created_at=now,
    )

    chunk0 = EvidenceChunkResponse(
        id=uuid4(),
        evidence_id=evidence.id,
        chunk_index=0,
        content="Customers want less packaging",
        created_at=now,
    )

    chunk1 = EvidenceChunkResponse(
        id=uuid4(),
        evidence_id=evidence.id,
        chunk_index=1,
        content="and lower prices.",
        created_at=now,
    )

    saved_evidence = repository.save_with_chunks(
        evidence,
        [chunk0, chunk1]
    )


    assert saved_evidence == evidence
    assert repository.get_by_id(evidence.id) == evidence
    assert repository.find_chunks_by_evidence_id(evidence.id) == [chunk0, chunk1]
    assert repository.find_chunks_by_evidence_id(uuid4()) == []
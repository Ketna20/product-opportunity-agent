from fastapi.testclient import TestClient
from uuid import UUID, uuid4

from pathlib import Path
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.model.opportunity_search_model import (
    OpportunitySearchModel,
)
from app.model.evidence_model import EvidenceModel
from app.model.evidence_chunk_model import EvidenceChunkModel

def test_health_check(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_create_opportunity_search(
        client: TestClient,
        db_session: Session,
) -> None:
    request_body = {
        "product_category": "Facial moisturizer",
        "market": "United States",
        "target_customer": (
            "Environmentally conscious skincare consumers"
        ),
        "objective": (
            "Identify an unmet customer need that could "
            "support a new product"
        ),
        "constraints": [
            "Retail price below $60",
            "Suitable for direct-to-consumer sales",
        ],
        "initial_hypothesis": None,
    }

    response = client.post(
        "/opportunity-searches",
        json=request_body,
    )
    response_body = response.json()

    persisted_model = db_session.get(
        OpportunitySearchModel,
        UUID(response_body["id"]),
    )

    assert persisted_model is not None
    assert (
        persisted_model.product_category
        == "Facial moisturizer"
    )
    assert persisted_model.status.value == "created"
    assert response.status_code == 201
    assert response_body["product_category"] == "Facial moisturizer"
    assert response_body["market"] == "United States"
    assert response_body["status"] == "created"
    assert response_body["id"] is not None
    assert response_body["created_at"] is not None




def test_rejects_short_objective(client: TestClient) -> None:
    request_body = {
        "product_category": "Facial moisturizer",
        "market": "United States",
        "target_customer": "Skincare consumers",
        "objective": "Find one",
    }

    response = client.post(
        "/opportunity-searches",
        json=request_body,
    )

    assert response.status_code == 422



def test_get_opportunity_search(client: TestClient) -> None:
    request_body = {
        "product_category": "Facial moisturizer",
        "market": "United States",
        "target_customer": (
            "Environmentally conscious skincare consumers"
        ),
        "objective": (
            "Identify an unmet customer need that could "
            "support a new product"
        ),
        "constraints": [
            "Retail price below $60",
            "Suitable for direct-to-consumer sales",
        ],
        "initial_hypothesis": None,
    }

    create_response = client.post(
        "/opportunity-searches",
        json=request_body,
    )

    assert create_response.status_code == 201

    search_id = create_response.json()["id"]

    get_response = client.get(
        f"/opportunity-searches/{search_id}"
    )

    assert get_response.status_code == 200
    assert get_response.json() == create_response.json()


def test_get_unknown_opportunity_search_returns_404(client: TestClient) -> None:
    unknown_id = uuid4()

    response = client.get(
        f"/opportunity-searches/{unknown_id}"
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Opportunity search not found"
    }

def test_create_evidence(
    client: TestClient,
    db_session: Session,
) -> None:
    search_request_body = {
        "product_category": "Facial moisturizer",
        "market": "United States",
        "target_customer": (
            "Environmentally conscious skincare consumers"
        ),
        "objective": (
            "Identify an unmet customer need that could "
            "support a new product"
        ),
        "constraints": [
            "Retail price below $60",
            "Suitable for direct-to-consumer sales",
        ],
        "initial_hypothesis": None,
    }
    create_search_response = client.post(
        "/opportunity-searches",
        json=search_request_body,
    )

    assert create_search_response.status_code == 201

    search_id = create_search_response.json()["id"]

    evidence_request_body = {
        "source_type": "customer_review",
        "source_name": "Amazon review",
        "content": (
            "The moisturizer works well, but the packaging "
            "creates too much waste."
        ),
        "source_url": "https://example.com/reviews/123",
    }

    response = client.post(
        f"/opportunity-searches/{search_id}/evidence",
        json=evidence_request_body,
    )
    response_body = response.json()

    persisted_model = db_session.get(
        EvidenceModel,
        UUID(response_body["id"]),
    )

    assert persisted_model is not None
    assert str(persisted_model.opportunity_search_id) == search_id
    assert persisted_model.source_type == "customer_review"
    assert persisted_model.source_url == evidence_request_body["source_url"]
    assert persisted_model.content == evidence_request_body["content"]

    assert response.status_code == 201
    assert response_body["opportunity_search_id"] == search_id
    assert response_body["source_type"] == "customer_review"
    assert response_body["source_name"] == "Amazon review"
    assert response_body["content"] == evidence_request_body["content"]
    assert response_body["source_url"] == evidence_request_body["source_url"]
    assert response_body["id"] is not None
    assert response_body["created_at"] is not None

    chunks = db_session.scalars(
        select(EvidenceChunkModel)
        .where(
            EvidenceChunkModel.evidence_id
            == UUID(response_body["id"])
        )
        .order_by(EvidenceChunkModel.chunk_index)
    ).all()

    assert len(chunks) == 1
    assert chunks[0].chunk_index == 0
    assert chunks[0].content == evidence_request_body["content"]
    assert chunks[0].created_at == persisted_model.created_at

def test_create_evidence_for_unknown_search_returns_404(
    client: TestClient,
) -> None:
    unknown_search_id = uuid4()
    request_body = {
        "source_type": "customer_review",
        "source_name": "Amazon review",
        "content": (
            "The moisturizer works well, but the packaging "
            "creates too much waste."
        ),
        "source_url": "https://example.com/reviews/123",
    }
    response = client.post(
        f"/opportunity-searches/{unknown_search_id}/evidence",
        json=request_body,
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Opportunity search not found"
    }


def test_list_evidence_for_opportunity_search(
    client: TestClient,
) -> None:
    search_request = {
        "product_category": "Facial moisturizer",
        "market": "United States",
        "target_customer": (
            "Environmentally conscious skincare consumers"
        ),
        "objective": (
            "Identify an unmet customer need that could "
            "support a new product"
        ),
        "constraints": [
            "Retail price below $60",
            "Suitable for direct-to-consumer sales",
        ],
        "initial_hypothesis": None,
    }

    create_search_response = client.post(
        "/opportunity-searches",
        json=search_request,
    )

    assert create_search_response.status_code == 201

    search_id = create_search_response.json()["id"]

    first_evidence_request = {
        "source_type": "customer_review",
        "source_name": "Amazon review",
        "content": (
            "The moisturizer works well, but the packaging "
            "creates too much waste."
        ),
        "source_url": "https://example.com/reviews/123",
    }

    second_evidence_request = {
        **first_evidence_request,
        "source_name": "Sephora review",
        "content": (
            "I like the moisturizer, but I wish it came in "
            "recyclable packaging."
        ),
        "source_url": "https://example.com/reviews/456",
    }

    first_create_response = client.post(
        f"/opportunity-searches/{search_id}/evidence",
        json=first_evidence_request,
    )
    second_create_response = client.post(
        f"/opportunity-searches/{search_id}/evidence",
        json=second_evidence_request,
    )

    assert first_create_response.status_code == 201
    assert second_create_response.status_code == 201

    response = client.get(
        f"/opportunity-searches/{search_id}/evidence"
    )

    assert response.status_code == 200
    assert response.json() == [
        first_create_response.json(),
        second_create_response.json(),
    ]


def test_list_evidence_returns_empty_list_when_none_exist(
    client: TestClient,
) -> None:
    search_request = {
        "product_category": "Facial moisturizer",
        "market": "United States",
        "target_customer": (
            "Environmentally conscious skincare consumers"
        ),
        "objective": (
            "Identify an unmet customer need that could "
            "support a new product"
        ),
        "constraints": [
            "Retail price below $60",
            "Suitable for direct-to-consumer sales",
        ],
        "initial_hypothesis": None,
    }

    create_search_response = client.post(
        "/opportunity-searches",
        json=search_request,
    )

    assert create_search_response.status_code == 201

    search_id = create_search_response.json()["id"]

    response = client.get(
        f"/opportunity-searches/{search_id}/evidence"
    )

    assert response.status_code == 200
    assert response.json() == []


def test_list_evidence_for_unknown_search_returns_404(
    client: TestClient,
) -> None:
    unknown_search_id = uuid4()

    response = client.get(
        f"/opportunity-searches/{unknown_search_id}/evidence"
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Opportunity search not found"
    }


def test_upload_text_document_as_evidence(
    client: TestClient,
    db_session: Session,
) -> None:
    search_response = client.post(
        "/opportunity-searches",
        json={
            "product_category": "Facial moisturizer",
            "market": "United States",
            "target_customer": (
                "Environmentally conscious consumers"
            ),
            "objective": (
                "Identify an unmet customer needs in skincare packaging"
            ),
            "constraints": [
                "Retail price below $60",
                "Suitable for direct-to-consumer sales",
            ],
            "initial_hypothesis": None,
        },
    )

    assert search_response.status_code == 201

    search_id = search_response.json()["id"]

    files={
        "file": (
            "feedback.txt",
            b"  Customers want recyclable packaging.  ",
            "text/plain",
        ),
    }

    response = client.post(
        f"/opportunity-searches/{search_id}/evidence/upload",
        files=files,
    )

    assert response.status_code == 201, response.text
    response_body = response.json()

    assert response_body["opportunity_search_id"] == search_id
    assert response_body["source_type"] == "document"
    assert response_body["source_name"] == "feedback.txt"
    assert response_body["content"] == "Customers want recyclable packaging."
    assert response_body["source_url"] is None

    persisted_model = db_session.get(
        EvidenceModel,
        UUID(response_body["id"]),
    )
    assert persisted_model is not None
    assert persisted_model.content == response_body["content"]
    assert str(persisted_model.opportunity_search_id) == search_id

    list_response = client.get(
        f"/opportunity-searches/{search_id}/evidence"
    )
    assert list_response.status_code == 200
    assert list_response.json() == [response_body]

    chunks = db_session.scalars(
        select(EvidenceChunkModel)
        .where(
            EvidenceChunkModel.evidence_id
            == UUID(response_body["id"])
        )
        .order_by(EvidenceChunkModel.chunk_index)
    ).all()

    assert len(chunks) == 1
    assert chunks[0].chunk_index == 0
    assert chunks[0].content == "Customers want recyclable packaging."
    assert chunks[0].created_at == persisted_model.created_at


def test_upload_document_for_unknown_search_returns_404(
    client: TestClient,
) -> None:
    unknown_search_id = uuid4()

    files={
        "file": (
            "feedback.txt",
            b"Customers want recyclable packaging.",
            "text/plain",
        ),
    }

    response = client.post(
        f"/opportunity-searches/{unknown_search_id}/evidence/upload",
        files=files,
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Opportunity search not found"
    }


def test_upload_unsupported_document_returns_400(
    client: TestClient,
) -> None:
    search_response = client.post(
        "/opportunity-searches",
        json={
            "product_category": "Facial moisturizer",
            "market": "United States",
            "target_customer": (
                "Environmentally conscious consumers"
            ),
            "objective": (
                "Identify an unmet customer needs in skincare packaging"
            ),
            "constraints": [
                "Retail price below $60",
                "Suitable for direct-to-consumer sales",
            ],
            "initial_hypothesis": None,
        },
    )

    assert search_response.status_code == 201

    search_id = search_response.json()["id"]

    response = client.post(
        f"/opportunity-searches/{search_id}/evidence/upload",
        files={
            "file": (
                "feedback.csv",
                b"Customers want recyclable packaging.",
                "text/csv",
            ),
        },
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Unsupported file extension: .csv"
    }

    list_response = client.get(
        f"/opportunity-searches/{search_id}/evidence"
    )

    assert list_response.status_code == 200
    assert list_response.json() == []


def test_upload_pdf_document_as_evidence(
    client: TestClient,
    db_session: Session,
) -> None:
    search_response = client.post(
        "/opportunity-searches",
        json={
            "product_category": "Facial moisturizer",
            "market": "United States",
            "target_customer": (
                "Environmentally conscious consumers"
            ),
            "objective": (
                "Identify an unmet customer needs in skincare packaging"
            ),
            "constraints": [
                "Retail price below $60",
                "Suitable for direct-to-consumer sales",
            ],
            "initial_hypothesis": None,
        },
    )

    assert search_response.status_code == 201

    search_id = search_response.json()["id"]

    pdf_path = (
        Path(__file__).parent / "fixtures" / "customer_feedback.pdf"
    )

    files = {
        "file": (
            "customer_feedback.pdf",
            pdf_path.read_bytes(),
            "application/pdf",
        ),
    }

    response = client.post(
        f"/opportunity-searches/{search_id}/evidence/upload",
        files=files,
    )

    assert response.status_code == 201, response.text
    response_body = response.json()

    assert response_body["opportunity_search_id"] == search_id
    assert response_body["source_type"] == "document"
    assert response_body["source_name"] == "customer_feedback.pdf"
    assert (
        " ".join(response_body["content"].split())
        == "Customers want clearer product labels."
    )
    assert response_body["source_url"] is None

    persisted_model = db_session.get(
        EvidenceModel,
        UUID(response_body["id"]),
    )
    assert persisted_model is not None
    assert persisted_model.content == response_body["content"]
    assert str(persisted_model.opportunity_search_id) == search_id

    list_response = client.get(
        f"/opportunity-searches/{search_id}/evidence"
    )
    assert list_response.status_code == 200
    assert list_response.json() == [response_body]
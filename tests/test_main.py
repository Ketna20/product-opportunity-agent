from fastapi.testclient import TestClient
from uuid import UUID, uuid4

from sqlalchemy.orm import Session

from app.model.opportunity_search_model import (
    OpportunitySearchModel,
)
from app.model.evidence_model import EvidenceModel

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
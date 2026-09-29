from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_check() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_create_opportunity_search() -> None:
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

    assert response.status_code == 201
    assert response_body["product_category"] == "Facial moisturizer"
    assert response_body["market"] == "United States"
    assert response_body["status"] == "created"
    assert response_body["id"] is not None
    assert response_body["created_at"] is not None


def test_rejects_short_objective() -> None:
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
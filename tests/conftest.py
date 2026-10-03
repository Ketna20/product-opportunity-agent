from collections.abc import Generator
from fastapi.testclient import TestClient
from app.database import get_db_session
from app.main import app

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

TEST_DATABASE_URL = (
    "postgresql+psycopg://opportunity_user:"
    "opportunity_password@localhost:5433/product_opportunity_test"
)

test_engine = create_engine(TEST_DATABASE_URL)


@pytest.fixture
def db_session() -> Generator[Session, None, None]:
    connection = test_engine.connect()
    transaction = connection.begin()

    session = Session(
        bind=connection,
        join_transaction_mode="create_savepoint",
        expire_on_commit=False,
    )

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()



@pytest.fixture
def client(
    db_session: Session,
) -> Generator[TestClient, None, None]:
    def override_get_db_session() -> Generator[
        Session,
        None,
        None,
    ]:
        yield db_session

    app.dependency_overrides[get_db_session] = (
        override_get_db_session
    )

    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.clear()
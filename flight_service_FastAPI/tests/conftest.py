import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import Base, get_db
from main import app

# Import models so SQLAlchemy registers their tables.
from models.user import User
from models.flight import Flight
from models.booking import Booking


TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

if not TEST_DATABASE_URL:
    raise RuntimeError(
        "TEST_DATABASE_URL is not set. "
        "Configure it to point to flight_booking_test_db."
    )

test_engine = create_engine(
    TEST_DATABASE_URL,
    pool_pre_ping=True,
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine,
)


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    # Safety check: refuse to run against another database.
    if test_engine.url.database != "flight_booking_test_db":
        raise RuntimeError(
            f"Refusing to run tests against database: "
            f"{test_engine.url.database}"
        )

    Base.metadata.create_all(bind=test_engine)

    yield

    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def db_session():
    db = TestingSessionLocal()

    try:
        # Clean existing rows before this test.
        db.query(Booking).delete()
        db.query(Flight).delete()
        db.query(User).delete()
        db.commit()

        yield db

    finally:
        db.close()

@pytest.fixture
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    try:
        # Do not run the application's normal database startup lifespan.
        with TestClient(app, raise_server_exceptions=True) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.clear()
from typing import Generator
from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import sessionmaker

from app import crud
from app.db.base_class import Base
from app.main import app
from app.api import deps
from app.models.user import User
from app.schemas.user import UserCreate


TEST_SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    TEST_SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def memory_session():
    try:
        db = TestingSessionLocal()
        # Base.metadata.create_all(bind=db.connection().engine)
        yield db
    finally:
        db.close()


override_session = next(memory_session())


def override_get_session():
    return override_session


def override_get_current_user() -> User:
    return override_session.query(User).filter(User.id == 1).scalar()


def override_get_spotify_client() -> MagicMock:
    mock = MagicMock()
    mock.get_access_refresh_tokens.return_value = "access", "refresh", "user"
    return mock


@pytest.fixture()
def client() -> Generator:
    with TestClient(app) as client:
        app.dependency_overrides[deps.get_spotify_client] = override_get_spotify_client
        app.dependency_overrides[deps.get_current_user] = override_get_current_user
        app.dependency_overrides[deps.get_session] = override_get_session
        yield client
        app.dependency_overrides = {}


@pytest.fixture(autouse=True)
def run_around_tests():
    """
    Called before and after each test.
    """
    # Before
    Base.metadata.create_all(bind=engine)
    user_in = UserCreate(
        email="admin@admin.admin",
        name="admin",
        is_superuser=False,
        password="password",
    )
    crud.user.create(override_session, object_in=user_in)

    # Test
    yield

    # After
    Base.metadata.drop_all(bind=engine)

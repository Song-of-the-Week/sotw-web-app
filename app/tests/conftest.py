from datetime import datetime
from time import sleep
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
from app import schemas
from app.shared.utils import get_next_datetime


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
    mock.create_playlist.side_effect = [
        {"id": 1, "external_urls": {"spotify": "www.example1.com"}},
        {"id": 2, "external_urls": {"spotify": "www.example2.com"}},
        {"id": 3, "external_urls": {"spotify": "www.example3.com"}},
        {"id": 4, "external_urls": {"spotify": "www.example4.com"}},
    ]
    mock.add_songs_to_playlist.return_value = {}
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
    Called before and after each module.
    """
    # Before
    Base.metadata.create_all(bind=engine)
    # create initial user to be current_user
    user_in = schemas.UserCreate(
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


@pytest.fixture()
def sotw():
    # create a sotw for testing responses
    sotw_in = schemas.SotwCreate(
        name="test",
        results_datetime=datetime(1907, 3, 3, 8, 0).timestamp() * 1000,
        owner_id=1,
    )
    sotw = crud.sotw.create(session=override_session, object_in=sotw_in)
    return sotw


@pytest.fixture()
def current_week(sotw):
    # add current_user to the created sotw
    user = override_get_current_user()
    crud.user.add_user_to_sotw(session=override_session, db_object=user, object_in=sotw)

    # create week with future results release
    results_datetime = datetime(1907, 3, 3, 8, 0)
    next_results_release = get_next_datetime(
        target_day=results_datetime.weekday(),
        target_hour=results_datetime.hour,
        target_minute=results_datetime.minute,
    )
    first_week = schemas.WeekCreate(
        id=str(sotw.id) + "+12345678",
        week_num=1,
        playlist_link="www.example.com",
        sotw_id=sotw.id,
        next_results_release=next_results_release,
        responses=[],
    )
    # create the first week of this sotw
    current_week = crud.week.create(session=override_session, object_in=first_week)


@pytest.fixture()
def current_week_not_enough_players(sotw):
    # add current_user to the created sotw
    user = override_get_current_user()
    crud.user.add_user_to_sotw(session=override_session, db_object=user, object_in=sotw)

    # create week with future results release
    results_datetime = datetime(1907, 3, 3, 8, 0)
    next_results_release = (
        get_next_datetime(
            target_day=results_datetime.weekday(),
            target_hour=results_datetime.hour,
            target_minute=results_datetime.minute,
        )
        - 604800000
    )
    first_week = schemas.WeekCreate(
        id=str(sotw.id) + "+12345678",
        week_num=1,
        playlist_link="www.example.com",
        sotw_id=sotw.id,
        next_results_release=next_results_release,
        responses=[],
    )
    # create the first week of this sotw
    current_week = crud.week.create(session=override_session, object_in=first_week)

    return current_week


@pytest.fixture()
def current_week_not_enough_responses(sotw, current_week_not_enough_players):
    # create two new users to be added to the sotw
    user_in = schemas.UserCreate(
        email="a@b.c",
        name="test",
        is_superuser=False,
        password="password",
    )
    user = crud.user.create(override_session, object_in=user_in)
    crud.user.add_user_to_sotw(session=override_session, db_object=user, object_in=sotw)
    user_in = schemas.UserCreate(
        email="x@y.z",
        name="test",
        is_superuser=False,
        password="password",
    )
    user = crud.user.create(override_session, object_in=user_in)
    crud.user.add_user_to_sotw(session=override_session, db_object=user, object_in=sotw)

    return current_week_not_enough_players


@pytest.fixture()
def current_week_new_week(sotw, current_week_not_enough_responses):
    # need to add three responses to the sotw
    song_in = schemas.SongCreate(
        spotify_uri="abc123",
        name="Chosen One (Feat. Sonyae Elise)",
        spotify_link="www.spotify.com",
        submitter_id=1,
    )
    song = crud.song.create(session=override_session, object_in=song_in)
    response_in = schemas.ResponseCreate(
        next_song_id=song.id,
        matched_users_songs=[],
        picked_song_1_id=1,
        picked_song_2_id=2,
        sotw_id=sotw.id,
        week_id=current_week_not_enough_responses.id,
        submitter_id=1,
    )
    response = crud.response.create(session=override_session, object_in=response_in)
    crud.week.add_response_to_week(
        session=override_session,
        db_object=current_week_not_enough_responses,
        object_in=response,
    )

    song_in = schemas.SongCreate(
        spotify_uri="xyz789",
        name="Fragments From the Decade",
        spotify_link="www.spotify.com",
        submitter_id=2,
    )
    song = crud.song.create(session=override_session, object_in=song_in)
    response_in = schemas.ResponseCreate(
        next_song_id=song.id,
        matched_users_songs=[],
        picked_song_1_id=2,
        picked_song_2_id=3,
        sotw_id=sotw.id,
        week_id=current_week_not_enough_responses.id,
        submitter_id=2,
    )
    response = crud.response.create(session=override_session, object_in=response_in)
    crud.week.add_response_to_week(
        session=override_session,
        db_object=current_week_not_enough_responses,
        object_in=response,
    )

    song_in = schemas.SongCreate(
        spotify_uri="dfg456",
        name="Reanimator (feat. Yves Tumor)",
        spotify_link="www.spotify.com",
        submitter_id=3,
    )
    song = crud.song.create(session=override_session, object_in=song_in)
    response_in = schemas.ResponseCreate(
        next_song_id=song.id,
        matched_users_songs=[],
        picked_song_1_id=1,
        picked_song_2_id=3,
        sotw_id=sotw.id,
        week_id=current_week_not_enough_responses.id,
        submitter_id=3,
    )
    response = crud.response.create(session=override_session, object_in=response_in)
    crud.week.add_response_to_week(
        session=override_session,
        db_object=current_week_not_enough_responses,
        object_in=response,
    )

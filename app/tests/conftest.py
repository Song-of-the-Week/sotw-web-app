from datetime import datetime
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
        {"id": "abc123", "external_urls": {"spotify": "www.example1.com"}},
        {"id": "abc456", "external_urls": {"spotify": "www.example2.com"}},
        {"id": "abc789", "external_urls": {"spotify": "www.example3.com"}},
        {"id": "xyz123", "external_urls": {"spotify": "www.example4.com"}},
    ]
    mock.add_songs_to_playlist.return_value = {}
    mock.get_track_info.return_value = {
        "album": {
            "album_type": "album",
            "artists": [
                {
                    "external_urls": {
                        "spotify": "https://open.spotify.com/artist/2x9SpqnPi8rlE9pjHBwmSC"
                    },
                    "href": "https://api.spotify.com/v1/artists/2x9SpqnPi8rlE9pjHBwmSC",
                    "id": "2x9SpqnPi8rlE9pjHBwmSC",
                    "name": "Talking Heads",
                    "type": "artist",
                    "uri": "spotify:artist:2x9SpqnPi8rlE9pjHBwmSC",
                }
            ],
            "available_markets": [
                "AR",
                "AU",
                "AT",
                "BE",
                "BO",
                "BR",
                "BG",
                "CA",
                "CL",
                "CO",
                "CR",
                "CY",
                "CZ",
                "DK",
                "DO",
                "DE",
                "EC",
                "EE",
                "SV",
                "FI",
                "FR",
                "GR",
                "GT",
                "HN",
                "HK",
                "HU",
                "IS",
                "IE",
                "IT",
                "LV",
                "LT",
                "LU",
                "MY",
                "MT",
                "MX",
                "NL",
                "NZ",
                "NI",
                "NO",
                "PA",
                "PY",
                "PE",
                "PH",
                "PL",
                "PT",
                "SG",
                "SK",
                "ES",
                "SE",
                "CH",
                "TW",
                "TR",
                "UY",
                "US",
                "GB",
                "AD",
                "LI",
                "MC",
                "ID",
                "JP",
                "TH",
                "VN",
                "RO",
                "IL",
                "ZA",
                "SA",
                "AE",
                "BH",
                "QA",
                "OM",
                "KW",
                "EG",
                "MA",
                "DZ",
                "TN",
                "LB",
                "JO",
                "PS",
                "IN",
                "KZ",
                "MD",
                "UA",
                "AL",
                "BA",
                "HR",
                "ME",
                "MK",
                "RS",
                "SI",
                "KR",
                "BD",
                "PK",
                "LK",
                "GH",
                "KE",
                "NG",
                "TZ",
                "UG",
                "AG",
                "AM",
                "BS",
                "BB",
                "BZ",
                "BT",
                "BW",
                "BF",
                "CV",
                "CW",
                "DM",
                "FJ",
                "GM",
                "GE",
                "GD",
                "GW",
                "GY",
                "HT",
                "JM",
                "KI",
                "LS",
                "LR",
                "MW",
                "MV",
                "ML",
                "MH",
                "FM",
                "NA",
                "NR",
                "NE",
                "PW",
                "PG",
                "PR",
                "WS",
                "SM",
                "ST",
                "SN",
                "SC",
                "SL",
                "SB",
                "KN",
                "LC",
                "VC",
                "SR",
                "TL",
                "TO",
                "TT",
                "TV",
                "VU",
                "AZ",
                "BN",
                "BI",
                "KH",
                "CM",
                "TD",
                "KM",
                "GQ",
                "SZ",
                "GA",
                "GN",
                "KG",
                "LA",
                "MO",
                "MR",
                "MN",
                "NP",
                "RW",
                "TG",
                "UZ",
                "ZW",
                "BJ",
                "MG",
                "MU",
                "MZ",
                "AO",
                "CI",
                "DJ",
                "ZM",
                "CD",
                "CG",
                "IQ",
                "LY",
                "TJ",
                "VE",
                "ET",
                "XK",
            ],
            "external_urls": {
                "spotify": "https://open.spotify.com/album/39jsLMRmrTpfdq2vE4TCUe"
            },
            "href": "https://api.spotify.com/v1/albums/39jsLMRmrTpfdq2vE4TCUe",
            "id": "39jsLMRmrTpfdq2vE4TCUe",
            "images": [
                {
                    "url": "https://i.scdn.co/image/ab67616d0000b27391237668384c4d646b30c05c",
                    "width": 640,
                    "height": 640,
                },
                {
                    "url": "https://i.scdn.co/image/ab67616d00001e0291237668384c4d646b30c05c",
                    "width": 300,
                    "height": 300,
                },
                {
                    "url": "https://i.scdn.co/image/ab67616d0000485191237668384c4d646b30c05c",
                    "width": 64,
                    "height": 64,
                },
            ],
            "name": "More Songs About Buildings and Food",
            "release_date": "1978-07-14",
            "release_date_precision": "day",
            "total_tracks": 11,
            "type": "album",
            "uri": "spotify:album:39jsLMRmrTpfdq2vE4TCUe",
        },
        "artists": [
            {
                "external_urls": {
                    "spotify": "https://open.spotify.com/artist/2x9SpqnPi8rlE9pjHBwmSC"
                },
                "href": "https://api.spotify.com/v1/artists/2x9SpqnPi8rlE9pjHBwmSC",
                "id": "2x9SpqnPi8rlE9pjHBwmSC",
                "name": "Talking Heads",
                "type": "artist",
                "uri": "spotify:artist:2x9SpqnPi8rlE9pjHBwmSC",
            }
        ],
        "available_markets": [
            "AR",
            "AU",
            "AT",
            "BE",
            "BO",
            "BR",
            "BG",
            "CA",
            "CL",
            "CO",
            "CR",
            "CY",
            "CZ",
            "DK",
            "DO",
            "DE",
            "EC",
            "EE",
            "SV",
            "FI",
            "FR",
            "GR",
            "GT",
            "HN",
            "HK",
            "HU",
            "IS",
            "IE",
            "IT",
            "LV",
            "LT",
            "LU",
            "MY",
            "MT",
            "MX",
            "NL",
            "NZ",
            "NI",
            "NO",
            "PA",
            "PY",
            "PE",
            "PH",
            "PL",
            "PT",
            "SG",
            "SK",
            "ES",
            "SE",
            "CH",
            "TW",
            "TR",
            "UY",
            "US",
            "GB",
            "AD",
            "LI",
            "MC",
            "ID",
            "JP",
            "TH",
            "VN",
            "RO",
            "IL",
            "ZA",
            "SA",
            "AE",
            "BH",
            "QA",
            "OM",
            "KW",
            "EG",
            "MA",
            "DZ",
            "TN",
            "LB",
            "JO",
            "PS",
            "IN",
            "KZ",
            "MD",
            "UA",
            "AL",
            "BA",
            "HR",
            "ME",
            "MK",
            "RS",
            "SI",
            "KR",
            "BD",
            "PK",
            "LK",
            "GH",
            "KE",
            "NG",
            "TZ",
            "UG",
            "AG",
            "AM",
            "BS",
            "BB",
            "BZ",
            "BT",
            "BW",
            "BF",
            "CV",
            "CW",
            "DM",
            "FJ",
            "GM",
            "GE",
            "GD",
            "GW",
            "GY",
            "HT",
            "JM",
            "KI",
            "LS",
            "LR",
            "MW",
            "MV",
            "ML",
            "MH",
            "FM",
            "NA",
            "NR",
            "NE",
            "PW",
            "PG",
            "PR",
            "WS",
            "SM",
            "ST",
            "SN",
            "SC",
            "SL",
            "SB",
            "KN",
            "LC",
            "VC",
            "SR",
            "TL",
            "TO",
            "TT",
            "TV",
            "VU",
            "AZ",
            "BN",
            "BI",
            "KH",
            "CM",
            "TD",
            "KM",
            "GQ",
            "SZ",
            "GA",
            "GN",
            "KG",
            "LA",
            "MO",
            "MR",
            "MN",
            "NP",
            "RW",
            "TG",
            "UZ",
            "ZW",
            "BJ",
            "MG",
            "MU",
            "MZ",
            "AO",
            "CI",
            "DJ",
            "ZM",
            "CD",
            "CG",
            "IQ",
            "LY",
            "TJ",
            "VE",
            "ET",
            "XK",
        ],
        "disc_number": 1,
        "duration_ms": 302893,
        "explicit": False,
        "external_ids": {"isrc": "USWB19900863"},
        "external_urls": {
            "spotify": "https://open.spotify.com/track/1auuYcOrua5hrsGCS7idun"
        },
        "href": "https://api.spotify.com/v1/tracks/1auuYcOrua5hrsGCS7idun",
        "id": "1auuYcOrua5hrsGCS7idun",
        "is_local": False,
        "name": "Take Me to the River",
        "popularity": 44,
        "preview_url": "https://p.scdn.co/mp3-preview/4ee57e49e6790eaa4f44682ae5eb4a464ca418a2?cid=cfe923b2d660439caf2b557b21f31221",
        "track_number": 10,
        "type": "track",
        "uri": "spotify:track:1auuYcOrua5hrsGCS7idun",
    }
    return mock


def override_get_email_client() -> MagicMock:
    mock = MagicMock()
    mock.send_verification_email.return_value = {"MessageId": "test-id"}
    return mock


@pytest.fixture()
def client() -> Generator:
    with TestClient(app) as client:
        app.dependency_overrides[deps.get_spotify_client] = override_get_spotify_client
        app.dependency_overrides[deps.get_email_client] = override_get_email_client
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
        name="test1",
        is_superuser=False,
        password="password",
    )
    crud.user.create(override_session, object_in=user_in)
    # Test
    yield

    # After
    Base.metadata.drop_all(bind=engine)


def _create_song_response(
    spotify_id,
    name,
    spotify_link,
    submitter_id,
    sotw,
    week,
    picked_song_1_id: int = None,
    picked_song_2_id: int = None,
):
    # add song
    song_in = schemas.SongCreate(
        spotify_id=spotify_id,
        name=name,
        spotify_link=spotify_link,
        submitter_id=submitter_id,
    )
    song = crud.song.create(session=override_session, object_in=song_in)
    # add response
    response_in = schemas.ResponseCreate(
        next_song_id=song.id,
        sotw_id=sotw.id,
        week_id=week.id,
        submitter_id=submitter_id,
    )
    if picked_song_1_id is not None and picked_song_2_id is not None:
        response_in.picked_song_1_id = picked_song_1_id
        response_in.picked_song_2_id = picked_song_2_id
    response = crud.response.create(session=override_session, object_in=response_in)
    crud.week.add_response_to_week(
        session=override_session,
        db_object=week,
        object_in=response,
    )
    return response


def _create_user_song_match(response, user_id, song_id, correct):
    # add user_song_matches
    user_song_match_in = schemas.UserSongMatchCreate(
        user_id=user_id,
        song_id=song_id,
        correct_guess=correct,
        response_id=response.id,
    )
    crud.user_song_match.create(session=override_session, object_in=user_song_match_in)


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
    user_playlist_create = schemas.UserPlaylistCreate(
        playlist_id="abc123",
        playlist_link="www.spotify.com",
        sotw_id=sotw.id,
        user_id=user.id,
    )
    crud.user_playlist.create(session=override_session, object_in=user_playlist_create)

    # create week with past results release
    results_datetime = datetime(1907, 3, 3, 8, 0)
    next_results_release = (
        get_next_datetime(
            target_day=results_datetime.weekday(),
            target_hour=results_datetime.hour,
            target_minute=results_datetime.minute,
        )
        - 604800000
    )
    week_in = schemas.WeekCreate(
        id=str(sotw.id) + "+0",
        week_num=0,
        playlist_link="www.example.com",
        sotw_id=sotw.id,
        next_results_release=next_results_release,
        responses=[],
    )
    # create the first week of this sotw
    current_week = crud.week.create(session=override_session, object_in=week_in)

    return current_week


@pytest.fixture()
def current_week_not_enough_responses(sotw, current_week_not_enough_players):
    # create two new users to be added to the sotw
    # create new user with playlist
    user_in = schemas.UserCreate(
        email="a@b.c",
        name="test2",
        is_superuser=False,
        password="password",
    )
    user = crud.user.create(override_session, object_in=user_in)
    crud.user.add_user_to_sotw(session=override_session, db_object=user, object_in=sotw)
    user_playlist_create = schemas.UserPlaylistCreate(
        playlist_id="abc456",
        playlist_link="www.spotify.com",
        sotw_id=sotw.id,
        user_id=user.id,
    )
    crud.user_playlist.create(session=override_session, object_in=user_playlist_create)

    # create new user with playlist
    user_in = schemas.UserCreate(
        email="x@y.z",
        name="test3",
        is_superuser=False,
        password="password",
    )
    user = crud.user.create(override_session, object_in=user_in)
    crud.user.add_user_to_sotw(session=override_session, db_object=user, object_in=sotw)
    user_playlist_create = schemas.UserPlaylistCreate(
        playlist_id="xyz123",
        playlist_link="www.spotify.com",
        sotw_id=sotw.id,
        user_id=user.id,
    )
    crud.user_playlist.create(session=override_session, object_in=user_playlist_create)

    return current_week_not_enough_players


@pytest.fixture()
def current_week_new_week(sotw, current_week_not_enough_responses):
    # need to add three responses to the week
    _create_song_response(
        spotify_id="6OmApaLQPqHZL3iI78FOUR",
        name="Doctor Worm - They Might Be Giants",
        spotify_link="https://open.spotify.com/track/6OmApaLQPqHZL3iI78FOUR?si=971c343da7fb4847",
        submitter_id=1,
        sotw=sotw,
        week=current_week_not_enough_responses,
    )

    _create_song_response(
        spotify_id="5mqceEgI5vhogd5pOAlwUO",
        name="Headlock - Snail Mail",
        spotify_link="https://open.spotify.com/track/5mqceEgI5vhogd5pOAlwUO?si=e3562627d25e4957",
        submitter_id=2,
        sotw=sotw,
        week=current_week_not_enough_responses,
    )

    _create_song_response(
        spotify_id="4JfpJrrGNXRj2yXm1fYV23",
        name="Lithonia - Childish Gambino",
        spotify_link="https://open.spotify.com/track/4JfpJrrGNXRj2yXm1fYV23?si=4366647118a34603",
        submitter_id=3,
        sotw=sotw,
        week=current_week_not_enough_responses,
    )

    return current_week_not_enough_responses


@pytest.fixture()
def current_week_new_week_new_results(sotw, current_week_new_week):
    # create week with past results release
    results_datetime = datetime(1907, 3, 3, 8, 0)
    next_results_release = (
        get_next_datetime(
            target_day=results_datetime.weekday(),
            target_hour=results_datetime.hour,
            target_minute=results_datetime.minute,
        )
        - 604800000
    )
    week_in = schemas.WeekCreate(
        id=str(sotw.id) + "+123456789",
        week_num=1,
        playlist_link="www.example.com",
        sotw_id=sotw.id,
        next_results_release=next_results_release,
        responses=[],
    )
    # create the first week of this sotw
    current_week = crud.week.create(session=override_session, object_in=week_in)

    # need to add three responses to the week
    # add song and response
    response_1 = _create_song_response(
        spotify_id="6OmApaLQPqHZL3iI78FOUR",
        name="Doctor Worm - They Might Be Giants",
        spotify_link="https://open.spotify.com/track/6OmApaLQPqHZL3iI78FOUR?si=971c343da7fb4847",
        submitter_id=1,
        sotw=sotw,
        week=current_week,
        picked_song_1_id=2,
        picked_song_2_id=3,
    )
    # add user_song_matches
    _create_user_song_match(response=response_1, user_id=1, song_id=1, correct=True)
    _create_user_song_match(response=response_1, user_id=2, song_id=2, correct=True)
    _create_user_song_match(response=response_1, user_id=3, song_id=3, correct=True)
    # update response
    crud.response.update(
        session=override_session,
        db_object=response_1,
        object_in=schemas.ResponseUpdate(number_correct_matches=3),
    )

    # add song and response
    response_2 = _create_song_response(
        spotify_id="5mqceEgI5vhogd5pOAlwUO",
        name="Headlock - Snail Mail",
        spotify_link="https://open.spotify.com/track/5mqceEgI5vhogd5pOAlwUO?si=e3562627d25e4957",
        submitter_id=2,
        sotw=sotw,
        week=current_week,
        picked_song_1_id=1,
        picked_song_2_id=3,
    )
    # add user_song_matches
    _create_user_song_match(response=response_2, user_id=1, song_id=3, correct=False)
    _create_user_song_match(response=response_2, user_id=2, song_id=2, correct=True)
    _create_user_song_match(response=response_2, user_id=3, song_id=1, correct=False)
    # update response
    crud.response.update(
        session=override_session,
        db_object=response_2,
        object_in=schemas.ResponseUpdate(number_correct_matches=1),
    )

    # add song and response
    response_3 = _create_song_response(
        spotify_id="4JfpJrrGNXRj2yXm1fYV23",
        name="Lithonia - Childish Gambino",
        spotify_link="https://open.spotify.com/track/4JfpJrrGNXRj2yXm1fYV23?si=4366647118a34603",
        submitter_id=3,
        sotw=sotw,
        week=current_week,
        picked_song_1_id=1,
        picked_song_2_id=2,
    )
    # add user_song_matches
    _create_user_song_match(response=response_3, user_id=1, song_id=1, correct=True)
    _create_user_song_match(response=response_3, user_id=2, song_id=3, correct=False)
    _create_user_song_match(response=response_3, user_id=3, song_id=2, correct=False)
    # update response
    crud.response.update(
        session=override_session,
        db_object=response_3,
        object_in=schemas.ResponseUpdate(number_correct_matches=1),
    )


@pytest.fixture()
def current_week_new_week_plus_1(sotw, current_week_new_week):
    # add one more user and response to sotw
    user_in = schemas.UserCreate(
        email="l@m.n",
        name="test4",
        is_superuser=False,
        password="password",
    )
    user = crud.user.create(override_session, object_in=user_in)
    crud.user.add_user_to_sotw(session=override_session, db_object=user, object_in=sotw)

    _create_song_response(
        spotify_id="1auuYcOrua5hrsGCS7idun",
        name="Take Me to the River - Talking Heads",
        spotify_link="https://open.spotify.com/track/1auuYcOrua5hrsGCS7idun?si=3ff1ee3bab954296",
        submitter_id=4,
        sotw=sotw,
        week=current_week_new_week,
    )

    return current_week_new_week

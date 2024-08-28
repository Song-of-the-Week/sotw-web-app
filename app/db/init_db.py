from datetime import datetime
import json
import sys
from loguru import logger
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app import crud
from app import schemas
from app.shared.utils import get_next_datetime


def _create_user(session, email, name, password, is_superuser: bool = False):
    user_in = schemas.UserCreate(
        email=email,
        name=name,
        is_superuser=is_superuser,
        password=password,
    )
    return crud.user.create(session, object_in=user_in)


def _create_song_response(
    session,
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
    song = crud.song.create(session=session, object_in=song_in)
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
    response = crud.response.create(session=session, object_in=response_in)
    crud.week.add_response_to_week(
        session=session,
        db_object=week,
        object_in=response,
    )
    return response


def _create_user_song_match(session, response, user_id, song_id, correct):
    # add user_song_matches
    user_song_match_in = schemas.UserSongMatchCreate(
        user_id=user_id,
        song_id=song_id,
        correct_guess=correct,
        response_id=response.id,
    )
    crud.user_song_match.create(session=session, object_in=user_song_match_in)


def _create_user_playlist(session, sotw_id, user_id):
    user_playlist_create = schemas.UserPlaylistCreate(
        playlist_id="3CiqmMz5FynlRAQXyexlbP",
        playlist_link="https://open.spotify.com/playlist/3CiqmMz5FynlRAQXyexlbP?si=25abf5c1d8a14a7a",
        sotw_id=sotw_id,
        user_id=user_id,
    )
    crud.user_playlist.create(session, object_in=user_playlist_create)


def init_db(session: Session):
    # 1-m, 2-t, 3-w, 4-th, 5-f, 6-sat, 7-sun
    results_datetime = datetime(1907, 4, 3, 8, 0)
    next_results_release = (
        get_next_datetime(
            target_day=results_datetime.weekday(),
            target_hour=results_datetime.hour,
            target_minute=results_datetime.minute,
        )
        # - 604800000 subtract a week
    )
    # create a superuser (admin)
    superuser = crud.user.get_by_email(session, email="admin@admin.admin")
    if not superuser:
        superuser = _create_user(
            session=session,
            email="admin@admin.admin",
            name="admin",
            password="password",
            is_superuser=True,
        )
    # create 3 normal users
    user1 = _create_user(
        session=session,
        email="test1@admin.admin",
        name="test1",
        password="password",
    )
    user2 = _create_user(
        session=session,
        email="test2@admin.admin",
        name="test2",
        password="password",
    )
    user3 = _create_user(
        session=session,
        email="test3@admin.admin",
        name="test3",
        password="password",
    )

    # create sotw1 and user playlists
    sotw_in = schemas.SotwCreate(
        name="sotw1",
        results_datetime=datetime(1907, 4, 3, 8, 0).timestamp() * 1000,
        owner_id=superuser.id,
        master_playlist_link="https://open.spotify.com/playlist/3CiqmMz5FynlRAQXyexlbP?si=25abf5c1d8a14a7a",
        master_playlist_id="3CiqmMz5FynlRAQXyexlbP",
        soty_playlist_link="https://open.spotify.com/playlist/3CiqmMz5FynlRAQXyexlbP?si=25abf5c1d8a14a7a",
        soty_playlist_id="3CiqmMz5FynlRAQXyexlbP",
    )
    sotw1 = crud.sotw.create(session, object_in=sotw_in)
    crud.user.add_user_to_sotw(session=session, db_object=superuser, object_in=sotw1)
    crud.user.add_user_to_sotw(session=session, db_object=user1, object_in=sotw1)
    crud.user.add_user_to_sotw(session=session, db_object=user2, object_in=sotw1)
    crud.user.add_user_to_sotw(session=session, db_object=user3, object_in=sotw1)
    _create_user_playlist(session=session, sotw_id=sotw1.id, user_id=superuser.id)
    _create_user_playlist(session=session, sotw_id=sotw1.id, user_id=user1.id)
    _create_user_playlist(session=session, sotw_id=sotw1.id, user_id=user2.id)
    _create_user_playlist(session=session, sotw_id=sotw1.id, user_id=user3.id)
    # create week 0 for sotw1 (release 1 week ago)
    week_in = schemas.WeekCreate(
        id=str(sotw1.id) + "+0",
        week_num=0,
        playlist_link="",
        sotw_id=sotw1.id,
        next_results_release=next_results_release - 604800000,
        responses=[],
    )
    sotw1_week0 = crud.week.create(session=session, object_in=week_in)
    # create the responses to week 0 for sotw1 for normal users
    _create_song_response(
        session=session,
        spotify_id="6OmApaLQPqHZL3iI78FOUR",
        name="Doctor Worm - They Might Be Giants",
        spotify_link="https://open.spotify.com/track/6OmApaLQPqHZL3iI78FOUR?si=971c343da7fb4847",
        submitter_id=user1.id,
        sotw=sotw1,
        week=sotw1_week0,
    )
    _create_song_response(
        session=session,
        spotify_id="5mqceEgI5vhogd5pOAlwUO",
        name="Headlock - Snail Mail",
        spotify_link="https://open.spotify.com/track/5mqceEgI5vhogd5pOAlwUO?si=e3562627d25e4957",
        submitter_id=user2.id,
        sotw=sotw1,
        week=sotw1_week0,
    )
    _create_song_response(
        session=session,
        spotify_id="4JfpJrrGNXRj2yXm1fYV23",
        name="Lithonia - Childish Gambino",
        spotify_link="https://open.spotify.com/track/4JfpJrrGNXRj2yXm1fYV23?si=4366647118a34603",
        submitter_id=user3.id,
        sotw=sotw1,
        week=sotw1_week0,
    )

    # create sotw2 and create user playlists
    sotw_in = schemas.SotwCreate(
        name="sotw2",
        results_datetime=datetime(1907, 4, 3, 8, 0).timestamp() * 1000,
        owner_id=superuser.id,
        master_playlist_link="https://open.spotify.com/playlist/3CiqmMz5FynlRAQXyexlbP?si=25abf5c1d8a14a7a",
        master_playlist_id="3CiqmMz5FynlRAQXyexlbP",
        soty_playlist_link="https://open.spotify.com/playlist/3CiqmMz5FynlRAQXyexlbP?si=25abf5c1d8a14a7a",
        soty_playlist_id="3CiqmMz5FynlRAQXyexlbP",
    )
    sotw2 = crud.sotw.create(session, object_in=sotw_in)
    crud.user.add_user_to_sotw(session=session, db_object=superuser, object_in=sotw2)
    crud.user.add_user_to_sotw(session=session, db_object=user1, object_in=sotw2)
    crud.user.add_user_to_sotw(session=session, db_object=user2, object_in=sotw2)
    crud.user.add_user_to_sotw(session=session, db_object=user3, object_in=sotw2)
    _create_user_playlist(session=session, sotw_id=sotw2.id, user_id=superuser.id)
    _create_user_playlist(session=session, sotw_id=sotw2.id, user_id=user1.id)
    _create_user_playlist(session=session, sotw_id=sotw2.id, user_id=user2.id)
    _create_user_playlist(session=session, sotw_id=sotw2.id, user_id=user3.id)
    # create week 0 for sotw2 (release 2 week ago)
    week_in = schemas.WeekCreate(
        id=str(sotw2.id) + "+0",
        week_num=0,
        playlist_link="",
        sotw_id=sotw2.id,
        next_results_release=next_results_release - (604800000 * 2),
        responses=[],
    )
    sotw2_week0 = crud.week.create(session=session, object_in=week_in)
    # create the responses to week 0 for sotw2 for everyone
    _create_song_response(
        session=session,
        spotify_id="3lPr8ghNDBLc2uZovNyLs9",
        name="Supermassive Black Hole - Muse",
        spotify_link="https://open.spotify.com/track/3lPr8ghNDBLc2uZovNyLs9?si=e39aaef4c57940a0",
        submitter_id=superuser.id,
        sotw=sotw2,
        week=sotw2_week0,
    )
    _create_song_response(
        session=session,
        spotify_id="0yLsJKNJHmSnmSGl3ZodYn",
        name="Acid Rain - Chance the Rapper",
        spotify_link="https://open.spotify.com/track/0yLsJKNJHmSnmSGl3ZodYn?si=a91ac9357d464bbd",
        submitter_id=user1.id,
        sotw=sotw2,
        week=sotw2_week0,
    )
    _create_song_response(
        session=session,
        spotify_id="1gk3FhAV07q9Jg77UxnVjX",
        name="Gooey - Glass Animals",
        spotify_link="https://open.spotify.com/track/1gk3FhAV07q9Jg77UxnVjX?si=a8dbb98132d74ba6",
        submitter_id=user2.id,
        sotw=sotw2,
        week=sotw2_week0,
    )
    _create_song_response(
        session=session,
        spotify_id="5h68SoVFGleijCtjEja3xG",
        name="365 - Charli xcx",
        spotify_link="https://open.spotify.com/track/5h68SoVFGleijCtjEja3xG?si=1e3400a5bb94439f",
        submitter_id=user3.id,
        sotw=sotw2,
        week=sotw2_week0,
    )
    # create week 1 for sotw2 (release 1 week ago)
    survey = {
        "songs": [
            {
                "id": 4,
                "name": "Supermassive Black Hole - Muse",
            },
            {
                "id": 5,
                "name": "Acid Rain - Chance the Rapper",
            },
            {
                "id": 6,
                "name": "Gooey - Glass Animals",
            },
            {
                "id": 7,
                "name": "365 - Charli xcx",
            },
        ],
        "users": [
            {
                "id": 1,
                "name": "admin",
                "matched": False,
            },
            {
                "id": 2,
                "name": "test1",
                "matched": False,
            },
            {
                "id": 3,
                "name": "test2",
                "matched": False,
            },
            {
                "id": 4,
                "name": "test3",
                "matched": False,
            },
        ],
    }
    week_in = schemas.WeekCreate(
        id=str(sotw2.id) + f"+{next_results_release - (604800000 * 2)}",
        week_num=1,
        playlist_link="https://open.spotify.com/playlist/3CiqmMz5FynlRAQXyexlbP?si=25abf5c1d8a14a7a",
        sotw_id=sotw2.id,
        next_results_release=next_results_release - (604800000),
        responses=[],
        survey=json.dumps(survey),
    )
    sotw2_week1 = crud.week.create(session=session, object_in=week_in)
    # create responses for week 1 for sotw2 for normal users
    response = _create_song_response(
        session=session,
        spotify_id="4atMrAadB7dS8xn9vfk9PQ",
        name="Fireside - Arctic Monkeys",
        spotify_link="https://open.spotify.com/track/4atMrAadB7dS8xn9vfk9PQ?si=c89df3effd344411",
        submitter_id=user1.id,
        sotw=sotw2,
        week=sotw2_week1,
        picked_song_1_id=7,
        picked_song_2_id=6,
    )
    # add user_song_matches
    _create_user_song_match(
        session=session, response=response, user_id=1, song_id=6, correct=False
    )
    _create_user_song_match(
        session=session, response=response, user_id=2, song_id=5, correct=True
    )
    _create_user_song_match(
        session=session, response=response, user_id=3, song_id=4, correct=False
    )
    _create_user_song_match(
        session=session, response=response, user_id=4, song_id=7, correct=True
    )
    # update response
    session.refresh(response)
    crud.response.update(
        session=session,
        db_object=response,
        object_in=schemas.ResponseUpdate(number_correct_matches=2),
    )

    response = _create_song_response(
        session=session,
        spotify_id="4xIhSUJantE6BMl3u8dtCJ",
        name="Father Time (feat. Sampha) - Kendrick Lamar, Sampha",
        spotify_link="https://open.spotify.com/track/4xIhSUJantE6BMl3u8dtCJ?si=d595104656934d7f",
        submitter_id=user2.id,
        sotw=sotw2,
        week=sotw2_week1,
        picked_song_1_id=7,
        picked_song_2_id=4,
    )
    # add user_song_matches
    _create_user_song_match(
        session=session, response=response, user_id=1, song_id=5, correct=False
    )
    _create_user_song_match(
        session=session, response=response, user_id=2, song_id=7, correct=False
    )
    _create_user_song_match(
        session=session, response=response, user_id=3, song_id=6, correct=True
    )
    _create_user_song_match(
        session=session, response=response, user_id=4, song_id=4, correct=False
    )
    # update response
    session.refresh(response)
    crud.response.update(
        session=session,
        db_object=response,
        object_in=schemas.ResponseUpdate(number_correct_matches=1),
    )

    response = _create_song_response(
        session=session,
        spotify_id="0EYOdF5FCkgOJJla8DI2Md",
        name="B.Y.O.B. - System Of A Down",
        spotify_link="https://open.spotify.com/track/0EYOdF5FCkgOJJla8DI2Md?si=1406da7e9ef04230",
        submitter_id=user3.id,
        sotw=sotw2,
        week=sotw2_week1,
        picked_song_1_id=4,
        picked_song_2_id=6,
    )
    # add user_song_matches
    _create_user_song_match(
        session=session, response=response, user_id=1, song_id=6, correct=False
    )
    _create_user_song_match(
        session=session, response=response, user_id=2, song_id=4, correct=False
    )
    _create_user_song_match(
        session=session, response=response, user_id=3, song_id=5, correct=False
    )
    _create_user_song_match(
        session=session, response=response, user_id=4, song_id=7, correct=True
    )
    # update response
    session.refresh(response)
    crud.response.update(
        session=session,
        db_object=response,
        object_in=schemas.ResponseUpdate(number_correct_matches=1),
    )

    # create sotw3
    # create week 0 for sotw2 (release 2 weeks ago)
    # create the responses to week 0 for sotw2
    # create week 1 for sotw2 (release next wednesday)
    # create responses for week 1 for sotw2 for normal users


def main():
    logger.info("Creating inital data")
    with SessionLocal() as session:
        init_db(session)
    logger.info("Initial data created")


if __name__ == '__main__':
    sys.exit(main())
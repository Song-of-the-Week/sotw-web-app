from datetime import datetime
import json
import random
from unittest.mock import patch

from app.shared.config import cfg
from app.shared.utils import get_next_datetime


def test_get_current_week_404(client):
    # When
    response = client.get(f"{cfg.API_V1_STR}/week/3/current_week")

    # Then
    assert response.status_code == 404


def test_get_current_week_403(client, sotw):
    # When
    response = client.get(f"{cfg.API_V1_STR}/week/1/current_week")

    # Then
    assert response.status_code == 403


def test_get_current_week_success_week_0(client):
    # When
    # "link" spotify
    payload = {
        "state": "admin@admin.admin-test1",
        "code": "success",
    }
    response = client.put(
        f"{cfg.API_V1_STR}/auth/spotify-access-token", data=json.dumps(payload)
    )
    # create sotw
    results_time = (
        get_next_datetime(
            datetime.now().day, datetime.now().hour, datetime.now().minute
        )
        - 604800000
    )
    payload = {
        "name": "test_sotw",
        "results_datetime": results_time,
        "results_timezone": "America/New_York",
    }
    response = client.post(f"{cfg.API_V1_STR}/sotw/", data=json.dumps(payload))
    data = response.json()
    sotw_id = data["id"]

    response = client.get(f"{cfg.API_V1_STR}/week/{sotw_id}/current_week")
    data = response.json()

    # Then
    assert response.status_code == 200
    assert "id" in data.keys()
    assert data["id"] == str(sotw_id) + "+0"
    assert "week_num" in data.keys()
    assert data["week_num"] == 0
    assert "playlist_link" in data.keys()
    assert data["playlist_link"] == ""
    assert "next_results_release" in data.keys()
    assert data["next_results_release"] == results_time + 604800000
    assert "survey" in data.keys()
    assert data["survey"] == ""
    assert "submitted" in data.keys()
    assert data["submitted"] == False


def test_get_current_week_success_week_n(client, current_week):
    # When
    response = client.get(f"{cfg.API_V1_STR}/week/1/current_week")
    data = response.json()

    # Then
    assert response.status_code == 200
    assert "id" in data.keys()
    assert data["id"] == "1+12345678"
    assert "week_num" in data.keys()
    assert data["week_num"] == 1
    assert "playlist_link" in data.keys()
    assert data["playlist_link"] == "www.example.com"
    assert "survey" in data.keys()
    assert data["survey"] == ""
    assert "submitted" in data.keys()
    assert data["submitted"] == False


def test_get_current_week_n_406_not_enough_players(
    client, current_week_not_enough_players
):
    # When
    response = client.get(f"{cfg.API_V1_STR}/week/1/current_week")
    data = response.json()

    # Then
    assert response.status_code == 200
    assert "week" in data.keys()
    assert data["week"]["week_num"] == 0
    assert "status" in data.keys()
    assert data["status"] == 406
    assert "message" in data.keys()
    assert (
        data["message"]
        == "You will need at least three players in your Song of the Week competition in order to continue playing."
    )


def test_get_current_week_n_406_not_enough_responses(
    client, current_week_not_enough_responses
):
    # When
    response = client.get(f"{cfg.API_V1_STR}/week/1/current_week")
    data = response.json()

    # Then
    assert response.status_code == 200
    assert "week" in data.keys()
    assert data["week"]["week_num"] == 0
    assert "status" in data.keys()
    assert data["status"] == 406
    assert "message" in data.keys()
    assert (
        data["message"]
        == "Please make sure everyone has submitted their surveys for the week. Looks like we're still waiting on 3 players to submit: test1, test2, and test3"
    )


def test_get_current_week_success_week_n_new_week(client, current_week_new_week):
    # When
    response = client.get(f"{cfg.API_V1_STR}/week/1/current_week")
    data = response.json()

    results_datetime = datetime(1907, 3, 3, 8, 0)
    next_results_release = (
        get_next_datetime(
            target_day=results_datetime.weekday(),
            target_hour=results_datetime.hour,
            target_minute=results_datetime.minute,
        )
        - 604800000
    )

    # Then
    assert response.status_code == 200
    assert "id" in data.keys()
    assert data["id"] == f"1+{next_results_release}"
    assert "week_num" in data.keys()
    assert data["week_num"] == 1
    assert "playlist_link" in data.keys()
    assert (
        data["playlist_link"] == "www.example1.com"
        or data["playlist_link"] == "www.example4.com"
    )
    assert "survey" in data.keys()
    assert "submitted" in data.keys()
    assert data["submitted"] == False
    assert "theme" in data.keys()
    assert data["theme"] == "test theme"
    assert "theme_description" in data.keys()
    assert data["theme_description"] == "test theme description"

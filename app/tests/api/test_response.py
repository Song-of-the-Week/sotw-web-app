import json
from app.shared.config import cfg


def test_post_response_404_sotw_not_found(client):
    # When
    payload = {
        "next_song": "https://open.spotify.com/track/0xzBmAsCfu3AzX1W0GYtMJ?si=baf54c28de79487f",
    }
    response = client.post(f"{cfg.API_V1_STR}/response/3/0", data=json.dumps(payload))
    data = response.json()

    # Then
    assert response.status_code == 404
    assert data["detail"] == "Sotw with given id 3 not found."


def test_post_response_403(client, sotw):
    # When
    payload = {
        "next_song": "https://open.spotify.com/track/0xzBmAsCfu3AzX1W0GYtMJ?si=baf54c28de79487f",
    }
    response = client.post(f"{cfg.API_V1_STR}/response/1/0", data=json.dumps(payload))

    # Then
    assert response.status_code == 403


def test_post_response_404_week_not_found(client):
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
    results_time = 1720719000000 - 604800000
    payload = {
        "name": "test_sotw",
        "results_datetime": results_time,
        "results_timezone": "America/New_York",
    }
    response = client.post(f"{cfg.API_V1_STR}/sotw/", data=json.dumps(payload))
    data = response.json()
    sotw_id = data["id"]

    payload = {
        "next_song": "https://open.spotify.com/track/0xzBmAsCfu3AzX1W0GYtMJ?si=baf54c28de79487f",
    }
    response = client.post(
        f"{cfg.API_V1_STR}/response/{sotw_id}/0", data=json.dumps(payload)
    )
    data = response.json()

    assert response.status_code == 404
    assert data["detail"] == "This song of the week competition hasn't started yet!"


def test_post_response_406(client, current_week):
    # When
    payload = {
        "next_song": "https://open.spotify.com/track/0xzBmAsCfu3AzX1W0GYtMJ?si=baf54c28de79487f",
    }
    response = client.post(f"{cfg.API_V1_STR}/response/1/4", data=json.dumps(payload))

    # Then
    assert response.status_code == 406


def test_post_response_success_week_0(client):
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
    results_time = 1720719000000 - 604800000
    payload = {
        "name": "test_sotw",
        "results_datetime": results_time,
        "results_timezone": "America/New_York",
    }
    response = client.post(f"{cfg.API_V1_STR}/sotw/", data=json.dumps(payload))
    data = response.json()
    sotw_id = data["id"]
    # create week 0
    client.get(f"{cfg.API_V1_STR}/week/{sotw_id}/current_week")

    payload = {
        "next_song": "https://open.spotify.com/track/0xzBmAsCfu3AzX1W0GYtMJ?si=baf54c28de79487f",
    }
    response = client.post(
        f"{cfg.API_V1_STR}/response/{sotw_id}/0", data=json.dumps(payload)
    )
    data = response.json()

    assert response.status_code == 201
    assert "repeat" in data.keys()
    assert data["repeat"] == False

    # check to see if the week shows that the current user has submitted
    response = client.get(f"{cfg.API_V1_STR}/week/{sotw_id}/current_week")
    data = response.json()

    assert response.status_code == 200
    assert "submitted" in data.keys()
    assert data["submitted"] == True


def test_post_response_400(client, current_week):
    # When
    payload = {
        "picked_song_1": 0,
        "picked_song_2": 1,
        "user_song_matches": [
            {
                "song_id": 46,
                "user_id": 1,
            },
        ],
        "next_song": "https://open.spotify.com/track/0xzBmAsCfu3AzX1W0GYtMJ?si=baf54c28de79487f",
    }
    response = client.post(f"{cfg.API_V1_STR}/response/1/1", data=json.dumps(payload))
    data = response.json()

    # Then
    assert response.status_code == 400
    assert (
        data["detail"]
        == "There's something wrong with your request. A song with the given id 46 does not exist."
    )


def test_post_response_success_week_n_no_repeat(client, current_week_new_week):
    # When
    # kick off the new week
    response = client.get(f"{cfg.API_V1_STR}/week/1/current_week")

    # post a response
    payload = {
        "picked_song_1": 1,
        "picked_song_2": 2,
        "user_song_matches": [
            {
                "song_id": 1,
                "user_id": 1,
            },
            {
                "song_id": 2,
                "user_id": 2,
            },
            {
                "song_id": 3,
                "user_id": 3,
            },
        ],
        "next_song": "https://open.spotify.com/track/1auuYcOrua5hrsGCS7idun?si=f951bceb14204344",
    }
    response = client.post(f"{cfg.API_V1_STR}/response/1/1", data=json.dumps(payload))
    data = response.json()

    # Then
    assert response.status_code == 201
    assert "repeat" in data.keys()
    assert not data["repeat"]


def test_post_response_success_week_n_repeat(client, current_week_new_week_plus_1):
    # When
    # kick off the new week
    response = client.get(f"{cfg.API_V1_STR}/week/1/current_week")

    # post a response
    payload = {
        "picked_song_1": 1,
        "picked_song_2": 2,
        "user_song_matches": [
            {
                "song_id": 1,
                "user_id": 1,
            },
            {
                "song_id": 2,
                "user_id": 2,
            },
            {
                "song_id": 3,
                "user_id": 3,
            },
        ],
        "next_song": "https://open.spotify.com/track/1auuYcOrua5hrsGCS7idun?si=f951bceb14204344",
    }
    response = client.post(f"{cfg.API_V1_STR}/response/1/1", data=json.dumps(payload))
    data = response.json()

    # Then
    assert response.status_code == 201
    assert "repeat" in data.keys()
    assert data["repeat"] == True


def test_post_response_success_week_n_repeat_approved(
    client, current_week_new_week_plus_1
):
    # When
    # kick off the new week
    response = client.get(f"{cfg.API_V1_STR}/week/1/current_week")

    # post a response
    payload = {
        "picked_song_1": 1,
        "picked_song_2": 2,
        "user_song_matches": [
            {
                "song_id": 1,
                "user_id": 1,
            },
            {
                "song_id": 2,
                "user_id": 2,
            },
            {
                "song_id": 3,
                "user_id": 3,
            },
        ],
        "next_song": "https://open.spotify.com/track/1auuYcOrua5hrsGCS7idun?si=f951bceb14204344",
        "repeat_approved": True,
    }
    response = client.post(f"{cfg.API_V1_STR}/response/1/1", data=json.dumps(payload))
    data = response.json()

    # Then
    assert response.status_code == 201
    assert "repeat" in data.keys()
    assert not data["repeat"]


def test_post_response_success_week_n_replace_existing_response(
    client, current_week_new_week
):
    # When
    # kick off the new week
    response = client.get(f"{cfg.API_V1_STR}/week/1/current_week")

    # post a response
    payload = {
        "picked_song_1": 1,
        "picked_song_2": 2,
        "user_song_matches": [
            {
                "song_id": 1,
                "user_id": 2,
            },
            {
                "song_id": 2,
                "user_id": 3,
            },
            {
                "song_id": 3,
                "user_id": 1,
            },
        ],
        "next_song": "https://open.spotify.com/track/1auuYcOrua5hrsGCS7idun?si=f951bceb14204344",
    }
    response = client.post(f"{cfg.API_V1_STR}/response/1/1", data=json.dumps(payload))
    data = response.json()

    # Then
    assert response.status_code == 201
    assert "repeat" in data.keys()
    assert data["repeat"] == False

    # kick off the new week
    response = client.get(f"{cfg.API_V1_STR}/week/1/current_week")

    # post a response
    payload = {
        "picked_song_1": 3,
        "picked_song_2": 2,
        "user_song_matches": [
            {
                "song_id": 1,
                "user_id": 1,
            },
            {
                "song_id": 2,
                "user_id": 2,
            },
            {
                "song_id": 3,
                "user_id": 3,
            },
        ],
        "next_song": "https://open.spotify.com/track/1auuYcOrua5hrsGCS7idun?si=f951bceb14204344",
    }
    response = client.post(f"{cfg.API_V1_STR}/response/1/1", data=json.dumps(payload))
    data = response.json()

    # Then
    assert response.status_code == 201
    assert "repeat" in data.keys()
    assert data["repeat"] == False


def test_get_response_success(client, current_week_new_week_new_results):
    # When
    url = f"{cfg.API_V1_STR}/response/1/1"
    response = client.get(url)
    data = response.json()

    # Then
    assert response.status_code == 200
    assert len(data["user_song_matches"]) == 3
    assert data["user_song_matches"][0]["song_id"] == "1"
    assert data["user_song_matches"][0]["user_id"] == "1"
    assert data["user_song_matches"][1]["user_id"] == "2"
    assert data["user_song_matches"][1]["user_id"] == "2"
    assert data["user_song_matches"][2]["user_id"] == "3"
    assert data["user_song_matches"][2]["user_id"] == "3"
    assert data["picked_song_1_id"] == "2"
    assert data["picked_song_2_id"] == "3"
    assert data["submitter_id"] == "1"
    assert (
        data["next_song"]
        == "https://open.spotify.com/track/6OmApaLQPqHZL3iI78FOUR?si=971c343da7fb4847"
    )


def test_get_response_wrong_user(client, current_week_new_week_new_results):
    # When
    url = f"{cfg.API_V1_STR}/response/1/2"
    response = client.get(url)
    data = response.json()

    # Then
    assert response.status_code == 403

from datetime import datetime
import json
from unittest.mock import MagicMock, patch

from app.clients.spotify import SpotifyClient
from app.main import app
from app.api import deps
from app.models.user import User
from app.shared.config import cfg
from app.tests.conftest import memory_session, override_session


def test_sotw_creation_406(client):
    # When
    payload = {
        "name": "test_sotw",
        "results_datetime": round(datetime.now().timestamp() * 1000),
    }
    response = client.post(f"{cfg.API_V1_STR}/sotw/", data=json.dumps(payload))

    # Then
    assert response.status_code == 406


def test_sotw_creation_success(client):
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
    payload = {
        "name": "test_sotw",
        "results_datetime": round(datetime.now().timestamp() * 1000),
    }
    response = client.post(f"{cfg.API_V1_STR}/sotw/", data=json.dumps(payload))
    data = response.json()

    # Then
    assert response.status_code == 201
    assert "name" in data.keys()
    assert data["name"] == "test_sotw"
    assert "master_playlist_link" in data.keys()
    assert data["master_playlist_link"] == "www.example1.com"
    assert "soty_playlist_link" in data.keys()
    assert data["soty_playlist_link"] == "www.example2.com"
    assert "owner_id" in data.keys()
    assert int(data["owner_id"]) == 1


def test_sotw_update_403(client, sotw_other_owner):
    # When
    payload = {
        "name": "new_name",
        "results_datetime": -1980399600000,
    }
    response = client.put(f"{cfg.API_V1_STR}/sotw/1", data=json.dumps(payload))

    # Then
    assert response.status_code == 403


def test_sotw_update_success(client):
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
    payload = {
        "name": "test_sotw",
        "results_datetime": round(datetime.now().timestamp() * 1000),
    }
    response = client.post(f"{cfg.API_V1_STR}/sotw/", data=json.dumps(payload))
    data = response.json()

    # When
    payload = {
        "name": "new_name",
        "results_datetime": -1980399600000,
    }
    response = client.put(f"{cfg.API_V1_STR}/sotw/1", data=json.dumps(payload))
    data = response.json()

    # Then
    assert response.status_code == 200
    assert "name" in data.keys()
    assert data["name"] == "new_name"
    assert "results_datetime" in data.keys()
    assert data["results_datetime"] == -1980399600000


def test_get_sotw_404(client):
    # When
    response = client.get(f"{cfg.API_V1_STR}/sotw/3")

    # Then
    assert response.status_code == 404


def test_get_sotw_403(client, sotw):
    # When
    response = client.get(f"{cfg.API_V1_STR}/sotw/1")

    # Then
    assert response.status_code == 403


def test_get_sotw_success(client):
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
    payload = {
        "name": "test_sotw",
        "results_datetime": round(datetime.now().timestamp() * 1000),
    }
    response = client.post(f"{cfg.API_V1_STR}/sotw/", data=json.dumps(payload))
    data = response.json()

    response = client.get(f"{cfg.API_V1_STR}/sotw/{data['id']}")
    data = response.json()

    # Then
    assert response.status_code == 200
    assert "name" in data.keys()
    assert data["name"] == "test_sotw"


def test_get_sotw_invite_link_404(client):
    # When
    response = client.get(f"{cfg.API_V1_STR}/sotw/3/invite")

    # Then
    assert response.status_code == 404


def test_get_sotw_invite_link_403(client, sotw):
    # When
    response = client.get(f"{cfg.API_V1_STR}/sotw/1/invite")

    # Then
    assert response.status_code == 403


@patch("app.core.auth._create_token")
def test_get_sotw_invite_link_success(_create_token, client):
    # Mock
    _create_token.return_value = "123ABC"
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
    payload = {
        "name": "test_sotw",
        "results_datetime": round(datetime.now().timestamp() * 1000),
    }
    response = client.post(f"{cfg.API_V1_STR}/sotw/", data=json.dumps(payload))
    data = response.json()

    response = client.get(f"{cfg.API_V1_STR}/sotw/{data['id']}/invite")
    data = response.json()

    # Then
    assert response.status_code == 200
    assert "url" in data.keys()
    assert data["url"] == "sotw/invite/123ABC"


def test_get_sotw_invite_pending_403(client):
    # When
    response = client.get(f"{cfg.API_V1_STR}/sotw/invite/pending/ABC123")

    # Then
    assert response.status_code == 403


@patch("app.api.api_v1.endpoints.sotw.jwt.decode")
def test_get_sotw_invite_pending_404(decode, client):
    # Mock
    decode.return_value = {"sub": 3}
    # When
    response = client.get(f"{cfg.API_V1_STR}/sotw/invite/pending/ABC123")

    # Then
    assert response.status_code == 404


@patch("app.api.api_v1.endpoints.sotw.jwt.decode")
def test_get_sotw_invite_pending_already_in_success(decode, client):
    # Mock
    decode.return_value = {"sub": 1}
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
    payload = {
        "name": "test_sotw",
        "results_datetime": round(datetime.now().timestamp() * 1000),
    }
    response = client.post(f"{cfg.API_V1_STR}/sotw/", data=json.dumps(payload))

    response = client.get(f"{cfg.API_V1_STR}/sotw/invite/pending/ABC123")
    data = response.json()

    # Then
    assert response.status_code == 200
    assert "already_in" in data.keys()
    assert data["already_in"] == True


@patch("app.api.api_v1.endpoints.sotw.jwt.decode")
def test_get_sotw_invite_pending_success(decode, client, sotw):
    # Mock
    decode.return_value = {"sub": 1}
    # When
    response = client.get(f"{cfg.API_V1_STR}/sotw/invite/pending/ABC123")
    data = response.json()

    # Then
    assert response.status_code == 200
    assert "already_in" in data.keys()
    assert data["already_in"] == False
    assert "id" in data.keys()
    assert int(data["id"]) == 1


def test_get_sotw_invite_join_403(client):
    # When
    # "link" spotify
    payload = {
        "state": "admin@admin.admin-test1",
        "code": "success",
    }
    response = client.put(
        f"{cfg.API_V1_STR}/auth/spotify-access-token", data=json.dumps(payload)
    )

    response = client.get(f"{cfg.API_V1_STR}/sotw/invite/join/ABC123")

    # Then
    assert response.status_code == 403


@patch("app.api.api_v1.endpoints.sotw.jwt.decode")
def test_get_sotw_invite_join_404(decode, client):
    # Mock
    decode.return_value = {"sub": 3}
    # When
    # "link" spotify
    payload = {
        "state": "admin@admin.admin-test1",
        "code": "success",
    }
    response = client.put(
        f"{cfg.API_V1_STR}/auth/spotify-access-token", data=json.dumps(payload)
    )

    response = client.get(f"{cfg.API_V1_STR}/sotw/invite/join/ABC123")

    # Then
    assert response.status_code == 404


def test_get_sotw_invite_join_406(client):
    # When
    response = client.get(f"{cfg.API_V1_STR}/sotw/invite/join/ABC123")

    # Then
    assert response.status_code == 406


@patch("app.api.api_v1.endpoints.sotw.jwt.decode")
def test_get_sotw_invite_join_400(decode, client, sotw):
    # Mock
    decode.return_value = {"sub": 1}

    # When
    response = client.get(f"{cfg.API_V1_STR}/auth/current_user")
    data = response.json()

    # Then
    assert "playlists" in data.keys()
    assert len(data["playlists"]) == 0
    assert "sotw_list" in data.keys()
    assert len(data["sotw_list"]) == 0

    # When
    # "link" spotify
    payload = {
        "state": "admin@admin.admin-test1",
        "code": "success",
    }
    response = client.put(
        f"{cfg.API_V1_STR}/auth/spotify-access-token", data=json.dumps(payload)
    )

    # Override the dependencie for this test
    mock_spotify = MagicMock()
    mock_spotify.create_playlist.side_effect = Exception("Spotify API Error")

    client.app.dependency_overrides[deps.get_spotify_client] = lambda: mock_spotify

    response = client.get(f"{cfg.API_V1_STR}/sotw/invite/join/ABC123")

    data = response.json()

    # Then
    assert response.status_code == 400
    assert "detail" in data.keys()
    assert data["detail"] == "An error occurred: 'Spotify API Error'"

    response = client.get(f"{cfg.API_V1_STR}/auth/current_user")
    data = response.json()

    assert "playlists" in data.keys()
    assert len(data["playlists"]) == 0
    assert "sotw_list" in data.keys()
    assert len(data["sotw_list"]) == 0


@patch("app.api.api_v1.endpoints.sotw.jwt.decode")
def test_get_sotw_invite_join_success(decode, client, sotw):
    # Mock
    decode.return_value = {"sub": 1}

    # When
    response = client.get(f"{cfg.API_V1_STR}/auth/current_user")
    data = response.json()

    # Then
    assert "playlists" in data.keys()
    assert len(data["playlists"]) == 0
    assert "sotw_list" in data.keys()
    assert len(data["sotw_list"]) == 0

    # When
    # "link" spotify
    payload = {
        "state": "admin@admin.admin-test1",
        "code": "success",
    }
    response = client.put(
        f"{cfg.API_V1_STR}/auth/spotify-access-token", data=json.dumps(payload)
    )

    response = client.get(f"{cfg.API_V1_STR}/sotw/invite/join/ABC123")
    data = response.json()

    # Then
    assert response.status_code == 200
    assert "id" in data.keys()
    assert int(data["id"]) == 1

    response = client.get(f"{cfg.API_V1_STR}/auth/current_user")
    data = response.json()

    assert "playlists" in data.keys()
    assert len(data["playlists"]) == 1
    assert "sotw_list" in data.keys()
    assert len(data["sotw_list"]) == 1


def test_get_leave_sotw_404(client, current_week):
    # When
    response = client.get(f"{cfg.API_V1_STR}/sotw/4/leave")
    data = response.json()

    # Then
    assert response.status_code == 404
    assert "detail" in data.keys()
    assert data["detail"] == "Sotw with given id 4 not found."


def test_get_leave_sotw_not_in(client, sotw):
    # When
    response = client.get(f"{cfg.API_V1_STR}/sotw/1/leave")
    data = response.json()

    # Then
    assert response.status_code == 200
    assert "sotw_list" in data.keys()
    assert len(data["sotw_list"]) == 0


def test_get_leave_sotw_success(client, current_week):
    # When
    response = client.get(f"{cfg.API_V1_STR}/auth/current_user")
    data = response.json()

    # Then
    assert "sotw_list" in data.keys()
    assert len(data["sotw_list"]) == 1

    # When
    response = client.get(f"{cfg.API_V1_STR}/sotw/1/leave")
    data = response.json()

    # Then
    assert response.status_code == 200
    assert "sotw_list" in data.keys()
    assert len(data["sotw_list"]) == 0


@patch("app.api.api_v1.endpoints.sotw.jwt.decode")
def test_get_leave_sotw_success_and_rejoin_with_same_playlist(decode, client, sotw):
    # Mock
    decode.return_value = {"sub": 1}

    # When
    response = client.get(f"{cfg.API_V1_STR}/auth/current_user")
    data = response.json()

    # Then
    assert "playlists" in data.keys()
    assert len(data["playlists"]) == 0
    assert "sotw_list" in data.keys()
    assert len(data["sotw_list"]) == 0

    # When
    # "link" spotify
    payload = {
        "state": "admin@admin.admin-test1",
        "code": "success",
    }
    response = client.put(
        f"{cfg.API_V1_STR}/auth/spotify-access-token", data=json.dumps(payload)
    )

    response = client.get(f"{cfg.API_V1_STR}/sotw/invite/join/ABC123")
    data = response.json()

    # Then
    assert response.status_code == 200
    assert "id" in data.keys()
    assert int(data["id"]) == 1

    response = client.get(f"{cfg.API_V1_STR}/auth/current_user")
    data = response.json()

    assert "playlists" in data.keys()
    assert len(data["playlists"]) == 1
    assert "sotw_list" in data.keys()
    assert len(data["sotw_list"]) == 1

    # When
    response = client.get(f"{cfg.API_V1_STR}/sotw/1/leave")
    data = response.json()

    # Then
    assert response.status_code == 200
    assert "playlists" in data.keys()
    assert len(data["playlists"]) == 1
    assert "sotw_list" in data.keys()
    assert len(data["sotw_list"]) == 0

    playlist_id = data["playlists"][0]["id"]

    # Rejoin
    response = client.get(f"{cfg.API_V1_STR}/sotw/invite/join/ABC123")
    data = response.json()

    # When
    response = client.get(f"{cfg.API_V1_STR}/auth/current_user")
    data = response.json()

    # Then
    assert "playlists" in data.keys()
    assert len(data["playlists"]) == 1
    assert data["playlists"][0]["id"] == playlist_id
    assert "sotw_list" in data.keys()
    assert len(data["sotw_list"]) == 1

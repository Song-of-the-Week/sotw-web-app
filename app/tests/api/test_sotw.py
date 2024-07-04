from datetime import datetime
import json
from unittest.mock import patch

from app.shared.config import cfg


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
        "state": "admin@admin.admin-admin",
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
    assert data["owner_id"] == 1


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
        "state": "admin@admin.admin-admin",
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
        "state": "admin@admin.admin-admin",
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
        "state": "admin@admin.admin-admin",
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
    assert data["id"] == 1


def test_get_sotw_invite_join_403(client):
    # When
    # "link" spotify
    payload = {
        "state": "admin@admin.admin-admin",
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
        "state": "admin@admin.admin-admin",
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
def test_get_sotw_invite_join_success(decode, client, sotw):
    # Mock
    decode.return_value = {"sub": 1}
    # When
    # "link" spotify
    payload = {
        "state": "admin@admin.admin-admin",
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
    assert data["id"] == 1

    response = client.get(f"{cfg.API_V1_STR}/auth/current_user")
    data = response.json()

    assert "playlists" in data.keys()
    assert len(data["playlists"]) == 1
    assert "sotw_list" in data.keys()
    assert len(data["sotw_list"]) == 1

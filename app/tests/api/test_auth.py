import json

from app.shared.config import cfg


def test_login_400(client):
    # When
    payload = {
        "username": "fake_user",
        "password": "fake_password",
    }
    response = client.post(f"{cfg.API_V1_STR}/auth/login", data=payload)

    # Then
    assert response.status_code == 400


def test_login_success(client):
    # When
    payload = {
        "username": "admin@admin.admin",
        "password": "password",
    }
    response = client.post(f"{cfg.API_V1_STR}/auth/login", data=payload)
    data = response.json()

    # Then
    assert response.status_code == 200
    assert "name" in data.keys()
    assert data["name"] == "test1"


def test_logout(client):
    # When
    response = client.get(f"{cfg.API_V1_STR}/auth/logout")
    data = response.json()

    # Then
    assert response.status_code == 200
    assert "status" in data.keys()
    assert data["status"] == 200


def test_get_current_user(client):
    # When
    response = client.get(f"{cfg.API_V1_STR}/auth/current_user")
    data = response.json()

    # Then
    assert response.status_code == 200
    assert "name" in data.keys()
    assert data["name"] == "test1"


def test_register_400(client):
    # When
    payload = {
        "email": "admin@admin.admin",
        "name": "admin",
        "password": "password",
    }
    response = client.post(f"{cfg.API_V1_STR}/auth/register", data=json.dumps(payload))

    # Then
    assert response.status_code == 400


def test_register_success(client):
    # When
    payload = {
        "email": "example@example.example",
        "name": "example",
        "password": "password",
    }
    response = client.post(f"{cfg.API_V1_STR}/auth/register", data=json.dumps(payload))
    data = response.json()

    # Then
    assert response.status_code == 201
    assert "name" in data.keys()
    assert data["name"] == "example"


def test_spotify_client(client):
    # When
    response = client.get(f"{cfg.API_V1_STR}/auth/spotify-client-id")
    data = response.json()

    # Then
    assert response.status_code == 200
    assert "client_id" in data.keys()
    assert data["client_id"] == cfg.SPOTIFY_CLIENT_ID


def test_spotify_access_token_401(client):
    # When
    payload = {
        "state": "bad-state",
        "code": "failure",
    }
    response = client.put(
        f"{cfg.API_V1_STR}/auth/spotify-access-token", data=json.dumps(payload)
    )

    # Then
    assert response.status_code == 401


def test_spotify_access_token_202(client):
    # When
    payload = {
        "state": "admin@admin.admin-test1",
        "error": "failure",
    }
    response = client.put(
        f"{cfg.API_V1_STR}/auth/spotify-access-token", data=json.dumps(payload)
    )
    data = response.json()

    # Then
    assert response.status_code == 202
    assert "spotify_linked" in data.keys()
    assert data["spotify_linked"] == False


def test_spotify_access_token_success(client):
    # When
    payload = {
        "state": "admin@admin.admin-test1",
        "code": "success",
    }
    response = client.put(
        f"{cfg.API_V1_STR}/auth/spotify-access-token", data=json.dumps(payload)
    )
    data = response.json()

    # Then
    assert response.status_code == 202
    assert "spotify_linked" in data.keys()
    assert data["spotify_linked"] == True

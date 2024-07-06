import json
from unittest.mock import patch

from app.models.user import User
from app.shared.config import cfg


def test_update_user_wrong_id_403(client):
    # When
    payload = {
        "email": "badmin@badmin.badmin",
        "name": "badmin",
    }
    response = client.put(f"{cfg.API_V1_STR}/user/{3}", data=json.dumps(payload))
    data = response.json()
    print(f"HELLLLLOOOO {data}")

    # Then
    assert response.status_code == 403
    assert data["detail"] == "Not authorized to update."


def test_update_user_wrong_password_403(client):
    # When
    payload = {
        "current_password": "badword",
        "new_password": "badminbadmin",
    }
    response = client.put(f"{cfg.API_V1_STR}/user/{1}", data=json.dumps(payload))
    data = response.json()

    # Then
    assert response.status_code == 403
    assert data["detail"] == "Incorrect password."


def test_update_user_password_change_success(client):
    # First verify current password works
    payload = {
        "username": "admin@admin.admin",
        "password": "password",
    }
    response = client.post(f"{cfg.API_V1_STR}/auth/login", data=payload)

    # Then
    assert response.status_code == 200

    # Change password
    payload = {
        "current_password": "password",
        "new_password": "badminbadmin",
    }
    response = client.put(f"{cfg.API_V1_STR}/user/{1}", data=json.dumps(payload))

    # Then
    assert response.status_code == 200

    # Verify old password doesn't work
    payload = {
        "username": "admin@admin.admin",
        "password": "password",
    }
    response = client.post(f"{cfg.API_V1_STR}/auth/login", data=payload)

    # Then
    assert response.status_code == 400

    # Verify new password works
    payload = {
        "username": "admin@admin.admin",
        "password": "badminbadmin",
    }
    response = client.post(f"{cfg.API_V1_STR}/auth/login", data=payload)

    # Then
    assert response.status_code == 200


def test_update_user_unlink_spotify_success(client):
    # First, link user's spotify
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

    # Unlink spotify
    payload = {
        "spotify_linked": False,
    }
    response = client.put(f"{cfg.API_V1_STR}/user/{1}", data=json.dumps(payload))
    data = response.json()

    # Then
    assert response.status_code == 200
    assert "spotify_linked" in data.keys()
    assert data["spotify_linked"] == False


def test_delete_user_403(client):
    # When
    payload = {
        "email": "example@example.example",
        "name": "example",
        "password": "password",
    }
    response = client.post(f"{cfg.API_V1_STR}/auth/register", data=json.dumps(payload))
    data = response.json()

    response = client.delete(f"{cfg.API_V1_STR}/user/{data['id']}")
    data = response.json()

    # Then
    assert response.status_code == 403
    assert data["detail"] == "Not authorized to delete."


def test_delete_user_success(client):
    # When
    response = client.delete(f"{cfg.API_V1_STR}/user/1")
    data = response.json()

    # Then
    assert response.status_code == 200
    assert data["id"] == 1

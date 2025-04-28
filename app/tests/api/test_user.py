import json
from unittest.mock import patch

from jose import JWTError

from app.shared.config import cfg


def test_update_user_wrong_id_403(client):
    # When
    payload = {
        "email": "badmin@badmin.badmin",
        "name": "badmin",
    }
    response = client.put(f"{cfg.API_V1_STR}/user/{3}", data=json.dumps(payload))
    data = response.json()

    # Then
    assert response.status_code == 403
    assert data["detail"] == "Not authorized to update."


def test_update_user_wrong_password_400(client):
    # When
    payload = {
        "current_password": "badword",
        "new_password": "badminbadmin",
    }
    response = client.put(f"{cfg.API_V1_STR}/user/{1}", data=json.dumps(payload))
    data = response.json()

    # Then
    assert response.status_code == 400
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


def test_update_user_email_success(client):
    # Change email
    payload = {
        "email": "email@email.email",
    }
    response = client.put(f"{cfg.API_V1_STR}/user/{1}", data=json.dumps(payload))
    data = response.json()

    # Then
    assert response.status_code == 200
    assert "email" in data.keys()
    assert data["email"] == "email@email.email"


@patch("app.api.api_v1.endpoints.user.jwt.decode")
def test_verify_email_change_success(decode, client):
    decode.return_value = {"sub": "email@email.email"}
    # When
    response = client.get(f"{cfg.API_V1_STR}/user/verify/exampletoken")
    data = response.json()

    # Then
    assert response.status_code == 200
    assert "email" in data.keys()
    assert data["email"] == "email@email.email"


def test_reset_password_request_404(client):
    # When
    payload = {
        "email": "email@email.email",
    }
    response = client.post(
        f"{cfg.API_V1_STR}/user/reset-password", data=json.dumps(payload)
    )
    data = response.json()

    assert response.status_code == 404
    assert data["detail"] == "No user found with email email@email.email."


def test_reset_password_request_success(client):
    # When
    payload = {
        "email": "admin@admin.admin",
    }
    response = client.post(
        f"{cfg.API_V1_STR}/user/reset-password", data=json.dumps(payload)
    )

    assert response.status_code == 200


def test_reset_password_change_400(client):
    # When
    payload = {}
    response = client.post(
        f"{cfg.API_V1_STR}/user/reset-password-change/exampletoken",
        data=json.dumps(payload),
    )
    data = response.json()

    # Then
    assert response.status_code == 400
    assert data["detail"] == "Request payload is incomplete."


@patch("app.api.api_v1.endpoints.user.jwt.decode")
def test_reset_password_change_404(decode, client):
    decode.return_value = {"sub": "email@email.email"}
    # When
    payload = {"new_password": "password"}
    response = client.post(
        f"{cfg.API_V1_STR}/user/reset-password-change/exampletoken",
        data=json.dumps(payload),
    )
    data = response.json()

    # Then
    assert response.status_code == 404
    assert (
        data["detail"]
        == "It seems that there is something wrong with your verification token. Please try resetting your password again."
    )


@patch("app.api.api_v1.endpoints.user.jwt.decode")
def test_reset_password_change_403(decode, client):
    decode.side_effect = JWTError()
    # When
    payload = {"new_password": "password"}
    response = client.post(
        f"{cfg.API_V1_STR}/user/reset-password-change/exampletoken",
        data=json.dumps(payload),
    )
    data = response.json()

    # Then
    assert response.status_code == 403
    assert data["detail"] == "The token is no longer valid."


@patch("app.api.api_v1.endpoints.user.jwt.decode")
def test_reset_password_change_success(decode, client):
    # When
    payload = {
        "username": "admin@admin.admin",
        "password": "new_password",
    }
    response = client.post(f"{cfg.API_V1_STR}/auth/login", data=payload)

    # Then
    assert response.status_code == 400

    decode.return_value = {"sub": "admin@admin.admin"}

    # When
    payload = {"new_password": "new_password"}
    response = client.post(
        f"{cfg.API_V1_STR}/user/reset-password-change/exampletoken",
        data=json.dumps(payload),
    )

    # Then
    assert response.status_code == 200

    # When
    payload = {
        "username": "admin@admin.admin",
        "password": "new_password",
    }
    response = client.post(f"{cfg.API_V1_STR}/auth/login", data=payload)
    data = response.json()

    # Then
    assert response.status_code == 200
    assert "email" in data.keys()
    assert data["email"] == "admin@admin.admin"


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
    assert int(data["id"]) == 1

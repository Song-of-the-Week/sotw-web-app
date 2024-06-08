from datetime import datetime
import json
import requests
import base64
from typing import Dict
from loguru import logger
from sqlalchemy.orm.session import Session
from app import crud, schemas
from app.shared.config import cfg


class SpotifyClient:
    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret

    def get_access_refresh_tokens(self, code):
        """
        Retrieve the initial access and refresh tokens with the given code and then get the user info

        Args:
            code (str): an authorization code returned from spotify

        Returns:
            dict: the json data response from the access token request
        """
        # get access token
        response = requests.post(
            "https://accounts.spotify.com/api/token",
            data={
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": cfg.SPOTIFY_CALLBACK_URI,
            },
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "Authorization": f"Basic {base64.urlsafe_b64encode((cfg.SPOTIFY_CLIENT_ID + ':' + cfg.SPOTIFY_CLIENT_SECRET).encode()).decode()}",
            },
        )

        if response.status_code != 200:
            logger.error(response.json())
            response.raise_for_status()

        data = response.json()
        access_token = data["access_token"]
        refresh_token = data["refresh_token"]

        # get user id
        response = requests.get(
            "https://api.spotify.com/v1/me",
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "Authorization": f"Bearer {access_token}",
            },
        )

        if response.status_code != 200:
            logger.error(response.json())
            response.raise_for_status()

        data = response.json()
        spotify_user_id = data["id"]

        return access_token, refresh_token, spotify_user_id

    def get_user_access_token(self, session: Session, user_id: int):
        """
        Retrieve the access token for a user given their ID

        Args:
            session (Session): a sqlalchemy session
            user_id (int): a user id

        Returns:
            User: the user with an updated access token
        """
        user = crud.user.get(session=session, id=user_id)

        # check to see if the user's access token is still valid
        response = requests.get(
            "https://api.spotify.com/v1/me",
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "Authorization": f"Bearer {user.spotify_access_token}",
            },
        )
        # if the user's access token is not expired, return the user with current access token
        if response.status_code == 200:
            return user
        elif response.status_code == 401:
            # refresh the user's access token
            response = requests.post(
                "https://accounts.spotify.com/api/token",
                data=json.dumps(
                    {
                        "grant_type": "refresh_token",
                        "refresh_token": user.spotify_refresh_token,
                    }
                ),
                headers={
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Authorization": f"Basic {base64.urlsafe_b64encode((cfg.SPOTIFY_CLIENT_ID + ':' + cfg.SPOTIFY_CLIENT_SECRET).encode()).decode()}",
                },
            )

            if response.status_code != 200:
                logger.error(response.json())
                response.raise_for_status()

            data = response.json()
            object_in = schemas.UserUpdate(
                spotify_linked=True,
                spotify_access_token=data["access_token"],
                spotify_refresh_token=data["refresh_token"],
                spotify_accessed_date=datetime.utcnow(),
            )

            return crud.user.update(
                session=session, db_object=user, object_in=object_in
            )
        else:
            logger.error(response.json())
            response.raise_for_status()

    def create_playlist(
        self,
        playlist_name: str,
        playlist_description: str,
        session: Session,
        user_id: int,
    ) -> Dict:
        user = self.get_user_access_token(session, user_id)

        response = requests.post(
            f"https://api.spotify.com/v1/users/{user.spotify_user_id}/playlists",
            data=json.dumps(
                {
                    "name": playlist_name,
                    "description": playlist_description,
                    "public": True,
                }
            ),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {user.spotify_access_token}",
            },
        )
        if response.status_code != 201:
            logger.error(response.json())
            response.raise_for_status()

        return response.json()

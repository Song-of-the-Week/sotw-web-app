from datetime import datetime
import json
import requests
import base64
from typing import Dict, List
from loguru import logger
from sqlalchemy.orm.session import Session
from app import crud, schemas
from app.models.user import User
from app.shared.config import cfg


class SpotifyClient:
    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret

    def get_access_refresh_tokens(self, code) -> Dict:
        """
        Retrieve the initial access and refresh tokens with the given code and then get the user info.

        Args:
            code (str): an authorization code returned from spotify.

        Returns:
            Dict: the json data response from the access token request.
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
                "Authorization": f"Basic {base64.urlsafe_b64encode((self.client_id + ':' + self.client_secret).encode()).decode()}",
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
            logger.error(f"ERROR STATUS: {response.status_code}")
            logger.error(f"ERROR RESPONSE CONTENT: {response.content}")
            logger.error(f"ERROR RESPONSE: {response}")
            logger.error(response.json())
            response.raise_for_status()

        data = response.json()
        spotify_user_id = data["id"]

        return access_token, refresh_token, spotify_user_id

    def get_user_access_token(self, session: Session, user_id: int) -> User:
        """
        Retrieve the access token for a user given their ID.

        Args:
            session (Session): A SQLAlchemy Session object that is connected to the database.
            user_id (int): ID of a user.

        Returns:
            User: The user with an updated access token.
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
                    "Authorization": f"Basic {base64.urlsafe_b64encode((self.client_id + ':' + self.client_secret).encode()).decode()}",
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
        """
        Create a Spotify playlist for the user specified by user_id.

        Args:
            playlist_name (str): Name of the playlist to create.
            playlist_description (str): Description of the playlist to create.
            session (Session): A SQLAlchemy Session object that is connected to the database.
            user_id (int): ID of the user to create a playlist for.

        Returns:
            Dict: The response from Spotify with the playlist details.
        """
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

    def add_songs_to_playlist(
        self, playlist_id: str, uris: List[str], session: Session, user_id: int
    ) -> Dict:
        """
        Add songs to an existing Spotify playlist.

        Args:
            playlist_id (str): The Spotify ID of the playlist to add to.
            uris (List[str]): A list of Spotify track URIs to be added to the playlist.
            session (Session): A SQLAlchemy Session object that is connected to the database.
            user_id (int): ID of the user who's playlist is being added to.

        Returns:
            Dict: The response from Spotify after adding the tracks,
        """
        user = self.get_user_access_token(session, user_id)

        response = requests.post(
            f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks",
            data=json.dumps(
                {
                    "uris": uris,
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

    def get_track_info(self, track_id: str, session: Session, user_id: int) -> Dict:
        """
        Get the track details from Spotify for a given track_id

        Args:
            track_id (str): The Spotify ID of the track being retreived.
            session (Session): A SQLAlchemy Session object that is connected to the database.
            user_id (int): The ID of the user who's crednetials are being used to look the track up.

        Returns:
            Dict: The Spotify response with the track details.
        """
        user = self.get_user_access_token(session, user_id)

        # get track info
        response = requests.get(
            f"https://api.spotify.com/v1/tracks/{track_id}",
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "Authorization": f"Bearer {user.spotify_access_token}",
            },
        )

        if response.status_code != 200:
            logger.error(response.json())
            response.raise_for_status()

        return response.json()

import requests
import base64
from typing import Dict


class SpotifyClient:
    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token = None

    def get_token(self):
        url = "https://accounts.spotify.com/api/token"
        headers = {
            "Authorization": "Basic "
            + base64.b64encode(
                f"{self.client_id}:{self.client_secret}".encode()
            ).decode()
        }
        data = {"grant_type": "client_credentials"}
        response = requests.post(url, headers=headers, data=data)
        response_data = response.json()
        self.token = response_data["access_token"]

    def get_song_details(self, song_id: str) -> Dict:
        if not self.token:
            self.get_token()

        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.get(
            f"https://api.spotify.com/v1/tracks/{song_id}", headers=headers
        )
        if response.status_code != 200:
            raise Exception(f"Failed to fetch song details: {response.status_code}")

        return response.json()

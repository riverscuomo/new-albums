import logging
import spotipy
from spotipy.oauth2 import SpotifyOAuth

from .config import (
    SPOTIFY_USER,
    SPOTIFY_REDIRECT_URI,
    scope,
    SPOTIFY_CLIENT_ID,
    SPOTIFY_CLIENT_SECRET,
)


def get_spotify(timeout=20) -> spotipy.Spotify:
    logging.info("[get_spotify] Creating Spotify client")
    print(SPOTIFY_REDIRECT_URI)

    # This code currently uses the deprecated username parameter.
    token = SpotifyOAuth(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        redirect_uri=SPOTIFY_REDIRECT_URI,
        scope=scope,
        username=SPOTIFY_USER,
        requests_timeout=timeout,
    )

    spotify = spotipy.Spotify(auth_manager=token, requests_timeout=timeout)
    return spotify

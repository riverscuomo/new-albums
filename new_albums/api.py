import os
import logging
from contextlib import suppress
from json.decoder import JSONDecodeError
import spotipy

# from spotipy.util import prompt_for_user_token
from spotipy.oauth2 import SpotifyOAuth

from new_albums.config import (
    SPOTIFY_USER,
    SPOTIFY_REDIRECT_URI,
    scope,
    SPOTIFY_CLIENT_ID,
    SPOTIFY_CLIENT_SECRET,
    spotify_scope_warning,
)


def get_spotify(timeout=20) -> spotipy.Spotify:
    logging.info("[get_spotify] Creating Spotify client")

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

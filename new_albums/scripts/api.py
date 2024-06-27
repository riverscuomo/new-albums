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


def get_spotify(timeout: int = 20) -> spotipy.Spotify:
    """
    Creates a Spotify client using the provided timeout value.

    Args:
        timeout (int): The timeout value for requests in seconds.

    Returns:
        spotipy.Spotify: A Spotify client instance.

    Raises:
        None
    """

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

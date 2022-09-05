import os
import logging
from json.decoder import JSONDecodeError

from new_albums.config import SPOTIFY_USER, SPOTIFY_REDIRECT_URI, scope, SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, spotify_scope_warning

import spotipy
from spotipy.util import prompt_for_user_token


def get_spotify() -> spotipy.Spotify:
    logging.info("get_spotify...")

    token = None
    spotify = None

    # TODO: Perhaps have this logic in a loop until it gets the correct credentials
    try:
        token = prompt_for_user_token(
            SPOTIFY_USER,
            redirect_uri=SPOTIFY_REDIRECT_URI,
            scope=scope,
            client_id=SPOTIFY_CLIENT_ID,
            client_secret=SPOTIFY_CLIENT_SECRET,
        )
    except (AttributeError, JSONDecodeError):
        os.remove(f".cache-{SPOTIFY_USER}")
        token = prompt_for_user_token(
            SPOTIFY_USER,
            redirect_uri=SPOTIFY_REDIRECT_URI,
            scope=scope,
            client_id=SPOTIFY_CLIENT_ID,
            client_secret=SPOTIFY_CLIENT_SECRET,
        )

    if token:
        spotify = spotipy.Spotify(auth=token)
    else:
        logging.warn(spotify_scope_warning)
        raise ValueError(spotify_scope_warning)
    return spotify

import os
import logging
from json.decoder import JSONDecodeError

from new_albums.config import *
import spotipy
from spotipy import util


def get_spotify() -> spotipy.Spotify:
    logging.info("get_spotify...")

    token = None
    spotify = None

    try:
        token = util.prompt_for_user_token(
            SPOTIFY_USER,
            redirect_uri=SPOTIFY_REDIRECT_URI,
            scope=scope,
            client_id=SPOTIFY_CLIENT_ID,
            client_secret=SPOTIFY_CLIENT_SECRET,
        )
    except (AttributeError, JSONDecodeError):
        os.remove(f".cache-{SPOTIFY_USER}")
        token = util.prompt_for_user_token(
            SPOTIFY_USER,
            redirect_uri=SPOTIFY_REDIRECT_URI,
            scope=scope,
            client_id=SPOTIFY_CLIENT_ID,
            client_secret=SPOTIFY_CLIENT_SECRET,
        )

    if token:
        spotify = spotipy.Spotify(auth=token)
    else:
        logging.warn(config.spotify_scope_warning)
        raise ValueError(config.spotify_scope_warning)
    return spotify

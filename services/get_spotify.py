import os
import logging
from json.decoder import JSONDecodeError

import config
import spotipy
from spotipy import util


def get_spotify() -> spotipy.Spotify:
    logging.info('get_spotify...')

    token = None
    spotify = None

    try:
        token = util.prompt_for_user_token(
            config.SPOTIFY_USER,
            redirect_uri=config.SPOTIFY_REDIRECT_URI,
            scope=config.scope,
            client_id=config.SPOTIFY_CLIENT_ID,
            client_secret=config.SPOTIFY_CLIENT_SECRET,
        )
    except (AttributeError, JSONDecodeError):
        os.remove(f".cache-{config.SPOTIFY_USER}")
        token = util.prompt_for_user_token(
            config.SPOTIFY_USER,
            redirect_uri=config.SPOTIFY_REDIRECT_URI,
            scope=config.scope,
            client_id=config.SPOTIFY_CLIENT_ID,
            client_secret=config.SPOTIFY_CLIENT_SECRET,
        )

    if token:
        spotify = spotipy.Spotify(auth=token)
    else:
        logging.warn(config.spotify_scope_warning)
        raise ValueError(config.spotify_scope_warning)
    return spotify

import os
from json.decoder import JSONDecodeError

import config
import spotipy
import spotipy.util as util


def get_spotify():
    print("get_spotify...")

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
        print(config.spotify_scope_warning)
    return spotify

import os
import spotipy
import spotipy.util as util
from json.decoder import JSONDecodeError
from config import *


def get_spotify():
    print("get_spotify...")

    try:
        # print(clientId)
        # print(secret)
        token = util.prompt_for_user_token(
            user,
            redirect_uri="http://localhost:8080",
            scope=scope,
            client_id=clientId,
            client_secret=secret,
        )
    except (AttributeError, JSONDecodeError):
        os.remove(f".cache-{user}")
        token = util.prompt_for_user_token(
            user,
            redirect_uri="http://localhost:8080",
            scope=scope,
            client_id=clientId,
            client_secret=secret,
        )

    if token:
        spotify = spotipy.Spotify(auth=token)
        # print(token)
        # print(spotify)
    else:
        print(spotify_scope_warning)
    return spotify

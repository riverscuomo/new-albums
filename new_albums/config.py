"""Configuration using decouple."""
from datetime import datetime
from decouple import config as dconfig

# Config settings from environment variables.
# These are treated as secrets and therefore sourced from environment variables to follow best practices.
PLAYLIST_ID = dconfig("NEW_ALBUMS_PLAYLIST_ID")
SPOTIFY_CLIENT_ID = dconfig("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = dconfig("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = dconfig("SPOTIFY_REDIRECT_URI", default="http://localhost:8080")
SPOTIFY_USER = dconfig("SPOTIFY_USER")
# FIAT_FILE is deprecated
# FIAT_FILE = dconfig("FIAT_FILE", default="_default_fiat")


# The rest are also config settings, but their literal values are commited to the codebase since they aren't secret.

# how spotify formats dates in it's API.
spotify_date_format = "%Y-%m-%dT%H:%M:%S"
# the way I want to see it
date_format = "%Y-%m-%d %A, %I:%M %p"
spotify_scope_warning = "signing into spotify...\nIf this program or another program with the same client_id\nhas changed scopes, you'll need to reauthorize each time.\nMake sure all programs have the same scope."
scope = "playlist-modify-private, playlist-modify-public, user-library-read, playlist-read-private, user-library-modify, user-read-recently-played,user-top-read"
now_utc = datetime.now()
now_local = now_utc.astimezone()
local_offset_str = datetime.strftime(now_local, "%z")
local_offset_int = float(
    local_offset_str[:3] + (".5" if local_offset_str[3] == "3" else ".0")
)

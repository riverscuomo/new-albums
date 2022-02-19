import os
from datetime import datetime

# in spotify result
spotify_date_format = "%Y-%m-%dT%H:%M:%S"

spotify_scope_warning = "signing into spotify...\nIf this program or another program with the same client_id\nhas changed scopes, you'll need to reauthorize each time.\nMake sure all programs have the same scope."
user = os.environ["SPOTIFY_USER"]
scope = "playlist-modify-private, playlist-modify-public, user-library-read, playlist-read-private, user-library-modify, user-read-recently-played"
clientId = os.environ["SPOTIFY_CLIENT_ID"]
secret = os.environ["SPOTIFY_CLIENT_SECRET"]

# the way I want to see it
date_format = "%Y-%m-%d %A, %I:%M %p"

now_utc = datetime.now()
now_local = now_utc.astimezone()
local_offset_str = datetime.strftime(now_local, "%z")
local_offset_int = float(
    local_offset_str[:3] + (".5" if local_offset_str[3] == "3" else ".0")
)

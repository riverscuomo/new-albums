# New Albums

A python script to update a Spotify playlist every day with all the songs from any significant new albums. It shouldn't include single-only releases. Anything older than a month should be deleted.

## Installation

Before you can run the New Albums script, there are some pre-requisites the script assumes.

### Spotify Developer Account

The script will need a Spotify Client Id and Client Secret to interact with Spotify's Web API.

Register for a [developer account](https://developer.spotify.com) on Spotify. After registering, create a new app. Once you create a new app, a Client Id and Client Secret will be generated. You will need these in later steps.

Additionally, the New Albums script uses an Authorization Code Flow. Due to this, you will need to set a redirect URL for your app. To add a redirect URL, open the app's settings. Note: The New Albums script is only intended to run locally, on your machine, so add a redirect link to `http://localhost:8080`.

### Spotify Playlist Id

The script will need the unique ID for one of your playlists. To get the ID for a playlist, in Spotify, right-click on the playlist > Share > Copy Share Link. The link will contain the playlist ID. It is the string between `playlist/` and `?si=`.

### Environment Variables

FIRST SET UP ENVIRONMENT VARIABLES ON YOUR COMPUTER, [SEE HERE FOR INSTRUCTIONS](https://superuser.com/questions/949560/how-do-i-set-system-environment-variables-in-windows-10).

To set all 4 in a one-liner on Windows:

```cmd
set SPOTIFY_CLIENT_ID=xxx && set SPOTIFY_CLIENT_SECRET=xxx && set SPOTIFY_REDIRECT_URI=http://localhost:8080 && set NEW_ALBUMS_PLAYLIST_ID=xxx && set SPOTIFY_USER=xxx
```

To view all currently set environment variables, use the command `set`.

### Set which genres to Reject
Create your own `fiat.py` file inside of the data folder. This is what the script will use to determine which genres to reject from your playlist. You can use the fiat_example as a template.
The `fiat.py` file will be ignored by git.

## Running

Once you have completed all the installation steps, run New Albums script by running `py setup.py`.

### Filter by country

By default, the script will filter by US. To filter by a specific country, you can pass the `--country` flag followed by the country ISO code, e.g. `py setup.py --country JP`

**Options**:
- `py setup.py`: filters by US
- `py setup.py --country GB`: filter by GB
- `py setup.py --country list`: list all available Spotify country codes. The script then prompts you to type an ISO code.
- `py setup.py --country all`: include all country codes (worldwide)

`-c` can also be used as an abbreviation for `--country`, e.g. `py setup.py -c all`

### Filter by top genres

By default, the script will not filter by top genres. To enable this filter, you can pass the `--top-genres` flag, e.g. `py setup.py --top-genres`

`-g` can also be used as an abbreviation for `--top-genres`, e.g. `py setup.py -g`
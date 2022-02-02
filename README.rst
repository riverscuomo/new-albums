A python script to update a Spotify playlist every day with all the songs from any significant new albums. It shouldn't include single-only releases. Anything older than a month should be deleted.  

This project is for me to experiment with open-source collaboration. So please feel free to participate.

FIRST SET UP ENVIRONMENT VARIABLES ON YOUR COMPUTER
https://superuser.com/questions/949560/how-do-i-set-system-environment-variables-in-windows-10


To set all 4 in a one-liner on Windows:
set SPOTIFY_CLIENT_ID=xxx&&set SPOTIFY_CLIENT_SECRET=xxx&&set SPOTIFY_REDIRECT_URI=http://localhost:8080&&set PLAYLIST_ID=xxx&& set SPOTIFY_USER=xxx

To view current environment variables: 
set

I made this package  with the manager Poetry 
https://python-poetry.org/docs/

I believe you can install the dependencies by:
poetry install

The run the program with py setup.py


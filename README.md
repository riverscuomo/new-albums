This project is for me to experiment with open-source collaboration. So please feel free to chime in and participate. If you like, you can join the 'coder' channel on my [discord server](https://discord.gg/mr-rivers-neighborhood).

I've been learning programming since 2015 but I've been mostly working on my own. So my github/collaboration skills are weak. I'd like to learn more about collaboration so I can accomplish more as a programmer through teamwork. One reason I've hesitated so long to try this is I'm worried about accidentally exposing API keys, secrets, credentials, and access to my users' data (not that I have much). So this project will be a first, low-risk, foray into the field of open-source collaboration. If things go well here, maybe I can start to open up some of my other repositiories. I could sure use some help. And I love that thought that some of my programs could be useful to others.

My first goal here is to understand how different developers can work on a codebase together without sharing credentials; to create a program that different people can use with their own credentials. I've attempted this by requiring collaborators (including myself) to use environment variables.

# New Albums

A python script to update a Spotify playlist every day with all the
songs from any significant new albums. It shouldn't include single-only
releases. Anything older than a month should be deleted.

FIRST SET UP ENVIRONMENT VARIABLES ON YOUR COMPUTER, [SEE HERE FOR INSTRUCTIONS](https://superuser.com/questions/949560/how-do-i-set-system-environment-variables-in-windows-10).

To set all 4 in a one-liner on Windows:

```cmd
set SPOTIFY_CLIENT_ID=xxx && set SPOTIFY_CLIENT_SECRET=xxx && set SPOTIFY_REDIRECT_URI=http://localhost:8080 && set PLAYLIST_ID=xxx && set SPOTIFY_USER=xxx
```

To view all currently set environment variables, use the command `set`.

I made this package with the package and dependency manager [Poetry](https://python-poetry.org/docs). Please make sure you [have it installed](https://python-poetry.org/docs/#installation) on your machine before running the New Albums script.

Once you have Poetry installed, run `poetry install` to install all the project's dependencies. After that, run New Albums script by running `poetry run python setup.py`.

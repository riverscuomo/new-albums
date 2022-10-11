class artistClass:
    """Encapsulate a Spotify artist.

    Parameters
    ----------
    artist_id : str
        Artist ID as a URI, URL, or base 64 number.
    spotify : spotipy.client.Spotify
        Spotipy client instance.

    Attributes
    ----------
    name : str
        Artist's name.
    genres: list[str]
        Artist's genres
    """

    def __init__(self, artist_id, spotify):
        # Init elements #
        artist_data = spotify.artist(artist_id)
        self.name = artist_data["name"]
        self.genres = artist_data["genres"]

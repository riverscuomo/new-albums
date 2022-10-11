import logging
from .toolsClass import toolsClass

class userClass :
    """Store user's top genres to use in filtering.

    Parameters
    ----------
    spotify : spotipy.client.Spotify
        Authenicated Spotify client.

    Attributes
    ----------
    spotify : spotipy.client.Spotify
        Authenicated Spotify client.

    genres : list[str]
        User's top genres.
    """

    def __init__(self,spotify):
        # Init elements #
        self.spotify=spotify
        self.genres=[]

    def set_user_top_genres(self):
        """
        Get the top 20 user styles in medium term.
        """

        # Get user top 40 styles #
        top_artist =  self.spotify.current_user_top_artists(40,0,'medium_term')['items']

        genres = []
         # Stores all genres in property genres[]
        for artist in top_artist:
            for genre in artist['genres'] :
                if genre not in genres:
                    self.genres.append(genre)

        # Remove duplicates , function unique in toolsClass.py
        self.genres=toolsClass.unique(self.genres)

        logging.debug(f"[userClass::set_user_top_genres] User's top genres: {self.genres}")

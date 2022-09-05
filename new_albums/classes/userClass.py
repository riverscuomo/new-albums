from .toolsClass import toolsClass

class userClass :

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
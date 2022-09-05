
class artistClass:

    def __init__(self,artist_id,spotify):
        # Init elements #
        artist_data = spotify.artist(artist_id)
        self.name = artist_data['name']
        self.genres = artist_data["genres"]

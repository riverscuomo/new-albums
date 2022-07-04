from classes.artistClass import artistClass
from classes.userClass import userClass
from classes.toolsClass import toolsClass
from data.fiat import reject, accept


class playlistClass:
    def __init__(self, playlistId, spotify):
        # Init elements #
        self.spotify = spotify
        self.accepted = []
        self.rejected_by_genre = []
        self.rejected_by_my_top = []

    def filter_by_fiat(self, new_albums):
        """
        Remove any albums whose first artist's first genre is in reject
        """
        albums = []
        for album in new_albums:

            # Get all artist info and set into variable artist, an instance of artistClass ( artistClass.py )
            artist = artistClass(album["artists"][0]["id"], self.spotify)

            # if len(artist.genres) == 0:
            #     print(f"- [] | {artist.name} ")
            if (
                any(element in reject for element in artist.genres)
                and artist.name not in accept
            ):
                # Check if any of the reject genres array has any of the elements in artist.genres
                album["genres"] = artist.genres
                self.rejected_by_genre.append(album)
            else:
                # Albums that are not rejected
                album["genres"] = artist.genres
                self.accepted.append(album)
            continue
        # Remove duplicates , function unique in toolsClass.py
        return toolsClass.unique(albums)

    def filter_by_your_top_genres(self, new_albums):
        """
        Remove any albums that is not in your top genres
        """
        # Get current user top genres using an instance of userClass ( userClass.py )
        user = userClass(self.spotify)
        user.set_user_top_genres()

        albums = []

        # Check album first artist genres and compare to user top genres
        for album in new_albums:
            in_my_top = False

            # Get first artist genres
            artist = artistClass(album["artists"][0]["id"], self.spotify)
            album["genres"] = artist.genres
            for genre in artist.genres:
                if genre in user.genres:

                    # If is in the list append the album set true to in_my_top and exit the loop
                    albums.append(album)
                    in_my_top = True
                    continue

            if not in_my_top:
                # If it's not in my top append to rejected_by_my_top
                self.rejected_by_my_top.append(album)

        # Remove duplicates , function unique in toolsClass.py
        return toolsClass.unique(albums)

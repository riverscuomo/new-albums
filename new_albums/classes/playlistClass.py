from importlib import import_module
from typing import List, Tuple
import os

from rich import print

from .artistClass import artistClass
from .userClass import userClass
from .toolsClass import toolsClass
from new_albums.config import FIAT_FILE
# from data.fiat import reject, accept


class playlistClass:
    def __init__(self, playlistId, spotify):
        # Init elements #
        self.spotify = spotify
        
        self.accept, self.reject = self.get_accepted_rejected_from_fiat_file(FIAT_FILE)

        self.accepted = []
        self.rejected_by_genre = []
        self.rejected_by_my_top = []
        
    def get_accepted_rejected_from_fiat_file(self, fiat_file: str) -> Tuple[List[str], List[str]]:
        # Parse the accepted / rejected from a Python fiat file
        try:
            mod = import_module("."+fiat_file, package="new_albums")
        except ValueError as e:
            print(f"Error importing from fiat file: {fiat_file} - {e}")     
        
        # Check that the imported module has the expected attributes: reject, accept
        for item in ('accept', 'reject'):
            if not hasattr(mod, item):
                raise ValueError(f"Cannot find {item} list in fiat file")

        return mod.accept, mod.reject

    def filter_by_fiat(self, new_albums):
        """
        Remove any albums whose first artist's first genre is in reject
        """
        albums = []
        for album in new_albums:

            # Get all artist info and set into variable artist, an instance of artistClass ( artistClass.py )
            artist = artistClass(album["artists"][0]["id"], self.spotify)
            album["genres"] = artist.genres

            # If the artist's first genre is in the reject list, reject the album.
            # (This is a little less strict because I was missing some albums I'd like to hear.)
            if artist.genres != [] and (
                any(element in self.reject for element in [artist.genres[0]])
                and artist.name not in self.accept
            ):
                # print(f"Rejected by fiat: {artist.name}")
                self.rejected_by_genre.append(album)

            else:
                # Albums that are not rejected
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

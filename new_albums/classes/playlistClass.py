from importlib import import_module
from typing import List, Tuple, Optional
from pathlib import Path
import logging

from rich import print

from .artistClass import artistClass
from .userClass import userClass
from .toolsClass import toolsClass
from classes.accept_reject import accept_reject_path


class playlistClass:
    """Pending playlist changes.

    Parameters
    ----------
    playlistId : str
        Spotify playlist ID as a URI, URL, or base 64 number.
    spotify : spotipy.client.Spotify
        Authenicated Spotipy client.
    conf_dir : Optional[str | pathlib.Path]
        Path to configuration directory containing "accept.txt" and/or "reject.txt".
        Defaults to XDG_CONFIG_HOME for Unix or APPHOME for Windows.

    Attributes
    ----------
    spotify : spotipy.client.Spotify
        Authenicated Spotipy client.
    accept : list[str]
        Artists to accept from the fiat file.
    reject : list[str]
        Genres to reject from the fiat file.
    accepted : list[dict[str, str | list[str]]]
        Albums accepted by the filters.
    rejected_by_genre : list[dict[str, str | list[str]]]
        Albums rejected by the fiat file.
    rejected_by_my_top : list[dict[str, str | list[str]]]
        Albums rejected by the artist's genres being precluded by the fiat file.
    """

    def __init__(self, playlistId, spotify, conf_dir=None):
        # Init elements #
        self.spotify = spotify
        self.accept, self.reject = self.get_accepted_rejected_from_fiat_file(conf_dir)
        self.accepted = []
        self.rejected_by_genre = []
        self.rejected_by_my_top = []

    def get_accepted_rejected_from_fiat_file(
        self, conf_dir: Optional[Path]
    ) -> Tuple[List[str], List[str]]:
        # Parse the accepted / rejected from accept.txt / reject.txt
        logging.info(f"[playListClass]: Config directory path => {conf_dir}")
        # accept = ["test accept"]
        # reject = ["test reject"]

        # Use conf_dir if present otherwise retrieve a default path.
        conf_dir = conf_dir if conf_dir else accept_reject_path()
        logging.info(f"[playListClass]: Config directory retrieved as => {conf_dir}")
        if conf_dir:
            logging.info(f"[playListClass]: Using config directory => {conf_dir}")
            accept = get_list_from_file(conf_dir.joinpath("accept.txt"))
            reject = get_list_from_file(conf_dir.joinpath("reject.txt"))
            return accept, reject
        else:
            logging.warn("[playListClass]: Not using accept.txt / reject.txt")
            return [], []
        # try:
        #     mod = import_module("."+fiat_file, package="new_albums")
        # except ModuleNotFoundError as e:
        #     logging.critical(f"[playListClass]: Error importing from fiat file: {fiat_file} - {e}")
        #     raise e

        # # Check that the imported module has the expected attributes: reject, accept
        # for item in ('accept', 'reject'):
        #     if not hasattr(mod, item):
        #         logging.critical(f"[playListClass]: {item} not found in {fiat_file}.\nYour fiat file should have two lists: `accept` and `reject`.")
        #         raise ValueError(f"Cannot find {item} list in fiat file")

        # # Check that accept and reject are list.
        # if not isinstance(mod.accept, list) or not isinstance(mod.reject, list):
        #     logging.critical("[playListClass]: `accept` or `reject` is not a list.")
        #     logging.debug(f"[playListClass]:\naccept: {mod.accept}\nreject: {mod.reject}")
        #     raise TypeError("In your fiat file, `accept` and `reject` should be lists of strings.")

        # # Check that accept and reject only consist of strings.
        # if not all(map(lambda x: isinstance(x, str), mod.accept + mod.reject)):
        #     logging.critical("[playListClass]: `accept` or `reject` doesn't consist only of strings.")
        #     logging.debug(f"[playListClass]:\naccept: {mod.accept}\nreject: {mod.reject}")
        #     raise TypeError("Your fiat file's `accept` and `reject` lists should ONLY consist of strings.")

    def filter_by_fiat(self, new_albums):
        """Remove any albums whose first artist's first genre is in reject."""
        albums = []
        for album in new_albums:

            # Get all artist info and set into variable artist, an instance of artistClass ( artistClass.py )
            artist = artistClass(album["artists"][0]["id"], self.spotify)
            album["genres"] = artist.genres

            # If the artist's first genre is in the reject list, reject the album.
            # (This is a little less strict because I was missing some albums I'd like to hear.)
            if artist.genres and (
                any(element in self.reject for element in [artist.genres[0]])
                and artist.name not in self.accept
            ):
                logging.info(
                    f"[playlistClass::filter_by_fiat] Rejected by fiat: {artist.name}"
                )
                self.rejected_by_genre.append(album)

            else:
                # Albums that are not rejected
                self.accepted.append(album)
            continue

        # Remove duplicates , function unique in toolsClass.py
        return toolsClass.unique(albums)

    def filter_by_your_top_genres(self, new_albums):
        """Remove any albums that is not in your top genres."""
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
                logging.info(
                    f"[playlistClass::filter_by_your_top_genres] Rejected by top genres - {album}"
                )
                self.rejected_by_my_top.append(album)

        # Remove duplicates , function unique in toolsClass.py
        return toolsClass.unique(albums)


def get_list_from_file(filename):
    """Get a list of strings from a text file."""
    try:
        with open(filename, "r") as f:
            lines = f.readlines()
        return [line.strip() for line in lines]
    except FileNotFoundError as e:
        return []

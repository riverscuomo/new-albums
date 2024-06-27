"""Convenience classes and tools for Spotipy albums."""

import logging
import itertools
from .playlistClass import playlistClass
# from new_albums.config import FIAT_FILE


def format_album(album):
    """Format a Spotipy album dict into a printable string.

    Parameters
    ----------
    album : dict[str, str | list[str] | list[dict[str, str, list[str]]]]
        Spotipy album dictionary.

    Returns
    -------
    str
        Formatted string.
    """
    return f"{album['name']} {album['genres']} | {album['artists'][0]['name']}"


class albumClass:
    """Helper class to process albums.

    Parameters
    ----------
    spotify : spotipy.client.Spotify
        Authenicated Spotify client.
    fiat_path : Optional[pathlib.Path]
        Path to directory containing accept.txt/reject.txt. Optional.
    limit : int
        Amount of new releases to pull.

    Attributes
    ----------
    spotify : spotipy.client.Spotify
        Authenicated Spotify client.
    fiat_path : Optional[pathlib.Path]
        Directory containing accept.txt/reject.txt.
    limit : int
        Amount of new releases to pull.
    reject_fields : list[str]
        Album keys that aren't important to the script.
    """

    def __init__(self, spotify, fiat_path=None, limit=20):
        # Init elements #
        self.spotify = spotify
        self.fiat_path = fiat_path
        self.limit = limit
        self.reject_fields = [
            "available_markets",
            "external_urls",
            "href",
            "images",
            "album_type",
            "release_date_precision",
            "uri",
            "type",
        ]

    def get_new_album_ids(self, filter_by_your_top_genres, countries):
        """
        Get all the album ids from the last x new albums.
        It doesn't include single-only releases OR any genres you've marked as reject.
        """

        logging.debug(f"[get_new_album_ids]: countries = {countries}")

        # Clean up countries by ensuring they're uppercased
        # countries = (country.upper() for country in countries) if countries else ["US"]

        print("!! The new_releases endpoint stopped working in April, 2024. Computing new album releases from Spotify's New Music Friday playlist instead !!")
        
        # WORKAROUND: get all the tracks from spotify's 'New Music Friday' playlist
        new = self.get_new_albums_from_nmf()
        
        # # Pull new albums and filter on each country
        # new = self.get_new_albums_from_api(countries)

        logging.debug(f"[get_new_albums_ids]: new = {new}")

        # Remove any albums that are single-only
        new_albums = [x for x in new if x["album_type"] == "album"]

        # Remove any fields that we don't need for the rest of the script
        for x in new_albums:
            for f in self.reject_fields:
                x.pop(f, None)

        # Filters the list of albums using an instance of ( playlistClass ), first by user top genres, then by rejects list
        playlist = playlistClass(new_albums, self.spotify, self.fiat_path)

        # If user choose to filter by his top genres then .... FILTER BY YOUR TOP GENRES ( function filter_by_your_top_genres in playlistClass)
        if filter_by_your_top_genres:
            logging.info("[albumClass::get_new_album_ids] Filtering by top genres")
            playlist.filter_by_your_top_genres(new_albums)

        logging.info("[albumClass::get_new_albums_ids] Filtering by fiat")
        playlist.filter_by_fiat(new_albums)

        return playlist

    def get_new_albums_from_api(self, countries):
        """
        Endpoint stopped working in April, 2024. This function is no longer used.
        """
        new = (
            self.spotify.new_releases(limit=self.limit, country=country)["albums"][
                "items"
            ]
            for country in countries
        )

        # Flatten new because it's currently a list of lists
        new = itertools.chain.from_iterable(new)

        # Consume the generators and sort by release date
        new = sorted(new, key=lambda x: x["release_date"], reverse=True)
        return new


    def get_new_albums_from_nmf(self):
        nmf_items = self.spotify.playlist_tracks("37i9dQZF1DX4JAvHpjipBk")["items"]

        new = [item["track"]["album"] for item in nmf_items]
        return new

    def get_track_ids_for_album(self, album_id):
        """
        Get the track ids for a single album.
        """
        logging.debug(
            f"[albumClass::get_new_album_ids] Getting track ids for album {album_id}"
        )
        album = self.spotify.album(album_id)

        logging.debug(album)
        return [x["id"] for x in album["tracks"]["items"]]

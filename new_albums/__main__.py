from new_albums.build_description import build_description
from new_albums.api import get_spotify
from new_albums.classes.albumClass import albumClass, format_album
from new_albums.classes.userClass import userClass
from rich import print
from typing import Iterable
import new_albums
import new_albums.config as config
import os
import importlib
import pycountry
import argparse
import sys
import spotipy
import logging
import _default_fiat


def log(message):
    """User facing log messages.

    Parameters
    ----------
    message : str
        Message to print.

    Returns
    -------
    None
    """
    print("=============================================")
    print(f" {message}")
    print("=============================================")


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments.

    Returns
    -------
    argparse.Namespace
        Parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description="Update a Spotify playlist with new songs from any significant albums.",
        epilog="Check README.md for help setting up the required environment variables.",
    )

    parser.add_argument(
        "-a",
        "--accept-artist",
        help="And artist to your accept list.",
        # nargs="+",
        type=str,
    )

    parser.add_argument(
        "-r",
        "--reject-genre",
        help="And genres to your reject list.",
        # nargs="+",
        type=str,
    )

    parser.add_argument(
        "-c",
        "--country",
        help="Filter by one or more countries using ISO country codes. Default is 'US'. Use 'ALL' for worldwide. Use 'LIST' to list all available countries.",
        nargs="+",
        type=str,
        default=["US"],
    )

    # a boolean kwarg should really just be optional and default to bools in memory, not strings
    parser.add_argument(
        "--top-genres",
        "-g",
        action="store_true",
        help="Allows you to filter by your top genres.",
        default=False,
    )

    parser.add_argument(
        "--fiat",
        "-f",
        help="File to use as fiat data instead of defaults.",
    )

    parser.add_argument(
        "--log",
        "-l",
        help="Set logging granularity. Defaults to 'warning'.",
        choices=["debug", "info", "warning", "error", "critical"],
        default="warning",
    )

    parser.add_argument(
        "--limit",
        "-m",
        help="Number of new releases to return. Default: 20 Max: 50",
        default=20,
        type=int,
    )

    parser.add_argument(
        "--timeout",
        "-t",
        help="Timeout in seconds to wait for responses from Spotify's servers before failing.",
        default=20,
        type=int,
    )

    # Parse and validate arguments
    args = parser.parse_args()
    init_logging(args.log)
    init_fiat(args)

    if args.limit > 50 or args.limit <= 0:
        logging.critical(f"[parse_arguments] Invalid limit: {args.limit}")
        raise ValueError(
            f"--limit should be between 1 and 50 inclusive. Got: {args.limit}."
        )

    return args


def markets(spotify):
    """Fetch and print available markets.

    Spotify requires authenication in order to request the available markets from
    its API.

    Parameters
    ----------
    spotify : spotipy.client.Spotipy
        An authenicated Spotipy instance.

    Returns
    -------
    None
    """
    logging.info("[markets]: Retrieving available markets.")
    available_countries = spotify.available_markets()["markets"]

    log("Spotify is available in...")

    for code in available_countries:
        if pycountry.countries.get(alpha_2=code):
            country_name = pycountry.countries.get(alpha_2=code).name
            print(country_name + " = " + "'" + code + "'")

    log(
        "Rerun the script with the desired country codes; ex. 'US', 'GB', 'JP', 'ES'... "
    )


def parse_country(countries, spotify):
    """Validate the country code argument.

    Parameters
    ----------
    countries : str | list[str]
        The country code(s) passed into the script.
    spotify : spotipy.client.Spotipy
        Authenicated Spotipy client.

    Returns
    -------
    str
        Validated country code.
    """
    logging.debug(f"[parse_country]: Parsing country arguments: {countries}")

    if "ALL" in countries:
        # ALL is worldwide (None)
        logging.info(f"[parse_country] Global country filter")
        return [None]
    elif "LIST" in countries:
        logging.debug("[parse_country]: Asked for list countries.")
        markets(spotify)
        sys.exit(0)
    elif isinstance(countries, Iterable):
        logging.debug("[parse_country]: Validating list of countries")
        all_markets = spotify.available_markets()["markets"]
        for country in countries:
            if country in all_markets:
                logging.info(f"[parse_country] Filtering on country code {country}.")
            else:
                logging.error(f"[parse_country] Invalid country code {country}.")
                raise ValueError(
                    f"Country code {country} is invalid.\nRun the scripts with `-c list` to see the available markets."
                )

        return countries
    else:
        raise ValueError(f"Invalid option passed to -c: {countries}")


def init_logging(log_level):
    """Initialize logging.

    Parameters
    ----------
    log_level : str
        Logging level. Must be one of debug, info, warning, error, or critical.

    Returns
    -------
    None
    """
    # Validate log_level. This code is more or less exactly how the docs handle it.
    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f"`{log_level}` is an invalid log level.")

    # Set requested level as well as a nicer default format.
    logging.basicConfig(
        force=True,
        format="(%(asctime)s (%(levelname)s)) => %(message)s",
        level=numeric_level,
    )

    logging.debug("[init_logging] Logger initialized.")


def init_fiat(args):
    """Dynamically set a fiat file.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed arguments.

    Returns
    -------
    None
    """
    logging.debug(f"[init_fiat] Fiat argument: {args.fiat}")

    if args.fiat:
        logging.info(f"[init_fiat] Using {args.fiat} as a fiat file.")

        # Logic is a bit hacky.
        # The FIAT_FILE env var is overwritten and decouple is reloaded so that it
        # loads the new changes AND sets the global variables.
        # Unfortunately, decouple's config instance is immutable. A cleaner solution
        # requires a larger scale overhaul of the script. This is fine for now.
        os.environ["FIAT_FILE"] = args.fiat
        importlib.reload(config)


def add_to_file(filepath, string):
    with open(filepath, "r") as f:
        lines = f.readlines()
        lines.append(f"{string}\n")
        lines.sort()
    with open(filepath, "w") as f:
        f.writelines(lines)

def main():
    # FOR RIVERS ONLY:
    # Handle the case when this script is called from a manual run of maintanence.py with an argument of 'new_albums'.
    # Even though you have an argparser by a different name, they're both
    # accessing the same sys.argv.
    logging.debug(sys.argv)
    if sys.argv[0] == "maintenance.py":
        sys.argv = ["new_albums.py"]

    logging.debug(sys.argv)

    # Setup and parse arguments
    args = parse_arguments()

    # print(args)

    if args.reject_genre:
        add_to_file(r".\new_albums\reject.txt", args.reject_genre)
    if args.accept_artist:
        add_to_file(r".\new_albums\accept.txt", args.accept_artist)


    filter_by_genre = args.top_genres

    logging.info("[main] Creating Spotipy instance.")

    try:
        spotify = get_spotify(timeout=args.timeout)
    except Exception as e:
        log("Could not get spotify auth. Exiting")
        logging.critical(f"Spotipy error:\n{e}")
        sys.exit(1)

    # Parse country/markets
    # Calls the Spotify API and therefore requires authentication
    countries = [country.upper() for country in args.country]
    logging.debug(f"[main] Countries after upper: {countries}")
    countries = parse_country(countries, spotify)
    logging.debug(f"[main] Countries after parse_country: {countries}")

    album = albumClass(spotify, config.FIAT_FILE, args.limit)

    # Get albums lists
    processed_albums = album.get_new_album_ids(
        countries=countries, filter_by_your_top_genres=filter_by_genre
    )

    track_ids = []

    for album_id in [x["id"] for x in processed_albums.accepted]:
        logging.debug(f"[main] Album id - {album_id}")
        track_ids.extend(album.get_track_ids_for_album(album_id))

    track_id_lists = []

    # split track_ids into lists of size 100
    for i in range(0, len(track_ids), 100):
        track_id_lists.append(track_ids[i : i + 100])

    # Results display screen

    if filter_by_genre:
        log("MY TOP GENRE LIST")

        user = userClass(spotify)
        user.set_user_top_genres()
        print(f"+ {user.genres}")

    log("ACCEPTED")

    for album in processed_albums.accepted:
        print(f"+ {format_album(album)}")

    if filter_by_genre:
        log("REJECTED BECAUSE OF MY TOP GENRE LIST")
        for album in processed_albums.rejected_by_my_top:
            print(f"+ {format_album(album)}")

    log("REJECTED BY GENRE FIAT")
    for album in processed_albums.rejected_by_genre:
        print(f"+ {format_album(album)}")

    # Sending to spotify
    log(f"updating spotify playlist for {config.SPOTIFY_USER}...")

    # empty playlist first
    result = spotify.user_playlist_replace_tracks(
        config.SPOTIFY_USER, config.PLAYLIST_ID, []
    )

    # add all of the sublists of track_id_lists
    result = [
        spotify.user_playlist_add_tracks(
            config.SPOTIFY_USER, config.PLAYLIST_ID, sublist
        )
        for sublist in track_id_lists
    ]

    description = build_description(
        processed_albums.accepted,
        processed_albums.rejected_by_genre + processed_albums.rejected_by_my_top,
    )

    spotify.user_playlist_change_details(
        config.SPOTIFY_USER, config.PLAYLIST_ID, description=description
    )

    print("Done!")
    print(
        f"Feel free to change your always accepted artists and always rejected genres in {config.FIAT_FILE} and run again."
    )

    logging.info(f"Success! {description}")


if __name__ == "__main__":

    main()

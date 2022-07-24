from build_description import build_description
from services.get_spotify import get_spotify
from config import *
from classes.albumClass import albumClass
from classes.userClass import userClass
from rich import print
import pycountry
import argparse


spotify = get_spotify()
parser = argparse.ArgumentParser()


def main():

    # Handle arguments (country, top genres)
    parser.add_argument("-c", "--country",
                        help="Allows you to filter by country using an ISO country code. Default is 'US'. Use 'ALL' for worldwide. Use 'LIST' to list all available countries.", default="US")
    parser.add_argument(
        "-g", "--top-genres", help="Allows you to filter by your top genres.", default="N", nargs="?", const="Y")
    args = parser.parse_args()
    country = args.country.upper()
    filter_by_genre = args.top_genres

    # ALL is worldwide
    if country == "ALL":
        country = None

    # LIST returns all available Spotify countries
    if country == "LIST":
        available_countries = list(spotify.available_markets().values())[0]
        for code in available_countries:
            if pycountry.countries.get(alpha_2=code):
                country_name = pycountry.countries.get(alpha_2=code).name
                print(country_name + " = " + "'" + code + "'")

        print("=============================================")
        print(" TYPE COUNTRY CODE, ex. 'US', 'GB', 'JP', 'ES'... ")
        print("=============================================")
        country = input().upper()

    print("new_albums.setup main...")
    print("=============================================")

    album = albumClass(spotify)

    # Get albums lists
    processed_albums = album.get_new_album_ids(country, filter_by_genre)

    track_ids = []

    for album_id in [x["id"] for x in processed_albums.accepted]:
        # print(album_id)
        track_ids.extend(album.get_track_ids_for_album(album_id))

    track_id_lists = []

    # split track_ids into lists of size 100
    for i in range(0, len(track_ids), 100):
        track_id_lists.append(track_ids[i : i + 100])

    # Results display screen

    # if filter_by_genre.upper() == "Y":
    #     print("=============================================")
    #     print(" MY TOP GENRE LIST")
    #     print("=============================================")

    #     user = userClass(spotify)
    #     user.set_user_to
    # from data import fiatp_genres()
    #     print(f"+ {user.genres}")

    print("=============================================")
    print(" ACCEPTED")
    print("=============================================")

    for album in processed_albums.accepted:
        print(f"+ {album['name']} {album['genres']} | {album['artists'][0]['name']}")

    # if filter_by_genre.upper() == "Y":
    #     print("=============================================")
    #     print(" REJECTED BECAUSE OF MY TOP GENRE LIST")
    #     print("=============================================")
    #     for album in processed_albums.rejected_by_my_top:
    #         print(
    #             f"+ {album['name']} {album['genres']} | {album['artists'][0]['name']}"
    #         )

    print("=============================================")
    print(" REJECTED BY GENRE FIAT")
    print("=============================================")
    for album in processed_albums.rejected_by_genre:
        print(f"+ {album['name']} {album['genres']} | {album['artists'][0]['name']}")

    # Sending to spotify

    # print(result)

    print("=============================================")
    print(f"updating spotify playlist for {SPOTIFY_USER}...")

    # empty playlist first
    result = spotify.user_playlist_replace_tracks(SPOTIFY_USER, PLAYLIST_ID, [])

    # add all of the sublists of track_id_lists
    for sublist in track_id_lists:
        result = spotify.user_playlist_add_tracks(SPOTIFY_USER, PLAYLIST_ID, sublist)

    description = build_description(processed_albums.accepted)

    spotify.user_playlist_change_details(
        SPOTIFY_USER, PLAYLIST_ID, description=description
    )

    print("Done!")
    print(
        "Feel free to change your always accepted artists and always rejected genres in data.fiat.py and run again."
    )

    return f"Success! {description}"


if __name__ == "__main__":

    main()

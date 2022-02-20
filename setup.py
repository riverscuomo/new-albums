import random

import config
from services.get_spotify import get_spotify

spotify = get_spotify()


def get_spotify_songs_from_playlist(
    playlistId, desired_quantity, skip_recents=None, name=""
):

    """
    This function will return a list of track ids from a playlist.
    I'm not sure we'll need it for this program, but it's been very useful in the past.
    """

    playlist = {"id": playlistId, "quantity": desired_quantity}

    print(
        f"\n - returning {desired_quantity} SPOTIFY track IDs for the spotify playlist '{name}' with ID: {playlistId}"
    )
    # print(spotify)

    # get the results for every song in the playlist
    results = spotify.user_playlist_tracks(config.SPOTIFY_USER, playlist["id"])
    # print(results)
    tracks = results["items"]
    while results["next"]:
        results = spotify.next(results)
        tracks.extend(results["items"])

    # pprint(tracks[:2])

    track_ids = []
    for x in tracks:
        track = x["track"]
        if track is None:
            print("TRACK IS NONE!")
            continue
        try:
            id = track["id"]
        except:
            print(track)
        track_ids.append(id)
    # # extract the trackids for every song in the playlist from results
    # [x["track"]["id"] for x in tracks]
    # # print(len(track_ids))

    # If you've passed a list of recently played track ids to skip
    if skip_recents != None:
        track_ids = [x for x in track_ids if x not in skip_recents]
    print(len(track_ids))

    # If there are still more track ids than you want to pull from this playlist,
    # take a random sample.
    if len(track_ids) > desired_quantity:
        track_ids = random.sample(track_ids, int(desired_quantity))

    # if name == "sparks":

    # print(track_ids)
    # exit()

    return track_ids


def get_track_ids():
    """
    TO DO:
    Get all the track ids from any significant new albums. It shouldn't include single-only releases.

    """
    new = spotify.new_releases(limit=10)
    print(new)

    return ["4cOdK2wGLETKBW3PvgPWqT"]


def main():

    print("new_albums.setup main...")

    track_ids = get_track_ids()

    # TODO:
    # Anything older than a month should be deleted.

    random.shuffle(track_ids)

    print("updating spotify playlist")
    # result = spotify.user_playlist_replace_tracks(
    #     config.SPOTIFY_USER, config.PLAYLIST_ID, track_ids
    # )
    # print(result)

    # # change the playlist description to a random fact
    # post_description(job)


if __name__ == "__main__":

    main()

from classes.artistClass import artistClass
from classes.userClass import userClass
from classes.toolsClass import toolsClass
from data.rejects import rejects, exceptions

class playlistClass :

    def __init__(self,playlistId,spotify):
        # Init elements #
        self.spotify = spotify
        self.accepted = []
        self.rejected_by_genre = []
        self.rejected_by_my_top = []


    # THIS FUNCTION IS NEVER USED #
    def get_spotify_songs_from_playlist(self,
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



    def remove_rejects(self,new_albums):
        """
        Remove any albums whose first artist's first genre is in rejects
        """
        albums = []
        for album in new_albums:

            # Get all artist info and set into variable artist, an instance of artistClass ( artistClass.py )
            artist = artistClass(album["artists"][0]['id'],self.spotify)

            # print(artist["name"],  artist["genres"])

            if len(artist.genres) == 0 :
                print(f"- [] | {artist.name} ")
                continue
            elif any(element in rejects for element in artist.genres) and artist.name not in exceptions :
               # Check if any of the reject genres array has any of the elements in artist.genres
                album['genres']=artist.genres
                self.rejected_by_genre.append(album)
                continue
            else:
                # Albums that are not rejected
                album['genres']=artist.genres
                self.accepted.append(album)
                continue

        # Remove duplicates , function unique in toolsClass.py
        return toolsClass.unique(albums)


    def filter_by_your_top_genres(self,new_albums):
        """
        Remove any albums that is not in your top genres
        """
        # Get current user top genres using an instance of userClass ( userClass.py )
        user = userClass(self.spotify)
        user.set_user_top_genres()

        albums=[]

        # Check album first artist genres and compare to user top genres
        for album in new_albums:
            in_my_top = False

            # Get first artist genres
            artist = artistClass(album["artists"][0]['id'],self.spotify)
            album['genres']=artist.genres
            for genre in artist.genres:
                if genre in user.genres:

                    # If is in the list append the album set true to in_my_top and exit the loop
                    albums.append(album)
                    in_my_top = True
                    continue

            if not in_my_top :
                # If it's not in my top append to rejected_by_my_top
                self.rejected_by_my_top.append(album)

        # Remove duplicates , function unique in toolsClass.py
        return toolsClass.unique(albums)
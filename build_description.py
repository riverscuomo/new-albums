from typing import List 

from classes.albumClass import albumClass

def build_description(accepted_albums: List[albumClass]) -> str:
    description = []

    for album in accepted_albums:
        album_description = f'{ album["artists"][0]["name"] } "{album["name"]} "'
        description.append(album_description)
    return ', '.join(description)

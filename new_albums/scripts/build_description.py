from typing import List

from new_albums.classes.albumClass import albumClass


def build_description(
    accepted_albums: List[albumClass], rejected_albums: List[albumClass]
) -> str:
    description = ""
    if accepted_albums:
        items = collect_items(accepted_albums)
        description = ", ".join(items)

    if rejected_albums:

        items = items = collect_items(rejected_albums)
        description += " REJECTED: " + ", ".join(items)

    return description


def collect_items(albums: List[albumClass]) -> List[str]:
    items = []
    for album in albums:
        # Handle artists with no genres
        top_genre = album["genres"][0] if album["genres"] else "''"
        item = f'{ album["artists"][0]["name"] } ({top_genre})'
        items.append(item)
    return items

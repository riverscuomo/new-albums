from typing import List
from new_albums.classes.albumClass import albumClass

def build_description(
    accepted_albums: List[albumClass], rejected_albums: List[albumClass]
) -> tuple[str, str]:
    """
    Builds two descriptions: one for Spotify (truncated) and one for the spreadsheet (full)
    
    Returns:
    tuple[str, str]: (spotify_description, spreadsheet_description)
    """
    description = ""
    if accepted_albums:
        items = collect_items(accepted_albums)
        description = ", ".join(items)
    if rejected_albums:
        items = items = collect_items(rejected_albums)
        description += " REJECTED: " + ", ".join(items)

    # Create truncated version for Spotify
    MAX_DESCRIPTION_LENGTH = 297  # 300 - 3 for the ellipsis
    spotify_description = (
        f"{description[:MAX_DESCRIPTION_LENGTH]}..."
        if len(description) > MAX_DESCRIPTION_LENGTH
        else description
    )
    
    # Return both versions
    return spotify_description, description

def collect_items(albums: List[albumClass]) -> List[str]:
    items = []
    for album in albums:
        # Handle artists with no genres
        top_genre = album["genres"][0] if album["genres"] else "''"
        item = f'{ album["artists"][0]["name"] } ({top_genre})'
        items.append(item)
    return items

# from typing import List

# from new_albums.classes.albumClass import albumClass


# def build_description(
#     accepted_albums: List[albumClass], rejected_albums: List[albumClass]
# ) -> str:
#     description = ""
#     if accepted_albums:
#         items = collect_items(accepted_albums)
#         description = ", ".join(items)

#     if rejected_albums:

#         items = items = collect_items(rejected_albums)
#         description += " REJECTED: " + ", ".join(items)

#     MAX_DESCRIPTION_LENGTH = 297  # 300 - 3 for the ellipsis
#     truncated_description = (
#         f"{description[:MAX_DESCRIPTION_LENGTH]}..."
#         if len(description) > MAX_DESCRIPTION_LENGTH
#         else description
#     )


#     return truncated_description


# def collect_items(albums: List[albumClass]) -> List[str]:
#     items = []
#     for album in albums:
#         # Handle artists with no genres
#         top_genre = album["genres"][0] if album["genres"] else "''"
#         item = f'{ album["artists"][0]["name"] } ({top_genre})'
#         items.append(item)
#     return items

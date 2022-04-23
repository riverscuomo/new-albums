def build_description(accepted_albums):
    description = ""

    for album in accepted_albums:
        description += f"{album['artists'][0]['name']} "
        description += '"'
        description += f"{album['name']} "
        description += '", '
    return description
